"""
THE BLACK BOX · ACT I · LEVEL 01 — IS IT HONEST?

Concept: function ki definition — har input ke liye **exactly one** output.
Book: Stewart, Early Transcendentals, §1.1, p. 8–9 (+ Figures 2 aur 3).

Colab me render:
    !manim -qh --media_dir /content/media \\
        "/content/drive/MyDrive/ch01-black-box/L01_is_it_honest/scene.py" L01Cinematic

Scenes:
    L01Cinematic   — pura level (~3 min)
    L01Recap       — 40s revision reel
    L01Myths       — sirf "many→1 vs 1→many" panel (standalone clip)

Koi LaTeX nahi — sab Pango Text hai, is liye Colab par `pip install manim` kaafi hai.
"""

import sys
from pathlib import Path

# ── shared/ ko path me lao (Colab aur local, dono me chalta hai) ──────────
_HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
for _cand in (_HERE.parent / "shared", _HERE / "shared", Path("shared"), Path("../shared")):
    if (_cand / "hud.py").exists():
        sys.path.insert(0, str(_cand))
        break

from manim import *  # noqa: E402

from theme import *  # noqa: E402,F403
from hud import *  # noqa: E402,F403

# ── level ka data — story aur math ek jagah ──────────────────────────────
BASE_FARE, PER_KM = 80, 70


def fare(d, surge=1.0):
    return int(round((BASE_FARE + PER_KM * d) * surge / 5.0) * 5)


def myth_panel(pairs, n_in, n_out, label, note, ok):
    """Ek chhota arrow-diagram card: jaiz naqsha ya najaiz. L01Cinematic aur
    L01Myths dono isi ko use karte hain."""
    c = OK if ok else BAD
    ad = ArrowDiagram(pairs, n_in=n_in, n_out=n_out, color=c, h=1.9, gap=2.4)
    tag = mono(label, size=FS_SMALL, color=c)
    sub = tiny(note, color=DIM)
    stamp = mono("FUNCTION" if ok else "NOT A FUNCTION", size=FS_TINY, color=c, weight="BOLD")
    inner = VGroup(tag, ad, sub, stamp).arrange(DOWN, buff=0.26)
    card = panel(inner.width + 0.7, inner.height + 0.7, stroke=c, radius=0.14)
    card.set_stroke(opacity=0.5)
    inner.move_to(card)
    return VGroup(card, inner)


def myth_row():
    return VGroup(
        myth_panel([(0, 0), (1, 1)], 2, 2, "1  →  1", "har input ka apna output", True),
        myth_panel([(0, 0), (1, 0)], 2, 1, "many  →  1", "do inputs, ek hi output", True),
        myth_panel([(0, 0), (0, 1)], 1, 2, "1  →  many", "ek input, do outputs", False),
    ).arrange(RIGHT, buff=0.75, aligned_edge=UP)


