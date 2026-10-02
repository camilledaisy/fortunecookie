# Cuts the cracked-cookie photo into left half, right half and crumb PNGs,
# with the blank slip removed and the cookie it hid filled back in.
from PIL import Image, ImageDraw, ImageFilter
from collections import deque
import json, random
src='cracked-cookie.jpg'   # the original photo
out=''
im=Image.open(src).convert('RGB'); W,H=im.size; px=im.load()

# background + soft shadows: flood fill through pale, unsaturated pixels from the border
bgmask=bytearray(W*H); q=deque()
for x in range(W): q.extend([(x,0),(x,H-1)])
for y in range(H): q.extend([(0,y),(W-1,y)])
def pale(p): return max(p)-min(p)<24 and sum(p)/3>150
while q:
    x,y=q.popleft(); i=y*W+x
    if bgmask[i] or not pale(px[x,y]): continue
    bgmask[i]=1
    for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
        if 0<=nx<W and 0<=ny<H and not bgmask[ny*W+nx]: q.append((nx,ny))

out_im=Image.new('RGBA',(W,H)); o=out_im.load()
for y in range(H):
    for x in range(W):
        r,g,b=px[x,y]
        if bgmask[y*W+x]:
            L=(r+g+b)/3; a=max(0,min(160,int((248-L)*4)))
            o[x,y]=(0,0,0,0)               # drop the photo shadow; the page adds its own
        else:
            o[x,y]=(r,g,b,255)

def smp_ok(x,y): return not (350<=x<425 and y>=250)
# the slip: clear it, then refill only inside each half's outline, borrowing cookie
# from above/below along that half's rim direction, and smooth the seams.
slip=[(217,150),(495,114),(505,187),(259,218)]
sm=Image.new('L',(W,H),0); ImageDraw.Draw(sm).polygon(slip,fill=255); sm=sm.filter(ImageFilter.MaxFilter(5)); smp=sm.load()
base=out_im.copy(); bp=base.load()
def edgeL(y): return 275+(287-275)*(y-147)/(218-147)     # left half's right edge under the slip
def edgeR(y): return 445+(415-445)*(y-117)/(192-117)     # right half's left edge under the slip
def ytop(x): return 150+(114-150)*(x-217)/(495-217)
def ybot(x): return 218+(187-218)*(x-259)/(505-259)
def take(x,y):
    if 0<=x<W and 0<=y<H and not smp[x,y] and smp_ok(x,y):
        p=bp[x,y]
        if p[3]==255: return p
    return None
res=base.copy(); r=res.load()
for y in range(H):
    for x in range(W):
        if not smp[x,y]: continue
        inL = x < edgeL(y) and x < 340
        inR = x > edgeR(y) and x > 380
        if not (inL or inR): r[x,y]=(0,0,0,0); continue
        dx = 19 if inL else -30
        A=B=None
        for d in (76,62,92,110,130):
            A=A or take(x-round(dx*d/76),y-d); B=B or take(x+round(dx*d/76),y+d)
        t=max(0,min(1,(y-ytop(x))/max(1,ybot(x)-ytop(x))))
        if A and B: r[x,y]=tuple(int(A[c]*(1-t)+B[c]*t) for c in range(3))+(255,)
        else: r[x,y]=A or B or (226,176,118,255)
seam=Image.new('L',(W,H),0); d=ImageDraw.Draw(seam); d.line(slip+[slip[0]],fill=255,width=7)
seam=seam.filter(ImageFilter.GaussianBlur(2))
out_im=Image.composite(res.filter(ImageFilter.GaussianBlur(1.6)),res,seam)
# soften the alpha edge a touch
al=out_im.getchannel('A').filter(ImageFilter.GaussianBlur(.6)); out_im.putalpha(al)

pieces={'left':(60,70,345,356),'right':(380,70,690,356),'crumb':(352,252,422,316)}
frame=(60,70,690,356)
meta={'frame':[frame[2]-frame[0],frame[3]-frame[1]]}
for name,box in pieces.items():
    c=out_im.crop(box)
    if name!='crumb':   # keep the crumb (and its shadow) out of the halves
        cm=c.load(); cx0=356-box[0]; cx1=418-box[0]
        for y in range(256-box[1],312-box[1]):
            for x in range(max(0,cx0),min(c.width,cx1)): cm[x,y]=(0,0,0,0)
    bb=c.getchannel('A').point(lambda v:255 if v>6 else 0).getbbox()
    c=c.crop(bb); c.save(out+f'open-{name}.png',optimize=True)
    gx=box[0]+bb[0]-frame[0]; gy=box[1]+bb[1]-frame[1]
    meta[name]=dict(left=gx,top=gy,w=c.width,h=c.height)
json.dump(meta,open('open_meta.json','w')); print(meta)
pv=Image.new('RGB',out_im.size,(40,60,90)); pv.paste(out_im,(0,0),out_im); pv.save('open_check.png')
