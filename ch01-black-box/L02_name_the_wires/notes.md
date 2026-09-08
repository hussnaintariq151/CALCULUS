# L02 — NAME THE WIRES
### ACT I · FIRST CONTACT · Stewart §1.1, p. 8–9 · TOOL: `LABEL GUN`

> Order: `play.html` → `L02Cinematic` → **phir** yeh notes.

---

## 1. Aapne khud kya dhoonda

| Game me | Math me |
|---|---|
| Diagram ke teen parts label kiye | machine diagram (Figure 2) |
| `f` = machine ka naam, `f(x)` = output | function vs function value |
| jo hum chunte hain / jo tay hota hai | independent / dependent variable |
| `f(2a)` aur `2f(a)` alag nikle | bracket ke andar = input, bahar = output |
| `f(a²)` aur `[f(a)]²` alag nikle | order of operations |
| 4 situations ko notation me likha | `output = f(input)` |

---

## 2. Notation — poora reference

### `f` vs `f(x)` — yeh table yaad rakhein

| | `f` | `f(x)` |
|---|---|---|
| **Kya hai** | rule / machine ka naam | ek **value** (aksar number) |
| **Bola jaata hai** | "eff" | "eff of x" |
| **Python** | `f` (function object) | `f(3)` → `26` |
| **Misal** | "f squaring rule hai" | `f(4) = 16` |
| **Ghalat likhai** | ~~`f = 3x² − x + 2`~~ | ✓ `f(x) = 3x² − x + 2` |

`f(x)` me brackets **multiplication nahi** hain. Woh kehte hain: "machine `f`
ko input `x` par chalao".

### Variables (p. 8–9)

| Naam | Matlab | Misal: `A = f(r) = πr²` |
|---|---|---|
| **independent variable** | input ka symbol — jo hum chunte hain | `r` |
| **dependent variable** | output ka symbol — jo tay ho jaata hai | `A` |
| **value of f at x** | `f(x)` | `f(2) = 4π` |

`π` variable **nahi** hai — woh constant hai. Aur `f` bhi variable nahi — woh naam hai.

---

## 3. Do naqshe (p. 9)

### Machine diagram — Figure 2

```
     x  ──────▶  ┌─────────┐  ──────▶  f(x)
  (input)        │    f    │           (output)
                 └─────────┘
   ▲                  ▲                   ▲
independent          RULE             dependent
```

### Arrow diagram — Figure 3

```
        D                          E
    ┌────────┐                 ┌────────┐
    │  x ●───┼─────────────────┼──▶ ● f(x)
    │  a ●───┼─────────────────┼──▶ ● f(a)
    │  4 ●───┼─────────────────┼──▶ ● f(4)
    └────────┘                 └────────┘
   domain                    outputs ka set
```

L01 ka poora imtihaan is naqshe par **ek nazar** ka kaam hai:

> Kisi bhi **ek** dot se **do** teer nahi nikalne chahiye.
> (Do dots se **ek hi** dot par aana bilkul theek hai — yeh L01 ka trap tha.)

---

## 4. THE BRACKET RULE — level ka nichor

> **Bracket ke ANDAR jo hai → INPUT par asar karta hai.**
> **Bracket ke BAHAR jo hai → OUTPUT par asar karta hai.**

`f(x) = 3x² − x + 2` ke saath:

| Likhai | Kaam ka order | Nateeja |
|---|---|---|
| `f(2a)` | pehle input doguna, phir machine | `12a² − 2a + 2` |
| `2f(a)` | pehle machine, phir output doguna | `6a² − 2a + 4` |
| `f(a²)` | pehle input square, phir machine | `3a⁴ − a² + 2` |
| `[f(a)]²` | pehle machine, phir output square | `9a⁴ − 6a³ + 13a² − 4a + 4` |

Chaaron mukhtalif. Yeh ittefaq nahi — **order badalne se nateeja badalta hai**.
Yehi cheez L25 (composition: `f(g(x))` vs `g(f(x))`) me poora level ban jaayegi.

---

## 5. Stewart ke chaar examples (p. 8) — sab ek shakal me

| | Situation | Notation | Rule ki shakal |
|---|---|---|---|
| A | circle ka area, radius se | `A = f(r) = πr²` | **formula** |
| B | duniya ki aabadi, waqt se | `P = f(t)` | **table** (Table 1) |
| C | envelope ka postage, wazan se | `C = f(w)` | **rule-book** (Table 3) |
| D | zameen ka acceleration, waqt se | `a = f(t)` | **graph** (Figure 1) |

Ghor karein: **sirf A me formula hai.** Baqi teen me nahi — aur chaaron phir bhi
functions hain. Function hone ke liye formula ki shart **nahi** hai; shart sirf
"har input ka exactly ek output" hai.

