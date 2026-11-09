# Chapitre 5 — Dynamique de la particule, partie 2

Vidéos d'appui pour le cours particulier (format 16:9, pas de voix off : on commente en direct).
Code couleur commun : **bleu** = position, **vert** = vitesse, **rose** = accélération, **violet** = forces, **orange** = mise en évidence.

| Dossier | Scène(s) | Section du cours |
|---|---|---|
| `001-frottement-statique-cinetique` | `FrottementStatiqueCinetique` | 5.1 — Frottement statique et cinétique. |
| `002-plan-incline-mu` | `PlanInclineMu` | 5.1 — Mesurer μs et μc avec un plan incliné. |
| `003-blocs-superposes` | `BlocsSuperposes` | 5.1 — Exemple 1 : deux blocs superposés (m1 = 2 kg sur m2 = 4 kg), sol sans frottement, μs = 0,4 et μc = 0,2 entre les blocs. Force F0 sur le bloc du bas. |
| `004-force-centripete` | `ForceCentripete` | 5.2 — La « force centripète » n'est pas une force de plus : c'est le rôle joué par T, N ou f. |
| `005-virage-releve` | `VirageReleve` | 5.2 — Exemple 3 : le virage relevé (vue en coupe). |
| `006-cercle-vertical` | `CercleVertical` | 5.2 — Mouvement circulaire non uniforme : la pierre au bout d'une corde dans un cercle vertical, puis le skieur sur une bosse. |
| `007-satellites` | `Satellites` | 5.3 — Les orbites des satellites : le canon de Newton, v_orb = √(GM/r), 3e loi de Kepler, apesanteur apparente. |
| `008-referentiels-non-inertiels` | `ReferentielsNonInertiels` | 5.4 — Référentiels non inertiels et forces fictives. |
| `009-coriolis` | `Coriolis` | 5.4 — Vitesse angulaire et force de Coriolis. |

## Rendu

Depuis la racine du repo :

```bash
# aperçu rapide
python -m manim -pql chapitres/physique-ch5-dynamique-2/001-.../scene.py NomDeLaScene

# toutes les scènes d'un fichier, qualité finale (1080p)
python -m manim -qh -a chapitres/physique-ch5-dynamique-2/001-.../scene.py

# une vidéo par étape (pratique pour avancer pas à pas pendant le cours)
python -m manim -qh --save_sections chapitres/physique-ch5-dynamique-2/001-.../scene.py NomDeLaScene
```

Les formules utilisent LaTeX (`MathTex`) : il faut MiKTeX (ou TeX Live) en plus de FFmpeg.

## Où sont les vidéos

Rangées comme le code : `media/videos/physique-ch5-dynamique-2/<NNN-video>/<qualité>/<NomDeLaScene>.mp4`
(`480p15` avec `-ql`, `1080p60` avec `-qh`). C'est `shared/physique.py` qui fixe ce rangement.
Le dossier `partial_movie_files/` n'est qu'un cache de morceaux (un par animation) : à ignorer, supprimable sans risque.
Avec `--save_sections`, les étapes séparées sont dans le sous-dossier `sections/`.
