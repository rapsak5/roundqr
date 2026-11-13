import sys, json, numpy as np
from PIL import Image, ImageOps
from scipy import ndimage
R='/home/claude/work/raw/'; G='/home/claude/roundqr/tools/gaver/'
def hx(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)
def render(slug, mode):
    a=np.asarray(Image.open(R+slug+'.png').convert('RGB')).astype(float)
    if mode=='w': out=a
    elif mode.startswith('rc:'):
        tgt=hx(mode[3:]); g=a.mean(-1); al=np.clip((255-g)/max(1,(255-g.min())),0,1)
        out=al[...,None]*tgt+(1-al[...,None])*255
    else:
        kind,tgt=mode.split(':')[0],hx(mode.split(':')[1])
        bgv=float(mode.split(':')[2]) if mode.count(':')>1 else 0.0
        mx=a.max(-1); mn=a.min(-1); sat=mx-mn
        alpha=np.clip((mx-bgv)/(255-bgv),0,1)
        white=np.ones(3)*255
        out=alpha[...,None]*tgt+(1-alpha[...,None])*white
        if kind=='mix':
            col=sat>45
            if col.any():
                sc=np.percentile(mx[col],90); ac=np.clip(mx/sc,0,1)
                cpx=a/np.maximum(ac,1e-3)[...,None]; cpx=np.clip(cpx,0,255)
                co=ac[...,None]*cpx+(1-ac[...,None])*white
                out[col]=co[col]
    im=Image.fromarray(np.clip(out,0,255).astype('uint8'))
    m=np.asarray(im.convert('L'))<235
    ys,xs=np.where(m); im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    im=ImageOps.expand(im,int(max(im.size)*0.03),fill=(255,255,255))
    return im
def segs(m,axis,mingap):
    prof=m.any(axis=axis); idx=np.where(prof)[0]
    out=[]; s=idx[0]; p=idx[0]
    for i in idx[1:]:
        if i-p>mingap: out.append((s,p)); s=i
        p=i
    out.append((s,p)); return out
def mark(im, how):
    a=np.asarray(im.convert('L'))<200
    H,W=a.shape
    if how=='all': box=(0,0,W,H)
    elif how.startswith('frac:'):
        f=[float(v) for v in how[5:].split(',')]; box=(int(f[0]*W),int(f[1]*H),int(f[2]*W),int(f[3]*H))
    else:
        parts=how.split('-'); box=(0,0,W,H)
        for p in parts:
            x0,y0,x1,y1=box; sub=a[y0:y1,x0:x1]
            if p in('left','right','mid'):
                s=segs(sub,0,max(4,int(W*0.02))); s=s[0] if p=='left' else s[-1] if p=='right' else s[len(s)//2]
                box=(x0+s[0],y0,x0+s[1]+1,y1)
            else:
                s=segs(sub,1,max(4,int(H*0.03))); s=s[0] if p=='top' else s[-1]
                box=(x0,y0+s[0],x1,y0+s[1]+1)
    c=im.crop(box); m=np.asarray(c.convert('L'))<235; ys,xs=np.where(m); c=c.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    c=c.convert('RGBA'); arr=np.array(c); wl=(arr[...,:3].min(-1)>238)
    lab,n=ndimage.label(wl); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    arr[np.isin(lab,list(edge)),3]=0
    c=Image.fromarray(arr); p=max(2,int(max(c.size)*0.04)); o=Image.new('RGBA',(c.width+2*p,c.height+2*p),(0,0,0,0)); o.paste(c,(p,p)); return o
spec=json.load(open(sys.argv[1]))
for slug,(mode,mk) in spec.items():
    if len(sys.argv)>2 and slug not in sys.argv[2:]: continue
    im=render(slug,mode)
    if im.width<360 and im.height<150: f=min(360/im.width,150/im.height); im=im.resize((round(im.width*f),round(im.height*f)),Image.LANCZOS)
    if im.width>900: im=im.resize((900,round(im.height*900/im.width)),Image.LANCZOS)
    im.save(G+'smv/logos/%s.png'%slug,optimize=True)
    if mk!='none':
        mark(im,mk).save(G+'marks/%s.png'%slug,optimize=True)
    print(slug,im.size,mk)
