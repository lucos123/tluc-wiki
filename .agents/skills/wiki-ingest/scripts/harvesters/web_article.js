async () => {
  const getMeta = (name) =>
    document.querySelector(`meta[property="${name}"], meta[name="${name}"]`)?.getAttribute("content") || "";

  // Parse JSON-LD including @graph wrappers (WordPress/Yoast, Ghost, Substack, Medium)
  let ldData = {};
  for (const s of Array.from(document.querySelectorAll('script[type="application/ld+json"]'))) {
    try {
      const parsed = JSON.parse(s.textContent || "{}");
      const items = Array.isArray(parsed)
        ? parsed
        : (Array.isArray(parsed?.["@graph"]) ? parsed["@graph"] : [parsed]);
      const hit = items.find((it) =>
        /Article|BlogPosting|TechArticle|NewsArticle|ScholarlyArticle|Report/i.test(String(it?.["@type"] || ""))
      );
      if (hit) {
        ldData = hit;
        break;
      }
    } catch {}
  }

  // Pick the most text-rich article container (avoids grabbing small sidebar/card <article> elements)
  const rootSelectors = [
    '[role="main"] article',
    "main article",
    "article",
    ".post-content",
    ".entry-content",
    ".article-content",
    ".prose",
    "main",
    '[role="main"]',
  ];
  let root = null;
  let bestLen = 0;
  for (const sel of rootSelectors) {
    for (const candidate of Array.from(document.querySelectorAll(sel))) {
      const len = (candidate.innerText || candidate.textContent || "").trim().length;
      if (len > bestLen && len > 200) {
        bestLen = len;
        root = candidate;
      }
    }
    if (root && bestLen > 500) break;
  }
  root = root || document.body;

  const paywalled = Boolean(
    root.querySelector('.paywall, [data-testid="paywall"], .paywall-jump, .paywall-title, .paywall-cta') ||
    /\bthis post is for paid subscribers\b/i.test(root.textContent || "")
  );

  const clone = root.cloneNode(true);
  for (const junk of clone.querySelectorAll(
    "script, style, noscript, nav, aside, footer, iframe, form, " +
    "[role='navigation'], [role='complementary'], .sidebar, .comments, #comments, .related-posts, .share-buttons, " +
    ".subscribe-widget, .subscription-widget, .subscription-widget-wrap, .captioned-button-wrap, .post-ufi, .facepile, " +
    ".button-wrapper, [data-testid='subscribe-widget'], .newsletter-post-promo, " +
    ".paywall, [data-testid='paywall'], .paywall-jump, .paywall-title, .paywall-cta"
  )) {
    junk.remove();
  }

  const txtOf = (node) => node.textContent || "";
  const isBoilerplate = (t) =>
    /is a reader-supported publication\.\s*To receive new posts/i.test(t) ||
    /^this post is for paid subscribers\.?$/i.test(t) ||
    /^upgrade to paid$/i.test(t);
  const stripTrailingPromo = (t) =>
    t.replace(/([.!?])\s*[^.!?]*is a reader-supported publication\.\s*To receive new posts[\s\S]*$/i, "$1").trim();
  const cellText = (cell) => txtOf(cell).replace(/\s+/g, " ").replace(/\|/g, "\\|").trim();

  const convertTable = (tableEl) => {
    const rows = Array.from(tableEl.querySelectorAll("tr"))
      .map((tr) => Array.from(tr.querySelectorAll("th, td")).map(cellText))
      .filter((cells) => cells.length > 0 && cells.some((c) => c !== ""));
    if (!rows.length) return "";
    const colCount = Math.max(...rows.map((r) => r.length));
    const pad = (r) => r.concat(Array(Math.max(0, colCount - r.length)).fill(""));
    const header = pad(rows[0]);
    const sep = Array(colCount).fill("---");
    const body = rows.slice(1).map(pad);
    const mdRows = [
      `| ${header.join(" | ")} |`,
      `| ${sep.join(" | ")} |`,
      ...body.map((r) => `| ${r.join(" | ")} |`),
    ];
    return "\n" + mdRows.join("\n") + "\n";
  };

  // Convert headings, code blocks (with language), tables, nested lists, and paragraphs cleanly
  const lines = [];
  const walk = (el, listDepth = 0) => {
    if (!el || el.nodeType !== 1) return;
    const tag = el.tagName.toLowerCase();
    if (/^h[1-6]$/.test(tag)) {
      const lvl = "#".repeat(parseInt(tag[1], 10));
      const t = txtOf(el).replace(/\s+/g, " ").trim();
      if (t && !isBoilerplate(t)) lines.push(`\n${lvl} ${t}`);
      return;
    }
    if (tag === "pre") {
      const codeEl = el.querySelector("code");
      const cls = `${el.className || ""} ${codeEl?.className || ""}`;
      const langMatch = cls.match(/(?:language-|lang-)([a-z0-9_+#-]+)/i);
      const lang = langMatch ? langMatch[1].toLowerCase() : "";
      const code = txtOf(codeEl || el).replace(/^\n+|\n+$/g, "");
      if (code) lines.push(`\n\`\`\`${lang}\n${code}\n\`\`\``);
      return;
    }
    if (tag === "table") {
      const mdTable = convertTable(el);
      if (mdTable) lines.push(mdTable);
      return;
    }
    if (tag === "li") {
      const nestedLists = Array.from(el.children).filter((c) => /^(ul|ol)$/i.test(c.tagName));
      const liClone = el.cloneNode(true);
      for (const nl of Array.from(liClone.children).filter((c) => /^(ul|ol)$/i.test(c.tagName))) {
        nl.remove();
      }
      const ownText = stripTrailingPromo(txtOf(liClone).replace(/\s+/g, " ").trim());
      if (ownText && !isBoilerplate(ownText)) lines.push(`${"  ".repeat(listDepth)}- ${ownText}`);
      for (const nl of nestedLists) walk(nl, listDepth + 1);
      return;
    }
    if (tag === "p" || tag === "blockquote") {
      const t = stripTrailingPromo(txtOf(el).replace(/\s+/g, " ").trim());
      if (t && !isBoilerplate(t)) lines.push(tag === "blockquote" ? `\n> ${t}` : `\n${t}`);
      return;
    }
    for (const child of el.children) walk(child, listDepth);
  };
  walk(clone, 0);
  const rawFallback = txtOf(clone).replace(/[ \t]+/g, " ").replace(/\n{3,}/g, "\n\n").trim();
  const structuredText = (lines.length ? lines.join("\n") : rawFallback).replace(/\n{3,}/g, "\n\n").trim().slice(0, 45000);

  // Comma-safe srcset parser (handles Substack/Cloudinary/Imgix URLs with commas inside parameters)
  const pickLargestSrc = (img) => {
    const srcset = img.srcset || img.getAttribute("data-srcset") || "";
    if (srcset) {
      const parts = srcset.trim().split(/,\s+(?=(?:https?:\/\/|\/|data:))/);
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
    const fallback = img.currentSrc || img.src || img.getAttribute("data-src") || img.getAttribute("data-original") || "";
    if (!fallback || fallback.startsWith("data:")) return "";
    try { return new URL(fallback, location.href).href; } catch { return fallback; }
  };

  const slides = [];
  const seen = new Set();
  for (const img of Array.from(root.querySelectorAll("img"))) {
    if (img.closest("nav, aside, footer, .comments, #comments, .related-posts")) continue;
    const r = img.getBoundingClientRect();
    const inFig = !!img.closest("figure");
    if (!inFig && (r.width < 220 || r.height < 140)) continue;
    if (img.naturalWidth && img.naturalWidth < 120) continue;
    const src = pickLargestSrc(img);
    if (!src.startsWith("http")) continue;
    const cleanPath = src.split("?")[0].toLowerCase();
    if (cleanPath.endsWith(".svg") || cleanPath.endsWith(".ico")) continue;
    if (seen.has(cleanPath)) continue;
    seen.add(cleanPath);
    const figCaption = img.closest("figure")?.querySelector("figcaption")?.innerText?.trim() || "";
    slides.push({
      index: slides.length + 1,
      src,
      dims: img.naturalWidth ? `${img.naturalWidth}x${img.naturalHeight}` : "unknown",
      alt: img.alt || "",
      note: figCaption,
    });
  }

  const ldAuthor = Array.isArray(ldData.author)
    ? ldData.author.map((a) => (typeof a === "string" ? a : a?.name)).filter(Boolean).join(", ")
    : (typeof ldData.author === "string" ? ldData.author : ldData.author?.name);

  return {
    platform: "web_article",
    status: "ok",
    paywalled,
    url: location.href,
    canonical_url: document.querySelector('link[rel="canonical"]')?.href || getMeta("og:url") || location.href,
    title: ldData.headline || getMeta("og:title") || document.title,
    author: ldAuthor || getMeta("author") || getMeta("og:site_name") || null,
    handle: location.hostname,
    published: ldData.datePublished || getMeta("article:published_time") || document.querySelector("time[datetime]")?.getAttribute("datetime") || null,
    engagement: {},
    text: structuredText,
    comments: [],
    external_links: Array.from(root.querySelectorAll('a[href^="http"]'))
      .filter((a) => {
        if (a.closest("nav, aside, footer, .comments, #comments, .post-ufi, .facepile, .subscription-widget-wrap, .captioned-button-wrap, .paywall, [data-testid='paywall'], .paywall-cta")) {
          return false;
        }
        if (a.classList?.contains("image-link")) return false;
        const h = a.href || "";
        if (
          h.includes("substackcdn.com/image/") ||
          h.includes("substack.com/profile/") ||
          h.includes("substack.com/@") ||
          h.includes("substack.com/note/") ||
          h.includes("substack.com/sign-in") ||
          h.includes("utm_source=paywall") ||
          /\.substack\.com\/subscribe(?:\?|\/|$)/i.test(h) ||
          h.includes("/restacks")
        ) {
          return false;
        }
        if (a.querySelector("img") && !(a.textContent || "").trim()) return false;
        return true;
      })
      .map((a) => a.href)
      .filter((v, i, a) => a.indexOf(v) === i)
      .slice(0, 25),
    total_slides: slides.length,
    slides,
  };
}
