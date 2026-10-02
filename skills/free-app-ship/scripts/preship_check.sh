#!/usr/bin/env bash
# Kiểm tra trước khi chia sẻ phần mềm: bí mật, file nhạy cảm, dữ liệu cá nhân, bản quyền, CI lạ.
#   bash preship_check.sh [thư-mục-repo]       → exit 1 nếu có ĐỎ
# Quét file ĐANG được git theo dõi + toàn bộ lịch sử git (bí mật đã xoá vẫn còn trong lịch sử).
set -uo pipefail
REPO="${1:-.}"; cd "$REPO" || exit 2
RED=0; YEL=0
red()  { echo "🔴 ĐỎ   $*"; RED=$((RED+1)); }
yel()  { echo "🟡 VÀNG  $*"; YEL=$((YEL+1)); }
ok()   { echo "🟢 OK    $*"; }
hdr()  { echo; echo "── $* ──"; }

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  FILES() { git ls-files; }
  GREP()  { git grep -nIE "$@" -- . ':!*.lock' ':!*lock.json' ':!*.min.js' 2>/dev/null; }
  IS_GIT=1
else
  echo "(không phải git repo — quét toàn bộ thư mục)"
  FILES() { find . -type f -not -path './.git/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' | sed 's#^\./##'; }
  GREP()  { grep -rnIE "$@" --exclude-dir={.git,node_modules,.venv,dist} . 2>/dev/null; }
  IS_GIT=0
fi

SECRET='(sk-ant-[A-Za-z0-9_-]{20,}|sk-(proj-)?[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{30,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|xox[abprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,})'

