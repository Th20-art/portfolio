# Portfolio 2026 · Théo Petitimbert

Site statique, sans dépendance ni framework (HTML, CSS, JS vanilla).

## Modifier le contenu

Tout le contenu (projets, textes, CV, images) se trouve dans `build.py`.
Après modification :

```bash
python build.py
```

Le script régénère `index.html` et `projets/*.html`, et ajoute une empreinte
aux liens CSS/JS pour que les navigateurs rechargent les fichiers modifiés.

## Prévisualiser

```bash
python -m http.server 5173
```

Puis ouvrir http://localhost:5173. Le scroll infini entre projets nécessite
un serveur (il est désactivé en `file://`, le lien « Projet suivant » prend le relais).

Astuce : `?motion` dans l'URL force les animations même si le système
demande de les réduire.

## Structure

- `assets/css/main.css` : styles (tokens en haut du fichier)
- `assets/js/main.js` : hero animé, index des projets, curseur, scroll infini
- `assets/img/` : visuels extraits du PDF, en WebP
- Typographies : Montserrat (titres) et Inter (texte et étiquettes)

## Mettre en ligne

Le dossier se publie tel quel sur GitHub Pages, Netlify ou Vercel.
