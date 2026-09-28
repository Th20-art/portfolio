/* Accueil · Partenaires : calibrage optique des noms-marques.
   Tous les noms partagent le même corps (donc la même hauteur de capitale) ;
   on règle ici l'axe de chasse d'Archivo (62 → 125 %) pour que chaque nom
   atteigne la même largeur relative, donc la même masse. Les valeurs sont en
   em : elles restent justes à toutes les tailles d'écran. */
(() => {
  const marks = [...document.querySelectorAll('.clients .mark')];
  if (!marks.length || !document.fonts) return;
  const TARGET = { base: 3.1, stack: 2.6, side: 3.0 };   // largeur visée, en em
  const MIN = 62, MAX = 125;

  const calibrate = () => {
    const ctx = document.createElement('canvas').getContext('2d');
    ctx.font = '800 100px Archivo';
    for (const m of marks) {
      const kind = m.classList.contains('mark--stack') ? 'stack' : m.classList.contains('mark--side') ? 'side' : 'base';
      const main = m.querySelector('.mark-main');
      const fs = parseFloat(getComputedStyle(m).fontSize);
      const set = (wd) => { m.style.setProperty('--wd', wd.toFixed(1) + '%'); m.style.setProperty('--wn', ((wd - MIN) / (MAX - MIN)).toFixed(3)); };
      const ratio = (wd) => { set(wd); return m.getBoundingClientRect().width / fs; };
      const t = TARGET[kind];
      let k = 1, wd;
      if (ratio(MIN) >= t) { wd = MIN; k = t / ratio(MIN); }
      else if (ratio(MAX) <= t) { wd = MAX; k = Math.min(1.1, t / ratio(MAX)); }
      else {
        let lo = MIN, hi = MAX;
        for (let n = 0; n < 12; n++) { const mid = (lo + hi) / 2; if (ratio(mid) < t) lo = mid; else hi = mid; }
        wd = (lo + hi) / 2;
      }
      set(wd);
      m.style.setProperty('--k', k.toFixed(3));

      /* Deux étages : le complément est justifié sur la largeur du nom principal */
      if (kind === 'stack') {
        const sub = m.querySelector('.mark-sub span');
        sub.style.letterSpacing = '0';
        const sfs = parseFloat(getComputedStyle(sub).fontSize);
        const n = [...sub.textContent].length;
        const ls = (main.getBoundingClientRect().width - sub.getBoundingClientRect().width) / Math.max(1, n - 1);
        sub.style.letterSpacing = (ls / sfs).toFixed(4) + 'em';
        sub.style.marginRight = (-ls / sfs).toFixed(4) + 'em';
      }

      /* Centrage optique : le centre de l'encre, pas celui de la boîte ;
         les jambages descendants ne comptent que pour un tiers. */
      if (kind === 'base') {
        const mt = ctx.measureText(main.textContent);
        const A = mt.fontBoundingBoxAscent / 100, D = mt.fontBoundingBoxDescent / 100;
        const ink = ((1 - (A + D)) / 2) + A + (mt.actualBoundingBoxDescent / 3 - mt.actualBoundingBoxAscent) / 200;
        m.style.setProperty('--oy', (0.5 - ink).toFixed(3) + 'em');
      }
    }
    document.querySelector('.clients .logos')?.classList.add('is-fit');
  };

  document.fonts.load('800 20px Archivo').then(() => document.fonts.ready).then(calibrate, calibrate);
})();
