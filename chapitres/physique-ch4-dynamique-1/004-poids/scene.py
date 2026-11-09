"""4.3 — Le poids : gravitation universelle, P = m g, masse ≠ poids (Terre / Lune).

    python -m manim -pql chapitres/physique-ch4-dynamique-1/004-poids/scene.py Poids
"""

from shared.physique import *


class Poids(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 4 · section 4.3", "Le poids",
                    "La force avec laquelle la Terre nous attire")

        # --- 1. Gravitation universelle ---------------------------------------------------
        self.next_section("gravitation")
        titre = bandeau("La gravitation universelle (Newton, 1687)")
        self.play(FadeIn(titre))
        r = ValueTracker(5.0)
        yc = 0.6
        cM = lambda: np.array([-r.get_value() / 2, yc, 0])
        cm = lambda: np.array([r.get_value() / 2, yc, 0])
        gros = always_redraw(lambda: VGroup(Circle(radius=0.7, color=C_POS, fill_opacity=0.5),
                                            M("M", size=32)).move_to(cM()))
        petit = always_redraw(lambda: VGroup(Circle(radius=0.35, color=ACCENT, fill_opacity=0.5),
                                             M("m", size=26)).move_to(cm()))

        def longueur():
            return min(6.0 / r.get_value() ** 2 * 4, 2.2)

        f1 = always_redraw(lambda: fleche(cM() + RIGHT * 0.75, cM() + RIGHT * (0.75 + longueur()), C_FORCE))
        f2 = always_redraw(lambda: fleche(cm() + LEFT * 0.4, cm() + LEFT * (0.4 + longueur()), C_FORCE))
        br = always_redraw(lambda: BraceBetweenPoints(cM(), cm(), direction=DOWN, color=C_GRIS).shift(DOWN * 0.8))
        lr = always_redraw(lambda: M("r", size=30, color=C_GRIS).next_to(br, DOWN, buff=0.05))
        self.play(FadeIn(gros), FadeIn(petit), FadeIn(br), FadeIn(lr))
        self.play(GrowArrow(f1), GrowArrow(f2))
        loi = encadre(VGroup(M(r"F_g = G\,\frac{m M}{r^2}", size=44, color=C_FORCE),
                             M(r"G = 6{,}67\times 10^{-11}\ \mathrm{N\,m^2/kg^2}", size=26, color=C_GRIS))
                      .arrange(DOWN, buff=0.15)).move_to(DOWN * 2.6)
        self.play(FadeIn(loi))
        self.play(r.animate.set_value(3.5), run_time=2)
        self.play(r.animate.set_value(7.0), run_time=2)
        note = T("2 fois plus loin → 4 fois plus faible.  Toujours attractive, le long de la droite qui les relie.",
                 size=20, color=C_GRIS).move_to(UP * 2.4)
        limiter(note, 13)
        self.play(FadeIn(note))
        self.wait(3)
        vider(self)

        # --- 2. À la surface de la Terre : P = mg ----------------------------------------------
        self.next_section("p-egal-mg")
        titre = bandeau("Près de la surface de la Terre : le poids")
        self.play(FadeIn(titre))
        terre = Circle(radius=2.2, color=C_POS, fill_opacity=0.3).move_to(LEFT * 3.6 + DOWN * 1.2)
        lT = M(r"M_T", size=30).move_to(terre)
        obj = Dot(terre.get_top() + UP * 1.1, radius=0.12, color=ACCENT)
        fp = force(obj.get_center(), DOWN * 0.9, r"\vec P", direction=RIGHT)
        rT = DashedLine(terre.get_center(), terre.get_top(), color=C_GRIS)
        lrT = M(r"R_T", size=28, color=C_GRIS).next_to(rT, RIGHT, buff=0.1)
        self.play(FadeIn(terre), FadeIn(lT), Create(rT), FadeIn(lrT))
        self.play(FadeIn(obj), GrowArrow(fp[0]), FadeIn(fp[1]))
        calc = VGroup(
            M(r"P = G\,\frac{m M_T}{R_T^2} = m\,g", size=40),
            M(r"g = \frac{G M_T}{R_T^2} \approx 9{,}8\ \mathrm{N/kg}", size=36),
            T("g = champ gravitationnel à la surface", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.2 + UP * 1.0)
        for c in calc:
            self.play(FadeIn(c, shift=UP * 0.1))
            self.wait(0.6)
        vec = encadre(M(r"\vec P = m\,\vec g", size=44, color=C_FORCE)).move_to(RIGHT * 3.2 + DOWN * 1.3)
        self.play(FadeIn(vec))
        alt = T("g diminue avec l'altitude : environ −9 % à 300 km", size=22, color=ACCENT)
        alt.move_to(RIGHT * 3.2 + DOWN * 2.6)
        limiter(alt, 6.6)
        self.play(FadeIn(alt))
        self.wait(4)
        vider(self)

        # --- 3. Masse ≠ poids --------------------------------------------------------------------
        self.next_section("terre-lune")
        titre = bandeau("Masse et poids : deux choses différentes", "un astronaute de 75 kg")
        self.play(FadeIn(titre))
        cols = []
        for x, nom, g, P, coul in [(-3.5, "Sur la Terre", 9.8, 735, C_POS), (3.5, "Sur la Lune", 1.6, 120, C_GRIS)]:
            sol = Arc(radius=8, start_angle=PI / 2 - 0.35, angle=0.7, color=coul, stroke_width=8)
            sol.move_to([x, -2.4, 0])
            astro = VGroup(Circle(radius=0.25, color=C_TEXTE), Line(UP * 0.0, DOWN * 0.8, color=C_TEXTE),
                           Line(DOWN * 0.8, DOWN * 1.3 + LEFT * 0.3, color=C_TEXTE),
                           Line(DOWN * 0.8, DOWN * 1.3 + RIGHT * 0.3, color=C_TEXTE),
                           Line(DOWN * 0.3 + LEFT * 0.4, DOWN * 0.3 + RIGHT * 0.4, color=C_TEXTE))
            astro[1:].shift(DOWN * 0.25)
            astro.move_to([x, -1.0, 0])
            fp = force(astro.get_center() + RIGHT * 0.7, DOWN * (P / 735) * 1.2, "", width=7)
            info = VGroup(T(nom, size=28, color=coul, weight=BOLD),
                          M(r"m = 75\ \mathrm{kg}", size=34),
                          M(rf"g \approx {fr(g, 1)}\ \mathrm{{N/kg}}", size=30, color=C_GRIS),
                          M(rf"P = mg \approx {P}\ \mathrm{{N}}", size=34, color=C_FORCE)
                          ).arrange(DOWN, buff=0.18).move_to([x, 1.6, 0])
            cols.append((sol, astro, fp, info))
        for sol, astro, fp, info in cols:
            self.play(Create(sol), FadeIn(astro), FadeIn(info[0]), FadeIn(info[1]))
        self.wait()
        for sol, astro, fp, info in cols:
            self.play(FadeIn(info[2]), FadeIn(info[3]), GrowArrow(fp[0]))
        tab = T("masse : inertie, scalaire, en kg, la même partout\n"
                "poids : force, vecteur, en N, dépend du g local", size=24, color=ACCENT)
        tab = encadre(tab).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(tab))
        self.wait(4)
        piege = encadre(T("Piège : « je pèse 75 kilos » → c'est ta MASSE.  Ton poids vaut 735 N.",
                          size=24, color=C_NEG), color=C_NEG)
        limiter(piege, 13).to_edge(DOWN, buff=0.2)
        self.play(FadeOut(tab), FadeIn(piege))
        self.wait(4)
        vider(self)
