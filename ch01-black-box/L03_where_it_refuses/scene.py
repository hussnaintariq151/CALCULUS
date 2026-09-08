"""
THE BLACK BOX · ACT I · LEVEL 03 — WHERE DOES IT REFUSE?

Concept: domain aur range; domain convention; interval notation.
Book: Stewart, Early Transcendentals, §1.1
      p. 8-9  — domain / range ki tareef
      p. 13   — DOMAIN CONVENTION + Example 6:  sqrt(x+2)  aur  1/(x^2 - x)
      p. 20   — Ex 39-48 (domain drills)

Design nukta: box ka rule `g(x) = 1/sqrt(x)` hai, is liye uske DO failure modes
hi woh DO banned operations hain jo poori calculus me domain torte hain —
even root ke andar negative, aur denominator me zero.

Colab me render:
    !manim -qh --media_dir /content/media  PROJECT/L03_where_it_refuses/scene.py L03Cinematic

Scenes:
    L03Cinematic      — pura level (~4 min)
    L03Traps          — teen domain traps (cube root / AND / strict)
    L03RangeParadox   — range endpoints par nahi hoti (x^2 on [-1,3])
    L03Recap          — 50s revision reel
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
for _cand in (_HERE.parent / "shared", _HERE / "shared", Path("shared"), Path("../shared")):
    if (_cand / "hud.py").exists():
        sys.path.insert(0, str(_cand))
        break

from manim import *  # noqa: E402

from theme import *  # noqa: E402,F403
from hud import *  # noqa: E402,F403


# ──────────────────────────────────────────────────────────── helpers


def numline(a, b, step=1, length=10.0, labels=None, label_step=1):
    """LaTeX-free number line: NumberLine + apne mono labels.

    `NumberLine(include_numbers=True)` MathTex use karta hai, is liye labels
    khud banate hain. Returns (group, nl).
    """
    nl = NumberLine(
        x_range=[a, b, step],
        length=length,
        color=DIM,
        stroke_width=2,
        include_tip=False,
        tick_size=0.07,
    )
    marks = VGroup()
    vals = labels if labels is not None else range(int(a), int(b) + 1, label_step)
    for v in vals:
        marks.add(
            mono(str(v), size=FS_TINY, color=DIM).next_to(nl.number_to_point(v), DOWN, buff=0.2)
        )
    return VGroup(nl, marks), nl


def tick_mark(nl, x, ok, dy=0.32):
    """Accepted = bhara dot · rejected = laal cross."""
    p = nl.number_to_point(x) + UP * dy
    if ok:
        return Dot(radius=0.085, color=OK).move_to(p)
    s = 0.1
    return VGroup(
        Line(p + np.array([-s, -s, 0]), p + np.array([s, s, 0]), stroke_color=BAD, stroke_width=4),
        Line(p + np.array([-s, s, 0]), p + np.array([s, -s, 0]), stroke_color=BAD, stroke_width=4),
    )


def hole(nl, x, dy=0.36):
    """Domain me surakh — khokhla laal circle."""
    return Circle(
        radius=0.1, stroke_color=BAD, stroke_width=4, fill_color=BG, fill_opacity=1
    ).move_to(nl.number_to_point(x) + UP * dy)


def domain_case(expr, why, answer, color=OK, w=11.0):
    """Ek domain problem ka teen-satri card: expression → shart → jawab."""
    rows = VGroup(
        VGroup(
            LabelChip("EXPRESSION", color=DIM, size=FS_TINY),
            mono(expr, size=FS_BODY, color=TEXT),
        ).arrange(RIGHT, buff=0.3),
        VGroup(
            LabelChip("SHART", color=WARN, size=FS_TINY),
            mono(why, size=FS_SMALL, color=WARN),
        ).arrange(RIGHT, buff=0.3),
        VGroup(
            LabelChip("DOMAIN", color=color, size=FS_TINY),
            mono(answer, size=FS_BODY, color=color, weight="BOLD"),
        ).arrange(RIGHT, buff=0.3),
    ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    card = panel(max(w, rows.width + 1.0), rows.height + 0.9, stroke=LINE, radius=0.14)
    rows.move_to(card)
    g = VGroup(card, rows)
    g.rows = rows
    return g


def range_rig(scene, f, dom, in_range, out_range, out_label_step=2, run_time=5.0):
    """INPUT line se OUTPUT line — input sweep karo, range khud paint hoti hai.

    Returns (group, in_nl, out_nl, trail, link) — caller cleanup karta hai.
    """
    in_grp, in_nl = numline(in_range[0], in_range[1], length=7.4)
    in_grp.shift(UP * 0.55)
    out_grp, out_nl = numline(out_range[0], out_range[1], length=9.6, label_step=out_label_step)
    out_grp.shift(DOWN * 1.9)
    in_tag = mono("INPUT", size=FS_TINY, color=WARN).next_to(in_nl, LEFT, buff=0.3)
    out_tag = mono("OUTPUT", size=FS_TINY, color=OK).next_to(out_nl, LEFT, buff=0.3)

    scene.play(FadeIn(in_grp), FadeIn(out_grp), FadeIn(in_tag), FadeIn(out_tag), run_time=0.7)
    dom_bar = interval_bar(in_nl, dom[0], dom[1], True, True, color=WARN, width=7, dy=0.3)
    scene.play(Create(dom_bar), run_time=0.7)

    t = ValueTracker(float(dom[0]))
    in_pt = lambda: in_nl.number_to_point(t.get_value()) + UP * 0.3
    out_pt = lambda: out_nl.number_to_point(f(t.get_value())) + UP * 0.3

    in_dot = Dot(radius=0.1, color=WARN).move_to(in_pt())
    out_dot = Dot(radius=0.1, color=OK).move_to(out_pt())
    in_dot.add_updater(lambda m: m.move_to(in_pt()))
    out_dot.add_updater(lambda m: m.move_to(out_pt()))
    link = always_redraw(
        lambda: DashedLine(
            in_dot.get_center(), out_dot.get_center(),
            stroke_color=LINE, stroke_width=2, dash_length=0.09,
        )
    )
    trail = TracedPath(out_dot.get_center, stroke_color=OK, stroke_width=8)

    scene.add(link, trail, in_dot, out_dot)
    scene.play(t.animate.set_value(float(dom[1])), run_time=run_time, rate_func=linear)
    in_dot.clear_updaters()
    out_dot.clear_updaters()

    static = VGroup(in_grp, out_grp, in_tag, out_tag, dom_bar, in_dot, out_dot)
    return static, in_nl, out_nl, trail, link


# ──────────────────────────────────────────────────────────── main scene


class L03Cinematic(Scene):
    def construct(self):
        apply_theme(self)
        self.hud = HudBar("L03", "WHERE DOES IT REFUSE?", act=1, decode=4.8)

        self.beat_title()
        self.beat_refuse()
        self.beat_scan()
        self.beat_reveal()
        self.beat_definition()
        self.beat_example6a()
        self.beat_example6b()
        self.beat_traps()
        self.beat_range()
        self.beat_reality()
        self.beat_ai()
        self.beat_reward()

    # ── helper
    def swap_caption(self, old, text):
        new = caption(text)
        if old is None:
            self.play(FadeIn(new, shift=UP * 0.2), run_time=0.5)
        else:
            self.play(FadeOut(old, shift=DOWN * 0.2), FadeIn(new, shift=UP * 0.2), run_time=0.5)
        return new

    # ── beats

    def beat_title(self):
        self.play(FadeIn(self.hud, shift=DOWN * 0.2), run_time=0.7)
        LevelCard(
            act_no=1,
            act_title="FIRST CONTACT",
            level_no=3,
            title="WHERE DOES IT REFUSE?",
            brief="Nayi box aayi hai. Yeh har number qubool nahi karti.",
        ).shift(DOWN * 0.25).play_in(self, hold=1.7)

    def beat_refuse(self):
        """Teen shots: ERROR, JAM, aur ek theek."""
        box = BlackBox("? ? ?", w=2.9, h=1.9).shift(LEFT * 2.9 + UP * 0.2)
        serial = mono("SALVAGE UNIT  ·  CH-03", size=FS_TINY, color=DIM)
        serial.next_to(box, DOWN, buff=0.32)
        log = LogTable("PROBE LOG", rows_max=3).to_edge(RIGHT, buff=0.4).shift(UP * 0.15)

        self.play(FadeIn(box, scale=0.92), FadeIn(serial), run_time=0.8)
        self.play(FadeIn(log, shift=LEFT * 0.3), run_time=0.6)
        cap = self.swap_caption(None, "PROBE nikala (L01 ka reward). Pehla shot: -5")

        shots = [
            ("-5", "ERROR", "reject", BAD, "Minus par ERROR. Theek — shayad negative allowed nahi."),
            ("0", "JAM", "reject", BAD, "Sifar par JAM — magar yeh ERROR se ALAG lafz hai. Kyun?"),
            ("3", "0.577", "logged", OK, "3 par jawab aa gaya. Box kaam karti hai — bas har jagah nahi."),
        ]
        for inp, out, status, c, text in shots:
            shot = Shot(box, inp, buff=0.85)
            self.play(FadeIn(shot.pill, shift=RIGHT * 0.2), run_time=0.3)
            shot.fire(self, out, out_color=c)
            log.add_row(self, inp, out, status, color=c)
            cap = self.swap_caption(cap, text)
            self.wait(0.9)
            self.play(FadeOut(shot), run_time=0.25)

        self.play(FadeOut(VGroup(box, serial, log)), FadeOut(cap), run_time=0.6)

    def beat_scan(self):
        """Number line par poora sweep — domain khud paint hoti hai."""
        title = h2("Poori number line scan karo").to_edge(UP, buff=1.3)
        grp, nl = numline(-6, 6, length=11.0)
        grp.shift(DOWN * 0.3)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.play(Create(nl), FadeIn(grp[1]), run_time=1.0)

        probes = [(-5, False), (-3, False), (-1, False), (0, False),
                  (0.5, True), (1, True), (2.5, True), (4, True), (5.5, True)]
        marks = VGroup()
        for x, ok in probes:
            m = tick_mark(nl, x, ok)
            marks.add(m)
            self.play(FadeIn(m, scale=0.6), run_time=0.17)
        self.wait(0.6)

        cap = self.swap_caption(None, "Sifar tak sab reject. Sifar ke baad sab qubool. Sarhad kahan hai?")
        bar = ray_bar(nl, 0, closed=False, to_right=True, color=OK, dy=-0.42)
        tag = mono("(0, inf)", size=FS_H2, color=OK, weight="BOLD").next_to(bar, DOWN, buff=0.5)

        self.play(Create(bar), run_time=1.0)
        self.play(FadeIn(tag, shift=UP * 0.2), run_time=0.5)
        self.play(Circumscribe(bar[1], color=WARN, buff=0.12), run_time=1.1)
        cap = self.swap_caption(
            cap, "Khokhla dot = woh point shamil NAHI. Isi liye round bracket: (0, inf)"
        )
        self.wait(2.0)
        self.play(FadeOut(VGroup(title, grp, marks, bar, tag)), FadeOut(cap), run_time=0.6)

    def beat_reveal(self):
        """Rule khulta hai — aur dono failures ki wajah alag nikalti hai."""
        rule = kbd("g(x) = 1 / sqrt(x)").scale(1.15).shift(UP * 1.55)
        self.play(Write(rule), run_time=1.0)
        self.play(
            Flash(rule.get_center(), color=BOXC, line_length=0.3, num_lines=18, flash_radius=2.2),
            run_time=0.7,
        )

        rows = VGroup(
            VGroup(
                mono("g(-5)", size=FS_BODY, color=TEXT),
                mono("=  1 / sqrt(-5)", size=FS_BODY, color=DIM),
                LabelChip("sqrt of NEGATIVE", color=BAD, size=FS_TINY),
            ).arrange(RIGHT, buff=0.35),
            VGroup(
                mono("g(0)", size=FS_BODY, color=TEXT),
                mono("=  1 / 0", size=FS_BODY, color=DIM),
                LabelChip("DIVIDE by zero", color=BAD, size=FS_TINY),
            ).arrange(RIGHT, buff=0.35),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows.next_to(rule, DOWN, buff=0.8)

        self.play(FadeIn(rows[0], shift=RIGHT * 0.25), run_time=0.7)
        self.play(FadeIn(rows[1], shift=RIGHT * 0.25), run_time=0.7)
        cap = self.swap_caption(None, "Do mukhtalif lafz thay kyunki do mukhtalif jurm thay.")
        self.wait(1.6)

        banned = InfoCard(
            "POORI CALCULUS ME SIRF DO CHEEZEIN MANA HAIN",
            "1.   EVEN root (sqrt, 4th root...) ke andar negative\n"
            "2.   denominator me zero",
            t2c={"EVEN root": WARN, "negative": BAD, "zero": BAD},
            width=9.8,
            color=BAD,
        ).next_to(rows, DOWN, buff=0.7)
        self.play(FadeIn(banned, shift=UP * 0.2), run_time=0.8)
        cap = self.swap_caption(cap, "Domain nikalna = sirf yeh do cheezein rokna. Bas itna hi.")
        self.wait(2.4)
        self.play(FadeOut(VGroup(rule, rows, banned)), FadeOut(cap), run_time=0.6)

    def beat_definition(self):
        card = InfoCard(
            "DEFINITION  ·  STEWART p. 8-9, 13",
            "DOMAIN  =  tamam jaiz inputs ka set   (set D)\n"
            "RANGE   =  tamam mumkin outputs ka set\n"
            "\n"
            "DOMAIN CONVENTION: agar domain likhi na ho, to domain woh tamam\n"
            "inputs hain jinke liye formula ka matlab bane aur real number de.",
            t2c={"DOMAIN": OK, "RANGE": WARN, "DOMAIN CONVENTION": ACCENT},
            width=10.8,
        ).shift(UP * 0.9)
        ref = book_ref("STEWART  ·  p. 13")
        self.play(FadeIn(card, shift=UP * 0.2), FadeIn(ref), run_time=0.8)
        self.wait(2.2)

        grp, nl = numline(-1, 5, length=8.4)
        grp.next_to(card, DOWN, buff=1.0)
        b1 = interval_bar(nl, 0, 3, True, True, color=OK, dy=0.34)
        t1 = mono("[0, 3]   dono shamil", size=FS_TINY, color=OK).next_to(b1, UP, buff=0.18)
        b2 = interval_bar(nl, 0, 3, False, False, color=WARN, dy=-0.34)
        t2 = mono("(0, 3)   dono bahar", size=FS_TINY, color=WARN).next_to(b2, DOWN, buff=0.45)

        self.play(FadeIn(grp), run_time=0.5)
        self.play(Create(b1), FadeIn(t1), run_time=0.7)
        self.play(Create(b2), FadeIn(t2), run_time=0.7)
        cap = self.swap_caption(None, "Square bracket = shamil.   Round bracket = shamil nahi.")
        self.wait(2.2)
        self.play(
            FadeOut(VGroup(card, grp, b1, t1, b2, t2)), FadeOut(cap), FadeOut(ref), run_time=0.6
        )

    def beat_example6a(self):
        title = h2("Example 6(a)  —  Stewart p. 13").to_edge(UP, buff=1.3)
        case = domain_case(
            "f(x) = sqrt(x + 2)",
            "x + 2 >= 0   ->   x >= -2",
            "[-2, inf)",
        ).next_to(title, DOWN, buff=0.7)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(case[0]), run_time=0.35)
        for r in case.rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.55)

        grp, nl = numline(-5, 5, length=9.0)
        grp.next_to(case, DOWN, buff=0.9)
        bar = ray_bar(nl, -2, closed=True, to_right=True, color=OK, dy=0.36)
        self.play(FadeIn(grp), run_time=0.4)
        self.play(Create(bar), run_time=0.8)
        cap = self.swap_caption(
            None, "-2 par sqrt(0) = 0 milta hai — jaiz. Is liye bhara dot, aur [ bracket."
        )
        self.wait(2.2)
        self.play(FadeOut(VGroup(title, case, grp, bar)), FadeOut(cap), run_time=0.6)

    def beat_example6b(self):
        title = h2("Example 6(b)  —  do surakh").to_edge(UP, buff=1.3)
        case = domain_case(
            "g(x) = 1 / (x^2 - x)  =  1 / [ x (x - 1) ]",
            "x (x - 1) != 0   ->   x != 0  aur  x != 1",
            "(-inf, 0) U (0, 1) U (1, inf)",
        ).next_to(title, DOWN, buff=0.7)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(case[0]), run_time=0.35)
        for r in case.rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.55)

        grp, nl = numline(-3, 4, length=9.0)
        grp.next_to(case, DOWN, buff=0.85)
        pieces = VGroup(
            ray_bar(nl, 0, closed=False, to_right=False, color=OK, dy=0.36),
            interval_bar(nl, 0, 1, False, False, color=OK, dy=0.36),
            ray_bar(nl, 1, closed=False, to_right=True, color=OK, dy=0.36),
        )
        holes = VGroup(hole(nl, 0), hole(nl, 1))
        self.play(FadeIn(grp), run_time=0.4)
        self.play(LaggedStart(*[Create(p) for p in pieces], lag_ratio=0.35), run_time=1.2)
        self.play(FadeIn(holes, scale=0.6), run_time=0.5)
        cap = self.swap_caption(
            None, "Pehle denominator ko factor karo — surakh khud nazar aa jaate hain."
        )
        self.wait(2.2)
        self.play(FadeOut(VGroup(title, case, grp, pieces, holes)), FadeOut(cap), run_time=0.6)

    def beat_traps(self):
        title = h2("Teen jagah log phaste hain").to_edge(UP, buff=1.25)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)

        traps = [
            (
                "f(t) = cbrt(2t - 1)",
                "CUBE root  —  koi shart nahi",
                "(-inf, inf)   saari real numbers",
                "Sirf EVEN roots negative se darte hain. Cube root -8 se -2 de deta hai.",
            ),
            (
                "g(t) = sqrt(3 - t) - sqrt(2 + t)",
                "3 - t >= 0   AUR   2 + t >= 0",
                "[-2, 3]   dono sharton ka OVERLAP",
                "Do sqrt = do shartein. AUR ka matlab intersection hai, union nahi.",
            ),
            (
                "h(x) = 1 / 4throot(x^2 - 5x)",
                "x^2 - 5x > 0   (strictly — barabar mana)",
                "(-inf, 0) U (5, inf)",
                "Root DENOMINATOR me hai, is liye zero bhi mana. >= ki jagah > lagta hai.",
            ),
        ]
        cap = None
        for expr, why, ans, note in traps:
            case = domain_case(expr, why, ans).next_to(title, DOWN, buff=0.85)
            self.play(FadeIn(case, shift=UP * 0.2), run_time=0.7)
            cap = self.swap_caption(cap, note)
            self.wait(2.6)
            self.play(FadeOut(case), run_time=0.4)

        ref = book_ref("STEWART  ·  Ex 1.1.41, 42, 43   p. 20")
        self.play(FadeIn(ref), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(title), FadeOut(cap), FadeOut(ref), run_time=0.5)

    def beat_range(self):
        """Range endpoints par nahi hoti — x^2 on [-1, 3]."""
        title = h2("Ab RANGE  —  aur ek badi ghalti").to_edge(UP, buff=1.25)
        given = mono("f(x) = x^2        domain = [-1, 3]", size=FS_BODY, color=OK)
        given.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(given), run_time=0.7)

        cap = self.swap_caption(
            None, "Input ko poori domain par ghumao — output khud apni range paint karega."
        )
        static, in_nl, out_nl, trail, link = range_rig(
            self, lambda x: x * x, (-1, 3), (-2, 4), (0, 10)
        )
        self.wait(0.6)

        wrong = VGroup(
            mono("[1, 9]", size=FS_H2, color=BAD, weight="BOLD"),
            mono("f(-1) = 1  aur  f(3) = 9  ...  is liye?   GALAT", size=FS_TINY, color=BAD),
        ).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=1.45)
        right = VGroup(
            mono("[0, 9]", size=FS_H2, color=OK, weight="BOLD"),
            mono("kyunki x = 0 bhi domain me hai, aur f(0) = 0", size=FS_TINY, color=OK),
        ).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=1.45)

        self.play(FadeOut(cap), FadeIn(wrong, shift=UP * 0.2), run_time=0.6)
        self.play(Indicate(wrong, color=BAD, scale_factor=1.04), run_time=0.8)
        self.wait(1.2)
        self.play(ReplacementTransform(wrong, right), run_time=0.8)
        self.play(
            Flash(out_nl.number_to_point(0) + UP * 0.3, color=OK,
                  line_length=0.22, num_lines=14, flash_radius=0.9),
            run_time=0.8,
        )
        cap = self.swap_caption(
            None, "Range sirf endpoints se nahi banti — beech ka koi point sabse chhota ho sakta hai."
        )
        self.wait(2.4)

        self.remove(link, trail)
        self.play(
            FadeOut(VGroup(title, given, static, right)), FadeOut(cap), run_time=0.7
        )

    def beat_reality(self):
        """Formula zyada allow karta hai, haqeeqat kam."""
        title = h2("Formula ki domain  vs  haqeeqat ki domain").to_edge(UP, buff=1.3)
        expr = mono("C(w) = 20w^2 + 180/w", size=FS_H2, color=BOXC).next_to(title, DOWN, buff=0.5)

        rows = VGroup(
            VGroup(
                LabelChip("MATH kehta hai", color=WARN, size=FS_TINY),
                mono("w != 0     (sirf denominator ki shart)", size=FS_BODY, color=WARN),
            ).arrange(RIGHT, buff=0.35),
            VGroup(
                LabelChip("HAQEEQAT kehti hai", color=OK, size=FS_TINY),
                mono("w > 0      (width manfi nahi ho sakti)", size=FS_BODY, color=OK),
            ).arrange(RIGHT, buff=0.35),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows.next_to(expr, DOWN, buff=0.75)

        self.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(expr), run_time=0.7)
        self.play(FadeIn(rows[0], shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(rows[1], shift=RIGHT * 0.2), run_time=0.6)

        note = body("Applied problem me hamesha CHHOTI domain jeetti hai.", color=DIM)
        note.next_to(rows, DOWN, buff=0.7)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.5)
        ref = book_ref("STEWART  ·  p. 12 Example 5   (L10 ka boss)")
        self.play(FadeIn(ref), run_time=0.4)
        self.wait(2.4)
        self.play(FadeOut(VGroup(title, expr, rows, note)), FadeOut(ref), run_time=0.6)

    def beat_ai(self):
        card = InfoCard(
            "AI CONNECTION",
            "domain  =  input validation  +  feature range\n"
            "range   =  output ki hadd   (sigmoid -> (0,1),  ReLU -> [0,inf))\n"
            "\n"
            "assert 0 < lr < 1            ek domain check hai\n"
            "log(p) ke liye p > 0         is liye log(p + 1e-9) likhte hain\n"
            "\n"
            "Training range se bahar input dena = domain violation.\n"
            "Model crash nahi karta — bas confidently bakwaas deta hai.",
            t2c={
                "input validation": OK,
                "output ki hadd": WARN,
                "domain check": OK,
                "confidently bakwaas": BAD,
            },
            width=11.0,
        )
        self.play(FadeIn(card, shift=UP * 0.25), run_time=0.8)
        self.wait(3.8)
        self.play(FadeOut(card), run_time=0.5)

    def beat_reward(self):
        tool = ToolCard(
            "BOUNDARY TAPE",
            "Kisi bhi rule ki domain aur range nikalna.\n"
            "Aage 8 levels me lagta hai: L08, L16, L17, L24, L25, L31, L36, L40.",
            icon=tape_icon(),
        ).shift(UP * 0.3)
        self.add(self.hud)
        tool.play_in(self, hold=1.3)
        self.hud.bump(self, 7.2)
        self.wait(0.7)

        nxt = VGroup(
            mono("NEXT", size=FS_TINY, color=DIM),
            mono("L04  ·  THE SILHOUETTE", size=FS_H2, color=BOXC, weight="BOLD"),
            tiny("bohat shots ke baad box ka shape nazar aata hai — graph", color=DIM),
        ).arrange(DOWN, buff=0.2).next_to(tool, DOWN, buff=0.7)
        self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(tool), FadeOut(nxt), FadeOut(self.hud), run_time=0.8)


# ──────────────────────────────────────────────────────────── standalone clips


class L03Traps(Scene):
    """Teen domain traps — revision clip."""

    def construct(self):
        apply_theme(self)
        title = h1("Domain ke teen traps").to_edge(UP, buff=0.8)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)

        cases = VGroup(
            domain_case("f(t) = cbrt(2t - 1)", "cube root — koi shart nahi", "(-inf, inf)", w=10.4),
            domain_case("g(t) = sqrt(3-t) - sqrt(2+t)", "dono shartein — AND", "[-2, 3]", w=10.4),
            domain_case(
                "h(x) = 1 / 4throot(x^2 - 5x)", "> 0 — denominator ki wajah se",
                "(-inf, 0) U (5, inf)", w=10.4,
            ),
        ).arrange(DOWN, buff=0.4)
        cases.scale_to_fit_height(5.1).next_to(title, DOWN, buff=0.5)

        for c in cases:
            self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.9)
        self.wait(1.6)


class L03RangeParadox(Scene):
    """Sirf range wala beat — 40s clip."""

    def construct(self):
        apply_theme(self)
        title = VGroup(
            h1("Range endpoints par nahi hoti"),
            mono("f(x) = x^2        domain = [-1, 3]", size=FS_BODY, color=OK),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.75)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)

        static, in_nl, out_nl, trail, link = range_rig(
            self, lambda x: x * x, (-1, 3), (-2, 4), (0, 10), run_time=4.5
        )

        ans = VGroup(
            mono("range = [0, 9]", size=FS_H1, color=OK, weight="BOLD"),
            mono("[1, 9] nahi — kyunki f(0) = 0", size=FS_SMALL, color=BAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ans, shift=UP * 0.2), run_time=0.7)
        self.wait(2.2)


class L03Recap(Scene):
    """50s revision reel."""

    def construct(self):
        apply_theme(self)
        hud = HudBar("L03", "WHERE DOES IT REFUSE?", act=1, decode=7.2)
        self.add(hud)

        rows = VGroup(
            self._row("1.", "domain", "tamam jaiz inputs ka set", OK),
            self._row("2.", "range", "tamam mumkin outputs ka set", WARN),
            self._row("3.", "sirf 2 jurm", "even root me negative, denominator me zero", BAD),
            self._row("4.", "cube root", "har real number qubool — trap", ACCENT),
            self._row("5.", "do shartein", "AND = overlap (intersection), union nahi", ACCENT),
            self._row("6.", "root neeche ho", "to > lagta hai, >= nahi", ACCENT),
            self._row("7.", "[ ] vs ( )", "bhara dot shamil, khokhla dot bahar", BOXC),
            self._row("8.", "range", "endpoints se nahi banti — beech dekho", BAD),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rows.scale_to_fit_height(4.9).next_to(hud, DOWN, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.16),
            run_time=2.6,
        )
        self.wait(1.4)
        ref = book_ref("STEWART  ·  p. 13 Example 6   ·   Ex 39-48")
        self.play(FadeIn(ref), run_time=0.4)
        self.wait(2.0)

    @staticmethod
    def _row(n, head, tail, color):
        return VGroup(
            mono(n, size=FS_SMALL, color=DIM),
            mono(head, size=FS_BODY, color=color, weight="BOLD"),
            body(tail, color=TEXT).scale(0.86),
        ).arrange(RIGHT, buff=0.3)
