"""Sponsor Kit — proxy tin tức cho app LOCAL viết bằng FastAPI (chép nguyên khối vào server).

Vì sao cần proxy thay vì để trình duyệt đọc thẳng feed: server lưu bản đã tải ra đĩa nên mất mạng
vẫn có quảng cáo/ thông báo cũ để hiện, và lọc dữ liệu một lần ở phía máy người dùng.

Cần sẵn trong file server: `app` (FastAPI), `log` (logging), `VERSION` (chuỗi phiên bản app).
Đổi 3 chỗ: NEWS_URL (link news.json), thư mục cache trong _news_cache_file(), User-Agent.
Frontend: SponsorKit.init({ feedUrl: "/api/news", ... }).
"""
import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

# ── Tin tức từ xa: banner quảng cáo, thông báo, báo có bản mới ──────────────
# Chủ phần mềm sửa docs/news.json trên GitHub Pages → mọi máy đã cài tự nhận,
# không cần phát hành lại. Chỉ nhận chữ + link https (không HTML/script); mất
# mạng thì dùng bản đã lưu. Tắt hẳn: APP_NEWS=off.
NEWS_URL = os.environ.get("APP_NEWS_URL", "https://<user>.github.io/<repo>/news.json")
NEWS_ENABLED = os.environ.get("APP_NEWS", "on").strip().lower() not in ("0", "off", "false", "no")
NEWS_TTL = 3 * 3600
_NEWS: Dict[str, Any] = {"at": 0.0, "data": None}
_NEWS_LOCK = threading.Lock()


def _https(url: Any) -> str:
    url = str(url or "").strip()
    return url if url.startswith("https://") and len(url) < 500 else ""


def _clean_news(raw: Any) -> Dict[str, Any]:
    """Giữ đúng các trường biết trước, cắt độ dài, bỏ link không phải https."""
    if not isinstance(raw, dict):
        return {}
    items = []
    for a in (raw.get("announcements") or [])[:10]:
        if not isinstance(a, dict) or not a.get("id"):
            continue
        items.append({
            "id": str(a["id"])[:60],
            "placement": "sidebar" if a.get("placement") == "sidebar" else "top",
            "tone": a.get("tone") if a.get("tone") in ("info", "warning", "promo") else "info",
            "title": str(a.get("title") or "")[:120],
            "text": str(a.get("text") or "")[:300],
            "image": _https(a.get("image")),
            "link": _https(a.get("link")),
            "cta": str(a.get("cta") or "")[:40],
            "label": str(a.get("label") or "")[:30],
            "campaign": str(a.get("campaign") or "")[:60],
            "apps": [str(x)[:40] for x in (a.get("apps") or [])][:20] if isinstance(a.get("apps"), list) else [],
            "start": str(a.get("start") or "")[:10],
            "end": str(a.get("end") or "")[:10],
            "min_version": str(a.get("min_version") or "")[:20],
            "max_version": str(a.get("max_version") or "")[:20],
            "dismissible": a.get("dismissible", True) is not False,
        })
    return {
        "latest_version": str(raw.get("latest_version") or "")[:20],
        "release_url": _https(raw.get("release_url")),
        "update_note": str(raw.get("update_note") or "")[:300],
        "announcements": items,
    }


def _news_cache_file() -> Path:
    return Path(os.environ.get("APP_HOME") or (Path.home() / ".my-app")) / "news-cache.json"


def _fetch_news() -> Optional[Dict[str, Any]]:
    import urllib.request
    try:
        req = urllib.request.Request(NEWS_URL, headers={"User-Agent": f"My-Free-App/{VERSION}"})
        with urllib.request.urlopen(req, timeout=4) as r:
            data = _clean_news(json.loads(r.read(200_000).decode("utf-8")))
        try:
            f = _news_cache_file()
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass
        return data
    except Exception as e:  # noqa: BLE001 — offline / lỗi mạng: dùng bản đã lưu
        log.info("Không tải được tin tức (%s) — dùng bản đã lưu.", e)
        try:
            return _clean_news(json.loads(_news_cache_file().read_text(encoding="utf-8")))
        except Exception:  # noqa: BLE001
            return None


@app.get("/api/news")
def news() -> Dict[str, Any]:
    if not NEWS_ENABLED:
        return {"enabled": False, "version": VERSION}
    with _NEWS_LOCK:
        if _NEWS["data"] is None or time.time() - _NEWS["at"] > NEWS_TTL:
            fresh = _fetch_news()
            if fresh is not None:
                _NEWS["data"] = fresh
            _NEWS["at"] = time.time()
    return {"enabled": True, "version": VERSION, **(_NEWS["data"] or {})}
