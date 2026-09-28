# Portfolio 2026 · Théo Petitimbert

Site statique, sans dépendance ni framework (HTML, CSS, JS vanilla).

## Modifier le contenu

Tout le contenu (projets, textes, CV, compétences, design studio, contacts) se
trouve dans `build.py`. Après modification :

```bash
python build.py
```

Le script (Python 3 + Pillow) régénère `index.html`, `a-propos.html` et
`projets/*.html`, et ajoute une empreinte aux liens CSS/JS pour que les
navigateurs rechargent les fichiers modifiés.

## Prévisualiser

```bash
python -m http.server 5173
```

Puis ouvrir http://localhost:5173.

## Structure

Chaque page est découpée en sections indépendantes. Une section =
une fonction `render_*` dans `build.py` + une feuille CSS (+ un script si
besoin). L'élément racine de chaque section porte un attribut `data-chunk`.

| Page | Section (`data-chunk`) | Rendu | CSS | JS |
| --- | --- | --- | --- | --- |
| Accueil | `hero` (navigation incluse) | `render_hero`, `render_nav` | `hero.css`, `nav.css` | `hero.js` |
| Accueil | `intro` | `render_intro` | `intro.css` | |
| Accueil | `work` | `render_work` | `work.css` | `work.js` |
| Accueil | `clients` | `render_clients` | `clients.css` | |
| Accueil | `services` | `render_services` | `services.css` | `services.js` |
| Accueil, À propos | `next` | `render_next` | `next.css` | |
| Accueil, À propos | `footer` | `render_footer` | `footer.css` | |
| Projet | `phero` | `render_phero` | `project-hero.css` | |
| Projet | `pintro` | `render_pintro` | `project-intro.css` | |
| Projet | `pgallery` | `render_pgallery` | `project-gallery.css` | |
| Projet | `pnext` (projet suivant + barre basse) | `render_pnext` | `project-next.css` | |
| À propos | portrait, parcours, compétences, studio | `render_ahero` … `render_astudio` | `about.css` | |

- `assets/css/base.css` : tokens (couleurs, gouttières, échelle typographique),
  reset, grille 12 colonnes, boutons, révélations au scroll
- `assets/js/base.js` : révélations au scroll, heure locale, couleur de la
  navigation au-dessus des sections sombres
- `assets/img/` : visuels en WebP
- Typographie : Instrument Sans (Google Fonts, axes graisse 400–700 et
  largeur 75–100 %), seule famille du site

Les animations respectent `prefers-reduced-motion` ; le défilement est natif.

## Mettre en ligne

Le dossier se publie tel quel sur GitHub Pages, Netlify ou Vercel.
