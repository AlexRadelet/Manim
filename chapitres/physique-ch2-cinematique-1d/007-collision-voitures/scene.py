"""2.6 — Exemple 2 : deux cascadeurs foncent l'un vers l'autre. Où et quand se percutent-ils ?

A : x_A0 = 0,  v_A0 = +16 m/s, a_A = +2 m/s²
B : x_B0 = 45, v_B0 = −8 m/s,  a_B = −4 m/s²
-> collision à t = 1,57 s, x = 27,6 m.

    manim -pql chapitres/physique-ch2-cinematique-1d/007-collision-voitures/scene.py CollisionVoitures
"""

from shared.physique import *

T_COL = (-24 + np.sqrt(24 ** 2 + 4 * 3 * 45)) / 6  # 1,568 s


def xa(t):
    return 16 * t + t * t


def xb(t):
    return 45 - 8 * t - 2 * t * t


class CollisionVoitures(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.6 · exemple 2", "Collision !",
                    "Deux MRUA sur le même axe : quand ont-ils la même position ?")
        titre = bandeau("Deux cascadeurs foncent l'un vers l'autre")
        self.play(FadeIn(titre))

        # --- La route ------------------------------------------------------------
        route = NumberLine(x_range=[0, 50, 5], length=11.5, include_numbers=True,
                           font_size=20, color=C_GRIS).move_to(UP * 1.95)
        lab = M(r"x\ (\mathrm{m})", size=24, color=C_GRIS).next_to(route, RIGHT, buff=0.1)
        t = ValueTracker(0)
        auto_a = voiture(C_POS, 0.75)
        auto_b = voiture(C_ACC, 0.75).flip(UP)
        auto_a.add_updater(lambda m: m.move_to(route.n2p(xa(t.get_value())) + UP * 0.3))
        auto_b.add_updater(lambda m: m.move_to(route.n2p(xb(t.get_value())) + UP * 0.3))
        la = T("A", size=24, color=C_POS, weight=BOLD)
        lb = T("B", size=24, color=C_ACC, weight=BOLD)
        la.add_updater(lambda m: m.next_to(auto_a, UP, buff=0.08))
        lb.add_updater(lambda m: m.next_to(auto_b, UP, buff=0.08))
        self.play(Create(route), FadeIn(lab), FadeIn(auto_a), FadeIn(auto_b), FadeIn(la),
                  FadeIn(lb))

        donnees = VGroup(
            M(r"A:\ x_{A0} = 0,\ \ v_{Ax0} = +16\ \mathrm{m/s},\ \ a_{Ax} = +2\ \mathrm{m/s^2}",
              size=30, color=C_POS),
            M(r"B:\ x_{B0} = 45\ \mathrm{m},\ \ v_{Bx0} = -8\ \mathrm{m/s},\ \ "
              r"a_{Bx} = -4\ \mathrm{m/s^2}", size=30, color=C_ACC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 0.15)
        attention = T("B va vers la gauche → sa vitesse ET son accélération sont négatives",
                      size=22, color=ACCENT).next_to(donnees, DOWN, buff=0.3)
        self.play(FadeIn(donnees[0]))
        self.play(FadeIn(donnees[1]))
        self.play(FadeIn(attention))
        self.wait(4)
        self.play(FadeOut(attention), donnees.animate.scale(0.7).move_to(RIGHT * 3.6 + UP * 0.6))

        # --- Graphe x(t) ----------------------------------------------------------
        self.next_section("graphe")
        ax = Axes(x_range=[0, 2, 0.5], y_range=[0, 50, 10], x_length=5.6, y_length=3.6,
                  axis_config={"color": C_GRIS, "include_numbers": True, "font_size": 20}
                  ).move_to(LEFT * 3.5 + DOWN * 1.75)
        ax_lt = M(r"t\ (\mathrm{s})", size=24, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        ax_lx = M(r"x\ (\mathrm{m})", size=24, color=C_GRIS).next_to(ax.y_axis, UP, buff=0.1)
        self.play(Create(ax), FadeIn(ax_lt), FadeIn(ax_lx))
        ca = always_redraw(lambda: ax.plot(xa, x_range=[0, max(t.get_value(), 1e-3)],
                                           color=C_POS, stroke_width=4))
        cb = always_redraw(lambda: ax.plot(xb, x_range=[0, max(t.get_value(), 1e-3)],
                                           color=C_ACC, stroke_width=4))
        horloge = Compteur("t =", lambda: t.get_value(), r"\mathrm{s}", decimales=2, size=30)
        horloge.next_to(route, DOWN, buff=0.35).set_x(0)
        ralenti = T("(ralenti)", size=20, color=C_GRIS).next_to(horloge, RIGHT, buff=0.3)
        self.add(ca, cb)
        self.play(FadeIn(horloge), FadeIn(ralenti))
        self.play(t.animate.set_value(T_COL), run_time=6, rate_func=linear)
        boum = Star(n=8, outer_radius=0.45, inner_radius=0.2, color=ACCENT, fill_opacity=0.9)
        boum.move_to(route.n2p(xa(T_COL)) + UP * 0.3)
        p_col = Dot(ax.c2p(T_COL, xa(T_COL)), color=ACCENT, radius=0.1)
        self.play(GrowFromCenter(boum), FadeIn(p_col, scale=2))
        idee = T("Collision ⇔ même position au même instant\n"
                 "⇔ les deux courbes se croisent", size=22, color=ACCENT)
        idee.move_to(RIGHT * 3.6 + DOWN * 0.45)
        self.play(FadeIn(idee))
        self.wait(3)

        # --- Le calcul ------------------------------------------------------------
        self.next_section("calcul")
        calc = VGroup(
            M(r"x_A = 16t + t^2", size=30, color=C_POS),
            M(r"x_B = 45 - 8t - 2t^2", size=30, color=C_ACC),
            M(r"x_A = x_B \ \Rightarrow\ 3t^2 + 24t - 45 = 0", size=32),
            M(r"t = \frac{-24 \pm \sqrt{24^2 - 4(3)(-45)}}{2(3)}", size=32),
            M(r"t = 1{,}57\ \mathrm{s}", r"\quad \text{ou} \quad", r"-9{,}57\ \mathrm{s}",
              size=32),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.6 + DOWN * 1.55)
        calc[-1][2].set_color(C_NEG)
        barre = Line(calc[-1][2].get_corner(DL), calc[-1][2].get_corner(UR), color=C_NEG,
                     stroke_width=4)
        self.play(FadeOut(donnees), idee.animate.scale(0.85).move_to(RIGHT * 3.6 + UP * 0.6))
        for c in calc:
            self.play(Write(c), run_time=1)
            self.wait(0.5)
        rejet = T("t < 0 : avant le début de l'histoire → rejeté", size=20, color=C_NEG)
        rejet.next_to(calc, DOWN, buff=0.12)
        self.play(Create(barre), FadeIn(rejet))
        self.wait(2)
        resultat = encadre(M(r"x_A(1{,}57) = 16(1{,}57) + 1{,}57^2 \approx 27{,}6\ \mathrm{m}",
                             size=32))
        resultat.move_to(LEFT * 3.4 + DOWN * 1.75)
        lect = VGroup(DashedLine(ax.c2p(T_COL, 0), p_col.get_center(), color=ACCENT),
                      DashedLine(ax.c2p(0, xa(T_COL)), p_col.get_center(), color=ACCENT))
        self.play(Create(lect))
        self.wait(1)
        self.play(FadeOut(VGroup(ax, ax_lt, ax_lx, ca, cb, p_col, lect)), FadeIn(resultat))
        self.wait(5)
        vider(self)
