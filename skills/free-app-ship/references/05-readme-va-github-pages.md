# 05 · README và trang giới thiệu (GitHub Pages)

## Giới hạn của README trên GitHub — đừng mất thời gian thử lại

GitHub lọc HTML trong README và có chính sách `media-src` chỉ cho phép file tải lên qua giao diện web:
- `<iframe>` (YouTube) → bị biến thành chữ. **Không nhúng được video YouTube vào README.**
- `<audio>` → bị xoá. **Không phát mp3 trong README.**
- `<video src>` chỉ phát được với link `github.com/user-attachments/…` (kéo thả file mp4 vào ô sửa README trên web,
  ≤ 10 MB với tài khoản miễn phí). File trong repo, Releases, raw.githubusercontent đều bị chặn.

→ README: ảnh bìa video (tự dựng, có nút ▶) **dẫn tới trang Pages**, nơi video và âm thanh phát tại chỗ.

## README — thứ tự khối

1. Banner (ảnh của người tạo) → tiêu đề + 1 câu giá trị → khung `> [!TIP]` dẫn tới trang giới thiệu.
2. "Phát triển bởi … · Dựa trên …" (ghi nhận).
3. Video giới thiệu (ảnh bìa → trang Pages).
4. **Cài đặt 1 lệnh** (macOS/Linux, Windows) + `> [!WARNING]` cho người dùng Mac.
5. Tải zip thủ công + "Đã tải zip và bị chặn?".
6. Nghe thử / demo (bảng, link tới Pages).
7. Tính năng + ảnh giao diện.
8. Cấu trúc repo · Ghi nhận · Giấy phép.

Bỏ tài liệu gốc tiếng Anh của dự án upstream (giữ link + ghi nhận) — người dùng cuối không cần.

## Trang Pages (`docs/index.html`)

- Bật: `gh api -X POST repos/<user>/<repo>/pages -f "source[branch]=main" -f "source[path]=/docs"`; chờ `status=built`.
- **Sinh trang bằng script** (vd `scripts/build_pages.py`) từ dữ liệu có sẵn (danh sách giọng, changelog, dung lượng release
  qua API GitHub) — đổi dữ liệu thì chạy lại, không sửa tay HTML.
- Khối nên có: hero + CTA "Tải miễn phí" · video YouTube nhúng (iframe, `aspect-ratio: 16/9`) · **tải trực tiếp** 3 nút
  (link `/releases/latest/download/…`, ghi phiên bản + dung lượng) · cài 1 lệnh có nút Sao chép · tính năng + 4 ảnh ·
  demo (audio `preload="none"`, phát một cái một lúc, lọc) · "Có gì mới" từ changelog · **"Không cài được?"**
  (`<details>`: Gatekeeper, SmartScreen, lỗi tải thư viện, cổng bận, model tải lâu, máy yếu, gỡ cài đặt) · footer ghi nhận.
- Âm thanh/ảnh dùng `https://raw.githubusercontent.com/<user>/<repo>/main/…` (Pages không chặn) hoặc đặt trong `docs/`.
- Pages trả `Access-Control-Allow-Origin: *` → app/website khác đọc thẳng `news.json` được.
- `og:image`, `og:title`, `og:description` để chia sẻ link lên Facebook/Zalo có ảnh. **Mở thử ảnh og** — trang khác có thể hỏng.
- Không dùng font pixel / font không có dấu tiếng Việt (Be Vietnam Pro có subset `vietnamese`).
- Kiểm: 1280px và 375px (không cuộn ngang), sáng/tối, iframe có, audio phát được (`a.play()` rồi đọc `currentTime`).

## Ảnh giao diện

- Chụp từ **bản app sạch**: chạy bản sao với thư mục dữ liệu trống (`APP_HOME=/tmp/clean`), tạo 2–3 mục demo trung tính,
  ẩn popup onboarding/thông báo (`localStorage` qua `addInitScript`), `deviceScaleFactor: 2`, thu về 1600px.
- Ảnh đặt `assets/readme/` (không phụ thuộc CDN ngoài). Cắt bỏ tooltip Dock/taskbar lọt mép ảnh.
- Đổi giao diện → chụp lại ảnh (ảnh cũ mang font/màu cũ làm trang trông lệch).
- Âm thanh demo: sinh bằng script gọi thẳng model (không qua API app → không làm đầy lịch sử của người tạo), nén MP3 64 kbps,
  nghe lại bằng nhận dạng giọng nói (whisper) để chắc đọc đủ câu. Tên riêng/từ nước ngoài model đọc sai thì viết phiên âm cho
  model nhưng **hiển thị** tên gốc (`display_text`).
