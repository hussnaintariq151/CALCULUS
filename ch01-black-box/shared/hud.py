"""
THE BLACK BOX — reusable game HUD components (Manim CE, LaTeX-free).

Yeh module poori 41-level campaign me dobara istemal hota hai. Har level ka
`scene.py` sirf story likhta hai; HUD, box, log table, glitch banner, arrow
diagram aur tool card yahan se aate hain.

    import sys; sys.path.insert(0, "<path>/shared")
    from theme import *
    from hud import *

Colab note: emoji use na karein — Colab image me emoji font nahi hota. Icons
ke liye `magnifier_icon()` jaisi vector helpers hain.
"""

import numpy as np
from manim import *

from theme import (
    ACCENT,
    ACT_COLOR,
    BAD,
    BG,
    BOXC,
    DIM,
    FS_BODY,
    FS_H1,
    FS_H2,
    FS_HERO,
    FS_SMALL,
    FS_TINY,
    LINE,
    MONO,
    OK,
    PANEL,
    PANEL_2,
    TEXT,
    WARN,
    body,
    glow,
    hairline,
    mono,
    panel,
    small,
)

HUD_WIDTH = 12.6
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}


# ══════════════════════════════════════════════════════════════ HUD BAR


class HudBar(VGroup):
    """Top status bar: campaign name · level · DECODE progress.

    DECODE ko animate karna:
        hud.bump(self, 2)                        # helper
        self.play(hud.decode.animate.set_value(2))   # manual
    """

    def __init__(self, level_id="L01", level_title="", act=1, decode=0.0, **kw):
        super().__init__(**kw)
        accent = ACT_COLOR.get(act, BOXC)
        self.accent = accent
        self.decode = ValueTracker(decode)

        brand = Text("THE BLACK BOX", font=MONO, font_size=FS_TINY, color=DIM)
        tag = Text(
            f"{level_id}  ·  {level_title}",
            font=MONO,
            font_size=FS_SMALL,
            color=accent,
            weight="BOLD",
        )
        left = VGroup(brand, tag).arrange(DOWN, buff=0.09, aligned_edge=LEFT)

        bar_w = 3.2
        track = RoundedRectangle(
            width=bar_w,
            height=0.17,
            corner_radius=0.085,
            stroke_width=0,
            fill_color=LINE,
            fill_opacity=1,
        )

        def _fill():
            frac = min(max(self.decode.get_value() / 100.0, 0.004), 1.0)
            bar = RoundedRectangle(
                width=bar_w * frac,
                height=0.17,
                corner_radius=0.085,
                stroke_width=0,
                fill_color=accent,
                fill_opacity=1,
            )
            return bar.move_to(track.get_left(), aligned_edge=LEFT)

        def _pct():
            return (
                Text(
                    f"DECODE {self.decode.get_value():4.0f}%",
                    font=MONO,
                    font_size=FS_TINY,
                    color=DIM,
                )
                .next_to(track, UP, buff=0.11)
                .align_to(track, RIGHT)
            )

        right = VGroup(track, always_redraw(_fill), always_redraw(_pct))

        # spine = invisible ruler jispe left/right ends align hote hain
        spine = Line(LEFT * HUD_WIDTH / 2, RIGHT * HUD_WIDTH / 2).set_opacity(0)
        left.move_to(spine.get_left(), aligned_edge=LEFT)
        right.move_to(spine.get_right(), aligned_edge=RIGHT)
        right.align_to(left, DOWN)
        rule = hairline(HUD_WIDTH).next_to(VGroup(left, right), DOWN, buff=0.2)

        self.add(spine, left, right, rule)
        self.to_edge(UP, buff=0.3)

    def bump(self, scene, to, run_time=1.2):
        scene.play(self.decode.animate.set_value(to), run_time=run_time, rate_func=smooth)


# ══════════════════════════════════════════════════════════════ LEVEL CARD


