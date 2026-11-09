"""3.3 — Projectiles : exemple 1 (tir horizontal d'une falaise) et exemple 2 (tir oblique en terrain plat).

Scène 1 : ExempleFalaise    — v0 = 15 m/s horizontal, falaise de 20 m -> t = 2,02 s ; R = 30,3 m.
Scène 2 : ProjectileOblique — décomposition de v0, v_x constant / v_y qui change, temps de vol,
                              portée, parabole, et comparaison des angles (45° = portée max).

    manim -pql chapitres/physique-ch3-mouvement-2d/005-projectile-oblique/scene.py ExempleFalaise
    manim -pql chapitres/physique-ch3-mouvement-2d/005-projectile-oblique/scene.py ProjectileOblique
"""

from shared.physique import *

G = 9.8


class ExempleFalaise(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.3 · exemple 1", "Tir horizontal d'une falaise",
                    "v₀ = 15 m/s horizontalement, depuis 20 m de haut")
        titre = bandeau("Une balle lancée horizontalement d'une falaise")
        self.play(FadeIn(titre))
        ax = Axes(x_range=[-5, 35, 5], y_range=[0, 24, 5], x_length=8, y_length=4.8,
                  axis_config={"color": C_GRIS, "include_numbers": True, "font_size": 18},
                  tips=False)
        ax.shift(np.array([-4.6, -2.55, 0]) - np.array(ax.c2p(0, 0)))
        lx = M(r"x\ (\mathrm{m})", size=24, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        ly = M(r"y\ (\mathrm{m})", size=24, color=C_GRIS).next_to(ax.c2p(-5, 24), UP, buff=0.1)
        falaise = Polygon(ax.c2p(-5, 0), ax.c2p(0, 0), ax.c2p(0, 20), ax.c2p(-5, 20),
                          color=C_SOL, fill_opacity=0.8, stroke_width=0)
        self.play(Create(ax), FadeIn(lx), FadeIn(ly), FadeIn(falaise))

        v0, y0 = 15.0, 20.0
        t_vol = np.sqrt(2 * y0 / G)
        t = ValueTracker(0)

        def pos(tt):
            return np.array(ax.c2p(v0 * tt, y0 - 0.5 * G * tt * tt))

        balle = always_redraw(lambda: particule().move_to(pos(t.get_value())))
        fv = always_redraw(lambda: fleche(pos(t.get_value()), pos(t.get_value()) +
                                          0.05 * np.array([v0, -G * t.get_value(), 0]), C_VIT,
                                          width=5, tip=0.16))
        donnees = VGroup(
            T("Données", size=24, color=ACCENT, weight=BOLD),
            M(r"x_0 = 0 \quad y_0 = 20\ \mathrm{m}", size=30),
            M(r"v_{x0} = 15\ \mathrm{m/s} \quad v_{y0} = 0", size=30),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(RIGHT * 4.85 + UP * 2.2)
        self.play(FadeIn(balle), GrowArrow(fv), FadeIn(donnees))
        trace = TracedPath(balle.get_center, stroke_color=ACCENT, stroke_width=3)
        self.add(trace)
        self.play(t.animate.set_value(t_vol), run_time=t_vol * 1.6, rate_func=linear)
        strobo = VGroup(*[Dot(pos(k * t_vol / 8), radius=0.06, color=ACCENT) for k in range(9)])
        verticales = VGroup(*[DashedLine(pos(k * t_vol / 8), ax.c2p(v0 * k * t_vol / 8, 0),
                                         color=C_GRIS, stroke_width=1.2) for k in range(9)])
        self.play(FadeIn(strobo), Create(verticales))
        self.wait()

        a = VGroup(
            T("(a) Durée du vol : au sol, y = 0", size=22, color=ACCENT),
            M(r"0 = 20 + 0 - 4{,}9\,t^2", size=30),
            M(r"t = 2{,}02\ \mathrm{s}\quad (\text{ou } -2{,}02 : \text{rejeté})", size=28),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        b = VGroup(
            T("(b) Portée horizontale R", size=22, color=ACCENT),
            M(r"R = v_{x0}\,t = 15 \times 2{,}02 = 30{,}3\ \mathrm{m}", size=30),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        bloc = VGroup(a, b).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        limiter(bloc, 4.1).move_to(RIGHT * 4.85 + DOWN * 0.6)
        astuce = T("v_y0 = 0 : la chute dure autant\nque si on lâchait simplement la balle",
                   size=20, color=C_GRIS)
        self.play(FadeIn(a))
        self.wait(2)
        limiter(astuce, 4.1).next_to(bloc, DOWN, buff=0.3)
        b_brace = BraceBetweenPoints(ax.c2p(0, 0), ax.c2p(v0 * t_vol, 0), direction=DOWN,
                                     color=ACCENT).shift(DOWN * 0.35)
        lR = M("R", size=30, color=ACCENT).next_to(b_brace, DOWN, buff=0.08)
        self.play(FadeIn(b), GrowFromCenter(b_brace), FadeIn(lR))
        self.play(FadeIn(astuce))
        self.wait(5)
        vider(self)


class ProjectileOblique(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.3 · exemple 2", "Le tir oblique",
                    "Lancer avec un angle θ₀ en terrain plat")
        v0, th = 15.0, np.radians(50)
        vx0, vy0 = v0 * np.cos(th), v0 * np.sin(th)
        t_vol = 2 * vy0 / G
        ax = Axes(x_range=[0, 25, 5], y_range=[0, 12, 2], x_length=11.5, y_length=5.52,
                  axis_config={"color": C_GRIS, "include_numbers": True, "font_size": 18},
                  tips=False)
        ax.shift(np.array([-6.0, -3.3, 0]) - np.array(ax.c2p(0, 0)))
        lx = M(r"x\ (\mathrm{m})", size=24, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        ly = M(r"y\ (\mathrm{m})", size=24, color=C_GRIS).next_to(ax.y_axis, UP, buff=0.1)
        O = np.array(ax.c2p(0, 0))
        EV = 0.12

        # --- 1. Décomposer v0 ----------------------------------------------------------
        self.next_section("decomposition")
        titre = bandeau("D'abord : décomposer la vitesse initiale")
        self.play(FadeIn(titre), Create(ax), FadeIn(lx), FadeIn(ly))
        bout = O + EV * np.array([vx0, vy0, 0]) * 1.6
        f0 = fleche(O, bout, C_VIT, width=7)
        l0 = M(r"\vec v_0", size=34, color=C_VIT).next_to(bout, UP, buff=0.1)
        angle = Arc(radius=0.7, start_angle=0, angle=th, arc_center=O, color=ACCENT)
        lth = M(r"\theta_0", size=30, color=ACCENT).move_to(O + 1.0 * np.array([np.cos(th / 2), np.sin(th / 2), 0]))
        self.play(GrowArrow(f0), FadeIn(l0), Create(angle), FadeIn(lth))
        cx = DashedLine(O, [bout[0], O[1], 0], color=C_VIT, stroke_width=3)
        cy = DashedLine([bout[0], O[1], 0], bout, color=C_VIT, stroke_width=3)
        lcx = M(r"v_{x0} = v_0\cos\theta_0", size=30, color=C_VIT).next_to(cx, DOWN, buff=0.4).shift(RIGHT * 0.6)
        lcy = M(r"v_{y0} = v_0\sin\theta_0", size=30, color=C_VIT).next_to(cy, RIGHT, buff=0.15)
        self.play(Create(cx), FadeIn(lcx))
        self.play(Create(cy), FadeIn(lcy))
        ex = T("ici : v₀ = 15 m/s, θ₀ = 50°  →  v_x0 = 9,64 m/s ; v_y0 = 11,5 m/s",
               size=22, color=C_GRIS).move_to(UP * 2.4)
        self.play(FadeIn(ex))
        self.wait(3)
        self.play(FadeOut(VGroup(f0, l0, cx, cy, lcx, lcy, angle, lth, ex)))

        # --- 2. Le vol ---------------------------------------------------------------------
        self.next_section("vol")
        titre2 = bandeau("Pendant le vol : v_x ne bouge pas, v_y diminue")
        self.play(Transform(titre, titre2))
        t = ValueTracker(0)

        def pos(tt):
            return np.array(ax.c2p(vx0 * tt, vy0 * tt - 0.5 * G * tt * tt))

        def vit(tt):
            return np.array([vx0, vy0 - G * tt, 0])

        balle = always_redraw(lambda: particule().move_to(pos(t.get_value())))
        fv = always_redraw(lambda: fleche(pos(t.get_value()), pos(t.get_value()) + EV * vit(t.get_value()),
                                          C_VIT, width=6))
        fvx = always_redraw(lambda: fleche(pos(t.get_value()), pos(t.get_value()) +
                                           EV * vit(t.get_value()) * np.array([1, 0, 0]),
                                           C_TEXTE, width=3, tip=0.14).set_opacity(0.8))
        fvy = always_redraw(lambda: fleche(pos(t.get_value()), pos(t.get_value()) +
                                           EV * vit(t.get_value()) * np.array([0, 1, 0]),
                                           C_TEXTE, width=3, tip=0.14).set_opacity(0.8))
        cvx = Compteur("v_x =", lambda: vx0, r"\mathrm{m/s}", size=28)
        cvy = Compteur("v_y =", lambda: vit(t.get_value())[1], r"\mathrm{m/s}", size=28,
                       couleur_nombre=C_VIT, signe=True)
        compteurs = VGroup(cvx, cvy).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 4.6 + UP * 2.2)
        trace = TracedPath(balle.get_center, stroke_color=ACCENT, stroke_width=3)
        self.add(trace)
        self.play(FadeIn(balle), FadeIn(fv), FadeIn(fvx), FadeIn(fvy), FadeIn(compteurs))
        self.play(t.animate.set_value(t_vol / 2), run_time=3, rate_func=linear)
        sommet = T("au sommet : v_y = 0,\nmais v_x est toujours là", size=22, color=ACCENT)
        sommet.next_to(pos(t_vol / 2), UP, buff=0.5)
        self.play(FadeIn(sommet))
        self.wait(2)
        self.play(FadeOut(sommet))
        self.play(t.animate.set_value(t_vol), run_time=3, rate_func=linear)
        strobo = VGroup(*[Dot(pos(k * t_vol / 10), radius=0.06, color=ACCENT) for k in range(11)])
        vert = VGroup(*[DashedLine(pos(k * t_vol / 10), ax.c2p(vx0 * k * t_vol / 10, 0),
                                   color=C_GRIS, stroke_width=1.2) for k in range(11)])
        self.play(FadeIn(strobo), Create(vert))
        note = T("intervalles de temps égaux → écarts horizontaux égaux", size=20, color=C_GRIS)
        note.move_to(ax.c2p(12.5, 9.5))
        self.play(FadeIn(note))
        self.wait(3)
        self.play(FadeOut(VGroup(note, compteurs, fv, fvx, fvy, balle, vert)))
        self.remove(fv, fvx, fvy, balle)

        # --- 3. Les résultats ---------------------------------------------------------------
        self.next_section("formules")
        titre3 = bandeau("Temps de vol, portée, forme de la trajectoire")
        self.play(Transform(titre, titre3))
        f1 = VGroup(T("(a) au sol, y = 0 :", size=22, color=ACCENT),
                    M(r"t_{tp} = \frac{2 v_0 \sin\theta_0}{g}", size=34)).arrange(RIGHT, buff=0.2)
        f2 = VGroup(T("(b) portée R = v_x0 · t_tp :", size=22, color=ACCENT),
                    M(r"R_{tp} = \frac{v_0^2 \sin 2\theta_0}{g}", size=34)).arrange(RIGHT, buff=0.2)
        f3 = VGroup(T("(c) on élimine t :", size=22, color=ACCENT),
                    M(r"y = (\tan\theta_0)\,x - \frac{g}{2(v_0\cos\theta_0)^2}\,x^2", size=32),
                    T("→ parabole", size=22, color=C_GRIS)).arrange(RIGHT, buff=0.2)
        formules = VGroup(f1, f2, f3).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        limiter(formules, 9.5).move_to(UP * 1.5 + RIGHT * 1.0)
        tp = T("« tp » = terrain plat : départ et arrivée à la même hauteur", size=18, color=C_GRIS)
        for f in formules:
            self.play(FadeIn(f, shift=UP * 0.1))
            self.wait(1.2)
        tp.next_to(formules, DOWN, buff=0.12).align_to(formules, LEFT)
        bR = DoubleArrow(O, ax.c2p(vx0 * t_vol, 0), buff=0, color=ACCENT, stroke_width=4,
                         tip_length=0.18).shift(UP * 0.18)
        lR = M(r"R \approx 22{,}6\ \mathrm{m}", size=26, color=ACCENT)
        lR.next_to(ax.c2p(vx0 * t_vol, 0), UR, buff=0.15)
        self.play(FadeIn(tp), GrowFromCenter(bR), FadeIn(lR))
        self.wait(4)
        self.play(FadeOut(VGroup(formules, tp, bR, lR, strobo, trace)))
        self.remove(trace)

        # --- 4. Quel angle va le plus loin ? -----------------------------------------------------
        self.next_section("angles")
        titre4 = bandeau("Même v₀, angles différents : lequel va le plus loin ?")
        self.play(Transform(titre, titre4))
        couleurs = {15: C_GRIS, 30: PRIMARY, 45: ACCENT, 60: PRIMARY, 75: C_GRIS}
        courbes = VGroup()
        etiquettes = VGroup()
        for deg in (15, 30, 45, 60, 75):
            a = np.radians(deg)
            tv = 2 * v0 * np.sin(a) / G
            c = ax.plot_parametric_curve(
                lambda s, a=a: np.array([v0 * np.cos(a) * s, v0 * np.sin(a) * s - 0.5 * G * s * s, 0]),
                t_range=[0, tv], color=couleurs[deg], stroke_width=5 if deg == 45 else 3)
            courbes.add(c)
            top = ax.c2p(v0 * np.cos(a) * tv / 2, (v0 * np.sin(a)) ** 2 / (2 * G))
            etiquettes.add(M(f"{deg}^\\circ", size=26, color=couleurs[deg]).next_to(top, UP, buff=0.08))
        for c, e in zip(courbes, etiquettes):
            self.play(Create(c), FadeIn(e), run_time=1.0)
        self.wait()
        R45 = v0 ** 2 / G
        m45 = Dot(ax.c2p(R45, 0), color=ACCENT, radius=0.1)
        l45 = T("45° : portée maximale\n(sin 2θ₀ = 1)", size=22, color=ACCENT)
        l45.move_to(ax.c2p(21.5, 7.6))
        self.play(FadeIn(m45), FadeIn(l45), Indicate(courbes[2], color=ACCENT))
        self.wait(2)
        R30 = v0 ** 2 * np.sin(np.radians(60)) / G
        m30 = Dot(ax.c2p(R30, 0), color=PRIMARY, radius=0.1)
        l30 = T("30° et 60° :\nmême portée !", size=22, color=PRIMARY)
        l30.move_to(ax.c2p(21.5, 5.2))
        self.play(FadeIn(m30), FadeIn(l30), Indicate(courbes[1], color=PRIMARY),
                  Indicate(courbes[3], color=PRIMARY))
        regle = T("Angles complémentaires 45° + α et 45° − α  →  même portée", size=24, color=C_TEXTE)
        regle.move_to(UP * 2.55 + RIGHT * 1.5)
        self.play(FadeIn(regle))
        self.wait(5)
        vider(self)
