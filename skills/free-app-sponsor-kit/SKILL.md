---
name: free-app-sponsor-kit
description: Gắn "góc tài trợ" vào phần mềm / website MIỄN PHÍ vibe code — thẻ quảng cáo nhãn "Ad · Sponsor" có nút (i) mở thư ngỏ dạng phong bì giải thích vì sao có quảng cáo, thanh thông báo + báo phiên bản mới, khung "Phát triển bởi", link gắn UTM. Nội dung điều khiển từ xa bằng một file news.json (GitHub Pages): app local vẫn đổi được khi có mạng, mất mạng dùng bản đã lưu; website đọc thẳng. Dùng khi người dùng nói "gắn quảng cáo / ad sponsor / góc tài trợ / banner Coachio", "thêm phát triển bởi", "thông báo bản mới", "nhúng sponsor kit", "làm giống AI Audio Studio", hoặc đang làm một phần mềm miễn phí và cần chỗ quảng cáo nhỏ để bù chi phí.
---

# Free App Sponsor Kit

Bộ code dùng lại cho mọi phần mềm miễn phí của **Đặng Hữu Sơn (CEO & Co-Founder LovinBot AI)**:
một góc quảng cáo nhỏ của **Coachio Academy** để bù chi phí phát triển, minh bạch với người dùng,
điều khiển từ xa không cần phát hành lại. Bản chạy thật đầu tiên: AI Audio Studio
(`github.com/sonlovinbot/vieneu-audio-studio`, thư mục `webapp/static/vendor/sponsor-kit/`).

## Có gì trong kit

| File | Vai trò |
|---|---|
| `kit/sponsor-kit.js` | Lõi, không phụ thuộc thư viện: đọc feed, lọc theo ngày/phiên bản/app, vẽ thẻ QC + thanh thông báo + khung credit, thư ngỏ phong bì, gắn UTM, nhớ nút ✕, lưu feed khi offline |
| `kit/sponsor-kit.css` | Giao diện; đổi màu theo app bằng biến `--sk-*` |
| `server/fastapi_news.py` | Proxy `/api/news` cho app local Python/FastAPI (cache đĩa 3 giờ, lọc trường, chỉ https) |
| `server/express_news.js` | Proxy tương tự cho Node/Express |
| `templates/news.json` | Feed mẫu: QC đang chạy + QC kế tiếp xếp lịch sẵn |
| `templates/HUONG-DAN-THONG-BAO.md` | Hướng dẫn cho chủ app: các trường, xếp lịch, an toàn |
| `scripts/validate_news.py` | Kiểm feed trước khi push (`--urls` mở thử link/ảnh) |
| `examples/integrate.html` | Đoạn HTML + `SponsorKit.init` mẫu |

## Quy trình gắn vào một phần mềm mới

**1. Thu thập cấu hình — dùng mặc định, chỉ hỏi cái chưa suy ra được** (thường chỉ tên app):

| Mục | Mặc định |
|---|---|
| `appName`, `appId` (slug `a_z_0_9`), `appVersion` | đọc từ code của app |
| `sponsorName` | Coachio Academy |
| `developer` | Đặng Hữu Sơn · CEO & Co-Founder LovinBot AI · https://www.facebook.com/danghuuson.182/ |
| `basedOn` | ghi nhận mã nguồn mở nếu app dựa trên model/dự án khác (bắt buộc giữ theo giấy phép) |
| `utm.medium` | `local_app` (chạy trên máy) · `website` · `extension` |
| Feed | `docs/news.json` trong repo của app, bật GitHub Pages (main → `/docs`). Nhiều app dùng chung một feed thì lọc bằng `apps` |

**2. Nhận dạng kiểu app → chọn `feedUrl`:**
- **App local có server** (FastAPI, Express…): chép `server/*` vào server, `feedUrl: "/api/news"`. Proxy lưu
  feed ra đĩa → mất mạng vẫn có bản cũ; tắt bằng biến môi trường `APP_NEWS=off`.
- **Website / app tĩnh không server / Electron**: `feedUrl` = link `news.json` trên GitHub Pages (Pages trả
  `Access-Control-Allow-Origin: *`). Kit tự lưu feed vào localStorage cho lần offline.

**3. Đặt vị trí theo đúng thứ tự này** (đã kiểm ở AI Audio Studio):
- Thẻ QC `slots.side`: cột bên/sidebar, **ngay trên** khung "Phát triển bởi". Chỉ 1 thẻ. Ẩn ở màn < 900px.
- Thanh thông báo `slots.top`: trên tiêu đề trang, tối đa 2 thanh; thanh "Đã có bản mới" tự sinh.
- Khung credit `slots.credit` (hoặc giữ khung credit sẵn có của app).
- Chép `kit/*` vào thư mục tĩnh (vd `static/vendor/sponsor-kit/`), thêm `<link>` + `<script>`, gọi
  `SponsorKit.init({...})` một lần — mẫu ở `examples/integrate.html`.
