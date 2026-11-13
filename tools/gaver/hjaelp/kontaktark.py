import sys
from PIL import Image, ImageDraw
G='/home/claude/roundqr/tools/gaver/'
slugs=sys.argv[2:]; out=sys.argv[1]
cw,ch=300,110; cols=4; rows=(len(slugs)+cols-1)//cols
S=Image.new('RGB',(cols*cw,rows*ch),(235,235,235)); d=ImageDraw.Draw(S)
import os
for i,s in enumerate(slugs):
    x,y=(i%cols)*cw,(i//cols)*ch
    L=Image.open(G+'smv/logos/%s.png'%s).convert('RGB'); L.thumbnail((200,90))
    S.paste(L,(x+4,y+14))
    if os.path.exists(G+'marks/%s.png'%s):
        M=Image.open(G+'marks/%s.png'%s).convert('RGBA'); M.thumbnail((80,80))
        bg=Image.new('RGBA',(84,84),(255,255,255,255)); bg.alpha_composite(M,((84-M.width)//2,(84-M.height)//2)); S.paste(bg.convert('RGB'),(x+210,y+14))
    d.text((x+4,y+1),s,fill=(200,0,0))
S.save(out)
