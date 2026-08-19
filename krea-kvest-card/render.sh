#!/usr/bin/env bash
# Render card-uz.html / card-ru.html into 2x PNGs for pasting onto a slide.
#
#   ./render.sh
#
# Fonts are pulled from Google Fonts once and inlined as data URIs into a
# temporary copy of each card, so headless Chromium renders with no network.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

CHROME="${CHROME:-/opt/pw-browsers/chromium}"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
GF="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap"

python3 "$HERE/build_card.py"

curl -s -A "$UA" "$GF" -o "$WORK/gf.css"

python3 - "$HERE" "$WORK" <<'PY'
import base64, os, pathlib, re, sys, urllib.request

here, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
css = (work / "gf.css").read_text()
proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"https": proxy} if proxy else {})
)

faces, cache = [], {}
for subset, block in re.findall(r"/\* ([a-z0-9-]+) \*/\s*(@font-face \{.*?\})", css, re.S):
    if subset not in {"latin", "latin-ext", "cyrillic"}:
        continue
    url = re.search(r"url\((https://[^)]+)\)", block).group(1)
    if url not in cache:
        cache[url] = base64.b64encode(opener.open(url, timeout=60).read()).decode()
    faces.append(block.replace(url, "data:font/woff2;base64," + cache[url]))

inline = "<style>" + "\n".join(faces) + "</style>"
for name in ("card-uz.html", "card-ru.html"):
    html = (here / name).read_text(encoding="utf-8")
    html = re.sub(r'<link rel="preconnect".*?display=swap">', inline, html, flags=re.S)
    (work / name).write_text(html, encoding="utf-8")
PY

for lang in uz ru; do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --force-device-scale-factor=2 --window-size=830,1500 \
    --default-background-color=00000000 --virtual-time-budget=6000 \
    --screenshot="$WORK/raw-$lang.png" "file://$WORK/card-$lang.html" 2>/dev/null
done

# Trim the transparent margin so the PNG is exactly the card (plus its shadow).
python3 - "$HERE" "$WORK" <<'PY'
import pathlib, sys
from PIL import Image

here, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
for lang in ("uz", "ru"):
    im = Image.open(work / f"raw-{lang}.png").convert("RGBA")
    im = im.crop(im.split()[3].getbbox())
    im.save(here / f"card-{lang}.png")
    print(f"card-{lang}.png  {im.size[0]}x{im.size[1]}")
PY
