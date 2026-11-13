#!/usr/bin/env python3
"""Beskærer et logo fra et skærmbillede (zoom med save_to_disk) og gemmer det som PNG.
Brug: python3 tools/gaver/logos.py SKÆRMBILLEDE.png UD.png [--invert HEX]
--invert HEX: logoet er hvidt på sort baggrund; det farves i HEX på hvid baggrund.
--bg HEX: logoet står på en farvet plade (fx hvid tekst på mørkeblå); der beskæres mod den farve, og pladen beholdes."""
import sys
from PIL import Image, ImageOps, ImageChops
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
if '--invert' in sys.argv:
    hx = sys.argv[sys.argv.index('--invert') + 1].lstrip('#')
    col = tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
    rgba = Image.new('RGBA', im.size, col + (0,)); rgba.putalpha(ImageOps.grayscale(im))
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(rgba); im = bg.convert('RGB')
bgc = (255, 255, 255)
if '--bg' in sys.argv:
    h2 = sys.argv[sys.argv.index('--bg') + 1].lstrip('#'); bgc = tuple(int(h2[i:i+2], 16) for i in (0, 2, 4))
diff = ImageChops.difference(im, Image.new('RGB', im.size, bgc)).convert('L').point(lambda p: 255 if p > 18 else 0)
im = im.crop(diff.getbbox())
im = ImageOps.expand(im, int(max(im.size) * (0.08 if '--bg' in sys.argv else 0.03)), fill=bgc)
if im.width > 900: im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
im.save(dst, optimize=True); print(dst, im.size)
