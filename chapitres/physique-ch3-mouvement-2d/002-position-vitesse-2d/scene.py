"""3.2 — Le mouvement dans le plan : vecteur position, déplacement, vitesse moyenne, vitesse instantanée.

Trajectoire : r(t) = (1 + 1,2t) i + (1 + 3 sin(0,5t)) j.

    manim -pql chapitres/physique-ch3-mouvement-2d/002-position-vitesse-2d/scene.py PositionVitesse2D
"""

from shared.physique import *


def r_de_t(t):
    return np.array([1 + 1.2 * t, 1 + 3 * np.sin(0.5 * t)])


def v_de_t(t):
    return np.array([1.2, 1.5 * np.cos(0.5 * t)])


class PositionVitesse2D(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.2", "Le mouvement dans le plan",
                    "Les mêmes idées qu'au chapitre 2… avec des vecteurs")

        ax = Axes(x_range=[-0.5, 8, 1], y_range=[-0.5, 5, 1], x_length=6.8, y_length=4.4,
                  axis_config={"color": C_GRIS, "include_numbers": True, "font_size": 18}
                  ).move_to(LEFT * 3.0 + DOWN * 0.6)
        lx = M("x", size=28, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        ly = M("y", size=28, color=C_GRIS).next_to(ax.y_axis, UP, buff=0.1)
        O = np.array(ax.c2p(0, 0))
        col = RIGHT * 4.2

        def P(t):
            x, y = r_de_t(t)
            return np.array(ax.c2p(x, y))

        traj = ax.plot_parametric_curve(lambda t: np.array([*r_de_t(t), 0]), t_range=[0, 5],
                                        color=C_GRIS, stroke_width=3)
        traj.set_stroke(opacity=0.7)

        # --- 1. Vecteur position --------------------------------------------------------
        self.next_section("position")
        titre = bandeau("Le vecteur position")
        i_v = fleche(O, ax.c2p(1, 0), C_TEXTE, width=5, tip=0.16)
        j_v = fleche(O, ax.c2p(0, 1), C_TEXTE, width=5, tip=0.16)
        li = M(r"\vec{\imath}", size=28).next_to(i_v, DOWN, buff=0.08)
        lj = M(r"\vec{\jmath}", size=28).next_to(j_v, LEFT, buff=0.08)
        self.play(FadeIn(titre), Create(ax), FadeIn(lx), FadeIn(ly))
        self.play(GrowArrow(i_v), GrowArrow(j_v), FadeIn(li), FadeIn(lj))
        unit = T("vecteurs unitaires (longueur 1)\nselon x et selon y", size=20, color=C_GRIS)
        unit.next_to(ax.c2p(1.2, 0.6), RIGHT, buff=0.1)
        self.play(FadeIn(unit))
        self.wait(1.5)
        self.play(FadeOut(unit))

        t = ValueTracker(0)
        bille = always_redraw(lambda: particule().move_to(P(t.get_value())))
        r_vec = always_redraw(lambda: fleche(O, P(t.get_value()), C_POS, width=6))
        r_lab = always_redraw(lambda: M(r"\vec r", size=34, color=C_POS)
                              .move_to((O + P(t.get_value())) / 2 + np.array([-0.25, 0.25, 0])))
        proj_x = always_redraw(lambda: DashedLine(P(t.get_value()),
                                                  ax.c2p(r_de_t(t.get_value())[0], 0),
                                                  color=C_GRIS, stroke_width=2))
        proj_y = always_redraw(lambda: DashedLine(P(t.get_value()),
                                                  ax.c2p(0, r_de_t(t.get_value())[1]),
                                                  color=C_GRIS, stroke_width=2))
        trace = TracedPath(bille.get_center, stroke_color=ACCENT, stroke_width=3)
        self.add(trace)
        self.play(FadeIn(bille), GrowArrow(r_vec), FadeIn(r_lab), Create(proj_x), Create(proj_y))
        formule = encadre(VGroup(
            M(r"\vec r = x\,\vec{\imath} + y\,\vec{\jmath}\ (+\ z\,\vec k)", size=40),
            T("x et y = composantes de r", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.2)).move_to(col + UP * 2.0)
        self.play(FadeIn(formule))
        coords = Compteur("", lambda: r_de_t(t.get_value())[0], "", decimales=1, size=30,
                          color=C_POS)
        coords2 = Compteur("", lambda: r_de_t(t.get_value())[1], "", decimales=1, size=30,
                           color=C_POS)
        ligne = VGroup(M(r"\vec r =", size=30, color=C_POS), coords, M(r"\vec{\imath}\ +", size=30, color=C_POS),
                       coords2, M(r"\vec{\jmath}", size=30, color=C_POS))
        ligne.arrange(RIGHT, buff=0.12).move_to(col + UP * 0.5)
        # les compteurs se ré-alignent eux-mêmes ; on recale la ligne à chaque image
        ligne.add_updater(lambda g: g.arrange(RIGHT, buff=0.12).move_to(col + UP * 0.5))
        self.play(FadeIn(ligne))
        self.play(t.animate.set_value(5), run_time=6, rate_func=linear)
        self.wait()
        self.play(FadeOut(ligne), FadeOut(proj_x), FadeOut(proj_y), FadeOut(trace),
                  FadeIn(traj))
        ligne.clear_updaters()
        self.remove(ligne)

        # --- 2. Déplacement et vitesse moyenne -------------------------------------------
        self.next_section("deplacement")
        titre2 = bandeau("Déplacement et vitesse moyenne")
        self.play(Transform(titre, titre2), FadeOut(formule), FadeOut(r_lab),
                  t.animate.set_value(1.0))
        t1 = 1.0
        r1 = fleche(O, P(t1), C_POS, width=5)
        l_r1 = M(r"\vec r_1", size=30, color=C_POS).move_to((O + P(t1)) / 2 + np.array([-0.3, 0.15, 0]))
        p1 = Dot(P(t1), color=ACCENT)
        dt = ValueTracker(2.5)
        self.remove(r_vec, bille)
        self.add(r1, p1)
        self.play(FadeIn(l_r1))
        r2 = always_redraw(lambda: fleche(O, P(t1 + dt.get_value()), C_POS, width=5))
        l_r2 = always_redraw(lambda: M(r"\vec r_2", size=30, color=C_POS)
                             .next_to(P(t1 + dt.get_value()), UP, buff=0.15))
        p2 = always_redraw(lambda: Dot(P(t1 + dt.get_value()), color=ACCENT))
        dr = always_redraw(lambda: fleche(P(t1), P(t1 + dt.get_value()), ACCENT, width=6))
        self.play(GrowArrow(r2), FadeIn(l_r2), FadeIn(p2))
        self.play(GrowArrow(dr))
        f_dr = VGroup(
            M(r"\Delta\vec r = \vec r_2 - \vec r_1", size=36, color=ACCENT),
            M(r"= \Delta x\,\vec{\imath} + \Delta y\,\vec{\jmath}", size=36, color=ACCENT),
            T("ne dépend pas de l'origine choisie", size=20, color=C_GRIS),
        ).arrange(DOWN, buff=0.15).move_to(col + UP * 2.0)
        self.play(FadeIn(f_dr))
        self.wait(2)
        vmoy = always_redraw(lambda: fleche(
            P(t1), P(t1) + 0.9 * (P(t1 + dt.get_value()) - P(t1)) / dt.get_value(), C_VIT,
            width=7))
        f_vm = VGroup(
            M(r"\vec v_{\mathrm{moy}} = \frac{\Delta\vec r}{\Delta t}", size=38, color=C_VIT),
            T("même direction que Δr (la sécante)", size=20, color=C_GRIS),
        ).arrange(DOWN, buff=0.15).move_to(col + UP * 0.1)
        self.play(GrowArrow(vmoy), FadeIn(f_vm))
        self.wait(2)
        c_dt = Compteur(r"\Delta t =", lambda: dt.get_value(), r"\mathrm{s}", decimales=2,
                        size=32).move_to(col + DOWN * 1.2)
        self.play(FadeIn(c_dt))
        self.play(FadeOut(l_r2), FadeOut(l_r1))
        self.play(dt.animate.set_value(0.02), run_time=6, rate_func=lambda a: 1 - (1 - a) ** 3)
        tangente = DashedLine(P(t1) - 1.8 * (P(t1 + 0.01) - P(t1)) / np.linalg.norm(P(t1 + 0.01) - P(t1)),
                              P(t1) + 2.6 * (P(t1 + 0.01) - P(t1)) / np.linalg.norm(P(t1 + 0.01) - P(t1)),
                              color=C_VIT, stroke_width=2)
        self.play(Create(tangente))
        f_v = encadre(VGroup(
            M(r"\vec v = \lim_{\Delta t\to 0}\frac{\Delta\vec r}{\Delta t} = \frac{d\vec r}{dt}"
              r" = v_x\vec{\imath} + v_y\vec{\jmath}", size=32, color=C_VIT),
            T("v est TANGENT à la trajectoire", size=24, color=ACCENT),
        ).arrange(DOWN, buff=0.2))
        limiter(f_v, 5.6)
        f_v.move_to(col + DOWN * 2.5)
        self.play(FadeIn(f_v))
        self.wait(4)

        # --- 3. La vitesse tout au long du trajet ------------------------------------------
        self.next_section("v-tangente")
        self.play(FadeOut(VGroup(r1, p1, r2, p2, dr, vmoy, tangente, f_dr, f_vm, c_dt)))
        self.remove(r2, p2, dr, vmoy)
        titre3 = bandeau("La vitesse : toujours tangente à la trajectoire")
        self.play(Transform(titre, titre3), f_v.animate.move_to(col + UP * 2.0))
        t.set_value(0)
        bille = always_redraw(lambda: particule().move_to(P(t.get_value())))

        def v_ecran(tt):
            vx, vy = v_de_t(tt)
            return (np.array(ax.c2p(vx, vy)) - O) * 0.9

        v_vec = always_redraw(lambda: fleche(P(t.get_value()), P(t.get_value()) + v_ecran(t.get_value()),
                                             C_VIT, width=6))
        vx_vec = always_redraw(lambda: DashedLine(P(t.get_value()), P(t.get_value()) +
                                                  v_ecran(t.get_value()) * np.array([1, 0, 0]),
                                                  color=C_VIT, stroke_width=2))
        vy_vec = always_redraw(lambda: DashedLine(P(t.get_value()) + v_ecran(t.get_value()) * np.array([1, 0, 0]),
                                                  P(t.get_value()) + v_ecran(t.get_value()),
                                                  color=C_VIT, stroke_width=2))
        self.play(FadeIn(bille), GrowArrow(v_vec), Create(vx_vec), Create(vy_vec))
        comp = VGroup(M(r"v_x = \frac{dx}{dt}", size=32, color=C_VIT),
                      M(r"v_y = \frac{dy}{dt}", size=32, color=C_VIT)).arrange(RIGHT, buff=0.8)
        comp.move_to(col + UP * 0.4)
        self.play(FadeIn(comp))
        self.play(t.animate.set_value(5), run_time=6, rate_func=linear)
        self.wait()
        attention = encadre(T("Attention : ce dessin est la TRAJECTOIRE\n"
                              "(y en fonction de x), pas un graphe x(t) :\n"
                              "le temps n'y apparaît pas !\n"
                              "v n'est donc pas « une pente » ici,\n"
                              "c'est un vecteur tangent dont\n"
                              "la longueur = la vitesse.", size=22), color=C_NEG)
        limiter(attention, 5.3)
        attention.move_to(col + DOWN * 1.75)
        self.play(FadeIn(attention))
        self.wait(5)
        vider(self)
