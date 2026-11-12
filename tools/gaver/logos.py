#!/usr/bin/env python3
"""Beskærer et logo fra et skærmbillede (zoom med save_to_disk) og gemmer det som PNG.
Brug: python3 tools/gaver/logos.py SKÆRMBILLEDE.png UD.png [--invert HEX]
--invert HEX: logoet er hvidt på sort baggrund; det farves i HEX på hvid baggrund."""
import sys
from PIL import Image, ImageOps, ImageChops
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
if '--invert' in sys.argv:
    hx = sys.argv[sys.argv.index('--invert') + 1].lstrip('#')
    col = tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
    rgba = Image.new('RGBA', im.size, col + (0,)); rgba.putalpha(ImageOps.grayscale(im))
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(rgba); im = bg.convert('RGB')
diff = ImageChops.difference(im, Image.new('RGB', im.size, (255, 255, 255))).point(lambda p: 255 if p > 18 else 0)
im = im.crop(diff.getbbox())
im = ImageOps.expand(im, int(max(im.size) * 0.03), fill='white')
if im.width > 900: im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
im.save(dst, optimize=True); print(dst, im.size)
