import base64, json, os, re
# Bygger index.html (hjemmesiden) og roundqr.html (offline-filen) ud fra src/round-qr.html.
# Kør fra repo-roden: python3 tools/build.py
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(OUT, 'src', 'round-qr.html')
src = open(SRC, encoding='utf-8').read()

FONTS = [
  ('Bricolage Grotesque', 600, 'bricolage-600.woff2'),
  ('Bricolage Grotesque', 700, 'bricolage-700.woff2'),
  ('IBM Plex Sans', 400, 'plex-sans-400.woff2'),
  ('IBM Plex Sans', 500, 'plex-sans-500.woff2'),
  ('IBM Plex Sans', 600, 'plex-sans-600.woff2'),
  ('IBM Plex Mono', 400, 'plex-mono-400.woff2'),
  ('IBM Plex Mono', 500, 'plex-mono-500.woff2'),
]
LIBS = ['qrcode.js', 'jsQR.js']

def fontface(inline):
    out = []
    for fam, w, name in FONTS:
        if inline:
            url = 'data:font/woff2;base64,' + base64.b64encode(open(os.path.join(OUT, 'assets', 'fonts', name), 'rb').read()).decode()
        else:
            url = 'assets/fonts/' + name
        out.append('@font-face{font-family:"%s";font-style:normal;font-weight:%d;font-display:swap;src:url(%s) format("woff2")}' % (fam, w, url))
    return '\n'.join(out)

# ---------- strip artifact-only head bits ----------
body = src
body = re.sub(r'<title>.*?</title>\n', '', body, count=1)
body = body.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
body = re.sub(r'<link rel="preconnect"[^>]*>\n', '', body)
body = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n', '', body)
assert 'fonts.googleapis' not in body

RESET = ':root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}'

