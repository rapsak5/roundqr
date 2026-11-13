#!/usr/bin/env python3
"""Mærke i midten af koden.

Det fulde logo bruges i brandbjælken og i skabelonerne Bred, Banner og Rund (under koden).
I midten af Kvadrat og Rund må der kun være et mærke: et symbol, et våbenskjold eller en forkortelse.
Har organisationen kun et tekstlogo, er midten tom ("none").

Mærket fylder hele den hvide cirkel i midten: runde mærker (tomme hjørner) fylder cirklen, andre lægges
så diagonalen rammer cirklen. Logostørrelsen sættes til SIZE.

Brug:
  mark.py SIDE.html MAERKE.png    sæt mærket i midten
  mark.py SIDE.html none          ingen logo i midten
Virker på færdigbyggede sider (roundqr.dk/<id>) og gavefiler, og kan køres igen på en side, der allerede er rettet.
build_brand.py kalder patch(), når brands.json har "mark_file".
"""
import base64, json, re, sys

SIZE = 34  # standard for mærker; skyderen går til MAX
MAX = 36

TAG = '/*RQ_MARK*/'
PRE = re.compile(r'  \(function \(\) \{ var src = ("data:image/[a-z+]+;base64,[^"]+"), img = new Image\(\);\n.*?    img\.src = src; \}\)\(\);\n', re.S)
SIDE = re.compile(r'  ' + re.escape(TAG) + r' window\.RQ_SIDE = null; \(function \(\) \{ var s = ("data:image/[a-z+]+;base64,[^"]+").*?\n', re.S)


def uri(path):
    mime = 'image/svg+xml' if path.endswith('.svg') else 'image/png'
    return '"data:%s;base64,%s"' % (mime, base64.b64encode(open(path, 'rb').read()).decode())


def is_round(path):
    """Rundt mærke: næsten kvadratisk og tomme hjørner."""
    if path.endswith('.svg'):
        return False
    from PIL import Image
    im = Image.open(path).convert('RGBA'); w, h = im.size
    if not 0.85 < w / h < 1.18:
        return False
    a = im.getchannel('A'); k = int(min(w, h) * 0.12)
    for box in ((0, 0, k, k), (w - k, 0, w, k), (0, h - k, k, h), (w - k, h - k, w, h)):
        c = a.crop(box)
        if c.point(lambda v: 255 if v > 40 else 0).histogram()[255] / (c.width * c.height) >= 0.04:
            return False
    return True


FIT = ('  /*RQ_MARK_FIT*/ var MARK_ROUND = %s;\n'
       '  (function () { var G1 = RQ.geometry; RQ.geometry = function (text, o) { var g = G1(text, o);\n'
       '    if (g.logoR && logo) { var a = logo.aspect || 1, R = g.logoR;\n'
       '      g.logoBox = MARK_ROUND && a > 0.85 && a < 1.18 ? 2 * R * 0.9 : 2 * R * 0.9 * (a >= 1 ? a : 1) / Math.sqrt(1 + a * a); }\n'
       '    return g; }; })();\n')


def patch(html, mark):
    """mark: sti til png/svg, eller None for ingen logo i midten."""
    m = SIDE.search(html)
    if m:
        full = m.group(1)
        html = html[:m.start()] + html[m.end():]
    else:
        p = PRE.search(html)
        if not p:
            raise SystemExit('fandt ikke logoet i siden')
        full = p.group(1)
    side = ('  %s window.RQ_SIDE = null; (function () { var s = %s, i = new Image(); i.onload = function () { '
            'window.RQ_SIDE = { img: i, src: s, aspect: (i.naturalWidth || 1) / (i.naturalHeight || 1) }; '
            'if (typeof render === "function" && lastGeom) render(); }; i.src = s; })();\n') % (TAG, full)
    p = PRE.search(html)
    if mark:
        center = ('  (function () { var src = %s, img = new Image();\n'
                  '    img.onload = function () {\n'
                  '      logo = { img: img, src: src, aspect: (img.naturalWidth || 1) / (img.naturalHeight || 1) };\n'
                  '      $("logoThumb").src = src; $("logoThumb").hidden = false;\n'
                  '      $("logoRemove").hidden = false; $("logoSizeRow").hidden = false; $("logoBtn").textContent = t("replace");\n'
                  '      if (typeof render === "function") render();\n'
                  '    };\n'
                  '    img.src = src; })();\n') % uri(mark)
    else:
        center = ''
    if p:
        html = html[:p.start()] + side + center + html[p.end():]
    else:
        hook = '  $("logoRemove").addEventListener("click", function () {'
        assert html.count(hook) == 1
        html = html.replace(hook, side + center + hook, 1)

    # skabelonerne ved siden af og under koden bruger det fulde logo
    old = '      var P = sidePanel(g, o, lg);'
    new = '      lg = window.RQ_SIDE || lg; var P = sidePanel(g, o, lg);'
    if new not in html:
        assert html.count(old) == 2, html.count(old)
        html = html.replace(old, new)
    # rund: mærket i midten, eller det fulde logo under koden, når midten er tom
    html, n = re.subn(r'var ROUND_LAYOUT = "(?:stack|center)";', 'var ROUND_LAYOUT = "%s";' % ('center' if mark else 'stack'), html, count=1)
    assert n == 1
    # mærket fylder cirklen i midten
    html = re.sub(r'  /\*RQ_MARK_FIT\*/ var MARK_ROUND = (?:true|false);\n.*?    return g; \}; \}\)\(\);\n', '', html, flags=re.S)
    hook = '  var _optsBase = opts;\n'
    assert html.count(hook) == 1
    html = html.replace(hook, FIT % ('true' if mark and is_round(mark) else 'false') + hook, 1)
    if mark:
        html, n = re.subn(r'<input type="range" id="logoSize" min="14" max="\d+" value="\d+"', '<input type="range" id="logoSize" min="14" max="%d" value="%d"' % (MAX, SIZE), html, count=1)
        assert n == 1
    # vælger brugeren sit eget logo, gælder det overalt
    hook = '  $("sideText").addEventListener("input", schedule);\n'
    extra = '  $("logoFile").addEventListener("change", function () { window.RQ_SIDE = null; MARK_ROUND = false; }); $("logoRemove").addEventListener("click", function () { window.RQ_SIDE = null; });\n'
    if extra not in html:
        assert html.count(hook) == 1
        html = html.replace(hook, hook + extra, 1)
    if not mark:
        html = html.replace(' Jeres logo ligger allerede i midten.', '')
    return html


if __name__ == '__main__':
    path, mk = sys.argv[1], sys.argv[2]
    h = open(path, encoding='utf-8').read()
    h = patch(h, None if mk == 'none' else mk)
    open(path, 'w', encoding='utf-8').write(h)
    print(path, 'ingen' if mk == 'none' else mk)