hdr "1. Bí mật trong file hiện tại"
hits=$(GREP "$SECRET" | head -20)
[ -n "$hits" ] && { red "Có chuỗi giống API key/token:"; echo "$hits" | sed 's/^/        /' | cut -c1-180; } || ok "không thấy khoá dạng chuẩn"
assign=$(GREP -i '(api[_-]?key|secret|token|password|passwd)["'"'"']?[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"'<>{}$ ]{12,}["'"'"']' \
  | grep -viE 'example|placeholder|your[-_ ]?(api)?[-_ ]?key|xxx|<api_key>|dummy|test|changeme|\$\{' | head -10)
[ -n "$assign" ] && { yel "Gán cứng khoá/mật khẩu — xem lại từng dòng:"; echo "$assign" | sed 's/^/        /' | cut -c1-180; } || ok "không thấy gán cứng khoá"

hdr "2. Bí mật trong LỊCH SỬ git"
if [ $IS_GIT = 1 ]; then
  n=$(git rev-list --all --count 2>/dev/null)
  hist=$(git log -p --all --no-color 2>/dev/null | grep -E "^\+.*$SECRET" | head -5)
  [ -n "$hist" ] && { red "Lịch sử git còn chuỗi giống khoá (đã xoá khỏi file nhưng vẫn lấy lại được):"; echo "$hist" | cut -c1-160 | sed 's/^/        /'; } || ok "quét $n commit, không thấy khoá"
fi

hdr "3. File nhạy cảm / rác của công cụ đang được theo dõi"
sens=$(FILES | grep -E '(^|/)(\.env(\..*)?|.*\.pem|.*\.key|id_rsa.*|.*\.p12|credentials.*\.json|token.*\.json|service[-_]account.*\.json|\.npmrc|\.pypirc)$' | grep -vE '\.env\.example$')
[ -n "$sens" ] && { red "File nhạy cảm:"; echo "$sens" | sed 's/^/        /'; } || ok "không có .env / khoá / credentials"
tool=$(FILES | grep -E '(^|/)\.gstack/|browse\.json$|browse-audit\.jsonl$|\.claude/settings\.local\.json$')
[ -n "$tool" ] && { red "File phiên làm việc của công cụ (có thể chứa token):"; echo "$tool" | sed 's/^/        /'; } || ok "không có file phiên công cụ (.gstack…)"
junk=$(FILES | grep -E '(^|/)(\.DS_Store|__pycache__/|.*\.pyc|.*\.egg-info/|.*\.log|Thumbs\.db|node_modules/)' | head -10)
[ -n "$junk" ] && { yel "File rác:"; echo "$junk" | sed 's/^/        /'; } || ok "không có file rác"

hdr "4. Dữ liệu cá nhân"
paths=$(GREP '(/Users/[A-Za-z0-9._-]+/|/home/[a-z0-9._-]+/|C:\\\\Users\\\\)' | grep -v 'preship_check' | head -8)
[ -n "$paths" ] && { yel "Đường dẫn máy cá nhân trong code/tài liệu:"; echo "$paths" | sed 's/^/        /' | cut -c1-160; } || ok "không có đường dẫn /Users/…"
mails=$(GREP '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}' -o | grep -vE 'noreply|example\.|@users\.noreply|\.png|\.jpg|@[0-9]x' | cut -d: -f3 | sort -u | head -10)
[ -n "$mails" ] && yel "Email xuất hiện — xác nhận có chủ đích: $(echo $mails | tr '\n' ' ')" || ok "không có email"
big=$(FILES | while read -r f; do [ -f "$f" ] && s=$(wc -c <"$f") && [ "$s" -gt 10485760 ] && echo "$((s/1048576)) MB  $f"; done)
[ -n "$big" ] && { echo "$big" | awk '$1>=95{exit 1}' || red "File ≥ 95 MB (GitHub chặn 100 MB):"; yel "File lớn > 10 MB:"; echo "$big" | sed 's/^/        /'; } || ok "không có file > 10 MB"

hdr "5. Bản quyền"
LIC=$(ls -d LICENSE* COPYING* 2>/dev/null | head -1)
[ -n "$LIC" ] && ok "có $LIC" || yel "Thiếu LICENSE — dự án dựa trên mã nguồn mở thì phải giữ LICENSE gốc"
grep -qiE 'GNU GENERAL PUBLIC|GPL-3|AGPL' LICENSE* 2>/dev/null && yel "Giấy phép GPL/AGPL: phần mềm phái sinh phải mở mã cùng giấy phép — hỏi người tạo"
[ -f README.md ] && (grep -qiE 'dựa trên|based on|credit|ghi nhận' README.md && ok "README có phần ghi nhận" || yel "README chưa có dòng ghi nhận dự án gốc / tác giả")

hdr "6. CI và cấu hình"
if ls .github/workflows/*.y*ml >/dev/null 2>&1; then
  pub=$(grep -lE 'pypi|twine|npm publish|docker push|gh-action-pypi|secrets\.' .github/workflows/*.y*ml 2>/dev/null)
  [ -n "$pub" ] && yel "Workflow dùng secrets / publish — có phải của dự án gốc? $(echo $pub | tr '\n' ' ')" || ok "workflow không publish"
else ok "không có .github/workflows"; fi
host=$(GREP -i '(host[[:space:]]*[:=][[:space:]]*["'"'"']0\.0\.0\.0|HOST", "0\.0\.0\.0|listen\(.*0\.0\.0\.0)' | grep -vE '\.md:' | head -3)
[ -n "$host" ] && yel "Server mặc định nghe 0.0.0.0 (ai cùng mạng cũng gọi được) — app local nên 127.0.0.1:" && echo "$host" | sed 's/^/        /' | cut -c1-160
cors=$(GREP "allow_origins=\[\"\*\"\]|Access-Control-Allow-Origin.*\*|cors\(\)" | grep -vE '\.md:' | head -3)
[ -n "$cors" ] && yel "CORS mở cho mọi trang — chỉ nên ở API đọc:" && echo "$cors" | sed 's/^/        /' | cut -c1-160
if [ -f .gitignore ]; then
  miss=""; for p in .env .gstack .DS_Store __pycache__ dist; do grep -q "$p" .gitignore || miss="$miss $p"; done
  [ -n "$miss" ] && yel ".gitignore nên có:$miss" || ok ".gitignore đủ mục cơ bản"
else yel "Chưa có .gitignore (mẫu ở templates/.gitignore)"; fi

echo; echo "══ Kết quả: $RED ĐỎ · $YEL VÀNG ══"
[ $RED -gt 0 ] && { echo "→ Chưa được push công khai. Xử lý theo references/03-bao-mat-truoc-khi-share.md"; exit 1; }
exit 0
