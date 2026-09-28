"""
Générateur du portfolio de Théo Petitimbert.

Tout le contenu (projets, textes, images) est dans ce fichier.
Modifier puis lancer :  python build.py
Le site statique est écrit à la racine (index.html + projets/*.html).
"""
import hashlib
from html import escape
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
IMG = ROOT / "assets" / "img"

SITE = {
    "name": "Théo Petitimbert",
    "email": "design.theop@gmail.com",
    "phone": "06 50 21 29 57",
    "phone_href": "+33650212957",
    "linkedin": "https://www.linkedin.com/in/theopetitimbert/",
    "roles": ["Product designer", "UX/UI designer", "Global designer"],
    "bio": (
        "Designer global, je transforme des sujets complexes en produits, services et "
        "expériences utiles, compréhensibles et désirables."
    ),
    "bio_more": [
        "Au Design Studio d’iXcampus, j’ai accompagné des projets deeptech de la recherche "
        "utilisateur au prototypage. J’utilise l’IA comme un matériau de conception et je "
        "conçois mes propres outils.",
        "J’aime le design avec toutes les disciplines qui se cachent derrière, c’est pourquoi "
        "j’ai choisi le design global : considérer une situation dans son ensemble et sa "
        "complexité, et parmi toutes les formes de design trouver celle qui répondra "
        "réellement aux besoins.",
    ],
}

CV = {
    "Expérience": [
        ("2024 → 2026", "Alternance · Design Studio, iXcampus",
         "Création du design studio et accompagnement de startups deeptech. TrembLess · VestaClim · Iroony · PiPop et autres."),
        ("Juin → juil. 2023", "Stage · SNCF Réseau", "Ergonomie, design & SHS."),
    ],
    "Formation": [
        ("2021 → 2026", "CY école de design · Master 2 Design Global",
         "Saint-Germain-en-Laye · plus de 16 projets partenaires."),
        ("2024 · semestre", "Erasmus · HOWEST, Belgique", "Design for Identity · design industriel · technologie."),
        ("2021", "Baccalauréat général",
         "Numérique et sciences informatiques · Humanités, Littérature et Philosophie · Mathématiques."),
    ],
}
SKILLS = {
    "Savoir-faire": ["Design produit", "UX/UI · design d’interface", "Conception stratégique",
                     "Prototypage rapide", "Recherche utilisateur", "Animation de workshops"],
    "Outils": ["Figma · Sketch · Suite Adobe", "Rhino 8 · Twinmotion · Vizcom", "Claude Code · GitHub · outils IA"],
    "Centres d’intérêt": ["Cinéma · voyages", "Culture nipponne · jeu de go", "Hockey sur glace · nature", "Informatique"],
}

STUDIO = {
    "intro": (
        "Offre portée par l’incubateur d’iXcampus, j’ai participé à la construction du design "
        "studio, qui a pour objectif l’accompagnement des startups deeptech. Des structures qui "
        "peuvent changer d’orientation d’un jour à l’autre : un cadre de travail instable, auquel "
        "la méthode s’adapte."
    ),
    "method": [
        ("Échange", "Comprendre le projet avec les fondateurs."),
        ("Analyse", "Identifier les points faibles."),
        ("Bilan régulier", "Restituer un diagnostic argumenté."),
        ("Solutions", "Concevoir, maquetter, prototyper."),
    ],
    "images": [
        ("studio-1", "Communication · Webdesign"),
        ("studio-2", "Stratégie de communication · Graphisme · Photographie"),
        ("studio-3", "Design produit · Maquettage"),
        ("studio-4", "UX-UI · Maquettage"),
    ],
    "missions": "TrembLess · Site web iXcampus · Étude à Lannion · VestaClim · PiPop",
    "deliverables": "PDF de restitution, maquettes digitales, prototypes basse fidélité",
}

