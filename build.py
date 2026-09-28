"""
Générateur du portfolio de Théo Petitimbert.

Tout le contenu (projets, textes, CV, images) est dans ce fichier.
Modifier puis lancer :  python build.py
Le site statique est écrit à la racine (index.html, a-propos.html, projets/*.html).

Chaque section de page a sa fonction render_* ici, sa feuille assets/css/<section>.css
et, si besoin, son script assets/js/<section>.js ; l'élément racine porte data-chunk.
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

# ---------------------------------------------------------------------------
# Mise en page : choix d'images, d'ordre et de libellés tirés du contenu
# ci-dessus (aucune information nouvelle).
# ---------------------------------------------------------------------------
INTRO_LINES = ["Je transforme", "des sujets complexes", "en expériences utiles", "et désirables."]

# Carrousel du hero : projet, visuel plein cadre et recadrage
HERO_SLIDES = [
    # fit : visuel détouré posé au centre (fx/fy = point focal, h = hauteur) ; sinon plein cadre
    {"slug": "vision", "img": "vision-screens", "alt": "Trois écrans de l’application Vision",
     "fit": {"h": "84%", "fx": "52%", "fy": "50%"}},
    {"slug": "liawalk", "img": "liawalk-float", "alt": "Rendu 3D du dispositif mobile LIAWALK",
     "pos": "50% 62%", "zoom": 1.16, "origin": "62% 64%"},
    {"slug": "pentagone", "img": "pentagone-cover", "alt": "Module pentagonal en liège, vue de dessus",
     "fit": {"h": "86%", "fx": "73%", "fy": "35%"}},
]

HERO_DIM = 0.9  # les visuels détourés sont légèrement assombris pour un fond gris

# Visuel de chaque projet dans la grille de l'accueil
CARDS = {
    "vision": "vision-cover", "liawalk": "liawalk-cover", "pentagone": "pentagone-nfc",
    "site-ixcampus": "ixcampus-mobile", "lannion": "lannion-book", "design-fablab": "fablab-cover",
}
CARDS_VISIBLE = 4  # les suivants s'affichent avec « Voir tous les projets »

# Organisations citées dans le CV et les projets (nom, relation, variante typographique)
CLIENTS = [
    ("iXcampus", "Alternance · 2024 → 2026", "a"),
    ("Inria", "Partenaire · LIAWALK", "c"),
    ("JCDecaux", "Partenaire · Pentagone", "b"),
    ("SNCF Réseau", "Stage · 2023", "d"),
    ("CY école de design", "Formation · Master 2", "e"),
    ("HOWEST", "Erasmus · 2024", "c"),
    ("TrembLess", "Startup · Design Studio", "a"),
    ("VestaClim", "Startup · Design Studio", "d"),
    ("Iroony", "Startup · Design Studio", "e"),
    ("PiPop", "Startup · Design Studio", "a"),
    ("Advitam", "Identité · Site iXcampus", "b"),
    ("Intuiti", "Développement · Site iXcampus", "d"),
]
MARQUEE = ["Partenaires", "Clients", "Collaborations"]


# Savoir-faire, disciplines et outils, repris du CV, des métadonnées projet et des légendes du studio
SERVICES = [
    "Design global", *SKILLS["Savoir-faire"],
    "Enquête de terrain", "Analyse qualitative", "Design thinking", "Webdesign", "Identité graphique",
    "Charte graphique", "Stratégie de communication", "Graphisme", "Photographie", "Maquettage",
    "Modélisation 3D", "Prototypage physique", "Découpe laser", "Mobilier urbain",
    "Figma", "Sketch", "Suite Adobe", "After Effects", "Rhino 8", "Twinmotion", "Vizcom",
    "Claude Code", "GitHub", "Outils IA",
]

# Placement des séries d'images : (colonne de départ, largeur en colonnes, décalage vertical px)
SET_LAYOUT = {
    1: [(3, 8, 0)],
    2: [(1, 7, 0), (10, 3, 0)],
    3: [(1, 5, 0), (7, 3, 120), (10, 3, 0)],
    4: [(1, 3, 0), (4, 3, 90), (7, 3, 0), (10, 3, 90)],
    5: [(1, 5, 0), (7, 3, 110), (10, 3, 0), (2, 4, 0), (7, 5, 0)],
}
STUDIO_LAYOUT = [(1, 5, 0), (8, 4, 140), (3, 4, 0), (8, 5, 80)]

FONTS = ("https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wdth,wght@"
         "0,75..100,400..700;1,75..100,400..700&display=swap")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
e = escape
_sizes = {}
_tones = {}


def ver(path):
    """Empreinte du fichier : force le navigateur à recharger CSS/JS modifiés."""
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


def size(name):
    if name not in _sizes:
        with Image.open(IMG / f"{name}.webp") as im:
            _sizes[name] = im.size
    return _sizes[name]


def tone(name, box=(0, .35, .6, 1)):
    """'dark' si la zone (x0, y0, x1, y1 en fractions) de l'image est sombre :
    le texte posé dessus passe alors en blanc."""
    key = (name, box)
    if key not in _tones:
        with Image.open(IMG / f"{name}.webp") as im:
            w, h = im.size
            zone = im.convert("L").crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
            _tones[key] = "dark" if zone.resize((1, 1), Image.BOX).getpixel((0, 0)) < 150 else "light"
    return _tones[key]


def edge_color(name, k=1.0):
    """Couleur moyenne du bord de l'image (fond studio), éventuellement assombrie."""
    with Image.open(IMG / f"{name}.webp") as im:
        rgb = im.convert("RGB")
        w, h = rgb.size
        b = max(4, w // 50)
        strips = [rgb.crop((0, 0, w, b)), rgb.crop((0, h - b, w, h)), rgb.crop((0, 0, b, h)), rgb.crop((w - b, 0, w, h))]
        cols = [s.resize((1, 1), Image.BOX).getpixel((0, 0)) for s in strips]
    return "rgb({})".format(",".join(str(round(sum(c[i] for c in cols) / 4 * k)) for i in range(3)))


def img(name, alt, base, cls="", eager=False):
    w, h = size(name)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    klass = f' class="{cls}"' if cls else ""
    return (f'<img src="{base}assets/img/{name}.webp" alt="{e(alt)}" width="{w}" height="{h}" '
            f'{load} decoding="async"{klass}>')


def svg(d, cls="arrow", w=1.5):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="{d}" fill="none" '
            f'stroke="currentColor" stroke-width="{w}"/></svg>')


