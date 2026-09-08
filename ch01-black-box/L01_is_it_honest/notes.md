# L01 — IS IT HONEST?
### ACT I · FIRST CONTACT · Stewart §1.1, p. 8–9 · TOOL: `PROBE`

> Pehle `play.html` khelein, phir `L01Cinematic` dekhein, **uske baad** yeh notes.
> Order ulta karne se maza aur samajh dono kam ho jaate hain.

---

## 1. Aapne khud kya dhoonda

| Game me | Math me |
|---|---|
| Box A: same input, hamesha same output | **function** |
| Box B: same input, do output | function **nahi** |
| BOX-19: teen inputs, ek hi output | function **hai** (jaiz) |
| BOX-23: kuch inputs reject | function **hai**, bas domain chhoti hai |
| BOX-31: dice engine | function nahi (randomness) |
| Box B repaired: `(d, s)` se output fix | adhoora input tha, rule nahi |

---

## 2. Definition — ab padhne ka waqt

Stewart, p. 8:

> **A function _f_ is a rule that assigns to each element _x_ in a set _D_
> exactly one element _f(x)_ in a set _E_.**

Teen lafz jo poori definition ka wazan uthate hain:

| Lafz | Game me kya tha |
|---|---|
| **rule** | box ke andar ki machine |
| **each element x** | har input jo box qubool karti hai |
| **exactly one** | Box B yahin fail hui |

### Terminology (p. 8–9)

| Naam | Matlab | L01 me |
|---|---|---|
| **domain** `D` | tamam jaiz inputs ka set | qubool shuda distances |
| **range** | tamam mumkin outputs ka set | tamam mumkin fares |
| **independent variable** | input ka symbol | `d` (distance) |
| **dependent variable** | output ka symbol | fare — `d` par depend karta hai |
| **value of f at x** | `f(x)` | `f(4.2) = 380` |

Notation: `fare = f(distance)`, ya chhota kar ke `y = f(x)`.
`f` machine ka **naam** hai, `f(x)` us machine ka **output** hai.
Yeh farq L02 me tool ban jaayega.

### Stewart ke chaar asli examples (p. 8)

| | Situation | Function notation |
|---|---|---|
| A | circle ka area, radius se | `A = f(r) = πr²` |
| B | duniya ki aabadi, waqt se | `P = f(t)` — formula nahi, table hai |
| C | envelope ka postage, wazan se | `C = f(w)` — post office ka rule |
| D | zameen ka acceleration, waqt se (seismograph) | `a = f(t)` — sirf graph hai |

Ghor karein: **sirf A me formula hai.** B table hai, C rule-book hai, D graph hai.
Chaaron phir bhi function hain — kyunki har ek me har input ka exactly ek output hai.
Yeh nukta L06 (four representations) ka poora level ban jaayega.

---

## 3. Do trap — aur khud Stewart ne yeh trap lagaya hai

Yeh dono cheezein log rozana ghalat karte hain. Interesting baat: book ke exercises
me **bilkul wohi do tables** hain jo aapke game me BOX-19 aur BOX-23 the.

### Trap 1 — "many → one" bilkul jaiz hai

**Ex 1.1.14 (p. 18)** — Year → Tuition cost:

| Year | Tuition |
|---|---|
| 2016 | 10,900 |
| 2017 | 11,000 |
| 2018 | **11,200** |
| 2019 | **11,200** |
| 2020 | 11,300 |

Do saal ka ek hi cost. **Yeh function hai.** Definition kehti hai
"each _x_ has exactly one _f(x)_" — yeh kahin nahi kehti ke "har output ka apna
akela input ho". Woh ulta sawaal (`one-to-one`) **L33 — THE TWIN TRAP** me aayega,
jab inverse banana hoga. Abhi uski zaroorat nahi.

### Trap 2 — "1 → 2" hi asal maut hai

**Ex 1.1.13 (p. 18)** — Height → Shoe size:

| Height (in) | Shoe size |
|---|---|
| 72 | 12 |
| **60** | **8** |
| **60** | **7** |
| 63 | 9 |
| 70 | 10 |

