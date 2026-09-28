/* Théo Petitimbert · Portfolio 2026 · vanilla JS, aucune dépendance */
(() => {
  const root = document.documentElement;
  const body = document.body;
  // ?motion force les animations (pratique pour tester quand l'OS réduit les animations)
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches && !/[?&]motion/.test(location.search);
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const lerp = (a, b, t) => a + (b - a) * t;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { /* stockage indisponible */ } },
  };

  /* ---------- Page prête (polices chargées) ---------- */
  const ready = () => body.classList.add('is-ready');
  Promise.race([document.fonts ? document.fonts.ready : Promise.resolve(), new Promise(r => setTimeout(r, 1200))])
    .then(() => requestAnimationFrame(ready));

  /* ---------- Horloge (Paris) ---------- */
  const clocks = document.querySelectorAll('[data-clock]');
  const fmt = new Intl.DateTimeFormat('fr-FR', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Paris' });
  const tick = () => clocks.forEach(c => { c.textContent = fmt.format(new Date()); });
  tick(); setInterval(tick, 15000);

  /* ---------- Nav : se cache en descendant, revient en remontant ---------- */
  const nav = document.querySelector('[data-nav]');
  let lastY = scrollY;
  addEventListener('scroll', () => {
    const y = scrollY;
    if (nav) nav.classList.toggle('is-hidden', y > 120 && y > lastY);
    lastY = y;
  }, { passive: true });

  /* ==========================================================================
     HERO : dégradé vivant + grille de pixels qui s'allument sous le curseur
     ========================================================================== */
  const hero = document.querySelector('[data-hero]');
  if (hero) {
    const bg = hero.querySelector('[data-hero-bg]');
    const grid = hero.querySelector('[data-hero-grid]');
    const inner = hero.querySelector('.hero-inner');
    const bctx = bg.getContext('2d');
    const gctx = grid.getContext('2d');
    const CELL = 28;
    const SCALE = 10; // le dégradé est dessiné en basse résolution puis agrandi (flou gratuit)
    let W = 0, H = 0, dpr = 1, cols = 0, rows = 0, cells, tint;
    const mouse = { x: .72, y: .62, tx: .72, ty: .62, px: -1, py: -1, active: false };

    const resize = () => {
      const r = hero.getBoundingClientRect();
      W = r.width; H = r.height; dpr = Math.min(devicePixelRatio || 1, 2);
      bg.width = Math.ceil(W / SCALE); bg.height = Math.ceil(H / SCALE);
      grid.width = Math.round(W * dpr); grid.height = Math.round(H * dpr);
      cols = Math.ceil(W / CELL); rows = Math.ceil(H / CELL);
      cells = new Float32Array(cols * rows);
      tint = new Uint8Array(cols * rows);
    };

    const blob = (x, y, r, color) => {
      const g = bctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, color); g.addColorStop(1, color.replace(/[\d.]+\)$/, '0)'));
      bctx.fillStyle = g; bctx.fillRect(0, 0, bg.width, bg.height);
    };

    const drawBg = (t) => {
      const w = bg.width, h = bg.height, m = Math.max(w, h);
      const lin = bctx.createLinearGradient(0, h, w, 0);
      lin.addColorStop(0, '#3F6B78'); lin.addColorStop(.55, '#8FB2BD'); lin.addColorStop(1, '#C8DAE0');
      bctx.fillStyle = lin; bctx.fillRect(0, 0, w, h);
      const s = t * 0.00012;
      blob(w * (.18 + .08 * Math.sin(s * 1.3)), h * (.85 + .06 * Math.cos(s)), m * .55, 'rgba(38,78,92,0.85)');
      blob(w * (.85 + .06 * Math.cos(s * .9)), h * (.12 + .08 * Math.sin(s * 1.1)), m * .42, 'rgba(226,236,240,0.6)');
      blob(w * (.5 + .2 * Math.sin(s * .7)), h * (.45 + .15 * Math.cos(s * .8)), m * .35, 'rgba(120,168,182,0.55)');
      // la touche orange (Vision / iXcampus) suit le curseur avec paresse
      blob(w * mouse.x, h * mouse.y, m * (.2 + .02 * Math.sin(s * 3)), 'rgba(242,84,45,0.75)');
      blob(w * (mouse.x * .6 + .25), h * (mouse.y * .5 + .45), m * .3, 'rgba(247,181,154,0.45)');
    };

    const light = (cx, cy, v) => {
      if (cx < 0 || cy < 0 || cx >= cols || cy >= rows) return;
      const i = cy * cols + cx;
      if (cells[i] < .05) tint[i] = Math.random() < .18 ? 1 : 0;
      cells[i] = Math.max(cells[i], v);
    };

    const drawGrid = (dt) => {
      gctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      gctx.clearRect(0, 0, W, H);
      gctx.fillStyle = 'rgba(255,255,255,0.13)';
      for (let x = CELL; x < W; x += CELL) gctx.fillRect(x, 0, 1 / dpr, H);
      for (let y = CELL; y < H; y += CELL) gctx.fillRect(0, y, W, 1 / dpr);
      const decay = Math.pow(0.925, dt / 16.7);
      for (let i = 0; i < cells.length; i++) {
        const v = cells[i];
        if (v < .01) { cells[i] = 0; continue; }
        const x = (i % cols) * CELL, y = ((i / cols) | 0) * CELL;
        gctx.fillStyle = tint[i] ? `rgba(242,84,45,${v * .9})` : `rgba(255,255,255,${v * .42})`;
        gctx.fillRect(x + 1, y + 1, CELL - 1, CELL - 1);
        cells[i] = v * decay;
      }
    };

    let running = false, last = 0, ambient = 0, raf = 0;
    const frame = (t) => {
      const dt = Math.min(64, t - (last || t)); last = t;
      mouse.x = lerp(mouse.x, mouse.tx, .035); mouse.y = lerp(mouse.y, mouse.ty, .035);
      drawBg(reduced ? 0 : t);
      ambient += dt;
      if (!reduced && ambient > (mouse.active ? 260 : 110)) {
        ambient = 0;
        light((Math.random() * cols) | 0, (Math.random() * rows) | 0, .45 + Math.random() * .4);
      }
      drawGrid(dt);
      if (running) raf = requestAnimationFrame(frame);
    };
    const start = () => { if (!running) { running = true; last = 0; raf = requestAnimationFrame(frame); } };
    const stop = () => { running = false; cancelAnimationFrame(raf); };

    resize();
    drawBg(0); drawGrid(16);
    addEventListener('resize', () => { resize(); drawBg(performance.now()); drawGrid(16); });

    hero.addEventListener('pointermove', (ev) => {
      const r = hero.getBoundingClientRect();
      const x = ev.clientX - r.left, y = ev.clientY - r.top;
      mouse.tx = x / r.width; mouse.ty = y / r.height; mouse.active = true;
      const cx = (x / CELL) | 0, cy = (y / CELL) | 0;
      // trace continue entre deux événements
      if (mouse.px >= 0) {
        const steps = Math.max(Math.abs(cx - mouse.px), Math.abs(cy - mouse.py));
        for (let k = 1; k <= steps; k++) {
          light(Math.round(lerp(mouse.px, cx, k / steps)), Math.round(lerp(mouse.py, cy, k / steps)), 1);
        }
      }
      light(cx, cy, 1);
      if (Math.random() < .35) light(cx + ((Math.random() * 3) | 0) - 1, cy + ((Math.random() * 3) | 0) - 1, .6);
      mouse.px = cx; mouse.py = cy;
    });
    hero.addEventListener('pointerleave', () => { mouse.active = false; mouse.px = -1; mouse.tx = .72; mouse.ty = .62; });

    // parallaxe du contenu + pause quand le hero n'est plus visible
    const onScroll = () => {
      const p = clamp(scrollY / innerHeight, 0, 1);
      if (!reduced) {
        inner.style.transform = `translate3d(0, ${p * 22}vh, 0) scale(${1 - p * .06})`;
        inner.style.opacity = String(1 - p * 1.1);
      }
      if (p >= 1) stop(); else if (!document.hidden) start();
    };
    addEventListener('scroll', onScroll, { passive: true });
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : onScroll()));
    onScroll();

    /* rôles qui défilent */
    const roles = [...hero.querySelectorAll('.role')];
    let ri = 0;
    roles[0]?.classList.add('is-on');
    if (roles.length > 1 && !reduced) {
      setInterval(() => {
        const cur = roles[ri], nx = roles[(ri + 1) % roles.length];
        cur.classList.replace('is-on', 'is-out');
        nx.style.transition = 'none'; nx.classList.remove('is-out', 'is-on');
        void nx.offsetWidth; nx.style.transition = '';
        nx.classList.add('is-on');
        ri = (ri + 1) % roles.length;
      }, 2400);
    }
  }

  /* ---------- Intro : les mots s'allument au fil du scroll ---------- */
  const scrub = document.querySelector('[data-scrub]');
  if (scrub && !reduced) {
    const words = [...scrub.querySelectorAll('.w')];
    const update = () => {
      const r = scrub.getBoundingClientRect(), vh = innerHeight;
      const p = clamp((vh * .85 - r.top) / (r.height + vh * .3), 0, 1);
      const n = Math.round(p * words.length);
      words.forEach((w, i) => w.classList.toggle('on', i < n));
    };
    addEventListener('scroll', update, { passive: true }); update();
  }

  /* ---------- Révélations ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: .12 });
  const observe = (scope) => scope.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
  observe(document);

  /* ==========================================================================
     Index des projets : filtres, vue liste / grille
     ========================================================================== */
  const list = document.querySelector('[data-list]');
  const vt = (fn) => (document.startViewTransition && !reduced ? document.startViewTransition(fn) : fn());
  if (list) {
    const rowsEls = [...list.querySelectorAll('.row')];
    const count = document.querySelector('[data-count]');
    document.querySelectorAll('[data-filter]').forEach(btn => btn.addEventListener('click', () => {
      const f = btn.dataset.filter;
      vt(() => {
        document.querySelectorAll('[data-filter]').forEach(b => {
          const on = b === btn; b.classList.toggle('is-active', on); b.setAttribute('aria-pressed', on);
        });
        let n = 0;
        rowsEls.forEach(r => {
          const show = f === 'all' || r.dataset.cats.split(' ').includes(f);
          r.classList.toggle('is-hidden', !show); if (show) n++;
        });
        if (count) count.textContent = String(n).padStart(2, '0');
      });
    }));

    const setView = (v, animate = true) => {
      const apply = () => {
        list.dataset.view = v;
        document.querySelectorAll('[data-view]').forEach(b => {
          if (b === list) return;
          const on = b.dataset.view === v; b.classList.toggle('is-active', on); b.setAttribute('aria-pressed', on);
        });
      };
      animate ? vt(apply) : apply();
      store.set('pf-view', v);
    };
    document.querySelectorAll('button[data-view]').forEach(b => b.addEventListener('click', () => setView(b.dataset.view)));
    if (store.get('pf-view') === 'grid') setView('grid', false);

    // morph de la vignette vers la couverture de la page projet
    list.addEventListener('click', (ev) => {
      const a = ev.target.closest('a[data-slug]');
      if (a && list.dataset.view === 'grid') a.querySelector('.row-thumb img').style.viewTransitionName = `cover-${a.dataset.slug}`;
    });
  }

  /* ---------- Aperçu flottant qui suit le curseur ---------- */
  const previewTargets = document.querySelectorAll('[data-preview]');
  if (finePointer && previewTargets.length) {
    const pv = document.createElement('div');
    pv.className = 'preview'; pv.setAttribute('aria-hidden', 'true');
    body.appendChild(pv);
    const imgs = new Map();
    const getImg = (src) => {
      if (!imgs.has(src)) { const im = new Image(); im.src = src; im.alt = ''; pv.appendChild(im); imgs.set(src, im); }
      return imgs.get(src);
    };
    const pos = { x: innerWidth / 2, y: innerHeight / 2, tx: innerWidth / 2, ty: innerHeight / 2, rot: 0 };
    let on = false, loop = 0, current = null;
    const run = () => {
      const px = pos.x;
      pos.x = lerp(pos.x, pos.tx, .14); pos.y = lerp(pos.y, pos.ty, .14);
      pos.rot = lerp(pos.rot, clamp((pos.x - px) * .35, -9, 9), .12);
      pv.style.transform = `translate3d(${pos.x}px, ${pos.y}px, 0) translate(-50%, -50%) rotate(${pos.rot}deg)`;
      if (on || Math.abs(pos.rot) > .05) loop = requestAnimationFrame(run); else loop = 0;
    };
    addEventListener('pointermove', (ev) => { pos.tx = ev.clientX; pos.ty = ev.clientY; }, { passive: true });
    previewTargets.forEach(a => {
      a.addEventListener('pointerenter', (ev) => {
        if (a.closest('.list')?.dataset.view === 'grid') return;
        if (!on) { pos.x = pos.tx = ev.clientX; pos.y = pos.ty = ev.clientY; }
        const im = getImg(a.dataset.preview);
        if (current && current !== im) current.classList.remove('is-on');
        requestAnimationFrame(() => im.classList.add('is-on'));
        current = im; on = true; pv.classList.add('is-on');
        if (!loop) loop = requestAnimationFrame(run);
      });
      a.addEventListener('pointerleave', () => {
        on = false; pv.classList.remove('is-on');
        const im = current; setTimeout(() => { if (!on && im) im.classList.remove('is-on'); }, 350);
      });
      a.addEventListener('click', () => { if (on && current) current.style.viewTransitionName = `cover-${a.dataset.slug}`; });
    });
    // précharge après le chargement
    addEventListener('load', () => setTimeout(() => previewTargets.forEach(a => getImg(a.dataset.preview)), 800));
  }

  /* ---------- Curseur ---------- */
  if (finePointer && !reduced) {
    root.classList.add('has-cursor');
    const c = document.querySelector('.cursor');
    const label = c.querySelector('.cursor-label');
    const p = { x: -100, y: -100, tx: -100, ty: -100 };
    addEventListener('pointermove', (ev) => { p.tx = ev.clientX; p.ty = ev.clientY; c.classList.remove('is-hidden'); }, { passive: true });
    document.addEventListener('pointerleave', () => c.classList.add('is-hidden'));
    const move = () => {
      p.x = lerp(p.x, p.tx, .22); p.y = lerp(p.y, p.ty, .22);
      c.style.transform = `translate3d(${p.x}px, ${p.y}px, 0)`;
      requestAnimationFrame(move);
    };
    move();
    // délégation : fonctionne aussi pour les projets ajoutés par le scroll infini
    document.addEventListener('pointerover', (ev) => {
      const el = ev.target.closest('[data-cursor]');
      if (el) { label.textContent = el.dataset.cursor; c.classList.add('is-big'); }
    });
    document.addEventListener('pointerout', (ev) => {
      const el = ev.target.closest('[data-cursor]');
      if (el && !el.contains(ev.relatedTarget)) c.classList.remove('is-big');
    });
  }

  /* ---------- Éléments magnétiques ---------- */
  const bindMagnetic = (scope) => {
    if (!finePointer || reduced) return;
    scope.querySelectorAll('[data-magnetic]').forEach(el => {
      el.style.transition = 'transform .6s cubic-bezier(.2,.7,.1,1)';
      el.addEventListener('pointermove', (ev) => {
        const r = el.getBoundingClientRect();
        const dx = ev.clientX - (r.left + r.width / 2), dy = ev.clientY - (r.top + r.height / 2);
        el.style.transition = 'transform .15s linear';
        el.style.transform = `translate(${dx * .18}px, ${dy * .3}px)`;
      });
      el.addEventListener('pointerleave', () => {
        el.style.transition = 'transform .6s cubic-bezier(.2,.7,.1,1)';
        el.style.transform = '';
      });
    });
  };
  bindMagnetic(document);

  /* ==========================================================================
     Scroll infini entre projets : à la fin d'un projet, le suivant est déjà là.
     Sans JS (ou hors ligne), le lien « Projet suivant » reste en place.
     ========================================================================== */
  const firstArticle = document.querySelector('.p-article[data-next]');
  if (firstArticle && location.protocol !== 'file:') {
    root.classList.add('infinite');
    if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
    const footer = document.querySelector('.contact');
    const articles = () => document.querySelectorAll('.p-article');
    const cache = new Map();
    let loading = false, current = firstArticle, jumpedToContact = false;
    document.addEventListener('click', (ev) => { if (ev.target.closest('a[href="#contact"]')) jumpedToContact = true; });

    const fetchArticle = (url) => {
      if (!cache.has(url)) {
        cache.set(url, fetch(url).then(r => {
          if (!r.ok) throw new Error(r.status);
          return r.text();
        }).then(html => new DOMParser().parseFromString(html, 'text/html').querySelector('.p-article')));
      }
      return cache.get(url);
    };

    const loadNext = async () => {
      const all = articles();
      const last = all[all.length - 1];
      if (loading || last.getBoundingClientRect().bottom - innerHeight > 1800) return;
      if (jumpedToContact) {
        if (footer && footer.getBoundingClientRect().top < innerHeight) return; // on reste sur le contact
        jumpedToContact = false; // l'utilisateur est remonté : on reprend
      }
      loading = true;
      try {
        const node = document.importNode(await fetchArticle(last.dataset.next), true);
        node.querySelectorAll('[style*="view-transition-name"]').forEach(el => { el.style.viewTransitionName = ''; });
        last.after(node);
        observe(node); bindMagnetic(node);
        trim();
        fetchArticle(node.dataset.next).catch(() => {}); // le suivant est prêt avant d'y arriver
      } catch {
        root.classList.remove('infinite'); // repli : lien classique vers le projet suivant
      }
      loading = false;
    };

    // garde le DOM léger : un projet loin au-dessus est remplacé par un bloc vide
    // de même hauteur, ce qui libère la mémoire sans jamais décaler le scroll
    const trim = () => {
      const all = articles();
      if (all.length <= 3) return;
      const a = all[0];
      if (a.getBoundingClientRect().bottom > -600) return;
      let h = all[1].getBoundingClientRect().top - a.getBoundingClientRect().top;
      const prev = a.previousElementSibling;
      if (prev && prev.classList.contains('p-ghost')) { h += Number(prev.dataset.h); prev.remove(); } // un seul bloc cumulé
      const ghost = document.createElement('div');
      ghost.className = 'p-ghost';
      ghost.dataset.h = h;
      ghost.style.height = `${h}px`;
      ghost.setAttribute('aria-hidden', 'true');
      a.replaceWith(ghost);
    };

    // l'URL et le titre suivent le projet en cours de lecture
    const sync = () => {
      let active = current;
      articles().forEach(a => { if (a.getBoundingClientRect().top <= innerHeight * .4) active = a; });
      if (active !== current && active.isConnected) {
        current = active;
        history.replaceState(null, '', `${active.dataset.slug}.html`);
        document.title = active.dataset.title;
      }
    };

    addEventListener('scroll', () => { sync(); loadNext(); }, { passive: true });
    // précharge le suivant dès que la page est calme
    addEventListener('load', () => setTimeout(() => fetchArticle(firstArticle.dataset.next).catch(() => {}), 1500));
  }

  /* ---------- Copier l'e-mail ---------- */
  const toast = document.querySelector('[data-toast]');
  let toastT = 0;
  const say = (msg) => {
    if (!toast) return;
    toast.textContent = msg; toast.classList.add('is-on');
    clearTimeout(toastT); toastT = setTimeout(() => toast.classList.remove('is-on'), 2200);
  };
  document.querySelectorAll('[data-copy]').forEach(btn => btn.addEventListener('click', async () => {
    const hint = btn.querySelector('[data-copy-hint]');
    try {
      await navigator.clipboard.writeText(btn.dataset.copy);
      say('Adresse copiée ✓');
      if (hint) { hint.textContent = 'Copié ✓'; setTimeout(() => { hint.textContent = 'Cliquer pour copier'; }, 2200); }
    } catch {
      location.href = `mailto:${btn.dataset.copy}`;
    }
  }));
})();
