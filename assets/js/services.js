/* Accueil · Savoir-faire : l'élément le plus proche du centre de l'écran passe
   en noir, ses voisins s'estompent. Hors écran, l'état de repos met en avant
   l'élément central de la liste. */
(() => {
  const list = document.querySelector('[data-services]');
  if (!list) return;
  const items = [...list.children];
  let raf = 0;
  const paint = () => {
    raf = 0;
    const vh = innerHeight;
    const lr = list.getBoundingClientRect();
    const rects = items.map((el) => el.getBoundingClientRect());
    const h = rects[0].height || 40;
    let c;
    if (lr.bottom < 0 || lr.top > vh) {
      const m = rects[Math.floor(items.length / 2)];
      c = m.top + m.height / 2;
    } else {
      c = Math.min(Math.max(vh / 2, lr.top + h / 2), lr.bottom - h / 2);
    }
    rects.forEach((r, i) => {
      const d = (r.top + r.height / 2 - c) / h;
      const k = Math.exp(-(d * d) / 1.1);
      items[i].style.setProperty('--k', k < 0.02 ? 0 : k.toFixed(3));
    });
  };
  const req = () => { if (!raf) raf = requestAnimationFrame(paint); };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req);
  paint();
})();