Height 60 ke do shoe sizes. **Function nahi** — bilkul aapki Box B jaisa.

Aur ek: **Table 4 (p. 13)** — wahan `x = 5` ke do outputs hain, `y = 7` aur `y = 8`.
Stewart khud likhte hain: *"Table 4 does not define y as a function of x."*
Yani book teen jagah aap ka Box B dohraati hai.

### Trap 3 — reject karna ≠ jhoot bolna

BOX-23 kuch inputs pe `ERROR` deti thi. Woh phir bhi function hai — uski
**domain chhoti** hai. `√x` sirf `x ≥ 0` leta hai; `1/x` sirf `x ≠ 0`.
Domain ka pura level: **L03 — WHERE DOES IT REFUSE?**

---

## 4. Machine aur arrow — do tasveerein (p. 9)

**Machine diagram** (Figure 2) — bilkul aapka probe rig:

```
   x  ──────▶ [  f  ] ──────▶  f(x)
 (input)                     (output)
```

**Arrow diagram** (Figure 3) — D se E tak teer:

```
      D                    E
   ┌───────┐           ┌───────┐
   │  x ●──┼───────────┼──▶ ● f(x)
   │  a ●──┼───────────┼──▶ ● f(a)
   └───────┘           └───────┘
```

Function ka imtihaan arrow diagram par **ek hi sawaal** hai:

> **Kya kisi bhi ek dot se do teer nikal rahe hain?**
> Nikal rahe hain → function nahi. Nahi nikal rahe → function hai.
> (Do dots se ek hi dot par aana bilkul theek hai.)

Yeh dono diagrams L02 ka tool hain — abhi sirf pehchan liya.

---

## 5. AI connection

```
y = model(x)                 same x → same y          function ✓
LLM(prompt, temperature=0.8) har baar naya jawab      function ✗
```

Do practical nataij:

1. **Seed fix karna** = model ko function banana. Bagair seed ke aapka
   experiment reproduce nahi hoga — kyunki technically woh ek rule hi nahi.
2. **"Model random behave kar raha hai"** ka pehla shak *randomness* nahi hona
   chahiye — pehla shak yeh: **koi input chhoot raha hai** (timestamp, session,
   locale, cache state, dropout on-at-inference). Yehi Box B ka sabaq tha.
   Poora input pakro, rule wapas honest ho jaata hai.

Bonus: `f(x)` notation aur `def f(x): return ...` ek hi cheez hai.
`f` naam hai, `f(x)` call ka nateeja hai.

---

## 6. Practice

### A) Book se — Stewart §1.1 (p. 18)

- **Ex 6** — rozmarra ki zindagi se teen functions likhein, har ek ka domain aur range.
- **Ex 7–14** — "Determine whether the equation or table defines y as a function of x."
  Yeh 8 problems L01 ka exact imtihaan hain. Zaroor karein.

> **Ex 15–18** (graph dekh kar faisla) abhi **na** karein — woh
> **L05 — FAKE BOX DETECTOR** ka reward hai. Wahan vertical line test milega.

### B) Scenario problems (L01 ki zubaan me)

**P1.** Vending machine me button A dabao → hamesha Coke. Button B dabao →
kabhi Sprite, kabhi Fanta. `drink = f(button)` — function hai?

**P2.** Ek box ka log: `(2, 140)`, `(5, 290)`, `(2, 140)`, `(8, 440)`.
(a) Kya yeh function ho sakti hai? (b) Rule dhoondein. (c) `f(10)` batayen.

**P3.** School me `naam = f(roll number)` — function hai?
Aur ulta, `roll number = g(naam)` — function hai?

**P4.** Production me aapka model ek hi input row par do mukhtalif predictions
de raha hai. Do mumkin wajuhat likhein — aur batayen kaun si wajah me model
phir bhi ek function hai.

**P5.** "Bijli ka bill units consumed par depend karta hai."
(a) Function notation me likhein. (b) Independent aur dependent variable batayen.
(c) Kya `f(150)` ki do values ho sakti hain? Kyun / kyun nahi?

---

## 7. Solutions

<details>
<summary>Book Ex 7–14</summary>

