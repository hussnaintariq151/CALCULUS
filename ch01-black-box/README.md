# THE BLACK BOX — Chapter 1 game campaign

Calculus · **Functions and Models** (Stewart, Early Transcendentals §1.1–1.5)
41 levels · 5 Acts · har level = ek playable mini-game + ek Manim cinematic + notes.

Poora campaign design:
`E:\AI Engineer Material\AI Engineer\Calculus\Functions and Models\CH01-GAME-CAMPAIGN.md`

---

## Shuru kaise karein

### 1. Khelein (koi install nahi)
`index.html` par **double-click**. Level map khul jayega — wahan se `L01` chunein.
Progress browser ke localStorage me save hota hai (tools, DECODE %).

### 2. Cinematic dekhein (Colab)
1. Yeh poora `ch01-black-box` folder Google Drive ke `MyDrive` me upload karein
2. `BLACKBOX_COLAB.ipynb` Colab me kholein
3. Cell 1 (setup, ~90 sec) → Cell 2 (drive mount) → Cell 3 (render helper)
4. Phir level ka render cell chalayein

Local par manim install karna zaroori **nahi** hai.

### 3. Notes padhein
Har level ke folder me `notes.md` — book walkthrough, exact page/exercise
references, aur practice problems with solutions.

> Order ahem hai: **khelo → dekho → parho**. Ulta karne se scenario-based
> learning ka poora faida chala jaata hai.

---

## Folder layout

```
ch01-black-box/
├── index.html                LEVEL MAP + tool belt (yahan se shuru)
├── BLACKBOX_COLAB.ipynb      Colab render notebook (sab levels)
├── README.md
├── shared/
│   ├── theme.py              Manim palette + type scale (LaTeX-free)
│   ├── hud.py                HudBar, BlackBox, LogTable, ArrowDiagram, ToolCard...
│   ├── game.css              mini-games ka common look (same palette)
│   └── game.js               41-level registry, progress, DECODE %, tool belt
└── L01_is_it_honest/
    ├── play.html             playable mini-game (4 stages, 1000 pts)
    ├── scene.py              L01Cinematic · L01Myths · L01Recap
    └── notes.md              Stewart p. 8–9 walkthrough + practice + solutions
```

Naya level banate waqt bas `Lxx_slug/` folder banayein, wahi teen files —
`shared/` sab kuch handle kar leta hai.

---

## Design rules (naye levels ke liye bhi)

1. **Koi LaTeX nahi.** Sab text Pango (`Text`, `mono()`, `kbd()`). Isi se Colab
   setup 90 second ka rehta hai. Formula dikhana ho to `kbd("f(x) = 2x - 1")`.
2. **Koi emoji Manim me nahi.** Colab image me emoji font nahi hota → dabbe
   (□□□) aate hain. Icons vector se banayein (`magnifier_icon()` dekhein).
   HTML me emoji theek hai.
3. **Ek palette.** `theme.py` aur `game.css` ke colors bilkul same hain —
   video aur game ek hi duniya lagti hai.
4. **Definition pehle nahi.** Har level: scenario → glitch (sawaal) → play →
   cinematic → phir book ki definition. Order badalna mana hai.
5. **Tool = interlink.** Har level ka reward aage lagta hai. Reward ka naam
   `game.js` ke registry me pehle se likha hua hai — usko change na karein,
   `CH01-GAME-CAMPAIGN.md` ka tool-belt map us par khara hai.
6. **Fail state nahi.** Galat jawab = hint + explanation, score kam. Khilaari
   kabhi atakta nahi.

---

## Progress

| Level | Tool | play.html | scene.py | notes.md |
|---|---|---|---|---|
| L01 · IS IT HONEST? | PROBE | ✅ | ✅ | ✅ |
| L02 · NAME THE WIRES | LABEL GUN | ✅ | ✅ | ✅ |
| L03 · WHERE DOES IT REFUSE? | BOUNDARY TAPE | ⬜ | ⬜ | ⬜ |

...baqi 38 levels `CH01-GAME-CAMPAIGN.md` me detail ke saath likhe hue hain.

### Shared components jo ban chuke hain

`hud.py` — `HudBar` · `LevelCard` · `BlackBox` · `pill` · `Shot` · `LogTable` ·
`ArrowDiagram` · `GlitchBanner` · `ToolCard` · `InfoCard` · `LabelChip` · `Slot` ·
`wire` · `verdict` · `book_ref` · `caption` · `beat` · `magnifier_icon` · `tag_icon`

`game.js` — 41-level registry · progress/localStorage · DECODE weights ·
tool belt · `mountHud` · `toast` · `stage` · `steps`

`game.css` — box/rig/pill · log table · objectives · banners · verdict ·
tool card · level map · **label slots + chips** (L02) · **quiz cards** (MCQ + numeric)

Naya level likhte waqt pehle inko dekh lein — 80% UI already maujood hai.
L02 ka `runQuiz()` (play.html me) copy karne layak generic quiz engine hai.
