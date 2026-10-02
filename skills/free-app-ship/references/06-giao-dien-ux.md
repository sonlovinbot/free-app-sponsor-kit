# 06 · Giao diện và trải nghiệm lần đầu

## Onboarding cho người mới (app chạy trên máy)

Popup tự hiện lần đầu (nhớ bằng localStorage), mở lại bằng nút ở sidebar. 4 bước:
1. **Giới thiệu** — nói rõ: *app chạy trên máy bạn; máy bật + app chạy thì dùng được giao diện và API; tắt máy / máy ngủ thì
   không*. Dữ liệu ở lại trên máy.
2. **Kiểm tra máy** — app local: server đo thật (HĐH, chip, RAM, CPU, ổ trống); bản web: trình duyệt đo (`navigator.deviceMemory`
   chỉ Chrome, tối đa 8; Safari không cho biết phiên bản macOS → báo ⚠️ kèm cách tự xem). Mỗi dòng ✅/⚠️/❌ + kết luận.
3. **Tải** — app local: tải model/tài nguyên lần đầu có tiến trình; bản web: tải bộ cài đúng HĐH + hướng dẫn + lệnh 1 dòng.
4. **Hoàn tất** — "Thử ngay" chạy luôn chức năng chính; chỉ chỗ dùng API.

## Luật giao diện đã trả giá mới học được

- **Tương phản ≥ 4.5:1** cho chữ thường. Cam thương hiệu `#F67D1C` + chữ trắng chỉ 2.67:1 → giữ màu cam, đổi chữ sang đen
  (6.65:1), hoặc dùng cam đậm `#C2410C` cho chữ trên nền sáng. Đặt thành token (`--c-on-primary`, `--c-primary-ink`).
- Màu **lỗi** phải khác màu **thương hiệu** (đỏ `#DC2626` ≠ cam) — không thì thông báo lỗi trông như thông báo thường.
- **Không font pixel / font không dấu** cho tiêu đề tiếng Việt.
- Khổ **1280–1500px** (laptop phổ biến) hay bị bóp: hai cột trong form → một cột khi khung hẹp; ô chọn bị cắt tên.
- **375px**: grid ngoài cùng `minmax(0, 1fr)`; chuỗi dài (URL, code) `word-break: break-all`; vùng bấm ≥ 24px.
- Ít viền đen, viền 1px xám nhạt, bo góc, bóng mềm; bên phải màn rộng không để trống — cột phụ (Kết quả / Gần đây / Mẹo).
- Văn bản dài làm máy yếu lag → bộ đếm ký tự + cảnh báo theo ngưỡng + khoá nút khi vượt giới hạn.
- Thẻ/tag không được hỗ trợ (vd cảm xúc ngoài danh sách model học) → cảnh báo ngay khi gõ, giải thích vì sao.

## Soi giao diện bằng skill `ui-ux` (evondevKit)

- Nhờ "xem giúp / soi" → nhánh soi: đo bằng `scripts/probe.mjs` (Playwright, cài vào thư mục tạm) ở 6 khổ + quét bề rộng +
  chế độ tối; lập bảng Hỏng / Lệch hệ / Gu; **người tạo chọn dòng rồi mới sửa**.
- Chạy probe trên **bản sao** app (thư mục dữ liệu sao chép), chèn sẵn `localStorage` để popup không che.
- Sửa xong **đo lại** — lần sửa có thể sinh lỗi mới (đã gặp: đổi chữ trên nền cam làm nhãn GET nền xanh tụt tương phản).
- Ảnh trước/sau: chèn CSS tạm (`page.addStyleTag`) rồi chụp, chưa sửa file; trang `so-sanh.html` qua `python3 -m http.server`.
