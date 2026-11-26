#!/usr/bin/env bash
# Builds the offline app bundle in www/ from the web game (index.html + words.json).
# - wraps the page in a full HTML document (the web Artifact host adds this skeleton itself)
# - swaps Google Fonts for the bundled copies in assets/fonts
# - pads the page by the Android system-bar insets that Capacitor's SystemBars plugin provides
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf www
mkdir -p www/fonts
cp assets/fonts/* www/fonts/
cp words.json www/words.json

python3 - <<'EOF'
import re
src = open('index.html', encoding='utf-8').read()
# drop the remote font tags, use bundled fonts instead
src = re.sub(r'<link rel="(preconnect|stylesheet)" href="https://fonts\.(googleapis|gstatic)\.com[^>]*>\n?', '', src)
head, body = src.split('<div class="app">', 1)
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
app_css = """<style>
:root{padding-top:var(--safe-area-inset-top,env(safe-area-inset-top,0px));padding-bottom:var(--safe-area-inset-bottom,env(safe-area-inset-bottom,0px))}
.app{padding-left:max(16px,var(--safe-area-inset-left,0px));padding-right:max(16px,var(--safe-area-inset-right,0px))}
</style>
"""
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">\n'
       '<meta name="theme-color" content="#110e2b">\n<link rel="stylesheet" href="fonts/fonts.css">\n'
       + head + app_css + '</head>\n<body>\n<div class="app">' + body + '\n</body>\n</html>\n')
open('www/index.html', 'w', encoding='utf-8').write(doc)
EOF
echo "www/ built: $(du -sh www | cut -f1)"
