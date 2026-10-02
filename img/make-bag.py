# Regenerates bag-top.png / bag-body.png from the original bag photo: paints out the
# brand logo, cuts away the white background, and splits off the folded top.
# Usage: python3 make-bag.py (edit `src` to point at the photo).
from PIL import Image, ImageFilter, ImageDraw
import random
from collections import deque
src='/root/.claude/uploads/4e625f96-1ef2-5154-b518-d2efe5cf5a94/ef7056a5-image.jpg'
im=Image.open(src).convert('RGB'); px=im.load(); W,H=im.size

# 1. paint out the logo: blend between clean paper on either side, then soften and re-grain
x0,x1,y0,y1=341,449,468,578
for y in range(y0,y1):
    L=[sum(px[x0-k,y][c] for k in range(1,6))/5 for c in range(3)]
    R=[sum(px[x1+k,y][c] for k in range(1,6))/5 for c in range(3)]
    for x in range(x0,x1):
        t=(x-x0)/(x1-x0)
        px[x,y]=tuple(int(L[c]*(1-t)+R[c]*t) for c in range(3))
box=(x0-8,y0-8,x1+8,y1+8)
soft=im.crop(box).filter(ImageFilter.GaussianBlur(4))
mask=Image.new('L',soft.size,0); ImageDraw.Draw(mask).rectangle((8,8,soft.width-9,soft.height-9),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(4))
im.paste(soft,box[:2],mask)
random.seed(1)
for y in range(y0,y1):
    for x in range(x0,x1):
        n=random.gauss(0,1.6); p=px[x,y]
        px[x,y]=tuple(max(0,min(255,int(v+n))) for v in p)
im.crop((300,440,500,620)).resize((400,360)).save('logo_after.png')

# 2. cut the white background away (flood fill from the edges)
alpha=Image.new('L',(W,H),255); a=alpha.load()
seen=bytearray(W*H); q=deque()
for x in range(W): q.extend([(x,0),(x,H-1)])
for y in range(H): q.extend([(0,y),(W-1,y)])
while q:
    x,y=q.popleft(); i=y*W+x
    if seen[i]: continue
    seen[i]=1
    if min(px[x,y])<244: continue
    a[x,y]=0
    if x>0: q.append((x-1,y))
    if x<W-1: q.append((x+1,y))
    if y>0: q.append((x,y-1))
    if y<H-1: q.append((x,y+1))
alpha=alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.8))
rgba=im.copy(); rgba.putalpha(alpha)

# 3. crop and split at the bottom of the folded band
bag=rgba.crop((192,254,604,1024))
bag.crop((0,0,bag.width,78)).save('bag-top.png',optimize=True)
bag.crop((0,78,bag.width,bag.height)).save('bag-body.png',optimize=True)
