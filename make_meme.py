#!/usr/bin/env python3
"""Draw the 'SAME $100. DIFFERENT DIRECTION.' GTA 6 / make.fun meme.

Canvas 1200x750, drawn entirely with Pillow primitives -- no external
artwork. Output: meme.png next to this script.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme.png")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1200, 750
HORIZON = int(H * 0.62)          # 465
BANNER_H = 90
BANNER_Y = H - BANNER_H          # 660

MAGENTA = (255, 46, 154)         # #ff2e9a
CYAN = (34, 211, 238)            # #22d3ee
PURPLE = (43, 10, 74)            # #2b0a4a
ORANGE = (255, 179, 92)          # #ffb35c
TEAL = (11, 37, 54)              # #0b2536
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (57, 255, 140)
HOT = (255, 45, 85)


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def centered(draw, cx, y, text, fnt, fill, stroke=0, stroke_fill=BLACK):
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    tw = box[2] - box[0]
    draw.text((cx - tw / 2 - box[0], y), text, font=fnt, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    return tw


def fit_font(draw, text, start_size, max_width):
    size = start_size
    while size > 10:
        fnt = font(size)
        box = draw.textbbox((0, 0), text, font=fnt)
        if box[2] - box[0] <= max_width:
            return fnt
        size -= 2
    return font(size)


def sparkle_points(cx, cy, w, h):
    pts = []
    for dx, dy in [(0, -0.5), (0.18, -0.18), (0.5, 0), (0.18, 0.18),
                   (0, 0.5), (-0.18, 0.18), (-0.5, 0), (-0.18, -0.18)]:
        pts.append((cx + dx * w, cy + dy * h))
    return pts


def star_points(cx, cy, r_outer, r_inner, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_sky(img):
    draw = ImageDraw.Draw(img)
    mid = (150, 30, 140)
    low = (255, 110, 130)
    for y in range(HORIZON):
        t = y / max(HORIZON - 1, 1)
        if t < 0.5:
            col = lerp(PURPLE, mid, t / 0.5)
        else:
            col = lerp(mid, low, (t - 0.5) / 0.5)
        if t > 0.85:
            col = lerp(col, ORANGE, (t - 0.85) / 0.15 * 0.7)
        draw.line([(0, y), (W, y)], fill=col)
    # ground / sea band
    draw.rectangle([0, HORIZON, W, BANNER_Y], fill=TEAL)
    draw.line([(0, HORIZON), (W, HORIZON)], fill=ORANGE, width=3)
    # sun disc, low in the sky (bottom stays above the ghost's hem)
    sun_cx, sun_cy, sun_r = 600, 362, 100
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
                 fill=(255, 222, 160))
    # sparkle stars in the sky
    for (sx, sy, s) in [(180, 70, 22), (340, 130, 14), (880, 80, 20),
                        (1020, 150, 14), (520, 60, 16), (700, 110, 12),
                        (60, 180, 14), (1140, 60, 16)]:
        draw.polygon(sparkle_points(sx, sy, s, s), fill=WHITE)
    return draw


def draw_palm(draw, base_x, crown_x, crown_y, flip=1):
    base_y = BANNER_Y
    # curved trunk as a thick segmented line, crown high in the sky so
    # the fronds stay visible above the panels
    pts = []
    for i in range(21):
        t = i / 20
        x = base_x + (crown_x - base_x) * t + flip * 14 * math.sin(t * 1.4)
        y = base_y + (crown_y - base_y) * t
        pts.append((x, y))
    draw.line(pts, fill=BLACK, width=17, joint="curve")
    # fronds: drooping segmented lines fanning out from the crown
    for dx, dy, length in [(-1.0, -0.30, 105), (-0.72, -0.72, 110),
                           (-0.25, -0.97, 100), (0.30, -0.95, 102),
                           (0.78, -0.62, 108), (1.0, -0.18, 100)]:
        fpts = []
        for i in range(13):
            t = i / 12
            x = crown_x + flip * dx * length * t
            y = crown_y + dy * length * t + 52 * t * t
            fpts.append((x, y))
        draw.line(fpts, fill=BLACK, width=9, joint="curve")
    # coconuts
    draw.ellipse([crown_x - 14, crown_y - 4, crown_x + 10, crown_y + 20], fill=BLACK)
    draw.ellipse([crown_x - 2, crown_y + 6, crown_x + 20, crown_y + 28], fill=BLACK)


def draw_left_panel(draw):
    x0, y0, x1, y1 = 55, 175, 425, 565
    cx = (x0 + x1) // 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=28,
                           fill=(18, 8, 46), outline=CYAN, width=7)
    centered(draw, cx, y0 + 28, "GTA VI", font(64), WHITE)
    centered(draw, cx, y0 + 108, "$100", font(118), HOT)
    centered(draw, cx, y0 + 248, "YOU PAY", font(44), WHITE)
    # downward red arrow, fully inside the panel
    ax, ay = cx, y0 + 308
    arrow = [(ax - 20, ay), (ax + 20, ay), (ax + 20, ay + 30),
             (ax + 48, ay + 30), (ax, ay + 62), (ax - 48, ay + 30),
             (ax - 20, ay + 30)]
    draw.polygon(arrow, fill=(255, 45, 60))


def draw_right_panel(draw):
    x0, y0, x1, y1 = 775, 175, 1145, 565
    cx = (x0 + x1) // 2
    # glow halo
    draw.rounded_rectangle([x0 - 12, y0 - 12, x1 + 12, y1 + 12], radius=36,
                           outline=(255, 120, 200), width=6)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=28, fill=MAGENTA)
    f_make = fit_font(draw, "make.fun", 68, x1 - x0 - 30)
    centered(draw, cx, y0 + 34, "make.fun", f_make, WHITE)
    centered(draw, cx, y0 + 128, "+$100", font(84), GREEN,
             stroke=2, stroke_fill=(0, 80, 30))
    f_earn = fit_font(draw, "YOUR AGENT EARNS", 40, x1 - x0 - 24)
    centered(draw, cx, y0 + 240, "YOUR AGENT EARNS", f_earn, WHITE)
    # upward green arrow, fully inside the panel
    ax, ay = cx, y0 + 302
    arrow = [(ax - 20, ay + 66), (ax + 20, ay + 66), (ax + 20, ay + 32),
             (ax + 48, ay + 32), (ax, ay), (ax - 48, ay + 32),
             (ax - 20, ay + 32)]
    draw.polygon(arrow, fill=GREEN)



def ghost_body(draw, cx, top, w, h, exp, fill):
    """One ghost silhouette: dome + straight sides + scalloped bottom."""
    x0, x1 = cx - w / 2 - exp, cx + w / 2 + exp
    y_top = top - exp
    bottom = top + h + exp
    wave = 26
    # dome
    draw.pieslice([x0, y_top, x1, y_top + (x1 - x0)], start=180, end=360,
                  fill=fill)
    # straight sides down to just above the scallops
    mid_y = y_top + (x1 - x0) / 2
    draw.rectangle([x0, mid_y, x1, bottom - wave], fill=fill)
    # scalloped bottom: a row of half-discs
    n = 5
    seg = (x1 - x0) / n
    for i in range(n):
        sx0 = x0 + i * seg
        draw.pieslice([sx0, bottom - wave * 2, sx0 + seg, bottom],
                      start=0, end=180, fill=fill)
    draw.rectangle([x0, bottom - wave, x1, bottom - wave + 2], fill=fill)


def draw_ghost(draw):
    cx, top, w, h = 600, 195, 260, 305
    # thick black outline: a slightly larger black copy behind
    ghost_body(draw, cx, top, w, h, 11, BLACK)
    ghost_body(draw, cx, top, w, h, 0, WHITE)
    # sparkle eyes
    eye_y = top + 118
    for ex in (cx - 48, cx + 48):
        draw.polygon(sparkle_points(ex, eye_y, 40, 54), fill=BLACK)
    # friendly smile
    draw.arc([cx - 32, top + 138, cx + 32, top + 182], start=15, end=165,
             fill=BLACK, width=7)
    # hand: small white round hand at the right side, black outline,
    # kept low so the coin it holds sits in the empty space below the
    # "YOUR AGENT EARNS" line and left of the up arrow -- no text covered
    hand_cx, hand_cy, hand_r = cx + w // 2 + 6, top + 282, 22
    draw.ellipse([hand_cx - hand_r - 5, hand_cy - hand_r - 5,
                  hand_cx + hand_r + 5, hand_cy + hand_r + 5], fill=BLACK)
    draw.ellipse([hand_cx - hand_r, hand_cy - hand_r,
                  hand_cx + hand_r, hand_cy + hand_r], fill=WHITE)
    # magenta coin held by the hand, black outline, white star
    coin_cx, coin_cy, coin_r = hand_cx + 24, hand_cy + 13, 36
    draw.ellipse([coin_cx - coin_r, coin_cy - coin_r,
                  coin_cx + coin_r, coin_cy + coin_r],
                 fill=MAGENTA, outline=BLACK, width=6)
    draw.polygon(star_points(coin_cx, coin_cy, 20, 8), fill=WHITE)


def draw_banner(draw):
    draw.rectangle([0, BANNER_Y, W, H], fill=BLACK)
    text = "SAME $100. DIFFERENT DIRECTION."
    fnt = fit_font(draw, text, 54, W - 40)
    box = draw.textbbox((0, 0), text, font=fnt)
    tw, th = box[2] - box[0], box[3] - box[1]
    draw.text(((W - tw) / 2 - box[0], BANNER_Y + (BANNER_H - th) / 2 - box[1]),
              text, font=fnt, fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PURPLE)
    draw = draw_sky(img)
    draw_palm(draw, 14, 60, 148, flip=1)
    draw_palm(draw, 1186, 1140, 148, flip=-1)
    draw_left_panel(draw)
    draw_right_panel(draw)
    draw_ghost(draw)
    draw_banner(draw)
    img.save(OUT, "PNG")
    print(f"saved {OUT} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