Yeh chaar shaklein — words, table, graph, formula — **L06 (FOUR INTERROGATION
ROOMS)** ka pura level hain.

---

## 6. AI connection

```python
def f(x):
    return 3*x**2 - x + 2

f        # <function f>   ← naam / rule
f(3)     # 26             ← output

f == f(3)   # False — do bilkul mukhtalif cheezein
```

Teen practical baatein:

1. **Type hint hi domain → range hai.** `def f(x: float) -> float` likhna
   exactly wahi keh raha hai jo `f: D → E`. Domain ka poora level L03 hai.
2. **`model` vs `model(x)`** ka farq bilkul `f` vs `f(x)` hai. Isi liye
   `predictions = model` ek classic bug hai — aap function object save kar
   rahe hain, output nahi.
3. **Higher-order functions** = `f` ko as-is pass karna (`map(f, xs)`),
   `f(x)` pass karna uska nateeja bhejna hai. Jo log `f` aur `f(x)` ka farq
   nahi samajhte, wahi `map(f(x), xs)` likh kar phasṭe hain.

---

## 7. Practice

### A) Book se — Stewart §1.1 (p. 19)

- **Ex 33** — `f(x) = 3x² − x + 2` par: `f(2)`, `f(−2)`, `f(a)`, `f(−a)`,
  `f(a+1)`, `2f(a)`, `f(2a)`, `f(a²)`, `[f(a)]²`, `f(a+h)`
  *(Game ka Stage 3 isi ka hissa tha — ab poora karein.)*
- **Ex 34** — `g(x) = x / √(x+1)` par: `g(0)`, `g(3)`, `5g(a)`, `½g(4a)`,
  `g(a²)`, `[g(a)]²`, `g(a+h)`, `g(x−a)`
- **Ex 6** — rozmarra se teen functions likhein aur unko notation me daalein.

> **Ex 35–38** (difference quotient) abhi **na** karein — woh **L10** ka reward hai.
> `f(a+h)` aap kar chuke hain, jo us ka aadha kaam hai.

### B) Scenario problems

**P1.** L01 wali box ka rule tha `f(d) = 40 + 50d`.
(a) `f(6)` batayen. (b) `f(2a)` aur `2f(a)` likhein.
(c) `a = 3` par kaun bara hai, aur kitna?
(d) Kaisi lines par `f(2a) = 2f(a)` hamesha sach hota hai?

**P2.** "GPU memory usage, batch size par depend karti hai."
Notation likhein, aur independent/dependent batayen.

**P3.** `f(x) = x²`. Kya `f(2a) = 2f(a)`? Aisi tamam `a` dhoondein jahan
dono barabar ho jaate hain.

**P4.** `T = f(t)` — nal ka paani, `t` minute me, `T` °C me. `f(3) = 45` ka
matlab alfaaz me likhein. Phir batayen `f(f(3))` kyun bemani hai.

**P5.** Kisi ne dawa ki: `f(x + y) = f(x) + f(y)` hamesha sach hota hai.
`f(x) = 3x² − x + 2` ke saath `x = 1, y = 2` par test karein. Phir sochein:
kaisi functions par yeh **waqai** sach hota hai?

---

## 8. Solutions

<details>
<summary>Book Ex 33 — f(x) = 3x² − x + 2</summary>

| | Hal | Jawab |
|---|---|---|
| `f(2)` | `3(4) − 2 + 2` | **12** |
| `f(−2)` | `3(4) + 2 + 2` | **16** |
| `f(a)` | x → a | **3a² − a + 2** |
| `f(−a)` | `3a² + a + 2` (sirf beech wali term ka sign palta) | **3a² + a + 2** |
| `f(a+1)` | `3(a²+2a+1) − a − 1 + 2 = 3a² + 6a + 3 − a + 1` | **3a² + 5a + 4** |
| `2f(a)` | `2(3a² − a + 2)` | **6a² − 2a + 4** |
| `f(2a)` | `3(4a²) − 2a + 2` | **12a² − 2a + 2** |
| `f(a²)` | `3(a²)² − a² + 2` | **3a⁴ − a² + 2** |
| `[f(a)]²` | `(3a² − a + 2)²` | **9a⁴ − 6a³ + 13a² − 4a + 4** |
| `f(a+h)` | `3(a+h)² − (a+h) + 2` | **3a² + 6ah + 3h² − a − h + 2** |

`[f(a)]²` ka phailao:
`(3a² − a + 2)² = 9a⁴ + a² + 4 + 2(3a²)(−a) + 2(3a²)(2) + 2(−a)(2)`
`= 9a⁴ + a² + 4 − 6a³ + 12a² − 4a = 9a⁴ − 6a³ + 13a² − 4a + 4`