class LevelCard(VGroup):
    """Level ka opening card."""

    def __init__(self, act_no, act_title, level_no, title, brief="", **kw):
        super().__init__(**kw)
        accent = ACT_COLOR.get(act_no, BOXC)

        act = Text(
            f"ACT {ROMAN.get(act_no, '?')}   ·   {act_title}",
            font=MONO,
            font_size=FS_SMALL,
            color=accent,
            weight="BOLD",
        )
        num = Text(f"LEVEL {level_no:02d}", font=MONO, font_size=FS_TINY, color=DIM)
        name = Text(title, font_size=FS_HERO, color=TEXT, weight="BOLD")
        rule = hairline(min(name.width + 1.2, 10.0), color=accent).set_stroke(opacity=0.55)

        parts = [act, num, name, rule]
        if brief:
            parts.append(body(brief, color=DIM))
        self.add(*parts)
        self.arrange(DOWN, buff=0.32)

    def play_in(self, scene, hold=1.7):
        scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.3) for m in self], lag_ratio=0.18))
        scene.wait(hold)
        scene.play(FadeOut(self, shift=UP * 0.4))


# ══════════════════════════════════════════════════════════════ THE BOX


class BlackBox(VGroup):
    """Sealed machine: rounded body + neon aura + in/out ports."""

    def __init__(self, label="? ? ?", w=3.1, h=2.1, color=BOXC, **kw):
        super().__init__(**kw)
        self.color_ = color
        self.body = RoundedRectangle(
            width=w,
            height=h,
            corner_radius=0.18,
            fill_color=PANEL_2,
            fill_opacity=1,
            stroke_color=color,
            stroke_width=3,
        )
        self.aura = glow(self.body, color)
        self.tag = Text(label, font=MONO, font_size=FS_H2, color=color, weight="BOLD")
        self.tag.move_to(self.body)

        rivets = VGroup(
            *[
                Dot(radius=0.035, color=LINE).move_to(
                    self.body.get_corner(c)
                    + np.array([-0.17 * np.sign(c[0]), -0.17 * np.sign(c[1]), 0.0])
                )
                for c in (UL, UR, DL, DR)
            ]
        )
        self.in_port = Dot(radius=0.075, color=DIM).move_to(self.body.get_left())
        self.out_port = Dot(radius=0.075, color=DIM).move_to(self.body.get_right())

        self.add(self.aura, self.body, rivets, self.tag, self.in_port, self.out_port)

    def relabel(self, new_label, color=None):
        new = Text(
            new_label,
            font=MONO,
            font_size=FS_SMALL if len(new_label) > 14 else FS_H2,
            color=color or self.color_,
            weight="BOLD",
        ).move_to(self.body)
        anim = ReplacementTransform(self.tag, new)
        self.tag = new
        return anim

    def pulse(self, color=None, scale=1.06):
        c = color or self.color_
        return AnimationGroup(
            Indicate(self.body, color=c, scale_factor=scale),
            Flash(
                self.body.get_center(),
                color=c,
                line_length=0.18,
                num_lines=14,
                flash_radius=1.35,
            ),
            lag_ratio=0.05,
        )

    def go_bad(self):
        return AnimationGroup(
            self.body.animate.set_stroke(BAD, width=4),
            self.aura.animate.set_stroke(BAD, width=22, opacity=0.30),
            self.tag.animate.set_color(BAD),
        )

    def go_good(self):
        return AnimationGroup(
            self.body.animate.set_stroke(OK, width=4),
            self.aura.animate.set_stroke(OK, width=18, opacity=0.22),
            self.tag.animate.set_color(OK),
        )

    def reset_color(self):
        return AnimationGroup(
            self.body.animate.set_stroke(self.color_, width=3),
            self.aura.animate.set_stroke(self.color_, width=16, opacity=0.16),
            self.tag.animate.set_color(self.color_),
        )

    def shake(self, scene, amount=0.1, times=4):
        for i in range(times):
            scene.play(
                self.animate.shift(RIGHT * amount * (1 if i % 2 == 0 else -1)),
                run_time=0.055,
                rate_func=there_and_back,
            )


