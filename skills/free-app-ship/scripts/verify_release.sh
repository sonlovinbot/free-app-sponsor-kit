#!/usr/bin/env bash
# Sau khi phát hành: mọi link người dùng sẽ bấm đều chạy.
#   bash verify_release.sh <user>/<repo> <TênFileZip-không-hậu-tố-OS>   vd: sonlovinbot/vieneu-audio-studio AI-Audio-Studio
set -uo pipefail
R="$1"; APP="$2"; USER="${R%%/*}"; NAME="${R##*/}"; FAIL=0
chk() { c=$(curl -sL -o /dev/null -w "%{http_code}" "$2"); [ "$c" = "200" ] && echo "✅ $1" || { echo "❌ $1 → HTTP $c ($2)"; FAIL=1; }; }
tag=$(gh release view --repo "$R" --json tagName -q .tagName 2>/dev/null); echo "Bản mới nhất: ${tag:-?}"
for os in macOS Windows Linux; do chk "Tải $os" "https://github.com/$R/releases/latest/download/$APP-$os.zip"; done
for f in install-online.sh install-online.ps1; do chk "Lệnh cài $f" "https://raw.githubusercontent.com/$R/main/$f"; done
PAGES="https://$USER.github.io/$NAME/"
chk "Trang giới thiệu" "$PAGES"
page=$(curl -s "$PAGES")   # tải trước rồi grep — tránh SIGPIPE + pipefail báo nhầm
grep -q "${tag}" <<<"$page" && echo "✅ Trang ghi đúng $tag" || echo "⚠️ Trang chưa ghi $tag (chạy lại script dựng trang?)"
if curl -s -o /dev/null -w "%{http_code}" "${PAGES}news.json" | grep -q 200; then
  lv=$(curl -s "${PAGES}news.json" | python3 -c "import sys,json;print(json.load(sys.stdin).get('latest_version',''))")
  [ "v$lv" = "$tag" ] && echo "✅ news.json latest_version = $lv" || echo "⚠️ news.json latest_version = $lv (release $tag)"
fi
exit $FAIL
