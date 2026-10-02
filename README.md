# 💌 Free App Sponsor Kit — skill cho Claude Code

Gắn **"góc tài trợ"** vào phần mềm / website **miễn phí** bạn vibe code — minh bạch với người dùng,
điều khiển từ xa, không cần phát hành lại phần mềm.

<p>
  <img src="assets/the-quang-cao.png" alt="Thẻ quảng cáo Ad · Sponsor" height="300">
  &nbsp;
  <img src="assets/thu-ngo.png" alt="Thư ngỏ dạng phong bì" height="300">
</p>

## Có gì

- **Thẻ quảng cáo** nhãn `AD · SPONSOR` + nút **(i)** mở **thư ngỏ dạng phong bì**: phần mềm hoàn toàn miễn phí, một góc
  nhỏ quảng cáo giúp có kinh phí phát triển, quảng cáo không dựa trên dữ liệu người dùng.
- **Thanh thông báo** trên đầu trang (sự kiện, bảo trì) và **"Đã có bản mới"** tự sinh khi tăng `latest_version`.
- **Khung "Phát triển bởi"** dùng chung.
- **UTM tự động**: `utm_source` = app, `utm_medium` = `local_app` / `website`, `utm_campaign`, `utm_content` = vị trí + phiên bản.
- **Lịch tự tắt**: mọi quảng cáo bắt buộc có ngày kết thúc (theo giờ máy người dùng); xếp sẵn quảng cáo kế tiếp, đến ngày tự thay.
- **Một file `news.json` điều khiển tất cả** (GitHub Pages): app chạy local vẫn đổi được khi có mạng, mất mạng dùng bản đã lưu;
  website đọc thẳng. Một feed dùng chung nhiều app (lọc bằng `apps`).
- **An toàn**: chỉ nhận chữ + link https, không chạy mã từ xa, không theo dõi người dùng.

## Cài vào Claude Code

```
/plugin marketplace add sonlovinbot/free-app-sponsor-kit
/plugin install free-app-sponsor-kit@sonlovinbot-skills
```

Hoặc chép tay thư mục `skills/free-app-sponsor-kit` vào `~/.claude/skills/`.

## Dùng

Khi đang làm một phần mềm miễn phí, chỉ cần nói với Claude:

> *"Gắn sponsor kit vào app này"* · *"thêm góc quảng cáo Coachio và khung phát triển bởi"* · *"làm giống AI Audio Studio"*

Claude sẽ chép bộ code, đặt vị trí, nối feed, gắn UTM và chạy bộ kiểm tra (giả lập đồng hồ ngày hết hạn, thử mục độc,
dọn cache thử). Chi tiết quy trình: [`skills/free-app-sponsor-kit/SKILL.md`](skills/free-app-sponsor-kit/SKILL.md).

| Thư mục | Nội dung |
|---|---|
| `kit/` | `sponsor-kit.js` + `sponsor-kit.css` — không phụ thuộc thư viện |
| `server/` | Proxy `/api/news` cho FastAPI và Express (cache đĩa khi offline) |
| `templates/` | `news.json` mẫu, hướng dẫn đăng thông báo, chỗ để ảnh quảng cáo |
| `scripts/validate_news.py` | Kiểm feed trước khi push (`--urls` mở thử link và ảnh) |
| `examples/integrate.html` | Đoạn gắn mẫu |

Bản chạy thật: [AI Audio Studio](https://github.com/sonlovinbot/vieneu-audio-studio) — giọng nói AI tiếng Việt chạy trên máy tính.

---
Phát triển bởi **[Đặng Hữu Sơn](https://www.facebook.com/danghuuson.182/)** — CEO & Co-Founder LovinBot AI · MIT License
