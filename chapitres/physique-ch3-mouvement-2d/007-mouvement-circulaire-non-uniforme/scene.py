"""3.5 — Mouvement circulaire non uniforme : a = a_t (tangentielle) + a_r (radiale = centripète).

1. Sur un cercle : on accélère, on garde la vitesse, on freine -> on voit a_t apparaître / disparaître.
2. N'importe quelle courbe : même formule avec r = rayon de courbure (cercle osculateur).

    manim -pql chapitres/physique-ch3-mouvement-2d/007-mouvement-circulaire-non-uniforme/scene.py MouvementCirculaireNonUniforme
"""

from shared.physique import *

C = np.array([-3.3, -0.5, 0])
R = 2.2
V0, AT, D1, D2 = 0.3, 1.4, 1.6, 2.5   # vitesse initiale, a_t, durée accélération, durée palier
VMAX = V0 + AT * D1
TT = 2 * D1 + D2
EV, EA = 0.5, 0.4


def cinematique(t):
    """(s, v, a_t) : abscisse curviligne, vitesse, accélération tangentielle."""
    if t <= D1:
        return V0 * t + 0.5 * AT * t * t, V0 + AT * t, AT
    s1 = V0 * D1 + 0.5 * AT * D1 * D1
    if t <= D1 + D2:
        return s1 + VMAX * (t - D1), VMAX, 0.0
    tt = min(t, TT) - D1 - D2
    return s1 + VMAX * D2 + VMAX * tt - 0.5 * AT * tt * tt, VMAX - AT * tt, -AT


def u(a):
    return np.array([np.cos(a), np.sin(a), 0])


def ut(a):
    return np.array([-np.sin(a), np.cos(a), 0])


