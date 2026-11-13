#!/usr/bin/env python3
"""Fjerner organisationens logo fra en færdigbygget gaveside og sætter en neutral pladsholder ind.

Farver, navn og tekster bliver. De tre steder, logoet lå (brandbjælken, under koden og midten af koden),
får i stedet en stiplet form med teksten "Jeres logo": en cirkel, hvis mærket var rundt eller kvadratisk,
ellers en afrundet firkant med samme proportioner.

Brug:  uden_logo.py IND.html UD.html
Scriptet fejler, hvis der bagefter stadig ligger et billede i siden, som ikke er Round QR's eget.
"""
import base64, io, re, sys
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
BB = re.compile(r'(<div class="bb-logo"><img src=")(data:image/[a-z+]+;base64,[^"]+)(" alt=")[^"]*(")')
SIDE = re.compile(r'(/\*RQ_MARK\*/ window\.RQ_SIDE = null; \(function \(\) \{ var s = ")(data:image/[a-z+]+;base64,[^"]+)(")')
PRE = re.compile(r'(  \(function \(\) \{ var src = ")(data:image/[a-z+]+;base64,[^"]+)(", img = new Image\(\);)')


def aspect(uri):
    if 'svg' in uri[:30]:
        return 1.0
    w, h = Image.open(io.BytesIO(base64.b64decode(uri.split(',', 1)[1]))).size
    return w / h


def placeholder(a, color, label='Jeres logo'):
    """PNG som data-URI. a = bredde/højde på det oprindelige mærke."""
    rund = 0.85 < a < 1.18
    a = 1.0 if rund else max(0.6, min(a, 3.2))
    S = 4  # tegnes stort og skaleres ned, så kanten bliver blød
    W = 480 if a >= 1 else round(480 * a)
    H = round(W / a)
    im = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pad, lw = 6 * S, 7 * S
    box = (pad, pad, W * S - pad, H * S - pad)
    if rund:
        d.ellipse(box, fill='#ffffff')
        # stiplet cirkel
        for k in range(0, 360, 15):
            d.arc(box, k, k + 9, fill=color, width=lw)
    else:
        r = round(min(W, H) * S * 0.16)
        d.rounded_rectangle(box, r, fill='#ffffff', outline=color, width=lw)
        # stiplet kant: hvide huller i stregen
        step = 34 * S
        for x in range(pad + r + step // 2, W * S - pad - r, step):
            for y in (pad, H * S - pad - lw):
                d.rectangle((x, y - S, x + step // 2.4, y + lw + S), fill='#ffffff')
        for y in range(pad + r + step // 2, H * S - pad - r, step):
            for x in (pad, W * S - pad - lw):
                d.rectangle((x - S, y, x + lw + S, y + step // 2.4), fill='#ffffff')
    # teksten på en eller to linjer, så stor som pladsen tillader
    best = None
    for lines in ([label], label.split(' ')):
        size = 200 * S
        while size > 8 * S:
            f = ImageFont.truetype(FONT, size)
            ws = [d.textbbox((0, 0), t, font=f)[2] for t in lines]
            lh = size * 1.15
            lim_w = (W * S - 2 * pad) * (0.66 if rund else 0.80)
            lim_h = (H * S - 2 * pad) * (0.52 if rund else 0.62)
            if max(ws) <= lim_w and lh * len(lines) <= lim_h:
                break
            size -= 2 * S
        if best is None or size > best[0]:
            best = (size, lines)
    size, lines = best
    f = ImageFont.truetype(FONT, size)
    lh = size * 1.15
    y = (H * S - lh * len(lines)) / 2 + lh / 2
    for t in lines:
        d.text((W * S / 2, y), t, font=f, fill=color, anchor='mm')
        y += lh
    im = im.resize((W, H), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def strip(html):
    color = re.search(r'<input type="color" id="fg" value="(#[0-9a-f]{6})"', html).group(1)
    short = re.search(r'<h1>QR-koder til ([^<]+)</h1>', html).group(1)
    gamle = set()
    for rx in (BB, SIDE, PRE):
        m = rx.search(html)
        assert m, rx.pattern[:40]
        gamle.add(m.group(2))
        ny = placeholder(aspect(m.group(2)), color)
        if rx is BB:
            html = html[:m.start()] + m.group(1) + ny + m.group(3) + 'Plads til jeres logo' + m.group(4) + html[m.end():]
        else:
            html = html[:m.start()] + m.group(1) + ny + m.group(3) + html[m.end():]
    for g in gamle:
        assert g not in html, 'logoet ligger stadig et sted i siden'
    # tekster, der lovede logoet
    html, n1 = re.subn(r"(Lav QR-koder i [^<.]*? farver) og med [^<.]*? logo\.", r"\1. Jeres eget logo sætter I selv ind, der hvor der står Jeres logo.", html)
    html, n2 = re.subn(r" Jeres logo ligger allerede i midten\.", " Jeres eget logo sætter I selv ind i midten.", html)
    assert n1 >= 1 and n2 >= 1, (n1, n2)
    return html, short, color


if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    html, short, color = strip(open(src, encoding='utf-8').read())
    open(out, 'w', encoding='utf-8').write(html)
    print('%-18s uden logo, pladsholder i %s, %d KB' % (short, color, len(html) // 1024))
