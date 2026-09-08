/* ============================================================
   THE BLACK BOX — shared game engine
   Chapter 1 · Functions and Models · 41 levels

   Progress localStorage me save hota hai. Har level ka reward ek TOOL hai,
   aur DECODE % act milestones (24 / 46 / 68 / 84 / 100) se match karta hai —
   bilkul CH01-GAME-CAMPAIGN.md ke mutabiq.
   ============================================================ */

(function (global) {
  'use strict';

  var KEY = 'bb-ch01-v1';

  var ACTS = [
    { n: 1, roman: 'I',   title: 'FIRST CONTACT',   section: '1.1', pages: 'p. 8–23',  tagline: 'Box function hai ya nahi?',    decode: 24 },
    { n: 2, roman: 'II',  title: 'THE SHAPE HUNT',  section: '1.2', pages: 'p. 24–36', tagline: 'Andar kaun sa family hai?',    decode: 46 },
    { n: 3, roman: 'III', title: 'THE WORKSHOP',    section: '1.3', pages: 'p. 37–46', tagline: 'Box ke andar aur boxes hain',  decode: 68 },
    { n: 4, roman: 'IV',  title: 'THE ENGINE ROOM', section: '1.4', pages: 'p. 47–56', tagline: 'Box ka core exponential hai',  decode: 84 },
    { n: 5, roman: 'V',   title: 'REVERSE',         section: '1.5', pages: 'p. 57–69', tagline: 'Ab isko ULTA chalao',          decode: 100 }
  ];

  /* id, act, title, tool, slug, built(=khela ja sakta hai), boss */
  var LEVELS = [
    { id: 'L01', act: 1, title: 'IS IT HONEST?',              tool: 'PROBE',             slug: 'L01_is_it_honest',    built: true },
    { id: 'L02', act: 1, title: 'NAME THE WIRES',             tool: 'LABEL GUN',         slug: 'L02_name_the_wires', built: true },
    { id: 'L03', act: 1, title: 'WHERE DOES IT REFUSE?',      tool: 'BOUNDARY TAPE',     slug: 'L03_where_it_refuses' },
    { id: 'L04', act: 1, title: 'THE SILHOUETTE',             tool: 'PLOTTER',           slug: 'L04_the_silhouette' },
    { id: 'L05', act: 1, title: 'FAKE BOX DETECTOR',          tool: 'VLT SCANNER',       slug: 'L05_fake_box_detector' },
    { id: 'L06', act: 1, title: 'FOUR INTERROGATION ROOMS',   tool: 'TRANSLATOR',        slug: 'L06_four_rooms' },
    { id: 'L07', act: 1, title: 'SKETCH FROM TESTIMONY',      tool: 'SKETCH PAD',        slug: 'L07_sketch_testimony' },
    { id: 'L08', act: 1, title: 'THE BROKEN BOX',             tool: 'SPLICER',           slug: 'L08_the_broken_box' },
    { id: 'L09', act: 1, title: 'MIRROR & COMPASS',           tool: 'SYMMETRY LENS',     slug: 'L09_mirror_compass' },
    { id: 'L10', act: 1, title: 'BUILD A BOX FROM WORDS',     tool: 'RATE METER',        slug: 'L10_build_from_words', boss: true },

    { id: 'L11', act: 2, title: 'THE MODELING LOOP',          tool: 'LOOP CHART',        slug: 'L11_modeling_loop' },
    { id: 'L12', act: 2, title: 'STRAIGHT LINE SUSPECT',      tool: 'SLOPE RULER',       slug: 'L12_straight_line' },
    { id: 'L13', act: 2, title: 'WHICH LINE?',                tool: 'BEST-FIT ENGINE',   slug: 'L13_which_line' },
    { id: 'L14', act: 2, title: 'PREDICTION TRAP',            tool: 'RISK GAUGE',        slug: 'L14_prediction_trap' },
    { id: 'L15', act: 2, title: 'PARABOLA BEAST',             tool: 'PARABOLA BOW',      slug: 'L15_parabola_beast' },
    { id: 'L16', act: 2, title: 'POWER RANGER',               tool: 'POWER DIAL',        slug: 'L16_power_ranger' },
    { id: 'L17', act: 2, title: 'BROKEN RATIO',               tool: 'RATIO KIT',         slug: 'L17_broken_ratio' },
    { id: 'L18', act: 2, title: 'THE HEARTBEAT',              tool: 'WAVE GENERATOR',    slug: 'L18_the_heartbeat' },
    { id: 'L19', act: 2, title: 'THE FAMILY ALBUM',           tool: 'FAMILY ALBUM',      slug: 'L19_family_album', boss: true },

    { id: 'L20', act: 3, title: 'MOVE IT',                    tool: 'SHIFT HANDLE',      slug: 'L20_move_it' },
    { id: 'L21', act: 3, title: 'STRETCH IT',                 tool: 'STRETCH CLAMP',     slug: 'L21_stretch_it' },
    { id: 'L22', act: 3, title: 'FLIP IT',                    tool: 'FLIP MIRROR',       slug: 'L22_flip_it' },
    { id: 'L23', act: 3, title: 'COMBO MOVE',                 tool: 'TRANSFORM CONSOLE', slug: 'L23_combo_move' },
    { id: 'L24', act: 3, title: 'TWO BOXES, ONE OUTPUT',      tool: 'MERGE BENCH',       slug: 'L24_two_boxes' },
    { id: 'L25', act: 3, title: 'THE STACK',                  tool: 'CHAIN LINK',        slug: 'L25_the_stack' },
    { id: 'L26', act: 3, title: 'OPEN THE BOX',               tool: 'DISASSEMBLER',      slug: 'L26_open_the_box', boss: true },

    { id: 'L27', act: 4, title: 'THE DOUBLING ROOM',          tool: 'GROWTH CORE',       slug: 'L27_doubling_room' },
    { id: 'L28', act: 4, title: 'EXPONENT LAWS',              tool: 'LAW TABLET',        slug: 'L28_exponent_laws' },
    { id: 'L29', act: 4, title: 'THE RACE: 2^x vs x²',        tool: 'RACE TRACK',        slug: 'L29_the_race' },
    { id: 'L30', act: 4, title: 'GROWTH FIT',                 tool: 'GROWTH FITTER',     slug: 'L30_growth_fit' },
    { id: 'L31', act: 4, title: 'THE HALF-LIFE ROOM',         tool: 'DECAY DIAL',        slug: 'L31_half_life' },
    { id: 'L32', act: 4, title: 'THE NUMBER e',               tool: 'e-CORE',            slug: 'L32_the_number_e', boss: true },

    { id: 'L33', act: 5, title: 'THE TWIN TRAP',              tool: 'HLT SCANNER',       slug: 'L33_twin_trap' },
    { id: 'L34', act: 5, title: 'THE UNDO BUTTON',            tool: 'UNDO KEY',          slug: 'L34_undo_button' },
    { id: 'L35', act: 5, title: 'SOLVE & SWAP',               tool: 'SWAP WRENCH',       slug: 'L35_solve_and_swap' },
    { id: 'L36', act: 5, title: 'THE MIRROR LINE',            tool: 'y=x MIRROR',        slug: 'L36_mirror_line' },
    { id: 'L37', act: 5, title: 'LOG = UNDO EXPONENTIAL',     tool: 'LOG KEY',           slug: 'L37_log_key' },
    { id: 'L38', act: 5, title: 'LOG LAWS COMBO',             tool: 'LOG TABLET',        slug: 'L38_log_laws' },
    { id: 'L39', act: 5, title: 'THE LOG LENS',               tool: 'LOG LENS',          slug: 'L39_log_lens' },
    { id: 'L40', act: 5, title: 'THE ANGLE RETRIEVER',        tool: 'ANGLE KEY',         slug: 'L40_angle_retriever' },
    { id: 'L41', act: 5, title: 'INVERT THE BLACK BOX',       tool: 'BOX DECODED',       slug: 'L41_final_boss', boss: true }
  ];

  /* DECODE weights — act ke andar barabar bant, act ke end pe milestone exact */
  var WEIGHT = (function () {
    var w = {}, prev = 0;
    ACTS.forEach(function (a) {
      var inAct = LEVELS.filter(function (l) { return l.act === a.n; });
      var share = (a.decode - prev) / inAct.length;
      inAct.forEach(function (l) { w[l.id] = share; });
      prev = a.decode;
    });
    return w;
  })();

  function blank() { return { done: {}, tools: [] }; }

  function load() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY));
      if (raw && raw.done) { return raw; }
    } catch (e) { /* file:// pe storage band ho to bhi game chalta rahega */ }
    return blank();
  }

  function persist(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {}
  }

  var state = load();

  var BB = {
    ACTS: ACTS,
    LEVELS: LEVELS,

    level: function (id) {
      return LEVELS.filter(function (l) { return l.id === id; })[0] || null;
    },

    index: function (id) {
      for (var i = 0; i < LEVELS.length; i++) { if (LEVELS[i].id === id) { return i; } }
      return -1;
    },

    isDone: function (id) { return !!state.done[id]; },

    /* level khul gaya? pehla level hamesha khula, baqi pichhla complete hone pe */
    isUnlocked: function (id) {
      var i = BB.index(id);
      if (i <= 0) { return i === 0; }
      return BB.isDone(LEVELS[i - 1].id);
    },

    decode: function () {
      var sum = 0;
      Object.keys(state.done).forEach(function (id) { sum += WEIGHT[id] || 0; });
      return Math.min(100, sum);
    },

    tools: function () {
      return LEVELS.filter(function (l) { return BB.isDone(l.id); }).map(function (l) { return l.tool; });
    },

    score: function (id) { return state.done[id] ? state.done[id].score : 0; },

    complete: function (id, score, max) {
      state.done[id] = { score: score || 0, max: max || 0, at: Date.now() };
      var lvl = BB.level(id);
      if (lvl && state.tools.indexOf(lvl.tool) < 0) { state.tools.push(lvl.tool); }
      persist(state);
      return BB.decode();
    },

    reset: function () { state = blank(); persist(state); },

    /* ------------------------------------------------ HUD */
    mountHud: function (el, levelId) {
      var lvl = BB.level(levelId);
      var pct = BB.decode();
      var toolCount = BB.tools().length;
      el.className = 'bb-hud';
      el.innerHTML =
        '<div>' +
          '<div class="bb-hud__brand">THE BLACK BOX</div>' +
          '<div class="bb-hud__level">' + (lvl ? lvl.id + '  ·  ' + lvl.title : 'LEVEL MAP') + '</div>' +
        '</div>' +
        '<div class="bb-hud__right">' +
          '<div class="bb-hud__tools">TOOLS ' + toolCount + ' / ' + LEVELS.length + '</div>' +
          '<div class="bb-hud__decode">DECODE ' + Math.round(pct) + '%</div>' +
          '<div class="bb-bar"><div class="bb-bar__fill" id="bb-bar-fill"></div></div>' +
        '</div>';
      requestAnimationFrame(function () {
        var f = document.getElementById('bb-bar-fill');
        if (f) { f.style.width = Math.max(pct, 1) + '%'; }
      });
    },

    refreshHud: function (levelId) {
      var el = document.getElementById('hud');
      if (el) { BB.mountHud(el, levelId); }
    },

    /* ------------------------------------------------ toast */
    toast: function (msg, ms) {
      var t = document.getElementById('bb-toast');
      if (!t) {
        t = document.createElement('div');
        t.id = 'bb-toast';
        t.className = 'toast';
        document.body.appendChild(t);
      }
      t.textContent = msg;
      t.classList.add('show');
      clearTimeout(t._timer);
      t._timer = setTimeout(function () { t.classList.remove('show'); }, ms || 2400);
    },

    /* ------------------------------------------------ chhote DOM helpers */
    el: function (tag, cls, html) {
      var n = document.createElement(tag);
      if (cls) { n.className = cls; }
      if (html !== undefined) { n.innerHTML = html; }
      return n;
    },

    stage: function (id) {
      var all = document.querySelectorAll('.stage');
      for (var i = 0; i < all.length; i++) { all[i].classList.remove('active'); }
      var s = document.getElementById(id);
      if (s) { s.classList.add('active'); window.scrollTo({ top: 0, behavior: 'smooth' }); }
    },

    /* ------------------------------------------------ quiz engine
       Ek waqt me ek sawaal, feedback ke saath. MCQ aur numeric dono.

       questions: [{ prompt, given?, options:[{t, ok}], why }]
              ya  [{ prompt, given?, answer:<number>, tol?, why }]

       opts: { mount, questions, pts, onScore(pts), onDone(got,total), doneLabel }

       Zaroori: sab kuch `mount` ke andar CLASS se dhoonda jaata hai, id se nahi —
       kai quizzes ek hi waqt me DOM me ho sakte hain (hidden stages). */
    quiz: function (opts) {
      var mount = document.getElementById(opts.mount);
      var qs = opts.questions;
      var pts = opts.pts || 50;
      var i = 0;
      var got = 0;

      function q$(sel) { return mount.querySelector(sel); }

      function render() {
        var q = qs[i];
        var last = (i === qs.length - 1);
        var body;

        if (q.options) {
          body = '<div class="qa">' + q.options.map(function (o, k) {
            return '<button class="btn opt" data-k="' + k + '">' + o.t + '</button>';
          }).join('') + '</div>';
        } else {
          body = '<div class="qnum">' +
                   '<input type="number" class="numin" placeholder="?" step="any">' +
                   '<button class="btn btn--primary numgo">CHECK</button>' +
                 '</div>';
        }

        mount.innerHTML =
          '<div class="card">' +
            '<h3>' + (i + 1) + ' / ' + qs.length + '</h3>' +
            '<p class="qprompt">' + q.prompt + '</p>' +
            (q.given ? '<p class="qgiven">' + q.given + '</p>' : '') +
            body +
            '<div class="fb"></div>' +
          '</div>';

        if (q.options) {
          mount.querySelectorAll('.opt').forEach(function (b) {
            b.onclick = function () { judge(+b.dataset.k, b); };
          });
        } else {
          var inp = q$('.numin');
          var fire = function () { judgeNum(inp.value); };
          q$('.numgo').onclick = fire;
          inp.onkeydown = function (e) { if (e.key === 'Enter') { fire(); } };
        }

        function lock(rightIdx) {
          mount.querySelectorAll('.opt').forEach(function (b, k) {
            b.disabled = true;
            if (k === rightIdx) { b.classList.add('right'); }
          });
          var n = q$('.numin');
          if (n) { n.disabled = true; q$('.numgo').disabled = true; }
        }

        function feedback(right) {
          if (right) {
            got++;
            if (opts.onScore) { opts.onScore(pts); }
          }
          q$('.fb').innerHTML =
            '<div class="banner ' + (right ? 'banner--ok' : 'banner--warn') +
                 '" style="margin-top:18px">' +
              '<div class="banner__chip">' +
                (right ? 'CORRECT · +' + pts : 'NOPE — yeh hint hai') +
              '</div>' +
              '<p class="why" style="margin:0">' + q.why + '</p>' +
            '</div>' +
            '<div class="navrow"><span class="score">' + (got * pts) + ' / ' +
              (qs.length * pts) + ' pts</span>' +
              '<button class="btn btn--primary qgo">' +
                (last ? (opts.doneLabel || 'NEXT STAGE →') : 'NEXT →') +
              '</button></div>';

          q$('.qgo').onclick = function () {
            if (last) {
              if (opts.onDone) { opts.onDone(got, qs.length); }
            } else {
              i++;
              render();
            }
          };
        }

        function judge(k, btn) {
          var rightIdx = -1;
          q.options.forEach(function (o, idx) { if (o.ok) { rightIdx = idx; } });
          var right = !!q.options[k].ok;
          if (!right) { btn.classList.add('wrong'); }
          lock(rightIdx);
          feedback(right);
        }

        function judgeNum(v) {
          var right = (v !== '' && Math.abs(parseFloat(v) - q.answer) <= (q.tol || 1e-9));
          var n = q$('.numin');
          n.style.borderColor = right ? 'var(--ok)' : 'var(--bad)';
          lock(-1);
          feedback(right);
        }
      }

      render();
    },

    steps: function (el, total, current) {
      el.className = 'steps';
      el.innerHTML = '';
      for (var i = 0; i < total; i++) {
        el.appendChild(BB.el('span', i < current ? 'done' : (i === current ? 'on' : '')));
      }
    }
  };

  global.BB = BB;
})(window);
