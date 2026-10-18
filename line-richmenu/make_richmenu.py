from PIL import Image, ImageDraw, ImageFont
import sys

OUT = sys.argv[1]
W, H = 2500, 1686
S = 2  # supersample
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf"

BG = (253, 248, 246)
BG2 = (251, 238, 233)
PLUM = (61, 42, 44)
GOLD = (193, 122, 99)
CHAR = (58, 43, 39)
MID = (107, 81, 72)
BORDER = (236, 217, 210)
WHITE = (255, 255, 255)

img = Image.new("RGB", (W * S, H * S), BG)
d = ImageDraw.Draw(img)

def f(size):
    return ImageFont.truetype(FONT, size * S)

cols = [0, 833, 1666, 2500]
rows = [0, 843, 1686]

tiles = [
    ("calendar", "WEB予約", "24時間受付", True),
    ("yen", "料金・メニュー", "初診 ¥12,000〜", False),
    ("pin", "アクセス", "月島駅 徒歩2分", False),
    ("leaf", "初めての方へ", "施術の流れ・HP", False),
    ("phone", "電話する", "090-5999-6407", False),
    ("chat", "ご相談", "お悩みをどうぞ", False),
]

def icon(kind, cx, cy, color, bg):
    r = 95 * S
    lw = 12 * S
    if kind == "calendar":
        x0, y0, x1, y1 = cx - r, cy - r + 15 * S, cx + r, cy + r
        d.rounded_rectangle([x0, y0, x1, y1], radius=18 * S, outline=color, width=lw)
        d.line([x0, y0 + 55 * S, x1, y0 + 55 * S], fill=color, width=lw)
        for dx in (-50, 50):
            d.line([cx + dx * S, y0 - 30 * S, cx + dx * S, y0 + 22 * S], fill=color, width=lw)
        for i in range(3):
            for j in range(2):
                px = cx - 55 * S + i * 55 * S
                py = y0 + 100 * S + j * 50 * S
                d.ellipse([px - 11 * S, py - 11 * S, px + 11 * S, py + 11 * S], fill=color)
    elif kind == "yen":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=lw)
        fy = f(120)
        d.text((cx, cy + 4 * S), "¥", font=fy, fill=color, anchor="mm")
    elif kind == "pin":
        rr = 72 * S
        top = cy - r + 10 * S
        d.ellipse([cx - rr, top, cx + rr, top + 2 * rr], outline=color, width=lw)
        d.polygon([(cx - rr * 0.8, top + rr * 1.55), (cx + rr * 0.8, top + rr * 1.55), (cx, cy + r + 5 * S)], fill=color)
        d.ellipse([cx - rr, top, cx + rr, top + 2 * rr], fill=color)
        d.ellipse([cx - 28 * S, top + rr - 28 * S, cx + 28 * S, top + rr + 28 * S], fill=bg)
    elif kind == "leaf":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=lw)
        fy = f(110)
        d.text((cx, cy + 4 * S), "i", font=fy, fill=color, anchor="mm")
    elif kind == "phone":
        x0, y0, x1, y1 = cx - 60 * S, cy - r, cx + 60 * S, cy + r
        d.rounded_rectangle([x0, y0, x1, y1], radius=22 * S, outline=color, width=lw)
        d.line([cx - 20 * S, y0 + 28 * S, cx + 20 * S, y0 + 28 * S], fill=color, width=lw // 2 + S)
        d.ellipse([cx - 12 * S, y1 - 42 * S, cx + 12 * S, y1 - 18 * S], fill=color)
    elif kind == "chat":
        x0, y0, x1, y1 = cx - r - 10 * S, cy - r + 10 * S, cx + r + 10 * S, cy + r - 40 * S
        d.rounded_rectangle([x0, y0, x1, y1], radius=40 * S, outline=color, width=lw)
        d.polygon([(cx - 50 * S, y1 - 2 * S), (cx - 5 * S, y1 - 2 * S), (cx - 60 * S, y1 + 55 * S)], fill=color)
        for dx in (-50, 0, 50):
            px, py = cx + dx * S, (y0 + y1) // 2
            d.ellipse([px - 13 * S, py - 13 * S, px + 13 * S, py + 13 * S], fill=color)

for idx, (kind, title, sub, hl) in enumerate(tiles):
    c, r_ = idx % 3, idx // 3
    x0, x1 = cols[c] * S, cols[c + 1] * S
    y0, y1 = rows[r_] * S, rows[r_ + 1] * S
    bg = GOLD if hl else (BG if (c + r_) % 2 == 0 else BG2)
    fg = WHITE if hl else PLUM
    subc = (255, 240, 233) if hl else MID
    d.rectangle([x0, y0, x1, y1], fill=bg)
    cx = (x0 + x1) // 2
    icon(kind, cx, y0 + 300 * S, GOLD if not hl else WHITE, bg)
    d.text((cx, y0 + 545 * S), title, font=f(92), fill=fg, anchor="mm")
    d.line([cx - 40 * S, y0 + 625 * S, cx + 40 * S, y0 + 625 * S], fill=(subc if hl else GOLD), width=4 * S)
    d.text((cx, y0 + 690 * S), sub, font=f(58), fill=subc, anchor="mm")

# grid lines
for x in cols[1:-1]:
    d.line([x * S, 0, x * S, H * S], fill=BORDER, width=6 * S)
d.line([0, rows[1] * S, W * S, rows[1] * S], fill=BORDER, width=6 * S)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
