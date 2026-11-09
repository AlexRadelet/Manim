"""4.1 — La force : interaction, forces usuelles, caractère vectoriel, loi de Hooke.

    python -m manim -pql chapitres/physique-ch4-dynamique-1/001-force-et-hooke/scene.py ForceEtHooke
"""

from shared.physique import *


class ForceEtHooke(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 4 · section 4.1", "La force",
                    "Cinématique : COMMENT ça bouge.  Dynamique : POURQUOI.")

        # --- 1. Les forces usuelles --------------------------------------------------
        self.next_section("forces-usuelles")
        titre = bandeau("Les forces qu'on rencontrera tout le temps",
                        "une force = une action d'un objet SUR un autre objet")
        self.play(FadeIn(titre))
        table = Line(LEFT * 6.5, RIGHT * 1.0, color=C_SOL, stroke_width=8).shift(DOWN * 1.3)
        b = bloc("m", 2.0, 1.4, size=40).next_to(table, UP, buff=0).shift(LEFT * 1.0)
        c = b.get_center()
        corde = Line(b.get_right(), b.get_right() + RIGHT * 1.5, color=C_TEXTE, stroke_width=3)
        main = Dot(corde.get_end(), radius=0.09, color=C_TEXTE)
        self.play(Create(table), FadeIn(b))
        self.play(Create(corde), FadeIn(main))
        forces = [
            (force(c, DOWN * 2.0, r"\vec P", direction=LEFT), "poids : la Terre attire (à distance)"),
            (force(c, UP * 2.0, r"\vec N", direction=LEFT), "normale : la table soutient"),
            (force(b.get_right() + UP * 0.25, RIGHT * 1.2, r"\vec T", direction=UP), "tension : la corde tire"),
            (force(b.get_corner(DL) + UP * 0.1, LEFT * 1.3, r"\vec f", direction=UP), "frottement : freine le glissement"),
        ]
        legende = VGroup()
        for k, (fo, txt) in enumerate(forces):
            l = VGroup(M(fo[1].get_tex_string(), size=34, color=C_FORCE), T(txt, size=24)).arrange(RIGHT, buff=0.25)
            legende.add(l)
        legende.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        limiter(legende, 5.4).move_to(RIGHT * 4.2 + UP * 0.8)
        for (fo, _), l in zip(forces, legende):
            self.play(GrowArrow(fo[0]), FadeIn(fo[1]), FadeIn(l), run_time=0.9)
            self.wait(0.6)
        res = VGroup(M(r"\vec F_{res}", size=34, color=C_FORCE),
                     T("ressort : tire ou pousse", size=24)
                     ).arrange(RIGHT, buff=0.25).next_to(legende, DOWN, buff=0.28, aligned_edge=LEFT)
        limiter(res, 5.4)
        self.play(FadeIn(res))
        cle = T("On ne voit jamais une force, seulement ses effets :\n"
                "elle change une vitesse, équilibre d'autres forces, ou déforme.",
                size=22, color=ACCENT).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cle))
        self.wait(4)
        vider(self)

        # --- 2. Une force est un vecteur ------------------------------------------------
        self.next_section("vecteur")
        titre = bandeau("Une force est un vecteur", "grandeur + direction + sens, et les forces s'additionnent comme des vecteurs")
        self.play(FadeIn(titre))
        O = LEFT * 5.0 + DOWN * 1.2
        pt = particule().move_to(O)
        F1 = np.array([2.8, 0.4, 0])
        F2 = np.array([0.6, 2.2, 0])
        f1 = force(O, F1, r"\vec F_1", direction=DOWN)
        f2 = force(O, F2, r"\vec F_2", direction=LEFT)
        self.play(FadeIn(pt), GrowArrow(f1[0]), FadeIn(f1[1]))
        self.play(GrowArrow(f2[0]), FadeIn(f2[1]))
        p1 = DashedLine(O + F1, O + F1 + F2, color=C_GRIS)
        p2 = DashedLine(O + F2, O + F1 + F2, color=C_GRIS)
        self.play(Create(p1), Create(p2))
        R = force(O, F1 + F2, r"\sum\vec F", color=ACCENT, direction=UR, width=8)
        self.play(GrowArrow(R[0]), FadeIn(R[1]))
        txt = VGroup(
            M(r"\sum\vec F = \vec F_1 + \vec F_2", size=40, color=ACCENT),
            T("règle du parallélogramme", size=22, color=C_GRIS),
            T("deux forces de 3 N et 2 N ne donnent PAS\nforcément 5 N : ça dépend de leurs directions",
              size=22),
        ).arrange(DOWN, buff=0.3)
        limiter(txt, 5.6).move_to(RIGHT * 3.7 + UP * 0.3)
        for t in txt:
            self.play(FadeIn(t, shift=UP * 0.1))
            self.wait(0.8)
        self.wait(3)
        vider(self)

        # --- 3. Loi de Hooke -------------------------------------------------------------
        self.next_section("hooke")
        titre = bandeau("Mesurer une force : le ressort (dynamomètre)", "loi de Hooke")
        self.play(FadeIn(titre))
        mur = Rectangle(width=0.3, height=2.2, color=C_GRIS, fill_opacity=0.6, stroke_width=0)
        mur.move_to(LEFT * 6.3 + UP * 0.3)
        x0 = -6.15
        L0 = 2.6
        k = 1.0  # unités écran par unité de force (pour le dessin)
        dl = ValueTracker(0)
        y = 0.3
        spring = always_redraw(lambda: ressort([x0, y, 0], [x0 + L0 + dl.get_value(), y, 0], spires=9))
        poignee = always_redraw(lambda: Dot([x0 + L0 + dl.get_value(), y, 0], radius=0.1, color=C_TEXTE))
        f_app = always_redraw(lambda: fleche([x0 + L0 + dl.get_value(), y, 0],
                                             [x0 + L0 + dl.get_value() + max(0.9 * dl.get_value(), 1e-3), y, 0],
                                             C_FORCE))
        repere = DashedLine([x0 + L0, y - 0.8, 0], [x0 + L0, y + 0.8, 0], color=C_GRIS)
        lab0 = T("repos", size=18, color=C_GRIS).next_to(repere, DOWN, buff=0.05)
        bdl = always_redraw(lambda: BraceBetweenPoints([x0 + L0, y - 0.45, 0],
                                                       [x0 + L0 + max(dl.get_value(), 1e-3), y - 0.45, 0],
                                                       direction=DOWN, color=ACCENT)
                            if dl.get_value() > 0.15 else VGroup())
        ldl = always_redraw(lambda: M(r"\Delta l", size=28, color=ACCENT).next_to(bdl, DOWN, buff=0.05)
                            if dl.get_value() > 0.15 else VGroup())
        self.play(FadeIn(mur), Create(spring), FadeIn(poignee), Create(repere), FadeIn(lab0))
        self.add(f_app, bdl, ldl)
        ax = Axes(x_range=[0, 2.2, 0.5], y_range=[0, 2.2, 0.5], x_length=4, y_length=3.2,
                  axis_config={"color": C_GRIS}, tips=False).move_to(RIGHT * 4.3 + DOWN * 0.4)
        lx = M(r"\Delta l", size=28, color=ACCENT).next_to(ax.x_axis, RIGHT, buff=0.1)
        ly = M(r"F_{res}", size=28, color=C_FORCE).next_to(ax.y_axis, UP, buff=0.1)
        trace = always_redraw(lambda: ax.plot(lambda x: x, x_range=[0, max(dl.get_value(), 1e-3)],
                                              color=C_FORCE, stroke_width=4))
        pt = always_redraw(lambda: Dot(ax.c2p(dl.get_value(), dl.get_value()), color=ACCENT, radius=0.07))
        self.play(Create(ax), FadeIn(lx), FadeIn(ly))
        self.add(trace, pt)
        self.play(dl.animate.set_value(1.0), run_time=2)
        self.wait(0.5)
        self.play(dl.animate.set_value(2.0), run_time=2)
        double = T("2 fois plus étiré → force 2 fois plus grande", size=22, color=ACCENT)
        limiter(double, 4.6).next_to(ax, UP, buff=0.4)
        self.play(FadeIn(double))
        self.wait(1)
        loi = encadre(VGroup(M(r"F_{res} = k\,\Delta l", size=44, color=C_FORCE),
                             T("k = constante de rappel (raideur), en N/m", size=20, color=C_GRIS)
                             ).arrange(DOWN, buff=0.15))
        loi.move_to(LEFT * 3.2 + DOWN * 2.2)
        self.play(FadeIn(loi))
        ideal = T("ressort idéal : masse négligeable, toujours proportionnel", size=20, color=C_GRIS)
        limiter(ideal, 6.0).next_to(loi, DOWN, buff=0.2)
        self.play(FadeIn(ideal))
        self.wait(4)
        vider(self)
