"""
THE BLACK BOX · ACT I · LEVEL 02 — NAME THE WIRES

Concept: function notation `f(x)`, independent/dependent variable,
machine diagram (Figure 2), arrow diagram (Figure 3).
Book: Stewart, Early Transcendentals, §1.1, p. 8–9 · Exercises 33–34 (p. 19).

Colab me render:
    !manim -qh --media_dir /content/media \\
        "/content/drive/MyDrive/ch01-black-box/L02_name_the_wires/scene.py" L02Cinematic

Scenes:
    L02Cinematic   — pura level (~3.5 min)
    L02Traps       — sirf notation traps (f(2a) vs 2f(a), f(a^2) vs [f(a)]^2)
    L02Recap       — 45s revision reel

Note: mono text me `^` notation use ki hai (`3a^2`) — superscript glyphs par
depend nahi karte, aur code jaisa look theme ke saath fit hai.
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

# Stewart Ex 1.1.33 ka function — poore level me yehi chalta hai
F_LABEL = "f(x) = 3x^2 - x + 2"


def machine_rig(rule="f", inp="x", out="f(x)", box_w=2.5, box_h=1.75):
    """Figure 2 ka machine diagram: input pill -> box -> output pill.
    Returns (group, box, in_pill, out_pill, arrows)."""
    box = BlackBox(rule, w=box_w, h=box_h)
    p_in = pill(inp, TEXT)
    p_out = pill(out, BOXC)
    p_in.next_to(box, LEFT, buff=1.5)
    p_out.next_to(box, RIGHT, buff=1.5)

    a_in = Arrow(p_in.get_right() + RIGHT * 0.1, box.get_left() + LEFT * 0.1, buff=0,
                 stroke_width=3, max_tip_length_to_length_ratio=0.13, color=DIM)
    a_out = Arrow(box.get_right() + RIGHT * 0.1, p_out.get_left() + LEFT * 0.1, buff=0,
                  stroke_width=3, max_tip_length_to_length_ratio=0.13, color=BOXC)

    g = VGroup(p_in, a_in, box, a_out, p_out)
    return g, box, p_in, p_out, VGroup(a_in, a_out)


def trap_pair(left_label, left_steps, right_label, right_steps, width=11.0):
    """Do expressions ka aamna saamna + beech me ≠ stamp."""
    def line(label, steps, color):
        chip = LabelChip(label, color=color, size=FS_SMALL)
        body_ = mono("   =  " + "  =  ".join(steps), size=FS_SMALL, color=TEXT)
        return VGroup(chip, body_).arrange(RIGHT, buff=0.12)

    top = line(left_label, left_steps, WARN)
    bot = line(right_label, right_steps, ACCENT)
    neq = mono("=/=", size=FS_H2, color=BAD, weight="BOLD")
    stack = VGroup(top, neq, bot).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    neq.align_to(top[0], LEFT).shift(RIGHT * 0.35)
    return VGroup(stack), top, bot, neq


class L02Cinematic(Scene):
    """Pura Level 02."""

    def construct(self):
        apply_theme(self)
        self.hud = HudBar("L02", "NAME THE WIRES", act=1, decode=2.4)

        self.beat_title()
        self.beat_problem()
        self.beat_machine()
        self.beat_f_vs_fx()
        self.beat_variables()
        self.beat_arrow()
        self.beat_situations()
        self.beat_traps()
        self.beat_a_plus_h()
        self.beat_ai()
        self.beat_reward()

    # ─────────────────────────────────────────────────────── helper
    def swap_caption(self, old, text):
        new = caption(text)
        if old is None:
            self.play(FadeIn(new, shift=UP * 0.2), run_time=0.5)
        else:
            self.play(FadeOut(old, shift=DOWN * 0.2), FadeIn(new, shift=UP * 0.2), run_time=0.5)
        return new

    # ─────────────────────────────────────────────────────── beats

    def beat_title(self):
        self.play(FadeIn(self.hud, shift=DOWN * 0.2), run_time=0.7)
        LevelCard(
            act_no=1,
            act_title="FIRST CONTACT",
            level_no=2,
            title="NAME THE WIRES",
            brief="Box honest nikli. Ab usko likhna hai — magar parts ke naam nahi.",
        ).shift(DOWN * 0.25).play_in(self, hold=1.7)

    def beat_problem(self):
        """L01 se jurra hua masla: rule maloom, likhne ka tareeqa nahi."""
        box = BlackBox("HONEST", w=3.0, h=1.9, color=OK).shift(LEFT * 3.4 + DOWN * 0.1)
        tick = mono("L01 clear", size=FS_TINY, color=OK).next_to(box, DOWN, buff=0.3)

        form = panel(5.6, 3.1, fill=PANEL, stroke=LINE).shift(RIGHT * 3.0 + DOWN * 0.1)
        head = mono("LAB MANUAL  ·  FORM 1.1", size=FS_TINY, color=DIM)
        head.next_to(form, UP, buff=0.16).align_to(form, LEFT)
        blanks = VGroup(
            *[
                VGroup(
                    mono(k, size=FS_SMALL, color=DIM),
                    Slot(width=2.0, height=0.44),
                ).arrange(RIGHT, buff=0.3)
                for k in ("machine ka naam", "jo daala jaata hai", "jo nikalta hai")
            ]
        ).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        blanks.move_to(form)

        self.play(FadeIn(box, scale=0.94), FadeIn(tick), run_time=0.7)
        self.play(FadeIn(form), FadeIn(head), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in blanks], lag_ratio=0.2),
                  run_time=1.0)

        cap = self.swap_caption(
            None, "Rule to pata chal gaya — magar isko likhein kaise? Form khaali pari hai."
        )
        self.wait(1.8)
        self.play(FadeOut(VGroup(box, tick, form, head, blanks)), FadeOut(cap), run_time=0.6)

    def beat_machine(self):
        """Figure 2 — machine diagram ke saare parts ke naam."""
        rig, box, p_in, p_out, arrows = machine_rig()
        rig.shift(UP * 0.55)
        self.play(FadeIn(rig, scale=0.95), run_time=0.9)

        # teeno slots ek hi line par — warna pill aur box ki heights ka farq
        # nazar aata hai aur diagram tirchha lagta hai
        slot_y = box.get_bottom()[1] - 1.05
        slots = VGroup(Slot(width=2.3), Slot(width=2.3), Slot(width=2.3))
        for s, m in zip(slots, (p_in, box, p_out)):
            s.move_to([m.get_x(), slot_y, 0])
        ties = VGroup(
            *[
                DashedLine(m.get_bottom(), s.get_top(), stroke_color=LINE, stroke_width=1.6)
                for m, s in zip((p_in, box, p_out), slots)
            ]
        )
        self.play(LaggedStart(*[FadeIn(s) for s in slots], lag_ratio=0.2),
                  LaggedStart(*[Create(t) for t in ties], lag_ratio=0.2), run_time=1.0)

        cap = self.swap_caption(None, "Teen parts, teen naam. LABEL GUN load ho rahi hai . . .")

        chips = [
            LabelChip("INPUT", color=OK, size=FS_SMALL),
            LabelChip("RULE  f", color=BOXC, size=FS_SMALL),
            LabelChip("OUTPUT  f(x)", color=WARN, size=FS_SMALL),
        ]
        colors = [OK, BOXC, WARN]
        for chip, slot, c in zip(chips, slots, colors):
            self.play(slot.fill_with(chip, color=c), run_time=0.6)
            self.add(chip)
        self.wait(0.8)

        eq = kbd("output = f(input)").next_to(slots, DOWN, buff=0.7)
        self.play(FadeIn(eq, shift=UP * 0.2), run_time=0.6)
        cap = self.swap_caption(cap, "Bas itna: jo nikla, woh 'f of input'. Isi ko f(x) likhte hain.")
        self.wait(1.8)

        self.play(
            FadeOut(VGroup(rig, slots, ties, eq, *chips)), FadeOut(cap), run_time=0.6
        )

    def beat_f_vs_fx(self):
        """Level ka core farq — f machine ka naam, f(x) uska output."""
        title = h2("Sabse bara confusion").to_edge(UP, buff=1.35)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)

        def side(sym, what, note, color):
            big = mono(sym, size=FS_TITLE, color=color, weight="BOLD")
            w = mono(what, size=FS_SMALL, color=TEXT)
            n = tiny(note, color=DIM)
            inner = VGroup(big, w, n).arrange(DOWN, buff=0.28)
            card = panel(inner.width + 1.3, inner.height + 1.0, stroke=color, radius=0.14)
            card.set_stroke(opacity=0.55)
            inner.move_to(card)
            return VGroup(card, inner)

        left = side("f", "machine ka NAAM", "ek rule / ek function", BOXC)
        right = side("f(x)", "us machine ka OUTPUT", "ek number, x par", WARN)
        pair = VGroup(left, right).arrange(RIGHT, buff=1.0).next_to(title, DOWN, buff=0.7)

        self.play(FadeIn(left, shift=RIGHT * 0.3), run_time=0.6)
        self.play(FadeIn(right, shift=LEFT * 0.3), run_time=0.6)
        self.wait(1.2)

        bad_line = VGroup(
            mono("f = 3x^2 - x + 2", size=FS_BODY, color=BAD),
            mono("X  sust likhai", size=FS_TINY, color=BAD),
        ).arrange(RIGHT, buff=0.5)
        ok_line = VGroup(
            mono(F_LABEL, size=FS_BODY, color=OK),
            mono("OK  yeh theek hai", size=FS_TINY, color=OK),
        ).arrange(RIGHT, buff=0.5)
        rows = VGroup(bad_line, ok_line).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        rows.next_to(pair, DOWN, buff=0.75)

        self.play(FadeIn(bad_line, shift=UP * 0.2), run_time=0.5)
        self.play(Indicate(bad_line, color=BAD, scale_factor=1.03), run_time=0.7)
        self.play(FadeIn(ok_line, shift=UP * 0.2), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(VGroup(title, pair, rows)), run_time=0.5)

    def beat_variables(self):
        """Independent vs dependent — Stewart ka Example A."""
        rig, box, p_in, p_out, _ = machine_rig(rule="f", inp="r", out="A")
        rig.shift(UP * 0.7)
        formula = kbd("A = f(r) = pi r^2").next_to(rig, DOWN, buff=0.9)

        self.play(FadeIn(rig, scale=0.95), run_time=0.7)
        self.play(FadeIn(formula, shift=UP * 0.2), run_time=0.5)

        left_tag = VGroup(
            LabelChip("r  ·  INDEPENDENT", color=OK, size=FS_TINY),
            tiny("jo hum chunte hain", color=DIM),
        ).arrange(DOWN, buff=0.16)
        right_tag = VGroup(
            LabelChip("A  ·  DEPENDENT", color=WARN, size=FS_TINY),
            tiny("jo khud tay ho jaata hai", color=DIM),
        ).arrange(DOWN, buff=0.16)
        left_tag.next_to(p_in, UP, buff=0.55)
        right_tag.next_to(p_out, UP, buff=0.55)

        self.play(FadeIn(left_tag, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(right_tag, shift=DOWN * 0.2), run_time=0.5)

        cap = self.swap_caption(
            None, "Radius aap chunte hain — area us par depend karta hai. Ulta likhna galat hoga."
        )
        self.wait(2.0)
        self.play(FadeOut(VGroup(rig, formula, left_tag, right_tag)), FadeOut(cap), run_time=0.6)

    def beat_arrow(self):
        """Figure 3 — arrow diagram, doosra naqsha."""
        title = h2("Doosra naqsha: arrow diagram").to_edge(UP, buff=1.35)
        ad = ArrowDiagram(
            [(0, 0), (1, 1), (2, 2)],
            n_in=3,
            n_out=3,
            in_labels=["x", "a", "4"],
            out_labels=["f(x)", "f(a)", "f(4)"],
            color=BOXC,
            h=2.7,
            gap=3.4,
        ).scale(1.05).next_to(title, DOWN, buff=0.65)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(ad, scale=0.94), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in ad.arrows], lag_ratio=0.3), run_time=1.2)

        note = body("D = domain (tamam jaiz inputs)     E = outputs ka set", color=DIM)
        note.next_to(ad, DOWN, buff=0.55)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.2)

        cap = self.swap_caption(
            None, "L01 ka imtihaan yahan ek nazar me: kisi ek dot se DO teer nahi nikalne chahiye."
        )
        self.play(Circumscribe(ad.in_dots, color=OK, buff=0.18), run_time=1.2)
        self.wait(1.4)
        self.play(FadeOut(VGroup(title, ad, note)), FadeOut(cap), run_time=0.6)

    def beat_situations(self):
        """Stewart ke chaar asli examples (p. 8) — notation practice."""
        title = h2("Stewart ke chaar examples — sab ek hi shakal me").to_edge(UP, buff=1.3)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)

        data = [
            ("A", "circle ka area, radius se", "A = f(r) = pi r^2", "r  ->  A", OK),
            ("B", "duniya ki aabadi, waqt se", "P = f(t)", "t  ->  P", BOXC),
            ("C", "envelope ka postage, wazan se", "C = f(w)", "w  ->  C", WARN),
            ("D", "zameen ka acceleration, waqt se", "a = f(t)", "t  ->  a", ACCENT),
        ]
        # columns ko fixed x par rakha hai — arrange() se cells line me nahi aate
        COL_TAG, COL_DESC, COL_NOT, COL_ARR = -6.1, -5.6, 1.0, 4.8
        y0 = title.get_bottom()[1] - 0.75
        rows = VGroup()
        for i, (tag, desc, notation, arrow) in enumerate([d[:4] for d in data]):
            c = data[i][4]
            y = y0 - i * 0.62
            cells = VGroup(
                mono(tag, size=FS_SMALL, color=c, weight="BOLD").move_to([COL_TAG, y, 0]),
                body(desc, color=TEXT).scale(0.8).move_to([COL_DESC, y, 0], aligned_edge=LEFT),
                mono(notation, size=FS_SMALL, color=c).move_to([COL_NOT, y, 0], aligned_edge=LEFT),
                mono(arrow, size=FS_TINY, color=DIM).move_to([COL_ARR, y, 0], aligned_edge=LEFT),
            )
            rows.add(cells)

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in rows], lag_ratio=0.22),
                  run_time=1.6)
        self.wait(1.4)

        cap = self.swap_caption(
            None, "Sirf A me formula hai. B table hai, C rule-book, D graph — chaaron phir bhi functions."
        )
        self.wait(2.2)
        self.play(FadeOut(VGroup(title, rows)), FadeOut(cap), run_time=0.6)

    def beat_traps(self):
        """Level ka boss beat — notation ke do classic dhoke."""
        head = VGroup(
            h2("Notation ke do dhoke"),
            mono(F_LABEL, size=FS_BODY, color=OK),
        ).arrange(DOWN, buff=0.24).to_edge(UP, buff=1.25)
        self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.6)

        # ── dhoka 1: f(2a) vs 2f(a)
        g1, top1, bot1, neq1 = trap_pair(
            "f(2a)", ["3(2a)^2 - (2a) + 2", "12a^2 - 2a + 2"],
            "2f(a)", ["2(3a^2 - a + 2)", "6a^2 - 2a + 4"],
        )
        g1.scale_to_fit_width(11.4).next_to(head, DOWN, buff=0.8)
        self.play(FadeIn(top1, shift=RIGHT * 0.25), run_time=0.7)
        self.play(FadeIn(bot1, shift=RIGHT * 0.25), run_time=0.7)
        self.wait(0.7)
        self.play(FadeIn(neq1, scale=0.7), Flash(neq1.get_center(), color=BAD,
                                                 line_length=0.22, num_lines=14, flash_radius=0.9),
                  run_time=0.8)
        cap = self.swap_caption(
            None, "f(2a): input ko doguna karo.  2f(a): output ko doguna karo. Do alag kaam."
        )
        self.wait(2.4)
        self.play(FadeOut(g1), run_time=0.5)

        # ── dhoka 2: f(a^2) vs [f(a)]^2
        g2, top2, bot2, neq2 = trap_pair(
            "f(a^2)", ["3(a^2)^2 - (a^2) + 2", "3a^4 - a^2 + 2"],
            "[f(a)]^2", ["(3a^2 - a + 2)^2", "9a^4 - 6a^3 + 13a^2 - 4a + 4"],
        )
        g2.scale_to_fit_width(11.4).next_to(head, DOWN, buff=0.8)
        self.play(FadeIn(top2, shift=RIGHT * 0.25), run_time=0.7)
        self.play(FadeIn(bot2, shift=RIGHT * 0.25), run_time=0.7)
        self.play(FadeIn(neq2, scale=0.7), run_time=0.6)
        cap = self.swap_caption(
            cap, "f(a^2): pehle square, phir machine.  [f(a)]^2: pehle machine, phir square."
        )
        self.wait(2.4)

        rule = InfoCard(
            "QAIDA",
            "Bracket ke ANDAR jo hai — woh INPUT hai.\n"
            "Bracket ke BAHAR jo hai — woh OUTPUT par lagta hai.",
            t2c={"ANDAR": OK, "INPUT": OK, "BAHAR": WARN, "OUTPUT": WARN},
            width=9.4,
        ).next_to(g2, DOWN, buff=0.7)
        self.play(FadeIn(rule, shift=UP * 0.2), run_time=0.7)
        self.wait(2.4)
        self.play(FadeOut(VGroup(head, g2, rule)), FadeOut(cap), run_time=0.6)

    def beat_a_plus_h(self):
        """L10 ka pul — f(a+h)."""
        title = h2("Aur ek notation jo aage bohat kaam aayegi").to_edge(UP, buff=1.35)
        steps = VGroup(
            mono("f(a + h)", size=FS_H2, color=WARN),
            mono("= 3(a + h)^2 - (a + h) + 2", size=FS_BODY, color=TEXT),
            mono("= 3a^2 + 6ah + 3h^2 - a - h + 2", size=FS_BODY, color=OK),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        steps.next_to(title, DOWN, buff=0.8)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        for s in steps:
            self.play(FadeIn(s, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.0)

        teaser = VGroup(
            mono("[ f(a+h) - f(a) ] / h", size=FS_H2, color=ACCENT),
            tiny("difference quotient  ·  L10 ka boss  ·  aur Chapter 2 ka darwaza", color=DIM),
        ).arrange(DOWN, buff=0.24).next_to(steps, DOWN, buff=0.85)
        self.play(FadeIn(teaser, scale=0.94), run_time=0.8)
        ref = book_ref("STEWART  ·  Ex 1.1.33-38  p. 19")
        self.play(FadeIn(ref), run_time=0.4)
        self.wait(2.2)
        self.play(FadeOut(VGroup(title, steps, teaser)), FadeOut(ref), run_time=0.6)

    def beat_ai(self):
        card = InfoCard(
            "AI CONNECTION",
            "def f(x): return 3*x**2 - x + 2\n"
            "\n"
            "f        ->  function object   (naam)\n"
            "f(3)     ->  26                (output)\n"
            "\n"
            "f: float -> float   yeh type hint hi domain -> range hai.\n"
            "model aur model(x) ka farq bhi bilkul yehi hai.",
            t2c={"function object": BOXC, "26": WARN, "domain -> range": OK},
            width=10.6,
        )
        self.play(FadeIn(card, shift=UP * 0.25), run_time=0.8)
        self.wait(3.4)
        self.play(FadeOut(card), run_time=0.5)

    def beat_reward(self):
        tool = ToolCard(
            "LABEL GUN",
            "Kisi bhi situation ko output = f(input) me likhna.\n"
            "Aage lagta hai: L10 (word problem), L25 (composition).",
            icon=tag_icon(),
        ).shift(UP * 0.3)
        self.add(self.hud)
        tool.play_in(self, hold=1.2)
        self.hud.bump(self, 4.8)
        self.wait(0.7)

        nxt = VGroup(
            mono("NEXT", size=FS_TINY, color=DIM),
            mono("L03  ·  WHERE DOES IT REFUSE?", size=FS_H2, color=BOXC, weight="BOLD"),
            tiny("box har number qubool nahi karti — domain aur range", color=DIM),
        ).arrange(DOWN, buff=0.2).next_to(tool, DOWN, buff=0.7)
        self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(tool), FadeOut(nxt), FadeOut(self.hud), run_time=0.8)


class L02Traps(Scene):
    """Standalone clip: f(2a) vs 2f(a), f(a^2) vs [f(a)]^2."""

    def construct(self):
        apply_theme(self)
        head = VGroup(
            h1("Bracket ke andar = input"),
            mono(F_LABEL, size=FS_BODY, color=OK),
        ).arrange(DOWN, buff=0.26).to_edge(UP, buff=0.8)
        self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.6)

        pairs = [
            ("f(2a)", ["12a^2 - 2a + 2"], "2f(a)", ["6a^2 - 2a + 4"]),
            ("f(a^2)", ["3a^4 - a^2 + 2"], "[f(a)]^2", ["9a^4 - 6a^3 + 13a^2 - 4a + 4"]),
        ]
        groups = VGroup()
        for pl, ls, pr, rs in pairs:
            g, _, _, _ = trap_pair(pl, ls, pr, rs)
            groups.add(g)
        groups.arrange(DOWN, buff=0.9)
        groups.scale_to_fit_width(11.0).next_to(head, DOWN, buff=0.8)

        for g in groups:
            self.play(FadeIn(g, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.8)
        self.wait(1.6)


class L02Recap(Scene):
    """45s revision reel."""

    def construct(self):
        apply_theme(self)
        hud = HudBar("L02", "NAME THE WIRES", act=1, decode=4.8)
        self.add(hud)

        rows = VGroup(
            self._row("1.", "f", "machine ka naam (rule)", BOXC),
            self._row("2.", "f(x)", "us machine ka output — ek number", WARN),
            self._row("3.", "independent", "jo hum chunte hain (input ka symbol)", OK),
            self._row("4.", "dependent", "jo khud tay hota hai (output ka symbol)", OK),
            self._row("5.", "f(2a) =/= 2f(a)", "bracket ke andar = input", BAD),
            self._row("6.", "f(a^2) =/= [f(a)]^2", "bracket ke bahar = output par", BAD),
        ).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows.next_to(hud, DOWN, buff=0.65)

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.2),
                  run_time=2.4)
        self.wait(1.4)
        ref = book_ref("STEWART  ·  §1.1  p. 8-9  ·  Ex 33-34")
        self.play(FadeIn(ref), run_time=0.4)
        self.wait(2.0)

    @staticmethod
    def _row(n, head, tail, color):
        return VGroup(
            mono(n, size=FS_SMALL, color=DIM),
            mono(head, size=FS_BODY, color=color, weight="BOLD"),
            body(tail, color=TEXT).scale(0.9),
        ).arrange(RIGHT, buff=0.3)
