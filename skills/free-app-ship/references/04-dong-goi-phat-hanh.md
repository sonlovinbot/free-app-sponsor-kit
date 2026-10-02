# 04 · Đóng gói, phát hành, cập nhật phiên bản

## Bộ chia sẻ chuẩn (người dùng nhận được gì)

| Thứ | Ở đâu | Ghi chú |
|---|---|---|
| **Lệnh cài 1 dòng** (khuyên dùng) | `install-online.sh` (macOS/Linux), `install-online.ps1` (Windows) ở gốc repo | Tải bằng curl/PowerShell nên **không bị Gatekeeper/SmartScreen chặn**; chạy lại = cập nhật |
| Zip theo hệ điều hành | GitHub Release, link cố định `…/releases/latest/download/<App>-macOS.zip` | Cho người không dùng Terminal; kèm hướng dẫn mở file bị chặn |
| Mã nguồn | repo GitHub | README tiếng Việt, bảng cấu trúc repo |
| Trang giới thiệu | GitHub Pages `https://<user>.github.io/<repo>/` | Video, nghe thử, tải trực tiếp, xử lý sự cố |
| Thông báo trong app | `docs/news.json` (skill `free-app-sponsor-kit`) | Báo bản mới, quảng cáo |

## Bộ cài

- `templates/build-installers.sh`: gom file chung + file riêng từng hệ điều hành → `dist/<App>-<OS>.zip`.
  Loại trừ `__pycache__`, `*.pyc`, `.DS_Store`, `.gstack`, `*.egg-info`, log. **Mở thử zip** (`unzip -l`) xem có lọt rác,
  có đúng phiên bản (`unzip -p … branding.json | grep version`).
- Script cài trong zip (`install.command` / `install.bat` / `install.sh`): cài trình quản lý môi trường (vd `uv`), cài
  thư viện, tạo icon Desktop, hỏi tự chạy khi mở máy, mở trình duyệt. File `.command` phải còn quyền chạy sau khi giải nén.
- `templates/install-online.sh` / `.ps1`: tải zip mới nhất về `~/<App>`, chép đè (giữ môi trường cũ để cập nhật nhanh),
  macOS gỡ cờ cách ly bằng **`/usr/bin/xattr -r -d com.apple.quarantine`** (đường dẫn tuyệt đối — máy có Python có thể có
  một `xattr` khác không hỗ trợ `-r`), rồi chạy bộ cài. Có biến `APP_NO_RUN=1` để thử phần tải/giải nén mà không cài thật.

### macOS chặn file tải bằng trình duyệt (không có chữ ký Apple)
- macOS 15+ hiện *"…" Not Opened — Apple could not verify…* chỉ có Done / Move to Trash. **Chuột phải → Open không còn
  tác dụng.** Cách mở: Done → Cài đặt hệ thống → Quyền riêng tư & Bảo mật → **Open Anyway** → nhập mật khẩu → mở lại.
- Đưa cảnh báo lớn (`> [!WARNING]`) lên đầu README cho người dùng Mac + mục "Không cài được?" trên trang Pages.
- Bỏ hẳn cảnh báo: cần Apple Developer ID (99 USD/năm) + notarize. Windows: chứng chỉ ký code. Nói rõ cho người tạo.

## Phát hành lần đầu

```bash
gh release create v1.0.0 dist/<App>-macOS.zip dist/<App>-Windows.zip dist/<App>-Linux.zip \
  --title "<App> 1.0.0" --notes-file RELEASE_NOTES.md --latest
curl -sIL https://github.com/<user>/<repo>/releases/latest/download/<App>-Windows.zip | grep -i content-disposition
```
Gắn link trang Pages vào ô Website của repo: `gh api repos/<user>/<repo> -X PATCH -f homepage=<url>`.

## Mỗi lần ra bản (chế độ B)

1. Tăng phiên bản ở **một chỗ** (vd `branding.json` / `package.json`), theo semver: sửa lỗi `x.y.Z`, tính năng `x.Y.0`.
2. Thêm mục đầu `changelog.json` (mẫu `templates/changelog.json`) — viết bằng lời người dùng thấy, không bằng tên hàm.
3. Tăng `?v=` của CSS/JS trong HTML (tránh trình duyệt giữ bản cũ).
4. `bash templates/build-installers.sh` → kiểm zip.
5. `scripts/preship_check.sh .` → 0 ĐỎ.
6. Commit (thông điệp tiếng Việt, liệt kê thay đổi) → push → `gh release create vX.Y.Z … --latest`.
7. Dựng lại trang Pages (lấy dung lượng zip mới) → push.
8. `docs/news.json`: `latest_version` = bản mới (sau khi release đã có zip).
9. `scripts/verify_release.sh <user>/<repo> <App>` → mọi link 200.
10. Khởi động lại app trên máy người tạo để chạy bản mới.

## Ghi chú phát hành (RELEASE_NOTES)

Mẫu `templates/RELEASE_NOTES.md`: tiêu đề có tên tính năng chính · 3–6 gạch đầu dòng lợi ích · lệnh cập nhật 1 dòng ·
link trang giới thiệu · dòng "Phát triển bởi … · Dựa trên …".