ARROW = svg("M4 12h16M14 6l6 6-6 6")
ARROW_L = svg("M20 12H4M10 6l-6 6 6 6")
ARROW_UP = svg("M7 17L17 7M8 7h9v9")
ARROW_TOP = svg("M12 20V4M6 10l6-6 6 6")
PLUS = svg("M12 2v20M2 12h20", "marquee-plus", 1.6)
MARK = ('<svg class="nav-mark" viewBox="0 0 22 22" aria-hidden="true"><path fill="currentColor" '
        'fill-rule="evenodd" d="M0 0h13v3.4H8.4V22H4.6V3.4H0zM10.6 7h5.3a4.8 4.8 0 0 1 0 9.6h-1.6V22h-3.7z'
        'm3.7 3.2v3.2h1.5a1.6 1.6 0 0 0 0-3.2z"/></svg>')


def head(title, desc, base, css, og="thumb-vision"):
    links = "\n".join(
        f'<link rel="stylesheet" href="{base}assets/css/{c}.css?v={ver(f"assets/css/{c}.css")}">'
        for c in ["base", "nav", *css])
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#F3F3F2">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{base}assets/img/{og}.webp">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
{links}
<script>document.documentElement.classList.add('js')</script>
</head>"""


def scripts(base, js):
    tags = "".join(f'\n<script src="{base}assets/js/{j}.js?v={ver(f"assets/js/{j}.js")}" defer></script>'
                   for j in ["base", *js])
    return f"{tags}\n</body>\n</html>\n"


def section_copy(b):
    """Titre, paragraphes et liste numérotée d'un bloc 'section'."""
    out = f'<h2 class="g-title">{e(b["title"])}</h2>' if b.get("title") else ""
    out += "".join(f'<p class="g-p">{e(x)}</p>' for x in b.get("text", []))
    if b.get("list"):
        out += '<ol class="g-list">' + "".join(
            f'<li><span class="g-n" aria-hidden="true">{n:02d}</span><h3>{e(h)}</h3><p>{e(x)}</p></li>'
            for n, (h, x) in enumerate(b["list"], 1)) + "</ol>"
    return out


