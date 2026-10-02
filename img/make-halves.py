# Splits cookie.png into the two pieces it breaks into: the front half (with its
# curled bottom) and the back half, which gets a slightly ragged, lighter broken edge.
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import random
random.seed(7)
c = Image.open('cookie.png').convert('RGBA'); W, H = c.size

# the front half's right edge (the fold), then the back half's own bottom edge
fold = [(88, 0), (92, 20), (107, 60), (130, 100), (152, 135), (167, 165), (180, 196)]
# the shadowed inside of the shell shows in a thin band just right of the front half's
# edge; it belongs to neither piece once they're apart, so both cuts skip it
front_edge = [(x - 11 + 7 * y / 196, y) for x, y in fold]
back_bottom = [(180, 196), (210, 206), (245, 216), (270, 228), (W, 242)]

def dense(pts, step=3):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(max(abs(x1 - x0), abs(y1 - y0)) / step))
        out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    return out + [pts[-1]]

edge = dense(fold)
ragged = [(x + 1.5 + random.uniform(0, 2.6), y) for x, y in edge]   # broken edge sits just right of the fold

back = Image.new('L', (W, H), 0)
ImageDraw.Draw(back).polygon(ragged + back_bottom[1:] + [(W, 0)], fill=255)
front = Image.new('L', (W, H), 0)
d = ImageDraw.Draw(front)
d.polygon([(0, 0)] + dense(front_edge) + back_bottom[1:] + [(W, H), (0, H)], fill=255)
d.rectangle((205, 0, W, 240), fill=0)   # stray rim bits of the back half

a = c.getchannel('A')
for name, m in (('front', front), ('back', back)):
    piece = c.copy(); piece.putalpha(ImageChops.multiply(a, m.filter(ImageFilter.GaussianBlur(.5))))
    if name == 'back':
        # a thin, lighter rim along the break: the cookie's thickness catching light
        rim = Image.new('L', (W, H), 0)
        ImageDraw.Draw(rim).line(ragged, fill=170, width=4)
        rim = ImageChops.multiply(rim.filter(ImageFilter.GaussianBlur(1)), piece.getchannel('A'))
        light = Image.new('RGBA', (W, H), (246, 214, 160, 255)); light.putalpha(rim)
        piece = Image.alpha_composite(piece, light)
    piece.save(f'cookie-{name}.png', optimize=True)
