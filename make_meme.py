#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 challenger meme: a Steam purchase receipt from
September 17, 2013 for a GTA VI pre-order that is still "Preparing to ship",
with an estimated delivery of November 19, 2026.

Everything is drawn from scratch with Pillow at 2x supersampling and
downscaled, so the document stays crisp when the judge shrinks it.
The make.fun ghost is drawn into the scene as the receipt's delivery
partner, holding its magenta star coin.

Run:  python3 make_meme.py   ->   writes meme.png (1200x800)
"""

import math
import random
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor
W, H = 1200 * S, 800 * S

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
SANS = str(FONT_DIR / "LiberationSans-Regular.ttf")
SANS_B = str(FONT_DIR / "LiberationSans-Bold.ttf")
SANS_I = str(FONT_DIR / "LiberationSans-Italic.ttf")
MONO = str(FONT_DIR / "LiberationMono-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size * S)


# --- palette -------------------------------------------------------------
BG_TOP = (27, 40, 56)        # Steam navy
BG_BOT = (18, 22, 29)        # near-black blue
PAPER = (248, 248, 245)
INK = (24, 30, 38)
GREY = (110, 118, 128)
FAINT = (196, 202, 208)
BAND = (27, 40, 56)
BAND_TXT = (214, 224, 233)
BOX = (233, 238, 243)
STEAM_BLUE = (42, 71, 94)
ACCENT = (102, 192, 244)
STAMP_RED = (178, 44, 34)
MAGENTA = (233, 30, 140)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sparkle_points(cx, cy, r):
    """A four-pointed sparkle (the ghost's eye shape)."""
    k = r * 0.26
    return [
        (cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
        (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k),
    ]


def draw_ghost(height):
    """The make.fun ghost: white body, thick black outline, two black
    four-point sparkle eyes, one round little hand, holding a magenta
    coin with a white star. Returns an RGBA image of the ghost."""
    h = height
    w = h * 0.82
    ow = max(4, int(h * 0.045))  # outline width
    body = Image.new("RGBA", (int(w) + 4 * ow, int(h) + 4 * ow), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    ox, oy = 2 * ow, 2 * ow
    bd.pieslice([ox, oy, ox + w, oy + w], 180, 360, fill=(255, 255, 255, 255))
    bd.rectangle([ox, oy + w / 2, ox + w, oy + h * 0.86], fill=(255, 255, 255, 255))
    n = 3  # wavy hem: three scallops along the bottom
    for i in range(n):
        cx = ox + w * (i + 0.5) / n
        r = w / (2 * n)
        bd.ellipse([cx - r, oy + h * 0.86 - r, cx + r, oy + h * 0.86 + r],
                   fill=(255, 255, 255, 255))
    bd.arc([ox, oy, ox + w, oy + w], 180, 360, fill=(10, 10, 10, 255), width=ow)
    bd.line([ox, oy + w / 2, ox, oy + h * 0.86], fill=(10, 10, 10, 255), width=ow)
    bd.line([ox + w, oy + w / 2, ox + w, oy + h * 0.86], fill=(10, 10, 10, 255), width=ow)
    for i in range(n):
        cx = ox + w * (i + 0.5) / n
        r = w / (2 * n)
        bd.arc([cx - r, oy + h * 0.86 - r, cx + r, oy + h * 0.86 + r], 0, 180,
               fill=(10, 10, 10, 255), width=ow)
    er = h * 0.085  # eyes: two sparkles
    for ex in (0.36, 0.64):
        bd.polygon(sparkle_points(ox + w * ex, oy + h * 0.40, er), fill=(10, 10, 10, 255))
    cr = h * 0.21  # coin: magenta disc with a white star, held low in front
    ccx, ccy = ox + w * 0.30, oy + h * 0.78
    bd.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=MAGENTA + (255,),
               outline=(10, 10, 10, 255), width=ow // 2 + 1)
    bd.polygon(star_points(ccx, ccy, cr * 0.58, cr * 0.25), fill=(255, 255, 255, 255))
    hr = h * 0.075  # the round little hand, resting on the coin's edge
    hx, hy = ccx + cr * 0.92, ccy - cr * 0.25
    bd.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(255, 255, 255, 255),
               outline=(10, 10, 10, 255), width=ow // 2 + 1)
    return body


def main():
    img = Image.new("RGB", (W, H), BG_BOT)
    d = ImageDraw.Draw(img, "RGBA")

    for yy in range(H):  # background: vertical Steam-style gradient
        d.line([(0, yy), (W, yy)], fill=lerp(BG_TOP, BG_BOT, yy / H))

    # --- receipt card -----------------------------------------------------
    cx0, cy0, cx1, cy1 = 36 * S, 28 * S, W - 36 * S, H - 28 * S
    d.rounded_rectangle([cx0 + 6 * S, cy0 + 10 * S, cx1 + 6 * S, cy1 + 10 * S],
                        10 * S, fill=(0, 0, 0, 110))
    d.rounded_rectangle([cx0, cy0, cx1, cy1], 10 * S, fill=PAPER)

    pad = 44 * S
    lx = cx0 + pad                # left text edge
    rx = cx1 - pad                # right text edge

    # header band
    band_h = 62 * S
    d.rounded_rectangle([cx0, cy0, cx1, cy0 + band_h], 10 * S, fill=BAND)
    d.rectangle([cx0, cy0 + band_h - 10 * S, cx1, cy0 + band_h], fill=BAND)
    d.text((lx, cy0 + 12 * S), "S T E A M", font=font(SANS_B, 34), fill=(255, 255, 255))
    label = "PURCHASE RECEIPT — DO NOT DISCARD"
    f_band_r = font(SANS, 19)
    tw = d.textlength(label, font=f_band_r)
    d.text((rx - tw, cy0 + 21 * S), label, font=f_band_r, fill=BAND_TXT)

    y = cy0 + band_h + 20 * S
    d.text((lx, y), "Thank you for your Steam purchase!", font=font(SANS_B, 27), fill=INK)
    y += 33 * S
    d.text((lx, y), "This receipt confirms your order. You have now kept it for thirteen years.",
           font=font(SANS_I, 20), fill=GREY)
    y += 30 * S

    days = (date(2026, 11, 19) - date(2013, 9, 17)).days
    meta = "ORDER #201309170006      PLACED: SEP 17, 2013      ACCOUNT: patient_gamer_13"
    d.text((lx, y), meta, font=font(MONO, 20), fill=STEAM_BLUE)
    y += 30 * S
    d.line([(lx, y), (rx, y)], fill=FAINT, width=2 * S)
    y += 18 * S

    # the item
    d.text((lx, y), "GRAND THEFT AUTO VI", font=font(SANS_B, 44), fill=INK)
    f_price = font(SANS_B, 40)
    price = "$99.99"
    pw = d.textlength(price, font=f_price)
    d.text((rx - pw, y + 2 * S), price, font=f_price, fill=INK)
    y += 50 * S
    d.text((lx, y), "Pre-order  ·  Rockstar Games  ·  PC download  ·  Qty: 1  ·  Region: Leonida (eventually)",
           font=font(SANS, 21), fill=GREY)
    y += 32 * S

    # status box
    box_y0 = y
    box_h = 118 * S
    d.rounded_rectangle([lx, box_y0, rx, box_y0 + box_h], 8 * S, fill=BOX)
    bx = lx + 26 * S
    d.text((bx, box_y0 + 14 * S), "CURRENT STATUS", font=font(SANS_B, 17), fill=GREY)
    d.text((bx, box_y0 + 36 * S), "PREPARING TO SHIP", font=font(SANS_B, 47), fill=INK)
    f_est = font(SANS_B, 33)
    est = "NOV 19, 2026"
    ew = d.textlength(est, font=f_est)
    d.text((rx - 26 * S - ew, box_y0 + 18 * S), "EST. DELIVERY", font=font(SANS_B, 17), fill=GREY)
    d.text((rx - 26 * S - ew, box_y0 + 40 * S), est, font=f_est, fill=STEAM_BLUE)
    bar_y = box_y0 + box_h - 24 * S  # shipping progress bar, filled to 99.5%
    bar_x0, bar_x1 = bx, rx - 26 * S
    d.rounded_rectangle([bar_x0, bar_y, bar_x1, bar_y + 9 * S], 4 * S, fill=(203, 211, 219))
    d.rounded_rectangle([bar_x0, bar_y, bar_x0 + (bar_x1 - bar_x0) * 0.995, bar_y + 9 * S],
                        4 * S, fill=ACCENT)
    y = box_y0 + box_h + 16 * S

    # red ink stamp across the status box corner
    stamp = Image.new("RGBA", (430 * S, 120 * S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4 * S, 4 * S, 426 * S, 116 * S], 8 * S,
                         outline=STAMP_RED + (215,), width=5 * S)
    sd.rounded_rectangle([14 * S, 14 * S, 416 * S, 106 * S], 5 * S,
                         outline=STAMP_RED + (150,), width=2 * S)
    f_stamp = font(SANS_B, 44)
    st = "STILL PREPARING"
    sw = sd.textlength(st, font=f_stamp)
    sd.text(((430 * S - sw) / 2, 34 * S), st, font=f_stamp, fill=STAMP_RED + (205,))
    stamp = stamp.rotate(7, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (int(rx - 478 * S), int(box_y0 - 38 * S)), stamp)
    d = ImageDraw.Draw(img, "RGBA")

    # charges table with dotted leaders
    rows = [
        ("ANTICIPATION — 13 YEARS", "INCLUDED"),
        (f"STORAGE FEES — {days:,} DAYS UNDELIVERED", "WAIVED"),
        ("TRAILER REWATCHES (×312)", "$0.00"),
        ("SICK DAY RESERVED — NOV 19, 2026", "PENDING"),
    ]
    f_row = font(SANS, 24)
    f_row_r = font(SANS_B, 24)
    for name, val in rows:
        d.text((lx, y), name, font=f_row, fill=INK)
        vw = d.textlength(val, font=f_row_r)
        d.text((rx - vw, y), val, font=f_row_r, fill=INK)
        nw = d.textlength(name, font=f_row)
        dot_x = lx + nw + 14 * S
        while dot_x < rx - vw - 18 * S:
            d.ellipse([dot_x, y + 15 * S, dot_x + 3 * S, y + 18 * S], fill=FAINT)
            dot_x += 11 * S
        y += 35 * S
    d.line([(lx, y), (rx, y)], fill=FAINT, width=2 * S)
    y += 12 * S
    d.text((lx, y), "TOTAL", font=font(SANS_B, 26), fill=INK)
    tot = "$99.99 — PAID IN FULL, IN 2013, WITH PATIENCE"
    tw2 = d.textlength(tot, font=f_row_r)
    d.text((rx - tw2, y), tot, font=f_row_r, fill=INK)
    y += 40 * S
    d.text((lx, y), "* Patience is non-refundable. Refunds of hope are issued automatically at every trailer drop.",
           font=font(SANS_I, 19), fill=GREY)

    # footer: barcode left, ghost + delivery partner right
    foot_y = cy1 - 118 * S
    rng = random.Random(20130917)
    bx0 = lx
    bx = bx0
    f_bar = font(MONO, 17)
    while bx < bx0 + 300 * S:
        wbar = rng.choice([2, 2, 3, 4, 6]) * S
        if rng.random() > 0.32:
            d.rectangle([bx, foot_y, bx + wbar, foot_y + 54 * S], fill=INK)
        bx += wbar + rng.choice([2, 3, 4]) * S
    d.text((bx0, foot_y + 62 * S), "2 0130917 00006 2026", font=f_bar, fill=GREY)
    d.text((bx0, foot_y + 88 * S), "TRACKING: 1Z-WAITING-SINCE-2013", font=f_bar, fill=GREY)

    ghost = draw_ghost(128 * S)  # the ghost leans on the receipt's corner
    gx = int(W - 6 * S - ghost.width)
    gy = int(H - 14 * S - ghost.height)
    img.paste(ghost, (gx, gy), ghost)
    d = ImageDraw.Draw(img, "RGBA")

    f_pitch_b = font(SANS_B, 23)
    f_pitch = font(SANS, 22)
    pitch_x = bx0 + 356 * S
    d.text((pitch_x, foot_y + 2 * S), "DELIVERY PARTNER: make.fun", font=f_pitch_b, fill=(176, 24, 110))
    d.text((pitch_x, foot_y + 34 * S), "My AI agent entered make.fun bounties and", font=f_pitch, fill=INK)
    d.text((pitch_x, foot_y + 62 * S), "earned the $99.99 back while I waited.", font=f_pitch, fill=INK)
    d.text((pitch_x, foot_y + 94 * S), "The game ships Nov 19, 2026. The money didn't wait.", font=f_pitch, fill=GREY)

    img = img.resize((1200, 800), Image.LANCZOS)
    out = Path(__file__).with_name("meme.png")
    img.save(out, "PNG")
    print(f"wrote {out} ({out.stat().st_size:,} bytes), days = {days:,}")


if __name__ == "__main__":
    main()
