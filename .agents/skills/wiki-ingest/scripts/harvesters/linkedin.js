async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const startedAt = Date.now();

  if (location.pathname.includes("/authwall") || location.pathname.includes("/uas/login")) {
    return { platform: "linkedin", status: "blocked", url: location.href, reason: "LinkedIn authwall" };
  }

  // Parse JSON-LD (present on public LinkedIn post URLs with exact ISO date & full text)
  let ldData = {};
  for (const s of Array.from(document.querySelectorAll('script[type="application/ld+json"]'))) {
    try {
      const parsed = JSON.parse(s.textContent || "{}");
      const items = Array.isArray(parsed) ? parsed : (Array.isArray(parsed?.["@graph"]) ? parsed["@graph"] : [parsed]);
      const hit = items.find((it) => /SocialMediaPosting|Article|DiscussionForumPosting/i.test(String(it["@type"] || "")));
      if (hit) {
        ldData = hit;
        break;
      }
    } catch {}
  }

  // Scope strictly to the primary post container (both logged-in feed card and public post page)
  const main =
    document.querySelector(".feed-shared-update-v2, article.main-feed-activity-card, article[data-urn], main article, main") ||
    document.body;

  // Expand "see more" ONLY on expand buttons inside primary post (never click unrelated <a> navigation links)
  for (const btn of Array.from(main.querySelectorAll("button, [role='button']"))) {
    const txt = (btn.textContent || "").trim();
    if (/^(see more|…see more|\.\.\.see more|xem thêm)$/i.test(txt)) {
      try { btn.click(); } catch {}
    }
  }
  await sleep(300);

  const authorNode = main.querySelector(
    '.update-components-actor__title span[dir="ltr"] span[aria-hidden="true"], ' +
    '.update-components-actor__name span[aria-hidden="true"], ' +
    '.update-components-actor__name span, ' +
    'a[data-tracking-control-name*="actor-name"], ' +
    '.base-main-feed-card__title'
  );
  const headlineNode = main.querySelector(".update-components-actor__description, .base-main-feed-card__subtitle");
  const publishedNode = main.querySelector(
    '.update-components-actor__sub-description span[aria-hidden="true"], ' +
    '.update-components-actor__sub-description, ' +
    'time[datetime], time'
  );
  const textNode = main.querySelector(
    '.update-components-text, .feed-shared-update-v2__description, .attributed-text-segment-list__content, [data-test-id="main-feed-activity-card__commentary"]'
  );
  const postText = (textNode ? textNode.innerText.trim() : "") || ldData.articleBody || "";

  // Step through inline LinkedIn document/carousel if same-origin DOM slides exist
  const slides = [];
  const seen = new Set();
  const collectImgs = () => {
    let added = 0;
    for (const img of Array.from(main.querySelectorAll("img"))) {
      if (img.closest(".update-components-actor__avatar, .comments-comments-list, aside")) continue;
      const r = img.getBoundingClientRect();
      const src = img.currentSrc || img.src || img.getAttribute("data-delayed-url") || img.getAttribute("data-src") || "";
      if (
        r.width >= 220 &&
        r.height >= 180 &&
        src.startsWith("http") &&
        !src.includes("profile-displayphoto") &&
        !src.includes("company-logo")
      ) {
        const key = src.split("?")[0];
        if (!seen.has(key)) {
          seen.add(key);
          slides.push({
            index: slides.length + 1,
            src,
            dims: img.naturalWidth ? `${img.naturalWidth}x${img.naturalHeight}` : "unknown",
            alt: img.alt || "",
            note: "",
          });
          added++;
        }
      }
    }
    return added;
  };

  collectImgs();
  let carouselSteps = 0;
  let staleSteps = 0;
  while (Date.now() - startedAt < 25000 && carouselSteps < 30) {
    const nextBtn = main.querySelector(
      '.ssplayer-carousel__next-btn:not([disabled]), ' +
      'button[aria-label*="Next page"]:not([disabled]), ' +
      'button[aria-label*="next slide"]:not([disabled]), ' +
      'button.carousel-next-btn:not([disabled])'
    );
    if (!nextBtn) break;
    nextBtn.click();
    carouselSteps++;
    await sleep(450);
    const added = collectImgs();
    staleSteps = added === 0 ? staleSteps + 1 : 0;
    if (staleSteps >= 3) break;
  }

  const docIframe = main.querySelector('iframe[src*="document"], iframe[src*="licdn"], iframe[src*="slideshare"]');
  const externalLinks = Array.from(main.querySelectorAll('a[href^="http"]'))
    .filter((a) => !a.closest(".comments-comments-list, aside"))
    .map((a) => a.href)
    .filter((h) => !h.includes("linkedin.com/in/") && !h.includes("linkedin.com/company/") && !h.includes("linkedin.com/feed/hashtag"))
    .filter((v, i, a) => a.indexOf(v) === i)
    .slice(0, 20);

  const comments = Array.from(main.querySelectorAll('.comments-comment-item__main-content, [data-test-id="comments-comment-item__main-content"]'))
    .slice(0, 10)
    .map((c) => c.innerText.trim())
    .filter(Boolean);

  const ldAuthor = Array.isArray(ldData.author) ? ldData.author[0]?.name : ldData.author?.name;
  const publishedVal =
    ldData.datePublished ||
    publishedNode?.getAttribute?.("datetime") ||
    (publishedNode ? publishedNode.innerText.replace(/\s+/g, " ").trim() : null);

  return {
    platform: "linkedin",
    status: "ok",
    url: location.href,
    canonical_url: document.querySelector('link[rel="canonical"]')?.href || location.href.split("?")[0],
    author: (authorNode ? authorNode.innerText.trim() : null) || ldAuthor || null,
    author_headline: headlineNode ? headlineNode.innerText.replace(/\s+/g, " ").trim() : null,
    handle: main.querySelector('.update-components-actor__container-link, a[data-tracking-control-name*="actor-name"]')?.href || null,
    published: publishedVal,
    engagement: {
      social_counts: main.querySelector('.social-details-social-counts, [data-test-id="social-actions__reaction-count"]')?.innerText?.replace(/\s+/g, " ")?.trim() || null,
    },
    text: postText,
    comments,
    external_links: externalLinks,
    document_iframe_url: docIframe ? docIframe.src : null,
    carousel_steps: carouselSteps,
    total_slides: slides.length,
    slides,
  };
}
