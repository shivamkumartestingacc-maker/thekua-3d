"""Cut front/back textures out of assets/thekua-angles.webp (4x3 angle sheet).

Run: python3 tools/make_textures.py
Writes assets/front.png, back.png, side.png (rim seen from the side), top.png (rim seen from above) (opaque, background bled with crust colour,
used as 3D textures) and assets/front-cut.png (transparent cut-out for 2D use).
"""
from PIL import Image, ImageFilter
import numpy as np

SHEET = 'assets/thekua-angles.webp'
CELLS = {'front': (0, 0), 'back': (1, 1), 'side': (0, 3), 'top': (2, 1)}  # (row, col) in the sheet
SIZES = {'front': (512, 768), 'back': (512, 768), 'side': (128, 512), 'top': (512, 192)}


def cut(a, r, c):
    H, W = a.shape[:2]
    ch, cw = H // 3, W // 4
    cell = a[r * ch + 4:(r + 1) * ch - 4, c * cw + 4:(c + 1) * cw - 4]
    mx, mn = cell.max(2), cell.min(2)
    mask = (mx - mn > 40) & (mx < 235)
    ys, xs = np.where(mask)
    crop = cell[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    m = Image.fromarray((mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1] * 255).astype('uint8'))
    m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(1))
    return crop, np.asarray(m)


def bleed(rgb, alpha, steps=60):
    # push edge colours outward so UV sampling near the rim never hits white
    rgb = rgb.astype(float).copy()
    known = alpha > 128
    for _ in range(steps):
        acc = np.zeros_like(rgb); n = np.zeros(known.shape)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            k = np.roll(known, (dy, dx), (0, 1)); v = np.roll(rgb, (dy, dx), (0, 1))
            acc += v * k[..., None]; n += k
        grow = (~known) & (n > 0)
        rgb[grow] = acc[grow] / n[grow][:, None]
        known = known | grow
    return rgb.clip(0, 255).astype('uint8')


a = np.asarray(Image.open(SHEET).convert('RGB')).astype(int)
for name, (r, c) in CELLS.items():
    rgb, alpha = cut(a, r, c)
    Image.fromarray(bleed(rgb, np.asarray(Image.fromarray(alpha).filter(ImageFilter.MinFilter(9))))).resize(SIZES[name], Image.LANCZOS).save(f'assets/{name}.png')
    if name == 'front':
        Image.fromarray(np.dstack([rgb.astype('uint8'), alpha])).save('assets/front-cut.png')
print('ok')
