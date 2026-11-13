import numpy as np, json, sys
from PIL import Image
def mask(im):
    a=np.array(im.convert('RGBA')).astype(int)
    al=a[...,3]
    corners=[a[0,0],a[0,-1],a[-1,0],a[-1,-1]]
    if min(c[3] for c in corners)<20: return al>40
    bg=np.median(np.array(corners)[:,:3],axis=0)
    d=np.abs(a[...,:3]-bg).sum(-1)
    return (d>60)&(al>40)
def segs(m,axis,gapfrac=0.025):
    p=m.any(axis=axis); n=len(p); gap=max(3,int(n*gapfrac))
    out=[];i=0
    while i<n:
        if p[i]:
            j=i
            while j<n:
                if p[j]: j+=1; continue
                k=j
                while k<n and not p[k]: k+=1
                if k-j>=gap or k==n: break
                j=k
            out.append((i,j)); i=j
        else: i+=1
    return out
if __name__=='__main__':
    info=json.load(open('info.json'))
    for s,v in info.items():
        if not v: continue
        im=Image.open(f'logos/{s}.png'); m=mask(im)
        print(s, im.size, 'H',segs(m,0),'V',segs(m,1))
