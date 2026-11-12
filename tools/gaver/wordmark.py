#!/usr/bin/env python3
"""Laver et tekstlogo, når kommunen ikke har et logo, der må bruges. Brug: wordmark.py UD.png "Linje 1" "Linje 2" HEX"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
out, l1, l2, col = sys.argv[1:5]
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 96)
im = Image.new('RGB', (1400, 260), 'white'); d = ImageDraw.Draw(im)
d.text((20, 20), l1, font=f, fill=col); d.text((20, 130), l2, font=f, fill=col)
im = ImageOps.expand(im.crop(ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()), 14, fill='white'); im.save(out); print(out, im.size)
