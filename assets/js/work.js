/* Accueil · Projets : affiche / masque les projets suivants. */
(() => {
  const btn = document.querySelector('[data-more-toggle]');
  const more = document.getElementById(btn?.getAttribute('aria-controls') || '');
  if (!btn || !more) return;
  const label = btn.querySelector('[data-more-label]');
  const open = label.textContent, close = btn.dataset.closeLabel;
  more.hidden = true;
  btn.hidden = false;
  btn.addEventListener('click', () => {
    const show = more.hidden;
    more.hidden = !show;
    btn.setAttribute('aria-expanded', String(show));
    label.textContent = show ? close : open;
    if (show) {
      more.querySelectorAll('[data-reveal]').forEach((el) => requestAnimationFrame(() => el.classList.add('is-in')));
      more.querySelector('a')?.focus({ preventScroll: true });
    }
  });
})();