Sabse aam ghalti: `(3a² − a + 2)² = 9a⁴ + a² + 4` likh dena — **cross terms bhool jaana**.
</details>

<details>
<summary>Book Ex 34 — g(x) = x / √(x+1)</summary>

| | Jawab |
|---|---|
| `g(0)` | `0 / √1` = **0** |
| `g(3)` | `3 / √4` = **3/2** |
| `5g(a)` | **5a / √(a+1)** |
| `½g(4a)` | `½ · 4a/√(4a+1)` = **2a / √(4a+1)** |
| `g(a²)` | **a² / √(a²+1)** |
| `[g(a)]²` | `a² / (a+1)` — √ square hone se ghayab | **a² / (a+1)** |
| `g(a+h)` | **(a+h) / √(a+h+1)** |
| `g(x−a)` | **(x−a) / √(x−a+1)** |

Do baatein pakrein:
1. `g(a²)` me √ **rehta** hai, `[g(a)]²` me √ **khatam** ho jaata hai — bracket rule.
2. `√(x+1)` ke liye `x + 1 > 0` chahiye, yani `x > −1`. Yeh **domain** hai —
   `g(−3)` bemani hoga. Poora hisaab **L03** me.
</details>

<details>
<summary>Scenario P1–P5</summary>

**P1.** `f(d) = 40 + 50d`
(a) `f(6) = 40 + 300 = ` **340**
(b) `f(2a) = 40 + 100a` &nbsp;·&nbsp; `2f(a) = 2(40 + 50a) = 80 + 100a`
(c) `a = 3`: `f(6) = 340`, `2f(3) = 2(190) = 380`. **`2f(a)` bara hai, 40 se.**
Woh 40 base fare hai jo doubling me do baar gina gaya.
(d) Sirf tab jab **intercept zero** ho — yani `f(d) = md` (origin se guzarne wali
line). Aisi functions ko "linear/homogeneous" kehte hain; `L12` me isi ki shakal
milegi, aur `L20` (shift) me pata chalega ke intercept hi shift hai.

**P2.** `M = f(b)` — `M` memory, `b` batch size.
independent = `b` (hum chunte hain), dependent = `M` (tay ho jaati hai).

**P3.** `f(2a) = (2a)² = 4a²`, &nbsp; `2f(a) = 2a²`.
Barabar tab: `4a² = 2a² ⟹ 2a² = 0 ⟹ ` **`a = 0` (sirf)**.
Yani squaring machine par input doubling aur output doubling kabhi ek nahi
(sifar ke ilawa) — kyunki square me doubling **4 guna** asar karti hai.

**P4.** `f(3) = 45` ka matlab: **"nal chalne ke 3 minute baad paani ka
temperature 45 °C tha."**
`f(f(3)) = f(45)` ka matlab hoga "45 **minute** par temperature" — lekin 45
temperature tha, waqt nahi. **Units match nahi karti**, is liye bemani hai.
Yehi cheez formally `L25` me aayegi: composition `f(g(x))` sirf tab chalti hai
jab `g` ka output `f` ki **domain** me ho.

**P5.** `f(x) = 3x² − x + 2`, `x = 1`, `y = 2`:
`f(3) = 27 − 3 + 2 = 26`
`f(1) + f(2) = (3 − 1 + 2) + (12 − 2 + 2) = 4 + 12 = 16`
`26 ≠ 16` → dawa **ghalat** hai.
Yeh sirf `f(x) = cx` (origin se guzarne wali seedhi line) par sach hota hai.
Aam qaida: **`f` ko andar "bantne" wala na samjhein** — `f(x+y)` ka matlab hai
"machine ko `x+y` par chalao", na ke "`f` ko distribute karo".
`√(x+y) ≠ √x + √y` aur `(x+y)² ≠ x² + y²` — dono isi ghalti ki misalein hain.
</details>

---

## 9. L03 se pehle checklist

- [ ] `f` aur `f(x)` ka farq ek jumle me bata sakte hain?
- [ ] independent vs dependent — kisi bhi situation me pehchan lete hain?
- [ ] `f(2a)`, `2f(a)`, `f(a²)`, `[f(a)]²` — chaaron alag likh sakte hain?
- [ ] bracket rule zubani yaad hai?
- [ ] Ex 33 aur 34 poore kiye?

**REWARD: `LABEL GUN`** — L10 (word problem se function) aur L25 (composition) me lagta hai.

**NEXT → L03 · WHERE DOES IT REFUSE?** — Box `−5` par ERROR deti hai, `0` par
JAM. Kaun se inputs jaiz hain? **Domain aur range.**
