await (async()=>{
const out={};
const vis=e=>{const r=e.getBoundingClientRect();return r.width>40&&r.height>14&&r.top<400;};
let cands=[...document.querySelectorAll('header img, header svg, a[href="/"] img, a[href="/"] svg, a[href$=".dk/"] img, a[href$=".dk/"] svg, [class*=logo] img, [class*=logo] svg, [class*=Logo] img, [class*=Logo] svg, img[alt*=logo i], img[src*=logo i]')].filter(vis);
cands=[...new Set(cands)];
out.logos=cands.slice(0,6).map(e=>{const r=e.getBoundingClientRect();return [e.tagName,(e.currentSrc||e.getAttribute('src')||'').split('?')[0].slice(-70),Math.round(r.width)+'x'+Math.round(r.height)]});
const cnt={};const add=(c,w)=>{if(!c)return;const m=c.match(/[\d.]+/g);if(!m)return;if(m.length>3&&+m[3]<0.5)return;const hx='#'+m.slice(0,3).map(x=>(+x|0).toString(16).padStart(2,'0')).join('');cnt[hx]=(cnt[hx]||0)+w;};
for(const el of document.querySelectorAll('body *')){if(el.closest('[id*=cookie i],[class*=cookie i],[id*=coi],[class*=coi-],[id*=consent i]'))continue;const r=el.getBoundingClientRect();if(r.width*r.height<1)continue;const s=getComputedStyle(el);add(s.backgroundColor,Math.min(r.width*r.height,150000)/1000);add(s.color,1);}
out.colors=Object.entries(cnt).sort((a,b)=>b[1]-a[1]).slice(0,12).map(([k,v])=>k+':'+Math.round(v)).join(' ');
const tc=document.querySelector('meta[name=theme-color]');if(tc)out.theme=tc.content;
const sc0=x=>{const src=(x.currentSrc||x.getAttribute('src')||'');return (/\.svg/i.test(src)?3:0)+(/logo/i.test(src)?1:0)+Math.min(x.getBoundingClientRect().width,400)/100-(/banner|hero|\.jpe?g/i.test(src)?5:0)-(/^data:/.test(src)?2:0);};const e=(window.__pick!==undefined?cands[window.__pick]:[...cands].sort((a,b)=>sc0(b)-sc0(a))[0]);
if(e){
 let src;
 if(e.tagName.toLowerCase()==='svg'){const c=e.cloneNode(true);const r=e.getBoundingClientRect();c.setAttribute('width',r.width);c.setAttribute('height',r.height);if(!c.getAttribute('xmlns'))c.setAttribute('xmlns','http://www.w3.org/2000/svg');
   const os=e.querySelectorAll('*'),cs=c.querySelectorAll('*');os.forEach((o,i)=>{const s=getComputedStyle(o);if(cs[i]){cs[i].setAttribute('fill',s.fill);if(s.stroke&&s.stroke!=='none')cs[i].setAttribute('stroke',s.stroke);}});
   src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(c));}
 else src=e.currentSrc||e.src;
 let o=document.getElementById('__lg');if(o)o.remove();
 o=document.createElement('div');o.id='__lg';o.style.cssText='position:fixed;inset:0;z-index:2147483647;background:'+(window.__bg||'#fff')+';padding:20px';
 const im=new Image();im.src=src;o.appendChild(im);document.documentElement.appendChild(o);
 await new Promise(r=>{im.onload=r;im.onerror=r;setTimeout(r,4000)});
 let w=im.naturalWidth||e.getBoundingClientRect().width, h=im.naturalHeight||e.getBoundingClientRect().height;
 const isSvg=/svg/i.test(src.slice(0,40))||/\.svg/i.test(src);
 let sc=isSvg?Math.min(600/w,220/h):Math.min(1,600/w,220/h);
 im.style.cssText='display:block;width:'+Math.round(w*sc)+'px;height:'+Math.round(h*sc)+'px';
 out.shown=[Math.round(w*sc),Math.round(h*sc),isSvg?'svg':'img'];
}
return JSON.stringify(out);
})()
