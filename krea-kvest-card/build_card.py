#!/usr/bin/env python3
"""Build the "Krea Kvest" recommendation card in Uzbek and Russian.

Produces, next to this script:
  card-uz.html / card-ru.html  - standalone card, sized exactly to the card box
                                 (these are what get screenshotted into PNG)
  index.html                   - preview page for both cards, published as an Artifact

Regenerate with:  python3 build_card.py
Screenshot with:  see render.sh
"""

import pathlib

HERE = pathlib.Path(__file__).parent
LINK = "https://krea-kvest.netlify.app/"
HOST = "krea-kvest.netlify.app"

# --- QR code ---------------------------------------------------------------
# Generated with segno (error correction M) for LINK; 29x29 modules.
# Rebuild with: pip install segno && python3 build_card.py --qr
QR_MODULES = 29
QR_PATH = (HERE / "qr-path.txt").read_text().strip()


def rebuild_qr() -> str:
    import segno

    matrix = [list(row) for row in segno.make(LINK, error="m").matrix]
    size = len(matrix)
    parts = []
    for y, row in enumerate(matrix):
        x = 0
        while x < size:
            if row[x]:
                run = 0
                while x + run < size and row[x + run]:
                    run += 1
                parts.append(f"M{x} {y}h{run}v1h-{run}z")
                x += run
            else:
                x += 1
    (HERE / "qr-path.txt").write_text("".join(parts))
    return "".join(parts)


# --- copy ------------------------------------------------------------------
UZ = {
    "lang": "uz",
    "file": "card-uz.html",
    "doc_title": "Krea Kvest — tavsiya kartochkasi",
    "eyebrow": "Foydali havola",
    "headline_lead": "Men tavsiya qilaman",
    "name": "Krea Kvest",
    "preview_title": "Krea Kvest — interaktiv onlayn kvest",
    "preview_desc": "To‘g‘ridan-to‘g‘ri brauzerda ochiladi: hech narsa yuklab olish "
    "ham, ro‘yxatdan o‘tish ham shart emas.",
    "wordmark": "Krea Kvest",
    "qr_hint": "QR-ni skaner qiling",
    "chips": ["Brauzerda ochiladi", "Yuklab olish shart emas", "Telefon va kompyuterda"],
}

RU = {
    "lang": "ru",
    "file": "card-ru.html",
    "doc_title": "Krea Kvest — карточка-рекомендация",
    "eyebrow": "Полезная ссылка",
    "headline_lead": "Рекомендую",
    "name": "Krea Kvest",
    "preview_title": "Krea Kvest — интерактивный онлайн-квест",
    "preview_desc": "Открывается прямо в браузере: ничего не нужно скачивать "
    "и не нужна регистрация.",
    "wordmark": "Krea Kvest",
    "qr_hint": "Отсканируйте QR",
    "chips": ["Работает в браузере", "Ничего не скачивать", "Телефон и компьютер"],
}

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Unbounded:wght@500;700&"
    "family=IBM+Plex+Sans:wght@400;500;600&"
    "family=IBM+Plex+Mono:wght@500&display=swap\">"
)

