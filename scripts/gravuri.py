"""Gravurile din prezentarea Agenți, desenate ca SVG (alb pe cerneală).

Înlocuiesc gravurile Hermes descărcate de pe site-ul lor: aceeași tehnică (hașură,
raze, puncte de tipar), dar cu subiecte din slide-uri, fără figuri mitologice.
Rulează: python3 scripts/gravuri.py  (scrie assets/agenti/gravura-*.svg)
"""
import math, random, os

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'agenti')
INK = '#070706'
W_ = '#ece6d8'


def f(x):
    return f'{x:.1f}'.rstrip('0').rstrip('.')


class Svg:
    def __init__(self, w, h, seed):
        self.w, self.h = w, h
        self.r = random.Random(seed)
        self.defs, self.body = [], []
        self.n = 0

    def uid(self, p):
        self.n += 1
        return f'{p}{self.n}'

    def hatch(self, angle, gap, width=1.2):
        """Un model de linii paralele; gap mic = ton închis (mai multă cerneală albă)."""
        i = self.uid('h')
        self.defs.append(
            f'<pattern id="{i}" width="{f(gap)}" height="10" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate({angle})"><line x1="0" y1="0" x2="0" y2="10" '
            f'stroke="{W_}" stroke-width="{width * 1.45}"/></pattern>')
        return f'url(#{i})'

    def clip(self, shape):
        i = self.uid('c')
        self.defs.append(f'<clipPath id="{i}">{shape}</clipPath>')
        return f'url(#{i})'

    def add(self, s):
        self.body.append(s)

    def rays(self, cx, cy, r0, r1, n, width=1.1, jitter=0.35, op=0.8):
        out = []
        for k in range(n):
            a = 2 * math.pi * k / n + self.r.uniform(-0.01, 0.01)
            rr = r1 * (1 - self.r.random() * jitter)
            out.append(f'M{f(cx + r0 * math.cos(a))} {f(cy + r0 * math.sin(a))}L{f(cx + rr * math.cos(a))} {f(cy + rr * math.sin(a))}')
        self.add(f'<path d="{"".join(out)}" stroke="{W_}" stroke-width="{width * 1.35}" opacity="{min(1, op * 1.25)}" fill="none"/>')

    def stipple(self, n, box, rmax=1.6, op=0.55, fn=None):
        x0, y0, x1, y1 = box
        pts = []
        while len(pts) < n:
            x, y = self.r.uniform(x0, x1), self.r.uniform(y0, y1)
            if fn is None or fn(x, y):
                pts.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(self.r.uniform(.4, rmax))}"/>')
        self.add(f'<g fill="{W_}" opacity="{op}">{"".join(pts)}</g>')

    def scanlines(self, gap=5, op=0.10):
        op = op * 1.8
        """Liniile de raster peste tot, ca în gravurile tipărite."""
        p = self.hatch(0, gap, 1)
        self.add(f'<rect width="{self.w}" height="{self.h}" fill="{p}" opacity="{op}" transform="rotate(90 {self.w/2} {self.h/2})"/>')

    def save(self, name):
        grain = ('<filter id="grain" x="0" y="0" width="100%" height="100%">'
                 '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>'
                 '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .9 -.35"/></filter>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}">'
               f'<defs>{grain}{"".join(self.defs)}</defs>'
               f'<rect width="100%" height="100%" fill="{INK}"/>'
               f'{"".join(self.body)}'
               f'<rect width="100%" height="100%" filter="url(#grain)" opacity=".13"/></svg>')
        with open(os.path.join(HERE, name), 'w') as fh:
            fh.write(svg)
        print(name, len(svg) // 1024, 'KB')


def sphere(s, cx, cy, R, light=(-0.55, -0.6)):
    """Glob gravat: meridiane, paralele și hașură mai deasă pe partea din umbră."""
    body = f'<circle cx="{cx}" cy="{cy}" r="{R}"/>'
    cp = s.clip(body)
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{INK}"/>')
    # tonuri: trei semilune de hașură, tot mai dese spre umbră
    lx, ly = light
    for k, (gap, ang) in enumerate([(9, 35), (6, -25), (4.2, 80)]):
        off = R * (0.55 + 0.38 * k)
        mx, my = cx - lx * off * 0.9, cy - ly * off * 0.9
        cp2 = s.clip(f'<circle cx="{f(mx)}" cy="{f(my)}" r="{f(R * (1.05 - 0.18 * k))}"/>')
        s.add(f'<g clip-path="{cp}"><rect x="{cx-R}" y="{cy-R}" width="{2*R}" height="{2*R}" fill="{s.hatch(ang, gap, 1.1)}" clip-path="{cp2}" opacity=".85"/></g>')
    g = []
    for k in range(-4, 5):  # paralele
        y = cy + R * k / 5
        rx = math.sqrt(max(R * R - (y - cy) ** 2, 0))
        g.append(f'<ellipse cx="{cx}" cy="{f(y)}" rx="{f(rx)}" ry="{f(rx * 0.16)}"/>')
    for k in range(0, 6):  # meridiane
        rx = R * abs(math.cos(math.pi * k / 6))
        g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{f(rx)}" ry="{R}"/>')
    s.add(f'<g fill="none" stroke="{W_}" stroke-width="1.6" opacity=".9" clip-path="{cp}">{"".join(g)}</g>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{W_}" stroke-width="3"/>')


def node(s, x, y, r, fill=True):
    s.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{INK}" stroke="{W_}" stroke-width="2.2"/>')
    if fill:
        s.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{s.hatch(45, 3.2, 1)}"/>')
        s.add(f'<circle cx="{f(x - r * .3)}" cy="{f(y - r * .3)}" r="{f(r * .28)}" fill="{W_}"/>')


def bundle(s, x0, y0, x1, y1, n=7, spread=10, op=.75):
    """Un mănunchi de fire între două noduri, ca un cablu gravat."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    d = []
    for k in range(n):
        o = (k - (n - 1) / 2) * spread / n
        bend = s.r.uniform(-0.08, 0.08) * L
        mx, my = (x0 + x1) / 2 + nx * (o * 3 + bend), (y0 + y1) / 2 + ny * (o * 3 + bend)
        d.append(f'M{f(x0 + nx * o)} {f(y0 + ny * o)}Q{f(mx)} {f(my)} {f(x1 + nx * o)} {f(y1 + ny * o)}')
    s.add(f'<path d="{"".join(d)}" fill="none" stroke="{W_}" stroke-width="1" opacity="{op}"/>')


# 1. Copertă: nucleul agentului, un glob cu orbite și raze (în locul figurii cu opt brațe)
def cover():
    s = Svg(950, 1024, 1)
    cx, cy = 520, 500
    s.add(f'<rect x="170" y="190" width="700" height="620" fill="none" stroke="{W_}" stroke-width="2" opacity=".55"/>')
    s.add(f'<rect x="170" y="190" width="700" height="620" fill="{s.hatch(-35, 5, 1)}" opacity=".6"/>')
    s.rays(cx, cy, 250, 520, 180, 1, .45, .7)
    s.rays(cx, cy, 250, 380, 90, 2, .2, .8)
    for k, (rx, ry, rot) in enumerate([(380, 110, -18), (330, 95, 28), (420, 70, 4)]):
        s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" fill="none" stroke="{W_}" stroke-width="1.4" stroke-dasharray="{"2 7" if k == 1 else "none"}" opacity=".8"/>')
    sphere(s, cx, cy, 210)
    for a, rx, ry, rot, r in [(200, 380, 110, -18, 22), (330, 330, 95, 28, 16), (20, 420, 70, 4, 18), (120, 330, 95, 28, 12)]:
        t = math.radians(a); rr = math.radians(rot)
        x, y = rx * math.cos(t), ry * math.sin(t)
        node(s, cx + x * math.cos(rr) - y * math.sin(rr), cy + x * math.sin(rr) + y * math.cos(rr), r)
    s.stipple(900, (0, 0, 950, 1024), 1.3, .45, lambda x, y: math.hypot(x - cx, y - cy) > 300)
    s.scanlines(6, .08)
    s.save('gravura-nucleu.svg')


# 2. Memorie: fișierul cu sertare, unul tras afară cu fișe (ce a învățat agentul)
def memory():
    s = Svg(1440, 1800, 2)
    x0, y0, cw, ch, cols, rows = 300, 250, 280, 190, 3, 6
    s.add(f'<rect x="{x0-30}" y="{y0-30}" width="{cols*cw+60}" height="{rows*ch+60}" fill="{s.hatch(-20, 5, 1.1)}" opacity=".5"/>')
    s.add(f'<rect x="{x0-30}" y="{y0-30}" width="{cols*cw+60}" height="{rows*ch+60}" fill="none" stroke="{W_}" stroke-width="3"/>')
    for r_ in range(rows):
        for c in range(cols):
            x, y = x0 + c * cw, y0 + r_ * ch
            if (r_, c) == (3, 1):
                continue
            s.add(f'<rect x="{x+10}" y="{y+10}" width="{cw-20}" height="{ch-20}" fill="{INK}" stroke="{W_}" stroke-width="2"/>')
            s.add(f'<rect x="{x+10}" y="{y+10}" width="{cw-20}" height="{ch-20}" fill="{s.hatch(90, 4.5 + (r_ + c) % 3, 1)}" opacity=".55"/>')
            s.add(f'<rect x="{x+cw/2-45}" y="{y+40}" width="90" height="34" fill="{INK}" stroke="{W_}" stroke-width="1.6"/>')
            s.add(f'<rect x="{x+cw/2-30}" y="{y+ch-62}" width="60" height="14" rx="7" fill="none" stroke="{W_}" stroke-width="2.4"/>')
    # sertarul scos, în perspectivă
    x, y = x0 + cw, y0 + 3 * ch
    s.add(f'<rect x="{x+10}" y="{y+10}" width="{cw-20}" height="{ch-20}" fill="{INK}" stroke="{W_}" stroke-width="2"/>')
    s.add(f'<rect x="{x+10}" y="{y+10}" width="{cw-20}" height="{ch-20}" fill="{s.hatch(0, 3, 1)}" opacity=".7"/>')
    px, py, dw, dh, dd = x - 60, y + 250, cw + 120, ch + 30, 260
    s.add(f'<path d="M{x+10} {y+ch-10}L{px} {py+dh}L{px+dw} {py+dh}L{x+cw-10} {y+ch-10}Z" fill="{s.hatch(60, 4, 1)}" stroke="{W_}" stroke-width="2"/>')
    for k in range(9):  # fișele, ca niște dinți de pieptene
        fx = px + 40 + k * (dw - 80) / 8
        s.add(f'<path d="M{f(fx)} {py+dh-10}L{f(fx+ (x+cw/2-fx)*.35)} {f(py+dh-dd*.9)}" stroke="{W_}" stroke-width="{3 if k%3==0 else 1.6}"/>')
    s.add(f'<rect x="{px}" y="{py+dh}" width="{dw}" height="{dh*.9}" fill="{INK}" stroke="{W_}" stroke-width="3"/>')
    s.add(f'<rect x="{px}" y="{py+dh}" width="{dw}" height="{dh*.9}" fill="{s.hatch(-30, 6, 1.1)}" opacity=".7"/>')
    s.add(f'<rect x="{px+dw/2-60}" y="{py+dh+50}" width="120" height="44" fill="{INK}" stroke="{W_}" stroke-width="2"/>')
    s.rays(x + cw / 2, py + dh + 30, 200, 700, 120, 1, .5, .45)
    s.stipple(1600, (0, 0, 1440, 1800), 1.4, .35, lambda a, b: not (x0 - 30 < a < x0 + cols * cw + 30 and y0 - 30 < b < y0 + rows * ch + 30))
    s.scanlines(6, .08)
    s.save('gravura-memorie.svg')


# 3. Conectare: un hub cu șase canale (Telegram, Discord, Slack…) legate prin mănunchiuri de fire
def connect():
    s = Svg(1600, 1411, 3)
    cx, cy = 800, 705
    s.rays(cx, cy, 170, 760, 220, 1, .55, .45)
    pts = []
    for k in range(6):
        a = math.radians(-90 + k * 60)
        pts.append((cx + 470 * math.cos(a), cy + 470 * math.sin(a)))
    for (x, y) in pts:
        bundle(s, cx, cy, x, y, 9, 34, .8)
    for i in range(6):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % 6]
        bundle(s, x0, y0, x1, y1, 3, 8, .35)
    for (x, y) in pts:
        node(s, x, y, 62)
        s.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="92" fill="none" stroke="{W_}" stroke-width="1.2" stroke-dasharray="3 6"/>')
    sphere(s, cx, cy, 165)
    s.stipple(1400, (0, 0, 1600, 1411), 1.3, .4)
    s.scanlines(6, .08)
    s.save('gravura-canale.svg')


# 4. Automatizare: cadranul unui ceas gravat, cu roți dințate („în fiecare dimineață la 8”)
def automation():
    s = Svg(1488, 1304, 4)
    cx, cy, R = 744, 652, 470

    def gear(x, y, r, teeth, op):
        d = []
        for k in range(teeth * 2):
            a = math.pi * k / teeth
            rr = r if k % 2 == 0 else r * .86
            a2 = a + math.pi / teeth
            d.append(f'{"M" if k == 0 else "L"}{f(x + rr * math.cos(a))} {f(y + rr * math.sin(a))}L{f(x + rr * math.cos(a2))} {f(y + rr * math.sin(a2))}')
        s.add(f'<path d="{"".join(d)}Z" fill="{s.hatch(30, 5, 1)}" stroke="{W_}" stroke-width="2" opacity="{op}"/>')
        s.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r*.5)}" fill="{INK}" stroke="{W_}" stroke-width="2" opacity="{op}"/>')
        s.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r*.12)}" fill="{W_}" opacity="{op}"/>')

    gear(250, 1080, 230, 18, .75)
    gear(1270, 230, 190, 16, .75)
    s.rays(cx, cy, R, R + 260, 120, 1, .5, .5)
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{INK}" stroke="{W_}" stroke-width="4"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{s.hatch(-45, 7, 1)}" opacity=".45"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{R-60}" fill="{INK}" stroke="{W_}" stroke-width="1.5"/>')
    ticks = []
    for k in range(60):
        a = 2 * math.pi * k / 60
        r0 = R - 60 - (38 if k % 5 == 0 else 16)
        ticks.append(f'M{f(cx + r0 * math.cos(a))} {f(cy + r0 * math.sin(a))}L{f(cx + (R - 62) * math.cos(a))} {f(cy + (R - 62) * math.sin(a))}')
    s.add(f'<path d="{"".join(ticks)}" stroke="{W_}" stroke-width="2.4"/>')
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        s.add(f'<text x="{f(cx + (R - 140) * math.cos(a))}" y="{f(cy + (R - 140) * math.sin(a) + 18)}" font-family="Georgia,serif" font-size="52" fill="{W_}" text-anchor="middle">{12 if k == 0 else k}</text>')
    # arcul de la 8:00 la 8:30, porțiunea „programată”
    a0, a1 = math.radians(8 * 30 - 90), math.radians(8.5 * 30 - 90)
    r = R - 30
    s.add(f'<path d="M{f(cx + r*math.cos(a0))} {f(cy + r*math.sin(a0))}A{r} {r} 0 0 1 {f(cx + r*math.cos(a1))} {f(cy + r*math.sin(a1))}" fill="none" stroke="{W_}" stroke-width="16"/>')

    def hand(ang, length, w):
        a = math.radians(ang - 90)
        x, y = cx + length * math.cos(a), cy + length * math.sin(a)
        nx, ny = -math.sin(a) * w, math.cos(a) * w
        s.add(f'<path d="M{f(cx+nx)} {f(cy+ny)}L{f(x)} {f(y)}L{f(cx-nx)} {f(cy-ny)}Z" fill="{s.hatch(ang, 3, 1)}" stroke="{W_}" stroke-width="2.4"/>')

    hand(240, R * .52, 18)
    hand(0, R * .78, 12)
    s.add(f'<circle cx="{cx}" cy="{cy}" r="22" fill="{W_}"/>')
    s.stipple(1300, (0, 0, 1488, 1304), 1.3, .4, lambda x, y: math.hypot(x - cx, y - cy) > R + 10)
    s.scanlines(6, .08)
    s.save('gravura-ceas.svg')


# 5. Subagenți: un nod care se desface în trei, apoi în nouă, apoi în douăzeci și șapte
def delegate():
    s = Svg(1600, 1600, 5)
    cx, cy = 800, 800
    s.rays(cx, cy, 120, 800, 260, 1, .6, .4)
    levels = [(0, 1), (260, 3), (480, 9), (680, 27)]
    prev = [(cx, cy, -90)]
    for li in range(1, len(levels)):
        r, n = levels[li]
        cur = []
        for i in range(n):
            a = -90 + 360 * (i + .5) / n
            x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
            px, py, _ = prev[i // 3]
            bundle(s, px, py, x, y, 5 if li < 3 else 3, 14 - li * 3, .8)
            cur.append((x, y, a))
        prev = cur
    for li, (r, n) in enumerate(levels):
        for i in range(n):
            a = -90 + 360 * (i + .5) / n
            x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
            if li == 0:
                sphere(s, cx, cy, 120)
            else:
                node(s, x, y, [0, 54, 32, 16][li], li < 3)
    for r in (260, 480, 680):
        s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{W_}" stroke-width="1" stroke-dasharray="2 9" opacity=".6"/>')
    s.stipple(1500, (0, 0, 1600, 1600), 1.3, .35)
    s.scanlines(6, .08)
    s.save('gravura-subagenti.svg')


# 6. Oriunde rulează: un container izometric pe o rețea, cu un al doilea în el
def sandbox():
    s = Svg(1416, 1800, 6)
    cx, cy = 708, 980

    def iso(x, y, z):
        return cx + (x - y) * math.cos(math.radians(30)), cy + (x + y) * math.sin(math.radians(30)) - z

    g = []
    for k in range(-8, 9):
        a, b = iso(k * 80, -640, 0), iso(k * 80, 640, 0)
        c, d = iso(-640, k * 80, 0), iso(640, k * 80, 0)
        g.append(f'M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}M{f(c[0])} {f(c[1])}L{f(d[0])} {f(d[1])}')
    s.add(f'<path d="{"".join(g)}" stroke="{W_}" stroke-width="1" opacity=".45"/>')

    def box(sz, h, z0, tones):
        P = lambda x, y, z: iso(x, y, z0 + z)
        faces = [
            ([P(-sz, sz, 0), P(sz, sz, 0), P(sz, sz, h), P(-sz, sz, h)], tones[0], -60),
            ([P(sz, -sz, 0), P(sz, sz, 0), P(sz, sz, h), P(sz, -sz, h)], tones[1], 60),
            ([P(-sz, -sz, h), P(sz, -sz, h), P(sz, sz, h), P(-sz, sz, h)], tones[2], 0),
        ]
        for pts, gap, ang in faces:
            d = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z'
            s.add(f'<path d="{d}" fill="{INK}"/>')
            if gap:
                s.add(f'<path d="{d}" fill="{s.hatch(ang, gap, 1.1)}"/>')
            s.add(f'<path d="{d}" fill="none" stroke="{W_}" stroke-width="3" stroke-linejoin="round"/>')

    tx, ty = iso(0, 0, 560)
    s.rays(tx, ty - 60, 60, 900, 160, 1, .55, .45)
    box(330, 520, 0, (3.4, 6.5, 0))
    # nervurile containerului pe fața din stânga
    for k in range(1, 9):
        x = -330 + k * 660 / 9
        a, b = iso(x, 330, 20), iso(x, 330, 500)
        s.add(f'<path d="M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}" stroke="{W_}" stroke-width="2.6"/>')
    box(150, 180, 520, (4, 8, 12))
    s.stipple(1500, (0, 0, 1416, 1800), 1.3, .35, lambda x, y: y < 380 or y > 1450)
    s.scanlines(6, .08)
    s.save('gravura-container.svg')


if __name__ == '__main__':
    cover(); memory(); connect(); automation(); delegate(); sandbox()
