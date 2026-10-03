#!/usr/bin/env python3
"""Kiểm sponsors.json (khung tài trợ website) trước khi push.

    python3 validate_sponsors.py sponsors/sponsors.json          # kiểm cấu trúc + ảnh trong thư mục
    python3 validate_sponsors.py sponsors/sponsors.json --urls   # mở thử từng link đăng ký

Lỗi (ĐỎ) → thoát mã 1. Cảnh báo (VÀNG) không chặn.
"""
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

KINDS = {"workshop", "community", "course", "elearning"}
FITS = {"cover", "contain"}


def parse_time(v):
    d = datetime.fromisoformat(v)
    if d.tzinfo is None:
        raise ValueError("thiếu múi giờ (thêm +07:00)")
    return d


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    check_urls = "--urls" in sys.argv
    errs, warns = [], []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"ĐỎ  không đọc được JSON: {e}")
        return 1

    items = data.get("items") or []
    ids = set()
    now = datetime.now(timezone.utc)
    for i, it in enumerate(items):
        tag = it.get("id") or f"items[{i}]"
        if not it.get("id"):
            errs.append(f"{tag}: thiếu id")
        elif it["id"] in ids:
            errs.append(f"{tag}: id trùng")
        ids.add(it.get("id"))
        for f in ("title", "desc", "image", "kind"):
            if not it.get(f):
                errs.append(f"{tag}: thiếu {f}")
        if it.get("kind") and it["kind"] not in KINDS:
            errs.append(f"{tag}: kind '{it['kind']}' không hợp lệ ({', '.join(sorted(KINDS))})")
        if it.get("fit") and it["fit"] not in FITS:
            errs.append(f"{tag}: fit phải là cover hoặc contain")
        url = it.get("url", "")
        if not url:
            warns.append(f"{tag}: chưa có url → mục này đang ẩn trên trang thật")
        elif not url.startswith("https://"):
            errs.append(f"{tag}: url phải bắt đầu bằng https://")
        if it.get("start") and it.get("deadline"):
            errs.append(f"{tag}: chỉ dùng start (sự kiện) HOẶC deadline (hạn ưu đãi), không dùng cả hai")
        for f in ("start", "deadline"):
            if it.get(f):
                try:
                    d = parse_time(it[f])
                    if d < now:
                        warns.append(f"{tag}: {f} {it[f]} đã qua → thẻ hiện mờ ở cuối (vẫn bấm được)")
                except ValueError as e:
                    errs.append(f"{tag}: {f} '{it[f]}' sai định dạng — {e}")
        # Không hiển thị giá tiền trên quảng cáo (yêu cầu của người tạo, 03/10/2026)
        for f in ("price", "price_note", "title", "desc"):
            v = str(it.get(f, ""))
            if re.search(r"\d[\d.,]*\s*(đ|₫|vnd|vnđ|k\b|tr\b|triệu|nghìn|ngàn)", v, re.I):
                errs.append(f"{tag}: {f} có giá tiền '{v}' — không ghi giá trên quảng cáo")
        if it.get("price_old"):
            errs.append(f"{tag}: bỏ price_old — không hiện giá gốc / giá giảm")
        img = it.get("image", "")
        if img and not img.startswith("https://") and not (path.parent / img).is_file():
            errs.append(f"{tag}: không thấy ảnh {path.parent / img}")
        if check_urls and url.startswith("https://"):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 validate_sponsors"})
                with urllib.request.urlopen(req, timeout=15) as r:
                    if r.status >= 400:
                        errs.append(f"{tag}: {url} trả {r.status}")
            except Exception as e:  # noqa: BLE001
                errs.append(f"{tag}: mở {url} lỗi — {e}")

    for name, cfg in (data.get("pages") or {}).items():
        for ref in cfg.get("items", []):
            if ref != "*" and ref not in ids:
                errs.append(f"pages.{name}: không có chương trình id '{ref}'")
        if cfg.get("layout") not in (None, "wide"):
            errs.append(f"pages.{name}: layout chỉ nhận 'wide'")

    for w in warns:
        print(f"VÀNG {w}")
    for e in errs:
        print(f"ĐỎ  {e}")
    print(f"{len(items)} chương trình · {len(data.get('pages') or {})} trang · {len(errs)} lỗi · {len(warns)} cảnh báo")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