class L01Cinematic(Scene):
    """Pura Level 01."""

    def construct(self):
        apply_theme(self)
        self.hud = HudBar("L01", "IS IT HONEST?", act=1, decode=0)

        self.beat_title()
        self.beat_arrival()
        self.beat_probe()
        self.beat_glitch()
        self.beat_one_to_many()
        self.beat_definition()
        self.beat_myths()
        self.beat_repair()
        self.beat_ai()
        self.beat_reward()

    # ─────────────────────────────────────────────────────── helpers

    def fire(self, box, log, inp, out, status, color=TEXT, keep=False):
        """Ek probe shot + log row. `keep=True` pe shot screen par reh jaata hai."""
        shot = Shot(box, inp, buff=0.95)
        self.play(FadeIn(shot.pill, shift=RIGHT * 0.2), run_time=0.32)
        shot.fire(self, out, out_color=color)
        log.add_row(self, inp, out, status, color=color)
        if not keep:
            self.play(FadeOut(shot), run_time=0.28)
        return shot

    def swap_caption(self, old, text):
        new = caption(text)
        if old is None:
            self.play(FadeIn(new, shift=UP * 0.2), run_time=0.5)
        else:
            self.play(FadeOut(old, shift=DOWN * 0.2), FadeIn(new, shift=UP * 0.2), run_time=0.5)
        return new

    # ─────────────────────────────────────────────────────── beats

    def beat_title(self):
        self.play(FadeIn(self.hud, shift=DOWN * 0.2), run_time=0.8)
        card = LevelCard(
            act_no=1,
            act_title="FIRST CONTACT",
            level_no=1,
            title="IS IT HONEST?",
            brief="Ek sealed machine. Sirf input daal sakte hain, andar dekh nahi sakte.",
        ).shift(DOWN * 0.25)
        card.play_in(self, hold=1.8)

    def beat_arrival(self):
        self.box = BlackBox("? ? ?").shift(DOWN * 0.2)
        serial = mono("SALVAGE UNIT  ·  CH-01", size=FS_TINY, color=DIM)
        serial.next_to(self.box, DOWN, buff=0.34)

        self.play(FadeIn(self.box, scale=0.9), run_time=1.0)
        self.play(self.box.pulse(), FadeIn(serial), run_time=0.7)

        cap = self.swap_caption(
            None, "Box seal-band hai. Do cheezein khuli hain: ek input port, ek output port."
        )
        self.wait(1.4)
        self.play(FadeOut(serial), FadeOut(cap), run_time=0.4)

    def beat_probe(self):
        """Shots fire karo, log banao — pehle 3 shots honest."""
        self.play(self.box.animate.move_to(LEFT * 2.85 + DOWN * 0.25), run_time=0.8)

        self.log = LogTable("PROBE LOG  ·  SHOTS", rows_max=4)
        self.log.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        self.play(FadeIn(self.log, shift=LEFT * 0.3), run_time=0.7)

        units = mono("input = distance (km)     output = fare (Rs)", size=FS_TINY, color=DIM)
        units.next_to(self.box, DOWN, buff=0.9)
        self.play(FadeIn(units), run_time=0.4)

        cap = self.swap_caption(None, "Shot 1 — 4.2 km daala.")
        self.fire(self.box, self.log, "4.2", str(fare(4.2)), "logged", color=TEXT)

        cap = self.swap_caption(cap, "Shot 2 — wahi 4.2 dobara. Kya wahi jawab aayega?")
        self.fire(self.box, self.log, "4.2", str(fare(4.2)), "same  ok", color=OK)
        self.play(self.box.go_good(), run_time=0.5)

        cap = self.swap_caption(cap, "Shot 3 — naya input 7.1. Box consistent lag rahi hai.")
        self.fire(self.box, self.log, "7.1", str(fare(7.1)), "logged", color=OK)
        self.wait(0.6)

        self.units, self.cap = units, cap

    def beat_glitch(self):
        """Chautha shot — wahi input, doosra output."""
        cap = self.swap_caption(self.cap, "Shot 4 — phir wahi 4.2 . . .")
        self.play(self.box.reset_color(), run_time=0.3)
        shot = self.fire(self.box, self.log, "4.2", "700", "CONFLICT", color=BAD, keep=True)

        self.play(self.box.go_bad(), run_time=0.4)
        self.box.shake(self)
        self.play(
            Circumscribe(self.log.rows[0], color=BAD, buff=0.07),
            Circumscribe(self.log.rows[3], color=BAD, buff=0.07),
            run_time=1.4,
        )

        self.play(FadeOut(cap), FadeOut(self.units), run_time=0.35)
        banner = GlitchBanner(
            "Ek hi input 4.2 — do mukhtalif output: 380 aur 700.\nTo yeh box kis rule pe chal rahi hai?",
            width=9.0,
        ).to_edge(DOWN, buff=0.45)
        banner.play_in(self)
        self.wait(2.0)

        self.play(
            FadeOut(banner), FadeOut(shot), FadeOut(self.log), FadeOut(self.box), run_time=0.6
        )

    def beat_one_to_many(self):
        """Glitch ko arrow diagram me — asal masla saaf dikhta hai."""
        ad = ArrowDiagram(
            [(0, 0), (0, 1)],
            n_in=1,
            n_out=2,
            in_labels=["4.2"],
            out_labels=["380", "700"],
            color=BAD,
        ).scale(1.15).shift(UP * 0.35)

        self.play(FadeIn(ad, scale=0.92), run_time=0.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in ad.arrows], lag_ratio=0.35), run_time=1.1)

        v = verdict("NOT A FUNCTION", ok=False).next_to(ad, DOWN, buff=0.75)
        self.play(FadeIn(v, shift=UP * 0.25), run_time=0.6)
        cap = self.swap_caption(None, "Ek input se do teer nikal rahe hain — yahin rule toot gaya.")
        self.wait(2.0)
        self.play(FadeOut(ad), FadeOut(v), FadeOut(cap), run_time=0.5)

    def beat_definition(self):
        """Ab definition — sawaal ke baad, is liye ab boring nahi."""
        card = InfoCard(
            "DEFINITION  ·  STEWART §1.1",
            "A function f is a rule that assigns to each element x\n"
            "in a set D exactly one element f(x) in a set E.",
            t2c={"exactly one": WARN, "rule": BOXC, "each element x": OK},
            width=10.4,
        ).shift(UP * 0.5)
        ref = book_ref("STEWART  ·  p. 8")

        self.play(FadeIn(card, shift=UP * 0.25), FadeIn(ref), run_time=0.9)
        self.wait(1.2)
        self.play(Indicate(card.para, color=WARN, scale_factor=1.04), run_time=1.0)

        note = VGroup(
            mono("exactly one", size=FS_H2, color=WARN),
            body("= poori definition ka wazan in do lafzon par hai.", color=DIM),
        ).arrange(RIGHT, buff=0.35)
        note.next_to(card, DOWN, buff=0.85)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.6)
        self.wait(2.2)
        self.play(FadeOut(card), FadeOut(note), FadeOut(ref), run_time=0.5)

    def beat_myths(self):
        """Sabse bara ghalat-fehmi wala panel."""
        title = h2("Kaun sa naqsha jaiz hai?").to_edge(UP, buff=1.35)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)

        panels = myth_row().scale_to_fit_width(12.4).next_to(title, DOWN, buff=0.55)

        for p in panels:
            self.play(FadeIn(p, shift=UP * 0.2), run_time=0.55)
        self.wait(1.0)

        self.play(Circumscribe(panels[1], color=OK, buff=0.12), run_time=1.2)
        cap = self.swap_caption(
            None, "Yaad rakhein: mukhtalif inputs ka ek hi output ho — yeh bilkul jaiz hai."
        )
        self.wait(1.8)
        cap = self.swap_caption(cap, "Mana sirf ek cheez hai: EK input ke DO output.")
        self.play(Circumscribe(panels[2], color=BAD, buff=0.12), run_time=1.2)
        self.wait(1.6)
        self.play(FadeOut(panels), FadeOut(title), FadeOut(cap), run_time=0.5)

    def beat_repair(self):
        """Box jhooti nahi thi — hamara input adhoora tha."""
        box = BlackBox("? ? ?", w=3.0, h=2.3).shift(RIGHT * 0.4 + UP * 0.35)
        self.play(FadeIn(box, scale=0.94), run_time=0.6)

        p_dist = pill("4.2", TEXT).next_to(box, LEFT, buff=1.5).shift(UP * 0.45)
        p_surge = pill("surge 1.85", WARN, size=FS_SMALL).next_to(box, LEFT, buff=1.5).shift(DOWN * 0.5)
        a1 = Arrow(p_dist.get_right(), box.get_left() + UP * 0.45, buff=0.12, stroke_width=3,
                   max_tip_length_to_length_ratio=0.13, color=DIM)
        a2 = Arrow(p_surge.get_right(), box.get_left() + DOWN * 0.5, buff=0.12, stroke_width=3,
                   max_tip_length_to_length_ratio=0.13, color=WARN)

        self.play(LaggedStart(FadeIn(p_dist), FadeIn(p_surge), lag_ratio=0.3), run_time=0.7)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.play(box.pulse(), run_time=0.5)

        out = pill("700", OK).next_to(box, RIGHT, buff=1.3)
        a3 = Arrow(box.get_right(), out.get_left(), buff=0.12, stroke_width=3,
                   max_tip_length_to_length_ratio=0.13, color=OK)
        self.play(GrowArrow(a3), FadeIn(out, shift=RIGHT * 0.2), run_time=0.5)
        # relabel aur go_good alag plays me — warna naya tag ek hi play me
        # do animations me aa jaata hai (Manim "mobject animated twice" warning)
        self.play(box.relabel("fare = (80 + 70d) × s", color=OK), run_time=0.7)
        self.play(box.go_good(), run_time=0.5)

        cap = self.swap_caption(
            None, "Box jhooti nahi thi — hamara input adhoora tha. Ek chhupa hua input bhi chal raha tha."
        )
        self.wait(2.0)
        cap = self.swap_caption(
            cap, "fare, sirf distance ka function nahi hai — (distance, surge) ka function hai."
        )
        self.wait(2.2)
        self.play(
            FadeOut(VGroup(box, p_dist, p_surge, a1, a2, a3, out)), FadeOut(cap), run_time=0.6
        )

    def beat_ai(self):
        card = InfoCard(
            "AI CONNECTION",
            "model(x)  →  same x, same y        yeh ek function hai\n"
            "LLM(prompt, temperature=0.8)       har baar naya jawab\n"
            "\n"
            "Isi liye reproducibility ke liye seed fix karte hain —\n"
            "warna aapka model bhi Level 01 ki surge box jaisa hai.",
            t2c={
                "same x, same y": OK,
                "yeh ek function hai": OK,
                "har baar naya jawab": BAD,
                "seed fix": WARN,
            },
            width=10.6,
        )
        self.play(FadeIn(card, shift=UP * 0.25), run_time=0.8)
        self.wait(3.2)
        self.play(FadeOut(card), run_time=0.5)

    def beat_reward(self):
        tool = ToolCard(
            "PROBE",
            "Box par input fire karke output log karna.\nAge ke levels me: L03 domain, L04 graph, L13 fitting.",
            icon=magnifier_icon(),
        ).shift(UP * 0.3)
        self.add(self.hud)
        tool.play_in(self, hold=1.2)
        self.hud.bump(self, 2)
        self.wait(0.8)

        nxt = VGroup(
            mono("NEXT", size=FS_TINY, color=DIM),
            mono("L02  ·  NAME THE WIRES", size=FS_H2, color=BOXC, weight="BOLD"),
            tiny("machine diagram, arrow diagram, aur f(x) notation", color=DIM),
        ).arrange(DOWN, buff=0.2)
        nxt.next_to(tool, DOWN, buff=0.7)
        self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(tool), FadeOut(nxt), FadeOut(self.hud), run_time=0.8)


