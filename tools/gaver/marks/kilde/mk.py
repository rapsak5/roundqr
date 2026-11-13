import json, numpy as np
from PIL import Image, ImageDraw, ImageFont
from seg import mask, segs
from spec import S, NONE, KEEP
info = json.load(open('info.json'))
def trim(im, pad=0.04):
    m = mask(im); ys, xs = np.where(m)
    if len(xs) == 0: return im
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    p = max(2, int(max(im.size) * pad))
    a = np.array(im.convert('RGBA')); corner = a[0, 0]
    out = Image.new('RGBA', (im.width + 2 * p, im.height + 2 * p), tuple(int(v) for v in corner) if corner[3] > 200 and False else (0, 0, 0, 0))
    out.paste(im.convert('RGBA'), (p, p)); return out
def clear_bg(im):
    # hvid baggrund, der hænger sammen med kanten, bliver gennemsigtig
    from PIL import ImageDraw as D
    im = im.convert('RGBA'); a = np.array(im)
    w = ((a[..., :3].min(-1) > 238) & (a[..., 3] > 200)) | (a[..., 3] < 20)
    from scipy import ndimage
    lab, n = ndimage.label(w)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge)); a[bg, 3] = 0
    return Image.fromarray(a)
def rounded(im, r=0.16):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], int(min(im.size) * r), fill=255)
    im = im.convert('RGBA'); a = np.array(im); a[..., 3] = np.minimum(a[..., 3], np.array(m)); return Image.fromarray(a)
def text_tile(t, fg, bg):
    f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 300)
    l, tp, r, b = f.getbbox(t); w, h = r - l, b - tp
    W, H = int(w * 1.36), int(h * 2.0)
    im = Image.new('RGBA', (W, H), bg); d = ImageDraw.Draw(im)
    d.text(((W - w) / 2 - l, (H - h) / 2 - tp), t, font=f, fill=fg)
    return rounded(im, 0.12)
def run(s):
    if s in NONE: return None
    src = Image.open(f'logos/{s}.png').convert('RGBA')
    if s in KEEP:
        c = np.array(src)[2, 2]
        if c[3] > 200 and c[:3].min() < 238: return src
        return trim(clear_bg(src), 0.02)
    im = src
    for op in S[s]:
        k = op[0]
        if k in ('H', 'V'):
            sg = segs(mask(im), 0 if k == 'H' else 1)[op[1]]
            im = im.crop((sg[0], 0, sg[1], im.height) if k == 'H' else (0, sg[0], im.width, sg[1])); im = trim(im, 0)
        elif k == 'Hr':
            sg = segs(mask(im), 0); im = trim(im.crop((sg[op[1]][0], 0, sg[op[2]][1], im.height)), 0)
        elif k == 'box': im = im.crop(op[1:])
        elif k == 'tile': return rounded(im.crop(op[1:]))
        elif k == 'redonly':
            a = np.array(im).astype(int); red = (a[..., 0] > 150) & (a[..., 1] < 110) & (a[..., 2] < 110)
            a[~red, 3] = 0; im = Image.fromarray(a.astype('uint8'))
        elif k == 'erase':
            a = np.array(im); a[op[2]:op[4], op[1]:op[3], 3] = 0; im = Image.fromarray(a)
        elif k == 'txt':
            bg = op[3] or '#%02x%02x%02x' % src.convert('RGB').getpixel((src.width // 2, 40))
            return text_tile(op[1], op[2], bg)
    return trim(clear_bg(im))
res = {}
for s, v in info.items():
    if not v: continue
    m = run(s)
    if m is None: res[s] = None; continue
    if max(m.size) > 640: m.thumbnail((640, 640), Image.LANCZOS)
    m.save(f'out/{s}.png'); res[s] = [m.width, m.height, round(m.width / m.height, 2)]
json.dump(res, open('marks.json', 'w'))
print(sum(1 for v in res.values() if v is None), 'uden', sum(1 for v in res.values() if v), 'med')
print(sorted([(v[2], s) for s, v in res.items() if v], reverse=True)[:15])