# ---------------------------------------------------------------------------
# Projets. Types de blocs :
#   section : label, title, text [..], list [(titre, texte)]
#   img     : src, alt, caption, size ('full' | 'wide' | 'narrow')
#   imgs    : items [(src, alt)], cols, caption
#   quotes  : items [(src, citation)]
#   link    : href, text
# ---------------------------------------------------------------------------
PROJECTS = [
    {
        "slug": "vision",
        "title": "Vision",
        "context": "Projet de fin de diplôme",
        "year": "2026",
        "tags": "App mobile · UX/UI",
        "cats": ["digital", "recherche"],
        "thumb": "thumb-vision",
        "cover": "vision-cover",
        "question": (
            "Comment accompagner la construction du jeune adulte dans une société où l’identité se "
            "définit davantage par ce que l’on consomme que par ce que l’on souhaite être ?"
        ),
        "summary": (
            "Une application qui intercepte les tentations d’achat, aide à formuler des objectifs "
            "et s’appuie sur un compagnon pour maintenir la motivation."
        ),
        "meta": [
            ("Durée", "Projet individuel · 9 mois"),
            ("Outils", "Figma · Claude Code · GitHub"),
            ("Prototype", ("th20-art.github.io/vision", "https://th20-art.github.io/vision/")),
        ],
        "blocks": [
            {"t": "section", "label": "Constat",
             "title": "Les objets ne servent plus seulement à répondre à des besoins.",
             "list": [
                 ("La consommation est devenue un moyen de construction identitaire",
                  "Aujourd’hui, les objets permettent aussi d’exister socialement et de se définir aux yeux des autres."),
                 ("Les habitudes de consommation influencent durablement les comportements",
                  "Les mécanismes d’habitude, renforcés par les plateformes et les interfaces numériques, poussent à "
                  "des achats automatiques et répétés, souvent sans réelle prise de recul, ce qui nous empêche de "
                  "réfléchir à plus long terme."),
                 ("Les jeunes sont encouragés à « paraître adultes » par les objets avant de se construire eux-mêmes",
                  "Téléphone, voiture ou logement deviennent des symboles de réussite et d’entrée dans l’âge adulte, "
                  "parfois avant même le développement d’une identité personnelle stable."),
             ]},
            {"t": "img", "src": "vision-constat", "alt": "File d’attente devant une boutique SHEIN", "size": "wide"},
            {"t": "quotes", "label": "Verbatims", "items": [
                ("vision-persona-1", "L’IA est une aide formidable au quotidien, mais j’aime quand on sent encore la "
                                     "sensibilité et l’intention humaine derrière l’écran."),
                ("vision-persona-2", "J’ai encore craqué et commandé un nouvel ordi sur un coup de tête… Résultat, ça "
                                     "va être vraiment chaud de partir en vacances cet été."),
            ]},
            {"t": "section", "label": "Idéation", "title": "Dessiner les pistes avant de choisir la forme."},
            {"t": "imgs", "cols": 3, "items": [
                ("vision-sketch-1", "Croquis d’idéation"), ("vision-sketch-2", "Croquis d’idéation"),
                ("vision-sketch-3", "Croquis d’idéation"), ("vision-sketch-4", "Croquis d’idéation"),
                ("vision-sketch-5", "Croquis d’idéation"),
            ]},
            {"t": "section", "label": "Solution retenue", "title": "Pourquoi proposer une solution digitale ?",
             "list": [
                 ("Le terrain de lutte est devenu numérique",
                  "L’e-commerce et nos impulsions se concentrent sur nos écrans. Pour être efficace, l’outil de "
                  "protection doit exister exactement là où le désir se crée, sans créer un énième objet physique "
                  "inutile."),
                 ("Combattre les algorithmes à armes égales",
                  "Les techniques de manipulation (dark patterns) s’adaptent et s’optimisent grâce à l’IA. Seule une "
                  "solution logicielle évolutive peut analyser, détecter et bloquer ces pièges dynamiques en temps réel."),
                 ("Intercepter au point de non-retour",
                  "Là où un objet agit trop tôt ou trop tard, une application permet de créer une friction positive au "
                  "moment très précis de la bascule cognitive, cassant le cycle de l’achat compulsif."),
             ]},
            {"t": "img", "src": "vision-solution", "alt": "Croquis de la solution retenue : un smartphone qui intercepte", "size": "narrow"},
            {"t": "section", "label": "Benchmark",
             "title": "Se situer face à opal, one sec, Noom, Fabulous, Forest et scored.",
             "text": ["Usage principal, consommation ciblée, moment d’intervention (avant, pendant, après), capacité à "
                      "sensibiliser, à favoriser l’esprit critique et risque d’app fatigue."]},
            {"t": "img", "src": "vision-benchmark", "alt": "Tableau de benchmark des applications concurrentes", "size": "wide"},
            {"t": "section", "label": "Tests", "title": "Du POC à la v2 bis, chaque version passe entre les mains des utilisateurs.",
             "text": ["Quatre itérations testées. Les retours ont ramené l’onboarding vers du concret dès le premier écran "
                      "et donné plus de place au compagnon dans la décision d’achat."]},
            {"t": "img", "src": "vision-poc", "alt": "Itérations du prototype, de v0 à v2 bis", "size": "wide"},
            {"t": "section", "label": "Objectifs", "title": "Fixer des objectifs SMART.",
             "text": ["Spécifique, Mesurable, Atteignable, Réaliste, Temporel : l’onboarding transforme une envie "
                      "floue en objectifs concrets, en quatre étapes."]},
            {"t": "imgs", "cols": 2, "items": [
                ("vision-smart", "Schéma de la méthode SMART"), ("vision-onboarding", "Écran « Fixe tes premiers objectifs »"),
            ]},
            {"t": "section", "label": "Système",
             "title": "Vision s’insère entre l’utilisateur et son environnement de consommation.",
             "text": ["Le conseiller IA intercepte, analyse et recommande, pour transformer une décision automatique "
                      "en choix conscient."]},
            {"t": "img", "src": "vision-layers", "alt": "Écrans de l’application et schéma en couches", "size": "wide"},
            {"t": "img", "src": "vision-userflow", "alt": "UserFlow simplifié de Vision", "size": "wide",
             "caption": "UserFlow simplifié : inscription, onboarding, objectifs concrets, vie quotidienne, interception, choix conscient. Le cycle se renforce."},
            {"t": "section", "label": "Compagnon", "title": "8 jours sans craquage.",
             "text": ["La gamification permet de lutter contre la perte de motivation. Changer ses habitudes peut être "
                      "compliqué : avoir un attachement émotionnel à son tamagotchi donne envie de progresser ensemble."]},
            {"t": "img", "src": "vision-gamification", "alt": "Écran d’accueil avec le compagnon renard", "size": "narrow"},
            {"t": "img", "src": "vision-final", "alt": "Vision, écran de bienvenue", "size": "full"},
            {"t": "link", "href": "https://th20-art.github.io/vision/", "text": "Tester le prototype en ligne"},
        ],
    },
    {
        "slug": "liawalk",
        "title": "LIAWALK",
        "context": "Inria",
        "year": "2025",
        "tags": "Design produit · IA",
        "cats": ["produit"],
        "thumb": "thumb-liawalk",
        "cover": "liawalk-cover",
        "question": (
            "Comment l’IA peut-elle réconcilier performance institutionnelle et reconnaissance humaine pour "
            "redonner du sens à l’action publique ?"
        ),
        "summary": (
            "Transformer l’expérience vécue des travailleurs sociaux, collectée et anonymisée, en doubles "
            "numériques qui soutiennent l’intervention, facilitent l’insertion professionnelle et transmettent "
            "les savoirs aux plus jeunes."
        ),
        "meta": [
            ("Partenaire", "Inria"),
            ("Durée", "Projet de groupe · 5 mois"),
            ("Outils", "Sketch · Rhino 8 · Twinmotion · Vizcom · Suite Adobe"),
        ],
        "blocks": [
            {"t": "section", "label": "Intention", "title": "Professionnel, 80’s vibe, véritable, analogique, rassurant."},
            {"t": "img", "src": "liawalk-moodboard", "alt": "Planche d’inspiration", "size": "wide"},
            {"t": "section", "label": "Scénario", "title": "Des doubles numériques nés du vécu professionnel.",
             "list": [
                 ("Documenter", "Le travailleur social documente son activité quotidienne et interroge des doubles "
                                "numériques pour l’aider dans ses interventions selon son agenda de missions."),
                 ("Anonymiser", "Ces données sont ensuite collectées et anonymisées."),
                 ("Générer", "Un double numérique est généré à partir de l’expérience et du vécu professionnel."),
                 ("Transmettre", "Les autres travailleurs sociaux, en particulier les plus jeunes, peuvent s’appuyer "
                                 "sur ces doubles pour obtenir de l’aide selon leur agenda de missions."),
             ]},
            {"t": "img", "src": "liawalk-story", "alt": "Storyboard du scénario d’usage", "size": "wide"},
            {"t": "section", "label": "Anatomie", "title": "Des commandes physiques, une fonction chacune.",
             "list": [
                 ("Sélecteur coulissant", "Change de double numérique pour varier les points de vue."),
                 ("Bouton « encore »", "Fait répéter l’IA avec exactement les mêmes termes."),
                 ("Bouton « lancer »", "Lance l’enregistrement audio d’un appui, le désactive au second."),
                 ("Molette · LED", "Règle le volume · indique l’état de la batterie."),
                 ("Enceinte · micro · jack", "Écouter l’IA en voiture, enregistrer sa voix, écouter en toute discrétion."),
             ]},
            {"t": "img", "src": "liawalk-anatomy", "alt": "Vue annotée du dispositif LIAWALK", "size": "full"},
            {"t": "section", "label": "IA embarquée", "title": "Les données restent sur l’objet.",
             "text": ["Le dispositif embarque une IA de traitement des données qui permet de traiter les informations "
                      "directement en local, sans avoir besoin de les transférer via un cloud."]},
            {"t": "img", "src": "liawalk-float", "alt": "Rendu 3D du dispositif mobile", "size": "wide"},
            {"t": "section", "label": "Station", "title": "« LIA, imprime-moi mes compétences. »",
             "text": ["La zone dédiée accueille la partie mobile qui enregistre et traite les données en déplacement "
                      "grâce à l’IA embarquée. Les informations sont ensuite transférées vers le dispositif fixe pour "
                      "être imprimées ou numérisées, tout en alimentant quotidiennement le mobile avec des doubles "
                      "numériques liés aux interventions et favorisant la sécurité des données."]},
            {"t": "img", "src": "liawalk-station", "alt": "Station fixe qui imprime les compétences", "size": "full"},
        ],
    },
    {
        "slug": "site-ixcampus",
        "title": "Site web",
        "context": "iXcampus",
        "year": "2025",
        "tags": "Webdesign · Identité",
        "cats": ["digital"],
        "thumb": "thumb-ixcampus",
        "cover": "ixcampus-cover",
        "question": (
            "Comment repenser l’identité numérique d’iXcampus pour mieux traduire sa vision, ses valeurs et "
            "ses collaborations ?"
        ),
        "summary": (
            "Refonte du site web : clarifier le positionnement, renforcer la communication et valoriser "
            "l’écosystème d’innovation. Le projet a aussi amené à redéfinir ce qu’est iXcampus : un lieu "
            "d’expérimentation et de collaboration entre étudiants, chercheurs, entreprises et institutions."
        ),
        "meta": [
            ("Contexte", "Projet en alternance · 9 mois"),
            ("Collaboration", "Advitam (identité graphique) & Intuiti (développement)"),
            ("Outils", "Identité graphique · Charte · Figma · After Effects"),
            ("Site", ("ixcampus.eu", "https://ixcampus.eu/")),
        ],
        "blocks": [
            {"t": "section", "label": "Charte graphique", "title": "Harmoniser tous les supports du campus.",
             "text": ["Suite aux recommandations graphiques proposées par un cabinet, nous avons approfondi cette "
                      "réflexion en concevant une charte graphique complète destinée à l’ensemble des collaborateurs "
                      "internes d’iXcampus. Noir, blanc, terra cotta #F36B47 et la Montserrat sur l’ensemble des "
                      "supports : brochures, rapport annuel, publicités, stands."]},
            {"t": "img", "src": "ixcampus-charte", "alt": "Extrait de la charte graphique iXcampus", "size": "wide"},
            {"t": "section", "label": "Maquettes", "title": "Du wireframe au site en ligne, dans Figma."},
            {"t": "imgs", "cols": 2, "items": [
                ("ixcampus-figma-1", "Maquettes desktop du site iXcampus dans Figma"),
                ("ixcampus-figma-2", "Maquettes mobile du site iXcampus dans Figma"),
            ]},
            {"t": "img", "src": "ixcampus-mobile", "alt": "Page d’accueil mobile « Ici, la science devient industrie »", "size": "full"},
            {"t": "link", "href": "https://ixcampus.eu/", "text": "Voir le site en ligne"},
        ],
    },
    {
        "slug": "pentagone",
        "title": "Pentagone",
        "context": "JCDecaux",
        "year": "2024",
        "tags": "Mobilier urbain · NFC",
        "cats": ["produit"],
        "thumb": "thumb-pentagone",
        "cover": "pentagone-cover",
        "question": (
            "Comment motiver les jeunes adultes à participer à des initiatives citoyennes et renforcer leur "
            "engagement envers la démocratie ?"
        ),
        "summary": (
            "Un banc augmenté en mobilier urbain, pensé comme point d’entrée léger vers l’engagement citoyen "
            "local. Structure pentagonale modulaire, borne NFC, QR code et charge USB-C donnant accès à des "
            "contenus civiques."
        ),
        "meta": [
            ("Partenaire", "JCDecaux"),
            ("Durée", "Projet de groupe · 5 mois"),
            ("Mon rôle", "Conception du mobilier · Modélisation 3D · Prototypage physique (découpe laser) + NFC · Interface de l’application"),
            ("Outils", "Sketch · Figma · Rhino 8 · Twinmotion · Suite Adobe · Découpe laser"),
        ],
        "blocks": [
            {"t": "section", "label": "Structure", "title": "Un module pentagonal qui s’assemble selon le lieu."},
            {"t": "img", "src": "pentagone-module", "alt": "Module et combinaisons d’assemblage", "size": "wide"},
            {"t": "imgs", "cols": 2, "items": [
                ("pentagone-plant", "Module végétalisé"), ("pentagone-nfc", "Borne NFC en liège"),
            ]},
            {"t": "section", "label": "Borne NFC", "title": "« Ton impact commence ici. »",
             "text": ["Un geste suffit : approcher son téléphone de la borne pour accéder aux initiatives citoyennes "
                      "locales."]},
            {"t": "img", "src": "pentagone-nfc-detail", "alt": "Détail de la gravure NFC et du QR code", "size": "wide"},
            {"t": "section", "label": "Prototype", "title": "Découpe laser et puce NFC, testés en vrai."},
            {"t": "imgs", "cols": 4, "items": [
                ("pentagone-proto-1", "Prototype de borne NFC, étape 1"), ("pentagone-proto-2", "Prototype, étape 2"),
                ("pentagone-proto-3", "Prototype, étape 3"), ("pentagone-proto-4", "Prototype, étape 4"),
            ]},
            {"t": "section", "label": "Application", "title": "Participer à la reforestation de sa ville."},
            {"t": "imgs", "cols": 3, "items": [
                ("pentagone-app-1", "Écran d’accueil de l’application"), ("pentagone-app-2", "Écran de détail d’une initiative"),
                ("pentagone-app-lock", "Notification sur l’écran verrouillé"),
            ]},
            {"t": "img", "src": "pentagone-scene", "alt": "Mise en situation des bancs dans l’espace public", "size": "full"},
        ],
    },
    {
        "slug": "lannion",
        "title": "Étude à Lannion",
        "context": "iXcampus",
        "year": "2025",
        "tags": "Recherche · Workshops",
        "cats": ["recherche"],
        "thumb": "thumb-lannion",
        "cover": "lannion-cover",
        "subtitle": "Faire Campus, Penser un territoire",
        "question": (
            "Comment transformer la relocalisation de l’ENSSAT, désavantageuse pour Lannion-Trégor, en "
            "opportunité de design territorial ?"
        ),
        "summary": (
            "L’étude visait à consulter les étudiants pour co-construire le nouveau campus selon leurs besoins, "
            "mais aussi à réinventer les mobilités et les loisirs lors du transfert de l’ENSSAT hors de son site "
            "historique en centre-ville."
        ),
        "meta": [
            ("Contexte", "Projet en alternance"),
            ("Durée", "Équipe de 2 · 2 mois"),
            ("Rôle", "Planification et création des ateliers · Enquête de terrain · Animation des workshops · Analyse qualitative · Restitution"),
        ],
        "blocks": [
            {"t": "section", "label": "Restitution",
             "title": "Étude de l’expérience étudiante à Lannion Trégor Communauté.",
             "text": ["Ateliers, enquête de terrain et analyse qualitative, restitués dans un document de synthèse "
                      "qui projette l’expérience étudiante future sur le territoire."]},
            {"t": "imgs", "cols": 2, "items": [
                ("lannion-book", "Couverture de l’étude"), ("lannion-spread", "Double page : scénario 2030"),
            ]},
        ],
    },
    {
        "slug": "design-fablab",
        "title": "Design Fablab",
        "context": "Projet personnel",
        "year": "2026",
        "tags": "Outil · IA · UX",
        "cats": ["digital"],
        "thumb": "thumb-fablab",
        "cover": "fablab-canvas",
        "subtitle": "Espace de travail augmenté",
        "question": (
            "Comment préserver la souveraineté du workflow et des données du designer face à des IA censées "
            "faciliter la démarche, mais qui l’opacifient ?"
        ),
        "summary": (
            "Un canvas où l’IA est un bloc parmi d’autres, au même niveau que les audios, les recherches et les "
            "notes. La structure du projet reste sous les yeux."
        ),
        "meta": [
            ("Contexte", "Projet personnel · seul"),
            ("Outils", "Figma · Claude Code"),
        ],
        "blocks": [
            {"t": "section", "label": "Constat", "title": "Le fil de conversation impose son ordre.",
             "text": ["On avance au rythme de l’IA, on perd la vue d’ensemble du projet et on finit par ne suivre "
                      "qu’elle, et les données sensibles et confidentielles se retrouvent en ligne."]},
            {"t": "section", "label": "Les blocs", "title": "Des blocs pensés pour la démarche créative.",
             "list": [
                 ("Analyse les ressources", "Convoqué au besoin, refermé ensuite. Il ne prend jamais tout l’écran."),
                 ("Souveraineté des informations", "Enregistrement transcrit en local, rattaché au point du projet concerné."),
                 ("Design thinking", "Des blocs pensés pour accompagner le designer dans ses démarches créatives."),
             ]},
            {"t": "imgs", "cols": 2, "items": [
                ("fablab-block-1", "Blocs de problématisation et carte d’empathie"),
                ("fablab-block-2", "Synthèse générée et rattachée au projet"),
            ]},
            {"t": "img", "src": "fablab-cover", "alt": "Bloc audio, analyse et persona reliés sur le canvas", "size": "narrow"},
        ],
    },
]