def pill(txt, color=TEXT, size=FS_BODY):
    """Input/output value ka capsule."""
    t = mono(txt, size=size, color=color)
    bg = RoundedRectangle(
        width=t.width + 0.44,
        height=0.62,
        corner_radius=0.31,
        fill_color=PANEL,
        fill_opacity=1,
        stroke_color=color,
        stroke_width=2,
    )
    g = VGroup(bg, t)
    g.value_color = color
    return g


class Shot(VGroup):
    """Ek probe shot: input pill → box → output pill."""

    def __init__(self, box, value, color=TEXT, buff=1.25, **kw):
        super().__init__(**kw)
        self.box = box
        self.buff = buff
        self.pill = pill(value, color)
        self.pill.next_to(box, LEFT, buff=buff)
        self.add(self.pill)

    def fire(self, scene, out_value, out_color=TEXT, flash=True):
        a_in = Arrow(
            self.pill.get_right() + RIGHT * 0.12,
            self.box.get_left() + LEFT * 0.12,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.13,
            color=DIM,
        )
        scene.play(GrowArrow(a_in), run_time=0.42)
        if flash:
            scene.play(self.box.pulse(), run_time=0.5)

        out = pill(out_value, out_color)
        out.next_to(self.box, RIGHT, buff=self.buff)
        a_out = Arrow(
            self.box.get_right() + RIGHT * 0.12,
            out.get_left() + LEFT * 0.12,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.13,
            color=out_color,
        )
        scene.play(GrowArrow(a_out), FadeIn(out, shift=RIGHT * 0.25), run_time=0.48)
        self.add(a_in, a_out, out)
        self.out = out
        return out


# ══════════════════════════════════════════════════════════════ LOG TABLE


class LogTable(VGroup):
    """Probe log — INPUT · OUTPUT · STATUS. Rows ek ek kar ke add hoti hain."""

    COLS = (1.5, 1.7, 1.6)
    ROW_H = 0.44
    HEAD_DROP = 0.74

    def __init__(self, title="PROBE LOG", rows_max=7, **kw):
        super().__init__(**kw)
        w = sum(self.COLS) + 0.9
        self.card = panel(w, self.HEAD_DROP + self.ROW_H * rows_max + 0.2, radius=0.12)
        heads = VGroup(
            *[Text(t, font=MONO, font_size=FS_TINY, color=DIM) for t in ("INPUT", "OUTPUT", "STATUS")]
        )
        for i, c in enumerate(heads):
            c.move_to(self.card.get_top() + DOWN * 0.4 + RIGHT * self._dx(i))
        rule = hairline(w - 0.5).next_to(heads, DOWN, buff=0.14)
        cap = Text(title, font=MONO, font_size=FS_TINY, color=DIM, weight="BOLD")
        cap.next_to(self.card, UP, buff=0.16).align_to(self.card, LEFT)

        self.rows = VGroup()
        self.add(self.card, heads, rule, cap, self.rows)

    def _dx(self, i):
        x = -sum(self.COLS) / 2
        for k in range(i):
            x += self.COLS[k]
        return x + self.COLS[i] / 2

    def make_row(self, inp, out, status, color=TEXT, index=None):
        """Row ki position card se relative nikalti hai — group move karne ke baad bhi theek."""
        idx = len(self.rows) if index is None else index
        y = self.card.get_top()[1] - self.HEAD_DROP - self.ROW_H * (idx + 0.5)
        cells = VGroup(
            mono(inp, size=FS_SMALL, color=TEXT),
            mono(out, size=FS_SMALL, color=color),
            mono(status, size=FS_TINY, color=color),
        )
        for i, c in enumerate(cells):
            c.move_to([self.card.get_x() + self._dx(i), y, 0])
        return cells

    def add_row(self, scene, inp, out, status, color=TEXT, run_time=0.38):
        row = self.make_row(inp, out, status, color)
        self.rows.add(row)
        scene.play(FadeIn(row, shift=RIGHT * 0.25), run_time=run_time)
        return row


