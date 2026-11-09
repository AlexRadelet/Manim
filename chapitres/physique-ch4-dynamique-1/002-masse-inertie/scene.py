"""4.1 — La masse = mesure de l'inertie (résistance aux variations de vitesse) et sa mesure.

1. Même poussée sur un chariot léger et un chariot lourd : le lourd prend moins de vitesse.
2. Deux rondelles repoussées par un ressort : v_B / v_A = m_A / m_B.

    python -m manim -pql chapitres/physique-ch4-dynamique-1/002-masse-inertie/scene.py MasseInertie
"""

from shared.physique import *


class MasseInertie(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 4 · section 4.1", "La masse",
                    "Ce n'est pas « la quantité de matière »… c'est l'inertie")

        # --- 1. Même poussée, masses différentes ------------------------------------------
        self.next_section("meme-poussee")
        titre = bandeau("Même poussée, pendant le même temps", "chariot de 1 kg et chariot de 3 kg")
        self.play(FadeIn(titre))
        rows = []
        for k, (m, y) in enumerate([(1, 1.0), (3, -1.6)]):
            sol = Line([-6.8, y - 0.45, 0], [6.8, y - 0.45, 0], color=C_SOL, stroke_width=5)
            ch = bloc(f"{m}\\ \\mathrm{{kg}}", 0.9 + 0.35 * m, 0.8, size=26).move_to([-5.6, y, 0])
            rows.append((m, y, sol, ch))
            self.play(Create(sol), FadeIn(ch), run_time=0.6)
        poussees = VGroup(*[force(ch.get_left() + LEFT * 0.9, RIGHT * 0.85, r"\vec F", direction=UP)
                            for _, _, _, ch in rows])
        self.play(*[GrowArrow(p[0]) for p in poussees], *[FadeIn(p[1]) for p in poussees])
        self.play(FadeOut(poussees))
        # après la poussée : vitesses 3 et 1 (unités écran / s) -> MRU
        t = ValueTracker(0)
        x0s = [ch.get_x() for _, _, _, ch in rows]
        vs = [3.0, 1.0]
        for (m, y, sol, ch), x0, v in zip(rows, x0s, vs):
            ch.add_updater(lambda mob, x0=x0, v=v: mob.set_x(x0 + v * t.get_value()))
        self.play(t.animate.set_value(3.6), run_time=3.6, rate_func=linear)
        strobo = VGroup(*[VGroup(*[ch[0].copy().set_x(x0 + v * s).set_fill(opacity=0.08).set_stroke(opacity=0.35)
                                   for s in np.arange(0, 3.61, 0.6)])
                          for (m, y, sol, ch), x0, v in zip(rows, x0s, vs)])
        self.play(FadeIn(strobo))
        lab = VGroup(T("1 kg : part vite", size=24, color=C_VIT).move_to([3.5, 2.0, 0]),
                     T("3 kg : 3 fois moins vite", size=24, color=C_VIT).move_to([3.5, -0.6, 0]))
        self.play(FadeIn(lab))
        defi = encadre(T("La masse mesure l'INERTIE : la résistance d'un corps\n"
                         "aux changements de sa vitesse (en grandeur et en direction).", size=24))
        defi.to_edge(DOWN, buff=0.15)
        for _, _, _, ch in rows:
            ch.clear_updaters()
        self.play(FadeIn(defi))
        self.wait(4)
        vider(self)

        # --- 2. Mesurer une masse -------------------------------------------------------------
        self.next_section("mesure")
        titre = bandeau("Comment mesurer une masse ?", "deux rondelles sans frottement, un ressort comprimé entre elles")
        self.play(FadeIn(titre))
        y = 0.4
        A = VGroup(Circle(radius=0.55, color=C_POS, fill_opacity=0.5), M(r"m_A", size=28)).move_to([-1.4, y, 0])
        B = VGroup(Circle(radius=0.38, color=ACCENT, fill_opacity=0.5), M(r"m_B", size=24)).move_to([0.1, y, 0])
        spr = ressort(A.get_right(), B.get_left(), spires=4, largeur=0.15)
        info = T("ici m_A = 2 × m_B", size=22, color=C_GRIS).move_to(UP * 2.2)
        self.play(FadeIn(A), FadeIn(B), Create(spr), FadeIn(info))
        self.wait()
        t = ValueTracker(0)
        vA, vB = -1.0, 2.0
        A.add_updater(lambda m: m.set_x(-1.4 + vA * t.get_value()))
        B.add_updater(lambda m: m.set_x(0.1 + vB * t.get_value()))
        self.play(FadeOut(spr, run_time=0.2))
        self.play(t.animate.set_value(2.0), run_time=2.0, rate_func=linear)
        fa = fleche(A.get_center() + DOWN * 0.9, A.get_center() + DOWN * 0.9 + LEFT * 0.8, C_VIT)
        fb = fleche(B.get_center() + DOWN * 0.9, B.get_center() + DOWN * 0.9 + RIGHT * 1.6, C_VIT)
        la = M(r"v_A", size=30, color=C_VIT).next_to(fa, DOWN, buff=0.1)
        lb = M(r"v_B = 2\,v_A", size=30, color=C_VIT).next_to(fb, DOWN, buff=0.1)
        self.play(GrowArrow(fa), GrowArrow(fb), FadeIn(la), FadeIn(lb))
        A.clear_updaters()
        B.clear_updaters()
        regle = encadre(M(r"\frac{m_A}{m_B} = \frac{v_B}{v_A}", size=46))
        regle.move_to(DOWN * 2.3 + LEFT * 2.5)
        txt = VGroup(T("la plus lourde part la moins vite", size=22),
                     T("on compare à l'étalon : 1 kg", size=22, color=C_GRIS),
                     T("masse : scalaire > 0, en kg, la même partout", size=22, color=ACCENT)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(regle, RIGHT, buff=0.7)
        self.play(FadeIn(regle))
        self.play(FadeIn(txt))
        self.wait(5)
        vider(self)
