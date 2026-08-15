# Manim Shorts — Maths

Scripts [Manim](https://www.manim.community/) pour mes vidéos courtes (shorts) de maths.

> À personnaliser : remplace ce paragraphe par une phrase sur le format (YouTube Shorts / TikTok / Reels), le rythme de publication et le public visé.

## Stack

- Python 3.12
- [Manim Community](https://docs.manim.community/) v0.21
- [uv](https://docs.astral.sh/uv/) pour la gestion de l'environnement et des dépendances
- FFmpeg (encodage vidéo)

## Structure du repo

```
Manim/
├── README.md
├── pyproject.toml          # dépendances du projet
├── .gitignore
├── shared/                 # code réutilisable entre chapitres (palette, mobjects custom, helpers)
│   ├── __init__.py
│   └── palette.py
├── chapitres/
│   ├── _exemples/          # bac à sable / tests, pas du contenu publiable
│   │   └── 001-premiers-pas/
│   │       └── scene.py
│   ├── derivees/
│   │   └── 001-intuition-derivee/
│   │       └── scene.py
│   ├── integrales/
│   └── espaces-vectoriels/
└── media/                   # généré par Manim au rendu — ignoré par git
```

Chaque grand chapitre de maths (dérivées, intégrales, espaces vectoriels...) a son propre dossier sous `chapitres/`. À l'intérieur, un sous-dossier numéroté par vidéo (`001-...`, `002-...`) contient le `scene.py` correspondant, et éventuellement des notes de script (voix off), assets, etc.

Le format vertical 9:16 (1080x1920, 60 fps) est configuré par défaut au niveau de la machine (`%APPDATA%\Manim\manim.cfg`), donc pas besoin de le répéter dans chaque script.

## Installation

```bash
git clone https://github.com/AlexRadelet/Manim.git
cd Manim
uv venv --python 3.12 .venv
uv pip install -e .
```

FFmpeg doit être installé et disponible dans le PATH.

## Utilisation

Toujours lancer `manim` depuis la racine du repo, en pointant vers le script (ça permet aux imports `from shared...` de fonctionner) :

```bash
# Aperçu rapide, basse qualité
manim -pql chapitres/derivees/001-intuition-derivee/scene.py NomDeLaScene

# Rendu final, haute qualité
manim -pqh chapitres/derivees/001-intuition-derivee/scene.py NomDeLaScene
```

## Convention de nommage

- Dossier de chapitre : `kebab-case` du thème (`derivees`, `espaces-vectoriels`...)
- Dossier de vidéo : `NNN-titre-court` (`001-intuition-derivee`)
- Classe de scène : `PascalCase` explicite (`IntuitionDerivee`)

## Chapitres prévus

- [ ] Dérivées
- [ ] Intégrales
- [ ] Espaces vectoriels

## Licence

À définir.
