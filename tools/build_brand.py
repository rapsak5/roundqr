#!/usr/bin/env python3
"""Bygger en brandet udgave af offline-filen roundqr.html, én fil pr. brand.

Kør først python3 tools/build.py, og derefter:
  python3 tools/build_brand.py brands.json UDMAPPE [id ...]

brands.json er en liste med et objekt pr. brand:
  id, name, short, website, colors {primary, secondary, accent, background, text}
Valgfrit: theme {light:{...}, dark:{...}} og qr {fg, eyec, bg} overstyrer det udledte,
fonts {display:[navn, [(vægt, sti.woff2)]], body:[...]} indlejrer en fri skrift.
Filerne er gaver: de er tydeligt mærket som lavet af Kasper Bergstrøm og ikke som forbundets eget produkt.
"""
import base64, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- farver ----------
def rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def hexc(t): return '#%02x%02x%02x' % tuple(max(0, min(255, round(v))) for v in t)
def mix(a, b, p):
    """p = andel af a (0..1) blandet ind i b."""
    A, B = rgb(a), rgb(b)
    return hexc(tuple(A[i] * p + B[i] * (1 - p) for i in range(3)))
def lum(h):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
def toward(c, target, need, against):
    """Flyt c mod target (sort eller hvid), til kontrasten mod against er mindst need."""
    out = c
    for i in range(0, 101, 2):
        out = mix(target, c, i / 100)
        if contrast(out, against) >= need: break
    return out
def on(c, dark='#16181c'):
    return '#ffffff' if contrast('#ffffff', c) >= contrast(dark, c) else dark
def ok_hex(v): return isinstance(v, str) and re.fullmatch(r'#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?', v.strip()) is not None

def palette(b):
    """Organisationens godkendte farver, i prioriteret rækkefølge, plus hvid."""
    c = b['colors']; out = []
    for v in [c.get('primary'), c.get('secondary'), c.get('accent'), c.get('text'), c.get('background')] + list(c.get('extra') or []):
        if isinstance(v, str) and ok_hex(v.strip()) and v.strip().lower() not in out: out.append(v.strip().lower())
    return out

def derive(b):
    """Kun palettens farver bruges som brandfarver. Gråtoner til tekst, streger og flader er neutrale.
    Gavefilerne har kun lys tilstand, så D er en kopi af L."""
    pal = palette(b); W = '#ffffff'
    P = pal[0]
    bgc = (b['colors'].get('background') or '').strip().lower()
    bg = bgc if ok_hex(bgc) and lum(bgc) > 0.8 else W
    darks = [x for x in pal if contrast(x, W) >= 7]
    T = (b['colors'].get('text') or '').strip().lower()
    ink = T if ok_hex(T) and contrast(T, bg) >= 7 else (darks[0] if darks and contrast(darks[0], bg) >= 7 else '#000000')
    L = {'bg': bg, 'surface': W, 'stage': bg if bg != W else '#f3f3f3', 'ink': ink}
    L.update((b.get('theme') or {}).get('light') or {})
    bg, ink = L['bg'], L['ink']
    # knapfarve: første palettefarve, der har en tekstfarve (hvid eller palette) med mindst 4,5:1
    best = None
    for cand in pal:
        if cand == W or lum(cand) > 0.85: continue
        okp = [x for x in [W, ink] + darks if contrast(x, cand) >= 4.5]
        partner = okp[0] if okp else max([W, ink] + darks, key=lambda x: contrast(x, cand))
        if contrast(partner, cand) >= 4.5: best = (cand, partner); break
    L['accent'], L['accent-ink'] = best or (ink, W)
    strong = [x for x in pal if min(contrast(x, bg), contrast(x, W), contrast(x, L['stage'])) >= 4.5]
    L['accent-strong'] = strong[0] if strong else ink
    L['muted'] = toward('#6b6b6b', '#000000', 4.6, min((L['stage'], bg, W), key=lambda x: contrast('#6b6b6b', x)))
    L['line'] = '#dedede' if lum(bg) > 0.9 else mix(ink, bg, 0.14)
    D = dict(L)
    qrd = [x for x in pal if contrast(x, W) >= 4.5]
    fg = qrd[0] if qrd else '#000000'
    eyec = P if contrast(P, W) >= 3 else fg
    qr = {'fg': fg, 'eyec': eyec, 'bg': W}
    for k, v in (b.get('qr') or {}).items():
        if k == 'bg' or v.lower() in pal: qr[k] = v.lower()
        else: print('  advarsel: %s qr.%s %s er ikke i paletten, bruger %s' % (b['id'], k, v, qr[k]))
    return L, D, qr