FILTERS = [("all", "Tout"), ("digital", "Digital"), ("produit", "Produit"), ("recherche", "Recherche")]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
e = escape
_sizes = {}


def ver(path):
    """Empreinte du fichier : force le navigateur à recharger CSS/JS modifiés."""
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


def size(name):
    if name not in _sizes:
        with Image.open(IMG / f"{name}.webp") as im:
            _sizes[name] = im.size
    return _sizes[name]


def img(name, alt, base, cls="", eager=False, extra=""):
    w, h = size(name)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{base}assets/img/{name}.webp" alt="{e(alt)}" width="{w}" height="{h}" '
            f'{load} decoding="async"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}{extra}>')


ARROW = ('<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" '
         'fill="none" stroke="currentColor" stroke-width="1.5"/></svg>')
ARROW_UP = ('<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9" '
            'fill="none" stroke="currentColor" stroke-width="1.5"/></svg>')


def roll(text):
    """Texte qui 'roule' au survol (deux copies empilées)."""
    t = e(text)
    return f'<span class="roll"><span class="roll-in"><span>{t}</span><span aria-hidden="true">{t}</span></span></span>'


def head(title, desc, base):
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#FAFAFA">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{base}assets/img/thumb-vision.webp">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/main.css?v={ver("assets/css/main.css")}">
<script>document.documentElement.classList.add('js')</script>
</head>"""


def nav(base, home):
    p = "" if home else f"{base}index.html"
    return f"""
