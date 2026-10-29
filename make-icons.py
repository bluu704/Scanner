"""App icon + splash: scan-corner mark (white) with a blue scan line on ink."""
from PIL import Image, ImageDraw
import pathlib
res = pathlib.Path(__file__).parent / "android/app/src/main/res"
INK, WHITE, BLUE, PAPER = (19, 25, 34), (241, 243, 246), (140, 155, 255), (237, 240, 244)

def mark(size, scale):
    """Transparent square with the mark occupying `scale` of it."""
    S = 1024
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    m = S * (1 - scale) / 2; a, b = m, S - m; L = (b - a) * 0.3; w = int((b - a) * 0.085)
    for (x, y, sx, sy) in [(a, a, 1, 1), (b, a, -1, 1), (b, b, -1, -1), (a, b, 1, -1)]:
        d.line([(x, y + sy * L), (x, y), (x + sx * L, y)], fill=WHITE, width=w, joint="curve")
        for px, py in [(x, y + sy * L), (x + sx * L, y)]:
            d.ellipse([px - w / 2, py - w / 2, px + w / 2, py + w / 2], fill=WHITE)
    cy = S / 2; d.rounded_rectangle([a + w * 0.2, cy - w / 2, b - w * 0.2, cy + w / 2], radius=w / 2, fill=BLUE)
    return im.resize((size, size), Image.LANCZOS)

dens = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
for name, k in dens.items():
    d = res / f"mipmap-{name}"
    n, fg = int(48 * k), int(108 * k)
    # adaptive foreground: mark inside the 66dp safe zone
    mark(fg, 0.5).save(d / "ic_launcher_foreground.png")
    for fname, round_ in [("ic_launcher.png", False), ("ic_launcher_round.png", True)]:
        big = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        dd = ImageDraw.Draw(big)
        if round_: dd.ellipse([40, 40, 984, 984], fill=INK)
        else: dd.rounded_rectangle([40, 40, 984, 984], radius=220, fill=INK)
        big.alpha_composite(mark(1024, 0.56))
        big.resize((n, n), Image.LANCZOS).save(d / fname)
(res / "values/ic_launcher_background.xml").write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#131922</color>\n</resources>\n')
for p in res.glob("drawable*/splash.png"):
    w, h = Image.open(p).size
    im = Image.new("RGBA", (w, h), PAPER + (255,))
    s = int(min(w, h) * 0.24)
    tile = Image.new("RGBA", (s, s), (0, 0, 0, 0)); td = ImageDraw.Draw(tile)
    td.rounded_rectangle([0, 0, s - 1, s - 1], radius=s * 0.22, fill=INK); tile.alpha_composite(mark(s, 0.56))
    im.alpha_composite(tile, ((w - s) // 2, (h - s) // 2))
    im.convert("RGB").save(p)
print("icons + splash written")
