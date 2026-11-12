# whitefix.py IN OUT HEX: logo på sort bund; hvide/grå (umættede) pixels farves HEX, farvede beholdes, sort bliver hvid
import sys,colorsys
from PIL import Image
im=Image.open(sys.argv[1]).convert('RGB'); hx=sys.argv[3].lstrip('#'); col=tuple(int(hx[i:i+2],16) for i in (0,2,4))
px=im.load()
for y in range(im.height):
  for x in range(im.width):
    r,g,b=px[x,y]; mx,mn=max(r,g,b),min(r,g,b)
    if mx-mn<40:  # grå/hvid/sort: alpha = lysstyrke
      a=mx/255; px[x,y]=tuple(int(255*(1-a)+c*a) for c in col)
    else:  # farvet: komponer over hvid i stedet for sort (antag fuld dækning)
      pass
im.save(sys.argv[2])
