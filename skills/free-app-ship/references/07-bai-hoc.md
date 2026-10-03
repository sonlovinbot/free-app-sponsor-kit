# 07 · Nhật ký bài học & phản hồi của người tạo

Dự án gốc: AI Audio Studio (09–10/2026). **Thêm dòng mới ở cuối mỗi dự án** — ngày, chuyện gì, rút ra gì.
Trước khi bắt đầu một bước, lướt cột "Bước" để không lặp lỗi cũ.

## Lỗi kỹ thuật đã gặp

| Ngày | Chuyện gì | Bài học | Bước |
|---|---|---|---|
| 01/10 | Thư mục làm việc chưa phải git repo dù người dùng bảo "commit" | Kiểm `git status`; chưa có thì `git init` + commit đầu, nói rõ đã khởi tạo | 1 |
| 01/10 | CI `Publish to PyPI` của dự án gốc chạy lỗi ở **mọi** lần release (3 email lỗi) | Xoá `.github/workflows` của upstream khi tách repo | 2 |
| 01/10 | Bỏ Gradio (194 MB) làm mất FastAPI/uvicorn — trước đó chỉ được cài kèm Gradio | Khai báo trực tiếp mọi thư viện app dùng; **cài mới từ zip vào thư mục trống** để thử | 2 |
| 01/10 | Test sinh audio qua API khi lịch sử đã đầy 50/50 → đẩy mất 1 lượt cũ nhất của người tạo | Không test trên dữ liệu thật: gọi thẳng model bằng script, hoặc chạy bản sao với thư mục dữ liệu riêng | mọi bước |
| 01/10 | Git rm cả thư mục cũng xoá file trên máy người tạo | Báo trước; chỉ ra chỗ khôi phục (lịch sử git / bản backup) | 2 |
| 01/10 | Thư mục `promo/` (video nặng) của người tạo suýt bị `git add -A` | Thư mục lạ không do mình tạo → `.git/info/exclude`, không đụng | 1 |
| 01/10 | macOS 15 chặn `install.command` tải từ trình duyệt; "chuột phải → Open" **hết tác dụng** | Cài 1 lệnh (curl) để không bị gắn cờ cách ly; hướng dẫn Open Anyway; cảnh báo lớn ở README | 4 |
| 01/10 | `xattr -r` báo "Option -r not recognized" | Máy có `xattr` của Python che bản hệ thống → gọi `/usr/bin/xattr` | 4 |
| 02/10 | Nhúng YouTube / audio vào README không được | GitHub lọc iframe/audio; CSP chỉ cho `user-attachments` → làm trang Pages | 5 |
| 02/10 | GitHub trả trang "Unicorn" cho trình duyệt tự động | Kiểm bằng `curl` header CSP / mã HTTP thay vì trình duyệt | 5 |
| 02/10 | Dữ liệu thông báo **thử** (webinar giả) nằm trong cache của app thật vì feed thật chưa lên mạng | Thử xong **xoá cache** (file proxy + localStorage) trước khi làm việc khác | 7 |
| 02/10 | So ngày hết hạn bằng `toISOString()` (UTC) → QC ở VN sống thêm 7 tiếng | So theo giờ máy người dùng; thử bằng đồng hồ giả + `timezoneId` | 7 |
| 02/10 | og:image của trang đích (khoá học) là PNG hỏng | Mở thử mọi ảnh trước khi dùng; tự dựng ảnh QC từ ảnh chụp trang, lưu `docs/ads/` | 5, 7 |
| 02/10 | **Token phiên trình duyệt (`.gstack/browse.json`) lọt vào repo công khai** khi chạy test trong thư mục skill | `preship_check` trước mọi push; `.gstack/` vào `.gitignore`; lỡ lộ → tắt phiên/thu hồi, sửa commit, force-push repo mới | 3 |
| 02/10 | Sửa màu chữ trên nền cam làm nhãn GET nền xanh tụt tương phản | Đo lại toàn bộ sau khi sửa; đổi biến dùng chung thì soát mọi chỗ dùng | 6 |
| 02/10 | Popup onboarding che nút khi đo bằng trình duyệt mới | Chèn `localStorage` bằng `addInitScript`, hoặc chạy bản sao có script đánh dấu "đã xem" | 6 |
| 02/10 | Model đọc "VieNeu" thành "vai nu" (kiểu tiếng Anh) | Viết phiên âm cho model, **hiển thị** tên gốc (người tạo yêu cầu "demo phải show đúng tên gốc") | 5 |
| 03/10 | Script kiểm báo "trang chưa có bản mới" dù trang đã có | `curl … \| grep -q` + `set -o pipefail`: grep dừng sớm → curl bị SIGPIPE → báo sai. Tải vào biến trước rồi mới grep | 7 |
| 03/10 | Script kiểm báo "Thiếu LICENSE" dù có | `ls LICENSE* COPYING*` lỗi khi một mẫu không khớp → dùng `ls -d … \| head -1` và kiểm chuỗi rỗng. **Viết script kiểm thì thử cả trên repo có lỗi cài sẵn lẫn repo sạch** | 3 |
| 03/10 | Hỏi nên xác minh `danghuuson.com` hay `app.danghuuson.com`; muốn `app…/a` hay `a.…` | Xác minh tên miền gốc là đủ; dùng repo `<user>.github.io` + CNAME để mọi dự án thành `app…/<repo>`. Trang 404 lúc đầu là do chưa có repo này | 5 |
| 03/10 | Khung tài trợ: CSS dời vị trí nhãn trong game không ăn | CSS của kit nạp **sau** CSS trang → cùng độ ưu tiên thì kit thắng. Ghi đè bằng `body .spk-game.pos-…` | 5 |
| 03/10 | Thử script mới trên game thật (https) bằng `http://localhost` → không chạy | Trang https chặn script http. Dùng Playwright `context.route()` trả file local cho đúng URL thật | 6 |
| 03/10 | Nhãn đặt góc trên trái che nút "Động tác" ở điện thoại; góc dưới trái đè chân trang | **Chụp từng game ở 1280px và 390px trước khi chọn góc**; đè đúng chỗ chip có sẵn (`data-anchor`) hoặc ẩn khi đang chơi (`data-hide-when`) | 6 |
| 03/10 | Phần tử `position: fixed` (nền popup) lệch khi cha có `transform` | `transform` tạo khung chứa mới cho con fixed → bỏ transform của cha khi popup mở | 6 |
| 03/10 | Ảnh trong thẻ bị trống khi chụp màn hình | `loading="lazy"` chưa kịp tải khi chụp phần tử dưới màn hình → ảnh nhỏ (vài chục KB) thì bỏ lazy | 6 |
| 30/09 | HF Space từ chối file nhị phân push thẳng | Zip/ảnh lớn qua Git LFS — hoặc để bộ cài ở GitHub Releases | 4 |