# ---------- strings for the new sections ----------
DA = {
 'spTitle': 'Sponsorer',
 'spIntro': 'Round QR er gratis og uden reklamer. Tak til dem, der støtter siden.',
 'sp1': 'Praktiske workshops og kurser i AI for medarbejdere, ledere og undervisere. Fra første prompt til faste arbejdsgange i hverdagen.',
 'sp2': 'Video, podcast og livestreaming af events. Klippekort, faste pakker eller en workshop, hvor I lærer at producere selv.',
 'sp3': 'Tidsregistrering med NFC. Et klistermærke ved døren stempler dig ind og ud, og den gratis app holder styr på timer og flex.',
 'sp4': 'Et nyt dansk forlag med bøger om naturen og de gode oplevelser i den, for både børn og voksne.',
 'sp5': 'Cider fra England, Irland, Frankrig, Danmark og USA. Med og uden alkohol, og flere af dem er økologiske.',
 'sp6': 'En konference om AI i arbejdslivet for den enkelte, teamet og organisationen. 11. februar 2027 i Dansk Arkitektur Center.',
 'sp7': 'Hjælper medicinalvirksomheder med at tage AI i brug på en ansvarlig måde med mennesket i centrum. Rådgivning, coaching og workshops.',
 'dlTitle': 'Hent Round QR',
 'dlText': 'Hele programmet i én HTML-fil. Åbn den i din browser og lav QR-koder, også uden internet. Der er intet at installere.',
 'dlBtn': 'Hent roundqr.html',
 'footNote': 'Ingen cookies og ingen sporing. Dine indstillinger gemmes kun i din egen browser.',
}
EN = {
 'spTitle': 'Sponsors',
 'spIntro': 'Round QR is free and has no ads. Thanks to the companies that support it.',
 'sp1': 'Hands-on AI workshops and courses for staff, managers and teachers. From the first prompt to routines that stick.',
 'sp2': 'Video, podcasts and livestreaming of events. Clip cards, fixed packages or a workshop where you learn to produce it yourself.',
 'sp3': 'Time tracking with NFC. A sticker by the door clocks you in and out, and the free app keeps track of your hours and balance.',
 'sp4': 'A new Danish publisher of books about nature and the good experiences it offers, for children and adults.',
 'sp5': 'Cider from England, Ireland, France, Denmark and the USA. With and without alcohol, and several are organic.',
 'sp6': 'A conference on AI at work for individuals, teams and organisations. 11 February 2027 at the Danish Architecture Centre.',
 'sp7': 'Helps pharmaceutical companies adopt AI responsibly, with people at the centre. Consulting, coaching and workshops.',
 'dlTitle': 'Download Round QR',
 'dlText': 'The whole program in one HTML file. Open it in your browser and make QR codes, even offline. Nothing to install.',
 'dlBtn': 'Download roundqr.html',
 'footNote': 'No cookies and no tracking. Your settings are only stored in your own browser.',
}
# Tysk, norsk og svensk til sponsorer, download-boksen og bunden.
SITE_LANGS = {
 "de": {
  "spTitle": "Sponsoren",
  "spIntro": "Round QR ist kostenlos und werbefrei. Danke an alle, die die Seite unterstützen.",
  "sp1": "Praxisnahe Workshops und Kurse zu KI für Mitarbeitende, Führungskräfte und Lehrende. Vom ersten Prompt bis zu festen Abläufen im Alltag.",
  "sp2": "Video, Podcast und Livestreaming von Events. Zehnerkarten, feste Pakete oder ein Workshop, in dem ihr lernt, selbst zu produzieren.",
  "sp3": "Zeiterfassung mit NFC. Ein Aufkleber an der Tür stempelt dich ein und aus, und die kostenlose App behält Stunden und Gleitzeit im Blick.",
  "sp4": "Ein neuer dänischer Verlag mit Büchern über die Natur und die schönen Erlebnisse darin, für Kinder und Erwachsene.",
  "sp5": "Cider aus England, Irland, Frankreich, Dänemark und den USA. Mit und ohne Alkohol, und mehrere davon sind Bio.",
  "sp6": "Eine Konferenz über KI im Arbeitsleben für den Einzelnen, das Team und die Organisation. 11. Februar 2027 im Dansk Arkitektur Center.",
  "sp7": "Hilft Pharmaunternehmen, KI verantwortungsvoll und mit dem Menschen im Mittelpunkt einzuführen. Beratung, Coaching und Workshops.",
  "dlTitle": "Round QR herunterladen",
  "dlText": "Das ganze Programm in einer HTML-Datei. Öffne sie im Browser und erstelle QR-Codes, auch ohne Internet. Es muss nichts installiert werden.",
  "dlBtn": "roundqr.html herunterladen",
  "footNote": "Keine Cookies und kein Tracking. Deine Einstellungen werden nur in deinem eigenen Browser gespeichert."
 },
 "no": {
  "spTitle": "Sponsorer",
  "spIntro": "Round QR er gratis og uten reklame. Takk til dem som støtter siden.",
  "sp1": "Praktiske workshops og kurs i KI for ansatte, ledere og undervisere. Fra første prompt til faste arbeidsrutiner i hverdagen.",
  "sp2": "Video, podkast og livestreaming av arrangementer. Klippekort, faste pakker eller en workshop der dere lærer å produsere selv.",
  "sp3": "Timeregistrering med NFC. Et klistremerke ved døra stempler deg inn og ut, og den gratis appen holder styr på timer og fleks.",
  "sp4": "Et nytt dansk forlag med bøker om naturen og de gode opplevelsene i den, for både barn og voksne.",
  "sp5": "Cider fra England, Irland, Frankrike, Danmark og USA. Med og uten alkohol, og flere av dem er økologiske.",
  "sp6": "En konferanse om KI i arbeidslivet for den enkelte, teamet og organisasjonen. 11. februar 2027 i Dansk Arkitektur Center.",
  "sp7": "Hjelper legemiddelselskaper med å ta i bruk KI på en ansvarlig måte med mennesket i sentrum. Rådgivning, coaching og workshops.",
  "dlTitle": "Last ned Round QR",
  "dlText": "Hele programmet i én HTML-fil. Åpne den i nettleseren og lag QR-koder, også uten internett. Det er ingenting å installere.",
  "dlBtn": "Last ned roundqr.html",
  "footNote": "Ingen informasjonskapsler og ingen sporing. Innstillingene dine lagres bare i din egen nettleser."
 },
 "sv": {
  "spTitle": "Sponsorer",
  "spIntro": "Round QR är gratis och utan reklam. Tack till dem som stöttar sidan.",
  "sp1": "Praktiska workshoppar och kurser i AI för medarbetare, chefer och lärare. Från första prompten till fasta arbetssätt i vardagen.",
  "sp2": "Video, podd och livestreaming av evenemang. Klippkort, fasta paket eller en workshop där ni lär er att producera själva.",
  "sp3": "Tidrapportering med NFC. Ett klistermärke vid dörren stämplar in och ut dig, och den kostnadsfria appen håller koll på timmar och flex.",
  "sp4": "Ett nytt danskt förlag med böcker om naturen och de fina upplevelserna i den, för både barn och vuxna.",
  "sp5": "Cider från England, Irland, Frankrike, Danmark och USA. Med och utan alkohol, och flera av dem är ekologiska.",
  "sp6": "En konferens om AI i arbetslivet för individen, teamet och organisationen. 11 februari 2027 på Dansk Arkitektur Center.",
  "sp7": "Hjälper läkemedelsföretag att börja använda AI på ett ansvarsfullt sätt med människan i centrum. Rådgivning, coachning och workshoppar.",
  "dlTitle": "Ladda ner Round QR",
  "dlText": "Hela programmet i en HTML-fil. Öppna den i webbläsaren och skapa QR-koder, även utan internet. Inget att installera.",
  "dlBtn": "Ladda ner roundqr.html",
  "footNote": "Inga kakor och ingen spårning. Dina inställningar sparas bara i din egen webbläsare."
 }
}

