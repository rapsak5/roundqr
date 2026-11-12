#!/usr/bin/env python3
# add.py slug "Navn Kommune" website primary secondary [accent] [--genitive X]
import json,sys
a=sys.argv[1:]; p='tools/gaver/kommuner/brands.json'
d=json.load(open(p)); slug,name,site,pri,sec=a[:5]; acc=a[5] if len(a)>5 and a[5] else None
gen=name+'s' if not name.endswith('s') else name
c={'primary':pri,'secondary':sec}
if acc: c['accent']=acc
c['text']='#222222'
b={'id':slug,'name':name,'short':name,'genitive':gen,'website':site,'colors':c,'source':'aflæst på hjemmesiden','logo_file':'tools/gaver/kommuner/logos/%s.png'%slug}
d=[x for x in d if x['id']!=slug]+[b]; json.dump(d,open(p,'w'),ensure_ascii=False,indent=1); print('ok',slug)