<header class="nav" data-nav>
  <a class="nav-brand" href="{base}index.html" data-magnetic>{roll("Théo Petitimbert")}</a>
  <nav class="nav-links" aria-label="Navigation principale">
    <a href="{p}#projets">{roll("Projets")}</a>
    <a href="{p}#a-propos">{roll("À propos")}</a>
    <a href="#contact">{roll("Contact")}</a>
  </nav>
  <span class="nav-time mono" aria-hidden="true"><span class="dot"></span>Paris <span data-clock>--:--</span></span>
</header>"""


def footer(base):
    return f"""
<footer class="contact" id="contact">
  <div class="wrap">
    <p class="mono label">(Contact)</p>
    <h2 class="contact-title" data-reveal>Parlons design.</h2>
    <button class="contact-mail" type="button" data-copy="{SITE['email']}" data-cursor="Copier" data-magnetic>
      <span class="contact-mail-text">{e(SITE['email'])}</span>
      <span class="contact-mail-hint mono" data-copy-hint>Cliquer pour copier</span>
    </button>
    <div class="contact-grid">
      <div><p class="mono label">E-mail</p><a class="ulink" href="mailto:{SITE['email']}">{e(SITE['email'])}</a></div>
      <div><p class="mono label">Téléphone</p><a class="ulink" href="tel:{SITE['phone_href']}">{e(SITE['phone'])}</a></div>
      <div><p class="mono label">Réseau</p><a class="ulink" href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn {ARROW_UP}</a></div>
      <div><p class="mono label">Heure locale</p><span>Paris · <span data-clock>--:--</span></span></div>
    </div>
    <div class="contact-bottom mono">
      <span>© 2026 Théo Petitimbert</span>
      <span>Portfolio 2026</span>
      <a href="#top" class="ulink" data-top>Retour en haut ↑</a>
    </div>
  </div>
