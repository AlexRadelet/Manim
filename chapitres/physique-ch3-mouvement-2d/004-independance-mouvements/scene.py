"""3.3 — Mouvement d'un projectile : horizontal et vertical sont INDÉPENDANTS.

1. Deux billes : l'une lâchée, l'autre lancée horizontalement -> elles touchent le sol en même temps.
2. Le bateau de Galilée : une boule lâchée du haut du mât tombe au pied du mât.
3. Les équations du projectile (3.10)-(3.13).

    manim -pql chapitres/physique-ch3-mouvement-2d/004-independance-mouvements/scene.py IndependanceMouvements
"""

from shared.physique import *

Y_HAUT, Y_SOL = 1.6, -3.0
T_CHUTE = 2.2
G_E = 2 * (Y_HAUT - Y_SOL) / T_CHUTE ** 2  # « g » à l'échelle de l'écran
V0_E = 4.3


class IndependanceMouvements(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.3", "Le mouvement d'un projectile",
                    "Deux mouvements qui s'ignorent complètement")

        # --- 1. Les deux billes ---------------------------------------------------------
        self.next_section("deux-billes")
        titre = bandeau("Une bille lâchée, une bille lancée horizontalement",
                        "au même instant, de la même hauteur")
        self.play(FadeIn(titre))
        sol = Line([-6.8, Y_SOL, 0], [6.8, Y_SOL, 0], color=C_SOL, stroke_width=6)
        table = Rectangle(width=1.0, height=0.15, color=C_GRIS, fill_opacity=0.6, stroke_width=0)
        table.move_to([-5.35, Y_HAUT - 0.2, 0])
        xa0, xb0 = -5.6, -5.1
        t = ValueTracker(0)

        def ya(tt):
            return Y_HAUT - 0.5 * G_E * tt * tt

        def xb(tt):
            return xb0 + V0_E * tt

        ba = always_redraw(lambda: Dot([xa0, ya(t.get_value()), 0], radius=0.13, color=C_POS))
        bb = always_redraw(lambda: Dot([xb(t.get_value()), ya(t.get_value()), 0], radius=0.13,
                                       color=ACCENT))
        la = T("lâchée", size=20, color=C_POS).next_to([xa0, Y_HAUT, 0], LEFT, buff=0.25).shift(UP * 0.3)
        lb = T("lancée →", size=20, color=ACCENT).next_to([xb0, Y_HAUT, 0], UP, buff=0.25).shift(RIGHT * 0.3)
        self.play(Create(sol), FadeIn(table), FadeIn(ba), FadeIn(bb), FadeIn(la), FadeIn(lb))
        self.wait()
        self.play(t.animate.set_value(T_CHUTE), run_time=T_CHUTE * 1.4, rate_func=linear)
        meme = T("Elles touchent le sol EN MÊME TEMPS", size=28, color=ACCENT).move_to(UP * 0.6 + RIGHT * 2.5)
        self.play(FadeIn(meme))
        self.wait(2)

        # images stroboscopiques
        self.next_section("strobo")
        self.play(FadeOut(meme), t.animate.set_value(0), run_time=0.6)
        n = 10
        instants = [k * T_CHUTE / n for k in range(n + 1)]
        sa = VGroup(*[Dot([xa0, ya(s), 0], radius=0.1, color=C_POS).set_opacity(0.55) for s in instants])
        sb = VGroup(*[Dot([xb(s), ya(s), 0], radius=0.1, color=ACCENT).set_opacity(0.55) for s in instants])
        self.play(LaggedStart(*[AnimationGroup(FadeIn(a), FadeIn(b)) for a, b in zip(sa, sb)],
                              lag_ratio=0.3), t.animate.set_value(T_CHUTE), run_time=T_CHUTE * 1.4)
        horiz = VGroup(*[DashedLine([xa0, ya(s), 0], [xb(s), ya(s), 0], color=C_GRIS,
                                    stroke_width=1.5, dash_length=0.08) for s in instants[1:]])
        self.play(Create(horiz), run_time=1.5)
        txt_v = VGroup(T("Verticalement : à chaque instant,", size=22),
                       T("la même hauteur → même MRUA (chute libre)", size=22, color=C_POS)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 3.4 + UP * 2.0)
        self.play(FadeIn(txt_v))
        self.wait(2)
        ombre = VGroup(*[Dot([xb(s), Y_SOL, 0], radius=0.08, color=ACCENT) for s in instants])
        vert = VGroup(*[DashedLine([xb(s), ya(s), 0], [xb(s), Y_SOL, 0], color=ACCENT,
                                   stroke_width=1.5, dash_length=0.08).set_opacity(0.6)
                        for s in instants])
        self.play(Create(vert), FadeIn(ombre), run_time=1.5)
        txt_h = VGroup(T("Horizontalement : des écarts tous égaux", size=22),
                       T("→ MRU, v_x constante", size=22, color=ACCENT)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(txt_v, DOWN, buff=0.35, aligned_edge=LEFT)
        accol = BraceBetweenPoints([xb(instants[3]), Y_SOL, 0], [xb(instants[4]), Y_SOL, 0],
                                   direction=DOWN, color=ACCENT)
        self.play(FadeIn(txt_h), GrowFromCenter(accol))
        self.wait(2)
        cle = encadre(T("Un projectile = un MRU horizontal + un MRUA vertical,\n"
                        "qui se font en même temps sans se gêner.", size=24))
        cle.move_to(RIGHT * 3.0 + UP * 2.0)
        self.play(FadeOut(txt_v), FadeOut(txt_h), FadeIn(cle))
        self.wait(4)
        vider(self)

        # --- 2. Le bateau de Galilée ---------------------------------------------------
        self.next_section("bateau")
        titre = bandeau("Le bateau de Galilée", "une boule tombe du haut du mât d'un bateau qui avance")
        self.play(FadeIn(titre))
        mer = Rectangle(width=14.5, height=0.9, color=PRIMARY, fill_opacity=0.25, stroke_width=0)
        mer.move_to([0, -3.4, 0])
        y_pont = -2.6
        H_MAT = 4.6
        u = 1.7
        T_B = np.sqrt(2 * H_MAT / G_E)

        def bateau():
            coque = Polygon([-1.4, 0, 0], [1.4, 0, 0], [1.0, -0.6, 0], [-1.0, -0.6, 0],
                            color=C_SOL, fill_opacity=1, stroke_width=0)
            mat = Line([0, 0, 0], [0, H_MAT, 0], color=C_TEXTE, stroke_width=4)
            voile = Polygon([0.05, H_MAT - 0.2, 0], [0.05, 0.6, 0], [1.3, 0.6, 0],
                            color=C_TEXTE, fill_opacity=0.15, stroke_width=2)
            return VGroup(coque, voile, mat)

        tb = ValueTracker(0)
        x_b0 = -5.0
        b = bateau()
        b.add_updater(lambda m: m.move_to([x_b0 + u * tb.get_value(), y_pont + (H_MAT - 0.6) / 2, 0]))

        def pos_boule():
            tt = min(tb.get_value(), T_B)
            return np.array([x_b0 + u * tt, y_pont + H_MAT - 0.5 * G_E * tt * tt, 0])

        boule = always_redraw(lambda: Dot(pos_boule(), radius=0.13, color=ACCENT).set_z_index(3))
        self.play(FadeIn(mer), FadeIn(b), FadeIn(boule))
        question = T("Le bateau avance à vitesse constante.\nOù la boule va-t-elle tomber ?",
                     size=24, color=ACCENT)
        limiter(question, 5.4).move_to(RIGHT * 3.9 + UP * 1.8)
        self.play(FadeIn(question))
        intuition = DashedLine([x_b0, y_pont + H_MAT, 0], [x_b0, y_pont, 0], color=C_NEG)
        l_int = T("intuition : « elle tombe\nderrière, ici » ?", size=20, color=C_NEG)
        l_int.next_to(intuition, UP, buff=0.15).shift(RIGHT * 0.6)
        self.play(Create(intuition), FadeIn(l_int))
        self.wait(2)
        trace = TracedPath(boule.get_center, stroke_color=ACCENT, stroke_width=3)
        self.add(trace)
        self.play(tb.animate.set_value(T_B), run_time=T_B * 1.5, rate_func=linear)
        pied = T("…au pied du mât !", size=28, color=C_VIT).move_to(RIGHT * 3.9 + UP * 0.7)
        self.play(FadeIn(pied))
        self.wait(1)
        expl = T("Au moment où on la lâche, la boule a déjà\nla vitesse horizontale du bateau,"
                 " et la garde\n(inertie). Bateau et boule avancent ensemble.", size=22)
        limiter(expl, 5.6)
        expl.move_to(RIGHT * 3.9 + DOWN * 0.4)
        self.play(FadeIn(expl))
        vu = T("Vue depuis le quai, la trajectoire est une parabole ;\n"
               "vue depuis le bateau, la boule tombe tout droit.", size=20, color=C_GRIS)
        limiter(vu, 5.6)
        vu.move_to(RIGHT * 3.9 + DOWN * 1.8)
        self.play(FadeIn(vu))
        b.clear_updaters()
        self.wait(5)
        vider(self)

        # --- 3. Les équations -----------------------------------------------------------------
        self.next_section("equations")
        titre = bandeau("Les équations du projectile",
                        "axe x horizontal, axe y vertical vers le haut, x₀ = 0")
        self.play(FadeIn(titre))
        acc = M(r"a_x = 0 \qquad a_y = -g", size=44, color=C_ACC).move_to(UP * 2.0)
        self.play(Write(acc))
        gauche = VGroup(T("horizontal : MRU", size=24, color=ACCENT),
                        M(r"x = v_{x0}\,t", size=38),
                        M(r"(3.10)", size=22, color=C_GRIS)).arrange(DOWN, buff=0.25)
        droite = VGroup(T("vertical : MRUA (chute libre)", size=24, color=C_POS),
                        M(r"v_y = v_{y0} - g t", size=36),
                        M(r"y = y_0 + v_{y0} t - \tfrac12 g t^2", size=36),
                        M(r"v_y^2 = v_{y0}^2 - 2g(y - y_0)", size=36),
                        M(r"(3.11)\ \text{à}\ (3.13)", size=22, color=C_GRIS)).arrange(DOWN, buff=0.22)
        VGroup(gauche, droite).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to(DOWN * 0.4)
        sep = DashedLine(UP * 1.2, DOWN * 2.3, color=C_GRIS).move_to(
            (gauche.get_right() + droite.get_left()) / 2 * np.array([1, 0, 0]) + DOWN * 0.5)
        self.play(FadeIn(gauche), Create(sep))
        self.play(FadeIn(droite))
        lien = T("Le seul lien entre les deux colonnes : le temps t.", size=24, color=ACCENT)
        lien.to_edge(DOWN, buff=0.75)
        nb = T("Valable si on néglige l'air, la rotation du projectile, la courbure et la rotation de la Terre.",
               size=18, color=C_GRIS).to_edge(DOWN, buff=0.25)
        limiter(nb, 13)
        self.play(FadeIn(lien))
        self.play(FadeIn(nb))
        self.wait(5)
        vider(self)