# --- card styles -----------------------------------------------------------
# The card is deliberately single-theme: it is a slide asset that will be
# pasted onto a light presentation background, so every colour is painted
# explicitly and never inherits from the host page.
CARD_CSS = """
.card {
  --ink: #10231F;
  --ink-soft: #556A63;
  --paper: #EEF3F0;
  --surface: #FFFFFF;
  --accent: #0E7C66;
  --accent-deep: #0A5C4C;
  --signal: #D9832B;
  --rule: #D5E2DD;

  width: 760px;
  box-sizing: border-box;
  display: flex;
  background: var(--paper);
  color: var(--ink);
  font-family: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(16, 35, 31, .10), 0 12px 32px rgba(16, 35, 31, .10);
}

.card .rail {
  flex: 0 0 8px;
  background: linear-gradient(180deg, var(--accent) 0%, var(--accent-deep) 100%);
}

.card .body {
  flex: 1 1 auto;
  min-width: 0;
  padding: 40px 44px 36px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.card .eyebrow {
  margin: 0;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--accent);
}

.card .headline {
  margin: 0;
  font-family: "Unbounded", "IBM Plex Sans", sans-serif;
  font-weight: 500;
  font-size: 34px;
  line-height: 1.22;
  letter-spacing: -.01em;
  text-wrap: balance;
}
.card .headline .name { font-weight: 700; color: var(--accent-deep); }

.card .url {
  display: block;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 19px;
  line-height: 1.5;
  font-weight: 500;
  color: var(--accent);
  text-decoration: underline;
  text-decoration-thickness: 1.5px;
  text-underline-offset: 4px;
  word-break: break-all;
}
.card .url:hover { color: var(--accent-deep); }
.card .url:focus-visible { outline: 3px solid var(--signal); outline-offset: 3px; }

/* link preview panel ---------------------------------------------------- */
.card .preview {
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 3px;
  padding: 22px 24px 26px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card .src {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 14px;
  font-weight: 500;
  color: var(--ink-soft);
}
.card .src svg { flex: 0 0 auto; }

.card .p-title {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  line-height: 1.3;
  color: var(--ink);
  text-wrap: balance;
}

.card .p-desc {
  margin: 0;
  font-size: 16px;
  line-height: 1.55;
  color: var(--ink-soft);
  max-width: 52ch;
}

.card .icon-wrap {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.card .tile {
  width: 132px;
  height: 132px;
  border-radius: 30px;
  background: radial-gradient(120% 120% at 28% 18%, #16997E 0%, var(--accent) 46%, var(--accent-deep) 100%);
  display: grid;
  place-items: center;
  box-shadow: 0 6px 18px rgba(10, 92, 76, .28);
}

.card .wordmark {
  margin: 0;
  font-family: "Unbounded", sans-serif;
  font-weight: 700;
  font-size: 19px;
  letter-spacing: -.01em;
  color: var(--signal);
}

/* footer: QR + facts ---------------------------------------------------- */
.card .foot {
  display: flex;
  align-items: center;
  gap: 22px;
}

.card .qr {
  flex: 0 0 auto;
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 3px;
  padding: 9px;
  line-height: 0;
}
.card .qr svg { display: block; width: 104px; height: 104px; }

.card .facts {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 9px;
  min-width: 0;
}

.card .facts li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15.5px;
  line-height: 1.35;
  color: var(--ink);
}
.card .facts li::before {
  content: "";
  flex: 0 0 auto;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent);
}
.card .facts .hint {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 13px;
  letter-spacing: .04em;
  color: var(--ink-soft);
}
.card .facts .hint::before { background: var(--signal); }
"""

GLOBE_SVG = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<circle cx="12" cy="12" r="9.2" stroke="currentColor" stroke-width="1.7"/>'
    '<path d="M2.8 12h18.4M12 2.8c2.4 2.6 3.6 5.7 3.6 9.2s-1.2 6.6-3.6 9.2'
    'c-2.4-2.6-3.6-5.7-3.6-9.2S9.6 5.4 12 2.8z" stroke="currentColor" '
    'stroke-width="1.7" stroke-linejoin="round"/></svg>'
)