</footer>
<div class="toast mono" role="status" aria-live="polite" data-toast></div>
<div class="cursor" aria-hidden="true"><span class="cursor-label"></span></div>
<script src="{base}assets/js/main.js?v={ver("assets/js/main.js")}" defer></script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Accueil
# ---------------------------------------------------------------------------
def project_rows(base):
    rows = []
    for i, p in enumerate(PROJECTS, 1):
        rows.append(f"""
      <li class="row" data-cats="{' '.join(p['cats'])}" style="view-transition-name: row-{p['slug']}">
        <a href="{base}projets/{p['slug']}.html" data-preview="{base}assets/img/{p['thumb']}.webp" data-slug="{p['slug']}" data-cursor="Voir">
          <span class="row-thumb">{img(p['thumb'], p['title'], base)}</span>
          <span class="row-num mono">{i:02d}</span>
          <span class="row-title">{roll(p['title'])}</span>
          <span class="row-ctx">{e(p['context'])}</span>
          <span class="row-tags">{e(p['tags'])}</span>
          <span class="row-year mono">{p['year']}</span>
          <span class="row-go">{ARROW}</span>
        </a>
      </li>""")
    return "".join(rows)


def build_index():
    base = ""
    counts = {k: (len(PROJECTS) if k == "all" else sum(k in p["cats"] for p in PROJECTS)) for k, _ in FILTERS}
    filters = "".join(
        f'<button type="button" class="chip{" is-active" if k == "all" else ""}" data-filter="{k}" '
        f'aria-pressed="{"true" if k == "all" else "false"}">{lbl}<sup>{counts[k]}</sup></button>'
        for k, lbl in FILTERS)
    letters = lambda w: "".join(f'<span class="ch" style="--i:{i}">{e(c)}</span>' for i, c in enumerate(w))
    roles = "".join(f'<span class="role">{e(r)}</span>' for r in SITE["roles"])
    method = "".join(f"""
        <li class="step" data-reveal style="--d:{i * 80}ms">
          <span class="mono step-num">0{i + 1}</span>
          <h3>{e(t)}</h3>
          <p>{e(d)}</p>
        </li>""" for i, (t, d) in enumerate(STUDIO["method"]))
    studio_imgs = "".join(f"""
        <figure class="studio-fig" data-reveal style="--d:{i * 80}ms">
          <div class="frame">{img(n, c, base)}</div>
          <figcaption class="mono">{e(c)}</figcaption>
        </figure>""" for i, (n, c) in enumerate(STUDIO["images"]))
    cv = "".join(
        f'<div class="cv-block" data-reveal><h3 class="mono label">{e(k)}</h3><ul>' +
        "".join(f'<li><span class="mono cv-date">{e(d)}</span><strong>{e(t)}</strong><span>{e(x)}</span></li>'
                for d, t, x in items) + "</ul></div>"
        for k, items in CV.items())
    skills = "".join(
        f'<div class="cv-block" data-reveal><h3 class="mono label">{e(k)}</h3><ul class="plain">' +
        "".join(f"<li>{e(x)}</li>" for x in items) + "</ul></div>"
        for k, items in SKILLS.items())
    words = " ".join(f'<span class="w">{e(w)}</span>' for w in SITE["bio"].split())

    html = head("Théo Petitimbert · Product & Global designer",
                "Portfolio 2026 de Théo Petitimbert, product designer, UX/UI designer et designer global.", base)
    html += f"""
<body class="home" id="top">
<a class="skip" href="#projets">Aller aux projets</a>
{nav(base, True)}
<main>
  <section class="hero" data-hero aria-label="Introduction">
    <canvas class="hero-bg" data-hero-bg aria-hidden="true"></canvas>
    <canvas class="hero-grid" data-hero-grid aria-hidden="true"></canvas>
    <div class="hero-grain" aria-hidden="true"></div>
    <div class="hero-inner">
      <div class="hero-top">
        <p class="hero-roles" aria-label="{e(', '.join(SITE['roles']))}"><span class="roles" aria-hidden="true">{roles}</span></p>
        <p class="hero-lede">Je transforme des sujets complexes en produits, services et expériences utiles, compréhensibles et désirables.</p>
      </div>
      <h1 class="hero-name" aria-label="Théo Petitimbert">
        <span class="line" aria-hidden="true">{letters("Théo")}</span>
        <span class="line" aria-hidden="true">{letters("Petitimbert")}</span>
      </h1>
      <div class="hero-bottom mono">
        <span>Portfolio · 2026</span>
        <span class="hide-s">Master 2 Design Global · CY école de design</span>
        <a href="#projets" class="hero-scroll" data-cursor="Go">Défiler <span class="scroll-line"></span></a>
      </div>
    </div>
  </section>

  <div class="sheet">
    <section class="intro wrap" aria-label="Présentation">
      <p class="mono label">(Designer global)</p>
      <p class="intro-text" data-scrub>{words}</p>
    </section>

    <section class="work wrap" id="projets" aria-labelledby="projets-title">
      <div class="work-head">
        <h2 id="projets-title" class="section-title">Projets <sup class="mono" data-count>{len(PROJECTS):02d}</sup></h2>
        <div class="work-tools">
          <div class="chips" role="group" aria-label="Filtrer les projets">{filters}</div>
          <div class="view-toggle" role="group" aria-label="Affichage">
            <button type="button" class="vt is-active" data-view="list" aria-pressed="true" aria-label="Vue liste">
              <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M1 4h14M1 8h14M1 12h14" stroke="currentColor" stroke-width="1.3"/></svg></button>
            <button type="button" class="vt" data-view="grid" aria-pressed="false" aria-label="Vue grille">
              <svg viewBox="0 0 16 16" aria-hidden="true"><rect x="1.5" y="1.5" width="5" height="5" fill="none" stroke="currentColor" stroke-width="1.3"/><rect x="9.5" y="1.5" width="5" height="5" fill="none" stroke="currentColor" stroke-width="1.3"/><rect x="1.5" y="9.5" width="5" height="5" fill="none" stroke="currentColor" stroke-width="1.3"/><rect x="9.5" y="9.5" width="5" height="5" fill="none" stroke="currentColor" stroke-width="1.3"/></svg></button>
          </div>
        </div>
      </div>
      <div class="list-legend mono" aria-hidden="true">
        <span>N°</span><span>Projet</span><span>Contexte</span><span>Discipline</span><span>Année</span><span></span>
      </div>
      <ol class="list" data-list data-view="list">{project_rows(base)}
      </ol>
    </section>

    <section class="studio wrap" aria-labelledby="studio-title">
      <div class="split">
        <div>
          <p class="mono label">(Expérience · 2024 → 2026)</p>
          <h2 id="studio-title" class="section-title">Design Studio<br><span class="muted">iXcampus, en alternance</span></h2>
        </div>
        <div class="studio-intro">
          <p data-reveal>{e(STUDIO['intro'])}</p>
          <dl class="studio-dl" data-reveal>
            <div><dt class="mono label">Missions</dt><dd>{e(STUDIO['missions'])}</dd></div>
            <div><dt class="mono label">Livrables</dt><dd>{e(STUDIO['deliverables'])}</dd></div>
          </dl>
        </div>
      </div>
      <ol class="steps">{method}
      </ol>
      <div class="studio-figs">{studio_imgs}
      </div>
    </section>

    <section class="about wrap" id="a-propos" aria-labelledby="about-title">
      <div class="about-grid">
        <figure class="about-portrait" data-reveal>
          <div class="frame">{img("portrait", "Portrait de Théo Petitimbert", base)}</div>
        </figure>
        <div class="about-body">
          <p class="mono label">(À propos)</p>
          <h2 id="about-title" class="about-lead" data-reveal>{e(SITE['bio'])}</h2>
          {''.join(f'<p class="about-p" data-reveal>{e(x)}</p>' for x in SITE['bio_more'])}
          <div class="cv">{cv}{skills}</div>
        </div>
      </div>
    </section>
  </div>
</main>"""
    html += footer(base)
    (ROOT / "index.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# Pages projet
# ---------------------------------------------------------------------------
def render_block(b, base):
    t = b["t"]
    if t == "section":
        body = ""
        if b.get("text"):
            body += "".join(f"<p>{e(x)}</p>" for x in b["text"])
        if b.get("list"):
            body += '<ol class="points">' + "".join(
                f'<li data-reveal><span class="mono">{i:02d}</span><div><h4>{e(h)}</h4><p>{e(x)}</p></div></li>'
                for i, (h, x) in enumerate(b["list"], 1)) + "</ol>"
        title = f'<h3 class="block-title">{e(b["title"])}</h3>' if b.get("title") else ""
        return f"""
    <section class="block wrap">
      <p class="mono label block-label">({e(b['label'])})</p>
      <div class="block-body" data-reveal>{title}{body}</div>
    </section>"""
    if t == "img":
        cap = f'<figcaption class="mono">{e(b["caption"])}</figcaption>' if b.get("caption") else ""
        return f"""
    <figure class="media media-{b.get('size', 'wide')} wrap" data-reveal>
      <div class="frame">{img(b['src'], b['alt'], base)}</div>{cap}
    </figure>"""
    if t == "imgs":
        items = "".join(f'<div class="frame" data-reveal style="--d:{i * 70}ms">{img(s, a, base)}</div>'
                        for i, (s, a) in enumerate(b["items"]))
        cap = f'<figcaption class="mono">{e(b["caption"])}</figcaption>' if b.get("caption") else ""
        return f"""
    <figure class="media wrap">
      <div class="gallery cols-{b.get('cols', 2)}">{items}</div>{cap}
    </figure>"""
    if t == "quotes":
        items = "".join(f"""
        <figure class="quote" data-reveal style="--d:{i * 90}ms">
          <div class="frame">{img(s, "Persona", base)}</div>
          <blockquote>« {e(q)} »</blockquote>
        </figure>""" for i, (s, q) in enumerate(b["items"]))
        return f"""
    <section class="block wrap">
      <p class="mono label block-label">({e(b['label'])})</p>
      <div class="quotes">{items}</div>
    </section>"""
    if t == "link":
        return f"""
    <div class="block wrap">
      <span></span>
      <a class="cta" href="{b['href']}" target="_blank" rel="noopener" data-magnetic data-cursor="Ouvrir">{roll(b['text'])} {ARROW_UP}</a>
    </div>"""
    raise ValueError(t)


def build_project(i, p):
    base = "../"
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    meta = ""
    for k, v in p["meta"]:
        val = (f'<a class="ulink" href="{v[1]}" target="_blank" rel="noopener">{e(v[0])} {ARROW_UP}</a>'
               if isinstance(v, tuple) else e(v))
        meta += f'<div><dt class="mono label">{e(k)}</dt><dd>{val}</dd></div>'
    letters = "".join(f'<span class="ch" style="--i:{j}">{e(c) if c != " " else "&nbsp;"}</span>'
                      for j, c in enumerate(p["title"]))
    sub = p.get("subtitle", p["context"])
    html = head(f"{p['title']} · Théo Petitimbert", p["summary"], base)
    html += f"""
<body class="project" id="top">
{nav(base, False)}
<main>
  <article class="p-article" data-slug="{p['slug']}" data-title="{e(p['title'])} · Théo Petitimbert" data-next="{nxt['slug']}.html">
    <header class="p-head wrap">
      <div class="p-crumbs mono">
        <a href="../index.html#projets" class="ulink back">← Index</a>
        <span>{i + 1:02d} / {len(PROJECTS):02d}</span>
      </div>
      <p class="mono p-kicker">{e(sub)} · {e(p['context']) if sub != p['context'] else ''}{' · ' if sub != p['context'] else ''}{p['year']}</p>
      <h1 class="p-title" aria-label="{e(p['title'])}"><span class="line" aria-hidden="true">{letters}</span></h1>
      <div class="p-intro">
        <p class="p-question">{e(p['question'])}</p>
        <div class="p-side">
          <p class="p-summary">{e(p['summary'])}</p>
          <dl class="p-meta">{meta}</dl>
        </div>
      </div>
    </header>
    <figure class="p-cover wrap">
      <div class="frame">{img(p['cover'], p['title'], base, eager=True, extra=f' style="view-transition-name: cover-{p["slug"]}"')}</div>
    </figure>
    {''.join(render_block(b, base) for b in p['blocks'])}
  </article>

  <a class="next wrap" href="{nxt['slug']}.html" data-preview="../assets/img/{nxt['thumb']}.webp" data-slug="{nxt['slug']}" data-cursor="Suivant">
    <span class="mono label">(Projet suivant)</span>
    <span class="next-title">{roll(nxt['title'])}</span>
    <span class="next-meta mono">{e(nxt['context'])} · {nxt['year']} {ARROW}</span>
  </a>
</main>"""
    html += footer(base)
    out = ROOT / "projets"
    out.mkdir(exist_ok=True)
    (out / f"{p['slug']}.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build_index()
    for i, p in enumerate(PROJECTS):
        build_project(i, p)
    print(f"OK · index.html + {len(PROJECTS)} pages projet")