def js_obj(d):
    import json
    return ''.join('      %s: %s,\n' % (k, json.dumps(v, ensure_ascii=False)) for k, v in d.items())

SPONSORS = [
  ('AI Workshop', 'ai-workshop.dk', 'https://ai-workshop.dk', 'ai-workshop.png', 'sp1'),
  ('Berg-Streaming', 'berg-streaming.dk', 'https://berg-streaming.dk', 'berg-streaming.png', 'sp2'),
  ('StemplerInd', 'stemplerind.dk', 'https://stemplerind.dk', 'stemplerind.svg', 'sp3'),
  ('Forlaget Uldahl', 'forlagetuldahl.dk', 'https://forlagetuldahl.dk', 'forlaget-uldahl.png', 'sp4'),
  ('Cider Kompagniet', 'ciderkompagniet.dk', 'https://ciderkompagniet.dk', 'ciderkompagniet.png', 'sp5'),
  ('Arbejdsliv.ai', 'arbejdsliv.ai', 'https://arbejdsliv.ai', 'arbejdsliv.png', 'sp6'),
  ('PharmaConsulting.ai', 'pharmaconsulting.ai', 'https://pharmaconsulting.ai', 'pharmaconsulting.png', 'sp7'),
]

SECTION_CSS = '''
/* Sponsors, download, footer (website only) */
:root { --plate: #ffffff; }
.sponsors { display: grid; grid-template-columns: minmax(0, 280px) minmax(0, 1fr); gap: 20px 48px; align-items: start;
  margin-top: 18px; padding-top: 36px; border-top: 1px solid var(--line); }
@media (max-width: 760px) { .sponsors { grid-template-columns: minmax(0, 1fr); } }
.site-h2 { font-family: var(--font-display); font-weight: 700; font-size: 27px; line-height: 1.1; letter-spacing: -0.015em; margin: 0 0 8px; text-wrap: balance; }
.sp-intro p, .dl-text p { margin: 0; color: var(--muted); max-width: 48ch; }
.sp-list { list-style: none; margin: 0; padding: 0; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; min-width: 0; }
.sp-list li + li { border-top: 1px solid var(--line); }
.sp { display: grid; grid-template-columns: 58px minmax(0, 1fr) auto; gap: 16px; align-items: start; padding: 16px 18px; color: inherit; text-decoration: none; }
.sp:hover { background: var(--bg); }
.sp:focus-visible { outline: 2px solid var(--accent-strong); outline-offset: -3px; border-radius: 12px; }
.sp-logo { width: 58px; height: 58px; border-radius: 13px; background: var(--plate); display: grid; place-items: center; padding: 6px; box-shadow: 0 0 0 1px var(--line); }
.sp-logo img { width: 46px; height: 46px; object-fit: contain; display: block; }
.sp-body { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
.sp-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 10px; }
.sp-name { font-weight: 600; font-size: 15.5px; }
.sp-url { font-family: var(--font-mono); font-size: 12.5px; color: var(--accent-strong); }
.sp-text { font-size: 14px; line-height: 1.5; color: var(--muted); max-width: 64ch; }
.sp-arrow { color: var(--muted); font-size: 18px; line-height: 1; align-self: center; }
.sp:hover .sp-arrow { color: var(--accent-strong); }
@media (max-width: 480px) {
  .sp { grid-template-columns: 48px minmax(0, 1fr); gap: 14px; padding: 14px; }
  .sp-logo { width: 48px; height: 48px; border-radius: 11px; padding: 5px; }
  .sp-logo img { width: 38px; height: 38px; }
  .sp-arrow { display: none; }
}
.download { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 18px 32px;
  padding: 26px 28px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; }
.dl-text { flex: 1 1 320px; min-width: 0; }
.dl-action { display: flex; flex-direction: column; align-items: flex-start; gap: 7px; }
.btn.big { font-size: 15.5px; padding: 12px 20px 12px 16px; border-radius: 10px; text-decoration: none; gap: 9px; }
.btn.big svg { width: 19px; height: 19px; flex: none; }
.foot { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 6px 24px; font-size: 13px; color: var(--muted);
  padding-top: 18px; border-top: 1px solid var(--line); }
.foot a { color: inherit; }
@media (max-width: 480px) { .download { padding: 20px 18px; } }
'''