def figure(name, alt, base, n, caption=None, cls="", style=""):
    """Image au ratio naturel + petite légende (texte à gauche, numéro à droite)."""
    w, h = size(name)
    text = caption or alt
    hide = "" if caption else ' aria-hidden="true"'
    long = " g-cap--long" if caption else ""
    st = f' style="{style}"' if style else ""
    return f"""<figure class="g-fig{cls}" data-reveal{st}>
        <div class="frame" style="aspect-ratio:{w}/{h}">{img(name, alt, base)}</div>
        <figcaption class="g-cap{long}"><span{hide}>{e(text)}</span><span aria-hidden="true">{n:02d}</span></figcaption>
      </figure>"""


# ---------------------------------------------------------------------------
# Blocs partagés
# ---------------------------------------------------------------------------
def render_nav(base, current):
    home = f"{base}index.html"
    items = [("home", "Accueil", home), ("work", "Projets", f"{home}#projets"),
             ("about", "À propos", f"{base}a-propos.html"), ("contact", "Contact", "#contact")]
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if k == current else ""}>{t}</a>' for k, t, h in items)
    return f"""
  <header class="nav" data-nav>
    <a class="nav-logo" href="{home}" aria-label="Théo Petitimbert, accueil">{MARK}<span class="nav-logo-name" aria-hidden="true">Théo Petitimbert</span></a>
    <nav class="nav-pill" aria-label="Navigation principale">{links}</nav>
    <a class="nav-cta" href="mailto:{SITE['email']}">Me contacter</a>
  </header>"""


def render_next(href, lines, sub):
    title = "".join(f'<span class="line"><span>{e(x)}</span></span>' for x in lines)
    return f"""
  <section class="next" data-chunk="next" aria-label="Page suivante">
    <p class="next-label">Page suivante</p>
    <a class="next-link" href="{href}" data-reveal>
      <span class="next-title">{title}</span>
      <span class="next-sub">{e(sub)} {ARROW}</span>
    </a>
  </section>"""


def render_footer(base):
    home = f"{base}index.html"
    lis = lambda links: "".join(f'<li><a href="{h}">{e(t)}</a></li>' for t, h in links)
    pages = [("Accueil", home), ("Projets", f"{home}#projets"), ("À propos", f"{base}a-propos.html")]
    projs = [(p["title"], f"{base}projets/{p['slug']}.html") for p in PROJECTS]
    half = (len(projs) + 1) // 2
    name = SITE["name"]
    return f"""
<footer class="footer" id="contact" data-chunk="footer" data-tone="dark">
  <div class="footer-cols grid">
    <div class="footer-col footer-col--cta">
      <h2 class="footer-h">Travaillons ensemble</h2>
      <a class="footer-mail" href="mailto:{SITE['email']}"><span>{e(SITE['email'])}</span>{ARROW_UP}</a>
      <ul class="footer-list footer-list--row">
        <li><a href="tel:{SITE['phone_href']}">{e(SITE['phone'])}</a></li>
        <li>{e(' · '.join(SITE['roles']))}</li>
      </ul>
    </div>
    <nav class="footer-col footer-col--map" aria-label="Plan du site">
      <h2 class="footer-h">Plan du site</h2>
      <div class="footer-map">
        <ul class="footer-list">{lis(pages)}</ul>
        <ul class="footer-list">{lis(projs[:half])}</ul>
        <ul class="footer-list">{lis(projs[half:])}</ul>
      </div>
    </nav>
    <p class="footer-col footer-time"><span class="footer-h">Heure locale · Paris</span><strong data-clock>--:--</strong></p>
  </div>
  <p class="footer-mark" data-reveal><span class="fm-w"><span class="fm-t">{e(name)}</span></span></p>
  <div class="footer-bar">
    <a href="#top">{ARROW_TOP} Retour en haut</a>
    <span>© 2026 {e(name)} · Portfolio 2026</span>
    <a href="{SITE['linkedin']}" target="_blank" rel="noopener">Suivre sur LinkedIn {ARROW_UP}</a>
  </div>
</footer>"""


