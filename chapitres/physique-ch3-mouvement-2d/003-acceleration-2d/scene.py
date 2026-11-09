"""3.2 — L'accélération dans le plan (équivalent du « film 3.1 »).

Un circuit : ligne droite où l'on accélère, virage à vitesse constante, ligne droite où l'on freine.
On suit en direct v (vert) et a (rose) :
- parties droites : a et v colinéaires (même sens -> accélère, sens opposés -> freine) ;
- virage : a pointe vers l'intérieur, alors que |v| ne change pas.

    manim -pql chapitres/physique-ch3-mouvement-2d/003-acceleration-2d/scene.py Acceleration2D
"""

from shared.physique import *

C = np.array([-1.5, -0.2, 0])
R = 2.3
X0, X1 = -5.5, -1.5
V_MIN, V_MAX = 0.3, 3.0
A_T = (V_MAX ** 2 - V_MIN ** 2) / (2 * (X1 - X0))
T1 = (V_MAX - V_MIN) / A_T
T2 = T1 + PI * R / V_MAX
T3 = T2 + T1
EV, EA = 0.45, 0.4


def etat(t):
    """(position, vitesse, accélération) en coordonnées écran à l'instant t."""
    if t <= T1:
        v = V_MIN + A_T * t
        x = X0 + V_MIN * t + 0.5 * A_T * t * t
        return np.array([x, C[1] - R, 0]), np.array([v, 0, 0]), np.array([A_T, 0, 0])
    if t <= T2:
        th = -PI / 2 + V_MAX * (t - T1) / R
        u_r = np.array([np.cos(th), np.sin(th), 0])
        u_t = np.array([-np.sin(th), np.cos(th), 0])
        return C + R * u_r, V_MAX * u_t, -V_MAX ** 2 / R * u_r
    tt = min(t, T3) - T2
    v = V_MAX - A_T * tt
    x = X1 - (V_MAX * tt - 0.5 * A_T * tt * tt)
    return np.array([x, C[1] + R, 0]), np.array([-v, 0, 0]), np.array([A_T, 0, 0])


