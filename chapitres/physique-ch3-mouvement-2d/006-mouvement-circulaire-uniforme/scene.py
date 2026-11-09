"""3.4 — Mouvement circulaire uniforme : l'accélération centripète.

1. La voiture qui tourne de l'est vers le sud : Δv pointe vers l'intérieur du virage.
2. Sur un cercle : quand Δθ -> 0, Δv devient perpendiculaire à v, vers le centre.
3. Triangles semblables -> a_c = v²/R.
4. Le mouvement en direct + période.

    manim -pql chapitres/physique-ch3-mouvement-2d/006-mouvement-circulaire-uniforme/scene.py MouvementCirculaireUniforme
"""

from shared.physique import *


def u(a):
    return np.array([np.cos(a), np.sin(a), 0])


def tang(a):  # tangente pour un sens de parcours anti-horaire
    return np.array([-np.sin(a), np.cos(a), 0])


class MouvementCirculaireUniforme(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.4", "Le mouvement circulaire uniforme",
                    "Vitesse de grandeur constante… et pourtant une accélération")

        # --- 1. La voiture qui tourne --------------------------------------------------
        self.next_section("virage")
        titre = bandeau("Une voiture roule vers l'est, puis tourne vers le sud",
                        "même compteur de vitesse avant et après")
        self.play(FadeIn(titre))
        Cv, Rv = np.array([-3.6, -2.3, 0]), 3.0
        route = Arc(radius=Rv, start_angle=PI / 2, angle=-PI / 2, arc_center=Cv,
                    stroke_width=26, color=C_GRIS).set_stroke(opacity=0.3)
        avant = Line(Cv + Rv * u(PI / 2) + LEFT * 2.5, Cv + Rv * u(PI / 2), stroke_width=26,
                     color=C_GRIS).set_stroke(opacity=0.3)
        apres = Line(Cv + Rv * u(0), Cv + Rv * u(0) + DOWN * 1.0, stroke_width=26,
                     color=C_GRIS).set_stroke(opacity=0.3)
        self.play(Create(avant), Create(route), Create(apres))
        L = 1.4
        a = ValueTracker(PI / 2)
        auto = always_redraw(lambda: particule(r=0.16).move_to(Cv + Rv * u(a.get_value())))
        fv = always_redraw(lambda: fleche(Cv + Rv * u(a.get_value()),
                                          Cv + Rv * u(a.get_value()) - L * tang(a.get_value()),
                                          C_VIT))
        self.play(FadeIn(auto), GrowArrow(fv))
        p1, p2 = Cv + Rv * u(PI / 2), Cv + Rv * u(0)
        v1 = fleche(p1, p1 + L * RIGHT, C_VIT)
        lv1 = M(r"\vec v_1", size=32, color=C_VIT).next_to(v1, UP, buff=0.1)
        self.add(v1, lv1)
        self.play(a.animate.set_value(0), run_time=3, rate_func=linear)
        v2 = fleche(p2, p2 + L * DOWN, C_VIT)
        lv2 = M(r"\vec v_2", size=32, color=C_VIT).next_to(v2, RIGHT, buff=0.1)
        self.add(v2, lv2)
        self.play(FadeOut(auto), FadeOut(fv), FadeIn(lv2))
        meme = T("|v₁| = |v₂|  mais  v₁ ≠ v₂ (plus la même direction)", size=24, color=ACCENT)
        meme.move_to(RIGHT * 3.4 + UP * 2.2)
        limiter(meme, 6.6)
        self.play(FadeIn(meme))
        o = np.array([3.0, -0.3, 0])
        c1 = fleche(o, o + L * 1.3 * RIGHT, C_VIT)
        c2 = fleche(o, o + L * 1.3 * DOWN, C_VIT)
        self.play(TransformFromCopy(v1, c1), TransformFromCopy(v2, c2))
        dv = fleche(c1.get_end(), c2.get_end(), C_ACC, width=7)
        ldv = M(r"\Delta\vec v = \vec v_2 - \vec v_1", size=30, color=C_ACC).next_to(dv.get_center(), DR, buff=0.2)
        self.play(GrowArrow(dv), FadeIn(ldv))
        milieu = Cv + Rv * u(PI / 4)
        dv_route = fleche(milieu, milieu + 1.0 * normalize(c2.get_end() - c1.get_end()), C_ACC, width=7)
        self.play(TransformFromCopy(dv, dv_route))
        txt = T("Δv — et donc l'accélération — pointe\nvers l'INTÉRIEUR du virage", size=24, color=C_ACC)
        txt.move_to(RIGHT * 3.4 + DOWN * 2.6)
        self.play(FadeIn(txt))
        self.wait(4)
        vider(self)

        # --- 2. Sur un cercle, Δθ -> 0 ---------------------------------------------------
        self.next_section("dtheta-vers-0")
        titre = bandeau("Sur un cercle, avec des instants de plus en plus proches")
        self.play(FadeIn(titre))
        C, R = np.array([-3.2, -0.5, 0]), 2.4
        cercle = Circle(radius=R, color=C_GRIS).move_to(C)
        centre = Dot(C, color=C_GRIS)
        lO = M("O", size=28, color=C_GRIS).next_to(C, DL, buff=0.08)
        self.play(Create(cercle), FadeIn(centre), FadeIn(lO))
        phi = PI / 3
        dth = ValueTracker(1.2)
        Lv = 1.3
        P = C + R * u(phi)
        pP = Dot(P, color=ACCENT)
        vP = fleche(P, P + Lv * tang(phi), C_VIT)
        Q = lambda: C + R * u(phi + dth.get_value())
        pQ = always_redraw(lambda: Dot(Q(), color=ACCENT))
        vQ = always_redraw(lambda: fleche(Q(), Q() + Lv * tang(phi + dth.get_value()), C_VIT))
        self.play(FadeIn(pP), GrowArrow(vP), FadeIn(pQ), GrowArrow(vQ))
        o = np.array([3.6, -1.2, 0])
        k = 1.5
        c1 = fleche(o, o + k * Lv * tang(phi), C_VIT)
        c2 = always_redraw(lambda: fleche(o, o + k * Lv * tang(phi + dth.get_value()), C_VIT))
        dv = always_redraw(lambda: fleche(o + k * Lv * tang(phi),
                                          o + k * Lv * tang(phi + dth.get_value()), C_ACC, width=7))
        l1 = M(r"\vec v_1", size=28, color=C_VIT).next_to(c1.get_end(), LEFT, buff=0.1)
        self.play(TransformFromCopy(vP, c1), TransformFromCopy(vQ, c2), FadeIn(l1))
        self.play(GrowArrow(dv))
        dth_txt = Compteur(r"\Delta\theta =", lambda: np.degrees(dth.get_value()), r"^\circ",
                           decimales=0, size=30).move_to(RIGHT * 3.6 + UP * 2.4)
        self.play(FadeIn(dth_txt))
        self.play(dth.animate.set_value(0.06), run_time=5, rate_func=lambda x: 1 - (1 - x) ** 2)
        rad = DashedLine(P, C, color=C_ACC, stroke_width=2)
        fl = fleche(P, P + 1.1 * normalize(C - P), C_ACC, width=7)
        self.play(Create(rad), TransformFromCopy(dv, fl))
        concl = T("Δv devient perpendiculaire à v :\nil pointe vers le CENTRE", size=24, color=C_ACC)
        concl.move_to(RIGHT * 3.6 + UP * 1.3)
        self.play(FadeIn(concl))
        nom = T("→ accélération centripète (« qui cherche le centre »)", size=22, color=ACCENT)
        nom.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(nom))
        self.wait(4)
        vider(self)

        # --- 3. Combien ? Triangles semblables ----------------------------------------------
        self.next_section("triangles")
        titre = bandeau("Combien vaut a ? Deux triangles semblables")
        self.play(FadeIn(titre))
        C, R = np.array([-4.0, -1.2, 0]), 2.6
        d = 0.7  # Δθ (rad), grand pour bien voir
        a1, a2 = PI / 2 - d / 2 - 0.25, PI / 2 + d / 2 - 0.25
        P, Q = C + R * u(a1), C + R * u(a2)
        arc = Arc(radius=R, start_angle=a1 - 0.6, angle=d + 1.2, arc_center=C, color=C_GRIS)
        tri_r = VGroup(fleche(C, P, C_POS, width=5), fleche(C, Q, C_POS, width=5),
                       fleche(P, Q, ACCENT, width=6))
        lr = VGroup(M(r"\vec r_1", size=28, color=C_POS).next_to((C + P) / 2, RIGHT, buff=0.1),
                    M(r"\vec r_2", size=28, color=C_POS).next_to((C + Q) / 2, LEFT, buff=0.1),
                    M(r"\Delta\vec r", size=28, color=ACCENT).next_to((P + Q) / 2, UP, buff=0.1))
        ang_r = Arc(radius=0.6, start_angle=a1, angle=d, arc_center=C, color=C_TEXTE)
        lang_r = M(r"\Delta\theta", size=26).move_to(C + 0.95 * u(PI / 2 - 0.25))
        self.play(Create(arc), *[GrowArrow(f) for f in tri_r], FadeIn(lr), Create(ang_r), FadeIn(lang_r))
        o = np.array([0.9, -2.0, 0])
        Lv = 2.6
        V1, V2 = o + Lv * tang(a1), o + Lv * tang(a2)
        tri_v = VGroup(fleche(o, V1, C_VIT, width=5), fleche(o, V2, C_VIT, width=5),
                       fleche(V1, V2, C_ACC, width=6))
        lv = VGroup(M(r"\vec v_1", size=28, color=C_VIT).next_to(V1, UP, buff=0.1),
                    M(r"\vec v_2", size=28, color=C_VIT).next_to(V2, DOWN, buff=0.12),
                    M(r"\Delta\vec v", size=28, color=C_ACC).next_to((V1 + V2) / 2, LEFT, buff=0.1))
        ang_v = Arc(radius=0.6, start_angle=a1 + PI / 2, angle=d, arc_center=o, color=C_TEXTE)
        lang_v = M(r"\Delta\theta", size=26).move_to(o + 0.95 * u(a1 + PI / 2 + d / 2))
        self.play(*[GrowArrow(f) for f in tri_v], FadeIn(lv), Create(ang_v), FadeIn(lang_v))
        pourquoi = T("même angle Δθ : v est toujours ⊥ à r,\nil tourne donc exactement autant",
                     size=22, color=C_GRIS).move_to(RIGHT * 3.6 + UP * 2.3)
        limiter(pourquoi, 6.6)
        self.play(FadeIn(pourquoi))
        self.wait(2)
        etapes = VGroup(
            T("triangles semblables :", size=24, color=C_GRIS),
            M(r"\frac{|\Delta\vec v|}{v} = \frac{|\Delta\vec r|}{r}", size=40),
            T("pour Δt petit :  |Δr| ≈ v Δt", size=24, color=C_GRIS),
            M(r"\frac{|\Delta\vec v|}{\Delta t} \approx \frac{v^2}{r}", size=40),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 4.6 + UP * 0.2)
        for e in etapes:
            self.play(FadeIn(e, shift=UP * 0.1))
            self.wait(0.8)
        res = encadre(M(r"a_c = \frac{v^2}{R}", size=48, color=C_ACC))
        res.move_to(RIGHT * 4.6 + DOWN * 2.6)
        self.play(FadeIn(res))
        self.wait(5)
        vider(self)

        # --- 4. En direct + période ------------------------------------------------------------
        self.next_section("direct")
        titre = bandeau("Le mouvement circulaire uniforme, en direct")
        self.play(FadeIn(titre))
        C, R = np.array([-3.4, -0.5, 0]), 2.4
        cercle = Circle(radius=R, color=C_GRIS).move_to(C)
        self.play(Create(cercle), FadeIn(Dot(C, color=C_GRIS)))
        ang = ValueTracker(0)
        pos = lambda: C + R * u(ang.get_value())
        bille = always_redraw(lambda: particule().move_to(pos()))
        fv = always_redraw(lambda: fleche(pos(), pos() + 1.3 * tang(ang.get_value()), C_VIT))
        fa = always_redraw(lambda: fleche(pos(), pos() - 1.1 * u(ang.get_value()), C_ACC))
        rayon = always_redraw(lambda: DashedLine(C, pos(), color=C_GRIS, stroke_width=2))
        self.play(FadeIn(bille), GrowArrow(fv), GrowArrow(fa), Create(rayon))
        leg = VGroup(T("v : tangente, longueur constante", size=22, color=C_VIT),
                     T("a : toujours vers le centre", size=22, color=C_ACC)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 3.8 + UP * 2.2)
        self.play(FadeIn(leg))
        self.play(ang.animate.set_value(2 * PI), run_time=5, rate_func=linear)
        formules = VGroup(
            M(r"\vec a = -\frac{v^2}{R}\,\vec u_r", size=34, color=C_ACC),
            T("période T = durée d'un tour complet (2πR)", size=22, color=C_GRIS),
            M(r"T = \frac{2\pi R}{v} \quad\Leftrightarrow\quad v = \frac{2\pi R}{T}", size=34),
            M(r"a_c = \frac{4\pi^2 R}{T^2}", size=34, color=C_ACC),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.8 + DOWN * 0.6)
        limiter(formules, 5.6)
        self.play(FadeIn(formules[0]), ang.animate.set_value(2 * PI + PI / 2), run_time=1.25,
                  rate_func=linear)
        for f in formules[1:]:
            self.play(FadeIn(f), ang.animate.increment_value(PI / 2), run_time=1.25, rate_func=linear)
        self.play(ang.animate.increment_value(4 * PI), run_time=5, rate_func=linear)
        self.wait(2)
        vider(self)
