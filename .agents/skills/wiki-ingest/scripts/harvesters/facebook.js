async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const startedAt = Date.now();
  const urlObj = new URL(location.href);
  const extractFbid = (href) => {
    try {
      const u = new URL(href);
      const q = u.searchParams.get("fbid");
      if (q) return q;
      const m = u.pathname.match(/\/photos\/(?:[^/]+\/)?(\d{6,})/);
      if (m) return m[1];
    } catch {}
    return null;
  };
  const inPhotoViewer =
    location.pathname.includes("/photo") ||
    location.pathname.includes("/photos/") ||
    urlObj.searchParams.has("fbid");

  const bodyText = (document.body?.innerText || "").slice(0, 1500);
  const hasLoginWall =
    !!document.querySelector('form[action*="login"] input[name="pass"]') &&
    !document.querySelector('[role="main"] [dir="auto"], img[data-visualcompletion="media-vc-image"]');
  if (hasLoginWall && /(log in|đăng nhập)/i.test(bodyText)) {
    return { platform: "facebook", status: "blocked", url: location.href, reason: "Facebook login wall" };
  }

  const getVisibleStageImg = () => {
    const candidates = Array.from(
      document.querySelectorAll('img[data-visualcompletion="media-vc-image"], [role="main"] img[src*="scontent"], img[src*="scontent"]')
    ).filter((el) => {
      const r = el.getBoundingClientRect();
      const st = getComputedStyle(el);
      return r.width > 200 && r.height > 200 && st.display !== "none" && st.visibility !== "hidden" && st.opacity !== "0";
    });
    candidates.sort((a, b) => {
      const ra = a.getBoundingClientRect();
      const rb = b.getBoundingClientRect();
      return rb.width * rb.height - ra.width * ra.height;
    });
    return candidates[0] || null;
  };

  const srcKey = (src) => {
    try { return new URL(src).pathname; } catch { return src || ""; }
  };

  if (inPhotoViewer) {
    const MAX_TOTAL_MS = 40000;
    const PER_SLIDE_MS = 1800;
    const snap = () => {
      const img = getVisibleStageImg();
      const src = img ? img.currentSrc || img.src : null;
      const fbid = extractFbid(location.href) || (src ? srcKey(src) : null);
      return {
        fbid,
        src,
        dims: img && img.naturalWidth ? `${img.naturalWidth}x${img.naturalHeight}` : "unknown",
        alt: img?.alt || "",
        note: "",
      };
    };

    const slides = [];
    const seen = new Set();
    let cur = snap();
    if (!cur.fbid || !cur.src) {
      return {
        platform: "facebook",
        status: "partial",
        in_photo_viewer: true,
        url: location.href,
        error: "Stage image or fbid not found",
        total_slides: 0,
        slides: [],
      };
    }
    seen.add(cur.fbid);
    slides.push({ index: 1, ...cur });

    while (Date.now() - startedAt < MAX_TOTAL_MS && slides.length < 40) {
      const prevFbid = cur.fbid;
      const prevSrc = cur.src;
      const nextBtn = Array.from(
        document.querySelectorAll(
          '[aria-label="Next photo"], [aria-label="Ảnh tiếp theo"], [aria-label="Next"], [aria-label="Tiếp"]'
        )
      ).find((el) => {
        const r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0 && !el.disabled;
      });
      if (!nextBtn) break;
      nextBtn.click();

      const stepStart = Date.now();
      let updated = null;
      while (Date.now() - stepStart < PER_SLIDE_MS) {
        await sleep(80);
        const probe = snap();
        if (probe.fbid && probe.fbid !== prevFbid && probe.src && probe.src !== prevSrc) {
          updated = probe;
          break;
        }
      }
      if (!updated) updated = snap();
      if (!updated.fbid || !updated.src || seen.has(updated.fbid)) break;
      seen.add(updated.fbid);
      cur = updated;
      slides.push({ index: slides.length + 1, ...cur });
    }

    const sideText = (document.querySelector('[role="complementary"], [role="dialog"]')?.innerText || "").slice(0, 4000);
    return {
      platform: "facebook",
      status: "ok",
      in_photo_viewer: true,
      url: location.href,
      canonical_url: location.href,
      elapsed_ms: Date.now() - startedAt,
      sidebar_text: sideText,
      total_slides: slides.length,
      slides,
    };
  }

  // On post view: expand "See more" / "Xem thêm" inside main post container first
  const main = document.querySelector('[role="main"], [role="dialog"]') || document.body;
  for (const btn of Array.from(main.querySelectorAll('[role="button"], button, span'))) {
    const txt = (btn.textContent || "").trim();
    if (/^(See more|Xem thêm)$/i.test(txt) && !btn.closest('[role="article"][aria-label*="Comment"], [role="article"][aria-label*="Bình luận"]')) {
      try { btn.click(); } catch {}
    }
  }
  await sleep(350);

  const isCommentEl = (el) =>
    !!el.closest('[role="article"][aria-label*="Comment"], [role="article"][aria-label*="Bình luận"]');

  const authorLink = main.querySelector('h2 a, h3 a, strong a[href*="facebook.com"]');
  const msgNodes = Array.from(main.querySelectorAll('[data-ad-preview="message"], [data-ad-comet-preview="message"]'))
    .filter((n) => !isCommentEl(n));
  const textBlocks = msgNodes.length
    ? msgNodes.map((n) => n.innerText.trim())
    : Array.from(main.querySelectorAll('div[dir="auto"]'))
        .filter((n) => !isCommentEl(n))
        .map((n) => n.innerText.trim())
        .filter((t) => t.length > 25);

  const postText = [...new Set(textBlocks)].join("\n\n").slice(0, 15000);
  const externalLinks = Array.from(main.querySelectorAll('a[href^="http"]'))
    .filter((a) => !isCommentEl(a))
    .map((a) => a.href)
    .filter((h) => !h.includes("facebook.com/login") && !h.includes("/photo") && !h.includes("hashtag/"))
    .filter((v, i, arr) => arr.indexOf(v) === i)
    .slice(0, 20);

  const photoLinks = Array.from(main.querySelectorAll('a[href*="/photo"], a[href*="/photos/"]'))
    .filter((a) => !isCommentEl(a) && !a.closest('[role="banner"]'))
    .map((a) => a.href)
    .filter((v, i, arr) => arr.indexOf(v) === i);

  const seenInline = new Set();
  const inlineImgs = [];
  for (const img of Array.from(main.querySelectorAll('img[src*="scontent"]'))) {
    if (isCommentEl(img) || img.closest('[role="banner"]')) continue;
    const r = img.getBoundingClientRect();
    if (r.width < 200 || r.height < 200) continue;
    const src = img.currentSrc || img.src;
    const k = srcKey(src);
    if (seenInline.has(k)) continue;
    seenInline.add(k);
    inlineImgs.push({
      index: inlineImgs.length + 1,
      src,
      dims: img.naturalWidth ? `${img.naturalWidth}x${img.naturalHeight}` : "unknown",
      alt: img.alt || "",
      note: "",
    });
  }

  const timeCandidate =
    document.querySelector('meta[property="article:published_time"]')?.getAttribute("content") ||
    main.querySelector('abbr[data-utime]')?.innerText?.trim() ||
    Array.from(main.querySelectorAll('a[href*="/posts/"], a[href*="/permalink/"], a[href*="story_fbid"]'))
      .map((a) => (a.getAttribute("aria-label") || a.innerText || "").trim())
      .find((t) => t && t.length <= 45) ||
    null;

  const commentEls = Array.from(
    main.querySelectorAll('[role="article"][aria-label*="Comment"], [role="article"][aria-label*="Bình luận"]')
  );
  const comments = commentEls.slice(0, 15).map((el) => el.innerText.trim()).filter(Boolean);

  return {
    platform: "facebook",
    status: photoLinks.length > 1 ? "needs_gallery_open" : "ok",
    in_photo_viewer: false,
    url: location.href,
    canonical_url: document.querySelector('link[rel="canonical"]')?.href || location.href,
    author: authorLink ? authorLink.innerText.trim() : null,
    handle: authorLink ? authorLink.href : null,
    published: timeCandidate,
    engagement: {
      raw_snippet: Array.from(main.querySelectorAll('[role="button"], span'))
        .map((el) => el.innerText.trim())
        .filter((t) => /(reactions?|likes?|comments?|shares?|lượt chia sẻ|bình luận)/i.test(t) && t.length < 80)
        .slice(0, 8),
    },
    text: postText,
    comments,
    external_links: externalLinks,
    first_photo_href: photoLinks[0] || null,
    photo_link_count: photoLinks.length,
    total_slides: inlineImgs.length,
    slides: inlineImgs,
  };
}
