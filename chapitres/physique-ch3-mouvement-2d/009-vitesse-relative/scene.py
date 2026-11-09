"""3.7 — Vitesse relative : un homme H traverse un train T qui roule par rapport au sol S (vue de dessus).

- Dans le train : il marche tout droit (axe y_T).
- Depuis le sol : il avance en diagonale.
- v_HS = v_HT + v_TS ; tan θ = v_HT / v_TS ; et v_AB = −v_BA.
(Valeurs choisies pour que le dessin soit lisible : v_TS = 2 × v_HT.)

    manim -pql chapitres/physique-ch3-mouvement-2d/009-vitesse-relative/scene.py VitesseRelative
"""

from shared.physique import *

V_TS, V_HT = 1.2, 0.6
DUREE = 3.3
X_T0 = -2.0
Y_TRAIN = -0.7
L_TRAIN, H_TRAIN = 6.0, 2.4


class VitesseRelative(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.7", "La vitesse relative",
                    "Une vitesse se mesure toujours PAR RAPPORT à quelque chose")

        # --- 0. Les positions s'additionnent ------------------------------------------------
        self.next_section("positions")
        titre = bandeau("D'abord les positions")
        self.play(FadeIn(titre))
        A = np.array([-4.5, -2.2, 0])
        B = np.array([-1.0, -1.4, 0])
        P = np.array([-2.3, 1.6, 0])
        dots = VGroup(Dot(A, color=C_GRIS), Dot(B, color=C_GRIS), Dot(P, color=ACCENT))
        noms = VGroup(T("A", size=26, color=C_GRIS).next_to(A, DL, buff=0.1),
                      T("B", size=26, color=C_GRIS).next_to(B, DR, buff=0.1),
                      T("P", size=26, color=ACCENT).next_to(P, UP, buff=0.1))
        rpa = fleche(A, P, C_POS)
        rbp = fleche(B, P, C_VIT)
        rba = fleche(A, B, ACCENT)
        l1 = M(r"\vec r_{PA}", size=30, color=C_POS).next_to((A + P) / 2, LEFT, buff=0.15)
        l2 = M(r"\vec r_{PB}", size=30, color=C_VIT).next_to((B + P) / 2, RIGHT, buff=0.15)
        l3 = M(r"\vec r_{BA}", size=30, color=ACCENT).next_to((A + B) / 2, DOWN, buff=0.15)
        self.play(FadeIn(dots), FadeIn(noms))
        self.play(GrowArrow(rpa), FadeIn(l1))
        self.play(GrowArrow(rba), FadeIn(l3))
        self.play(GrowArrow(rbp), FadeIn(l2))
        lecture = VGroup(
            T("lecture des indices :", size=22, color=C_GRIS),
            M(r"\vec r_{PA} = \text{position de } P \text{ par rapport à } A", size=30),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(RIGHT * 3.6 + UP * 1.8)
        rel = encadre(M(r"\vec r_{PA} = \vec r_{PB} + \vec r_{BA}", size=42))
        rel.move_to(RIGHT * 3.6 + UP * 0.1)
        derive = VGroup(T("on dérive par rapport au temps :", size=22, color=C_GRIS),
                        M(r"\vec v_{PA} = \vec v_{PB} + \vec v_{BA}", size=42, color=C_VIT),
                        M("(3.18)", size=22, color=C_GRIS)).arrange(DOWN, buff=0.15)
        derive.move_to(RIGHT * 3.6 + DOWN * 2.0)
        limiter(lecture, 6.4)
        self.play(FadeIn(lecture))
        self.play(FadeIn(rel))
        self.wait(1)
        self.play(FadeIn(derive))
        self.wait(4)
        vider(self)

        # --- 1. Le train vu de dessus -----------------------------------------------------------
        t = ValueTracker(0)
        vue = ValueTracker(1)  # 1 = vu depuis le train, 0 = vu depuis le sol

        def x_train():
            return X_T0 + V_TS * t.get_value()

        def ecran_x(xm):
            return xm - vue.get_value() * x_train()

        def sol():
            g = VGroup()
            for xm in np.arange(-24, 24, 0.8):
                xs = ecran_x(xm)
                if -7.3 < xs < 7.3:
                    for ym in np.arange(-3.6, 2.6, 0.8):
                        g.add(Dot([xs, ym, 0], radius=0.025, color=C_GRIS))
            return g

        def train():
            xs = ecran_x(x_train())
            r = Rectangle(width=L_TRAIN, height=H_TRAIN, color=C_POS, fill_color=BACKGROUND,
                          fill_opacity=0.85, stroke_width=4).move_to([xs, Y_TRAIN, 0])
            ax_t = VGroup(fleche([xs - 2.7, Y_TRAIN - 1.0, 0], [xs - 1.9, Y_TRAIN - 1.0, 0], C_POS, width=3, tip=0.12),
                          fleche([xs - 2.7, Y_TRAIN - 1.0, 0], [xs - 2.7, Y_TRAIN - 0.2, 0], C_POS, width=3, tip=0.12))
            lab = VGroup(M("x_T", size=22, color=C_POS).next_to(ax_t[0], RIGHT, buff=0.05),
                         M("y_T", size=22, color=C_POS).next_to(ax_t[1], UP, buff=0.05))
            return VGroup(r, ax_t, lab)

        def pos_homme():
            return np.array([ecran_x(x_train()), Y_TRAIN - 1.0 + V_HT * t.get_value(), 0])

        g_sol = always_redraw(sol)
        g_train = always_redraw(train)
        homme = always_redraw(lambda: Dot(pos_homme(), radius=0.14, color=ACCENT).set_z_index(4))
        etiquette = always_redraw(lambda: T(
            "Vu depuis le TRAIN" if vue.get_value() > 0.5 else "Vu depuis le SOL",
            size=26, color=ACCENT).move_to(RIGHT * 4.4 + UP * 2.55))

        self.next_section("vu-train")
        titre = bandeau("Un homme traverse le wagon d'un train qui roule", "vue de dessus")
        self.play(FadeIn(titre), FadeIn(g_sol), FadeIn(g_train), FadeIn(homme), FadeIn(etiquette))
        fl_sol = VGroup(fleche([5.6, 1.3, 0], [4.4, 1.3, 0], C_GRIS),
                        M(r"\vec v_{ST} = -\vec v_{TS}", size=28, color=C_GRIS).move_to([5.0, 1.75, 0]))
        self.play(FadeIn(fl_sol))
        trace1 = TracedPath(homme.get_center, stroke_color=ACCENT, stroke_width=4)
        self.add(trace1)
        self.play(t.animate.set_value(DUREE), run_time=DUREE * 1.3, rate_func=linear)
        fv_ht = fleche(pos_homme() + RIGHT * 0.5 + DOWN * 1.6, pos_homme() + RIGHT * 0.5 + DOWN * 1.6 + UP * 1.2, C_VIT)
        l_ht = M(r"\vec v_{HT}", size=30, color=C_VIT).next_to(fv_ht, RIGHT, buff=0.1)
        msg1 = T("dans le train : il marche tout droit, selon y_T", size=22, color=C_TEXTE)
        msg1.move_to(DOWN * 3.4)
        self.play(GrowArrow(fv_ht), FadeIn(l_ht), FadeIn(msg1))
        self.wait(3)
        self.play(FadeOut(VGroup(fv_ht, l_ht, msg1, fl_sol, trace1)))
        self.remove(trace1)

        # --- 2. Vu depuis le sol ---------------------------------------------------------------------
        self.next_section("vu-sol")
        self.play(t.animate.set_value(0), run_time=0.5)
        self.play(vue.animate.set_value(0), run_time=1.2)
        trace2 = TracedPath(homme.get_center, stroke_color=ACCENT, stroke_width=4)
        self.add(trace2)
        self.play(t.animate.set_value(DUREE), run_time=DUREE * 1.3, rate_func=linear)
        msg2 = T("depuis le sol : il avance en diagonale", size=22, color=C_TEXTE).move_to(DOWN * 3.4)
        self.play(FadeIn(msg2))
        self.wait(3)

        # --- 3. Le triangle des vitesses -----------------------------------------------------------
        self.next_section("triangle")
        trace_fixe = trace2.copy().clear_updaters()
        self.add(trace_fixe)
        self.remove(trace2)
        self.play(FadeOut(VGroup(g_sol, g_train, homme, msg2, etiquette)))
        titre3 = bandeau("Le triangle des vitesses")
        self.play(Transform(titre, titre3), FadeOut(trace_fixe))
        o = np.array([-5.0, -2.6, 0])
        k = 3.6
        f_ts = fleche(o, o + k * V_TS * RIGHT, C_POS, width=7)
        f_ht = fleche(o + k * V_TS * RIGHT, o + k * (V_TS * RIGHT + V_HT * UP), C_VIT, width=7)
        f_hs = fleche(o, o + k * (V_TS * RIGHT + V_HT * UP), ACCENT, width=8)
        l_ts = M(r"\vec v_{TS}", size=32, color=C_POS).next_to(f_ts, DOWN, buff=0.12)
        l_ht = M(r"\vec v_{HT}", size=32, color=C_VIT).next_to(f_ht, RIGHT, buff=0.12)
        l_hs = M(r"\vec v_{HS}", size=32, color=ACCENT).next_to(f_hs.get_center(), UL, buff=0.15)
        th = Angle(Line(o, o + RIGHT), Line(o, f_hs.get_end()), radius=0.9, color=C_TEXTE)
        lth = M(r"\theta", size=30).move_to(o + 1.25 * np.array([np.cos(0.23), np.sin(0.23), 0]))
        self.play(GrowArrow(f_ts), FadeIn(l_ts))
        self.play(GrowArrow(f_ht), FadeIn(l_ht))
        self.play(GrowArrow(f_hs), FadeIn(l_hs), Create(th), FadeIn(lth))
        formules = VGroup(
            M(r"\vec v_{HS} = \vec v_{HT} + \vec v_{TS}", size=40, color=ACCENT),
            M(r"\tan\theta = \frac{v_{HT}}{v_{TS}}", size=40),
            T("homme / sol = homme / train + train / sol", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.8 + UP * 1.4)
        for f in formules:
            self.play(FadeIn(f, shift=UP * 0.1))
            self.wait(0.8)
        astuce = encadre(VGroup(
            T("Astuce : les indices s'enchaînent", size=24, color=ACCENT),
            T("H/T  +  T/S  =  H/S", size=26),
            T("inverser les indices change le signe :", size=22, color=C_GRIS),
            M(r"\vec v_{AB} = -\vec v_{BA}", size=36),
        ).arrange(DOWN, buff=0.18))
        limiter(astuce, 5.6).move_to(RIGHT * 3.9 + DOWN * 1.9)
        self.play(FadeIn(astuce))
        self.wait(5)
        vider(self)
