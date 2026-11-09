# Chapitre 3 — L'inertie et le mouvement à deux dimensions

Vidéos d'appui pour le cours particulier (format 16:9, pas de voix off : on commente en direct).
Code couleur commun : **bleu** = position/déplacement, **vert** = vitesse, **rose** = accélération, **orange** = mise en évidence.

| Dossier | Scène(s) | Section du cours |
|---|---|---|
| `001-premiere-loi-newton` | `PremiereLoiNewton` | 3.1 — La première loi de Newton (principe d'inertie). |
| `002-position-vitesse-2d` | `PositionVitesse2D` | 3.2 — Le mouvement dans le plan : vecteur position, déplacement, vitesse moyenne, vitesse instantanée. |
| `003-acceleration-2d` | `Acceleration2D` | 3.2 — L'accélération dans le plan (équivalent du « film 3.1 »). |
| `004-independance-mouvements` | `IndependanceMouvements` | 3.3 — Mouvement d'un projectile : horizontal et vertical sont INDÉPENDANTS. |
| `005-projectile-oblique` | `ExempleFalaise`, `ProjectileOblique` | 3.3 — Projectiles : exemple 1 (tir horizontal d'une falaise) et exemple 2 (tir oblique en terrain plat). |
| `006-mouvement-circulaire-uniforme` | `MouvementCirculaireUniforme` | 3.4 — Mouvement circulaire uniforme : l'accélération centripète. |
| `007-mouvement-circulaire-non-uniforme` | `MouvementCirculaireNonUniforme` | 3.5 — Mouvement circulaire non uniforme : a = a_t (tangentielle) + a_r (radiale = centripète). |
| `008-referentiels-inertie` | `ReferentielsInertie` | 3.6 — Les référentiels d'inertie. |
| `009-vitesse-relative` | `VitesseRelative` | 3.7 — Vitesse relative : un homme H traverse un train T qui roule par rapport au sol S (vue de dessus). |
| `010-transformation-galilee` | `TransformationGalilee` | 3.8 — La transformation de Galilée. |

## Rendu

Depuis la racine du repo :

```bash
# aperçu rapide
python -m manim -pql chapitres/physique-ch3-mouvement-2d/001-.../scene.py NomDeLaScene

# toutes les scènes d'un fichier, qualité finale (1080p)
python -m manim -qh -a chapitres/physique-ch3-mouvement-2d/001-.../scene.py

# une vidéo par étape (pratique pour avancer pas à pas pendant le cours)
python -m manim -qh --save_sections chapitres/physique-ch3-mouvement-2d/001-.../scene.py NomDeLaScene
```

Les formules utilisent LaTeX (`MathTex`) : il faut une distribution LaTeX installée (MiKTeX ou TeX Live) en plus de FFmpeg.

## Où sont les vidéos

Rangées comme le code : `media/videos/physique-ch3-mouvement-2d/<NNN-video>/<qualité>/<NomDeLaScene>.mp4`
(`480p15` avec `-ql`, `1080p60` avec `-qh`). C'est `shared/physique.py` qui fixe ce rangement.
Le dossier `partial_movie_files/` n'est qu'un cache de morceaux (un par animation) : à ignorer, supprimable sans risque.
Avec `--save_sections`, les étapes séparées sont dans le sous-dossier `sections/`.
