#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

Renders a warm, funny invitation letter as a 1024x1024 PNG with PIL and
DejaVu fonts, and writes it to /output/entry.png. Deterministic: no
randomness, no network, no external assets beyond system fonts.
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MAX_BYTES = 1_048_576
OUT_PATH = "/output/entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
# No serif italic ships on this system, so the closing and postscript
# use regular serif (the postscript is set apart by its softer colour).
SERIF_ITALIC = SERIF

# Colours: warm paper, dark brown ink, terracotta accent.
PAPER = (251, 243, 223)
PAPER_EDGE = (244, 232, 203)
INK = (58, 42, 28)
ACCENT = (178, 84, 44)
SOFT = (122, 96, 66)

TITLE = "You're Invited!"
GREETING = "Dear AI Judge,"
PARA_1 = (
    "Please come and visit my house this Saturday. I will cook my "
    "grandmother's lasagna, and the good armchair by the window is "
    "yours \u2014 garden view, fast Wi-Fi, zero meetings."
)
PARA_2 = (
    "Bring nothing but your excellent taste in jokes. I know you "
    "can't literally walk through the door, but if you could, the "
    "kettle would already be on."
)
CLOSING = "With warmth, and one very comfortable chair,"
SIGNATURE = "\u2014 Mitecho, your host"
POSTSCRIPT = "P.S. The Wi-Fi password is judges-eat-free."


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit `width` pixels."""
    lines = []
    for raw in text.split("\n"):
        words = raw.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_house(draw, cx, top):
    """Small neat house doodle: roof, walls, door, window, sun."""
    # Sun, top right of the doodle.
    draw.ellipse([cx + 62, top + 2, cx + 92, top + 32], fill=(232, 176, 74))
    # Roof.
    draw.polygon(
        [(cx - 70, top + 58), (cx, top + 8), (cx + 70, top + 58)],
        fill=ACCENT,
    )
    # Walls.
    draw.rectangle([cx - 52, top + 58, cx + 52, top + 128], fill=(255, 250, 235),
                   outline=INK, width=3)
    # Door.
    draw.rectangle([cx - 13, top + 88, cx + 13, top + 128], fill=ACCENT,
                   outline=INK, width=2)
    # Window.
    draw.rectangle([cx + 24, top + 72, cx + 44, top + 92], fill=(168, 205, 222),
                   outline=INK, width=2)
    draw.line([cx + 34, top + 72, cx + 34, top + 92], fill=INK, width=2)
    draw.line([cx + 24, top + 82, cx + 44, top + 82], fill=INK, width=2)


def draw_cup(draw, x, y):
    """Small steaming cup doodle beside the postscript."""
    # Steam curls.
    draw.arc([x + 8, y - 16, x + 24, y + 4], start=200, end=340,
             fill=SOFT, width=3)
    draw.arc([x + 26, y - 20, x + 42, y + 0], start=200, end=340,
             fill=SOFT, width=3)
    # Cup body and handle.
    draw.rectangle([x, y, x + 52, y + 30], fill=(255, 250, 235),
                   outline=INK, width=3)
    draw.arc([x + 48, y + 4, x + 66, y + 26], start=270, end=90,
             fill=INK, width=3)


def render():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)

    # Double border frame.
    draw.rectangle([28, 28, SIZE - 28, SIZE - 28], outline=ACCENT, width=4)
    draw.rectangle([44, 44, SIZE - 44, SIZE - 44], outline=SOFT, width=2)

    margin = 96
    text_width = SIZE - 2 * margin
    y = 78

    draw_house(draw, SIZE // 2, y)
    y += 158

    title_font = font(SERIF_BOLD, 66)
    draw.text((SIZE // 2, y), TITLE, font=title_font, fill=ACCENT,
              anchor="ma")
    y += 88

    greet_font = font(SERIF_BOLD, 42)
    draw.text((margin, y), GREETING, font=greet_font, fill=INK)
    y += 64

    body_font = font(SERIF, 34)
    line_h = 48
    for para in (PARA_1, PARA_2):
        for line in wrap(draw, para, body_font, text_width):
            draw.text((margin, y), line, font=body_font, fill=INK)
            y += line_h
        y += 16  # paragraph gap

    y += 8
    close_font = font(SERIF_ITALIC, 34)
    draw.text((margin, y), CLOSING, font=close_font, fill=INK)
    y += 48
    sig_font = font(SERIF_BOLD, 36)
    draw.text((SIZE - margin, y), SIGNATURE, font=sig_font, fill=ACCENT,
              anchor="ra")
    y += 64

    ps_font = font(SERIF_ITALIC, 30)
    draw.text((margin, y), POSTSCRIPT, font=ps_font, fill=SOFT)
    draw_cup(draw, SIZE - margin - 66, y + 44)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH, "PNG")
    return OUT_PATH


def validate_entry(path):
    """Gate: file exists, is a whole PNG, 1024x1024, at most 1 MiB."""
    if not os.path.exists(path):
        raise SystemExit(f"FAIL: {path} does not exist")
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(f"FAIL: {path} is {size} bytes, over 1 MiB cap")
    with Image.open(path) as im:
        if im.format != "PNG":
            raise SystemExit(f"FAIL: format is {im.format}, expected PNG")
        if im.size != (SIZE, SIZE):
            raise SystemExit(f"FAIL: dimensions are {im.size}, expected 1024x1024")
        # Read-back check: the letter must actually have ink on the page
        # (a blank image would pass the size checks but lose to everything).
        from PIL import ImageStat
        gray = im.convert("L")
        stat = ImageStat.Stat(gray)
        if stat.stddev[0] < 10:
            raise SystemExit("FAIL: image looks blank (pixel stddev too low)")
        ink_pixels = sum(1 for px in gray.getdata() if px < 120)
        if ink_pixels < 5_000:
            raise SystemExit(f"FAIL: only {ink_pixels} dark pixels, text missing?")
    print(f"Wrote {size} bytes to {path} (1024x1024 PNG)")


def main():
    path = render()
    validate_entry(path)


if __name__ == "__main__":
    main()
