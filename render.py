#!/usr/bin/env python3
"""Render the 22 November 2026 world-news infographic (1024x1024 PNG).

Pure Pillow, no network. Reads nothing at runtime except the DejaVu fonts.
All news text is baked into this script, drawn from reporting dated
22 November 2026 (AFP, AP, France 24, The Japan Times, Arab News).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 246, 238)          # warm paper
INK = (20, 33, 61)            # dark navy
MUTED = (90, 98, 115)
CARD = (255, 255, 255)
LINE = (214, 206, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
f_title = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 21)
f_body = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 17)
f_tag = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 14)
f_head = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 58)
f_sub = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 22)
f_kicker = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 16)
f_foot = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 14)

# (tag, accent colour, title, summary, source)
STORIES = [
    ("GULF WAR", (178, 34, 34),
     "Iran strikes Bahrain; tankers hit in Hormuz",
     "Iran hits a Bahrain industrial site and claims strikes on two US bases. "
     "Two tankers are struck in the Strait of Hormuz.",
     "AFP"),
    ("CLIMATE", (15, 118, 110),
     "COP31 final draft drops fossil fuels",
     "The draft deal, released early on Sunday, never mentions fossil fuels. "
     "Nearly 200 nations must approve it at a closing session today.",
     "AP"),
    ("MEXICO", (146, 64, 14),
     "Mexico captures 'El Chapo Isidro'",
     "FBI most-wanted cartel boss Fausto Isidro Meza Flores is seized in "
     "Sinaloa. Eleven people are killed in the raid.",
     "AP"),
    ("BALTIC SEA", (29, 78, 137),
     "Cargo ship ablaze after drone strike",
     "Russian-linked vessel Sparta II catches fire in the Gulf of Finland and "
     "drifts into Finnish waters. Sixteen crew are evacuated.",
     "France 24"),
    ("FRANCE", (107, 33, 141),
     "Protests enter a sixth weekend",
     "Crowds rally across France again over living costs and public services, "
     "keeping pressure on the government.",
     "AFP"),
    ("UNITED STATES", (120, 20, 60),
     "US agencies breached by hackers",
     "The Agriculture Department and the FBI were breached by hackers, "
     "according to reports.",
     "The Japan Times"),
    ("SPACE", (13, 92, 99),
     "Mercury gets its first visitor in years",
     "Two spacecraft loop into orbit around Mercury, the Solar System's "
     "smallest planet.",
     "Arab News"),
    ("INDONESIA", (120, 85, 10),
     "39 missing after factory fire",
     "Rescuers search for 39 people missing after a fire at a factory "
     "in Indonesia.",
     "AFP"),
]


def wrap(draw, text, font, max_w):
    """Greedy word wrap measured in pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header band ----
    d.rectangle([0, 0, W, 128], fill=INK)
    d.text((32, 18), "THE WORLD IN ONE DAY", font=f_kicker, fill=(232, 196, 106))
    d.text((32, 40), "22 November 2026", font=f_head, fill=(255, 255, 255))
    d.text((32, 100), "Sunday's world news in one image",
           font=f_sub, fill=(205, 212, 226))
    # small globe mark, top right
    cx, cy, r = 948, 64, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(232, 196, 106), width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=None)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(232, 196, 106), width=3)
    d.line([cx - r, cy, cx + r, cy], fill=(232, 196, 106), width=2)
    d.line([cx, cy - r, cx, cy + r], fill=(232, 196, 106), width=2)

    # ---- story grid: 2 cols x 4 rows ----
    margin, gap = 24, 16
    top = 148
    col_w = (W - 2 * margin - gap) // 2
    row_h = (H - top - 44 - 3 * gap) // 4  # 44px footer strip
    for i, (tag, accent, title, summary, src) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x0 = margin + col * (col_w + gap)
        y0 = top + row * (row_h + gap)
        x1, y1 = x0 + col_w, y0 + row_h
        # card
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                            outline=LINE, width=1)
        d.rectangle([x0, y0 + 10, x0 + 6, y1 - 10], fill=accent)
        tx = x0 + 20
        # tag chip
        tw = d.textlength(tag, font=f_tag) + 16
        d.rounded_rectangle([tx, y0 + 14, tx + tw, y0 + 38], radius=6,
                            fill=accent)
        d.text((tx + 8, y0 + 18), tag, font=f_tag, fill=(255, 255, 255))
        # title (up to 2 lines)
        ty = y0 + 48
        max_w = col_w - 40
        tlines = wrap(d, title, f_title, max_w)[:2]
        for ln in tlines:
            d.text((tx, ty), ln, font=f_title, fill=INK)
            ty += 26
        # summary (up to 3 lines)
        sy = ty + 4
        slines = wrap(d, summary, f_body, max_w)[:3]
        for ln in slines:
            d.text((tx, sy), ln, font=f_body, fill=(52, 60, 78))
            sy += 22
        # source line at card bottom
        d.text((tx, y1 - 26), "Source: " + src, font=f_foot, fill=MUTED)

    # ---- footer ----
    fy = H - 34
    d.text((margin, fy),
           "Sources: AFP  ·  AP  ·  France 24  ·  The Japan Times  ·  Arab News",
           font=f_foot, fill=MUTED)
    d.text((W - margin - d.textlength("22 November 2026", font=f_foot), fy),
           "22 November 2026", font=f_foot, fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