# ══════════════════════════════════════════════════════════════ ARROW DIAGRAM


class ArrowDiagram(VGroup):
    """D → E arrow diagram (Stewart Figure 3 style).

    pairs: [(i, j), ...] — D ke i-th dot se E ke j-th dot tak arrow.
    """

    def __init__(
        self,
        pairs,
        n_in=2,
        n_out=2,
        in_labels=None,
        out_labels=None,
        d_label="D",
        e_label="E",
        color=BOXC,
        w=1.45,
        h=2.3,
        gap=2.9,
        **kw,
    ):
        super().__init__(**kw)
        left = Ellipse(width=w, height=h, stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1)
        right = left.copy().shift(RIGHT * gap)

        def dots(oval, n):
            span = (h - 0.9) if n > 1 else 0.0
            ys = np.linspace(span / 2, -span / 2, n)
            return VGroup(*[Dot(radius=0.06, color=TEXT).move_to(oval.get_center() + UP * y) for y in ys])

        self.in_dots = dots(left, n_in)
        self.out_dots = dots(right, n_out)

        self.arrows = VGroup()
        for i, j in pairs:
            self.arrows.add(
                Arrow(
                    self.in_dots[i].get_center(),
                    self.out_dots[j].get_center(),
                    buff=0.14,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.09,
                    color=color,
                )
            )

        caps = VGroup(
            Text(d_label, font=MONO, font_size=FS_TINY, color=DIM).next_to(left, DOWN, buff=0.18),
            Text(e_label, font=MONO, font_size=FS_TINY, color=DIM).next_to(right, DOWN, buff=0.18),
        )
        self.add(left, right, self.arrows, self.in_dots, self.out_dots, caps)

        if in_labels:
            for d, s in zip(self.in_dots, in_labels):
                self.add(mono(s, size=FS_TINY, color=DIM).next_to(d, LEFT, buff=0.14))
        if out_labels:
            for d, s in zip(self.out_dots, out_labels):
                self.add(mono(s, size=FS_TINY, color=DIM).next_to(d, RIGHT, buff=0.14))


# ══════════════════════════════════════════════════════════════ BANNERS & CARDS


class GlitchBanner(VGroup):
    """Level ka core sawaal — jab box samajh se bahar kuch karti hai."""

    def __init__(self, text, label="GLITCH", color=BAD, width=8.6, **kw):
        super().__init__(**kw)
        self.card = panel(width, 1.3, fill="#1A0C10", stroke=color, radius=0.12)
        chip = VGroup(
            RoundedRectangle(
                width=1.4, height=0.4, corner_radius=0.2, fill_color=color, fill_opacity=1, stroke_width=0
            ),
            Text(label, font=MONO, font_size=FS_TINY, color="#12060A", weight="BOLD"),
        )
        stack = VGroup(chip, body(text, color=TEXT)).arrange(DOWN, buff=0.24).move_to(self.card)
        self.add(glow(self.card, color, width=20, opacity=0.14), self.card, stack)

    def play_in(self, scene, jitter=True):
        scene.play(FadeIn(self, scale=0.94), run_time=0.5)
        if jitter:
            for i in range(3):
                scene.play(
                    self.animate.shift(RIGHT * 0.07 * (1 if i % 2 == 0 else -1)),
                    run_time=0.05,
                    rate_func=there_and_back,
                )


