"""Outils communs aux vidéos de physique (cinématique, chapitres 2 et 3).

Importer avec ``from shared.physique import *`` : ça importe aussi tout Manim.

- Passe le rendu en 16:9 (paysage) : ces vidéos sont faites pour le partage
  d'écran en cours à distance, pas pour les shorts verticaux.
- Fixe un code couleur unique pour toutes les vidéos :
    position / déplacement -> bleu   (C_POS)
    vitesse                -> vert   (C_VIT)
    accélération           -> rose   (C_ACC)
    mise en évidence       -> orange (C_ACCENT)
"""

from manim import *  # noqa: F401,F403

from shared.palette import ACCENT, BACKGROUND, PRIMARY, SECONDARY, TEXT


# ---------------------------------------------------------------------------
# Format 16:9
# ---------------------------------------------------------------------------
def format_paysage() -> None:
    """Force un cadre 16:9 quelle que soit la config machine (souvent 9:16).

    Garde la qualité choisie en ligne de commande (-ql, -qh...) : on remet
    juste la plus grande dimension en largeur.
    """
    w, h = config.pixel_width, config.pixel_height
    if h > w:
        w, h = h, w
    config.pixel_width = w
    config.pixel_height = h
    config.frame_height = 8.0
    config.frame_width = 8.0 * w / h
    config.background_color = BACKGROUND


def ranger_par_chapitre() -> None:
    """Range les vidéos comme le code.

    chapitres/<chapitre>/<NNN-video>/scene.py
    -> media/videos/<chapitre>/<NNN-video>/<qualité>/<NomDeLaScene>.mp4
    (sans ça, tous les scene.py finiraient dans le même dossier media/videos/scene/).
    """
    from pathlib import Path

    if not config.input_file:
        return
    src = Path(config.input_file).resolve()
    if len(src.parents) > 2 and src.parents[2].name == "chapitres":
        chapitre, video = src.parents[1].name, src.parent.name
        config.video_dir = "{media_dir}/videos/" + f"{chapitre}/{video}" + "/{quality}"


format_paysage()
ranger_par_chapitre()


# ---------------------------------------------------------------------------
# Couleurs
# ---------------------------------------------------------------------------
C_POS = PRIMARY
C_VIT = ManimColor("#81C784")
C_ACC = SECONDARY
C_ACCENT = ACCENT
C_TEXTE = TEXT
C_GRIS = ManimColor("#8A8FA3")
C_NEG = ManimColor("#EF5350")  # aires / grandeurs négatives
C_SOL = ManimColor("#6D5D4B")


# ---------------------------------------------------------------------------
# Texte et formules
# ---------------------------------------------------------------------------
POLICE = "Sans"  # alias générique : Arial/Segoe sous Windows, DejaVu Sans sous Linux


def T(texte: str, size: float = 30, color=TEXT, **kw) -> Text:
    """Texte (Pango) — pour les phrases en français."""
    kw.setdefault("font", POLICE)
    return Text(texte, font_size=size, color=color, **kw)


def limiter(mob: Mobject, largeur: float) -> Mobject:
    """Réduit un objet s'il dépasse la largeur donnée (évite les débordements)."""
    if mob.width > largeur:
        mob.scale_to_fit_width(largeur)
    return mob


def M(*tex: str, size: float = 40, color=TEXT, **kw) -> MathTex:
    """Formule LaTeX. Virgule décimale : écrire ``2{,}5``."""
    return MathTex(*tex, font_size=size, color=color, **kw)


def fr(x: float, decimales: int = 2) -> str:
    """Nombre formaté à la française pour MathTex : 2.5 -> '2{,}5'."""
    s = f"{x:.{decimales}f}"
    return s.replace(".", "{,}")


class DecimalFR(DecimalNumber):
    """DecimalNumber avec une virgule décimale (affichage live, rapide)."""

    def __init__(self, number: float = 0, **kw):
        kw.setdefault("group_with_commas", False)
        kw.setdefault("color", TEXT)
        super().__init__(number, **kw)

    def _get_num_string(self, number):  # noqa: D401
        return super()._get_num_string(number).replace(".", ",")


def encadre(mob: Mobject, color=ACCENT, buff: float = 0.22) -> VGroup:
    """Encadre une formule clé (comme les boîtes du cours)."""
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12,
                               stroke_width=3)
    box.set_fill(BACKGROUND, opacity=0.85)
    return VGroup(box, mob)


def bandeau(texte: str, sous_titre: str | None = None) -> VGroup:
    """Titre de partie, en haut à gauche."""
    t = T(texte, size=34, color=ACCENT, weight=BOLD)
    g = VGroup(t)
    if sous_titre:
        s = T(sous_titre, size=22, color=C_GRIS)
        s.next_to(t, DOWN, aligned_edge=LEFT, buff=0.12)
        g.add(s)
    g.to_corner(UL, buff=0.4)
    return g


def carte_titre(scene: Scene, numero: str, titre: str, resume: str = "") -> None:
    """Écran d'ouverture : numéro de section du cours + titre + 1 phrase."""
    n = T(numero, size=30, color=C_GRIS)
    t = T(titre, size=52, color=TEXT, weight=BOLD)
    limiter(t, config.frame_width - 1.2)
    g = VGroup(n, t).arrange(DOWN, buff=0.3)
    if resume:
        r = limiter(T(resume, size=26, color=ACCENT), config.frame_width - 1.5)
        r.next_to(t, DOWN, buff=0.45)
        g.add(r)
    g.move_to(ORIGIN)
    ligne = Line(LEFT * 3, RIGHT * 3, color=ACCENT).next_to(t, UP, buff=0.18)
    scene.play(FadeIn(n, shift=DOWN * 0.2), Create(ligne), Write(t), run_time=1.5)
    if resume:
        scene.play(FadeIn(g[2], shift=UP * 0.2))
    scene.wait(2)
    scene.play(FadeOut(VGroup(g, ligne)))


