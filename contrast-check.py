"""Text contrast + colour-blind check.

Usage:
  python contrast-check.py FG BG                      opaque background
  python contrast-check.py FG BG --alpha A --over X   translucent BG (alpha A) on backdrop X
  python contrast-check.py --file pairs.txt           one "label | FG | BG [| alpha | over]" per line

A translucent panel must be checked over the LIGHTEST thing that can sit behind it
(for a 3D or image page, assume #ffffff). That is where low contrast hides.

Prints the WCAG 2 ratio for normal vision and under simulated protanopia,
deuteranopia and tritanopia (Machado et al. 2009, severity 1.0).
WCAG AA: 4.5 for body text, 3.0 for large text (24px+, or 19px+ bold).
"""
import sys

CVD = {
    'protan': ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    'deutan': ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    'tritan': ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def unlin(c):
    c = min(1.0, max(0.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def sim(c, kind):
    if kind == 'normal':
        return c
    l = [lin(v) for v in c]
    return tuple(unlin(sum(m * v for m, v in zip(row, l))) for row in CVD[kind])


def lum(c):
    r, g, b = (lin(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def blend(fg, alpha, over):
    return tuple(alpha * f + (1 - alpha) * o for f, o in zip(fg, over))


def check(label, fg, bg, alpha=1.0, over='#ffffff', need=4.5):
    b = blend(rgb(bg), alpha, rgb(over)) if alpha < 1 else rgb(bg)
    f = rgb(fg)
    res = {k: ratio(sim(f, k), sim(b, k)) for k in ('normal', 'protan', 'deutan', 'tritan')}
    worst = min(res.values())
    flag = 'PASS' if worst >= need else ('LARGE ONLY' if worst >= 3 else 'FAIL')
    cells = '  '.join(f'{k} {v:5.2f}' for k, v in res.items())
    print(f'{flag:10} {label:44} {cells}')
    return worst >= need


def main(argv):
    if argv[:1] == ['--file']:
        ok = True
        for line in open(argv[1], encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            p = [x.strip() for x in line.split('|')]
            ok &= check(p[0], p[1], p[2], float(p[3]) if len(p) > 3 else 1.0, p[4] if len(p) > 4 else '#ffffff')
        return 0 if ok else 1
    fg, bg = argv[0], argv[1]
    alpha = float(argv[argv.index('--alpha') + 1]) if '--alpha' in argv else 1.0
    over = argv[argv.index('--over') + 1] if '--over' in argv else '#ffffff'
    return 0 if check(f'{fg} on {bg}', fg, bg, alpha, over) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
