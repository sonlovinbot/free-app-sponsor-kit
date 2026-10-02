# 03 · Bảo mật, bản quyền, dữ liệu cá nhân — trước khi share

Chạy: `bash <skill>/scripts/preship_check.sh <thư-mục-repo>` → báo ĐỎ (phải sửa) / VÀNG (xem lại) / XANH.
Script là lưới lọc thô; **đọc kết quả bằng mắt**, rồi đi tiếp bảng dưới cho phần máy không bắt được.

## 1. Bí mật (API key, token, mật khẩu)

| Kiểm | Cách |
|---|---|
| Khoá dạng chuẩn trong file đã commit | script quét: `sk-…` (OpenAI), `sk-ant-…`, `hf_…`, `ghp_/gho_/github_pat_…`, `AKIA…` (AWS), `AIza…` (Google), `xox[bp]-…` (Slack), `-----BEGIN … PRIVATE KEY` |
| Gán cứng `api_key = "…"`, `token: "…"`, `password=` | script quét; loại trừ placeholder `<API_KEY>`, `your-key-here`, chuỗi rỗng |
| `.env`, `*.pem`, `*.key`, `credentials*.json`, `token*.json` bị commit | script liệt kê; phải nằm trong `.gitignore` |
| **Lịch sử git**, không chỉ bản hiện tại | `git log -p --all | grep -E "<mẫu khoá>"` — file đã xoá vẫn còn trong lịch sử |
| File phiên làm việc của công cụ (`.gstack/browse.json` chứa token, log trình duyệt) | script báo ĐỎ; thêm `.gstack/` vào `.gitignore` |
| Khoá của **người tạo** dùng trong app (gọi API trả phí) | không đóng gói; cho người dùng nhập khoá của họ (lưu localStorage / file cấu hình riêng trên máy họ) |

**Lỡ đẩy bí mật lên rồi** (đã xảy ra: token phiên trình duyệt lọt vào repo công khai):
1. **Thu hồi / đổi khoá ngay** (trang quản lý của nhà cung cấp; với phiên cục bộ: tắt tiến trình). Coi như đã lộ.
2. Xoá khỏi lịch sử: repo vừa tạo, chưa ai clone → sửa commit (`git commit --amend` / rebase) rồi `git push --force`.
   Repo đã có người dùng → `git filter-repo --path <file> --invert-paths`, báo người dùng clone lại.
3. Thêm mẫu vào `.gitignore`, chạy lại `preship_check`.
4. Báo người tạo đúng sự thật: lộ cái gì, đã thu hồi chưa, còn rủi ro gì.

## 2. Bản quyền & giấy phép

- Dự án dựa trên mã nguồn mở: **giữ file LICENSE gốc**, ghi tên tác giả gốc ở README, trong app ("Dựa trên…") và trang Pages.
  Apache 2.0 / MIT cho phép thương mại + quảng cáo nhưng bắt buộc giữ thông báo bản quyền. GPL: phần mềm phái sinh phải mở mã
  cùng giấy phép — hỏi người tạo trước khi đóng gói kèm quảng cáo.
- Model AI có giấy phép riêng (có model cấm thương mại / cấm dùng giọng người thật) → đọc model card.
- Ảnh, font, nhạc, video trong app/trang: có quyền dùng không? Font Google Fonts (OFL) dùng được. Ảnh lấy từ trang khác → hỏi.
- Không dùng tên/logo thương hiệu người khác như của mình.
- Repo phái sinh: đổi `project.urls` / `homepage` sang repo của mình, nhưng không xoá dòng tác giả gốc trong `authors`.

## 3. Dữ liệu cá nhân trong thứ sắp chia sẻ

| Nguồn hay lọt | Xử lý |
|---|---|
| Ảnh chụp màn hình (README, Pages): lịch sử, tên giọng riêng, email, đường dẫn máy | Chụp từ **bản app sạch** (thư mục dữ liệu riêng, nội dung demo) — không chụp app đang dùng |
| Audio/giọng clone của người thật | Không đưa giọng clone riêng của người tạo vào bản công khai trừ khi họ đồng ý |
| Đường dẫn tuyệt đối `/Users/<tên>/…`, `C:\Users\…` trong code/log | script báo VÀNG; thay bằng đường dẫn tương đối / biến |
| Email cá nhân trong code (ngoài phần tác giả có chủ đích) | script liệt kê để người tạo xác nhận |
| Log, cache, file dữ liệu thử (`*.log`, `history.json`, `news-cache.json`) | không commit; dọn cache thử trên máy sau khi test |

## 4. Cấu hình nguy hiểm khi share

- Server nghe `0.0.0.0` mặc định → ai cùng mạng Wi-Fi cũng gọi được API. Mặc định nên là `127.0.0.1`.
- CORS `*` trên API có hành động (xoá, ghi file) → giới hạn.
- Endpoint quản trị (đổi model, xem log) không có khoá → khoá lại khi chạy công khai.
- Nội dung tải từ xa (quảng cáo, thông báo) phải gắn bằng `textContent`, chỉ nhận `https` — đúng như sponsor-kit.
- CI/CD thừa hưởng từ dự án gốc (publish PyPI/npm, deploy) → xoá, tránh chạy bằng bí mật không có / lỗi mỗi lần release.

## 5. Kết quả giao cho người tạo

Một bảng ngắn: mục · kết quả (✅ / ⚠️ / ❌) · đã làm gì. Ví dụ dòng: *"Bí mật trong lịch sử git — ✅ quét 214 commit, không có."*
Không nói "an toàn tuyệt đối"; nói đã kiểm những gì.