def vider(scene: Scene, run_time: float = 0.8) -> None:
    """Efface tout l'écran."""
    for m in scene.mobjects:  # figer les objets « vivants » (always_redraw, compteurs…)
        m.clear_updaters()
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=run_time)


# ---------------------------------------------------------------------------
# Flèches de grandeurs physiques
# ---------------------------------------------------------------------------
def fleche(debut, fin, color, width: float = 6, tip: float = 0.22) -> Arrow:
    """Flèche "vecteur" sans marge, qui reste propre même très courte."""
    debut, fin = np.array(debut, dtype=float), np.array(fin, dtype=float)
    if np.linalg.norm(fin - debut) < 1e-3:
        fin = debut + np.array([1e-3, 0, 0])
    return Arrow(debut, fin, buff=0, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=0.45,
                 max_stroke_width_to_length_ratio=12, tip_length=tip)


def particule(color=ACCENT, r: float = 0.13) -> Dot:
    return Dot(radius=r, color=color).set_z_index(5)


def voiture(color=PRIMARY, largeur: float = 0.9) -> VGroup:
    """Petite voiture stylisée (vue de côté) ; son centre est le point suivi."""
    h = largeur * 0.32
    caisse = RoundedRectangle(width=largeur, height=h, corner_radius=0.06,
                              color=color, fill_opacity=0.9, stroke_width=0)
    toit = RoundedRectangle(width=largeur * 0.5, height=h * 0.75, corner_radius=0.06,
                            color=color, fill_opacity=0.9, stroke_width=0)
    toit.next_to(caisse, UP, buff=-0.02)
    roues = VGroup(*[Circle(radius=h * 0.38, color=C_GRIS, fill_color=BACKGROUND,
                            fill_opacity=1, stroke_width=3)
                     .move_to(caisse.get_bottom() + RIGHT * dx * largeur * 0.3)
                     for dx in (-1, 1)])
    v = VGroup(caisse, toit, roues)
    v.move_to(ORIGIN)
    return v


class Compteur(VGroup):
    """Affichage live « texte = valeur unité » qui se ré-aligne tout seul.

    ``fonction`` est appelée à chaque image (ex. ``lambda: t.get_value()``).
    """

    def __init__(self, avant: str, fonction, apres: str = "", decimales: int = 1,
                 size: float = 32, color=TEXT, couleur_nombre=None, signe: bool = False):
        self.fonction = fonction
        self.nombre = DecimalFR(fonction(), num_decimal_places=decimales, font_size=size,
                                color=couleur_nombre or color, include_sign=signe)
        parts = []
        if avant:
            parts.append(M(avant, size=size, color=color))
        parts.append(self.nombre)
        if apres:
            parts.append(M(apres, size=size, color=color))
        super().__init__(*parts)
        self.arrange(RIGHT, buff=0.12)
        self.add_updater(lambda g: g._maj())

    def _maj(self):
        gauche = self.get_left()
        self.nombre.set_value(self.fonction())
        self.arrange(RIGHT, buff=0.12)
        self.move_to(gauche, aligned_edge=LEFT)


# ---------------------------------------------------------------------------
# Dynamique (chapitres 4 et 5)
# ---------------------------------------------------------------------------
C_FORCE = ManimColor("#CE93D8")  # forces (violet) — distinct de v (vert) et a (rose)


def bloc(masse: str = "", largeur: float = 1.0, hauteur: float = 0.8, color=PRIMARY,
         size: float = 26) -> VGroup:
    """Bloc rectangulaire avec son étiquette de masse au centre."""
    r = Rectangle(width=largeur, height=hauteur, color=color, fill_opacity=0.35,
                  stroke_width=3)
    g = VGroup(r)
    if masse:
        g.add(M(masse, size=size).move_to(r))
    return g


def ressort(debut, fin, spires: int = 10, largeur: float = 0.25, color=C_GRIS) -> VMobject:
    """Ressort en zigzag entre deux points (s'étire avec la distance)."""
    debut, fin = np.array(debut, dtype=float), np.array(fin, dtype=float)
    d = fin - debut
    L = np.linalg.norm(d)
    u = d / L if L > 0 else RIGHT
    n = np.array([-u[1], u[0], 0])
    pts = [debut, debut + u * 0.1 * L]
    for k in range(2 * spires):
        s = 0.1 + 0.8 * (k + 0.5) / (2 * spires)
        pts.append(debut + u * s * L + n * largeur * (1 if k % 2 == 0 else -1))
    pts += [debut + u * 0.9 * L, fin]
    return VMobject(color=color, stroke_width=3).set_points_as_corners(pts)


def force(point, vecteur, nom: str = "", color=None, direction=None, size: float = 30,
          width: float = 6) -> VGroup:
    """Flèche de force partant de `point`, avec son nom LaTeX au bout."""
    color = color or C_FORCE
    point = np.array(point, dtype=float)
    vecteur = np.array(vecteur, dtype=float)
    f = fleche(point, point + vecteur, color, width=width)
    g = VGroup(f)
    if nom:
        dirn = direction if direction is not None else (
            vecteur / np.linalg.norm(vecteur) if np.linalg.norm(vecteur) > 1e-6 else UP)
        g.add(M(nom, size=size, color=color).next_to(point + vecteur, dirn, buff=0.1))
    return g
