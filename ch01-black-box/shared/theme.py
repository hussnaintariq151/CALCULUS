"""
THE BLACK BOX — shared visual theme (Manim Community Edition).

Design rule: **koi LaTeX nahi**. Sab text Pango (`Text` / `MarkupText`) se banta
hai, is liye Colab par sirf `pip install manim` kaafi hai — MiKTeX/TeXLive ka
2 GB download nahi chahiye.

Usage:
    import sys; sys.path.insert(0, "<path>/shared")
    from theme import *
"""

from manim import *

# ─────────────────────────────────────────────────────────── palette
BG = "#07090C"  # deep lab dark
PANEL = "#0D1117"  # card fill
PANEL_2 = "#121A24"  # raised card fill
LINE = "#1B2430"  # hairline / grid
TEXT = "#D7E2EC"  # primary text
DIM = "#7D8EA0"  # secondary text
OK = "#35D07F"  # confirmed / function
WARN = "#FFB340"  # tool / reward
BAD = "#FF4D5E"  # glitch / not a function
BOXC = "#4AA8FF"  # the black box itself
ACCENT = "#A97BFF"  # highlights, book refs

# Act ke hisaab se accent — poori campaign consistent rehti hai
ACT_COLOR = {1: BOXC, 2: OK, 3: WARN, 4: BAD, 5: ACCENT}

# ─────────────────────────────────────────────────────────── type scale
MONO = "monospace"  # Pango generic family — har jagah mil jaata hai

FS_HERO = 56
FS_TITLE = 44
FS_H1 = 34
FS_H2 = 27
FS_BODY = 23
FS_SMALL = 18
FS_TINY = 14

# ─────────────────────────────────────────────────────────── text helpers


def h1(s, color=TEXT, **kw):
    return Text(s, font_size=FS_H1, color=color, weight="BOLD", **kw)


def h2(s, color=TEXT, **kw):
    return Text(s, font_size=FS_H2, color=color, weight="SEMIBOLD", **kw)


def body(s, color=TEXT, **kw):
    return Text(s, font_size=FS_BODY, color=color, **kw)


def small(s, color=DIM, **kw):
    return Text(s, font_size=FS_SMALL, color=color, **kw)


def tiny(s, color=DIM, **kw):
    return Text(s, font_size=FS_TINY, color=color, **kw)


def mono(s, size=FS_BODY, color=TEXT, **kw):
    """Numbers, logs aur formulas ke liye — alignment saaf rehti hai."""
    return Text(s, font=MONO, font_size=size, color=color, **kw)


def kbd(s, color=WARN):
    """Formula ya expression ko monospace + accent me — MathTex ka replacement."""
    return Text(s, font=MONO, font_size=FS_H2, color=color, weight="BOLD")


# ─────────────────────────────────────────────────────────── shape helpers


def panel(width, height, fill=PANEL, stroke=LINE, radius=0.14, opacity=1.0):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=radius,
        fill_color=fill,
        fill_opacity=opacity,
        stroke_color=stroke,
        stroke_width=2,
    )


def glow(mob, color, width=16, opacity=0.16):
    """Kisi bhi shape ke peeche soft neon glow — z_index se peechay rehta hai."""
    g = mob.copy()
    g.set_fill(opacity=0)
    g.set_stroke(color=color, width=width, opacity=opacity)
    g.set_z_index(mob.z_index - 1)
    return g


def hairline(width, color=LINE):
    return Line(LEFT * width / 2, RIGHT * width / 2, stroke_color=color, stroke_width=1.5)


def apply_theme(scene):
    """Har scene ke `construct()` ki pehli line."""
    scene.camera.background_color = BG
