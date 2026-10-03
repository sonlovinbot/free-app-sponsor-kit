---
name: free-app-sponsor-kit
description: Gắn "góc tài trợ" vào phần mềm / website MIỄN PHÍ vibe code — thẻ quảng cáo nhãn "Ad · Sponsor" có nút (i) mở thư ngỏ dạng phong bì giải thích vì sao có quảng cáo, thanh thông báo + báo phiên bản mới, khung "Phát triển bởi", link gắn UTM. Nội dung điều khiển từ xa bằng một file news.json (GitHub Pages): app local vẫn đổi được khi có mạng, mất mạng dùng bản đã lưu; website đọc thẳng. Dùng khi người dùng nói "gắn quảng cáo / ad sponsor / góc tài trợ / banner Coachio", "thêm phát triển bởi", "thông báo bản mới", "nhúng sponsor kit", "làm giống AI Audio Studio", hoặc đang làm một phần mềm miễn phí và cần chỗ quảng cáo nhỏ để bù chi phí. Có thêm "khung tài trợ" cho website/trang giới thiệu (nhiều chương trình: khoá học, e-learning, workshop, cộng đồng Zalo — tự xếp cái gần ngày lên đầu, nhãn GẤP, đếm ngược, hết hạn vẫn bấm được) và nhãn + popup "Về game" trong game 3D, điều khiển bằng một file sponsors.json — dùng khi nói "box sponsor", "đặt quảng cáo khoá học/workshop dưới trang", "popup giới thiệu game", "ad nào đặt ở link nào".
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
| `web/sponsors.js` + `web/sponsors.css` | **Khung tài trợ cho website** (nhiều chương trình, tự xếp theo độ gấp) + **nhãn/popup "Về game"** trong game — xem mục cuối |
| `templates/sponsors.json` | Dữ liệu mẫu: 4 chương trình (workshop, cộng đồng Zalo, khoá Zoom, e-learning) + bảng trang nào hiện gì |
| `scripts/validate_sponsors.py` | Kiểm `sponsors.json` trước khi push (`--urls` mở thử link đăng ký) |
| `examples/sponsor-box.html` | 4 cách gắn: lưới, thẻ rộng, nền tối, popup trong game |

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

## Khung tài trợ cho website & game (`sponsors.json`)

Khác `news.json` (1 thẻ nhỏ trong **app**), đây là khung **cuối trang web** quảng bá nhiều chương trình cùng lúc,
và nhãn "Về game" trong **game/app toàn màn hình**. Một file dữ liệu điều khiển mọi trang.

**Cài một lần:** chép `web/sponsors.js`, `web/sponsors.css`, `templates/sponsors.json` vào thư mục `sponsors/` của
trang chủ tổng hợp (vd repo `<user>.github.io` → `app.danghuuson.com/sponsors/`), ảnh vào `sponsors/img/`.
Trang khác (kể cả tên miền khác) gắn script tuyệt đối tới đó — Pages trả CORS `*` nên đọc được JSON.

**Dữ liệu** — mỗi chương trình trong `items`:

| Trường | Ý nghĩa |
|---|---|
| `id`, `campaign` | `campaign` → `utm_campaign` |
| `kind` | `workshop` · `community` (Zalo) · `course` (khoá Zoom) · `elearning` — quyết định nhãn + biểu tượng |
| `title`, `desc`, `short` | `short` = chữ ngắn trên nhãn trong game ("Workshop 3D") |
| `start` + `duration_min` | **sự kiện** (workshop, live): trước giờ → đếm ngược; trong giờ → LIVE; sau → "Đã diễn ra" |
| `deadline` + `deadline_label` | **hạn ưu đãi** (khoá học): "Ưu đãi đến 23:59 đêm mai" |
| không có cả hai | **không thời hạn** (e-learning): "Học mọi lúc", xếp sau các mục có ngày |
| `price`, `price_note` | dòng chữ dưới thẻ ("Miễn phí", "Học trọn đời", mã giảm giá). **Không ghi giá tiền** — validator chặn số tiền (đ, k, tr…); `price_old` đã bỏ |
| `url` | link đăng ký https. **Trống → tự ẩn** trên trang thật (`?spk_preview` mới hiện) |
| `image`, `fit`, `pos`, `bg`, `accent` | ảnh trong `img/`; bìa sách/ảnh dọc dùng `fit: contain` + `bg` cùng tông; `accent` = màu nhãn + nút |
| `cta`, `cta_popup`, `pitch` | chữ nút; chữ nút + câu mời trong popup game |

Giờ luôn ghi **kèm múi giờ** (`2026-10-03T19:30:00+07:00`) — validator chặn nếu thiếu.

**Trang nào hiện gì** — `pages.<tên>`: `items` (`["*"]` = tất cả), `source` (→ `utm_source`), `title`, `lead`,
`layout: "wide"` (1–2 thẻ ngang, thoáng). Trang `game` = popup trong game: lấy **chương trình còn hạn đầu tiên**
(workshop hết giờ → tự chuyển sang mục kế, vd e-learning).

**Tự động theo thời gian:** xếp LIVE → còn hạn gần nhất → không thời hạn → đã hết (mờ, xuống cuối, nút "Xem lại",
**vẫn bấm được**). ≤ 24 giờ: viền đỏ + "GẤP" + chấm nhấp nháy; ≤ 3 ngày: nhãn vàng. Đếm ngược tự cập nhật mỗi phút.
UTM: `utm_source`=`pages.<tên>.source`, `utm_medium`=`sponsor_box` (popup game: `game_popup`), `utm_campaign`,
`utm_content`=`<trang>-<vị trí>`. Trang đã có Meta Pixel → tự gửi `SponsorClick` (content_ids, content_type, placement).

