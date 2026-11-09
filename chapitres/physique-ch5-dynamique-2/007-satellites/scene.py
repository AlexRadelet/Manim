"""5.3 — Les orbites des satellites : le canon de Newton, v_orb = √(GM/r), 3e loi de Kepler,
apesanteur apparente.

Les trajectoires du canon sont calculées (gravité en 1/r², unités d'écran).

    python -m manim -pql chapitres/physique-ch5-dynamique-2/007-satellites/scene.py Satellites
"""

from shared.physique import *

CT = np.array([-3.0, -0.35, 0])  # centre de la Terre
RT = 1.7
H = 0.35
R0 = RT + H
V_CIRC = 1.6
GM = V_CIRC ** 2 * R0


def trajectoire(v0, t_max=12.0, dt=0.002):
    """Intégration (Verlet) depuis le sommet de la montagne, vitesse horizontale v0."""
    p = np.array([0.0, R0])
    v = np.array([v0, 0.0])
    pts = [p.copy()]
    a = -GM * p / np.linalg.norm(p) ** 3
    t = 0.0
    tour = False
    while t < t_max:
        p = p + v * dt + 0.5 * a * dt * dt
        a2 = -GM * p / np.linalg.norm(p) ** 3
        v = v + 0.5 * (a + a2) * dt
        a = a2
        t += dt
        pts.append(p.copy())
        if np.linalg.norm(p) < RT:
            break
        if p[0] < 0 and pts[-2][0] >= 0 and p[1] > 0 and t > 1:  # un tour complet
            tour = True
            break
    return [CT + np.array([q[0], q[1], 0]) for q in pts[::5]], tour


class Satellites(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 5 · section 5.3", "Les satellites",
                    "Être en orbite, c'est tomber… sans jamais toucher le sol")

        # --- 1. Le canon de Newton ----------------------------------------------------------------
        self.next_section("canon")
        titre = bandeau("Le canon de Newton", "un boulet tiré horizontalement du haut d'une immense montagne, sans air")
        self.play(FadeIn(titre))
        terre = Circle(radius=RT, color=C_POS, fill_opacity=0.35).move_to(CT)
        mont = Polygon(CT + UP * RT + LEFT * 0.25, CT + UP * R0, CT + UP * RT + RIGHT * 0.25, color=C_SOL,
                       fill_opacity=1, stroke_width=0)
        self.play(FadeIn(terre), FadeIn(mont))
        vitesses = [(0.7, C_GRIS), (1.1, C_GRIS), (1.4, C_GRIS), (V_CIRC, ACCENT), (1.75, C_VIT)]
        legendes = ["trop lent : retombe", "plus vite : retombe plus loin", "encore plus loin…",
                    "juste assez vite : il fait le tour !", "plus vite encore : orbite elliptique"]
        txt = None
        for (v0, coul), leg in zip(vitesses, legendes):
            pts, tour = trajectoire(v0)
            chemin = VMobject(color=coul, stroke_width=4 if coul != C_GRIS else 3).set_points_smoothly(pts)
            boulet = Dot(pts[0], radius=0.08, color=coul)
            nouveau = T(leg, size=24, color=coul if coul != C_GRIS else C_TEXTE).move_to(RIGHT * 3.6 + UP * 2.3)
            self.play(FadeIn(boulet), FadeOut(txt) if txt else Wait(0.01), FadeIn(nouveau), run_time=0.5)
            txt = nouveau
            self.play(Create(chemin), MoveAlongPath(boulet, chemin), run_time=2.2 if tour else 1.4, rate_func=linear)
            self.wait(0.6)
        expl = T("Le boulet tombe sans cesse vers la Terre…\nmais la surface « se dérobe » sous lui\nà cause de la courbure : il ne la touche jamais.",
                 size=22, color=C_TEXTE).move_to(RIGHT * 3.6 + UP * 0.6)
        limiter(expl, 6.4)
        self.play(FadeIn(expl))
        self.wait(4)
        vider(self)

        # --- 2. Vitesse orbitale et Kepler -------------------------------------------------------------
        self.next_section("formules")
        titre = bandeau("Orbite circulaire : la gravitation est la force centripète")
        self.play(FadeIn(titre))
        terre = Circle(radius=1.1, color=C_POS, fill_opacity=0.35).move_to(LEFT * 3.6 + DOWN * 0.4)
        Ro = 2.3
        orbite = DashedVMobject(Circle(radius=Ro, color=C_GRIS).move_to(terre), num_dashes=60)
        ang = ValueTracker(0)
        sat = always_redraw(lambda: Square(0.22, color=ACCENT, fill_opacity=0.9)
                            .move_to(terre.get_center() + Ro * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0])))
        fg = always_redraw(lambda: fleche(sat.get_center(), sat.get_center() - 0.9 * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
                                          C_FORCE, width=6))
        fv = always_redraw(lambda: fleche(sat.get_center(), sat.get_center() + 1.0 * np.array([-np.sin(ang.get_value()), np.cos(ang.get_value()), 0]),
                                          C_VIT, width=5))
        self.play(FadeIn(terre), Create(orbite), FadeIn(sat), FadeIn(fg), FadeIn(fv))
        self.play(ang.animate.set_value(PI), run_time=3, rate_func=linear)
        eqs = VGroup(
            M(r"\frac{G m M}{r^2} = \frac{m v_{orb}^2}{r}", size=38),
            M(r"v_{orb} = \sqrt{\frac{G M}{r}}", size=40, color=C_VIT),
            T("la masse m du satellite n'intervient pas", size=20, color=C_GRIS),
            M(r"T = \frac{2\pi r}{v_{orb}} \;\Rightarrow\; T^2 = \frac{4\pi^2}{G M}\,r^3", size=36, color=ACCENT),
            T("3e loi de Kepler (1619) : T² ∝ r³", size=22, color=ACCENT),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.3 + UP * 0.4)
        limiter(eqs, 6.6)
        for e in eqs:
            self.play(FadeIn(e, shift=UP * 0.1), ang.animate.increment_value(0.9), run_time=1.0, rate_func=linear)
            self.wait(0.3)
        iss = T("Ordre de grandeur (hors cours) : à 400 km d'altitude, v ≈ 7,7 km/s, un tour en ≈ 92 min.",
                size=20, color=C_GRIS).to_edge(DOWN, buff=0.25)
        limiter(iss, 13)
        self.play(FadeIn(iss), ang.animate.increment_value(2 * PI), run_time=4, rate_func=linear)
        self.wait(3)
        vider(self)

        # --- 3. Apesanteur apparente ---------------------------------------------------------------------
        self.next_section("apesanteur")
        titre = bandeau("Pourquoi les astronautes « flottent » ?")
        self.play(FadeIn(titre))
        lignes = VGroup(
            T("Le vaisseau est en CHUTE LIBRE permanente autour de la Terre,", size=26),
            T("exactement comme l'ascenseur dont le câble a cassé (chapitre 4) :", size=26),
            T("astronautes et vaisseau tombent ensemble → N = 0.", size=26, color=ACCENT),
            T("Poids apparent nul… mais poids réel bien présent (g ≈ 8,7 N/kg à 400 km) !", size=26, color=C_NEG),
            T("Sur Terre : un avion qui suit une parabole de chute libre (vol « 0 g »).", size=24, color=C_GRIS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        limiter(lignes, 12.8).move_to(DOWN * 0.2)
        for l in lignes:
            self.play(FadeIn(l, shift=UP * 0.1))
            self.wait(1)
        self.wait(4)
        vider(self)
