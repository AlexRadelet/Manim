"""5.1 — Mesurer μs et μc avec un plan incliné.

On incline le plan de plus en plus : f_s = mg sin θ grandit, f_s(max) = μs mg cos θ diminue.
Le bloc part quand ils se croisent : μs = tan θc (indépendant de la masse).
Exemple : μs = 0,5 -> θc = 26,6°.

    python -m manim -pql chapitres/physique-ch5-dynamique-2/002-plan-incline-mu/scene.py PlanInclineMu
"""

from shared.physique import *

MUS, MUC = 0.5, 0.3
THC = np.arctan(MUS)
L = 7.0
A = np.array([-6.6, -2.8, 0])
K = 1.5  # longueur écran pour m g


class PlanInclineMu(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 5 · section 5.1", "Mesurer un coefficient de frottement",
                    "Il suffit d'un plan qu'on incline doucement")
        titre = bandeau("On incline le plan jusqu'à ce que le bloc glisse", "μs = 0,5 dans cet exemple")
        self.play(FadeIn(titre))

        th = ValueTracker(np.radians(5))
        s = ValueTracker(3.6)  # position du bloc le long de la pente

        def u():
            return np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0])

        def n():
            return np.array([-np.sin(th.get_value()), np.cos(th.get_value()), 0])

        def C():
            return A + u() * s.get_value() + n() * 0.36

        plan = always_redraw(lambda: Polygon(A, A + L * u(), np.array([A[0] + L * np.cos(th.get_value()), A[1], 0]),
                                             color=C_SOL, fill_opacity=0.45, stroke_width=0))
        sol = Line(A + LEFT * 0.2, A + RIGHT * 7.4, color=C_GRIS, stroke_width=2)
        blk = always_redraw(lambda: Square(0.7, color=PRIMARY, fill_opacity=0.6).rotate(th.get_value()).move_to(C()))
        arc = always_redraw(lambda: Arc(radius=1.0, start_angle=0, angle=th.get_value(), arc_center=A, color=ACCENT))

        def fs():
            return min(np.sin(th.get_value()), MUS * np.cos(th.get_value())) if th.get_value() <= THC + 1e-6 \
                else MUC * np.cos(th.get_value())

        fP = always_redraw(lambda: fleche(C(), C() + DOWN * K, C_FORCE, width=5))
        fN = always_redraw(lambda: fleche(C(), C() + n() * K * np.cos(th.get_value()), C_FORCE, width=5))
        fF = always_redraw(lambda: fleche(C() - n() * 0.3, C() - n() * 0.3 + u() * K * fs(), ACCENT, width=6))
        labs = always_redraw(lambda: VGroup(
            M(r"m\vec g", size=26, color=C_FORCE).next_to(C() + DOWN * K, LEFT, buff=0.08),
            M(r"\vec N", size=26, color=C_FORCE).next_to(C() + n() * K * np.cos(th.get_value()), UP, buff=0.05),
            M(r"\vec f_s", size=26, color=ACCENT).next_to(C() - n() * 0.3 + u() * K * fs(), DOWN + RIGHT, buff=0.02)))
        self.play(FadeIn(plan), Create(sol), FadeIn(blk), Create(arc))
        self.add(fP, fN, fF, labs)
        cpt = VGroup(
            Compteur(r"\theta =", lambda: np.degrees(th.get_value()), r"^\circ", decimales=1, size=30, couleur_nombre=ACCENT),
            Compteur(r"\text{besoin : } mg\sin\theta =", lambda: np.sin(th.get_value()), r"\,mg", decimales=2, size=28),
            Compteur(r"\text{max : } \mu_s N = \mu_s mg\cos\theta =", lambda: MUS * np.cos(th.get_value()), r"\,mg",
                     decimales=2, size=28, couleur_nombre=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.3 + UP * 2.0)
        limiter(cpt, 6.4)
        self.play(FadeIn(cpt))
        self.play(th.animate.set_value(THC), run_time=6, rate_func=linear)
        self.wait(1)
        part = T("ça part !  θc ≈ 26,6°", size=28, color=C_NEG).move_to(RIGHT * 3.3 + UP * 0.2)
        self.play(FadeIn(part))
        self.play(th.animate.set_value(THC + 0.005), s.animate.set_value(0.6), run_time=2.2,
                  rate_func=rate_functions.ease_in_quad)
        self.wait()

        # --- calcul ------------------------------------------------------------------------------
        self.next_section("calcul")
        self.play(FadeOut(cpt), FadeOut(part))
        eqs = VGroup(
            M(r"\sum F_x = mg\sin\theta - f_s = 0", size=30),
            M(r"\sum F_y = N - mg\cos\theta = 0", size=30),
            T("au moment où ça part : f_s = μs N", size=22, color=C_GRIS),
            M(r"\mu_s\,mg\cos\theta_c = mg\sin\theta_c", size=30),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.4 + UP * 1.6)
        limiter(eqs, 6.6)
        for e in eqs:
            self.play(FadeIn(e, shift=UP * 0.1))
            self.wait(0.6)
        res = encadre(VGroup(M(r"\mu_s = \tan\theta_c", size=46, color=ACCENT),
                             T("m s'est simplifié : l'angle ne dépend pas de la masse", size=20, color=C_GRIS)
                             ).arrange(DOWN, buff=0.15))
        res.move_to(RIGHT * 3.4 + DOWN * 1.1)
        self.play(FadeIn(res))
        dyn = T("Et pour μc : on ajuste θ pour que le bloc, une fois lancé,\n"
                "descende à vitesse CONSTANTE : alors μc = tan θc'.",
                size=20, color=C_GRIS).move_to(RIGHT * 3.4 + DOWN * 2.7)
        limiter(dyn, 6.8)
        self.play(FadeIn(dyn))
        self.wait(5)
        vider(self)
