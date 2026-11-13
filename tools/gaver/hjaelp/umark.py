#!/usr/bin/env python3
# umark.py IND.png slug [--tile x0 y0 x1 y1] [--crop x0 y0 x1 y1] [--invert HEX]
# Laver mærket til midten af koden (tools/gaver/marks/<slug>.png) ud fra et skærmbillede af symbolet eller seglet.
# Standard: hvid baggrund, der hænger sammen med kanten, bliver gennemsigtig, og der beskæres tæt.
# --tile: beskær til en plade med runde hjørner (fx hvidt segl på farvet felt). --invert: hvidt symbol på sort, farves HEX.
import sys, numpy as np
from PIL import Image, ImageDraw, ImageOps
from scipy import ndimage
a = sys.argv[1:]; src, slug = a[0], a[1]
def opt(k, n):
    return [int(v) if v.lstrip('-').isdigit() else v for v in a[a.index(k) + 1:a.index(k) + 1 + n]] if k in a else None
im = Image.open(src).convert('RGB')
if opt('--crop', 4): im = im.crop(tuple(opt('--crop', 4)))
inv = opt('--invert', 1)
if inv:
    hx = inv[0].lstrip('#'); col = tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
    rgba = Image.new('RGBA', im.size, col + (0,)); rgba.putalpha(ImageOps.grayscale(im))
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(rgba); im = bg.convert('RGB')
t = opt('--tile', 4)
if t:
    im = im.crop(tuple(t)).convert('RGBA')
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], int(min(im.size) * 0.16), fill=255)
    im.putalpha(m)
else:
    x = np.array(im.convert('RGBA'))
    w = x[..., :3].min(-1) > 238
    lab, n = ndimage.label(w); edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    x[np.isin(lab, list(edge)), 3] = 0
    ys, xs = np.where(x[..., 3] > 40)
    x = x[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    im = Image.fromarray(x); p = max(2, int(max(im.size) * 0.04))
    out = Image.new('RGBA', (im.width + 2 * p, im.height + 2 * p), (0, 0, 0, 0)); out.paste(im, (p, p)); im = out
if max(im.size) > 600: im.thumbnail((600, 600), Image.LANCZOS)
im.save('tools/gaver/marks/%s.png' % slug, optimize=True); print('marks/%s.png' % slug, im.size)
