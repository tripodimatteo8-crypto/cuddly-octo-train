import sys, numpy as np
from PIL import Image, ImageFilter
OUT = sys.argv[1]
STOP = [(-1.0, (0x32, 0x52, 0x5C)), (-0.45, (0x1A, 0x22, 0x26)), (0.0, (0x12, 0x11, 0x14)), (0.25, (0x30, 0x18, 0x18)),
        (0.48, (0x95, 0x2E, 0x27)), (0.66, (0xDA, 0x4E, 0x34)), (0.8, (0xEA, 0x6F, 0x41)), (1.0, (0xCE, 0x93, 0x58))]
def colora(t):
    t = np.clip(t, -1, 1); out = np.zeros(t.shape + (3,))
    for (a, ca), (b, cb) in zip(STOP, STOP[1:]):
        m = (t >= a) & (t <= b); f = ((t - a) / (b - a))[m][:, None]
        out[m] = np.array(ca) * (1 - f) + np.array(cb) * f
    return out
def campo(W, H, macchie):
    y, x = np.mgrid[0:H, 0:W] / max(W, H)
    t = np.zeros((H, W))
    for cx, cy, sx, sy, v, ang in macchie:   # coordinate in frazioni della larghezza
        c, s = np.cos(ang), np.sin(ang); dx, dy = x - cx, y - cy * H / max(W, H)
        u, w = c * dx + s * dy, -s * dx + c * dy
        t += v * np.exp(-(u ** 2 / (2 * sx ** 2) + w ** 2 / (2 * sy ** 2)))
    return t
def genera(nome, W, H, macchie, grana=11, seme=1):
    rng = np.random.default_rng(seme)
    t = campo(W, H, macchie)
    # leggera turbolenza per bordi organici
    # turbolenza morbida su due scale, poi sfocata: bordi organici, niente quadretti
    tur = np.zeros((H, W))
    for passo, peso in [(9, 0.22), (22, 0.08)]:
        n = Image.fromarray((rng.random((passo * H // W + 2, passo + 2)) * 255).astype('uint8')).resize((W, H), Image.BICUBIC)
        tur += (np.asarray(n.filter(ImageFilter.GaussianBlur(W / passo / 3))) / 255 - 0.5) * peso
    t = t * (1 + tur * 2.2) + tur * 0.25
    t = np.tanh(t * 1.15) * 0.93      # comprime i picchi: la pesca resta solo al centro delle macchie
    rgb = colora(t)
    rgb += rng.normal(0, grana, (H, W, 1))          # grana monocromatica
    rgb += rng.normal(0, grana * 0.35, (H, W, 3))   # un filo di grana colorata
    Image.fromarray(np.clip(rgb, 0, 255).astype('uint8')).save(f'{OUT}/{nome}.jpg', quality=93)
# biglietti 91x61 mm a 600 dpi (2150x1441)
genera('biglietto-a', 2150, 1441, [(0.78, 0.62, 0.22, 0.13, 1.05, -0.35), (0.55, 0.85, 0.16, 0.08, 0.7, 0.1), (0.18, 0.98, 0.2, 0.1, -0.95, 0.0)], seme=3)
genera('biglietto-b', 2150, 1441, [(0.5, 0.55, 0.6, 0.075, 1.0, 0.08), (0.88, 0.42, 0.18, 0.09, 0.8, -0.4), (0.3, 1.0, 0.25, 0.1, -0.9, 0.0)], seme=7)
genera('biglietto-c', 2150, 1441, [(0.62, 0.48, 0.1, 0.26, 1.05, 0.05), (0.79, 0.62, 0.09, 0.22, 0.95, -0.05), (0.62, 0.2, 0.05, 0.05, 0.9, 0)], seme=11)
# sito: apertura e tessera
genera('sito-apertura', 2400, 1350, [(0.5, 0.95, 0.35, 0.16, 1.05, 0.0), (0.82, 0.7, 0.18, 0.1, 0.75, -0.5), (0.12, 1.05, 0.22, 0.12, -0.9, 0.2)], seme=5)
genera('sito-alone', 1600, 1600, [(0.5, 0.5, 0.28, 0.28, 0.85, 0)], grana=9, seme=9)
print('ok')