class ToolCard(VGroup):
    """Level ka reward."""

    def __init__(self, name, note, icon=None, color=WARN, **kw):
        super().__init__(**kw)
        self.card = panel(6.9, 2.5, fill=PANEL_2, stroke=color, radius=0.16)
        head = Text("TOOL UNLOCKED", font=MONO, font_size=FS_TINY, color=color, weight="BOLD")
        title = Text(name, font=MONO, font_size=FS_H1, color=TEXT, weight="BOLD")
        stack = VGroup(head, title, small(note, color=DIM)).arrange(DOWN, buff=0.22)

        if icon is not None:
            icon.set_color(color).scale_to_fit_height(1.0)
            row = VGroup(icon, stack).arrange(RIGHT, buff=0.55)
        else:
            row = stack
        row.move_to(self.card)
        self.add(glow(self.card, color, width=24, opacity=0.16), self.card, row)

    def play_in(self, scene, hold=2.0):
        scene.play(
            FadeIn(self, scale=0.9),
            Flash(self.get_center(), color=WARN, line_length=0.4, num_lines=22, flash_radius=2.7),
            run_time=0.9,
        )
        scene.wait(hold)


class InfoCard(VGroup):
    """Definition / concept card. `t2c` se keywords highlight karein."""

    def __init__(self, heading, text, t2c=None, color=ACCENT, width=10.2, **kw):
        super().__init__(**kw)
        head = Text(heading, font=MONO, font_size=FS_TINY, color=color, weight="BOLD")
        para = Text(
            text,
            font_size=FS_BODY,
            color=TEXT,
            line_spacing=0.85,
            t2c=t2c or {},
        )
        inner = VGroup(head, para).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        card = panel(max(width, inner.width + 1.0), inner.height + 1.0, fill=PANEL, stroke=color, radius=0.14)
        inner.move_to(card)
        self.card = card
        self.para = para
        self.add(glow(card, color, width=16, opacity=0.10), card, inner)


def verdict(text, ok=True, width=6.2):
    """Bara faisla card — FUNCTION / NOT A FUNCTION."""
    c = OK if ok else BAD
    card = panel(width, 1.1, fill=PANEL_2, stroke=c, radius=0.55)
    t = Text(text, font=MONO, font_size=FS_H1, color=c, weight="BOLD").move_to(card)
    return VGroup(glow(card, c, width=22, opacity=0.16), card, t)


def book_ref(text, color=ACCENT):
    """Bottom-right citation — 'STEWART · p. 8'."""
    return Text(text, font=MONO, font_size=FS_TINY, color=color).to_corner(DR, buff=0.34).set_opacity(0.85)


def caption(text, color=DIM):
    return body(text, color=color).to_edge(DOWN, buff=0.62)


def beat(scene, mobs, lag=0.15, run_time=0.9, hold=0.0):
    """Standard staggered reveal."""
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.22) for m in mobs], lag_ratio=lag), run_time=run_time)
    if hold:
        scene.wait(hold)


# ══════════════════════════════════════════════════════════════ LABELS & SLOTS


class LabelChip(VGroup):
    """Chhoti rounded label — diagram ke parts ko naam dene ke liye."""

    def __init__(self, text, color=WARN, size=FS_TINY, **kw):
        super().__init__(**kw)
        t = Text(text, font=MONO, font_size=size, color=color, weight="BOLD")
        bg = RoundedRectangle(
            width=t.width + 0.34,
            height=t.height + 0.24,
            corner_radius=0.12,
            fill_color=PANEL,
            fill_opacity=1,
            stroke_color=color,
            stroke_width=1.6,
        )
        self.text = t
        self.bg = bg
        self.add(bg, t)


class Slot(VGroup):
    """Khaali dashed jagah jahan label lagni hai. `fill_with()` se label baithti hai."""

    def __init__(self, width=1.9, height=0.5, color=DIM, **kw):
        super().__init__(**kw)
        self.frame = DashedVMobject(
            RoundedRectangle(
                width=width, height=height, corner_radius=0.1,
                stroke_color=color, stroke_width=2, fill_opacity=0,
            ),
            num_dashes=22,
        )
        self.q = Text("?", font=MONO, font_size=FS_SMALL, color=color).move_to(self.frame)
        self.add(self.frame, self.q)

    def fill_with(self, chip, color=OK):
        """Slot me chip ko baithane ki animation."""
        chip.move_to(self.frame)
        return AnimationGroup(
            FadeOut(self.q, scale=0.6),
            self.frame.animate.set_stroke(color, opacity=0.45),
            FadeIn(chip, scale=1.15),
            lag_ratio=0.12,
        )