def css_vars(d): return ' '.join('--%s: %s;' % (k, v) for k, v in d.items())

def fontfaces(b):
    """fonts_embed: {"display": [pakke, navn, [vægte]], "body": [...]}. Pakker er @fontsource (frie skrifter),
    hentet med npm til mappen i miljøvariablen FONTSOURCE. Kun det latinske tegnsæt indlejres (dækker æ, ø og å)."""
    out, fam, seen = [], {}, set()
    base = os.environ.get('FONTSOURCE', '')
    for role, (pkg, name, weights) in (b.get('fonts_embed') or {}).items():
        fam[role] = name
        for w in weights:
            if (pkg, w) in seen: continue
            seen.add((pkg, w))
            path = os.path.join(base, pkg, 'files', '%s-latin-%d-normal.woff2' % (pkg, w))
            data = base64.b64encode(open(path, 'rb').read()).decode()
            out.append('@font-face{font-family:"%s";font-style:normal;font-weight:%d;font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2")}' % (name, w, data))
    return '\n'.join(out), fam

def js(s): return json.dumps(s, ensure_ascii=False)

def build(base, b):
    L, D, qr = derive(b)
    bid, name, short, site = b['id'], b['name'], b.get('short') or b['name'], b['website'].rstrip('/')
    # ejefald: forkortelser får apostrof (DM's, HK's, 3F's), navne får bare s (Djøfs)
    gen = b.get('genitive') or (short + ("'s" if short.isupper() or any(ch.isdigit() for ch in short) else 's'))
    html = base

    # sprog: kun dansk. Sprogvælgeren fjernes helt.
    html, n = re.subn(r'\s*<div class="seg lang" role="radiogroup".*?</div>', '', html, count=1, flags=re.S)
    assert n == 1
    assert 'applyLang(startLang);' in html
    html = html.replace('applyLang(startLang);', 'applyLang("da");', 1)
    # kun lys tilstand
    html = html.replace('color-scheme: dark;', 'color-scheme: light;')

    # firkant som standard, fejlkorrektion H (logo i midten)
    for old, new in (('id="shape-circle" value="circle" checked', 'id="shape-circle" value="circle"'), ('id="shape-square" value="square"', 'id="shape-square" value="square" checked'),
                     ('id="ec-Q" value="Q" checked', 'id="ec-Q" value="Q"'), ('id="ec-H" value="H"', 'id="ec-H" value="H" checked')):
        assert html.count(old) == 1, old
        html = html.replace(old, new, 1)

    # organisationens logo lagt ind på forhånd
    if b.get('logo_file'):
        lf = b['logo_file']
        mime = 'image/svg+xml' if lf.endswith('.svg') else 'image/png'
        uri = 'data:%s;base64,%s' % (mime, base64.b64encode(open(lf, 'rb').read()).decode())
        hook = '  $("logoRemove").addEventListener("click", function () {'
        assert html.count(hook) == 1
        pre = ('  (function () { var src = ' + json.dumps(uri) + ', img = new Image();\n'
               '    img.onload = function () {\n'
               '      logo = { img: img, src: src, aspect: (img.naturalWidth || 1) / (img.naturalHeight || 1) };\n'
               '      $("logoThumb").src = src; $("logoThumb").hidden = false;\n'
               '      $("logoRemove").hidden = false; $("logoSizeRow").hidden = false; $("logoBtn").textContent = t("replace");\n'
               '      if (typeof render === "function") render();\n'
               '    };\n'
               '    img.src = src; })();\n')
        html = html.replace(hook, pre + hook, 1)
        if b.get('logo_size'):
            html = re.sub(r'(<input type="range" id="logoSize" min="14" max="30" value=")\d+"', lambda m: m.group(1) + str(b['logo_size']) + '"', html, count=1)

    # egne nøgler i browserens lager, så filen ikke deler indstillinger med roundqr.dk
    for k in ('"round-qr-lang"', '"round-qr"'):
        assert k in html
        html = html.replace(k, k[:-1] + '-' + bid + '"')

    # tema
    faces, fam = fontfaces(b)
    font_vars = ''
    if fam.get('display'): font_vars += ' --font-display: "%s", "Segoe UI", system-ui, sans-serif;' % fam['display']
    if fam.get('body'): font_vars += ' --font-body: "%s", "Segoe UI", system-ui, sans-serif;' % fam['body']
    if b.get('display_font'): font_vars += ' --font-display: %s;' % b['display_font']
    radius = b.get('radius')
    extra = ''
    if radius is not None:
        r2 = max(0, min(radius, 12) - 4) if radius < 16 else 999
        extra = '.preview,.controls{border-radius:%dpx}.stage{border-radius:%dpx}.btn,.file span,.seg,.seg span,header .lang,header .lang label > span,#link,select,input[type="color"]{border-radius:%dpx}' % (min(radius, 24), max(0, min(radius, 24) - 4), r2 if r2 < 999 else 999)
    theme = '''
/* Brand: %s */
%s
:root { %s%s }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { %s } }
:root[data-theme="dark"] { %s }
h1 .for { font-weight: 600; color: var(--accent-strong); white-space: nowrap; }
.gift { display: grid; gap: 4px; }
.gift a { color: var(--accent-strong); font-weight: 500; }
.foot a { color: inherit; }
%s
''' % (name, faces, css_vars(L), font_vars, css_vars(D), css_vars(D), extra)
    # egen style-blok lige før indholdet, så den ligger efter alle værktøjets egne regler
    mark = '<div class="wrap">'
    assert html.count(mark) == 1
    html = html.replace(mark, '<style>' + theme + '</style>\n' + mark, 1)

    # ikon i fanen
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="31" fill="%s"/>'
           '<rect x="17" y="17" width="30" height="30" rx="9" fill="%s"/><rect x="23" y="23" width="18" height="18" rx="5" fill="%s"/>'
           '<rect x="27.5" y="27.5" width="9" height="9" rx="2.5" fill="%s"/></svg>') % (L['accent'], L['accent-ink'], L['accent'], L['accent-ink'])
    html, n = re.subn(r'<link rel="icon" href="data:image/svg\+xml;base64,[^"]*">', '<link rel="icon" href="data:image/svg+xml;base64,%s">' % base64.b64encode(fav.encode()).decode(), html, count=1)
    assert n == 1
    html = html.replace('<link rel="canonical" href="https://roundqr.dk/">\n', '', 1)
    html = html.replace('<title>Round QR</title>', '<title>Round QR til %s</title>' % short, 1)

    # tekster
    da = {
      'forWho': 'til ' + short,
      'about': 'Kære %s. Her er en lille gave: Round QR i jeres farver. Jeres logo ligger allerede i midten. Lav QR-koder til plakater, slides, nyhedsbreve og arrangementer, firkantede eller runde. Filen virker uden internet, og intet bliver sendt nogen steder hen. Jeg har bygget værktøjet sammen med AI, og det er et lille eksempel på, hvad man kan lave med AI i dag.' % short,
      'giftPitch': 'Jeg holder oplæg og workshops om AI i arbejdslivet. Skriv, hvis det kunne være noget for jeres medlemmer eller medarbejdere.',
      'giftNote': 'En gave fra Kasper Bergstrøm, ikke et officielt produkt fra %s. %s' % (short, ('Farverne er aflæst på %s hjemmeside.' % gen) if str(b.get('source','')).startswith('aflæst') else ('Farverne er hentet fra %s designguide.' % gen)),
      'footNote': 'Virker uden internet. Ingen cookies og ingen sporing.',
    }
    en = {
      'forWho': 'for ' + short,
      'about': 'Dear %s. Here is a small gift: Round QR in your colours. Make round or square QR codes for posters, slides, newsletters and member events. The file works offline, and nothing is sent anywhere. I built the tool together with AI, and it is a small example of what you can make with AI today.' % short,
      'giftPitch': 'I give talks and workshops on AI at work. Get in touch if that could be something for your members or staff.',
      'giftNote': 'A gift from Kasper Bergstrøm, not an official product from %s. The colours follow the public look of %s.' % (short, short),
      'footNote': 'Works offline. No cookies and no tracking.',
    }
    da.update((b.get('text') or {}).get('da') or {})
    if not b.get('logo_file'): da['about'] = da['about'].replace(' Jeres logo ligger allerede i midten.', ''); en.update((b.get('text') or {}).get('en') or {})
    for lg, d, start, about0 in (('da', da, '      subtitle: "Indsæt et link', '      about: "Jeg har udviklet'), ('en', en, '      subtitle: "Paste a link', '      about: "I built Round QR')):
        html, n = re.subn(r'%s[^\n]*",\n' % re.escape(about0), lambda m: '      about: ' + js(d['about']) + ',\n', html, count=1)
        assert n == 1, about0
        ins = ''.join('      %s: %s,\n' % (k, js(d[k])) for k in ('forWho', 'giftPitch', 'giftNote'))
        assert html.count(start) == 1, start
        html = html.replace(start, ins + start, 1)
    html, n = re.subn(r'<span data-t="about">[^<]*</span>', lambda m: '<span data-t="about">' + da['about'] + '</span>', html, count=1)
    assert n == 1
    h1 = '<h1>R<span class="o"><span class="vh">o</span></span>und QR</h1>'
    assert h1 in html
    html = html.replace(h1, h1[:-5] + ' <span class="for" data-t="forWho">' + da['forWho'] + '</span></h1>', 1)

    # bund: afsender og det lille tilbud
    html, n = re.subn(r'  <footer class="foot".*?</footer>\n', lambda m: '''  <footer class="foot" style="display:grid;gap:10px;font-size:13px;color:var(--muted);padding-top:18px;border-top:1px solid var(--line)">
    <div class="gift"><span data-t="giftPitch">%s</span><span><a href="https://ai-workshop.dk">ai-workshop.dk</a> · <a href="mailto:kasper@ai-workshop.dk">kasper@ai-workshop.dk</a></span></div>
    <span data-t="giftNote">%s</span>
    <span style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px 24px">__DEVBY__<span data-t="footNote">%s</span></span>
  </footer>
''' % (da['giftPitch'], da['giftNote'], da['footNote']), html, count=1, flags=re.S)
    html = html.replace('__DEVBY__', devby(), 1).replace('<div class="wrap">', '<style>\n' + DEVBY_CSS + '</style>\n<div class="wrap">', 1)
    assert n == 1

    # skabeloner: kvadrat, bred og banner
    TD = os.path.join(ROOT, 'tools', 'brand')
    dom = re.sub(r'^https?://(www\.)?', '', site).rstrip('/')
    side = b.get('slogan') or ('Scan og læs mere på %s' % dom)
    lay_html = open(os.path.join(TD, 'layout.html'), encoding='utf-8').read().replace('__SIDE__', side.replace('"', '&quot;'))
    anc = '        <p class="hint" id="linkHint" hidden></p>\n      </div>\n'
    assert html.count(anc) == 1
    html = html.replace(anc, anc + lay_html, 1)
    css = open(os.path.join(TD, 'layout.css'), encoding='utf-8').read()
    html = html.replace('<div class="wrap">', '<style>\n' + css + '</style>\n<div class="wrap">', 1)
    # rund skabelon: kompakte mærker i midten af koden, brede og teksttunge logoer under koden
    round_lay = 'stack'
    if b.get('logo_file'):
        from PIL import Image
        w, h = Image.open(b['logo_file']).size
        if 0.6 <= w / h <= 1.6: round_lay = 'center'
    round_lay = b.get('round_layout') or round_lay
    js_lay = open(os.path.join(TD, 'layout.js'), encoding='utf-8').read().replace('__ORG__', json.dumps({'short': short, 'site': dom}, ensure_ascii=False)).replace('__ROUND__', round_lay)
    anc2 = '  var scanState = null;\n'
    assert html.count(anc2) == 1
    html = html.replace(anc2, anc2 + js_lay, 1)

    # forvalg: forbundets link og farver
    old = 'id="link" value="https://ai-workshop.dk"'
    assert old in html
    html = html.replace(old, 'id="link" value="%s"' % site, 1)
    for k in ('fg', 'eyec', 'bg'):
        html, n = re.subn(r'(<input type="color" id="%s" value=")#[0-9a-f]{6}"' % k, lambda m: m.group(1) + qr[k] + '"', html, count=1)
        assert n == 1, k
    # farvesæt: kun kombinationer fra organisationens palet
    pal = palette(b); W = '#ffffff'
    codes = [x for x in pal if contrast(x, W) >= 4.5]
    eyes = [x for x in pal if contrast(x, W) >= 3]
    P0 = pal[0]
    cand = [(qr['fg'], qr['eyec']), (qr['fg'], qr['fg'])]
    for c in codes:
        cand += [(c, c)] + ([(c, P0)] if P0 in eyes else [])
    sets = []
    for fe in cand:
        if fe not in sets: sets.append(fe)
    sets = sets[:6]
    if not any(f == '#000000' for f, _ in sets) and ('#000000' in pal or len(sets) < 3): sets.append(('#000000', '#000000'))
    m = re.search(r'  var PLAIN = \[\n.*?\n  \];', html, re.S)
    assert m
    html = html[:m.start()] + '  var PLAIN = [\n' + ',\n'.join('    { fg: "%s", eyec: "%s", bg: "#ffffff" }' % fe for fe in sets) + '\n  ];' + html[m.end():]
    names = [short] + ['%s %d' % (short, k + 2) for k in range(len(sets) - 1)]
    names = ['Sort' if f == '#000000' and e == '#000000' else nm for nm, (f, e) in zip(names, sets)]
    html, n = re.subn(r'(      presets: )\["Blæk"[^\]]*\]', lambda m: m.group(1) + js(names), html)
    assert n == 1, n
    fg2 = next((x for x in codes if x != qr['fg']), qr['fg'])
    html = html.replace('id="fg2" value="#2a6f8f"', 'id="fg2" value="%s"' % fg2, 1)
    assert 'cdn.jsdelivr' not in html and 'googleapis' not in html
    if os.environ.get('SITE') == '1':
        html = site_mode(html, b, short, gen, L)
    return html, (L, D, qr)

