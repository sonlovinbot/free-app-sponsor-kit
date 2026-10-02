// Sponsor Kit — proxy tin tức cho app LOCAL viết bằng Node/Express (Node 18+ có sẵn fetch).
// app.use(require("./express_news")({ feedUrl: "https://<user>.github.io/<repo>/news.json", version: "1.0.0" }))
// Frontend: SponsorKit.init({ feedUrl: "/api/news", ... })
const fs = require("fs"), path = require("path"), os = require("os");

module.exports = function sponsorNews({ feedUrl, version, cacheFile, ttlMs = 3 * 3600e3, enabled = process.env.APP_NEWS !== "off" }) {
  const file = cacheFile || path.join(os.homedir(), ".my-app", "news-cache.json");
  let mem = null, at = 0;
  const https = (u) => (typeof u === "string" && u.startsWith("https://") && u.length < 500 ? u : "");
  const clean = (raw) => ({
    latest_version: String(raw?.latest_version || "").slice(0, 20),
    release_url: https(raw?.release_url),
    update_note: String(raw?.update_note || "").slice(0, 300),
    announcements: (raw?.announcements || []).filter((a) => a && a.id).slice(0, 10).map((a) => ({
      id: String(a.id).slice(0, 60),
      placement: a.placement === "sidebar" || a.placement === "side" ? "sidebar" : "top",
      tone: ["info", "warning", "promo"].includes(a.tone) ? a.tone : "info",
      label: String(a.label || "").slice(0, 30), campaign: String(a.campaign || "").slice(0, 60),
      apps: Array.isArray(a.apps) ? a.apps.map((x) => String(x).slice(0, 40)).slice(0, 20) : [],
      title: String(a.title || "").slice(0, 120), text: String(a.text || "").slice(0, 300),
      image: https(a.image), link: https(a.link), cta: String(a.cta || "").slice(0, 40),
      start: String(a.start || "").slice(0, 10), end: String(a.end || "").slice(0, 10),
      min_version: String(a.min_version || "").slice(0, 20), max_version: String(a.max_version || "").slice(0, 20),
      dismissible: a.dismissible !== false,
    })),
  });
  async function fetchFeed() {
    try {
      const r = await fetch(feedUrl, { signal: AbortSignal.timeout(4000), headers: { "User-Agent": `My-Free-App/${version}` } });
      const data = clean(await r.json());
      fs.mkdirSync(path.dirname(file), { recursive: true });
      fs.writeFileSync(file, JSON.stringify(data));
      return data;
    } catch {
      try { return clean(JSON.parse(fs.readFileSync(file, "utf8"))); } catch { return null; }
    }
  }
  return async function (req, res, next) {
    if (req.path !== "/api/news") return next();
    if (!enabled) return res.json({ enabled: false, version });
    if (!mem || Date.now() - at > ttlMs) { const f = await fetchFeed(); if (f) mem = f; at = Date.now(); }
    res.json({ enabled: true, version, ...(mem || {}) });
  };
};
