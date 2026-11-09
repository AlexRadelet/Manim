"""4.4 — La troisième loi de Newton : F_AB = −F_BA, et les trois erreurs classiques.

1. Deux patineurs qui se poussent.
2. Même force, accélérations différentes (pomme / Terre).
3. La pomme sur la table : deux paires action-réaction, et l'équilibre qui n'en est PAS une.

    python -m manim -pql chapitres/physique-ch4-dynamique-1/005-troisieme-loi-newton/scene.py TroisiemeLoiNewton
"""

from shared.physique import *


class TroisiemeLoiNewton(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 4 · section 4.4", "La troisième loi de Newton",
                    "Impossible de pousser sans être poussé")

        # --- 1. La loi -------------------------------------------------------------------------
        self.next_section("loi")
        titre = bandeau("Les forces vont toujours par paires", "F_AB = force exercée SUR A PAR B")
        self.play(FadeIn(titre))
        y = 0.6
        A = VGroup(Circle(radius=0.55, color=C_POS, fill_opacity=0.5), T("A", size=30)).move_to([-0.6, y, 0])
        B = VGroup(Circle(radius=0.55, color=ACCENT, fill_opacity=0.5), T("B", size=30)).move_to([0.6, y, 0])
        sol = Line([-6.5, y - 0.6, 0], [6.5, y - 0.6, 0], color=PRIMARY, stroke_width=4).set_opacity(0.5)
        glace = T("patinoire (sans frottement)", size=18, color=PRIMARY).next_to(sol, DOWN, buff=0.1)
        self.play(FadeIn(sol), FadeIn(glace), FadeIn(A), FadeIn(B))
        fab = force(A.get_center(), LEFT * 1.4, r"\vec F_{AB}", direction=UP)
        fba = force(B.get_center(), RIGHT * 1.4, r"\vec F_{BA}", direction=UP)
        self.play(GrowArrow(fab[0]), GrowArrow(fba[0]), FadeIn(fab[1]), FadeIn(fba[1]))
        loi = encadre(VGroup(M(r"\vec F_{AB} = -\vec F_{BA}", size=46, color=C_FORCE),
                             T("même grandeur, sens opposés, appliquées à DEUX objets différents",
                               size=22, color=C_GRIS)).arrange(DOWN, buff=0.2)).move_to(DOWN * 2.4)
        self.play(FadeIn(loi))
        self.wait(1)
        t = ValueTracker(0)
        self.play(FadeOut(fab), FadeOut(fba))
        A.add_updater(lambda m: m.set_x(-0.6 - 1.2 * t.get_value()))
        B.add_updater(lambda m: m.set_x(0.6 + 1.2 * t.get_value()))
        self.play(t.animate.set_value(3.5), run_time=3, rate_func=linear)
        A.clear_updaters()
        B.clear_updaters()
        q = T("B pousse A… et A repousse B : les deux reculent.", size=24, color=ACCENT).move_to(UP * 2.2)
        self.play(FadeIn(q))
        self.wait(3)
        vider(self)

        # --- 2. Même force, accélérations différentes ---------------------------------------------
        self.next_section("pomme-terre")
        titre = bandeau("Erreur 1 : « même force, donc même effet »")
        self.play(FadeIn(titre))
        terre = Circle(radius=1.6, color=C_POS, fill_opacity=0.3).move_to(LEFT * 3.6 + DOWN * 1.9)
        pomme = Circle(radius=0.2, color=C_NEG, fill_opacity=0.9).move_to(terre.get_top() + UP * 2.4)
        f1 = force(pomme.get_center() + DOWN * 0.2, DOWN * 0.8, r"\vec F", direction=RIGHT)
        f2 = force(terre.get_top(), UP * 0.8, r"-\vec F", direction=RIGHT)
        self.play(FadeIn(terre), FadeIn(pomme), FadeIn(T("Terre ≈ 10²⁵ kg", size=22).move_to(terre)),
                  FadeIn(T("pomme ≈ 0,1 kg", size=20).next_to(pomme, LEFT, buff=0.2)))
        self.play(GrowArrow(f1[0]), GrowArrow(f2[0]), FadeIn(f1[1]), FadeIn(f2[1]))
        calc = VGroup(
            T("même force sur les deux (3e loi), mais a = F / m :", size=22, color=C_GRIS),
            M(r"a_{\text{pomme}} \approx 9{,}8\ \mathrm{m/s^2}", size=34, color=C_ACC),
            M(r"a_{\text{Terre}} \approx \frac{1}{10^{26}} \times 9{,}8 \approx 10^{-25}\ \mathrm{m/s^2}",
              size=34, color=C_ACC),
            T("→ seule la pomme semble bouger", size=24, color=ACCENT),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.0 + UP * 0.3)
        limiter(calc, 7.0)
        for c in calc:
            self.play(FadeIn(c, shift=UP * 0.1))
            self.wait(0.7)
        lanceur = T("Idem pour un projectile lancé : il accélère à cause des forces QU'IL subit,\n"
                    "la force qu'il exerce sur la main ne compte pas pour lui.", size=20, color=C_GRIS)
        lanceur.to_edge(DOWN, buff=0.3)
        limiter(lanceur, 13)
        self.play(FadeIn(lanceur))
        self.wait(4)
        vider(self)

        # --- 3. La pomme sur la table ----------------------------------------------------------------
        self.next_section("pomme-table")
        titre = bandeau("Erreur 3 : se tromper de paire", "une pomme posée sur une table, sur la Terre")
        self.play(FadeIn(titre))
        # objets séparés (vue « éclatée ») pour dessiner chaque force sur SON objet
        pomme = Circle(radius=0.35, color=C_NEG, fill_opacity=0.9).move_to(LEFT * 4.2 + UP * 1.0)
        table = Rectangle(width=2.6, height=0.3, color=C_SOL, fill_opacity=1, stroke_width=0)
        table.move_to(LEFT * 4.2 + DOWN * 0.5)
        terre = Arc(radius=6, start_angle=PI / 2 - 0.3, angle=0.6, color=C_POS, stroke_width=10)
        terre.move_to(LEFT * 4.2 + DOWN * 2.6)
        noms = VGroup(T("pomme", size=20).next_to(pomme, LEFT, buff=0.15),
                      T("table", size=20).next_to(table, LEFT, buff=0.15),
                      T("Terre", size=20, color=C_POS).next_to(terre, LEFT, buff=0.1))
        self.play(FadeIn(pomme), FadeIn(table), Create(terre), FadeIn(noms))
        cp = pomme.get_center()
        c_grav, c_cont = C_FORCE, ACCENT
        P_pT = force(cp + LEFT * 0.15, DOWN * 1.1, r"\vec P_{pT}", color=c_grav, direction=LEFT, size=26)
        N_pt = force(cp + RIGHT * 0.15, UP * 1.1, r"\vec N_{pt}", color=c_cont, direction=RIGHT, size=26)
        N_tp = force(table.get_top() + RIGHT * 0.6, DOWN * 0.9, r"\vec N_{tp}", color=c_cont, direction=RIGHT, size=26)
        P_Tp = force(terre.get_top() + RIGHT * 1.6, UP * 0.9, r"\vec P_{Tp}", color=c_grav, direction=RIGHT, size=26)
        self.play(*[GrowArrow(f[0]) for f in (P_pT, N_pt, N_tp, P_Tp)],
                  *[FadeIn(f[1]) for f in (P_pT, N_pt, N_tp, P_Tp)])
        paires = VGroup(
            T("Paire 1 (gravitation, à distance) :", size=22, color=c_grav),
            M(r"\vec P_{Tp} = -\vec P_{pT}", size=32, color=c_grav),
            T("Paire 2 (contact) :", size=22, color=c_cont),
            M(r"\vec N_{tp} = -\vec N_{pt}", size=32, color=c_cont),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 2.8 + UP * 1.4)
        self.play(FadeIn(paires[:2]), Indicate(P_pT, color=c_grav), Indicate(P_Tp, color=c_grav))
        self.play(FadeIn(paires[2:]), Indicate(N_pt, color=c_cont), Indicate(N_tp, color=c_cont))
        self.wait(2)
        piege = encadre(VGroup(
            T("P_pT et N_pt : égales et opposées (pomme au repos)…", size=24),
            T("…mais PAS une paire action-réaction :", size=24, color=C_NEG),
            T("même objet, et natures différentes.", size=24, color=C_NEG),
            T("Une paire = 2 objets différents, même nature.", size=24, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14), color=C_NEG)
        limiter(piege, 8.0).move_to(RIGHT * 2.6 + DOWN * 1.7)
        self.play(FadeIn(piege), Indicate(VGroup(P_pT, N_pt), color=C_NEG))
        self.wait(5)
        vider(self)