# ---------------------------------------------------------------------------
# Accueil : un rendu par section
# ---------------------------------------------------------------------------
def render_hero(base):
    by = {p["slug"]: p for p in PROJECTS}
    n = len(HERO_SLIDES)
    slides = nums = ""
    for i, s in enumerate(HERO_SLIDES):
        p = by[s["slug"]]
        on = " is-active" if i == 0 else ""
        style = f'--pos:{s.get("pos", "50% 50%")};--zoom:{s.get("zoom", 1)};--origin:{s.get("origin", "50% 50%")}'
        fit = s.get("fit")
        if fit:
            style += (f';--h:{fit["h"]};--fx:{fit["fx"]};--fy:{fit["fy"]};'
                      f'--b:{HERO_DIM};--slide-bg:{edge_color(s["img"], HERO_DIM)}')
        mode = " hero-slide--fit" if fit else ""
        slides += f"""
      <article class="hero-slide{mode}{on}" aria-roledescription="diapositive" aria-label="{i + 1} sur {n}" style="{style}">
        <div class="hero-media">{img(s['img'], s['alt'], base, eager=i == 0)}</div>
        <h2 class="hero-title"><a href="{base}projets/{p['slug']}.html"><span>{e(p['title'])}</span></a></h2>
        <p class="hero-caption">{e(p['context'])} · {p['year']}<br>{e(p['tags'])}</p>
      </article>"""
        nums += f"""
      <button type="button" class="hero-num{on}" data-go="{i}" aria-label="Afficher {e(p['title'])}"><span>{i + 1:02d}.</span><i class="track" aria-hidden="true"><i class="fill"></i></i></button>"""
    return f"""
  <section class="hero" data-chunk="hero" data-hero aria-roledescription="carrousel" aria-label="Projets à la une">
    <a class="skip" href="#intro">Aller au contenu</a>
    {render_nav(base, "home")}
    <h1 class="sr-only">Théo Petitimbert · {e(', '.join(SITE['roles']))}</h1>
    <div class="hero-slides">{slides}
    </div>
    <div class="hero-index">{nums}
    </div>
    <div class="hero-bar">
      <a class="hero-scroll" href="#intro"><i aria-hidden="true"></i>Défiler</a>
      <div class="hero-arrows">
        <button type="button" data-prev aria-label="Projet précédent">{ARROW_L}</button>
        <span>Projets à la une</span>
        <button type="button" data-next aria-label="Projet suivant">{ARROW}</button>
      </div>
      <span>Portfolio 2026</span>
    </div>
  </section>"""


def render_intro(base):
    lines = "".join(f'<span class="line">{e(x)}</span>' for x in INTRO_LINES)
    return f"""
  <section class="intro grid" id="intro" data-chunk="intro" aria-label="Présentation">
    <h2 class="intro-title" data-reveal>{lines}</h2>
    <div class="intro-side" data-reveal style="--d:.15s">
      <p>{e(SITE['bio_more'][0])}</p>
      <a class="btn" href="{base}a-propos.html"><span>Mon parcours</span><span class="btn-ico">{ARROW}</span></a>
    </div>
  </section>"""


