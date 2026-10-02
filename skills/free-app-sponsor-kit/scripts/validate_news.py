"""Kiểm news.json trước khi push. Chạy: python3 validate_news.py docs/news.json [--urls]

Báo LỖI (exit 1): JSON hỏng, thiếu id / trùng id, quảng cáo thiếu `end`, ngày sai dạng hoặc
end < start, link/ảnh không phải https. Báo CẢNH BÁO: 2 quảng cáo sidebar trùng thời gian cho cùng
app (chỉ cái đứng trước hiện), quảng cáo đã hết hạn còn nằm trong file, chữ quá dài sẽ bị cắt.
--urls: mở thử từng link và ảnh (cần mạng).
"""
import datetime as dt
import json
import re
import sys
import urllib.request

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def main(path, check_urls=False):
    errs, warns = [], []
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"LỖI: không đọc được JSON — {e}")
        return 1
    today = dt.date.today().isoformat()
    items = data.get("announcements") or []
    seen = set()
    for i, a in enumerate(items):
        tag = f"#{i} {a.get('id', '?')}"
        if not a.get("id"):
            errs.append(f"{tag}: thiếu id")
        elif a["id"] in seen:
            errs.append(f"{tag}: trùng id")
        seen.add(a.get("id"))
        is_ad = a.get("placement") in ("sidebar", "side") or a.get("tone") == "promo"
        for k in ("start", "end"):
            if a.get(k) and not DATE.match(a[k]):
                errs.append(f"{tag}: {k} phải dạng YYYY-MM-DD")
        if is_ad and not a.get("end"):
            errs.append(f"{tag}: quảng cáo bắt buộc có end (ngày cuối còn hiện)")
        if a.get("start") and a.get("end") and a["end"] < a["start"]:
            errs.append(f"{tag}: end trước start")
        if a.get("end") and a["end"] < today:
            warns.append(f"{tag}: đã hết hạn ({a['end']}) — có thể xoá khỏi file")
        for k in ("link", "image"):
            if a.get(k) and not str(a[k]).startswith("https://"):
                errs.append(f"{tag}: {k} phải là https://")
        if len(a.get("title", "")) > 120 or len(a.get("text", "")) > 300:
            warns.append(f"{tag}: tiêu đề >120 hoặc mô tả >300 ký tự sẽ bị cắt")
        if check_urls:
            for k in ("link", "image"):
                if a.get(k):
                    try:
                        req = urllib.request.Request(a[k], headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req, timeout=10) as r:
                            if r.status >= 400:
                                errs.append(f"{tag}: {k} trả về {r.status}")
                    except Exception as e:  # noqa: BLE001
                        errs.append(f"{tag}: {k} không mở được — {e}")
    side = [a for a in items if a.get("placement") in ("sidebar", "side")
            and (not a.get("end") or a["end"] >= today) and not (a.get("start") and a.get("end") and a["end"] < a["start"])]
    for x in range(len(side)):
        for y in range(x + 1, len(side)):
            a, b = side[x], side[y]
            same_app = not a.get("apps") or not b.get("apps") or set(a["apps"]) & set(b["apps"])
            overlap = (a.get("start") or "0000") <= (b.get("end") or "9999") and (b.get("start") or "0000") <= (a.get("end") or "9999")
            if same_app and overlap:
                warns.append(f"{a['id']} và {b['id']}: cùng thời gian ở thẻ sidebar — chỉ {a['id']} hiện")
    for w in warns:
        print("CẢNH BÁO:", w)
    for e in errs:
        print("LỖI:", e)
    print(f"→ {len(items)} mục · {len(errs)} lỗi · {len(warns)} cảnh báo")
    return 1 if errs else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(main(args[0] if args else "docs/news.json", "--urls" in sys.argv))
