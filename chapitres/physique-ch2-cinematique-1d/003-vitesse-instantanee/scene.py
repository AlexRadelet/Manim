"""2.3 — Vitesse instantanée : la sécante devient tangente quand Δt → 0.

x(t) = 1 + 4t − 0,6t²  (monte, s'arrête, redescend : le signe de v change).

    manim -pql chapitres/physique-ch2-cinematique-1d/003-vitesse-instantanee/scene.py VitesseInstantanee
"""

from shared.physique import *


def x_de_t(t):
    return 1 + 4 * t - 0.6 * t * t


def v_de_t(t):
    return 4 - 1.2 * t


class VitesseInstantanee(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.3", "La vitesse instantanée",
                    "Que vaut la vitesse à UN instant précis ?")

        titre = bandeau("De la sécante à la tangente")
        ax = Axes(x_range=[0, 6.5, 1], y_range=[0, 9, 2], x_length=6.6, y_length=5.2,
                  axis_config={"color": C_GRIS, "include_numbers": True, "font_size": 22}
                  ).move_to(LEFT * 1.3 + DOWN * 0.35)
        lab_t = M(r"t\ (\mathrm{s})", size=28, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        lab_x = M(r"x\ (\mathrm{m})", size=28, color=C_GRIS).next_to(ax.y_axis, UP, buff=0.1)
        courbe = ax.plot(x_de_t, x_range=[0, 6], color=C_POS, stroke_width=5)
        self.play(FadeIn(titre), Create(ax), FadeIn(lab_t), FadeIn(lab_x))
        self.play(Create(courbe), run_time=2)

        def P(tt):
            return np.array(ax.c2p(tt, x_de_t(tt)))

        # --- 1. Δt → 0 ------------------------------------------------------
        self.next_section("dt-vers-0")
        ti = 1.5
        dt = ValueTracker(3.0)

        def pente():
            d = dt.get_value()
            return (x_de_t(ti + d) - x_de_t(ti)) / d

        def droite(point, m, couleur, demi=1.6):
            u = np.array(ax.c2p(1, m)) - np.array(ax.c2p(0, 0))
            u = u / np.linalg.norm(u)
            return Line(point - u * demi, point + u * demi, color=couleur, stroke_width=4)

        def secante():
            a, b = P(ti), P(ti + dt.get_value())
            u = (b - a) / np.linalg.norm(b - a)
            return Line(a - u * 0.9, b + u * 0.9, color=C_VIT, stroke_width=4)

        sec = always_redraw(secante)
        pi_dot = Dot(P(ti), color=ACCENT, radius=0.09).set_z_index(3)
        pf_dot = always_redraw(lambda: Dot(P(ti + dt.get_value()), color=ACCENT, radius=0.08))
        lab_ti = M("t_i", size=28, color=ACCENT).next_to(ax.c2p(ti, 0), DOWN, buff=0.45)
        self.play(FadeIn(pi_dot), FadeIn(lab_ti))
        self.play(FadeIn(pf_dot), Create(sec))

        panneau = VGroup(
            VGroup(M(r"\Delta t =", size=36), DecimalFR(3, num_decimal_places=3, font_size=36),
                   M(r"\mathrm{s}", size=32)).arrange(RIGHT, buff=0.12),
            VGroup(M(r"\frac{\Delta x}{\Delta t} =", size=36, color=C_VIT),
                   DecimalFR(pente(), num_decimal_places=3, font_size=36, color=C_VIT),
                   M(r"\mathrm{m/s}", size=32)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 4.6 + UP * 1.6)
        panneau[0][1].add_updater(lambda d: d.set_value(dt.get_value()))
        panneau[1][1].add_updater(lambda d: d.set_value(pente()))
        self.play(FadeIn(panneau))
        self.wait()
        self.play(dt.animate.set_value(0.01), run_time=7, rate_func=lambda a: 1 - (1 - a) ** 3)
        self.wait()
        tangente_txt = T("La sécante est devenue\nla TANGENTE en t_i", size=26, color=ACCENT)
        tangente_txt.next_to(panneau, DOWN, buff=0.5)
        self.play(FadeIn(tangente_txt))
        self.wait(2)

        definition = encadre(VGroup(
            M(r"v_x = \lim_{\Delta t \to 0} \frac{\Delta x}{\Delta t} = \frac{dx}{dt}",
              size=40, color=C_VIT),
            T("= pente de la tangente à x(t)", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.2))
        limiter(definition, 4.2)
        definition.move_to(RIGHT * 4.85 + DOWN * 1.55)
        self.play(FadeIn(definition, shift=UP * 0.2))
        self.wait(4)

        # --- 2. La tangente se promène : signe de v ---------------------------
        self.next_section("tangente-mobile")
        self.play(FadeOut(VGroup(panneau, tangente_txt, sec, pf_dot, pi_dot, lab_ti)),
                  definition.animate.scale(0.8).to_corner(DR, buff=0.4))
        t = ValueTracker(0.3)

        def couleur(v):
            if abs(v) < 0.08:
                return ACCENT
            return C_VIT if v > 0 else C_NEG

        tang = always_redraw(lambda: droite(P(t.get_value()), v_de_t(t.get_value()),
                                            couleur(v_de_t(t.get_value()))))
        point = always_redraw(lambda: Dot(P(t.get_value()), color=ACCENT, radius=0.09))

        # la particule sur l'axe des x « redressé », à gauche
        x_ecran = ax.y_axis.get_x() - 1.3
        rail = Line(ax.c2p(0, 0), ax.c2p(0, 9), color=C_GRIS).set_x(x_ecran)
        bille = always_redraw(lambda: particule().move_to(
            [x_ecran, ax.c2p(0, x_de_t(t.get_value()))[1], 0]))
        fl_v = always_redraw(lambda: fleche(
            bille.get_center(),
            bille.get_center() + UP * 0.35 * v_de_t(t.get_value()),
            couleur(v_de_t(t.get_value())), width=6))
        lab_rail = M("x", size=28, color=C_GRIS).next_to(rail, UP, buff=0.1)
        val = VGroup(M("v_x =", size=36),
                     DecimalFR(v_de_t(0.3), num_decimal_places=2, include_sign=True,
                               font_size=36),
                     M(r"\mathrm{m/s}", size=32)).arrange(RIGHT, buff=0.12)
        val.move_to(RIGHT * 4.6 + UP * 1.9)
        val[1].add_updater(lambda d: d.set_value(v_de_t(t.get_value()))
                           .set_color(couleur(v_de_t(t.get_value()))))
        self.play(Create(rail), FadeIn(lab_rail), FadeIn(bille), FadeIn(point), Create(tang),
                  FadeIn(fl_v), FadeIn(val))
        self.play(t.animate.set_value(10 / 3), run_time=5, rate_func=linear)
        arret = T("Tangente horizontale\n→ v = 0 : demi-tour !", size=26, color=ACCENT)
        arret.next_to(val, DOWN, buff=0.5)
        self.play(FadeIn(arret))
        self.wait(2)
        self.play(FadeOut(arret))
        self.play(t.animate.set_value(5.8), run_time=4, rate_func=linear)
        signes = VGroup(
            T("pente > 0  →  v > 0 : vers les x positifs", size=22, color=C_VIT),
            T("pente < 0  →  v < 0 : vers les x négatifs", size=22, color=C_NEG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(val, DOWN, buff=0.5)
        limiter(signes, 4.3)
        signes.set_x(4.85)
        self.play(FadeIn(signes))
        self.wait(4)
        vider(self)