## Phản hồi của người tạo (gu & yêu cầu lặp lại)

| Ngày | Người tạo nói | Áp dụng từ nay |
|---|---|---|
| 01/10 | "Bên phải giao diện trống quá", "line đen không nên nhiều" | Màn rộng có cột phụ hữu ích; viền mảnh xám, ít đường kẻ đậm |
| 01/10 | "Ghi rõ tôi là người phát triển, nhưng dựa trên model AI của …" | Khung "Phát triển bởi" + "Dựa trên …" ở app, README, Pages |
| 01/10 | "Phát triển bởi Đặng Hữu Sơn — CEO & Co-Founder LovinBot AI" | Dùng đúng chức danh này mặc định |
| 01/10 | "Giới hạn 5000 dài quá sẽ lag, cần bộ đếm" | Bộ đếm ký tự + ngưỡng cảnh báo (1.500 / 3.000) + khoá nút khi vượt (giới hạn là **ký tự**, không phải từ) |
| 01/10 | "Thêm cảm xúc được không?" | Kiểm model học gì trước khi hứa; không được thì đưa giải pháp thay (giọng cảm xúc qua clone) + giải thích trong app |
| 01/10 | "Không phải ai cũng biết cài, cần onboarding" | Onboarding 4 bước, nói rõ "app chạy trên máy, tắt máy thì không dùng được" |
| 01/10 | "Bỏ tài liệu gốc tiếng Anh", "repo nhiều file thừa, bỏ cho nhẹ" | README chỉ tiếng Việt của sản phẩm; dọn repo theo bảng ở `01` |
| 02/10 | "Nhúng video vào để không cần click qua YouTube" | Nói thẳng giới hạn GitHub, đưa giải pháp Pages ngay |
| 02/10 | "Thêm lưu ý khi không cài được", "show đường dẫn tải trực tiếp" | Mục "Không cài được?" + 3 nút tải có phiên bản/dung lượng trên Pages |
| 02/10 | "Bỏ font pixel" | Tiêu đề Be Vietnam Pro; không font không dấu |
| 02/10 | "Box quảng cáo ghi Ad · Sponsor, mỗi quảng cáo phải có lịch tự mất" | Nhãn + (i) thư ngỏ; `end` bắt buộc |
| 02/10 | "Thêm UTM để biết từ AI Audio Studio local app" | UTM tự gắn: source = app, medium = local_app |
| 02/10 | "Popup dễ thương, thư ngỏ, nền kem, như phong bì" | Thư ngỏ trong `free-app-sponsor-kit` |
| 02/10 | "Brand dùng xuyên suốt kiểu 7Audio, 7Banner" | Gợi ý thương hiệu mẹ + hậu tố; ưu tiên tận dụng thương hiệu sẵn có (Lovin + …) |
| 03/10 | "Box sponsor đẹp, hài hoà, cái nào gần ngày thì gấp, ưu tiên; phân loại khoá / e-learning; hết hạn vẫn click được" | Khung `sponsors.json`: tự xếp theo độ gấp, nhãn GẤP + đếm ngược, nhãn loại có biểu tượng, hết hạn mờ nhưng vẫn là link |
| 03/10 | "Cho tôi xem trước preview" | Dựng bản xem trước chạy local (có tham số giả lập giờ) và mở cho người tạo **trước** khi đưa lên trang thật |
| 03/10 | "2 banner cách nhau ra, thoải mái, không nhồi nhét" | Trang dự án dùng `layout: "wide"` — 1–2 thẻ ngang, khoảng cách rộng |
| 03/10 | "Trong game có tag và popup dễ thương: giới thiệu game, tác giả, tham gia workshop" | Nhãn "Về game" + popup trong `sponsors.js`; không tự bật, không che HUD |

## Cách làm việc người tạo thích

- Trả lời tiếng Việt, ngắn, có bảng; nói thẳng giới hạn và rủi ro, kèm phương án thay thế.
- Tự quyết các mặc định hợp lý, chỉ hỏi khi thật sự cần (tài khoản, công khai/riêng tư, nội dung quảng cáo).
- Mỗi lần xong: phiên bản mới + release + Pages cập nhật + app trên máy chạy bản mới.
