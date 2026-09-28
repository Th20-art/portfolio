/* Accueil · Savoir-faire : point focal fixe au centre du viewport.
   L'élément qui le traverse passe à l'encre, ses voisins s'estompent selon
   une courbe continue (cœur net + traîne douce), les éléments proches des
   bords de l'écran fondent vers le fond. Un compteur à rouleau sous
   l'intitulé suit la position exacte du point focal dans la liste.
   Hors écran, l'état de repos met en avant l'élément central de la liste. */
(() => {
  const list = document.querySelector('[data-services]');
  if (!list) return;
  const items = [...list.children];
  const n = items.length;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pad = (i) => String(i).padStart(2, '0');

  // Compteur (décoratif) : 01 → n, rouleau vertical + filet de progression
  const label = document.querySelector('.services-label');
  let roll, bar, count;
  if (label) {
    count = document.createElement('span');
    count.className = 'services-count';
    count.setAttribute('aria-hidden', 'true');
    count.innerHTML = `<span class="roll"><span>${items.map((_, i) => `<i>${pad(i + 1)}</i>`).join('')}</span></span>`
      + `<span class="bar"><i></i></span><b>${pad(n)}</b>`;
    label.appendChild(count);
    roll = count.querySelector('.roll > span');
    bar = count.querySelector('.bar');
  }

  let raf = 0, live = null;
  const paint = () => {
    raf = 0;
    const vh = innerHeight;
    const lr = list.getBoundingClientRect();
    const rects = items.map((el) => el.getBoundingClientRect());
    const h = rects[0].height || 32;
    const inView = lr.bottom > 0 && lr.top < vh;
    const c = inView ? vh / 2 : rects[n >> 1].top + h / 2;
    const half = vh / 2;
    // Position du point focal dans la liste (en éléments), puis aimantation :
    // l'élément reste pleinement allumé sur ~60 % de sa hauteur et le relais
    // vers le suivant se fait par un fondu court et continu.
    const first = rects[0].top + h / 2;
    const raw = (c - first) / h;
    const base = Math.floor(raw), t = raw - base;
    const u = Math.min(1, Math.max(0, (t - 0.3) / 0.4));
    const f = base + u * u * (3 - 2 * u);
    rects.forEach((r, i) => {
      const y = r.top + r.height / 2;
      const d = i - f;
      // cœur étroit (un seul élément franc) + traîne exponentielle (dégradé)
      const core = Math.exp(-(d * d) / 0.22);
      let k = 0.64 * core + 0.36 * Math.exp(-Math.abs(d) / 1.6);
      if (k < 0.01) k = 0;
      let e = 0;
      if (inView) {
        const q = Math.min(1, Math.max(0, (Math.abs(y - half) / half - 0.5) / 0.5));
        e = q * q;
      }
      const s = items[i].style;
      s.setProperty('--k', k.toFixed(3));
      s.setProperty('--e', e.toFixed(3));
      s.setProperty('--x', inView && !reduce ? (core * 18).toFixed(2) : 0);
    });
    if (roll) {
      const g = Math.min(n - 1, Math.max(0, f));
      roll.style.transform = `translate3d(0, ${(-g * 14).toFixed(2)}px, 0)`;
      bar.style.setProperty('--p', (g / (n - 1)).toFixed(4));
      const on = inView && lr.top < half && lr.bottom > half;
      if (on !== live) { live = on; count.classList.toggle('is-live', on); }
    }
  };
  const req = () => { if (!raf) raf = requestAnimationFrame(paint); };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req);
  paint();
})();