class L01Myths(Scene):
    """Standalone clip: many→1 jaiz hai, 1→many nahi. Revision ke liye."""

    def construct(self):
        apply_theme(self)
        title = h1("Function ka asli imtihaan").to_edge(UP, buff=0.7)
        panels = myth_row().scale_to_fit_width(12.4).next_to(title, DOWN, buff=0.7)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.25) for p in panels], lag_ratio=0.25), run_time=1.4)
        self.play(Circumscribe(panels[1], color=OK, buff=0.12), run_time=1.1)
        self.play(Circumscribe(panels[2], color=BAD, buff=0.12), run_time=1.1)
        self.wait(1.6)


class L01Recap(Scene):
    """40s revision reel — level ka nichor."""

    def construct(self):
        apply_theme(self)
        hud = HudBar("L01", "IS IT HONEST?", act=1, decode=2)
        self.add(hud)

        rows = VGroup(
            self._row("1.", "Function = rule", "har input ko EXACTLY ONE output", OK),
            self._row("2.", "1 input → 2 output", "function nahi (Level 01 ki surge box)", BAD),
            self._row("3.", "2 input → 1 output", "bilkul function hai", OK),
            self._row("4.", "Notation", "output = f(input),  jaise  fare = f(distance)", BOXC),
            self._row("5.", "Reality check", "adhoora input mile to rule galat lagta hai", WARN),
        ).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        rows.next_to(hud, DOWN, buff=0.7)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.22), run_time=2.2
        )
        self.wait(1.4)
        ref = book_ref("STEWART  ·  §1.1  p. 8-9")
        self.play(FadeIn(ref), run_time=0.4)
        self.wait(2.0)

    @staticmethod
    def _row(n, head, tail, color):
        return VGroup(
            mono(n, size=FS_SMALL, color=DIM),
            mono(head, size=FS_BODY, color=color, weight="BOLD"),
            body(tail, color=TEXT),
        ).arrange(RIGHT, buff=0.3)