def render_work(base):
    pos = "abcdef"

    def card(i, p):
        return f"""
      <article class="card card--{pos[i % 6]}" data-reveal>
        <a href="{base}projets/{p['slug']}.html">
          <span class="card-num" aria-hidden="true">{i + 1:02d}</span>
          <span class="card-frame frame">{img(CARDS[p['slug']], '', base)}</span>
          <span class="card-meta"><span class="card-title">{e(p['title'])}</span><span class="card-cat">{e(p['tags'])}</span></span>
        </a>
      </article>"""

    first = "".join(card(i, p) for i, p in enumerate(PROJECTS[:CARDS_VISIBLE]))
    rest = "".join(card(i, p) for i, p in enumerate(PROJECTS) if i >= CARDS_VISIBLE)
    return f"""
  <section class="work" id="projets" data-chunk="work" aria-labelledby="work-title">
    <h2 id="work-title" class="sr-only">Projets</h2>
    <div class="work-grid grid">{first}
      <div class="work-more" id="work-more">{rest}
      </div>
    </div>
    <div class="work-foot">
      <button type="button" class="work-toggle" data-more-toggle aria-expanded="false" aria-controls="work-more" data-close-label="Voir moins de projets" hidden>
        <span class="work-plus" aria-hidden="true"></span>
        <span class="work-all"><span data-more-label>Voir tous les projets</span><sup>{len(PROJECTS):02d}</sup></span>
      </button>
    </div>
  </section>"""


def render_clients(base):
    track = "".join(f"<span>{e(w)}</span>{PLUS}" for w in MARQUEE * 2)
    tiles = "".join(f"""
      <li class="logo"><span class="logo-tag">{e(tag)}</span><span class="logo-name logo-name--{v}">{e(name)}</span></li>"""
                    for name, tag, v in CLIENTS)
    return f"""
  <section class="clients" data-chunk="clients" data-tone="dark" aria-labelledby="clients-title">
    <h2 id="clients-title" class="sr-only">Partenaires, clients et collaborations</h2>
    <div class="marquee" aria-hidden="true"><div class="marquee-track">{track}</div><div class="marquee-track">{track}</div></div>
    <ul class="logos">{tiles}
    </ul>
  </section>"""


def render_services(base):
    items = "".join(f"\n      <li>{e(s)}</li>" for s in SERVICES)
    return f"""
  <section class="services grid" data-chunk="services" aria-labelledby="services-title">
    <h2 class="services-label" id="services-title">Savoir-faire, outils<br>et expertises</h2>
    <ul class="services-list" data-services>{items}
    </ul>
  </section>"""


