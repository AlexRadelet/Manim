# Chapitre 2 — La cinématique à une dimension

Vidéos d'appui pour le cours particulier (format 16:9, pas de voix off : on commente en direct).
Code couleur commun : **bleu** = position/déplacement, **vert** = vitesse, **rose** = accélération, **orange** = mise en évidence.

| Dossier | Scène(s) | Section du cours |
|---|---|---|
| `001-deplacement-distance` | `DeplacementDistance` | 2.2 — Déplacement vs distance parcourue, vitesse moyenne vs vitesse scalaire moyenne. |
| `002-graphe-position-temps` | `GraphePositionTemps` | 2.2 — Représentation graphique : le graphe x(t) et la vitesse moyenne = pente de la sécante. |
| `003-vitesse-instantanee` | `VitesseInstantanee` | 2.3 — Vitesse instantanée : la sécante devient tangente quand Δt → 0. |
| `004-aire-sous-vitesse` | `AireSousVitesse` | 2.3 — Le déplacement = aire sous la courbe de v_x(t) (aires sous l'axe comptées négativement). |
| `005-acceleration-signes` | `SignesAcceleration` | 2.5 — L'accélération : définition, et surtout les 4 cas de signes (A, B, C, D du cours). |
| `006-equations-mrua` | `EquationsMRUA`, `ExempleAutomobile` | 2.6 — MRUA : d'où viennent les 4 équations, et comment choisir la bonne. |
| `007-collision-voitures` | `CollisionVoitures` | 2.6 — Exemple 2 : deux cascadeurs foncent l'un vers l'autre. Où et quand se percutent-ils ? |
| `008-chute-libre` | `ChuteLibreGalilee`, `BalleLanceeDuToit` | 2.7 — Chute libre verticale. |
| `009-acceleration-variable` | `AccelerationVariable` | 2.8 — Accélération variable : a_x = 3t -> v_x = 3t²/2 -> x = t³/2 (départ au repos, à l'origine). |

## Rendu

Depuis la racine du repo :

```bash
# aperçu rapide
python -m manim -pql chapitres/physique-ch2-cinematique-1d/001-.../scene.py NomDeLaScene

# toutes les scènes d'un fichier, qualité finale (1080p)
python -m manim -qh -a chapitres/physique-ch2-cinematique-1d/001-.../scene.py

# une vidéo par étape (pratique pour avancer pas à pas pendant le cours)
python -m manim -qh --save_sections chapitres/physique-ch2-cinematique-1d/001-.../scene.py NomDeLaScene
```

Les formules utilisent LaTeX (`MathTex`) : il faut une distribution LaTeX installée (MiKTeX ou TeX Live) en plus de FFmpeg.

## Où sont les vidéos

Rangées comme le code : `media/videos/physique-ch2-cinematique-1d/<NNN-video>/<qualité>/<NomDeLaScene>.mp4`
(`480p15` avec `-ql`, `1080p60` avec `-qh`). C'est `shared/physique.py` qui fixe ce rangement.
Le dossier `partial_movie_files/` n'est qu'un cache de morceaux (un par animation) : à ignorer, supprimable sans risque.
Avec `--save_sections`, les étapes séparées sont dans le sous-dossier `sections/`.
