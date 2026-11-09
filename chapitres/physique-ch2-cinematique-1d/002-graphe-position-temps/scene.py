"""2.2 — Représentation graphique : le graphe x(t) et la vitesse moyenne = pente de la sécante.

Idée clé : on « couche » l'axe des x à la verticale, à côté du graphe,
pour que l'élève voie que la hauteur de la courbe = la position de la particule.

    manim -pql chapitres/physique-ch2-cinematique-1d/002-graphe-position-temps/scene.py GraphePositionTemps
"""

from shared.physique import *


def x_de_t(t: float) -> float:
    s = t / 6
    return 2 + 7 * s * s * (3 - 2 * s)


class GraphePositionTemps(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.2", "Le graphe de la position x(t)",
                    "La vitesse moyenne se lit comme une pente")

        # --- 1. De l'axe horizontal à l'axe vertical -------------------------
        self.next_section("axe-vertical")
        titre = bandeau("Raconter un mouvement avec un graphe")
        ligne = NumberLine(x_range=[0, 10, 1], length=5.2, include_numbers=True,
                           font_size=22, color=C_GRIS)
        bille = particule().move_to(ligne.n2p(2))
        self.play(FadeIn(titre), Create(ligne), FadeIn(bille))
        self.play(bille.animate.move_to(ligne.n2p(9)), run_time=2)
        self.play(bille.animate.move_to(ligne.n2p(2)), run_time=1)
        idee = T("On redresse l'axe des x à la verticale…\n…pour garder le temps à l'horizontale",
                 size=24, color=C_GRIS).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(idee))

        ax = Axes(x_range=[0, 6.5, 1], y_range=[0, 10.5, 2], x_length=6.6, y_length=5.2,
                  axis_config={"color": C_GRIS, "include_numbers": True, "font_size": 22},
                  tips=True).move_to(LEFT * 1.3 + DOWN * 0.35)
        lab_t = M(r"t\ (\mathrm{s})", size=28, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        lab_x = M(r"x\ (\mathrm{m})", size=28, color=C_GRIS).next_to(ax.y_axis, UP, buff=0.1)
        x_ecran = ax.y_axis.get_x() - 1.5

        def y_ecran(x):
            return ax.c2p(0, x)[1]

        cible = ligne.copy().rotate(PI / 2)
        cible.stretch_to_fit_height(y_ecran(10) - y_ecran(0))
        cible.move_to([x_ecran, (y_ecran(10) + y_ecran(0)) / 2, 0])
        for n in cible.numbers:  # remettre les nombres à l'endroit
            n.rotate(-PI / 2)
        self.play(Transform(ligne, cible),
                  bille.animate.move_to([x_ecran, y_ecran(2), 0]), run_time=1.8)
        self.play(FadeOut(idee), Create(ax), FadeIn(lab_t), FadeIn(lab_x))
        self.wait()

        # --- 2. On trace x(t) en même temps que la particule bouge -----------
        self.next_section("trace")
        t = ValueTracker(0)
        bille.add_updater(lambda m: m.move_to([x_ecran, y_ecran(x_de_t(t.get_value())), 0]))
        courbe = always_redraw(lambda: ax.plot(x_de_t, x_range=[0, max(t.get_value(), 1e-3)],
                                                color=C_POS, stroke_width=5))
        point = always_redraw(lambda: Dot(ax.c2p(t.get_value(), x_de_t(t.get_value())),
                                          color=C_POS, radius=0.09))
        lien = always_redraw(lambda: DashedLine(bille.get_center(), point.get_center(),
                                                color=C_GRIS, stroke_width=2,
                                                dash_length=0.08))
        horloge = VGroup(M("t =", size=34), DecimalFR(0, num_decimal_places=1, font_size=34),
                         M(r"\mathrm{s}", size=34)).arrange(RIGHT, buff=0.12)
        horloge.to_corner(UR, buff=0.6)
        horloge[1].add_updater(lambda d: d.set_value(t.get_value()))
        self.add(courbe, point, lien)
        self.play(FadeIn(horloge))
        self.play(t.animate.set_value(6), run_time=6, rate_func=linear)
        self.wait()
        lecture = T("Chaque point de la courbe =\n« à l'instant t, la particule\nest en x »",
                    size=24, color=C_TEXTE).move_to(RIGHT * 4.7 + DOWN * 0.4)
        self.play(FadeIn(lecture))
        self.wait(3)
        self.play(FadeOut(lecture), FadeOut(horloge))
        bille.clear_updaters()
        self.remove(courbe, point, lien)
        self.add(ax.plot(x_de_t, x_range=[0, 6], color=C_POS, stroke_width=5))

        # --- 3. La sécante : vitesse moyenne ---------------------------------
        self.next_section("secante")
        ti = 1.0
        tf = ValueTracker(4.0)

        def P(tt):
            return ax.c2p(tt, x_de_t(tt))

        def pente():
            return (x_de_t(tf.get_value()) - x_de_t(ti)) / (tf.get_value() - ti)

        pi_dot = Dot(P(ti), color=ACCENT)
        pf_dot = always_redraw(lambda: Dot(P(tf.get_value()), color=ACCENT))
        coin = lambda: ax.c2p(tf.get_value(), x_de_t(ti))
        dt_ligne = always_redraw(lambda: DashedLine(P(ti), coin(), color=C_GRIS))
        dx_ligne = always_redraw(lambda: Line(coin(), P(tf.get_value()), color=C_POS,
                                              stroke_width=5))
        dt_lab = always_redraw(lambda: M(r"\Delta t", size=30, color=C_GRIS)
                               .next_to(dt_ligne, DOWN, buff=0.1))
        dx_lab = always_redraw(lambda: M(r"\Delta x", size=30, color=C_POS)
                               .next_to(dx_ligne, RIGHT, buff=0.1))

        def secante():
            a, b = np.array(P(ti)), np.array(P(tf.get_value()))
            d = (b - a) / np.linalg.norm(b - a)
            return Line(a - d * 0.8, b + d * 0.8, color=C_VIT, stroke_width=4)

        sec = always_redraw(secante)
        lab_ti = M("t_i", size=28, color=ACCENT).next_to(ax.c2p(ti, 0), DOWN, buff=0.45)
        lab_tf = always_redraw(lambda: M("t_f", size=28, color=ACCENT)
                               .next_to(ax.c2p(tf.get_value(), 0), DOWN, buff=0.45))
        self.play(FadeIn(pi_dot), FadeIn(pf_dot), FadeIn(lab_ti), FadeIn(lab_tf))
        self.play(Create(dt_ligne), Create(dx_ligne), FadeIn(dt_lab), FadeIn(dx_lab))
        self.play(Create(sec))

        formule = M(r"v_{x\,\mathrm{moy}} = \frac{\Delta x}{\Delta t}", size=42, color=C_VIT)
        egal = T("= pente de la sécante", size=26, color=C_VIT)
        valeur = VGroup(M(r"\approx", size=40), DecimalFR(pente(), num_decimal_places=2,
                                                           font_size=40, color=C_VIT),
                        M(r"\mathrm{m/s}", size=36)).arrange(RIGHT, buff=0.12)
        valeur[1].add_updater(lambda d: d.set_value(pente()))
        bloc = VGroup(formule, egal, valeur).arrange(DOWN, buff=0.3)
        bloc.move_to(RIGHT * 4.7 + UP * 1.3)
        self.play(Write(formule))
        self.play(FadeIn(egal), FadeIn(valeur))
        self.wait(2)
        msg = T("Autre intervalle →\nautre vitesse moyenne", size=22, color=C_GRIS)
        msg.next_to(bloc, DOWN, buff=0.5)
        self.play(FadeIn(msg))
        for v in (5.6, 2.2, 4.0):
            self.play(tf.animate.set_value(v), run_time=2.2)
            self.wait(0.8)
        self.play(FadeOut(msg))

        # --- 4. Rappel de maths : la pente -----------------------------------
        self.next_section("rappel-pente")
        rappel = VGroup(
            T("Rappel de maths", size=24, color=ACCENT, weight=BOLD),
            M(r"y = m\,x + b", size=36),
            M(r"m = \frac{y_2 - y_1}{x_2 - x_1} = \frac{\Delta y}{\Delta x} = \tan\alpha",
              size=32),
            T("ici : y → x  et  x → t", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.22)
        rappel = encadre(rappel, color=C_GRIS)
        limiter(rappel, 4.0)
        rappel.move_to(RIGHT * 4.85 + DOWN * 2.0)
        a0, a1 = np.array(P(ti)), np.array(P(tf.get_value()))
        alpha = Angle(Line(a0, a0 + RIGHT), Line(a0, a1), radius=0.6, color=ACCENT)
        alpha_lab = M(r"\alpha", size=30, color=ACCENT).next_to(alpha, RIGHT, buff=0.08)
        self.play(FadeIn(rappel), Create(alpha), FadeIn(alpha_lab))
        self.wait(4)
        vider(self)