def site_mode(html, b, short, gen, L):
    """Hjemmesideudgave til roundqr.dk/<id>: brandbjælke med logo, skabeloner som store kort øverst, Round QR i baggrunden."""
    TD = os.path.join(ROOT, 'tools', 'brand')
    logo = ''
    if b.get('logo_file'):
        logo = '<div class="bb-logo"><img src="data:image/png;base64,%s" alt="%s"></div>' % (base64.b64encode(open(b['logo_file'], 'rb').read()).decode(), short)
    intro = b.get('site_intro') or ('Lav QR-koder i %s farver og med %s logo. Vælg en skabelon, tilpas den, og gem koden som PNG, JPG eller SVG. Gratis, uden login, og intet bliver sendt nogen steder hen.' % (gen, gen))
    band = '<header class="brandbar"><div class="bb-inner">%s<div class="bb-text"><h1>QR-koder til %s</h1><p>%s</p></div></div></header>\n' % (logo, short, intro)
    html, n = re.subn(r'  <header>.*?</header>\n', '', html, count=1, flags=re.S)
    assert n == 1
    mark = '<div class="wrap">'
    html = html.replace(mark, band + mark, 1)
    # skabelonerne flyttes op over værktøjet og får levende miniaturer
    m = re.search(r'      <div class="group">\n        <span class="label">Skabelon</span>.*?herunder\.</p>\n      </div>\n', html, re.S)
    assert m, 'skabelongruppe'
    grp = m.group(0)
    html = html[:m.start()] + html[m.end():]
    for key in ('center', 'wide', 'banner', 'round'):
        grp = re.sub(r'(<input type="radio" name="layout" id="layout-%s"[^>]*><span>)<svg.*?</svg>' % key, lambda mm, k=key: mm.group(1) + '<span class="th"><img id="th-%s" alt=""></span>' % k, grp, count=1, flags=re.S)
    grp = grp.replace('<div class="group">', '<section class="tplsec" aria-label="Skabeloner">', 1).replace('<span class="label">Skabelon</span>', '<span class="label">Vælg skabelon</span>', 1)
    grp = grp[:grp.rstrip().rfind('</div>')] + '</section>\n'
    grp = grp.replace('<p class="hint">Vælg en skabelon, og tilpas den bagefter med indstillingerne herunder.</p>', '<p class="hint">Vælg en skabelon, og tilpas den bagefter med indstillingerne nedenfor.</p>')
    html = html.replace('  <div class="grid">', grp + '  <div class="grid">', 1)
    css = open(os.path.join(TD, 'site.css'), encoding='utf-8').read()
    html = html.replace('<div class="wrap">', '<style>\n' + css + '</style>\n<div class="wrap">', 1)
    js = open(os.path.join(TD, 'site.js'), encoding='utf-8').read()
    anc = '  $("sideText").addEventListener("input", schedule);\n'
    assert anc in html
    html = html.replace(anc, anc + js, 1)
    dl = ('<section class="dlbox" aria-label="Hent programmet"><div><h2>Hent programmet</h2>'
          '<p>Hele QR-generatoren til %s i én HTML-fil. Gem den på din egen computer, og lav QR-koder, også uden internet. '
          'Der er intet at installere, og intet bliver sendt nogen steder hen.</p></div>'
          '<a class="btn primary" href="index.html" download="qr-koder-%s.html">Hent HTML-filen</a></section>\n') % (short, b['id'])
    fanc = '  <footer class="foot"'
    assert html.count(fanc) == 1
    html = html.replace(fanc, dl + fanc, 1)
    html = re.sub(r'<title>[^<]*</title>', '<title>QR-koder til %s</title>' % short, html, count=1)
    # ikke i Google, før organisationen har sagt god for siden
    html = html.replace('</title>', '</title>\n<meta name="robots" content="noindex">', 1)
    return html

