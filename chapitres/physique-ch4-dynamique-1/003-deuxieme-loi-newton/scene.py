"""4.2 — La deuxième loi de Newton : ΣF = m a.

1. a ∝ F (masse fixée) et a ∝ 1/m (force fixée), vu avec des images stroboscopiques.
2. La loi, l'unité newton, les composantes.
3. a a la direction de la force RÉSULTANTE, pas forcément celle de v.

    python -m manim -pql chapitres/physique-ch4-dynamique-1/003-deuxieme-loi-newton/scene.py DeuxiemeLoiNewton
"""

from shared.physique import *


class DeuxiemeLoiNewton(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 4 · section 4.2", "La deuxième loi de Newton",
                    "De combien une force change-t-elle la vitesse ?")

        # --- 1. Trois expériences -----------------------------------------------------------
        self.next_section("experiences")
        titre = bandeau("Trois chariots, partis du repos", "images toutes les 0,4 s")
        self.play(FadeIn(titre))
        cas = [("F", "m", 1.0, "a"), ("2F", "m", 2.0, "2a"), ("F", "2m", 0.5, "a/2")]
        ys = [1.6, 0.0, -1.6]
        x0 = -5.6
        t = ValueTracker(0)
        objets = VGroup()
        for (Fs, ms, a, res), y in zip(cas, ys):
            sol = Line([-6.8, y - 0.38, 0], [4.0, y - 0.38, 0], color=C_SOL, stroke_width=4)
            larg = 0.8 if ms == "m" else 1.15
            ch = bloc(ms, larg, 0.6, size=24).move_to([x0, y, 0])
            fl = always_redraw(lambda ch=ch, Fs=Fs: force(ch.get_right(), RIGHT * (0.7 if Fs == "F" else 1.4),
                                                          "", width=5))
            ch.add_updater(lambda mob, a=a: mob.set_x(x0 + 0.5 * a * 1.0 * t.get_value() ** 2))
            lab = M(Fs + r",\ " + ms, size=26, color=C_FORCE).next_to([-6.8, y + 0.35, 0], RIGHT, buff=0.0)
            objets.add(VGroup(sol, ch, fl, lab))
            self.play(Create(sol), FadeIn(ch), FadeIn(fl), FadeIn(lab), run_time=0.6)
        self.play(t.animate.set_value(3.0), run_time=3.0, rate_func=linear)
        strobo = VGroup()
        for (Fs, ms, a, res), y in zip(cas, ys):
            for s in np.arange(0, 3.01, 0.4):
                strobo.add(Dot([x0 + 0.5 * a * s * s, y, 0], radius=0.06, color=ACCENT).set_opacity(0.7))
        self.play(FadeIn(strobo))
        resultats = VGroup(*[M(r"\Rightarrow\ " + res, size=34, color=C_ACC).move_to([6.2, y, 0])
                             for (_, _, _, res), y in zip(cas, ys)])
        self.play(LaggedStart(*[FadeIn(r) for r in resultats], lag_ratio=0.4))
        conclu = VGroup(M(r"a \propto F", size=36, color=C_ACC), M(r"a \propto \frac{1}{m}", size=36, color=C_ACC)
                        ).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(conclu))
        self.wait(4)
        for o in objets:
            o[1].clear_updaters()
        vider(self)

        # --- 2. La loi -------------------------------------------------------------------------
        self.next_section("loi")
        titre = bandeau("La deuxième loi de Newton")
        self.play(FadeIn(titre))
        loi = encadre(VGroup(M(r"\sum \vec F = m\,\vec a", size=60),
                             T("la force RÉSULTANTE produit une accélération de même direction",
                               size=22, color=C_GRIS)).arrange(DOWN, buff=0.25)).move_to(UP * 1.2)
        self.play(FadeIn(loi))
        unite = M(r"1\ \mathrm{N} = 1\ \mathrm{kg}\cdot\mathrm{m/s^2}", size=36).move_to(DOWN * 0.6)
        comp = M(r"\sum F_x = m a_x \qquad \sum F_y = m a_y \qquad \sum F_z = m a_z", size=34)
        comp.move_to(DOWN * 1.7)
        nb = T("valable seulement dans un référentiel d'inertie", size=22, color=ACCENT).move_to(DOWN * 2.8)
        self.play(Write(unite))
        self.play(FadeIn(comp))
        self.play(FadeIn(nb))
        self.wait(4)
        vider(self)

        # --- 3. Direction : la résultante, pas la vitesse ---------------------------------------
        self.next_section("direction")
        titre = bandeau("a suit la force résultante… pas la vitesse")
        self.play(FadeIn(titre))
        O = LEFT * 3.8 + DOWN * 0.4
        p = particule().move_to(O)
        F1, F2, F3 = np.array([2.2, 0.8, 0]), np.array([-0.6, 1.6, 0]), np.array([0.2, -1.2, 0])
        fs = [force(O, F1, r"\vec F_1", direction=RIGHT), force(O, F2, r"\vec F_2", direction=UP),
              force(O, F3, r"\vec F_3", direction=DOWN)]
        self.play(FadeIn(p), *[GrowArrow(f[0]) for f in fs], *[FadeIn(f[1]) for f in fs])
        S = F1 + F2 + F3
        # construction bout à bout
        c2 = fs[1][0].copy()
        c3 = fs[2][0].copy()
        self.play(c2.animate.shift(F1), c3.animate.shift(F1 + F2))
        R = force(O, S, r"\sum\vec F", color=ACCENT, direction=UR, width=8)
        self.play(GrowArrow(R[0]), FadeIn(R[1]))
        acc = force(O, S / np.linalg.norm(S) * 1.0 + 0.0001, r"\vec a", color=C_ACC, direction=DR, width=7)
        perp = np.array([S[1], -S[0], 0]) / np.linalg.norm(S)
        acc.shift(perp * 0.3)
        self.play(FadeOut(c2), FadeOut(c3), GrowArrow(acc[0]), FadeIn(acc[1]))
        t1 = T("a est parallèle à ΣF\n(et ΣF / m en longueur)", size=24, color=C_ACC).move_to(RIGHT * 3.4 + UP * 1.5)
        self.play(FadeIn(t1))
        self.wait(2)
        # projectile : v tangent, F = mg vers le bas
        self.play(FadeOut(VGroup(p, *fs, R, acc)))
        ax0 = np.array([-5.8, -2.6, 0])
        traj = ParametricFunction(lambda s: ax0 + np.array([s, 2.4 * s - 0.55 * s * s, 0]),
                                  t_range=[0, 4.4], color=C_GRIS, stroke_width=3)
        s0 = 1.0
        P0 = ax0 + np.array([s0, 2.4 * s0 - 0.55 * s0 ** 2, 0])
        v = np.array([1, 2.4 - 1.1 * s0, 0])
        v = v / np.linalg.norm(v) * 1.5
        self.play(Create(traj))
        bille = particule().move_to(P0)
        fv = fleche(P0, P0 + v, C_VIT)
        lv = M(r"\vec v", size=30, color=C_VIT).next_to(P0 + v, UR, buff=0.05)
        fp = force(P0, DOWN * 1.3, r"\sum\vec F = m\vec g", direction=RIGHT)
        self.play(FadeIn(bille), GrowArrow(fv), FadeIn(lv), GrowArrow(fp[0]), FadeIn(fp[1]))
        t2 = T("Projectile : v est tangente à la trajectoire,\nmais la force (le poids) est verticale.",
               size=24).move_to(RIGHT * 3.4 + DOWN * 0.6)
        limiter(t2, 6.4)
        self.play(FadeIn(t2))
        self.wait(4)
        vider(self)
