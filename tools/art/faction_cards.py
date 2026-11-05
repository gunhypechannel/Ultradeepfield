# Faction selector cards (v305): each faction's painted flagship over a space scene in its colours.
from PIL import Image, ImageFilter, ImageDraw, ImageChops
import numpy as np, cv2, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
P = 'pack/raw/UDF_Flagship_Art_Pack/06_Flagships/'
W, H = 960, 317
COL = {'terran': ((20, 60, 160), (60, 150, 255), (150, 210, 255)), 'solar': ((150, 60, 10), (255, 150, 40), (255, 215, 130)),
       'nyx': ((110, 8, 20), (230, 40, 60), (255, 130, 140)), 'verdant': ((10, 80, 50), (40, 200, 120), (160, 255, 200))}
def nyx_red(a):
    hsv = cv2.cvtColor(a[..., :3], cv2.COLOR_RGB2HSV).astype(float); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    blu = (h >= 78) & (h <= 165); glow = blu & (((s > 95) & (v > 105)) | ((s > 150) & (v > 60))); rest = blu & ~glow
    h[glow] = 177; s[glow] = np.clip(s[glow] * 1.08 + 12, 0, 255); v[glow] = np.clip(v[glow] * 1.04, 0, 255); s[rest] = s[rest] * .35
    a[..., :3] = cv2.cvtColor(np.dstack([h, s, v]).astype(np.uint8), cv2.COLOR_HSV2RGB); return a
def noise(rng, sig):
    z = rng.random((H, W)); z = cv2.GaussianBlur(z, (0, 0), sig); return (z - z.min()) / (z.max() - z.min())
for f, (c0, c1, c2) in COL.items():
    rng = np.random.default_rng(sum(map(ord, f)) * 7)
    yy, xx = np.mgrid[0:H, 0:W]
    n = noise(rng, 38) * .6 + noise(rng, 14) * .3 + noise(rng, 5) * .1
    n = np.clip((n - .42) / .5, 0, 1) ** 1.8
    side = np.clip(1 - ((xx - W * .76) ** 2 / (W * .55) ** 2 + (yy - H * .28) ** 2 / (H * 1.0) ** 2), 0, 1)
    neb = n * (.25 + .75 * side)
    base = np.zeros((H, W, 3)); base[:] = (5, 8, 18)
    base += np.array(c0)[None, None, :] * neb[..., None] * 1.25 + np.array(c1)[None, None, :] * (neb ** 2.4)[..., None] * .8
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    for i in range(360):
        x, y = rng.random() * W, rng.random() * H; r = rng.random(); b = int(110 + r * 145); s = .45 if r < .88 else 1.1
        d.ellipse((x - s, y - s, x + s, y + s), fill=(b, b, min(255, b + 20)))
    fl = Image.new('RGB', (W, H)); fd = ImageDraw.Draw(fl); fx, fy = int(W * .76), int(H * .2)
    for r, a in [(70, 26), (30, 70), (11, 190), (4, 255)]: fd.ellipse((fx - r, fy - r, fx + r, fy + r), fill=tuple(int(c * a / 255) for c in c2))
    fd.line((fx - 150, fy, fx + 150, fy), fill=c2, width=1); fd.line((fx, fy - 70, fx, fy + 70), fill=c2, width=1)
    img = ImageChops.add(img, fl.filter(ImageFilter.GaussianBlur(5)))
    # a planet's limb across the bottom left, lit at its rim
    R = 560; cx, cy = -40, H + R - 96; dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    v = np.array(img).astype(float); inside = dist < R
    tex = cv2.GaussianBlur(rng.random((H, W)), (0, 0), 9); tex = (tex - tex.min()) / (tex.max() - tex.min())
    rim = np.clip(1 - (R - dist) / 70, 0, 1) ** 1.5
    for k in range(3): v[..., k][inside] = 10 + tex[inside] * 26 * (c0[k] / 160 + .3) + rim[inside] * c1[k] * .75
    atm = np.clip(1 - np.abs(dist - R) / 26, 0, 1) ** 2 * (dist >= R)
    v += np.array(c1)[None, None, :] * atm[..., None] * .7
    img = Image.fromarray(np.clip(v, 0, 255).astype(np.uint8)).convert('RGBA')
    sh = np.array(Image.open(P + f'flag-{f}.png').convert('RGBA'))
    if f == 'nyx': sh = nyx_red(sh)
    s = Image.fromarray(sh, 'RGBA'); s = s.crop(s.getbbox()); sw = int(W * .84); s = s.resize((sw, int(s.height * sw / s.width)), Image.LANCZOS).rotate(3, resample=Image.BICUBIC, expand=True)
    gl = Image.new('RGBA', img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(gl); ox, oy = (W - s.width) // 2 + 14, (H - s.height) // 2 + 4
    gd.ellipse((ox + 60, oy + s.height * .55, ox + s.width - 60, oy + s.height * 1.05), fill=c1 + (64,)); gl = gl.filter(ImageFilter.GaussianBlur(30))
    img = Image.alpha_composite(img, gl); img.alpha_composite(s, (ox, oy))
    v = np.array(img).astype(float); vg = np.clip(1 - (((xx - W / 2) / (W * .62)) ** 2 + ((yy - H / 2) / (H * .85)) ** 2) * .42, .5, 1); v[..., :3] *= vg[..., None]
    Image.fromarray(np.clip(v, 0, 255).astype(np.uint8)).convert('RGB').save(f'fac/{f}.webp', quality=82, method=6)
print('ok')