def devby():
    import base64
    aw = base64.b64encode(open(os.path.join(ROOT, 'logos', 'ai-workshop.png'), 'rb').read()).decode()
    rq = base64.b64encode(open(os.path.join(ROOT, 'favicon.svg'), 'rb').read()).decode()
    return ('<span class="devby"><span>Udviklet af</span>'
            '<a class="devlogo" href="https://ai-workshop.dk"><img src="data:image/png;base64,%s" alt="" width="28" height="28">ai-workshop.dk</a>'
            '<span>og</span>'
            '<a class="devlogo" href="https://roundqr.dk"><img src="data:image/svg+xml;base64,%s" alt="" width="28" height="28">Round QR</a></span>') % (aw, rq)

DEVBY_CSS = """.devby { display: inline-flex; flex-wrap: wrap; align-items: center; gap: 8px 10px; font-size: 13.5px; color: var(--ink); }
.devby .devlogo { display: inline-flex; align-items: center; gap: 7px; color: var(--ink); font-weight: 600; text-decoration: none; padding: 4px 12px 4px 4px; border: 1px solid var(--line); border-radius: 999px; background: #fff; }
.devby .devlogo:hover, .devby .devlogo:focus-visible { border-color: var(--accent-strong); text-decoration: underline; }
.devby .devlogo img { width: 28px; height: 28px; display: block; }
"""

def main():
    src, out = sys.argv[1], sys.argv[2]
    only = set(sys.argv[3:])
    base = open(os.path.join(ROOT, 'roundqr.html'), encoding='utf-8').read()
    os.makedirs(out, exist_ok=True)
    for b in json.load(open(src, encoding='utf-8')):
        if only and b['id'] not in only: continue
        if not ok_hex((b.get('colors') or {}).get('primary') or ''):
            print('SPRUNGET OVER', b['id'], '(ingen verificeret primærfarve)'); continue
        html, (L, D, qr) = build(base, b)
        path = os.path.join(out, 'roundqr-%s.html' % b['id'])
        open(path, 'w', encoding='utf-8').write(html)
        print('%-28s %4d KB  accent %s  QR %s / %s' % (os.path.basename(path), os.path.getsize(path) // 1024, L['accent'], qr['fg'], qr['eyec']))

if __name__ == '__main__':
    main()