class Acceleration2D(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.2", "L'accélération dans le plan",
                    "Accélérer, c'est changer de vitesse… ou de DIRECTION")
        titre = bandeau("Un circuit : accélérer, tourner, freiner",
                        "vert = vitesse,  rose = accélération")
        self.play(FadeIn(titre))

        circuit = VGroup(
            Line([X0, C[1] - R, 0], [X1, C[1] - R, 0]),
            Arc(radius=R, start_angle=-PI / 2, angle=PI, arc_center=C),
            Line([X1, C[1] + R, 0], [X0, C[1] + R, 0]),
        ).set_stroke(C_GRIS, width=14, opacity=0.35)
        self.play(Create(circuit), run_time=1.5)

        t = ValueTracker(0)
        bille = always_redraw(lambda: particule().move_to(etat(t.get_value())[0]))
        fv = always_redraw(lambda: fleche(etat(t.get_value())[0],
                                          etat(t.get_value())[0] + EV * etat(t.get_value())[1],
                                          C_VIT, width=6))
        fa = always_redraw(lambda: fleche(etat(t.get_value())[0],
                                          etat(t.get_value())[0] + EA * etat(t.get_value())[2],
                                          C_ACC, width=6))
        self.play(FadeIn(bille), FadeIn(fv), FadeIn(fa))
        col = RIGHT * 4.3

        def message(*lignes):
            g = VGroup(*lignes).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            limiter(g, 5.0)
            return g.move_to(col + UP * 0.3)

        lent = 1.6  # ralenti
        m1 = message(T("Ligne droite, on accélère", size=26, color=ACCENT),
                     T("a et v colinéaires, même sens", size=22),
                     T("→ seule la LONGUEUR de v change", size=22, color=C_GRIS))
        self.play(FadeIn(m1))
        self.play(t.animate.set_value(T1), run_time=T1 * lent, rate_func=linear)
        self.wait()
        m2 = message(T("Virage à vitesse constante", size=26, color=ACCENT),
                     T("|v| ne change pas… et pourtant a ≠ 0 !", size=22),
                     T("a pointe vers l'INTÉRIEUR du virage", size=22, color=C_ACC),
                     T("→ seule la DIRECTION de v change", size=22, color=C_GRIS))
        self.play(FadeOut(m1), FadeIn(m2))
        self.play(t.animate.set_value(T2), run_time=(T2 - T1) * lent, rate_func=linear)
        self.wait()
        m3 = message(T("Ligne droite, on freine", size=26, color=ACCENT),
                     T("a et v colinéaires, sens opposés", size=22),
                     T("→ la longueur de v diminue", size=22, color=C_GRIS))
        self.play(FadeOut(m2), FadeIn(m3))
        self.play(t.animate.set_value(T3), run_time=(T3 - T2) * lent, rate_func=linear)
        self.wait()
        bilan = encadre(VGroup(
            M(r"\vec a = \frac{d\vec v}{dt} = a_x\vec{\imath} + a_y\vec{\jmath}", size=34),
            T("a et v colinéaires SEULEMENT\nsur les parties rectilignes", size=22),
        ).arrange(DOWN, buff=0.2))
        limiter(bilan, 5.0).move_to(col + DOWN * 2.2)
        self.play(FadeOut(m3), FadeIn(bilan))
        self.wait(3)

        # --- Pourquoi a pointe vers l'intérieur : construire Δv ---------------------------
        self.next_section("delta-v")
        self.play(FadeOut(bille), FadeOut(fv), FadeOut(fa), FadeOut(bilan))
        titre2 = bandeau("Pourquoi vers l'intérieur ?", "on compare deux vitesses dans le virage")
        self.play(Transform(titre, titre2))
        ta, tb = T1 + (T2 - T1) * 0.3, T1 + (T2 - T1) * 0.6
        (pa, va, _), (pb, vb, _) = etat(ta), etat(tb)
        fa_ = fleche(pa, pa + EV * va, C_VIT)
        fb_ = fleche(pb, pb + EV * vb, C_VIT)
        la = M(r"\vec v_1", size=30, color=C_VIT).next_to(fa_.get_end(), RIGHT, buff=0.1)
        lb = M(r"\vec v_2", size=30, color=C_VIT).next_to(fb_.get_end(), UP, buff=0.1)
        self.play(FadeIn(Dot(pa, color=ACCENT)), FadeIn(Dot(pb, color=ACCENT)),
                  GrowArrow(fa_), GrowArrow(fb_), FadeIn(la), FadeIn(lb))
        origine = col + LEFT * 0.4 + DOWN * 1.0
        ca = fleche(origine, origine + 1.7 * EV * va, C_VIT)
        cb = fleche(origine, origine + 1.7 * EV * vb, C_VIT)
        cla = M(r"\vec v_1", size=30, color=C_VIT).next_to(ca.get_end(), RIGHT, buff=0.1)
        clb = M(r"\vec v_2", size=30, color=C_VIT).next_to(cb.get_end(), LEFT, buff=0.1)
        expl = T("on les place à la même origine", size=22, color=C_GRIS).move_to(col + DOWN * 1.55)
        self.play(FadeIn(expl))
        self.play(TransformFromCopy(fa_, ca), TransformFromCopy(fb_, cb), FadeIn(cla), FadeIn(clb))
        dv = fleche(ca.get_end(), cb.get_end(), C_ACC, width=7)
        ldv = M(r"\Delta\vec v = \vec v_2 - \vec v_1", size=30, color=C_ACC)
        ldv.next_to(dv, UP, buff=0.2)
        self.play(GrowArrow(dv), FadeIn(ldv))
        self.wait(2)
        tm = (ta + tb) / 2
        pm = etat(tm)[0]
        u = (cb.get_end() - ca.get_end())
        u = u / np.linalg.norm(u)
        dv_traj = fleche(pm, pm + 1.0 * u, C_ACC, width=7)
        vers_c = DashedLine(pm, C, color=C_GRIS, stroke_width=2)
        centre = Dot(C, color=C_GRIS)
        self.play(TransformFromCopy(dv, dv_traj), Create(vers_c), FadeIn(centre))
        concl = T("Δv (donc a) pointe vers le centre du virage", size=24, color=C_ACC)
        concl.move_to(col + DOWN * 2.4)
        limiter(concl, 5.4)
        self.play(FadeIn(concl))
        self.wait(5)
        vider(self)
