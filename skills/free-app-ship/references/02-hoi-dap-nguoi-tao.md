# 02 · Hỏi đáp với người tạo

Mục tiêu: lấy đủ quyết định **một lần**, ghi vào `SHIP.md` ở gốc repo, lần sau đọc lại thay vì hỏi.

## Cách hỏi

1. **Tự trả lời trước** từ code và máy: tên app (`branding.json`, `package.json`, `<title>`), phiên bản, có server không,
   hệ điều hành chạy được, tài khoản GitHub đang đăng nhập (`gh auth status`), dự án gốc + giấy phép (`LICENSE`, `pyproject`).
2. **Chỉ hỏi phần còn thiếu**, gom 1 lần bằng AskUserQuestion (tối đa 4 câu/lần), mỗi câu có phương án khuyên dùng đứng đầu.
3. Ghi kết quả vào `SHIP.md` (mẫu ở `templates/SHIP.md`), commit cùng repo.

## Bộ câu hỏi

### Nhận diện
- Tên phần mềm hiển thị? Tên repo (slug)? *(gợi ý: tên thương hiệu mẹ + chức năng, vd "LovinAudio")*
- Người phát triển hiển thị ở đâu, chức danh, link (Facebook/website)?
- Dựa trên dự án/model mã nguồn mở nào? Giấy phép gì? → bắt buộc ghi nhận.

### Phát hành
- Tài khoản GitHub nào? Repo **công khai** (người ngoài tải được, link "latest" chạy) hay **riêng tư**?
- Phát cho hệ điều hành nào? Có máy Windows/Linux để thử không? (không có → ghi rõ "chưa thử" khi giao)
- Có tự chạy khi mở máy không? Cổng mặc định?
- Có cần trang giới thiệu (GitHub Pages)? Video YouTube giới thiệu (link)? Ảnh banner?

### Kiếm tiền / quảng cáo
- Có góc quảng cáo không? Nhà tài trợ? Quảng cáo đầu tiên: tiêu đề, link, ảnh, **ngày kết thúc**?
- Theo dõi bằng UTM: `utm_source` (slug app), `utm_medium` (`local_app` / `website`)?

### Dữ liệu người dùng
- App lưu gì trên máy (lịch sử, file, khoá)? Ở đâu? Có gửi gì lên mạng không? → đưa vào thư ngỏ + README cho đúng sự thật.
- Có dùng API key của **người tạo** không (OpenAI, ElevenLabs…)? → **không được đóng gói khoá của mình** vào bản chia sẻ;
  chuyển sang để người dùng nhập khoá của họ, hoặc chạy qua server riêng.

### Hỗ trợ
- Người dùng gặp lỗi thì liên hệ đâu? (link Facebook/Zalo/email) → đưa vào mục "Không cài được?".

## Mẫu ghi nhanh (dán vào SHIP.md)

```markdown
## Quyết định phát hành (cập nhật 2026-10-02)
- Tên: AI Audio Studio · repo: sonlovinbot/vieneu-audio-studio (public)
- Phát triển bởi: Đặng Hữu Sơn — CEO & Co-Founder LovinBot AI — https://www.facebook.com/danghuuson.182/
- Dựa trên: VieNeu-TTS (Phạm Nguyễn Ngọc Bảo), Apache 2.0 — giữ LICENSE + ghi nhận
- Hệ điều hành: macOS / Windows / Linux · đã thử thật: macOS (chip M) · Windows: chưa thử
- Trang: https://sonlovinbot.github.io/vieneu-audio-studio/ · video: https://youtu.be/…
- Quảng cáo: Coachio Academy · feed docs/news.json · utm_source=ai_audio_studio, utm_medium=local_app
- Dữ liệu: lưu ở ~/.vieneu (giọng, lịch sử) · không gửi lên mạng · không dùng API key của người tạo
```