| # | Equation / Table | Hal | Faisla |
|---|---|---|---|
| 7 | `3x − 5y = 7` | `y = (3x − 7)/5` | **function** ✓ |
| 8 | `3x² − 2y = 5` | `y = (3x² − 5)/2` | **function** ✓ |
| 9 | `x² + (y−3)² = 5` | `y = 3 ± √(5 − x²)` — circle | **nahi** ✗ |
| 10 | `2xy + 5y² = 4` | `5y² + 2xy − 4 = 0` → `y = [−2x ± √(4x² + 80)]/10`, do values | **nahi** ✗ |
| 11 | `(y+3)³ + 1 = 2x` | `y = ∛(2x − 1) − 3` — cube root single-valued | **function** ✓ |
| 12 | `2x − |y| = 0` | `|y| = 2x` → `y = ±2x` | **nahi** ✗ |
| 13 | Height → Shoe size | `60 → 8` aur `60 → 7` | **nahi** ✗ |
| 14 | Year → Tuition | har year ka ek cost (11,200 do baar aana jaiz) | **function** ✓ |

Pattern pakrein: `y` ki **even power** ya `|y|` aaye to ± ka khatra hota hai →
aksar function nahi. `y` ki **odd power** ya akela `y` → aksar function.
Yeh shortcut L05 me vertical line test se pukhta hoga.
</details>

<details>
<summary>Scenario P1–P5</summary>

**P1.** Button A ka hissa theek hai, lekin **poori machine function nahi** —
input `B` ke do outputs hain. (Aur agar pata chal jaye ke andar stock rotate ho
raha hai, to `drink = f(button, stock_position)` function ban jaata hai — Box B
ka repair yaad karein.)

**P2.**
(a) Haan — `2` dono baar `140` de raha hai, koi conflict nahi.
(b) Constant difference dhoondein: `(5 − 2) = 3` km pe `(290 − 140) = 150` Rs
→ per km 50, aur `140 − 2(50) = 40` base. So `f(d) = 40 + 50d`.
Check: `f(8) = 40 + 400 = 440` ✓
(c) `f(10) = 40 + 500 = 540`
*(Constant difference se rule pakarna* **L12 — STRAIGHT LINE SUSPECT** *ka tool banega.)*

**P3.** `naam = f(roll number)` — **function**, kyunki har roll number ek hi
student ka hai. `roll number = g(naam)` — **function nahi**, agar do students ka
naam same ho (ek input "Ali" → do roll numbers). Yeh farq — kaun sa function
palta ja sakta hai — **L33/L34** ka pura mauzoo hai.

**P4.**
1. **Chhupa hua input** (timestamp, session id, feature ka stale cache, A/B
   bucket) — poora input shamil karne pe model **phir bhi ek function hai**,
   hum galat input dekh rahe the. ← yeh case function rehta hai.
2. **Asli randomness** (dropout inference me on, unseeded sampling,
   `temperature > 0`, non-deterministic GPU kernels) — yeh **function nahi**.
   Seed/eval-mode fix karne pe function ban jaata hai.

**P5.**
(a) `B = f(u)` — `B` bill, `u` units.
(b) independent = `u`, dependent = `B`.
(c) Nahi. Agar `f(150)` ki do values hain to `f` function hi nahi.
Agar bill waqai mukhtalif aa raha hai to koi doosra input chal raha hai
(peak/off-peak timing, slab, tax) — yani rule `B = f(u, t)` tha, `B = f(u)` nahi.
Slabs ka pura level: **L08 — THE BROKEN BOX**.
</details>

---

## 8. L02 se pehle checklist

- [ ] "exactly one" bina dekhe bol sakte hain?
- [ ] many→one **jaiz** hai — yeh pakka yaad hai?
- [ ] `f` aur `f(x)` ka farq bata sakte hain?
- [ ] domain aur range ki definition apne alfaaz me?
- [ ] `play.html` me 1000/1000 aaya?

**REWARD: `PROBE`** — aage L03 (domain), L04 (graph), L13 (best fit) me lagta hai.

**NEXT → L02 · NAME THE WIRES** — machine diagram, arrow diagram, aur `f(x)`
notation ko hathiyaar banana.
