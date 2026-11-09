"""5.4 — Référentiels non inertiels et forces fictives.

1. Une boîte qui accélère : dans le labo, la balle reste immobile ; dans la boîte, elle « part » vers
   l'arrière -> force fictive F' = −m a.
2. La force centrifuge : vue du référentiel tournant.
3. La voiture dans un virage : la balle va tout droit (sol), donc vers l'extérieur (voiture).

    python -m manim -pql chapitres/physique-ch5-dynamique-2/008-referentiels-non-inertiels/scene.py ReferentielsNonInertiels
"""

from shared.physique import *


def u(a):
    return np.array([np.cos(a), np.sin(a), 0])


class ReferentielsNonInertiels(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 5 · section 5.4", "Les référentiels non inertiels",
                    "Quand il faut inventer des forces pour que Newton marche encore")

        # --- 1. La boîte qui accélère -------------------------------------------------------------
        self.next_section("boite")
        titre = bandeau("Une balle dans une boîte qui accélère", "pas de frottement entre la balle et le fond")
        self.play(FadeIn(titre))
        sep = Line(UP * 3.0, DOWN * 3.9, color=C_GRIS, stroke_width=2)
        tg = T("Labo (S) : inertiel", size=24, color=C_VIT).move_to([-3.55, 2.5, 0])
        td = T("Boîte (S') : accélérée", size=24, color=C_NEG).move_to([3.55, 2.5, 0])
        self.play(Create(sep), FadeIn(tg), FadeIn(td))
        t = ValueTracker(0)
        A = 0.6
        dep = lambda: 0.5 * A * t.get_value() ** 2
        W, Hb = 3.8, 1.4
        y = -0.6

        def boite(cx):
            return VGroup(Line([cx - W / 2, y - Hb / 2, 0], [cx + W / 2, y - Hb / 2, 0], color=C_POS, stroke_width=5),
                          Line([cx - W / 2, y - Hb / 2, 0], [cx - W / 2, y + Hb / 2, 0], color=C_POS, stroke_width=5),
                          Line([cx + W / 2, y - Hb / 2, 0], [cx + W / 2, y + Hb / 2, 0], color=C_POS, stroke_width=5))

        bg = always_redraw(lambda: boite(-6.9 + W / 2 + dep()))
        balle_g = Dot([-6.9 + W / 2 + 1.0, y - Hb / 2 + 0.2, 0], radius=0.2, color=ACCENT)
        bd = boite(3.55)
        balle_d = always_redraw(lambda: Dot([3.55 + 1.0 - dep(), y - Hb / 2 + 0.2, 0], radius=0.2, color=ACCENT))
        ag = always_redraw(lambda: fleche([-6.9 + W / 2 + dep() - 0.6, y + Hb / 2 + 0.4, 0],
                                          [-6.9 + W / 2 + dep() + 0.6, y + Hb / 2 + 0.4, 0], C_ACC))
        la = always_redraw(lambda: M(r"\vec a", size=28, color=C_ACC).next_to(ag, UP, buff=0.05))
        self.play(FadeIn(bg), FadeIn(balle_g), FadeIn(bd), FadeIn(balle_d), FadeIn(ag), FadeIn(la))
        self.play(t.animate.set_value(2.4), run_time=3.5, rate_func=linear)
        cg = T("la balle ne bouge pas :\nforce résultante nulle ✔", size=20, color=C_VIT).move_to([-3.55, -2.6, 0])
        cd = T("la balle accélère vers l'arrière\nsans que rien ne la pousse ?!", size=20, color=C_NEG).move_to([3.55, -2.6, 0])
        self.play(FadeIn(cg), FadeIn(cd))
        self.wait(2)
        ff = fleche(balle_d.get_center() + UP * 0.45, balle_d.get_center() + UP * 0.45 + LEFT * 1.2, C_FORCE, width=6)
        lff = M(r"\vec F' = -m\vec a", size=30, color=C_FORCE).next_to(ff, UP, buff=0.08)
        self.play(GrowArrow(ff), FadeIn(lff))
        txt = encadre(T("Pour garder ΣF = m a dans S', l'observateur doit ajouter une force FICTIVE :\n"
                        "aucun objet ne l'exerce (pas de paire action-réaction), c'est l'effet de l'accélération du référentiel.",
                        size=20), color=C_FORCE)
        limiter(txt, 13.2).to_edge(DOWN, buff=0.1)
        self.play(FadeOut(cg), FadeOut(cd), FadeIn(txt))
        self.wait(5)
        vider(self)

        # --- 2. La force centrifuge -------------------------------------------------------------------
        self.next_section("centrifuge")
        titre = bandeau("La force centrifuge", "une particule au bout d'un fil, en mouvement circulaire uniforme")
        self.play(FadeIn(titre))
        sep = Line(UP * 2.9, DOWN * 3.9, color=C_GRIS, stroke_width=2)
        tg = T("Référentiel d'inertie", size=24, color=C_VIT).move_to([-3.55, 2.4, 0])
        td = T("Référentiel qui tourne avec le fil", size=24, color=C_NEG).move_to([3.55, 2.4, 0])
        self.play(Create(sep), FadeIn(tg), FadeIn(td))
        Cg, Cd, R = np.array([-3.55, -0.6, 0]), np.array([3.55, -0.6, 0]), 1.8
        ang = ValueTracker(0)
        cer = DashedVMobject(Circle(radius=R, color=C_GRIS).move_to(Cg), num_dashes=40)
        gauche = always_redraw(lambda: VGroup(
            Line(Cg, Cg + R * u(ang.get_value()), color=C_TEXTE, stroke_width=2),
            Dot(Cg + R * u(ang.get_value()), radius=0.15, color=ACCENT),
            fleche(Cg + R * u(ang.get_value()), Cg + (R - 1.0) * u(ang.get_value()), C_FORCE, width=6),
            fleche(Cg, Cg + 0.8 * u(ang.get_value()), C_GRIS, width=2, tip=0.12),
            fleche(Cg, Cg + 0.8 * u(ang.get_value() + PI / 2), C_GRIS, width=2, tip=0.12)))
        droite = VGroup(Line(Cd, Cd + R * RIGHT, color=C_TEXTE, stroke_width=2),
                        Dot(Cd + R * RIGHT, radius=0.15, color=ACCENT),
                        fleche(Cd, Cd + 0.8 * RIGHT, C_GRIS, width=2, tip=0.12),
                        fleche(Cd, Cd + 0.8 * UP, C_GRIS, width=2, tip=0.12))
        self.play(Create(cer), FadeIn(gauche), FadeIn(droite))
        self.play(ang.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        lt = M(r"\vec T", size=28, color=C_FORCE)
        g1 = T("seule force : T, vers le centre\n= force centripète", size=20, color=C_VIT).move_to([-3.55, -3.2, 0])
        fT = force(Cd + R * RIGHT, LEFT * 1.0, r"\vec T", direction=DOWN)
        fC = force(Cd + R * RIGHT, RIGHT * 1.0, r"\vec F_{cf} = \frac{m v^2}{r}", direction=UP, size=26)
        self.play(FadeIn(g1), GrowArrow(fT[0]), FadeIn(fT[1]), ang.animate.set_value(2.5 * PI), run_time=1.5, rate_func=linear)
        self.play(GrowArrow(fC[0]), FadeIn(fC[1]))
        d1 = T("la particule est au repos : il faut une force\nvers l'extérieur qui équilibre T → force centrifuge (fictive)",
               size=20, color=C_NEG).move_to([3.55, -3.2, 0])
        limiter(d1, 6.6)
        self.play(FadeIn(d1), ang.animate.set_value(3.5 * PI), run_time=2, rate_func=linear)
        self.wait(4)
        vider(self)

        # --- 3. La voiture dans un virage -------------------------------------------------------------
        self.next_section("virage")
        titre = bandeau("Le virage : d'où vient la « force centrifuge » ?",
                        "balle sans frottement sur le plancher d'une voiture qui tourne à gauche (vue de dessus)")
        self.play(FadeIn(titre))
        C = np.array([-5.6, -0.5, 0])
        Rv = 3.4
        w = 0.45
        tt = ValueTracker(0)
        a0 = -0.6
        route = Arc(radius=Rv, start_angle=a0 - 0.2, angle=1.4, arc_center=C, color=C_GRIS, stroke_width=30).set_stroke(opacity=0.25)
        P0 = C + Rv * u(a0)
        V0 = Rv * w * u(a0 + PI / 2)

        def voiture_pos():
            return C + Rv * u(a0 + w * tt.get_value())

        def balle_pos():
            return P0 + V0 * tt.get_value()

        auto = always_redraw(lambda: Rectangle(width=0.9, height=0.5, color=PRIMARY, fill_opacity=0.5)
                             .rotate(a0 + w * tt.get_value() + PI / 2).move_to(voiture_pos()))
        balle = always_redraw(lambda: Dot(balle_pos(), radius=0.1, color=ACCENT).set_z_index(3))
        trace = TracedPath(balle.get_center, stroke_color=ACCENT, stroke_width=3, dissipating_time=None)
        self.play(FadeIn(route), FadeIn(auto), FadeIn(balle))
        self.add(trace)
        self.play(tt.animate.set_value(1.6), run_time=3.5, rate_func=linear)
        sol = T("vue du sol : la balle continue TOUT DROIT (aucune force)\nc'est la voiture qui tourne sous elle",
                size=20, color=C_VIT).move_to(RIGHT * 3.3 + UP * 2.2)
        limiter(sol, 7.2)
        self.play(FadeIn(sol))
        # vue depuis la voiture (encart)
        cadre = Rectangle(width=4.2, height=3.0, color=C_GRIS).move_to(RIGHT * 4.2 + DOWN * 0.8)
        tit = T("vue depuis la voiture", size=20, color=C_NEG).next_to(cadre, UP, buff=0.08)
        auto_fixe = Rectangle(width=1.6, height=2.4, color=PRIMARY, fill_opacity=0.25).move_to(cadre)
        fl_av = Arrow(cadre.get_center() + DOWN * 0.6, cadre.get_center() + UP * 0.8, color=C_GRIS, buff=0, stroke_width=2)
        tt2 = ValueTracker(0)

        def rel():
            s = tt2.get_value()
            d = (P0 + V0 * s) - (C + Rv * u(a0 + w * s))
            th = a0 + w * s + PI / 2  # orientation de la voiture
            # coordonnées dans la voiture : (latéral droite, avant)
            avant = np.array([np.cos(th), np.sin(th), 0])
            droite = np.array([np.sin(th), -np.cos(th), 0])
            return cadre.get_center() + 1.6 * (np.dot(d, droite) * RIGHT + np.dot(d, avant) * UP)

        balle2 = always_redraw(lambda: Dot(rel(), radius=0.1, color=ACCENT))
        trace2 = TracedPath(balle2.get_center, stroke_color=ACCENT, stroke_width=3)
        self.play(Create(cadre), FadeIn(tit), FadeIn(auto_fixe), GrowArrow(fl_av), FadeIn(balle2))
        self.add(trace2)
        self.play(tt2.animate.set_value(1.1), run_time=3, rate_func=linear)
        ext = T("→ vers l'EXTÉRIEUR du virage :\non « invente » la force centrifuge", size=20, color=C_NEG)
        limiter(ext, 4.4)
        ext.next_to(cadre, DOWN, buff=0.15)
        self.play(FadeIn(ext))
        self.wait(5)
        vider(self)