class MouvementCirculaireNonUniforme(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.5", "Le mouvement circulaire non uniforme",
                    "Quand la vitesse change de grandeur ET de direction")
        titre = bandeau("Deux morceaux d'accélération",
                        "orange = tangentielle,  rose = radiale (centripète),  blanc = totale")
        self.play(FadeIn(titre))
        cercle = Circle(radius=R, color=C_GRIS).move_to(C)
        self.play(Create(cercle), FadeIn(Dot(C, color=C_GRIS)))

        t = ValueTracker(0)
        ang0 = -PI / 2

        def etat():
            s, v, at = cinematique(t.get_value())
            a = ang0 + s / R
            return a, v, at

        def pos():
            return C + R * u(etat()[0])

        def vec_at():
            a, v, at = etat()
            return EA * at * ut(a)

        def vec_ar():
            a, v, at = etat()
            return -EA * v * v / R * u(a)

        bille = always_redraw(lambda: particule().move_to(pos()))
        fv = always_redraw(lambda: fleche(pos(), pos() + EV * etat()[1] * ut(etat()[0]), C_VIT, width=5))
        fat = always_redraw(lambda: fleche(pos(), pos() + vec_at(), ACCENT, width=6))
        far = always_redraw(lambda: fleche(pos(), pos() + vec_ar(), C_ACC, width=6))
        ftot = always_redraw(lambda: fleche(pos(), pos() + vec_at() + vec_ar(), C_TEXTE, width=7))
        para = always_redraw(lambda: VGroup(
            DashedLine(pos() + vec_at(), pos() + vec_at() + vec_ar(), color=C_GRIS, stroke_width=1.5),
            DashedLine(pos() + vec_ar(), pos() + vec_at() + vec_ar(), color=C_GRIS, stroke_width=1.5)))
        self.play(FadeIn(bille), FadeIn(fv), FadeIn(fat), FadeIn(far), FadeIn(ftot), FadeIn(para))

        col = RIGHT * 3.9
        comp = VGroup(
            Compteur("v =", lambda: etat()[1], r"\mathrm{m/s}", decimales=2, size=28,
                     couleur_nombre=C_VIT),
            Compteur(r"a_t = \tfrac{dv_t}{dt} =", lambda: etat()[2], r"\mathrm{m/s^2}", decimales=2,
                     size=28, couleur_nombre=ACCENT, signe=True),
            Compteur(r"a_r = \tfrac{v^2}{r} =", lambda: etat()[1] ** 2 / R, r"\mathrm{m/s^2}",
                     decimales=2, size=28, couleur_nombre=C_ACC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(col + UP * 1.8)
        self.play(FadeIn(comp))

        def phase(txt, couleur):
            return T(txt, size=26, color=couleur).move_to(col + UP * 0.1)

        lent = 2.2
        p1 = phase("on accélère : a_t dans le sens de v", ACCENT)
        self.play(FadeIn(p1))
        self.play(t.animate.set_value(D1), run_time=D1 * lent, rate_func=linear)
        p2 = phase("vitesse constante : a_t = 0 → MCU", C_ACC)
        self.play(FadeOut(p1), FadeIn(p2))
        self.play(t.animate.set_value(D1 + D2), run_time=D2 * lent, rate_func=linear)
        p3 = phase("on freine : a_t opposé à v", ACCENT)
        self.play(FadeOut(p2), FadeIn(p3))
        self.play(t.animate.set_value(TT), run_time=D1 * lent, rate_func=linear)
        self.wait()
        self.play(FadeOut(p3))

        roles = VGroup(
            T("a_t (tangentielle) : change la GRANDEUR de v", size=22, color=ACCENT),
            T("a_r (radiale) : change la DIRECTION de v", size=22, color=C_ACC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(col + DOWN * 0.3)
        limiter(roles, 6.0)
        formule = encadre(M(r"\vec a = \frac{dv_t}{dt}\,\vec u_\theta - \frac{v^2}{r}\,\vec u_r",
                            size=38))
        formule.move_to(col + DOWN * 1.9)
        num = M("(3.17)", size=22, color=C_GRIS).next_to(formule, DOWN, buff=0.12)
        self.play(FadeIn(roles))
        self.play(FadeIn(formule), FadeIn(num))
        self.wait(5)
        vider(self)

        # --- 2. N'importe quelle courbe ------------------------------------------------------
        self.next_section("rayon-courbure")
        titre = bandeau("Et sur une courbe quelconque ?",
                        "on remplace r par le rayon de courbure : le rayon du cercle qui « colle » à la courbe")
        self.play(FadeIn(titre))
        A, k, y0 = 1.3, 0.85, -0.6

        def f(x):
            return y0 + A * np.sin(k * (x + 6.5))

        def d1(x):
            return A * k * np.cos(k * (x + 6.5))

        def d2(x):
            return -A * k * k * np.sin(k * (x + 6.5))

        courbe = ParametricFunction(lambda x: np.array([x, f(x), 0]), t_range=[-6.8, 1.5],
                                    color=C_GRIS, stroke_width=4)
        self.play(Create(courbe))
        x = ValueTracker(-6.3)

        def osc():
            xx = x.get_value()
            p = np.array([xx, f(xx), 0])
            kap = abs(d2(xx)) / (1 + d1(xx) ** 2) ** 1.5
            n = np.array([-d1(xx), 1, 0]) / np.sqrt(1 + d1(xx) ** 2) * np.sign(d2(xx) or 1)
            if kap < 1 / 2.4:
                return VGroup(Dot(p, color=ACCENT))
            rho = 1 / kap
            c = p + rho * n
            return VGroup(Circle(radius=rho, color=PRIMARY, stroke_width=2).move_to(c),
                          DashedLine(p, c, color=PRIMARY, stroke_width=2),
                          Dot(c, color=PRIMARY, radius=0.05),
                          Dot(p, color=ACCENT))

        cercle_osc = always_redraw(osc)
        self.play(FadeIn(cercle_osc))
        self.play(x.animate.set_value(1.0), run_time=8, rate_func=linear)
        txt = VGroup(
            T("virage serré → petit rayon → a_r grand", size=22, color=C_ACC),
            T("presque droit → rayon énorme → a_r ≈ 0", size=22, color=C_GRIS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 4.5 + DOWN * 2.9)
        limiter(txt, 4.6)
        self.play(FadeIn(txt))
        self.play(x.animate.set_value(-6.3), run_time=6, rate_func=linear)
        self.wait(3)
        vider(self)
