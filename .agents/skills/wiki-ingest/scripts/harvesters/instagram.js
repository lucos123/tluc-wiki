async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const startedAt = Date.now();
  const MAX_TOTAL_MS = 38000;

  const loginForm = document.querySelector('input[name="username"], form[id*="loginForm"]');
  const postRoot =
    document.querySelector("article") ||
    document.querySelector('main [role="presentation"]') ||
    document.querySelector("main") ||
    document.body;

  if (loginForm && !postRoot?.querySelector("img")) {
    return { platform: "instagram", status: "blocked", url: location.href, reason: "Instagram login wall" };
  }

  const shortcodeMatch = location.pathname.match(/\/(?:p|reels?|tv)\/([A-Za-z0-9_-]{5,})/);
  const shortcode = shortcodeMatch ? shortcodeMatch[1] : null;

  // Expand caption if truncated
  const moreBtn = Array.from(postRoot.querySelectorAll('span, button, div[role="button"]'))
    .find((el) => /^(more|xem thêm)$/i.test((el.textContent || "").trim()));
  if (moreBtn) {
    try { moreBtn.click(); await sleep(300); } catch {}
  }

  // Comma-safe srcset parser (handles CDN URLs with embedded commas)
  const pickBestSrc = (img) => {
    if (img.srcset) {
      const parts = img.srcset.trim().split(/,\s+(?=(?:https?:\/\/|\/|data:))/);
      let bestUrl = "";
      let bestScore = -1;
      for (const part of parts) {
        const seg = part.trim().split(/\s+/);
        if (!seg[0] || seg[0].startsWith("data:")) continue;
        let score = 0;
        if (seg[1]) {
          if (seg[1].endsWith("w")) score = parseInt(seg[1], 10) || 0;
          else if (seg[1].endsWith("x")) score = Math.round((parseFloat(seg[1]) || 0) * 1000);
        }
        if (score >= bestScore) {
          bestScore = score;
          bestUrl = seg[0];
        }
      }
      if (bestUrl) {
        try { return new URL(bestUrl, location.href).href; } catch { return bestUrl; }
      }
    }
    return img.currentSrc || img.src || "";
  };

  // Rewind to slide 1 if opened mid-carousel (e.g., ?img_index=5)
  let rewound = 0;
  while (rewound < 25 && Date.now() - startedAt < 8000) {
    const prevBtn = postRoot.querySelector(
      'button[aria-label="Go Back"], button[aria-label="Previous"], button[aria-label="Quay lại"], button[aria-label="Trước"]'
    );
    if (!prevBtn || prevBtn.disabled) break;
    prevBtn.click();
    rewound++;
    await sleep(220);
  }
  if (rewound > 0) await sleep(350);

  // Scope strictly inside primary post carousel/media stage and exclude "More posts from @author" links
  const mediaScope = postRoot.querySelector("ul li img") ? postRoot.querySelector("ul") : postRoot;
  const collectVisibleImgs = () => {
    const imgs = Array.from(mediaScope.querySelectorAll("img")).filter((img) => {
      const link = img.closest('a[href*="/p/"], a[href*="/reel/"], a[href*="/reels/"]');
      if (link && shortcode && !link.href.includes(shortcode)) return false;
      const r = img.getBoundingClientRect();
      const src = img.currentSrc || img.src || "";
      return (
        r.width >= 240 &&
        r.height >= 240 &&
        r.bottom > 0 &&
        r.top < window.innerHeight + 180 &&
        src.startsWith("http") &&
        !src.includes("s150x150") &&
        !src.includes("s320x320")
      );
    });
    imgs.sort((a, b) => a.getBoundingClientRect().left - b.getBoundingClientRect().left);
    return imgs.map((img) => ({
      src: pickBestSrc(img),
      dims: img.naturalWidth ? `${img.naturalWidth}x${img.naturalHeight}` : "unknown",
      alt: img.alt || "",
      note: "",
    }));
  };

  const ordered = [];
  const seenPath = new Set();
  const keyOf = (url) => {
    try { return new URL(url).pathname; } catch { return url; }
  };
  const recordCurrent = () => {
    let added = 0;
    for (const item of collectVisibleImgs()) {
      const k = keyOf(item.src);
      if (!seenPath.has(k)) {
        seenPath.add(k);
        ordered.push({ index: ordered.length + 1, ...item });
        added++;
      }
    }
    return added;
  };

  recordCurrent();
  let stepsClicked = 0;
  let staleSteps = 0;
  while (Date.now() - startedAt < MAX_TOTAL_MS && stepsClicked < 35) {
    const nextBtn = postRoot.querySelector(
      'button[aria-label="Next"], button[aria-label="Tiếp"], button[aria-label="Go Forward"], [aria-label="Go Forward"]'
    );
    if (!nextBtn || nextBtn.disabled) break;
    nextBtn.click();
    stepsClicked++;

    let added = 0;
    for (let poll = 0; poll < 4; poll++) {
      await sleep(220);
      added += recordCurrent();
      if (added > 0) break;
    }
    staleSteps = added === 0 ? staleSteps + 1 : 0;
    if (staleSteps >= 3) break;
  }

  const getMeta = (prop) =>
    document.querySelector(`meta[property="${prop}"], meta[name="${prop}"]`)?.getAttribute("content") || "";

  const times = Array.from(postRoot.querySelectorAll("time[datetime]")).map((t) => ({
    datetime: t.getAttribute("datetime"),
    title: t.getAttribute("title"),
    text: (t.textContent || "").trim(),
    href: t.closest("a")?.getAttribute("href") || null,
  }));
  const postTime =
    times.find((t) => t.href && (t.href.includes("/p/") || t.href.includes("/reel/"))) ||
    times[times.length - 1] ||
    times[0] ||
    null;

  const ogDesc = getMeta("og:description") || getMeta("description");
  const ogTitle = getMeta("og:title");
  const authorFromOg = ogTitle ? ogTitle.split(/\s+(?:on|trên)\s+Instagram/i)[0].trim() : null;

  const coAuthors = Array.from(postRoot.querySelectorAll("header a[href]"))
    .map((a) => (a.textContent || "").trim())
    .filter((t) => t && !t.includes(" ") && t.length < 40);

  const reserved = new Set(["p", "reel", "reels", "tv", "stories", "explore", "accounts"]);
  const handleMatch = (getMeta("og:url") || location.href).match(/instagram\.com\/([^/]+)\//);
  const rawHandle = handleMatch && !reserved.has(handleMatch[1].toLowerCase()) ? handleMatch[1] : coAuthors[0] || null;

  const captionNode = postRoot.querySelector("h1");
  const captionText = captionNode ? captionNode.innerText.trim() : ogDesc;
  const videosFound = Array.from(postRoot.querySelectorAll("video"))
    .map((v) => v.currentSrc || v.src)
    .filter(Boolean);

  return {
    platform: "instagram",
    status: "ok",
    url: location.href,
    canonical_url: getMeta("og:url") || location.href.split("?")[0],
    author: authorFromOg || rawHandle,
    handle: rawHandle ? `@${rawHandle.replace(/^@/, "")}` : null,
    co_authors: [...new Set(coAuthors)],
    published: postTime ? postTime.datetime : null,
    engagement: { meta_summary: ogDesc },
    text: captionText,
    comments: [],
    external_links: Array.from(postRoot.querySelectorAll('a[href^="http"]'))
      .map((a) => a.href)
      .filter((h) => !h.includes("instagram.com")),
    videos_found: videosFound,
    rewound_steps: rewound,
    steps_clicked: stepsClicked,
    elapsed_ms: Date.now() - startedAt,
    total_slides: ordered.length,
    slides: ordered,
  };
}
