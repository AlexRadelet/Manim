"""3.8 — La transformation de Galilée.

1. S' se déplace à vitesse u par rapport à S : r' = r − u t, d'où v' = v − u et a' = a.
2. Écran partagé : une balle lâchée dans une voiture qui roule.
   Dans la voiture : chute verticale. Depuis la route : parabole. MÊME accélération dans les deux.
   -> aucune expérience ne dit qui est « vraiment » au repos.

    manim -pql chapitres/physique-ch3-mouvement-2d/010-transformation-galilee/scene.py TransformationGalilee
"""

from shared.physique import *


class TransformationGalilee(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.8", "La transformation de Galilée",
                    "Passer d'un référentiel d'inertie à un autre")

        # --- 1. r' = r − u t ------------------------------------------------------------------
        self.next_section("r-prime")
        titre = bandeau("S' glisse à vitesse u par rapport à S", "les origines coïncident à t = 0")
        self.play(FadeIn(titre))
        O = np.array([-5.6, -2.6, 0])
        u = 0.9
        t = ValueTracker(0)

        def axes(o, couleur, prime):
            ax = VGroup(fleche(o, o + RIGHT * 2.0, couleur, width=4, tip=0.16),
                        fleche(o, o + UP * 2.0, couleur, width=4, tip=0.16))
            s = "'" if prime else ""
            lab = VGroup(M(f"x{s}", size=28, color=couleur).next_to(ax[0], DOWN, buff=0.08).align_to(ax[0], RIGHT),
                         M(f"y{s}", size=28, color=couleur).next_to(ax[1], LEFT, buff=0.08).align_to(ax[1], UP),
                         M(f"O{s}", size=28, color=couleur).next_to(o, DL if not prime else DR, buff=0.06))
            return VGroup(ax, lab)

        S = axes(O, C_GRIS, False)
        lS = T("S", size=30, color=C_GRIS, weight=BOLD).next_to(O + UP * 2.0, UP, buff=0.4)
        Op = lambda: O + RIGHT * u * t.get_value()
        Sp = always_redraw(lambda: axes(Op(), C_VIT, True))
        lSp = always_redraw(lambda: T("S'", size=30, color=C_VIT, weight=BOLD)
                            .next_to(Op() + UP * 2.0, UP, buff=0.4).shift(RIGHT * 0.3))
        P = np.array([0.2, 1.6, 0])
        pP = Dot(P, color=ACCENT, radius=0.1)
        lP = T("P", size=26, color=ACCENT).next_to(P, UR, buff=0.08)
        self.play(FadeIn(S), FadeIn(lS), FadeIn(Sp), FadeIn(lSp), FadeIn(pP), FadeIn(lP))
        fu = always_redraw(lambda: fleche(Op() + UP * 2.5, Op() + UP * 2.5 + RIGHT * 1.0, C_VIT, width=4, tip=0.15))
        lu = always_redraw(lambda: M(r"\vec u", size=28, color=C_VIT).next_to(fu, UP, buff=0.05))
        self.play(FadeIn(fu), FadeIn(lu))
        self.play(t.animate.set_value(3.2), run_time=3, rate_func=linear)
        r = fleche(O, P, C_POS, width=6)
        lr = M(r"\vec r", size=32, color=C_POS).next_to((O + P) / 2, UL, buff=0.08)
        rp = always_redraw(lambda: fleche(Op(), P, ACCENT, width=6))
        lrp = always_redraw(lambda: M(r"\vec r\,'", size=32, color=ACCENT).next_to((Op() + P) / 2, RIGHT, buff=0.1))
        ut = always_redraw(lambda: fleche(O, Op(), C_VIT, width=6))
        lut = always_redraw(lambda: M(r"\vec u\,t", size=30, color=C_VIT).next_to(ut, DOWN, buff=0.1))
        self.play(GrowArrow(r), FadeIn(lr))
        self.play(FadeIn(ut), FadeIn(lut))
        self.play(FadeIn(rp), FadeIn(lrp))
        col = RIGHT * 4.0
        f1 = encadre(VGroup(M(r"\vec r\,' = \vec r - \vec u\,t", size=40),
                            M("(3.19)", size=22, color=C_GRIS)).arrange(RIGHT, buff=0.3))
        f1.move_to(col + UP * 2.2)
        self.play(FadeIn(f1))
        self.play(t.animate.set_value(4.6), run_time=1.5, rate_func=linear)
        comp = VGroup(T("si x et x' sont sur la même droite et u = u i :", size=20, color=C_GRIS),
                      M(r"x' = x - ut \quad y' = y \quad z' = z \quad t' = t", size=32),
                      M("(3.20)", size=22, color=C_GRIS)).arrange(DOWN, buff=0.15)
        limiter(comp, 6.2).move_to(col + UP * 0.6)
        self.play(FadeIn(comp))
        self.wait(2)
        der = VGroup(T("on dérive :", size=22, color=C_GRIS),
                     M(r"\vec v\,' = \vec v - \vec u", size=38, color=C_VIT),
                     T("on dérive encore (u est constant) :", size=22, color=C_GRIS),
                     M(r"\vec a\,' = \vec a", size=42, color=C_ACC)).arrange(DOWN, buff=0.18)
        der.move_to(col + DOWN * 1.65)
        for d in der:
            self.play(FadeIn(d, shift=UP * 0.1))
            self.wait(0.6)
        nb = T("valable si les vitesses sont ≪ vitesse de la lumière", size=18, color=C_GRIS)
        nb.to_edge(DOWN, buff=0.15).set_x(4.0)
        self.play(FadeIn(nb))
        self.wait(4)
        vider(self)

        # --- 2. Écran partagé -------------------------------------------------------------------
        self.next_section("ecran-partage")
        titre = bandeau("Une balle lâchée dans une voiture qui roule à vitesse u")
        self.play(FadeIn(titre))
        sep = Line(UP * 3.1, DOWN * 3.9, color=C_GRIS, stroke_width=2)
        g_titre = T("Dans la voiture (S')", size=26, color=C_VIT).move_to([-3.55, 2.6, 0])
        d_titre = T("Depuis la route (S)", size=26, color=C_POS).move_to([3.55, 2.6, 0])
        self.play(Create(sep), FadeIn(g_titre), FadeIn(d_titre))

        Y_SOL, H = -2.7, 3.6
        T_CH = 1.7
        G_E = 2 * (H - 0.78) / T_CH ** 2  # 0,78 = hauteur du toit + rayon de la balle
        U = 1.9
        tt = ValueTracker(0)
        CX_G, X_D0 = -3.55, 1.0

        def voiture_lacher(cx):
            caisse = RoundedRectangle(width=1.8, height=0.45, corner_radius=0.08, color=C_POS,
                                      fill_opacity=0.9, stroke_width=0).move_to([cx, Y_SOL + 0.42, 0])
            roues = VGroup(*[Circle(radius=0.16, color=C_GRIS, fill_color=BACKGROUND, fill_opacity=1,
                                    stroke_width=3).move_to([cx + d, Y_SOL + 0.17, 0]) for d in (-0.55, 0.55)])
            perche = Line([cx, Y_SOL + 0.62, 0], [cx, Y_SOL + H, 0], color=C_TEXTE, stroke_width=3)
            main = Dot([cx, Y_SOL + H, 0], radius=0.06, color=C_TEXTE)
            return VGroup(perche, main, caisse, roues)

        def marques(decalage, xmin, xmax):
            g = VGroup()
            for xm in np.arange(-20, 20, 1.2):
                xs = xm - decalage
                if xmin < xs < xmax - 0.5:
                    g.add(Line([xs, Y_SOL - 0.25, 0], [xs + 0.5, Y_SOL - 0.25, 0], color=C_GRIS, stroke_width=3))
            return g

        def y_balle():  # tombe du haut de la perche jusque sur le toit de la voiture
            s = min(tt.get_value(), T_CH)
            return Y_SOL + H - 0.5 * G_E * s * s

        sol_g = Line([-7.1, Y_SOL, 0], [-0.1, Y_SOL, 0], color=C_SOL, stroke_width=5)
        sol_d = Line([0.1, Y_SOL, 0], [7.1, Y_SOL, 0], color=C_SOL, stroke_width=5)
        v_g = voiture_lacher(CX_G)
        v_d = always_redraw(lambda: voiture_lacher(X_D0 + U * tt.get_value()))
        m_g = always_redraw(lambda: marques(U * tt.get_value() - 3.5, -7.1, -0.1))
        m_d = marques(-3.5, 0.1, 7.1)
        b_g = always_redraw(lambda: Dot([CX_G, y_balle(), 0], radius=0.13, color=ACCENT).set_z_index(3))
        b_d = always_redraw(lambda: Dot([X_D0 + U * min(tt.get_value(), T_CH), y_balle(), 0], radius=0.13,
                                        color=ACCENT).set_z_index(3))
        a_g = always_redraw(lambda: fleche(b_g.get_center() + RIGHT * 0.3,
                                           b_g.get_center() + RIGHT * 0.3 + DOWN * 0.8, C_ACC, width=5, tip=0.16))
        a_d = always_redraw(lambda: fleche(b_d.get_center() + RIGHT * 0.3,
                                           b_d.get_center() + RIGHT * 0.3 + DOWN * 0.8, C_ACC, width=5, tip=0.16))
        self.play(Create(sol_g), Create(sol_d), FadeIn(v_g), FadeIn(v_d), FadeIn(m_g), FadeIn(m_d),
                  FadeIn(b_g), FadeIn(b_d))
        u_g = T("la route défile vers l'arrière", size=20, color=C_GRIS).move_to([-3.55, Y_SOL - 0.65, 0])
        u_d = T("la voiture avance à u", size=20, color=C_GRIS).move_to([3.55, Y_SOL - 0.65, 0])
        self.play(FadeIn(u_g), FadeIn(u_d))
        tr_g = TracedPath(b_g.get_center, stroke_color=ACCENT, stroke_width=4)
        tr_d = TracedPath(b_d.get_center, stroke_color=ACCENT, stroke_width=4)
        self.add(tr_g, tr_d)
        self.play(FadeIn(a_g), FadeIn(a_d))
        self.play(tt.animate.set_value(T_CH * 0.5), run_time=T_CH, rate_func=linear)
        la_g = M(r"\vec a\,' = -g\,\vec\jmath", size=30, color=C_ACC).next_to(a_g, RIGHT, buff=0.1)
        la_d = M(r"\vec a = -g\,\vec\jmath", size=30, color=C_ACC).next_to(a_d, RIGHT, buff=0.1)
        self.play(FadeIn(la_g), FadeIn(la_d))
        meme = T("même accélération des deux côtés", size=22, color=C_ACC).move_to([0, 1.3, 0])
        self.play(FadeIn(meme))
        self.wait(2)
        self.play(FadeOut(la_g), FadeOut(la_d), FadeOut(meme))
        self.play(tt.animate.set_value(T_CH), run_time=T_CH, rate_func=linear)
        self.play(FadeOut(a_g), FadeOut(a_d))
        r_g = T("ligne droite verticale", size=24, color=ACCENT).move_to([-3.55, 1.9, 0])
        r_d = T("parabole", size=24, color=ACCENT).move_to([3.55, 1.9, 0])
        self.play(FadeIn(r_g), FadeIn(r_d))
        self.wait(2)
        concl = encadre(T("Trajectoires différentes, mais MÊME accélération : a' = a.\n"
                          "Aucune expérience ne peut dire lequel est « vraiment » au repos :\n"
                          "le repos absolu n'existe pas (relativité de Galilée-Newton).", size=22))
        limiter(concl, 12.5).move_to(UP * 0.9)
        self.play(FadeIn(concl))
        self.wait(6)
        vider(self)
