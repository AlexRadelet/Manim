"""4.5 — Hors équilibre : la luge tirée sur une pente sans frottement (exemple 1).

Le geste clé : axes inclinés (x le long de la pente) et décomposition du poids
(P sin θ le long de la pente, P cos θ perpendiculairement).
Exemple chiffré (valeurs choisies) : m = 10 kg, T = 60 N, θ = 25°, α = 20°.

    python -m manim -pql chapitres/physique-ch4-dynamique-1/007-plan-incline-luge/scene.py PlanInclineLuge
"""

from shared.physique import *

TH, AL = np.radians(25), np.radians(20)
m, g, T_ = 10.0, 9.8, 60.0
P = m * g
N_ = P * np.cos(TH) - T_ * np.sin(AL)
AX = (T_ * np.cos(AL) - P * np.sin(TH)) / m
K = 0.017


def rot(v, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0])


class PlanInclineLuge(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 4 · section 4.5 · exemple 1", "La luge sur une pente",
                    "Le plan incliné : choisir les bons axes")

        # --- 1. Le schéma ------------------------------------------------------------------
        self.next_section("schema")
        titre = bandeau("Une luge tirée vers le haut d'une pente sans frottement")
        self.play(FadeIn(titre))
        A = np.array([-6.6, -3.0, 0])
        L = 7.6
        B = A + L * np.array([np.cos(TH), np.sin(TH), 0])
        pente = Polygon(A, np.array([B[0], A[1], 0]), B, color=C_SOL, fill_opacity=0.45, stroke_width=0)
        u = np.array([np.cos(TH), np.sin(TH), 0])  # le long de la pente (x)
        n = np.array([-np.sin(TH), np.cos(TH), 0])  # perpendiculaire (y)
        luge = Rectangle(width=1.3, height=0.45, color=PRIMARY, fill_opacity=0.5).rotate(TH)
        C = A + u * 4.6 + n * 0.25
        luge.move_to(C)
        a_th = Angle(Line(np.array([B[0], A[1], 0]), A), Line(A, B), radius=0.9, other_angle=True, color=ACCENT)
        a_th = Arc(radius=0.9, start_angle=0, angle=TH, arc_center=A, color=ACCENT)
        lth = M(r"\theta", size=28, color=ACCENT).move_to(A + 1.25 * np.array([np.cos(TH / 2), np.sin(TH / 2), 0]))
        dT = rot(u, AL)
        corde = Line(C + u * 0.65, C + u * 0.65 + dT * 2.2, color=C_TEXTE, stroke_width=3)
        a_al = Arc(radius=0.8, start_angle=TH, angle=AL, arc_center=C + u * 0.65, color=ACCENT)
        lal = M(r"\alpha", size=26, color=ACCENT).move_to(C + u * 0.65 + 1.1 * rot(u, AL / 2))
        guide = DashedLine(C + u * 0.65, C + u * 2.6, color=C_GRIS, stroke_width=2)
        self.play(FadeIn(pente), Create(a_th), FadeIn(lth))
        self.play(FadeIn(luge), Create(corde), Create(guide), Create(a_al), FadeIn(lal))
        self.wait(1)

        # --- 2. Forces + axes inclinés ---------------------------------------------------------
        self.next_section("forces")
        fP = force(C, DOWN * P * K, r"\vec P", direction=LEFT)
        fN = force(C, n * N_ * K, r"\vec N", direction=UP)
        fT = force(C, dT * T_ * K, r"\vec T", direction=UP)
        self.play(FadeOut(corde), FadeOut(a_al), FadeOut(lal), FadeOut(guide))
        for f in (fP, fN, fT):
            self.play(GrowArrow(f[0]), FadeIn(f[1]), run_time=0.7)
        axes = VGroup(DashedLine(C - u * 2.4, C + u * 3.0, color=C_GRIS, stroke_width=2),
                      DashedLine(C - n * 2.0, C + n * 2.4, color=C_GRIS, stroke_width=2))
        lax = VGroup(M("x", size=28, color=C_GRIS).move_to(C + u * 3.25),
                     M("y", size=28, color=C_GRIS).move_to(C + n * 2.65))
        astuce = T("Astuce : l'axe x LE LONG de la pente,\ncar c'est là que la luge accélère.",
                   size=22, color=ACCENT).move_to(RIGHT * 3.7 + UP * 2.3)
        self.play(Create(axes), FadeIn(lax), FadeIn(astuce))
        self.wait(2)

        # --- 3. Décomposer le poids ---------------------------------------------------------------
        self.next_section("decomposition")
        Pv = DOWN * P * K
        px = np.dot(Pv, u) * u
        py = np.dot(Pv, n) * n
        cx = fleche(C, C + px, C_FORCE, width=4)
        cy = fleche(C, C + py, C_FORCE, width=4)
        d1 = DashedLine(C + px, C + Pv, color=C_FORCE, stroke_width=2)
        d2 = DashedLine(C + py, C + Pv, color=C_FORCE, stroke_width=2)
        lpx = M(r"P\sin\theta", size=26, color=C_FORCE).next_to(C + px, LEFT, buff=0.1)
        lpy = M(r"P\cos\theta", size=26, color=C_FORCE).next_to(C + py, RIGHT, buff=0.1)
        self.play(Create(d1), Create(d2))
        self.play(GrowArrow(cx), GrowArrow(cy), FadeIn(lpx), FadeIn(lpy))
        ang = Arc(radius=0.75, start_angle=-PI / 2, angle=TH, arc_center=C, color=ACCENT)
        lang = M(r"\theta", size=26, color=ACCENT).move_to(C + 1.0 * rot(DOWN, TH / 2))
        pourquoi = T("Le même angle θ se retrouve entre P et l'axe −y\n(deux angles à côtés perpendiculaires)",
                     size=20, color=C_GRIS).next_to(astuce, DOWN, buff=0.35)
        self.play(Create(ang), FadeIn(lang), FadeIn(pourquoi))
        self.wait(3)

        # --- 4. Les équations ------------------------------------------------------------------------
        self.next_section("equations")
        self.play(FadeOut(pourquoi), FadeOut(astuce))
        eqs = VGroup(
            M(r"\sum F_x = T\cos\alpha - P\sin\theta = m a_x", size=30),
            M(r"\sum F_y = T\sin\alpha - P\cos\theta + N = 0", size=30),
            T("(pas d'accélération perpendiculaire à la pente)", size=18, color=C_GRIS),
            M(r"a_x = \frac{T\cos\alpha - P\sin\theta}{m}", size=34, color=C_ACC),
            M(r"N = P\cos\theta - T\sin\alpha", size=34, color=C_FORCE),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.75 + UP * 1.1)
        limiter(eqs, 6.4)
        for e in eqs:
            self.play(FadeIn(e, shift=UP * 0.1))
            self.wait(0.6)
        chiffres = encadre(VGroup(
            T("exemple : m = 10 kg, T = 60 N, θ = 25°, α = 20°", size=20, color=C_GRIS),
            M(rf"a_x = {fr(AX, 2)}\ \mathrm{{m/s^2}} \qquad N = {fr(N_, 1)}\ \mathrm{{N}}", size=30),
        ).arrange(DOWN, buff=0.15), color=C_GRIS)
        limiter(chiffres, 6.4).move_to(RIGHT * 3.75 + DOWN * 2.6)
        self.play(FadeIn(chiffres))
        piege = T("N ≠ P : ici N < P cos θ car la corde soulève un peu la luge", size=20, color=ACCENT)
        limiter(piege, 6.6).next_to(chiffres, UP, buff=0.2)
        self.play(FadeIn(piege))
        self.wait(5)
        vider(self)