def build_index():
    base = ""
    html = head("Théo Petitimbert · Product & Global designer",
                "Portfolio 2026 de Théo Petitimbert, product designer, UX/UI designer et designer global.", base,
                ["hero", "intro", "work", "clients", "services", "next", "footer"])
    html += f"""
<body class="page-home" id="top">
<main id="main">{render_hero(base)}{render_intro(base)}{render_work(base)}{render_clients(base)}{render_services(base)}{render_next("a-propos.html", ["Parcours", "& savoir-faire"], "Découvrir le parcours")}
</main>{render_footer(base)}{scripts(base, ["hero", "work", "services"])}"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# Pages projet : un rendu par section
# ---------------------------------------------------------------------------
def render_phero(i, p, base):
    cover = p["cover"]
    t = tone(cover)
    dark = ' data-tone="dark"' if t == "dark" else ""
    sub = p.get("subtitle", p["context"])
    return f"""
  <section class="phero phero--{t}" data-chunk="phero"{dark} aria-labelledby="p-title">
    <a class="skip" href="#pintro">Aller au contenu</a>
    {render_nav(base, "work")}
    <div class="phero-media">{img(cover, f"{p['title']}, image de couverture", base, eager=True)}</div>
    <h1 class="phero-title" id="p-title"><span><span>{e(p['title'])}</span></span></h1>
    <p class="phero-year">{p['year']}</p>
    <p class="phero-text">{e(p['summary'])}</p>
    <div class="phero-bar">
      <span>{e(p['title'])} · {e(sub)}</span>
      <a href="#pintro"><i aria-hidden="true"></i>Défiler</a>
      <span>{i + 1:02d} / {len(PROJECTS):02d}</span>
    </div>
  </section>"""


def render_pintro(p, base):
    keys = [k for k, _ in p["meta"]]
    values = " ".join(v if isinstance(v, str) else v[0] for _, v in p["meta"])
    meta = []
    if p["context"] not in values:
        meta.append(("Contexte" if "Contexte" not in keys else "Structure", p["context"]))
    meta.append(("Discipline", p["tags"]))
    meta += p["meta"]
    items = ""
    for k, v in meta:
        val = (f'<a class="ulink" href="{v[1]}" target="_blank" rel="noopener">{e(v[0])}</a> {ARROW_UP}'
               if isinstance(v, tuple) else e(v))
        items += f"\n      <div><dt>{e(k)}</dt><dd>{val}</dd></div>"
    return f"""
  <section class="pintro grid" id="pintro" data-chunk="pintro" aria-label="Présentation du projet">
    <dl class="pintro-meta" data-reveal>{items}
    </dl>
    <p class="pintro-lead" data-reveal style="--d:.1s">{e(p['question'])}</p>
  </section>"""


def render_pgallery(p, base):
    blocks = p["blocks"]
    out = []
    count = [0]

    def num():
        count[0] += 1
        return count[0]

    def pair(sec, im, flip):
        narrow = " g-pair--narrow" if im.get("size") == "narrow" else ""
        fl = " is-flip" if flip else ""
        return f"""
    <div class="g-row g-pair grid{narrow}{fl}">
      {figure(im['src'], im['alt'], base, num(), im.get('caption'))}
      <div class="g-copy" data-reveal style="--d:.12s"><p class="g-label">{e(sec['label'])}</p>{section_copy(sec)}</div>
    </div>"""

    def full(im, link):
        w, h = size(im["src"])
        t = tone(im["src"], (.2, .3, .8, .7))
        dark = ' data-tone="dark"' if t == "dark" else ""
        text = ""
        if link:
            text = f'<a href="{link["href"]}" target="_blank" rel="noopener">{e(link["text"])} {ARROW_UP}</a>'
        elif im.get("caption"):
            text = e(im["caption"])
        side = " g-full-text--side" if link else ""
        cap = (f'\n      <figcaption class="g-full-text{side}"><span data-reveal>{text}</span></figcaption>'
               if text else "")
        num()
        return f"""
    <figure class="g-row g-full g-full--{t}"{dark}>
      <div class="frame" style="--ar:{w}/{h}">{img(im['src'], im['alt'], base)}</div>{cap}
    </figure>"""

    flip = False
    i = 0
    while i < len(blocks):
        b = blocks[i]
        nx = blocks[i + 1] if i + 1 < len(blocks) else None
        t = b["t"]
        if t == "section" and nx and nx["t"] == "img" and nx.get("size", "wide") != "full":
            out.append(pair(b, nx, flip))
            flip = not flip
            i += 2
            continue
        if t == "img" and b.get("size") == "full":
            link = nx if nx and nx["t"] == "link" else None
            out.append(full(b, link))
            i += 2 if link else 1
            continue
        if t == "section":
            out.append(f"""
    <section class="g-row g-text grid">
      <p class="g-label" data-reveal>{e(b['label'])}</p>
      <div class="g-body" data-reveal style="--d:.1s">{section_copy(b)}</div>
    </section>""")
        elif t == "img":
            narrow = " g-img--narrow" if b.get("size") == "narrow" else ""
            out.append(f"""
    <div class="g-row g-img grid{narrow}{' is-flip' if flip else ''}">
      {figure(b['src'], b['alt'], base, num(), b.get('caption'))}
    </div>""")
            flip = not flip
        elif t == "imgs":
            items = b["items"]
            layout = SET_LAYOUT.get(len(items)) or [(1 + (k % 3) * 4, 4, 0) for k in range(len(items))]
            figs = ""
            for k, ((src, alt), (c, s, o)) in enumerate(zip(items, layout)):
                w, h = size(src)
                if h > w * 1.25 and s > 4:
                    s = 3
                figs += "\n      " + figure(src, alt, base, num(), None, "",
                                           f"--c:{c};--s:{s};--o:{o}px;--d:{k * 0.06:.2f}s")
            out.append(f"""
    <div class="g-row g-set grid">{figs}
    </div>""")
        elif t == "quotes":
            qs = ""
            for k, (src, q) in enumerate(b["items"]):
                qs += f"""
      <div class="g-quote{' is-flip' if k % 2 else ''}">
        {figure(src, 'Persona', base, num())}
        <blockquote data-reveal style="--d:.1s">« {e(q)} »</blockquote>
      </div>"""
            out.append(f"""
    <section class="g-row g-quotes grid" aria-label="{e(b['label'])}">
      <p class="g-label">{e(b['label'])}</p>{qs}
    </section>""")
        elif t == "link":
            out.append(f"""
    <div class="g-row g-link grid">
      <a class="btn" href="{b['href']}" target="_blank" rel="noopener"><span>{e(b['text'])}</span><span class="btn-ico">{ARROW_UP}</span></a>
    </div>""")
        else:
            raise ValueError(t)
        i += 1
    return f"""
  <div class="pgallery" data-chunk="pgallery">{''.join(out)}
  </div>"""


def render_pnext(nxt, base):
    t = tone(nxt["cover"], (.25, .3, .75, .7))
    return f"""