def interval_bar(nl, a, b, closed_left=True, closed_right=True, color=OK, width=8, dy=0.0):
    """NumberLine par ek interval highlight karo.

    Bhara hua dot = closed endpoint (<=), khokhla dot = open endpoint (<).
    L03 (domain), L08 (piecewise slabs), L33/L40 (restricted domain) me lagta hai.
    """
    p1 = nl.number_to_point(a) + UP * dy
    p2 = nl.number_to_point(b) + UP * dy
    seg = Line(p1, p2, stroke_color=color, stroke_width=width)

    def cap(p, closed):
        if closed:
            return Dot(radius=0.095, color=color).move_to(p)
        return Circle(
            radius=0.095, stroke_color=color, stroke_width=3.5,
            fill_color=BG, fill_opacity=1,
        ).move_to(p)

    return VGroup(seg, cap(p1, closed_left), cap(p2, closed_right))


def ray_bar(nl, a, closed=True, to_right=True, color=OK, width=8, dy=0.0):
    """Infinite taraf jaane wala interval — [a, inf) ya (-inf, a]."""
    end = nl.get_right() if to_right else nl.get_left()
    p1 = nl.number_to_point(a) + UP * dy
    p2 = np.array([end[0], p1[1], 0.0])
    seg = Arrow(p1, p2, buff=0, stroke_width=width,
                max_tip_length_to_length_ratio=0.06, color=color)
    if closed:
        cap = Dot(radius=0.095, color=color).move_to(p1)
    else:
        cap = Circle(radius=0.095, stroke_color=color, stroke_width=3.5,
                     fill_color=BG, fill_opacity=1).move_to(p1)
    return VGroup(seg, cap)


def wire(start, end, color=DIM, label=None, label_color=None, dashed=False):
    """Labelled arrow — machine diagram ki taar."""
    a = Arrow(
        start, end, buff=0,
        stroke_width=3,
        max_tip_length_to_length_ratio=0.13,
        color=color,
    )
    if dashed:
        a = VGroup(DashedVMobject(a, num_dashes=12))
    if label is None:
        return a
    lab = Text(label, font=MONO, font_size=FS_TINY, color=label_color or color)
    lab.next_to(a, UP, buff=0.14)
    return VGroup(a, lab)


# ══════════════════════════════════════════════════════════════ ICONS (vector, emoji-free)


def magnifier_icon(color=WARN):
    """PROBE tool."""
    lens = Circle(radius=0.34, stroke_color=color, stroke_width=6)
    handle = Line(
        lens.get_center() + np.array([0.24, -0.24, 0]),
        lens.get_center() + np.array([0.60, -0.60, 0]),
        stroke_color=color,
        stroke_width=7,
    )
    return VGroup(lens, handle)


def tape_icon(color=WARN):
    """BOUNDARY TAPE tool (L03) — |----| yani ek marked interval."""
    span = Line([-0.42, 0, 0], [0.42, 0, 0], stroke_color=color, stroke_width=6)
    left = Line([-0.42, -0.2, 0], [-0.42, 0.2, 0], stroke_color=color, stroke_width=6)
    right = Line([0.42, -0.2, 0], [0.42, 0.2, 0], stroke_color=color, stroke_width=6)
    return VGroup(span, left, right)


def tag_icon(color=WARN):
    """LABEL GUN tool (L02)."""
    body_ = Polygon(
        [-0.35, 0.22, 0], [0.22, 0.22, 0], [0.42, 0.0, 0], [0.22, -0.22, 0], [-0.35, -0.22, 0],
        stroke_color=color,
        stroke_width=5,
    )
    hole = Dot(radius=0.05, color=color).move_to([-0.18, 0, 0])
    return VGroup(body_, hole)