- Ánh xạ màu: đặt `--sk-surface/--sk-border/--sk-text/--sk-title/--sk-muted/--sk-chip/--sk-link/--sk-accent-soft/--sk-font`
  sang token của app trong CSS của app (không sửa file kit).

**4. Nội dung feed** — sửa `docs/news.json`, chạy `python3 <skill>/scripts/validate_news.py docs/news.json --urls`, push.
Luật bắt buộc (kit và validator cùng ép):
- Mọi QC (`placement: sidebar` hoặc `tone: promo`) **phải có `end`** = ngày cuối còn hiện; ngày theo giờ máy người
  dùng; thiếu `end` thì không hiện. Muốn QC sau tự thay → thêm mục mới với `start` = ngày hôm sau, đặt **sau** QC hiện tại.
- `id` đổi khi đổi nội dung (người đã bấm ✕ id cũ vẫn thấy QC mới). `campaign` (mặc định = id) đi vào `utm_campaign`.
- Ảnh QC: ngang ~2:1, rộng ~960px, để ở `docs/ads/`. **Mở thử ảnh trước** — og:image của trang đích có thể hỏng.
- UTM tự gắn: `utm_source`=appId, `utm_medium`, `utm_campaign`, `utm_content`=`<vị trí>_v<phiên bản>`. Link đã có utm thì giữ nguyên.

**5. Kiểm trước khi giao** (mỗi dòng đã từng sai thật):
- [ ] Mở app thật: thẻ có nhãn `AD · SPONSOR` + nút (i); bấm (i) mở thư, Esc / nền / nút đóng được, focus về chỗ cũ.
- [ ] Con dấu ♥ không đè tiêu đề thư (đo `boundingBox` seal < title), thư cuộn được ở 375px, dark mode vẫn đọc rõ.
- [ ] Link trong thẻ có đủ 4 tham số utm.
- [ ] **Giả lập đồng hồ** (`page.clock.setFixedTime`, `timezoneId: "Asia/Ho_Chi_Minh"`): 23:30 ngày `end` còn hiện,
      00:05 hôm sau mất và QC xếp lịch kế tiếp tự lên. (Bản đầu dùng UTC → ở VN QC sống thêm 7 tiếng.)
- [ ] Feed thử có mục độc (`"link": "javascript:alert(1)"`, `"title": "<img onerror>"`) → không chạy, không hiện link.
- [ ] **Thử xong phải xoá cache feed thử** (file cache của proxy + `localStorage <prefix>_feed`) — đã từng để
      lọt QC "Webinar" giả vào máy thật vì cache giữ dữ liệu thử khi feed thật chưa lên mạng.
- [ ] Sau khi push: `curl` link `news.json` và ảnh trên Pages ra 200 rồi mới báo xong.

**6. Phát hành bản mới của app:** tăng `latest_version` trong feed → mọi máy bản cũ thấy thanh "Đã có bản mới".

## Thư ngỏ (popup phong bì)

Nền kraft, nắp gập tam giác, con dấu sáp ♥, giấy kem kẻ dòng, tem "FREE". Nội dung mặc định nói 4 ý, theo thứ tự:
phần mềm + web **hoàn toàn miễn phí** → có **một góc nhỏ** quảng cáo của `sponsorName` để có kinh phí làm bản tốt hơn →
QC chọn chung cho mọi người, **không dựa trên dữ liệu người dùng**, app không theo dõi, đóng bằng ✕ được →
cảm ơn; ký tên `developer`. Đổi lời bằng `letter: { title, paragraphs: [[["", "chữ thường"], ["b", "chữ đậm"]]], button }`.
Giữ đúng sự thật: nếu app CÓ gửi dữ liệu đi đâu thì sửa đoạn thứ ba cho đúng, không được hứa sai.

## Không làm
- Không chèn HTML / script từ feed, không nhận link `http:` hay `javascript:` (kit gắn bằng `textContent`).
- Không thêm theo dõi người dùng (pixel, analytics) vào app để đo QC — đo bằng UTM ở trang đích.
- Không hiện quá 1 thẻ QC + 2 thanh; không popup QC tự bật; không QC không có ngày kết thúc.
- Không bỏ dòng ghi nhận dự án gốc (`basedOn`) của app dựa trên mã nguồn mở.
