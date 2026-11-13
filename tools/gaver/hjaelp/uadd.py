#!/usr/bin/env python3
# uadd.py slug "Navn" "Kort navn" website sprog(kommasepareret) primary secondary [accent] [--note TEKST]
# Lægger et universitet i universiteter/brands.json. Logo forventes i universiteter/logos/<slug>.png.
import json, sys
a = sys.argv[1:]; note = ''
if '--note' in a: i = a.index('--note'); note = a[i + 1]; a = a[:i] + a[i + 2:]
p = 'tools/gaver/universiteter/brands.json'
d = json.load(open(p, encoding='utf-8'))
slug, name, short, site, langs, pri, sec = a[:7]
c = {'primary': pri, 'secondary': sec}
if len(a) > 7 and a[7]: c['accent'] = a[7]
c['text'] = '#222222'
b = {'id': slug, 'name': name, 'short': short, 'website': site, 'colors': c, 'languages': langs.split(','),
     'source': 'aflæst på hjemmesiden', 'logo_file': 'tools/gaver/universiteter/logos/%s.png' % slug, 'logo_note': note}
d = [x for x in d if x['id'] != slug] + [b]
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('ok', slug)
