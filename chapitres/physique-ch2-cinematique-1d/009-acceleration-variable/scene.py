"""2.8 — Accélération variable : a_x = 3t -> v_x = 3t²/2 -> x = t³/2 (départ au repos, à l'origine).

Synthèse du chapitre : on DESCEND par des aires (intégrales), on REMONTE par des pentes (dérivées).

    manim -pql chapitres/physique-ch2-cinematique-1d/009-acceleration-variable/scene.py AccelerationVariable
"""

from shared.physique import *


def a_f(t):
    return 3 * t


def v_f(t):
    return 1.5 * t * t


def x_f(t):
    return 0.5 * t ** 3


class AccelerationVariable(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.8", "Quand l'accélération varie",
                    "Plus d'équations toutes faites : on intègre")
        titre = bandeau("a(t), v(t), x(t) : trois étages reliés")
        self.play(FadeIn(titre))

        def axes(ymax, pas, nom, couleur, y):
            ax = Axes(x_range=[0, 2.2, 0.5], y_range=[0, ymax, pas], x_length=6.2, y_length=1.55,
                      axis_config={"color": C_GRIS, "font_size": 18},
                      x_axis_config={"include_numbers": True, "numbers_to_include": [1, 2],
                                     "decimal_number_config": {"num_decimal_places": 0}},
                      y_axis_config={"include_numbers": True},
                      tips=False).move_to([-2.6, y, 0])
            l = M(nom, size=28, color=couleur).next_to(ax.y_axis, UP, buff=0.05)
            return ax, l

        ax_a, la = axes(6, 3, "a_x", C_ACC, 1.85)
        ax_v, lv = axes(6, 3, "v_x", C_VIT, -0.5)
        ax_x, lx = axes(4, 2, "x", C_POS, -2.85)
        g_a = ax_a.plot(a_f, x_range=[0, 2], color=C_ACC, stroke_width=4)
        g_v = ax_v.plot(v_f, x_range=[0, 2], color=C_VIT, stroke_width=4)
        g_x = ax_x.plot(x_f, x_range=[0, 2], color=C_POS, stroke_width=4)
        e_a = M(r"a_x = 3t", size=30, color=C_ACC).next_to(ax_a.c2p(2, 6), RIGHT, buff=0.2)
        e_v = M(r"v_x = \tfrac{3}{2}t^2", size=30, color=C_VIT).next_to(ax_v.c2p(2, 6), RIGHT, buff=0.2)
        e_x = M(r"x = \tfrac12 t^3", size=30, color=C_POS).next_to(ax_x.c2p(2, 4), RIGHT, buff=0.2)

        self.play(Create(ax_a), FadeIn(la), Create(g_a), FadeIn(e_a))
        self.wait()

        # --- calcul ---------------------------------------------------------------
        calc = VGroup(
            T("départ au repos, à l'origine", size=20, color=C_GRIS),
            M(r"v_x = \int_0^t 3t\,dt = \frac{3t^2}{2}", size=32, color=C_VIT),
            M(r"x = \int_0^t \frac{3t^2}{2}\,dt = \frac{t^3}{2}", size=32, color=C_POS),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 4.6 + UP * 0.1)
        self.play(FadeIn(calc[0]), Write(calc[1]))
        self.play(Create(ax_v), FadeIn(lv), Create(g_v), FadeIn(e_v))
        self.play(Write(calc[2]))
        self.play(Create(ax_x), FadeIn(lx), Create(g_x), FadeIn(e_x))
        self.wait(2)
        self.play(FadeOut(calc))

        # flèches « intégrer » / « dériver »
        fl_int = VGroup(Arrow(UP * 2.2, DOWN * 2.6, color=ACCENT, buff=0, stroke_width=5),
                        T("intégrer\n(aire)", size=22, color=ACCENT))
        fl_int[1].next_to(fl_int[0], RIGHT, buff=0.15)
        fl_der = VGroup(Arrow(DOWN * 2.6, UP * 2.2, color=C_TEXTE, buff=0, stroke_width=5),
                        T("dériver\n(pente)", size=22, color=C_TEXTE))
        fl_der[1].next_to(fl_der[0], RIGHT, buff=0.15)
        fl_int.move_to(RIGHT * 3.9 + DOWN * 0.3)
        fl_der.move_to(RIGHT * 5.9 + DOWN * 0.3)

        # --- 1. on descend par les aires -------------------------------------------
        self.next_section("aires")
        self.play(GrowArrow(fl_int[0]), FadeIn(fl_int[1]))
        t = ValueTracker(0.05)
        aire_a = always_redraw(lambda: ax_a.get_area(g_a, x_range=[0, t.get_value()],
                                                     color=C_ACC, opacity=0.4))
        aire_v = always_redraw(lambda: ax_v.get_area(g_v, x_range=[0, t.get_value()],
                                                     color=C_VIT, opacity=0.4))
        pt_v = always_redraw(lambda: Dot(ax_v.c2p(t.get_value(), v_f(t.get_value())),
                                         color=ACCENT, radius=0.08))
        pt_x = always_redraw(lambda: Dot(ax_x.c2p(t.get_value(), x_f(t.get_value())),
                                         color=ACCENT, radius=0.08))
        curseur = always_redraw(lambda: DashedLine(ax_a.c2p(t.get_value(), 6),
                                                   ax_x.c2p(t.get_value(), 0),
                                                   color=C_GRIS, stroke_width=1.5))
        c_a = Compteur(r"\text{aire} =", lambda: v_f(t.get_value()), "", decimales=2, size=24,
                       color=C_ACC).move_to(ax_a.c2p(0.55, 4.6))
        c_v = Compteur(r"\text{aire} =", lambda: x_f(t.get_value()), "", decimales=2, size=24,
                       color=C_VIT).move_to(ax_v.c2p(0.55, 4.6))
        self.add(aire_a, aire_v, curseur)
        self.play(FadeIn(pt_v), FadeIn(pt_x), FadeIn(c_a), FadeIn(c_v))
        self.play(t.animate.set_value(2), run_time=6, rate_func=linear)
        msg = T("aire sous a(t) = hauteur de v(t)\naire sous v(t) = hauteur de x(t)",
                size=22, color=ACCENT).to_corner(UR, buff=0.35)
        self.play(FadeIn(msg))
        self.wait(3)
        self.play(FadeOut(VGroup(aire_a, aire_v, c_a, c_v, msg, pt_v, pt_x, curseur)))
        self.remove(aire_a, aire_v, curseur, pt_v, pt_x)

        # --- 2. on remonte par les pentes --------------------------------------------
        self.next_section("pentes")
        self.play(GrowArrow(fl_der[0]), FadeIn(fl_der[1]))
        t.set_value(0.3)

        def tangente(ax, f, df, tt, couleur):
            p = np.array(ax.c2p(tt, f(tt)))
            u = np.array(ax.c2p(1, df(tt))) - np.array(ax.c2p(0, 0))
            u = u / np.linalg.norm(u)
            return Line(p - u * 0.7, p + u * 0.7, color=couleur, stroke_width=4)

        tg_x = always_redraw(lambda: tangente(ax_x, x_f, v_f, t.get_value(), C_VIT))
        tg_v = always_redraw(lambda: tangente(ax_v, v_f, a_f, t.get_value(), C_ACC))
        pt_a = always_redraw(lambda: Dot(ax_a.c2p(t.get_value(), a_f(t.get_value())),
                                         color=ACCENT, radius=0.08))
        pt_v = always_redraw(lambda: Dot(ax_v.c2p(t.get_value(), v_f(t.get_value())),
                                         color=ACCENT, radius=0.08))
        c_x = Compteur(r"\text{pente} =", lambda: v_f(t.get_value()), "", decimales=2, size=24,
                       color=C_VIT).move_to(ax_x.c2p(0.6, 3.2))
        c_v2 = Compteur(r"\text{pente} =", lambda: a_f(t.get_value()), "", decimales=2, size=24,
                        color=C_ACC).move_to(ax_v.c2p(0.6, 4.6))
        self.play(FadeIn(tg_x), FadeIn(tg_v), FadeIn(pt_a), FadeIn(pt_v), FadeIn(c_x),
                  FadeIn(c_v2))
        self.play(t.animate.set_value(1.95), run_time=6, rate_func=linear)
        msg2 = T("pente de x(t) = valeur de v\npente de v(t) = valeur de a", size=22,
                 color=C_TEXTE).to_corner(UR, buff=0.35)
        self.play(FadeIn(msg2))
        self.wait(5)
        vider(self)
