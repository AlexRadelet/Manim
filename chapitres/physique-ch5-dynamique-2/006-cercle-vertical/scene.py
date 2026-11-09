"""5.2 — Mouvement circulaire non uniforme : la pierre au bout d'une corde dans un cercle vertical,
puis le skieur sur une bosse.

Pierre : r = 1 m, m = 1 kg, v_haut = 4 m/s (vitesse non uniforme, elle accélère en descendant).
  T = m v²/r + m g cos θ (θ mesuré depuis le bas) -> T_bas ≈ 65 N, T_haut ≈ 6,2 N.
Skieur : N = m g − m v²/r, décolle si v > √(r g).

    python -m manim -pql chapitres/physique-ch5-dynamique-2/006-cercle-vertical/scene.py CercleVertical
"""

from shared.physique import *

g, r, m = 9.8, 1.0, 1.0
V_HAUT = 4.0
V_BAS2 = V_HAUT ** 2 + 4 * g * r


def v2(phi):  # phi : angle depuis le bas
    return V_BAS2 - 2 * g * r * (1 - np.cos(phi))


def tension(phi):
    return m * v2(phi) / r + m * g * np.cos(phi)


# phi(t) : on intègre dphi/dt = v / r (une révolution)
_ts, _ph = [0.0], [0.0]
while _ph[-1] < 2 * PI:
    _ph.append(_ph[-1] + np.sqrt(v2(_ph[-1])) / r * 0.001)
    _ts.append(_ts[-1] + 0.001)
T_TOUR = _ts[-1]


def phi_de_t(t):
    t = t % T_TOUR
    return float(np.interp(t, _ts, _ph))


