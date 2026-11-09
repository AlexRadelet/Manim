# Chapitre 4 — Dynamique de la particule, partie 1

Vidéos d'appui pour le cours particulier (format 16:9, pas de voix off : on commente en direct).
Code couleur commun : **bleu** = position, **vert** = vitesse, **rose** = accélération, **violet** = forces, **orange** = mise en évidence.

| Dossier | Scène(s) | Section du cours |
|---|---|---|
| `001-force-et-hooke` | `ForceEtHooke` | 4.1 — La force : interaction, forces usuelles, caractère vectoriel, loi de Hooke. |
| `002-masse-inertie` | `MasseInertie` | 4.1 — La masse = mesure de l'inertie (résistance aux variations de vitesse) et sa mesure. |
| `003-deuxieme-loi-newton` | `DeuxiemeLoiNewton` | 4.2 — La deuxième loi de Newton : ΣF = m a. |
| `004-poids` | `Poids` | 4.3 — Le poids : gravitation universelle, P = m g, masse ≠ poids (Terre / Lune). |
| `005-troisieme-loi-newton` | `TroisiemeLoiNewton` | 4.4 — La troisième loi de Newton : F_AB = −F_BA, et les trois erreurs classiques. |
| `006-methode-equilibre` | `MethodeEquilibre` | 4.5 — Méthode de résolution + exemple d'équilibre. |
| `007-plan-incline-luge` | `PlanInclineLuge` | 4.5 — Hors équilibre : la luge tirée sur une pente sans frottement (exemple 1). |
| `008-machine-atwood` | `MachineAtwood` | 4.5 — Exemple 3 : la machine d'Atwood (m1 = 3 kg, m2 = 5 kg). |
| `009-poids-apparent` | `PoidsApparent` | 4.6 — Le poids apparent : une personne de 70 kg sur une balance dans un ascenseur. |

## Rendu

Depuis la racine du repo :

```bash
# aperçu rapide
python -m manim -pql chapitres/physique-ch4-dynamique-1/001-.../scene.py NomDeLaScene

# toutes les scènes d'un fichier, qualité finale (1080p)
python -m manim -qh -a chapitres/physique-ch4-dynamique-1/001-.../scene.py

# une vidéo par étape (pratique pour avancer pas à pas pendant le cours)
python -m manim -qh --save_sections chapitres/physique-ch4-dynamique-1/001-.../scene.py NomDeLaScene
```

Les formules utilisent LaTeX (`MathTex`) : il faut MiKTeX (ou TeX Live) en plus de FFmpeg.

## Où sont les vidéos

Rangées comme le code : `media/videos/physique-ch4-dynamique-1/<NNN-video>/<qualité>/<NomDeLaScene>.mp4`
(`480p15` avec `-ql`, `1080p60` avec `-qh`). C'est `shared/physique.py` qui fixe ce rangement.
Le dossier `partial_movie_files/` n'est qu'un cache de morceaux (un par animation) : à ignorer, supprimable sans risque.
Avec `--save_sections`, les étapes séparées sont dans le sous-dossier `sections/`.