DL_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10.5l5 5 5-5M5 19.5h14"/></svg>'

def sponsor_html():
    rows = []
    for name, host, url, logo, key in SPONSORS:
        rows.append(f'''      <li><a class="sp" href="{url}" target="_blank" rel="noopener">
        <span class="sp-logo"><img src="logos/{logo}" alt="{name} logo" width="46" height="46" loading="lazy" decoding="async"></span>
        <span class="sp-body"><span class="sp-head"><span class="sp-name">{name}</span><span class="sp-url">{host}</span></span>
          <span class="sp-text" data-t="{key}">{DA[key]}</span></span>
        <span class="sp-arrow" aria-hidden="true">&#8599;</span></a></li>''')
    return '\n'.join(rows)

def site_sections(dl_size):
    return f'''
  <section class="sponsors" id="sponsorer" aria-labelledby="sp-h">
    <div class="sp-intro">
      <h2 class="site-h2" id="sp-h" data-t="spTitle">{DA['spTitle']}</h2>
      <p data-t="spIntro">{DA['spIntro']}</p>
    </div>
    <ul class="sp-list">
{sponsor_html()}
    </ul>
  </section>

  <section class="download" id="hent" aria-labelledby="dl-h">
    <div class="dl-text">
      <h2 class="site-h2" id="dl-h" data-t="dlTitle">{DA['dlTitle']}</h2>
      <p data-t="dlText">{DA['dlText']}</p>
    </div>
    <div class="dl-action">
      <a class="btn primary big" href="roundqr.html" download="roundqr.html">{DL_ICON}<span data-t="dlBtn">{DA['dlBtn']}</span></a>
      <span class="spec">HTML · {dl_size}</span>
    </div>
  </section>

  <footer class="foot">
    <span>Round QR · roundqr.dk</span>
    <span data-t="footNote">{DA['footNote']}</span>
  </footer>
'''

OFFLINE_FOOT = '''
  <footer class="foot" style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 24px;font-size:13px;color:var(--muted);padding-top:18px;border-top:1px solid var(--line)">
    <span>Round QR · <a href="https://roundqr.dk" style="color:inherit">roundqr.dk</a></span>
    <span data-t="footNote"></span>
  </footer>
'''

ANCHORS = {'da': '      subtitle: "Indsæt et link', 'en': '      subtitle: "Paste a link', 'de': '      subtitle: "Link einfügen',
           'no': '      subtitle: "Lim inn en lenke', 'sv': '      subtitle: "Klistra in en länk'}
def add_strings(html, per_lang):
    for lg, d in per_lang.items():
        assert html.count(ANCHORS[lg]) == 1, lg
        html = html.replace(ANCHORS[lg], js_obj(d) + ANCHORS[lg], 1)
    return html

def head(title, desc, extra=''):
    return f'''<!doctype html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{extra}<style>{RESET}</style>
</head>
<body>
'''

def libs(inline):
    if not inline:
        return '\n'.join('<script src="assets/%s"></script>' % n for n in LIBS)
    out = []
    for n in LIBS:
        code = open(os.path.join(OUT, 'assets', n), encoding='utf-8').read().replace('</script', '<\\/script')
        out.append('<script>\n' + code + '\n</script>')
    return '\n'.join(out)

CDN = '<script src="https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.js"></script>\n<script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>'
assert CDN in body
END_WRAP = '</div>\n\n' + CDN
assert END_WRAP in body, 'wrap end'
DESC = 'Lav runde eller almindelige QR-koder fra et link. Vælg form, farver og logo, og gem som PNG, JPG eller SVG. Gratis, uden login og uden reklamer.'

