"""2.3 — Le déplacement = aire sous la courbe de v_x(t) (aires sous l'axe comptées négativement).

Partie 1 : v constante -> rectangle.
Partie 2 : v_x(t) = 4 − t -> somme de rectangles -> intégrale ; Δx = 8 − 2 = 6 m.

    manim -pql chapitres/physique-ch2-cinematique-1d/004-aire-sous-vitesse/scene.py AireSousVitesse
"""

from shared.physique import *


def v_de_t(t):
    return 4 - t


def x_de_t(t):  # x(0) = 0
    return 4 * t - t * t / 2


class AireSousVitesse(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.3", "Le déplacement à partir de la vitesse",
                    "On a lu la vitesse comme une pente… on lit le déplacement comme une aire")

        ax = Axes(x_range=[0, 6.5, 1], y_range=[-3, 5, 1], x_length=7, y_length=5.2,
                  axis_config={"color": C_GRIS, "include_numbers": True, "font_size": 22}
                  ).move_to(LEFT * 2.2 + DOWN * 0.5)
        lab_t = M(r"t\ (\mathrm{s})", size=28, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        lab_v = M(r"v_x\ (\mathrm{m/s})", size=28, color=C_GRIS).next_to(ax.y_axis, UP, buff=0.1)
        droite_x = 4.55  # centre de la colonne de droite

        # --- 1. Vitesse constante --------------------------------------------
        self.next_section("constante")
        titre = bandeau("Vitesse constante : un rectangle")
        cst = ax.plot(lambda t: 3, x_range=[0, 6], color=C_VIT, stroke_width=5)
        self.play(FadeIn(titre), Create(ax), FadeIn(lab_t), FadeIn(lab_v))
        self.play(Create(cst))
        rect = Polygon(ax.c2p(0, 0), ax.c2p(4, 0), ax.c2p(4, 3), ax.c2p(0, 3),
                       stroke_width=0, fill_color=C_VIT, fill_opacity=0.35)
        b_h = BraceBetweenPoints(ax.c2p(0, 0), ax.c2p(4, 0), direction=DOWN, color=C_GRIS)
        b_h.shift(DOWN * 0.4)
        l_h = M(r"\Delta t = 4\ \mathrm{s}", size=30).next_to(b_h, DOWN, buff=0.1)
        b_v = BraceBetweenPoints(ax.c2p(4, 0), ax.c2p(4, 3), direction=RIGHT, color=C_GRIS)
        l_v = M(r"v_x = 3\ \mathrm{m/s}", size=30, color=C_VIT).next_to(b_v, RIGHT, buff=0.1)
        self.play(FadeIn(rect), GrowFromCenter(b_h), FadeIn(l_h), GrowFromCenter(b_v),
                  FadeIn(l_v))
        calc = VGroup(
            M(r"\Delta x = v_x\,\Delta t", size=40),
            M(r"= 3 \times 4 = 12\ \mathrm{m}", size=40),
            T("= aire du rectangle", size=26, color=C_VIT),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * droite_x + UP * 1.2)
        for c in calc:
            self.play(FadeIn(c, shift=UP * 0.15))
        self.wait(3)
        self.play(FadeOut(VGroup(cst, rect, b_h, l_h, b_v, l_v, calc)))

        # --- 2. Vitesse variable : des rectangles de plus en plus fins -----------
        self.next_section("rectangles")
        titre2 = bandeau("Vitesse variable : plein de petits rectangles")
        self.play(Transform(titre, titre2))
        graphe = ax.plot(v_de_t, x_range=[0, 6], color=C_VIT, stroke_width=5)
        g_lab = M(r"v_x = 4 - t", size=32, color=C_VIT).next_to(ax.c2p(0.7, 4.2), RIGHT)
        self.play(Create(graphe), FadeIn(g_lab))

        def rectangles(dx):
            rs = ax.get_riemann_rectangles(graphe, x_range=[0, 6], dx=dx,
                                           input_sample_type="center", stroke_width=1,
                                           stroke_color=BACKGROUND, fill_opacity=0.55)
            for r in rs:
                tm = ax.p2c(r.get_center())[0]
                r.set_fill(C_VIT if v_de_t(tm) > 0 else C_NEG, opacity=0.55)
            return rs

        somme = VGroup(
            M(r"\Delta x \approx \sum_j v_{xj}\,\Delta t", size=40),
            T("chaque rectangle :\nvitesse × petit intervalle", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * droite_x + UP * 1.6)
        rs = rectangles(1)
        self.play(Create(rs), FadeIn(somme))
        self.wait(2)
        for dx in (0.5, 0.25, 0.1, 0.03):
            self.play(Transform(rs, rectangles(dx)), run_time=1.3)
            self.wait(0.4)
        integrale = encadre(VGroup(
            M(r"\Delta x = \lim_{\Delta t\to 0}\sum_j v_{xj}\Delta t = \int_{t_i}^{t_f} v_x\,dt",
              size=34),
            T("= aire entre la courbe et l'axe des t", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.2))
        limiter(integrale, 4.4)
        integrale.move_to(RIGHT * droite_x + DOWN * 0.3)
        self.play(FadeIn(integrale, shift=UP * 0.2))
        self.wait(3)

        # --- 3. Les aires sous l'axe comptent négativement -------------------
        self.next_section("signe")
        self.play(FadeOut(VGroup(somme, integrale)))
        a_pos = ax.get_area(graphe, x_range=[0, 4], color=C_VIT, opacity=0.5)
        a_neg = ax.get_area(graphe, x_range=[4, 6], color=C_NEG, opacity=0.5)
        self.play(FadeOut(rs), FadeIn(a_pos), FadeIn(a_neg))
        l_pos = M(r"+8\ \mathrm{m}", size=36, color=C_TEXTE).move_to(ax.c2p(1.4, 1.2))
        l_neg = M(r"-2\ \mathrm{m}", size=32, color=C_NEG).move_to(ax.c2p(6.75, -1.3))
        self.play(Write(l_pos))
        explication = VGroup(
            T("v < 0 → la particule recule", size=24, color=C_NEG),
            T("→ cette aire compte en négatif", size=24, color=C_NEG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        limiter(explication, 4.4).move_to(RIGHT * droite_x + UP * 1.7)
        self.play(Write(l_neg), FadeIn(explication))
        total = M(r"\Delta x = (+8) + (-2) = +6\ \mathrm{m}", size=40, color=C_POS)
        limiter(total, 4.4).move_to(RIGHT * droite_x + UP * 0.5)
        self.play(Write(total))
        self.wait(2)

        # on le vérifie en regardant la particule
        rail = NumberLine(x_range=[0, 9, 1], length=4.0, include_numbers=True, font_size=20,
                          color=C_GRIS).move_to(RIGHT * (droite_x - 0.2) + DOWN * 1.6)
        rail_lab = M(r"x\ (\mathrm{m})", size=24, color=C_GRIS).next_to(rail, RIGHT, buff=0.1)
        t = ValueTracker(0)
        bille = always_redraw(lambda: particule().move_to(rail.n2p(x_de_t(t.get_value()))))
        curseur = always_redraw(lambda: DashedLine(ax.c2p(t.get_value(), -3),
                                                   ax.c2p(t.get_value(), 5),
                                                   color=ACCENT, stroke_width=2))
        verif = T("Vérification : on regarde bouger la particule", size=22, color=C_GRIS)
        limiter(verif, 4.4).next_to(rail, UP, buff=0.35).set_x(droite_x)
        self.play(FadeIn(verif), Create(rail), FadeIn(rail_lab), FadeIn(bille), FadeIn(curseur))
        self.play(t.animate.set_value(4), run_time=4, rate_func=linear)
        n1 = T("va jusqu'à 8 m…", size=22, color=C_VIT).next_to(rail, DOWN, buff=0.5)
        self.play(FadeIn(n1))
        self.play(t.animate.set_value(6), run_time=2.5, rate_func=linear)
        n2 = T("…puis recule de 2 m : arrive à 6 m ✔", size=22, color=C_POS)
        limiter(n2, 4.4).next_to(rail, DOWN, buff=0.5)
        self.play(ReplacementTransform(n1, n2))
        self.wait(4)
        vider(self)
