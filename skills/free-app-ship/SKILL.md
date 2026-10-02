---
name: free-app-ship
description: Quy trình đưa một phần mềm MIỄN PHÍ vibe code từ "chạy được trên máy" tới "chia sẻ được cho người dùng" — hỏi đáp với người tạo, kiểm tra bảo mật trước khi share (API key, token, bản quyền, dữ liệu cá nhân trong ảnh/log), dọn repo, đóng gói zip + cài 1 lệnh (macOS/Windows/Linux), GitHub Releases, cập nhật phiên bản + changelog + báo bản mới, README, trang giới thiệu GitHub Pages (video, ảnh, nghe thử), giao diện + onboarding, quảng cáo (dùng skill free-app-sponsor-kit). Dùng khi người dùng nói "đẩy lên cho người dùng", "phát hành", "release", "share phần mềm", "đóng gói", "tạo bộ cài", "lên GitHub", "làm trang giới thiệu", "check security trước khi share", "cập nhật phiên bản mới", "ship", hoặc vừa vibe code xong một app và muốn đưa ra ngoài.
---

# Free App Ship — từ app chạy được tới bản chia sẻ an toàn

Rút ra từ dự án thật **AI Audio Studio** (Đặng Hữu Sơn, 09–10/2026): một app local dựa trên mã nguồn mở,
đi qua đủ các bước dọn repo → bộ cài → GitHub Releases → trang Pages → quảng cáo → nhiều vòng cập nhật.
Mỗi bước dưới đây có lý do từ một lần làm sai thật — xem `references/07-bai-hoc.md`.

## Bốn chế độ — nhận từ câu người dùng, không hỏi

| Người dùng nói | Chế độ | Mở |
|---|---|---|
| "chuẩn bị phát hành / đẩy lên cho người dùng / share" (lần đầu) | **A. Phát hành lần đầu** — đi hết 7 bước dưới | tất cả, theo thứ tự |
| "ra bản mới / cập nhật phiên bản / release x.y" | **B. Cập nhật** — bước 3 → 4 → 6 → 7 | `04-dong-goi-phat-hanh.md` mục "Mỗi lần ra bản" |
| "check security / kiểm tra trước khi share" | **C. Chỉ kiểm bảo mật** — bước 3, giao báo cáo | `03-bao-mat-truoc-khi-share.md` |
| "làm trang giới thiệu / README / nhúng video" | **D. Chỉ trang giới thiệu** — bước 5 | `05-readme-va-github-pages.md` |

## Bảy bước (chế độ A)

1. **Hỏi người tạo** — bộ câu hỏi ngắn ở `references/02-hoi-dap-nguoi-tao.md`. Câu nào suy ra được từ code
   thì tự trả lời, chỉ hỏi phần còn lại, **gom một lần** (AskUserQuestion). Ghi câu trả lời vào `SHIP.md` ở gốc repo
   để lần sau không hỏi lại.
2. **Dọn repo** — bỏ thứ không cần cho người dùng cuối, giữ ghi nhận bản quyền. `references/01-quy-trinh-tong.md` mục "Dọn repo".
3. **Kiểm bảo mật + bản quyền** — chạy `scripts/preship_check.sh <repo>`; đọc từng dòng, xử lý hết ĐỎ trước khi
   push công khai. Chi tiết + cách xử lý từng loại: `references/03-bao-mat-truoc-khi-share.md`.
4. **Đóng gói + phát hành** — zip theo hệ điều hành, script cài 1 lệnh, GitHub Releases, link "latest" cố định.
   Mẫu ở `templates/`, quy trình ở `references/04-dong-goi-phat-hanh.md`.
5. **README + trang giới thiệu** — README tiếng Việt, trang GitHub Pages có video nhúng, ảnh chụp từ bản app sạch,
   tải trực tiếp, xử lý sự cố. `references/05-readme-va-github-pages.md`.
6. **Giao diện + trải nghiệm lần đầu** — onboarding, độ tương phản, khổ màn hình. `references/06-giao-dien-ux.md`.
   Có skill `ui-ux` (evondevKit) thì dùng nó để soi.
7. **Sau phát hành** — báo bản mới + quảng cáo từ xa bằng skill `free-app-sponsor-kit`; ghi bài học mới vào
   `references/07-bai-hoc.md` của skill này.

## Luật xuyên suốt

- **Hỏi trước khi làm việc ra bên ngoài**: tạo repo công khai, push, tạo release, bật Pages, đổi website repo — xác nhận
  tài khoản, tên repo, công khai/riêng tư một lần ở bước 1; sau đó làm theo đúng câu trả lời.
- **Không bao giờ push khi `preship_check` còn ĐỎ.** Lỡ push bí mật lên repo công khai → coi như đã lộ: thu hồi/đổi
  khoá trước, xoá khỏi lịch sử sau (`03`, mục "Lỡ đẩy lên rồi").
- **Thử trên bản sao, không trên dữ liệu thật** của người tạo (lịch sử, giọng đã lưu…). Chụp ảnh giới thiệu từ một bản
  app sạch với dữ liệu demo.
- **Kiểm bằng chạy thật, không bằng đọc code**: cài mới từ zip vào thư mục trống, mở link release/Pages bằng `curl`,
  giả lập đồng hồ cho lịch hết hạn, mở trang bằng trình duyệt ở 375px và 1280px.
- **Báo đúng sự thật**: bước nào chưa thử được (vd không có máy Windows) thì nói rõ là chưa thử.
- **Ghi nhận tác giả gốc** khi dựa trên mã nguồn mở — giữ LICENSE, ghi tên dự án gốc ở README, app, trang Pages.

## Tài liệu

| File | Nội dung |
|---|---|
| `references/01-quy-trinh-tong.md` | Bản đồ toàn bộ quy trình, lệnh cụ thể từng bước, dọn repo |
| `references/02-hoi-dap-nguoi-tao.md` | Bộ câu hỏi cho người tạo + mẫu `SHIP.md` |
| `references/03-bao-mat-truoc-khi-share.md` | Bảo mật, bản quyền, dữ liệu cá nhân; xử lý khi lỡ lộ |
| `references/04-dong-goi-phat-hanh.md` | Zip, cài 1 lệnh, Gatekeeper/SmartScreen, Releases, phiên bản, changelog |
| `references/05-readme-va-github-pages.md` | README, Pages, nhúng video/âm thanh (giới hạn của GitHub), ảnh |
| `references/06-giao-dien-ux.md` | Onboarding, tương phản, khổ màn hình, font tiếng Việt |
| `references/07-bai-hoc.md` | Nhật ký bài học + phản hồi của người tạo, có ngày |
| `scripts/preship_check.sh` | Quét bí mật, file rác, dữ liệu cá nhân, bản quyền, CI lạ |
| `scripts/verify_release.sh` | Sau khi phát hành: link tải, Pages, news.json đều trả 200 |
| `templates/` | `install-online.sh/.ps1`, `build-installers.sh`, `RELEASE_NOTES.md`, `changelog.json`, `README.md`, `.gitignore`, `SHIP.md` |