class CercleVertical(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 5 · section 5.2", "Le cercle vertical",
                    "Quand la vitesse ET la direction changent")

        # --- 1. La pierre -------------------------------------------------------------------
        self.next_section("pierre")
        titre = bandeau("Une pierre au bout d'une corde, dans un cercle vertical",
                        "seules forces : la tension et le poids ; r = 1 m, m = 1 kg, v = 4 m/s en haut")
        self.play(FadeIn(titre))
        C = np.array([-3.4, -0.4, 0])
        R = 2.0
        K = 0.025
        t = ValueTracker(0)
        cercle = DashedVMobject(Circle(radius=R, color=C_GRIS).move_to(C), num_dashes=50)

        def pos():
            ph = phi_de_t(t.get_value())
            return C + R * np.array([np.sin(ph), -np.cos(ph), 0])

        def scene_pierre():
            ph = phi_de_t(t.get_value())
            p = pos()
            vers_c = (C - p) / R
            g_ = VGroup(Line(C, p, color=C_TEXTE, stroke_width=2), Dot(C, color=C_GRIS),
                        Dot(p, radius=0.15, color=ACCENT).set_z_index(3))
            g_.add(fleche(p, p + vers_c * tension(ph) * K, C_FORCE, width=6))
            g_.add(fleche(p + RIGHT * 0.25, p + RIGHT * 0.25 + DOWN * m * g * K * 3, C_FORCE, width=4))
            return g_

        pierre = always_redraw(scene_pierre)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=C_FORCE, stroke_width=6), M(r"\vec T", size=26, color=C_FORCE)).arrange(RIGHT),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, color=C_FORCE, stroke_width=4), M(r"m\vec g\ (\times 3)", size=24, color=C_FORCE)).arrange(RIGHT)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(C + DOWN * 2.9 + LEFT * 1.3)
        cpt = VGroup(Compteur("v =", lambda: np.sqrt(v2(phi_de_t(t.get_value()))), r"\mathrm{m/s}", size=30, couleur_nombre=C_VIT),
                     Compteur("T =", lambda: tension(phi_de_t(t.get_value())), r"\mathrm{N}", size=30, couleur_nombre=C_FORCE)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(C + DOWN * 2.9 + RIGHT * 1.6)
        self.play(Create(cercle), FadeIn(pierre), FadeIn(leg), FadeIn(cpt))
        self.play(t.animate.set_value(2 * T_TOUR), run_time=2 * T_TOUR * 2.2, rate_func=linear)
        self.wait()

        col = RIGHT * 3.5
        bas = VGroup(T("en bas : T et mg opposés", size=22, color=ACCENT),
                     M(r"T - mg = \frac{m v_b^2}{r} \Rightarrow T = \frac{m v_b^2}{r} + mg", size=30)).arrange(DOWN, buff=0.12)
        haut = VGroup(T("en haut : T et mg tous deux vers le centre", size=22, color=ACCENT),
                      M(r"T + mg = \frac{m v_h^2}{r} \Rightarrow T = \frac{m v_h^2}{r} - mg", size=30)).arrange(DOWN, buff=0.12)
        quel = VGroup(T("à un angle θ quelconque (depuis le bas) :", size=22, color=ACCENT),
                      M(r"T = \frac{m v^2}{r} + mg\cos\theta \qquad a_t = g\sin\theta", size=30)).arrange(DOWN, buff=0.12)
        bloc_eq = VGroup(bas, haut, quel).arrange(DOWN, buff=0.35)
        limiter(bloc_eq, 6.6)
        if bloc_eq.height > 5.2:
            bloc_eq.scale_to_fit_height(5.2)
        bloc_eq.move_to(col + DOWN * 0.15)
        # arrêt en bas, puis en haut
        self.play(t.animate.set_value(3 * T_TOUR), run_time=1.0)
        self.play(FadeIn(bas))
        self.wait(2)
        t_haut = _ts[int(np.searchsorted(_ph, PI))]
        self.play(t.animate.set_value(3 * T_TOUR + t_haut), run_time=1.6)
        self.play(FadeIn(haut))
        self.wait(2)
        self.play(FadeIn(quel))
        cle = T("La corde tire le plus fort en bas (≈ 65 N) et le moins en haut (≈ 6 N) :\n"
                "c'est en bas qu'elle risque de casser.", size=20, color=C_VIT).to_edge(DOWN, buff=0.15).set_x(3.4)
        limiter(cle, 7.2)
        self.play(FadeIn(cle))
        self.wait(5)
        vider(self)

        # --- 2. Le skieur sur la bosse ------------------------------------------------------------
        self.next_section("skieur")
        titre = bandeau("Un skieur passe sur une bosse arrondie (rayon r)",
                        "jusqu'à quelle vitesse garde-t-il le contact ?")
        self.play(FadeIn(titre))
        Rb, gs = 2.2, 2.0  # rayon écran, « g » écran
        O = np.array([-2.6, -3.0, 0])
        bosse = Arc(radius=Rb, start_angle=0, angle=PI, arc_center=O, color=C_TEXTE, stroke_width=4)
        neige = Line(O + LEFT * 4.4, O + RIGHT * 6.0, color=C_TEXTE, stroke_width=4)
        top = O + UP * Rb
        self.play(Create(neige), Create(bosse))
        v = ValueTracker(0.8)
        ski = Dot(top, radius=0.15, color=ACCENT).set_z_index(3)
        Kf = 0.9

        def N_de_v():
            return max(gs - v.get_value() ** 2 / Rb, 0)

        fP = force(top + LEFT * 0.25, DOWN * gs * Kf, r"m\vec g", direction=LEFT)
        fN = always_redraw(lambda: fleche(top + RIGHT * 0.25, top + RIGHT * 0.25 + UP * (N_de_v() * Kf + 1e-3), C_FORCE, width=6))
        lN = always_redraw(lambda: M(r"\vec N", size=28, color=C_FORCE).next_to(top + RIGHT * 0.25 + UP * N_de_v() * Kf, RIGHT, buff=0.1))
        self.play(FadeIn(ski), GrowArrow(fP[0]), FadeIn(fP[1]), FadeIn(fN), FadeIn(lN))
        eqs = VGroup(
            T("au sommet, le centre est EN DESSOUS :", size=22, color=C_GRIS),
            M(r"mg - N = \frac{m v^2}{r} \;\Rightarrow\; N = mg - \frac{m v^2}{r}", size=32),
            T("N = poids apparent : plus on va vite, plus on se sent léger", size=20, color=ACCENT),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.5 + UP * 1.6)
        limiter(eqs, 6.6)
        self.play(FadeIn(eqs))
        cv = Compteur("v / \\sqrt{rg} =", lambda: v.get_value() / np.sqrt(gs * Rb), "", decimales=2, size=30,
                      couleur_nombre=C_VIT).move_to(RIGHT * 3.5 + DOWN * 0.1)
        self.play(FadeIn(cv))
        self.play(v.animate.set_value(np.sqrt(gs * Rb)), run_time=4, rate_func=linear)
        n0 = encadre(VGroup(T("N = 0 quand", size=22), M(r"v = \sqrt{r g}", size=40, color=ACCENT)).arrange(RIGHT, buff=0.3))
        n0.move_to(RIGHT * 3.5 + DOWN * 1.2)
        self.play(FadeIn(n0))
        self.wait(1)
        # plus vite : il décolle
        self.play(FadeOut(fN), FadeOut(lN), FadeOut(fP))
        vs = 1.35 * np.sqrt(gs * Rb)
        tt = ValueTracker(0)
        ski.add_updater(lambda d: d.move_to(top + np.array([vs * tt.get_value(), -0.5 * gs * tt.get_value() ** 2, 0])))
        trace = TracedPath(ski.get_center, stroke_color=ACCENT, stroke_width=3)
        self.add(trace)
        self.play(tt.animate.set_value(np.sqrt(2 * Rb / gs)), run_time=2.5, rate_func=linear)
        ski.clear_updaters()
        vole = T("plus vite : les skis décollent\n→ chute libre (parabole)", size=24, color=C_NEG)
        limiter(vole, 4.8)
        vole.move_to(RIGHT * 4.6 + DOWN * 2.45)
        self.play(FadeIn(vole))
        self.wait(5)
        vider(self)
