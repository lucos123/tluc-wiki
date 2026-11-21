async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const startedAt = Date.now();

  const loginGate =
    document.querySelector('[data-testid="loginButton"]') &&
    !document.querySelector('article[data-testid="tweet"], [data-testid="twitterArticleReadView"], [data-testid="article-content"]');
  if (loginGate) {
    return { platform: "x_twitter", status: "blocked", url: location.href, reason: "X/Twitter login wall" };
  }

  const upgradeXMedia = (rawUrl) => {
    try {
      const u = new URL(rawUrl);
      if (u.hostname.includes("pbs.twimg.com") && u.pathname.includes("/media/")) {
        u.searchParams.set("name", "orig");
        return u.toString();
      }
      return rawUrl;
    } catch {
      return rawUrl;
    }
  };

  const getTweetHandle = (tw) =>
    tw.querySelector('[data-testid="User-Name"]')?.innerText?.match(/@[A-Za-z0-9_]+/)?.[0] || null;
  const getTweetStatusId = (tw) => {
    const link = tw.querySelector('a[href*="/status/"]');
    return link?.getAttribute("href")?.match(/\/status\/(\d+)/)?.[1] || null;
  };
  const expandInTweets = () => {
    for (const btn of Array.from(document.querySelectorAll('article[data-testid="tweet"] [data-testid="tweet-text-show-more-link"]'))) {
      try { btn.click(); } catch {}
    }
  };

  expandInTweets();
  await sleep(300);

  const focalId = location.pathname.match(/\/(?:status|article)\/(\d+)/)?.[1] || null;
  const initialTweets = Array.from(document.querySelectorAll('article[data-testid="tweet"]'));
  const focalTweet =
    (focalId && initialTweets.find((tw) => getTweetStatusId(tw) === focalId)) ||
    initialTweets[0] ||
    null;

  const primaryUserText = focalTweet?.querySelector('[data-testid="User-Name"]')?.innerText || "";
  const primaryHandle = getTweetHandle(focalTweet) || primaryUserText.match(/@[A-Za-z0-9_]+/)?.[0] || null;
  const primaryAuthor = primaryUserText ? primaryUserText.split("\n")[0].trim() : null;

  // Support X Longform Articles (note/article view)
  const articleView = document.querySelector('[data-testid="twitterArticleReadView"], [data-testid="article-content"]');
  const articleTitle = articleView?.querySelector("h1")?.innerText?.trim() || null;
  const articleBody = articleView ? articleView.innerText.trim().slice(0, 35000) : "";

  // Collect focal tweet + connected self-thread tweets across virtualized scroll (stop once another author replies)
  const seenTweetKeys = new Set();
  const threadEntries = [];
  const seenMedia = new Set();
  const slides = [];
  const seenExt = new Set();
  const externalLinks = [];
  const videosFound = [];
  let sawFocal = !focalId;
  let reachedOtherReply = false;

  const harvestVisibleTweets = () => {
    expandInTweets();
    const visible = Array.from(document.querySelectorAll('article[data-testid="tweet"]'));
    for (const tw of visible) {
      const tid = getTweetStatusId(tw);
      const handle = getTweetHandle(tw);
      const key = tid || (tw.querySelector('[data-testid="tweetText"]')?.innerText || "").slice(0, 80);
      if (!key) continue;

      const isFocal = !!(focalId && tid === focalId);
      if (isFocal) sawFocal = true;

      if (primaryHandle && handle && handle.toLowerCase() !== primaryHandle.toLowerCase()) {
        if (sawFocal && !isFocal) {
          reachedOtherReply = true;
          break;
        }
        continue;
      }

      if (!seenTweetKeys.has(key)) {
        seenTweetKeys.add(key);
        const text = tw.querySelector('[data-testid="tweetText"]')?.innerText?.trim() || "";
        if (text) threadEntries.push({ id: tid, text });

        for (const img of Array.from(tw.querySelectorAll('img[src*="pbs.twimg.com/media"], img[src*="pbs.twimg.com/card_img"]'))) {
          const r = img.getBoundingClientRect();
          if (r.width < 120 || r.height < 100) continue;
          const hiRes = upgradeXMedia(img.currentSrc || img.src);
          const mKey = hiRes.split("?")[0];
          if (!seenMedia.has(mKey)) {
            seenMedia.add(mKey);
            slides.push({
              index: slides.length + 1,
              src: hiRes,
              dims: img.naturalWidth ? `${img.naturalWidth}x${img.naturalHeight}` : "unknown",
              alt: img.alt || "",
              note: "",
            });
          }
        }

        if (tw.querySelector('video, [data-testid="videoPlayer"]')) {
          videosFound.push(tid ? `https://x.com/i/status/${tid}` : location.href);
        }

        for (const a of Array.from(tw.querySelectorAll('a[href^="http"]'))) {
          const href = a.href;
          if (href.includes("x.com/") || href.includes("twitter.com/")) continue;
          const label = (a.innerText || "").trim();
          const chosen = /^https?:\/\//i.test(label) && !label.endsWith("…") && !label.endsWith("...") ? label : href;
          if (!seenExt.has(chosen)) {
            seenExt.add(chosen);
            externalLinks.push(chosen);
          }
        }
      }
    }
  };

  harvestVisibleTweets();
  if (!articleView) {
    let scrollSteps = 0;
    while (!reachedOtherReply && scrollSteps < 6 && Date.now() - startedAt < 18000) {
      const beforeCount = threadEntries.length;
      const beforeY = window.scrollY;
      window.scrollBy(0, Math.round(window.innerHeight * 0.85));
      await sleep(450);
      harvestVisibleTweets();
      scrollSteps++;
      if (window.scrollY === beforeY && threadEntries.length === beforeCount) break;
    }
    window.scrollTo(0, 0);
  } else {
    for (const img of Array.from(articleView.querySelectorAll('img[src*="pbs.twimg.com/media"]'))) {
      const hiRes = upgradeXMedia(img.currentSrc || img.src);
      const mKey = hiRes.split("?")[0];
      if (!seenMedia.has(mKey)) {
        seenMedia.add(mKey);
        slides.push({
          index: slides.length + 1,
          src: hiRes,
          dims: img.naturalWidth ? `${img.naturalWidth}x${img.naturalHeight}` : "unknown",
          alt: img.alt || "",
          note: "",
        });
      }
    }
  }

  const timeEl = focalTweet?.querySelector("time[datetime]") || document.querySelector("time[datetime]");
  const metricGroups = focalTweet
    ? Array.from(focalTweet.querySelectorAll('[data-testid="reply"], [data-testid="retweet"], [data-testid="like"], [data-testid="bookmark"], a[href*="/analytics"]'))
        .map((el) => `${el.getAttribute("data-testid") || "views"}:${(el.innerText || "").trim()}`)
        .filter((s) => !s.endsWith(":"))
    : [];

  return {
    platform: "x_twitter",
    status: "ok",
    url: location.href,
    canonical_url: location.href.split("?")[0],
    title: articleTitle,
    author: primaryAuthor,
    handle: primaryHandle,
    published: timeEl ? timeEl.getAttribute("datetime") : null,
    is_longform_article: !!articleView,
    tweet_count: threadEntries.length,
    engagement: metricGroups,
    text: articleBody || threadEntries.map((t) => t.text).join("\n\n---\n\n"),
    comments: [],
    external_links: externalLinks.slice(0, 20),
    videos_found: [...new Set(videosFound)],
    total_slides: slides.length,
    slides,
  };
}