# ---------- offline single file ----------
# Julelys er kun til hjemmesiden. Download-filen får ikke juletilstanden.
JUL = re.compile(r'(?:<!-- julelys:start -->|/\* julelys:start \*/).*?(?:<!-- julelys:end -->|/\* julelys:end \*/)\n?', re.S)
off = JUL.sub('', body)
assert 'julelys:' not in off and 'id="xbar"' not in off and 'setXmas' not in off
off = off.replace('<style>\n', '<style>\n' + fontface(True) + '\n', 1)
off = off.replace(END_WRAP, OFFLINE_FOOT + END_WRAP, 1).replace(CDN, libs(True), 1)
off = add_strings(off, {'da': {'footNote': 'Virker uden internet. Ingen cookies og ingen sporing.'}, 'en': {'footNote': 'Works offline. No cookies and no tracking.'},
  'de': {'footNote': 'Funktioniert ohne Internet. Keine Cookies und kein Tracking.'}, 'no': {'footNote': 'Virker uten internett. Ingen informasjonskapsler og ingen sporing.'},
  'sv': {'footNote': 'Fungerar utan internet. Inga kakor och ingen spårning.'}})
OFF_DA = 'Jeg har udviklet Round QR sammen med AI, fordi jeg selv manglede et godt værktøj til QR-koder. Den er gratis, uden abonnement, login og reklamer, og virker også uden internet.'
OFF_EN = "I built Round QR together with AI because I needed a good QR code tool myself. It's free, with no subscriptions, logins or ads, and it works offline too."
off = re.sub(r'(      about: )"Jeg har udviklet[^"]*"', lambda m: m.group(1) + '"' + OFF_DA + '"', off)
off = re.sub(r'(      about: )"I built Round QR[^"]*"', lambda m: m.group(1) + '"' + OFF_EN.replace('"', '\\"') + '"', off)
OFF_ABOUT = {
  'Ich habe Round QR': 'Ich habe Round QR zusammen mit KI entwickelt, weil mir selbst ein gutes Werkzeug für QR-Codes fehlte. Es ist kostenlos, ohne Abo, Login und Werbung, und funktioniert auch ohne Internet.',
  'Jeg har utviklet': 'Jeg har utviklet Round QR sammen med KI fordi jeg selv manglet et godt verktøy for QR-koder. Det er gratis, uten abonnement, innlogging og reklame, og virker også uten internett.',
  'Jag har utvecklat': 'Jag har utvecklat Round QR tillsammans med AI eftersom jag själv saknade ett bra verktyg för QR-koder. Det är gratis, utan prenumeration, inloggning och reklam, och fungerar även utan internet.',
}
for start, text in OFF_ABOUT.items():
    off, n = re.subn(r'(      about: )"' + start + r'[^"]*"', lambda m, text=text: m.group(1) + json.dumps(text, ensure_ascii=False), off)
    assert n == 1, start
off = re.sub(r'<span data-t="about">[^<]*</span>', '<span data-t="about">' + OFF_DA + '</span>', off)
off = head('Round QR', DESC, '<link rel="icon" href="data:image/svg+xml;base64,' + base64.b64encode(open(OUT + '/favicon.svg','rb').read()).decode() + '">\n') + off + '\n</body>\n</html>\n'
assert 'cdn.jsdelivr' not in off and 'googleapis' not in off
open(OUT + '/roundqr.html', 'w', encoding='utf-8').write(off)
size = os.path.getsize(OUT + '/roundqr.html')
dl_size = f'{round(size/1024)} KB'

# ---------- website ----------
site = body.replace('<style>\n', '<style>\n' + fontface(False) + '\n', 1)
site = site.replace('</style>', SECTION_CSS + '</style>', 1)
site = site.replace(END_WRAP, site_sections(dl_size) + END_WRAP, 1).replace(CDN, libs(False), 1)
site = add_strings(site, dict({'da': DA, 'en': EN}, **SITE_LANGS))
SITE_META = '''<link rel="canonical" href="https://roundqr.dk/">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#f5f3ee" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#141310" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:url" content="https://roundqr.dk/">
<meta property="og:site_name" content="Round QR">
<meta property="og:title" content="Round QR">
<meta property="og:description" content="Gratis runde og firkantede QR-koder. Uden login og uden reklamer.">
<meta property="og:image" content="https://roundqr.dk/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="da_DK">
<meta name="twitter:card" content="summary_large_image">
'''
site = head('Round QR · Gratis runde og firkantede QR-koder', DESC, SITE_META) + site + '\n</body>\n</html>\n'
assert 'cdn.jsdelivr' not in site and 'googleapis' not in site
open(OUT + '/index.html', 'w', encoding='utf-8').write(site)

print('roundqr.html', dl_size, '| index.html', round(os.path.getsize(OUT + '/index.html')/1024), 'KB')
