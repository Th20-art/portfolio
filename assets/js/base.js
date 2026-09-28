/* Base partagée : révélations au scroll, heure locale, ton de la navigation. */
(() => {
  const doc = document.documentElement;

  /* Révélations : une fois l'élément entré dans l'écran, il reste visible. */
  const items = [...document.querySelectorAll('[data-reveal]')];
  const show = (el) => el.classList.add('is-in');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      for (const en of entries) if (en.isIntersecting) { show(en.target); io.unobserve(en.target); }
    }, { rootMargin: '0px 0px -6% 0px' });
    items.forEach((el) => io.observe(el));
  } else {
    items.forEach(show);
  }
  requestAnimationFrame(() => doc.classList.add('is-ready'));

  /* Heure locale (Paris) */
  const clocks = document.querySelectorAll('[data-clock]');
  if (clocks.length) {
    const fmt = new Intl.DateTimeFormat('fr-FR', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Paris' });
    const tick = () => { const t = fmt.format(new Date()); clocks.forEach((c) => { c.textContent = t; }); };
    tick(); setInterval(tick, 15000);
  }

  /* Navigation : passe en clair au-dessus des sections sombres */
  const nav = document.querySelector('[data-nav]');
  const darks = [...document.querySelectorAll('[data-tone="dark"]')];
  if (nav && darks.length) {
    let raf = 0;
    const probe = () => {
      raf = 0;
      const y = nav.getBoundingClientRect().height / 2;
      const over = darks.some((s) => { const r = s.getBoundingClientRect(); return r.top <= y && r.bottom >= y; });
      nav.classList.toggle('on-dark', over);
    };
    const req = () => { if (!raf) raf = requestAnimationFrame(probe); };
    addEventListener('scroll', req, { passive: true });
    addEventListener('resize', req);
    probe();
  }
})();