<div class="pnext" data-chunk="pnext">
  <a class="pnext-link{' is-dark' if t == 'dark' else ''}" href="{nxt['slug']}.html"{' data-tone="dark"' if t == 'dark' else ''}>
    {img(nxt['cover'], '', base)}
    <span class="pnext-center"><span class="pnext-title">{e(nxt['title'])}</span><span class="pnext-sub">Projet suivant {ARROW}</span></span>
  </a>
  <footer class="pbar" id="contact">
    <a href="#top">{ARROW_TOP} Retour en haut</a>
    <span>© 2026 Théo Petitimbert</span>
    <span><a class="ulink" href="mailto:{SITE['email']}">{e(SITE['email'])}</a><a class="ulink" href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn</a></span>
  </footer>
</div>"""


def build_project(i, p):
    base = "../"
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    html = head(f"{p['title']} · Théo Petitimbert", p["summary"], base,
                ["project-hero", "project-intro", "project-gallery", "project-next"], og=p["thumb"])
    html += f"""
<body class="page-project" id="top">
<main id="main">{render_phero(i, p, base)}{render_pintro(p, base)}{render_pgallery(p, base)}
</main>{render_pnext(nxt, base)}{scripts(base, [])}"""
    out = ROOT / "projets"
    out.mkdir(exist_ok=True)
    (out / f"{p['slug']}.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# Page À propos
# ---------------------------------------------------------------------------
def render_ahero(base):
    roles = "".join(f"<li>{e(r)}</li>" for r in SITE["roles"])
    first, last = SITE["name"].split(" ", 1)
    school = CV["Formation"][0][1].split(" · ")
    return f"""
  <section class="ahero grid" aria-labelledby="a-title">
    <a class="skip" href="#parcours">Aller au contenu</a>
    {render_nav(base, "about")}
    <div class="ahero-head">
      <p class="ahero-label">À propos</p>
      <h1 class="ahero-title" id="a-title"><span><span>{e(first)}</span></span><span><span>{e(last)}</span></span></h1>
      <ul class="ahero-roles">{roles}</ul>
    </div>
    <figure class="ahero-fig">
      <div class="frame">{img("portrait", f"Portrait de {SITE['name']}", base, eager=True)}</div>
      <figcaption class="g-cap"><span>{e(school[1])}</span><span>{e(school[0])}</span></figcaption>
    </figure>
  </section>"""


def render_abio(base):
    xp = CV["Expérience"][0]
    meta = [
        ("Formation", e(CV["Formation"][0][1])),
        ("Expérience", f"{e(xp[1])} · {e(xp[0])}"),
        ("E-mail", f'<a class="ulink" href="mailto:{SITE["email"]}">{e(SITE["email"])}</a>'),
        ("Téléphone", f'<a href="tel:{SITE["phone_href"]}">{e(SITE["phone"])}</a>'),
        ("Réseau", f'<a class="ulink" href="{SITE["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a> {ARROW_UP}'),
    ]
    dl = "".join(f"\n      <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta)
    more = "".join(f"<p>{e(x)}</p>" for x in SITE["bio_more"])
    return f"""
  <section class="abio grid" id="parcours" aria-label="Présentation">
    <dl class="abio-meta" data-reveal>{dl}
    </dl>
    <p class="abio-lead" data-reveal style="--d:.1s">{e(SITE['bio'])}</p>
    <div class="abio-more" data-reveal style="--d:.2s">{more}</div>
  </section>"""


def render_acv(base):
    groups = ""
    for k, items in CV.items():
        rows = "".join(f"""
        <li><span class="acv-date">{e(d)}</span><span class="acv-title">{e(t)}</span><span class="acv-detail">{e(x)}</span></li>"""
                       for d, t, x in items)
        groups += f"""
    <div class="acv-group grid" data-reveal>
      <h2 class="acv-h">{e(k)}</h2>
      <ul class="acv-list">{rows}
      </ul>
    </div>"""
    return f"""
  <section class="acv" aria-label="Parcours">{groups}
  </section>"""


def render_askills(base):
    cols = "".join(f"""
      <div><h3>{e(k)}</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in items)}</ul></div>""" for k, items in SKILLS.items())
    return f"""
  <section class="askills grid" aria-labelledby="skills-title" data-reveal>
    <h2 class="askills-h" id="skills-title">Compétences</h2>
    <div class="askills-cols">{cols}
    </div>
  </section>"""


def render_astudio(base):
    steps = "".join(f"""
      <li data-reveal style="--d:{k * 0.08:.2f}s"><span class="n">{k + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>"""
                    for k, (t, d) in enumerate(STUDIO["method"]))
    figs = ""
    for k, ((src, cap), (c, s, o)) in enumerate(zip(STUDIO["images"], STUDIO_LAYOUT)):
        w, h = size(src)
        figs += f"""
      <figure style="--c:{c};--s:{s};--o:{o}px" data-reveal>
        <div class="frame" style="aspect-ratio:{w}/{h}">{img(src, cap, base)}</div>
        <figcaption class="g-cap"><span aria-hidden="true">{e(cap)}</span><span aria-hidden="true">{k + 1:02d}</span></figcaption>
      </figure>"""
    xp = CV["Expérience"][0]
    return f"""
  <section class="astudio" data-tone="dark" aria-labelledby="studio-title">
    <div class="astudio-head grid">
      <p class="astudio-label">Expérience · {e(xp[0])}</p>
      <h2 class="astudio-title" id="studio-title" data-reveal>Design Studio<br><span>iXcampus, en alternance</span></h2>
      <p class="astudio-intro" data-reveal style="--d:.1s">{e(STUDIO['intro'])}</p>
    </div>
    <ol class="astudio-steps">{steps}
    </ol>
    <div class="astudio-figs grid">{figs}
    </div>
    <dl class="astudio-dl grid">
      <div data-reveal><dt>Missions</dt><dd>{e(STUDIO['missions'])}</dd></div>
      <div data-reveal style="--d:.1s"><dt>Livrables</dt><dd>{e(STUDIO['deliverables'])}</dd></div>
    </dl>
  </section>"""


def build_about():
    base = ""
    html = head(f"À propos · {SITE['name']}", SITE["bio"], base, ["about", "next", "footer"], og="portrait")
    html += f"""
<body class="page-about" id="top">
<main id="main">{render_ahero(base)}{render_abio(base)}{render_acv(base)}{render_askills(base)}{render_astudio(base)}{render_next("index.html#projets", ["Projets", "sélectionnés"], "Voir les projets")}
</main>{render_footer(base)}{scripts(base, [])}"""
    (ROOT / "a-propos.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build_index()
    build_about()
    for i, p in enumerate(PROJECTS):
        build_project(i, p)
    print(f"OK · index.html + a-propos.html + {len(PROJECTS)} pages projet")