# Compass needle: the mark for a "quest" — something you navigate.
COMPASS_SVG = """<svg width="132" height="132" viewBox="-50 -50 100 100" aria-hidden="true">
  <circle r="38" fill="none" stroke="#FFFFFF" stroke-opacity=".34" stroke-width="2.4"/>
  <circle cy="-38" r="2.6" fill="#FFFFFF" fill-opacity=".55"/>
  <circle cy="38" r="2.6" fill="#FFFFFF" fill-opacity=".55"/>
  <circle cx="-38" r="2.6" fill="#FFFFFF" fill-opacity=".55"/>
  <circle cx="38" r="2.6" fill="#FFFFFF" fill-opacity=".55"/>
  <path d="M0 -30 L13 14 L0 4 Z" fill="#FFFFFF"/>
  <path d="M0 -30 L-13 14 L0 4 Z" fill="#FFFFFF" fill-opacity=".55"/>
  <path d="M0 4 L13 14 L0 26 Z" fill="#D9832B"/>
  <path d="M0 4 L-13 14 L0 26 Z" fill="#D9832B" fill-opacity=".62"/>
  <circle r="4.4" fill="#0A5C4C" stroke="#FFFFFF" stroke-width="2.2"/>
</svg>"""


def qr_svg() -> str:
    return (
        f'<svg viewBox="0 0 {QR_MODULES} {QR_MODULES}" '
        f'role="img" aria-label="{LINK} QR kod">'
        f'<path d="{QR_PATH}" fill="#0A5C4C"/></svg>'
    )


def card_html(t: dict) -> str:
    facts = "".join(f"<li>{c}</li>" for c in t["chips"])
    return f"""<div class="card">
  <div class="rail"></div>
  <div class="body">
    <p class="eyebrow">{t['eyebrow']}</p>
    <h1 class="headline">{t['headline_lead']}<br><span class="name">«{t['name']}»</span></h1>
    <a class="url" href="{LINK}">{LINK}</a>

    <div class="preview">
      <p class="src">{GLOBE_SVG}{HOST}</p>
      <h2 class="p-title">{t['preview_title']}</h2>
      <p class="p-desc">{t['preview_desc']}</p>
      <div class="icon-wrap">
        <div class="tile">{COMPASS_SVG}</div>
        <p class="wordmark">{t['wordmark']}</p>
      </div>
    </div>

    <div class="foot">
      <div class="qr">{qr_svg()}</div>
      <ul class="facts">
        {facts}
        <li class="hint">{t['qr_hint']}</li>
      </ul>
    </div>
  </div>
</div>"""


STANDALONE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{doc_title}</title>
{fonts}
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ background: transparent; }}
  body {{ display: inline-block; padding: 28px; }}
{card_css}
</style>
</head>
<body>
{card}
</body>
</html>
"""


def write_standalone(t: dict) -> None:
    html = STANDALONE.format(
        lang=t["lang"],
        doc_title=t["doc_title"],
        fonts=FONTS,
        card_css=CARD_CSS,
        card=card_html(t),
    )
    (HERE / t["file"]).write_text(html, encoding="utf-8")


# --- preview page (published as an Artifact) -------------------------------
PAGE_CSS = """
:root {
  --bg: #F4F7F5;
  --panel: #FFFFFF;
  --fg: #14211D;
  --fg-muted: #5B6F68;
  --edge: #DDE7E2;
  --link: #0E7C66;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0B1512;
    --panel: #12211D;
    --fg: #E6F0EC;
    --fg-muted: #9AB0A8;
    --edge: #1F332C;
    --link: #45C2A3;
  }
}
:root[data-theme="dark"] {
  --bg: #0B1512;
  --panel: #12211D;
  --fg: #E6F0EC;
  --fg-muted: #9AB0A8;
  --edge: #1F332C;
  --link: #45C2A3;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.wrap {
  max-width: 880px;
  margin: 0 auto;
  padding: 56px 24px 80px;
  display: flex;
  flex-direction: column;
  gap: 44px;
}

header { display: flex; flex-direction: column; gap: 12px; }

.kicker {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 12.5px;
  font-weight: 500;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--link);
}

h1 {
  margin: 0;
  font-family: "Unbounded", sans-serif;
  font-weight: 700;
  font-size: clamp(28px, 5vw, 40px);
  line-height: 1.15;
  letter-spacing: -.02em;
  text-wrap: balance;
}

.lede { margin: 0; max-width: 62ch; color: var(--fg-muted); font-size: 17px; }