**Gắn:** xem `examples/sponsor-box.html`.
- Cuối trang: `<div data-sponsor-page="hub"></div>` + 1 thẻ script. Trang luôn nền tối: thêm `data-theme="dark"`.
- Trong game: thẻ script có `data-game`, `data-desc`, `data-landing`, `data-source`, vị trí `data-pos`
  (4 góc) **hoặc** `data-anchor=".selector"` (đè đúng chỗ một chip có sẵn, vd "Tác giả", và ẩn chip đó; chip không
  có trên màn hình → nhãn ẩn). `data-hide-when="#hud:not(.hidden)"` ẩn nhãn lúc đang chơi.
  Dời vị trí theo màn hình bằng CSS của game: `body .spk-game.pos-bottom-left { bottom: 128px }` (**phải có `body`**
  — CSS của kit nạp sau nên cùng độ ưu tiên sẽ thắng).
- Popup không tự bật; khi mở, game **không nhận phím/chuột** (Esc đóng) để không bắn nhầm / xoay camera.

**Kiểm trước khi giao:**
- [ ] `python3 scripts/validate_sponsors.py sponsors/sponsors.json --urls` → 0 lỗi.
- [ ] Xem trước các mốc giờ bằng `?spk_preview&spk_now=2026-10-03T20:00:00%2B07:00` (LIVE / GẤP / đã hết).
- [ ] 1280px + 375px (điện thoại: vuốt ngang, thẻ sau ló ra), nền sáng/tối, không cuộn ngang.
- [ ] **Từng game, cả máy tính lẫn điện thoại**: nhãn không che nút/HUD (chụp màn hình rồi mới chọn góc).
      Thử trên game thật chưa deploy: Playwright `context.route("https://app.danghuuson.com/sponsors/**")` trả file
      local rồi chèn thẻ script (script `http://localhost` bị trang https chặn).
- [ ] Popup mở: bấm phím (W, Space) → game không nhận; Esc đóng; link có đủ 4 utm.

## Popup giới thiệu người phát triển (bấm "Phát triển bởi")

Kit 1.1: thêm `about` vào `SponsorKit.init` → khung "Phát triển bởi" thành **nút** mở popup (không nhảy sang Facebook):
ảnh tròn + bong bóng "Xin chào! 👋", tên, chức danh, giới thiệu ngắn, danh sách link (Facebook, fanpage, trang chủ
dự án — link không phải mạng xã hội tự gắn UTM `utm_content=about-popup`), dòng "Dựa trên …" (`basedOn`), và
**"Chương trình đang mở"**: quảng cáo đang chạy, **hiện lại kể cả khi người dùng đã bấm ✕** ở thẻ menu (vẫn tôn trọng
`start`/`end`). App có khung credit riêng thì gọi `SponsorKit.openAbout()` từ nút đó.

```js
about: {
  avatar: "/img/dev-avatar.jpg",          // ảnh đóng gói trong app (chạy offline)
  intro: "Mình làm phần mềm và game bằng AI, chia sẻ miễn phí…",
  links: [{ label: "Facebook …", note: "Trang cá nhân", url: "https://…", icon: "👤", utm: false }, …],
}
```
Link nên để ở `config/branding.json` rồi app điền vào mảng `links` (popup dựng lúc mở lần đầu).
Kiểm: tắt thẻ QC ở menu → mở popup vẫn thấy QC; popup cao hơn màn 768px vẫn mở ở **đầu** (focus `preventScroll`).

## Nhật ký phiên bản trong app — chỉ hiện thay đổi về sản phẩm

Bản cài gửi khách không cần biết các lần chỉnh quảng cáo / thư ngỏ. Trong `changelog.json` giữ đủ lịch sử (repo), thêm:
`"app": false` → ẩn cả mục; `"app_title"` / `"app_changes"` → bản hiển thị cho người dùng. Server trả bản đã lọc ở
`/api/changelog` (`?all=1` = đủ), script dựng trang giới thiệu lọc giống vậy.

## Thư ngỏ (popup phong bì)

Nền kraft, nắp gập tam giác, con dấu sáp ♥, giấy kem kẻ dòng, tem "FREE". Nội dung mặc định nói 4 ý, theo thứ tự:
phần mềm + web **hoàn toàn miễn phí** → có **một góc nhỏ** quảng cáo của `sponsorName` để có kinh phí làm bản tốt hơn →
QC chọn chung cho mọi người, **không dựa trên dữ liệu người dùng**, app không theo dõi, đóng bằng ✕ được →
cảm ơn; ký tên `developer`. Đổi lời bằng `letter: { title, paragraphs: [[["", "chữ thường"], ["b", "chữ đậm"]]], button }`.
Giữ đúng sự thật: nếu app CÓ gửi dữ liệu đi đâu thì sửa đoạn thứ ba cho đúng, không được hứa sai.

## Không làm
- Không chèn HTML / script từ feed, không nhận link `http:` hay `javascript:` (kit gắn bằng `textContent`).
- Không thêm theo dõi người dùng (pixel, analytics) vào **app chạy trên máy** để đo QC — đo bằng UTM ở trang đích.
  (Khung tài trợ trên website chỉ gửi `SponsorClick` khi trang đó vốn đã có Meta Pixel và đã ghi rõ ở chân trang.)
- Không hiện quá 1 thẻ QC + 2 thanh **trong app**; không popup QC tự bật (kể cả popup game); QC trong app không có ngày kết thúc.
- Không bỏ dòng ghi nhận dự án gốc (`basedOn`) của app dựa trên mã nguồn mở.
