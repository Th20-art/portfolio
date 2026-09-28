/* Accueil · Hero : carrousel des projets à la une (autoplay, pause, clavier). */
(() => {
  const hero = document.querySelector('[data-hero]');
  if (!hero) return;
  const slides = [...hero.querySelectorAll('.hero-slide')];
  const nums = [...hero.querySelectorAll('[data-go]')];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const DUR = 6500;
  let idx = 0;

  hero.style.setProperty('--dur', DUR + 'ms');
  if (reduce) hero.classList.add('is-static');

  const go = (n) => {
    idx = (n + slides.length) % slides.length;
    slides.forEach((s, i) => {
      const on = i === idx;
      s.classList.toggle('is-active', on);
      s.setAttribute('aria-hidden', on ? 'false' : 'true');
      s.inert = !on;
    });
    nums.forEach((b, i) => {
      b.classList.toggle('is-active', i === idx);
      b.setAttribute('aria-current', i === idx ? 'true' : 'false');
      /* relance l'animation de progression */
      const f = b.querySelector('.fill');
      if (f) { f.style.animation = 'none'; void f.offsetWidth; f.style.animation = ''; }
    });
  };

  /* L'avance automatique suit la fin de la barre de progression. */
  nums.forEach((b) => {
    b.addEventListener('click', () => go(+b.dataset.go));
    const f = b.querySelector('.fill');
    if (f) f.addEventListener('animationend', () => { if (b.classList.contains('is-active')) go(idx + 1); });
  });
  hero.querySelector('[data-prev]')?.addEventListener('click', () => go(idx - 1));
  hero.querySelector('[data-next]')?.addEventListener('click', () => go(idx + 1));

  const pause = (on) => hero.classList.toggle('is-paused', on);
  hero.addEventListener('mouseenter', () => pause(true));
  hero.addEventListener('mouseleave', () => pause(false));
  hero.addEventListener('focusin', () => pause(true));
  hero.addEventListener('focusout', () => pause(false));
  document.addEventListener('visibilitychange', () => pause(document.hidden));
  hero.addEventListener('keydown', (ev) => {
    if (ev.key === 'ArrowRight') go(idx + 1);
    if (ev.key === 'ArrowLeft') go(idx - 1);
  });

  /* Glisser au doigt */
  let x0 = null;
  hero.addEventListener('pointerdown', (ev) => { if (ev.pointerType !== 'mouse') x0 = ev.clientX; });
  hero.addEventListener('pointerup', (ev) => {
    if (x0 === null) return;
    const dx = ev.clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) go(idx + (dx < 0 ? 1 : -1));
  });

  go(0);
})();