.lede a { color: var(--link); font-family: "IBM Plex Mono", monospace; font-size: 15.5px; }

section { display: flex; flex-direction: column; gap: 16px; }

h2 {
  margin: 0;
  font-family: "Unbounded", sans-serif;
  font-weight: 500;
  font-size: 20px;
  letter-spacing: -.01em;
}

.stage {
  background: var(--panel);
  border: 1px solid var(--edge);
  border-radius: 6px;
  padding: 32px;
  overflow-x: auto;
}

.note {
  margin: 0;
  padding: 18px 20px;
  background: var(--panel);
  border: 1px solid var(--edge);
  border-left: 4px solid var(--link);
  border-radius: 4px;
  color: var(--fg-muted);
  font-size: 15px;
}
.note strong { color: var(--fg); font-weight: 600; }

ol.steps { margin: 0; padding-left: 22px; color: var(--fg-muted); display: flex; flex-direction: column; gap: 8px; }
ol.steps strong { color: var(--fg); font-weight: 600; }

code {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 14px;
  background: var(--bg);
  border: 1px solid var(--edge);
  border-radius: 3px;
  padding: 1px 6px;
}

footer { color: var(--fg-muted); font-size: 14px; border-top: 1px solid var(--edge); padding-top: 20px; }
"""

PAGE = """<title>Krea Kvest tavsiya kartochkasi</title>
{fonts}
<style>
{page_css}
{card_css}
</style>

<div class="wrap">
  <header>
    <p class="kicker">Slayd uchun tayyor grafika</p>
    <h1>Krea Kvest tavsiya kartochkasi</h1>
    <p class="lede">
      Slaydning chap tomonidagi «Рекомендую» kartochkasi asosida qayta ishlangan —
      lekin bu safar tavsiya qilinadigan havola
      <a href="{link}">{link}</a>.
      Ikkita til varianti: o‘zbekcha va ruscha.
    </p>
  </header>

  <section>
    <h2>O‘zbekcha variant</h2>
    <div class="stage">{card_uz}</div>
  </section>

  <section>
    <h2>Ruscha variant</h2>
    <div class="stage">{card_ru}</div>
  </section>

  <section>
    <h2>Slaydga qanday qo‘yiladi</h2>
    <ol class="steps">
      <li><strong>PNG</strong> fayllarni oling: <code>card-uz.png</code> yoki <code>card-ru.png</code> — 2× o‘lchamda, proyektorda ham aniq chiqadi.</li>
      <li>PowerPoint’da <strong>Вставка → Рисунки</strong> orqali slaydga qo‘ying va chetidan tortib kattalashtiring.</li>
      <li>Kartochka fon rangi ochiq — och rangli slayd fonida yaxshi o‘tiradi.</li>
    </ol>
    <p class="note">
      <strong>Matnni o‘zgartirish kerak bo‘lsa:</strong> <code>build_card.py</code> faylidagi
      <code>UZ</code> va <code>RU</code> lug‘atlaridagi matnni tahrirlab, <code>python3 build_card.py</code>
      va <code>./render.sh</code> ni qayta ishga tushiring.
    </p>
  </section>

  <footer>
    QR kod {link} manziliga olib boradi — auditoriya telefonidan to‘g‘ridan-to‘g‘ri ochishi mumkin.
  </footer>
</div>
"""


def main() -> None:
    import sys

    if "--qr" in sys.argv:
        global QR_PATH
        QR_PATH = rebuild_qr()

    write_standalone(UZ)
    write_standalone(RU)

    (HERE / "index.html").write_text(
        PAGE.format(
            fonts=FONTS,
            page_css=PAGE_CSS,
            card_css=CARD_CSS,
            link=LINK,
            card_uz=card_html(UZ),
            card_ru=card_html(RU),
        ),
        encoding="utf-8",
    )
    print("wrote card-uz.html, card-ru.html, index.html")


if __name__ == "__main__":
    main()
