# 01 · Bản đồ quy trình

```
 app chạy được trên máy
   │ 1 hỏi người tạo  → SHIP.md (tên, tài khoản GitHub, công khai?, tác giả gốc, nhà tài trợ…)
   │ 2 dọn repo        → chỉ giữ thứ người dùng cần + LICENSE + ghi nhận
   │ 3 kiểm bảo mật    → scripts/preship_check.sh: 0 ĐỎ
   │ 4 đóng gói        → dist/<App>-macOS|Windows|Linux.zip + install-online.sh/.ps1
   │   phát hành       → git tag + GitHub Release (zip đính kèm) + link /releases/latest/download/…
   │ 5 giới thiệu      → README tiếng Việt + docs/index.html (Pages) + ảnh từ bản sạch
   │ 6 giao diện       → onboarding, tương phản ≥ 4.5:1, 375px không tràn
   │ 7 sau phát hành   → docs/news.json: báo bản mới, quảng cáo có ngày hết hạn
   ▼
 người dùng: mở trang → nghe/xem → dán 1 lệnh → app tự mở → tự báo khi có bản mới
```

## Bước 1 — chuẩn bị git

- Thư mục chưa là repo: `git init -b main`, commit đầu tiên tên tác giả là người tạo
  (`git -c user.name="…" -c user.email="…" commit`), **đọc `.gitignore` trước khi `git add -A`**.
- Tạo repo GitHub: `gh repo create <user>/<tên> --public|--private --description "…" --source . --push`.
  Kiểm trước: `gh auth status` (máy có thể đăng nhập nhiều tài khoản — hỏi dùng tài khoản nào).
- Repo dựa trên dự án mã nguồn mở khác: **không fork kiểu giữ nguyên lịch sử CI** — xoá `.github/workflows` của dự án
  gốc (xem bài học "Publish to PyPI chạy lỗi mỗi lần release").

## Bước 2 — dọn repo

Mục tiêu: người dùng tải về chỉ thấy thứ để **chạy**; người đọc repo thấy rõ đây là sản phẩm của ai.

| Bỏ | Giữ |
|---|---|
| Tài liệu, ví dụ, test, notebook, fine-tune, Docker, cấu hình deploy của dự án gốc | Code app + lõi cần để chạy |
| Giao diện cũ / app phụ không dùng (vd Gradio khi đã có web app riêng) | `LICENSE` gốc (bắt buộc theo giấy phép) |
| `.github/workflows` của dự án gốc | Ghi nhận tác giả gốc trong README / app / trang Pages |
| File rác: `.DS_Store`, `__pycache__`, `*.egg-info`, `.gstack/`, log, `dist/` | Bộ cài, script cài 1 lệnh, script dựng trang |
| Thư viện nặng không dùng tới trong `pyproject.toml` / `package.json` | Thư viện app thật sự cần — **khai báo trực tiếp**, đừng dựa vào thư viện kéo theo |

Sau khi bỏ thư viện: **cài mới hoàn toàn từ zip vào thư mục trống** và chạy thử các chức năng chính. (Bài học:
bỏ Gradio thì mất luôn FastAPI/uvicorn vì trước đó chúng chỉ được cài kèm Gradio.)

Thêm vào README một bảng "Cấu trúc repo" — thư mục nào làm gì.

## Bước 3 — bảo mật: xem `03-bao-mat-truoc-khi-share.md`

## Bước 4 — đóng gói, phát hành: xem `04-dong-goi-phat-hanh.md`

## Bước 5 — README + Pages: xem `05-readme-va-github-pages.md`

## Bước 6 — giao diện: xem `06-giao-dien-ux.md`

## Bước 7 — sau phát hành

- Gắn skill `free-app-sponsor-kit`: thanh "Đã có bản mới", quảng cáo có lịch, thư ngỏ, khung "Phát triển bởi".
- Mỗi lần ra bản: tăng `latest_version` trong `docs/news.json` **sau khi** release đã có zip (không thì người dùng bấm
  "xem bản mới" mà link tải còn bản cũ).
- Thêm dự án vào trang chủ tổng hợp (`projects.json` của repo `<user>.github.io`, xem `05` mục "Tên miền riêng").
- Chạy `scripts/verify_release.sh` rồi mới báo xong.
- Thêm bài học mới (nếu có) vào `07-bai-hoc.md`.
