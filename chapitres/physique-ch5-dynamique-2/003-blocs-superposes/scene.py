"""5.1 — Exemple 1 : deux blocs superposés (m1 = 2 kg sur m2 = 4 kg), sol sans frottement,
μs = 0,4 et μc = 0,2 entre les blocs. Force F0 sur le bloc du bas.

(a) F0 = 20 N : pas de glissement, a = 3,33 m/s²
(b) F0 = 30 N : il faudrait f = 10 N > f_s(max) = 7,84 N -> glissement
(c) F0 = 40 N : a1 = 1,96 m/s², a2 = 9,02 m/s²

    python -m manim -pql chapitres/physique-ch5-dynamique-2/003-blocs-superposes/scene.py BlocsSuperposes
"""

from shared.physique import *

m1, m2, g, MUS, MUC = 2.0, 4.0, 9.8, 0.4, 0.2
FSMAX = MUS * m1 * g
FC = MUC * m1 * g
Y_SOL = -0.6


class BlocsSuperposes(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 5 · section 5.1 · exemple 1", "Deux blocs superposés",
                    "Qui entraîne le bloc du dessus ? Le frottement !")
        titre = bandeau("On tire sur le bloc du bas", "m₁ = 2 kg sur m₂ = 4 kg ; sol sans frottement ; μs = 0,4 et μc = 0,2 entre les blocs")
        self.play(FadeIn(titre))
        sol = Line([-6.8, Y_SOL, 0], [6.8, Y_SOL, 0], color=PRIMARY, stroke_width=4).set_opacity(0.6)
        x2 = ValueTracker(-4.0)
        x1 = ValueTracker(-3.35)  # bloc du haut posé vers l'avant du bloc du bas
        b2 = always_redraw(lambda: bloc(r"m_2", 2.6, 0.9, color=ACCENT).move_to([x2.get_value(), Y_SOL + 0.45, 0]))
        b1 = always_redraw(lambda: bloc(r"m_1", 1.2, 0.7, color=PRIMARY).move_to([x1.get_value(), Y_SOL + 0.9 + 0.35, 0]))
        F0 = ValueTracker(20)
        f0 = always_redraw(lambda: fleche(b2.get_right(), b2.get_right() + RIGHT * 0.05 * F0.get_value(), C_FORCE, width=7))
        lf0 = always_redraw(lambda: M(r"\vec F_0", size=28, color=C_FORCE).next_to(f0, UP, buff=0.05))
        self.play(Create(sol), FadeIn(b2), FadeIn(b1))
        self.play(GrowArrow(f0), FadeIn(lf0))

        # --- Qui pousse m1 ? -----------------------------------------------------------------
        self.next_section("diagramme")
        q = T("Le bloc du haut n'est pas tiré. Pourquoi avance-t-il ?", size=24, color=ACCENT).move_to(UP * 2.3)
        self.play(FadeIn(q))
        self.wait(1)
        f1 = fleche(b1.get_bottom() + UP * 0.12 + LEFT * 0.1, b1.get_bottom() + UP * 0.12 + RIGHT * 0.9, ACCENT, width=6)
        lf1 = M(r"\vec f_1", size=28, color=ACCENT).next_to(f1, UP, buff=0.02)
        f2 = fleche(b2.get_top() + DOWN * 0.15 + RIGHT * 0.1, b2.get_top() + DOWN * 0.15 + LEFT * 0.9, ACCENT, width=6)
        lf2 = M(r"\vec f_2", size=28, color=ACCENT).next_to(f2, DOWN, buff=0.02)
        self.play(GrowArrow(f1), FadeIn(lf1))
        self.play(GrowArrow(f2), FadeIn(lf2))
        rep = VGroup(T("le frottement du bloc 2 sur le bloc 1 le TIRE vers l'avant", size=22, color=ACCENT),
                     T("et (3e loi) le bloc 1 freine le bloc 2 : |f₁| = |f₂| = f", size=22, color=C_GRIS)
                     ).arrange(DOWN, buff=0.12).next_to(q, DOWN, buff=0.2)
        self.play(FadeIn(rep))
        eqs = VGroup(M(r"\text{bloc 1 : } f = m_1 a_1", size=30), M(r"\text{bloc 2 : } F_0 - f = m_2 a_2", size=30)
                     ).arrange(RIGHT, buff=0.9).move_to(DOWN * 1.6)
        self.play(FadeIn(eqs))
        self.wait(3)
        self.play(FadeOut(VGroup(q, rep, f1, lf1, f2, lf2)))

        # --- les trois cas -------------------------------------------------------------------------
        def cas(F, lignes, glisse, duree=1.7):
            self.play(F0.animate.set_value(F), x1.animate.set_value(-3.35), x2.animate.set_value(-4.0), run_time=0.8)
            if glisse:
                a1, a2 = FC / m1, (F - FC) / m2
            else:
                a1 = a2 = F / (m1 + m2)
            t = ValueTracker(0)
            x1.add_updater(lambda m: m.set_value(-3.35 + 0.5 * 0.12 * a1 * t.get_value() ** 2))
            x2.add_updater(lambda m: m.set_value(-4.0 + 0.5 * 0.12 * a2 * t.get_value() ** 2))
            self.add(x1, x2)
            texte = VGroup(*lignes).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 2.6 + UP * 1.6)
            limiter(texte, 8.0)
            self.play(t.animate.set_value(duree), run_time=duree, rate_func=linear)
            x1.clear_updaters()
            x2.clear_updaters()
            self.play(FadeIn(texte))
            self.wait(3)
            self.play(FadeOut(texte))

        self.next_section("cas-a")
        cas(20, [T("(a) F₀ = 20 N : les blocs restent collés", size=26, color=ACCENT),
                 M(r"a = \frac{F_0}{m_1 + m_2} = \frac{20}{6} = 3{,}33\ \mathrm{m/s^2}", size=32),
                 M(r"f = m_1 a = 6{,}67\ \mathrm{N} \;<\; f_{s,max} = \mu_s m_1 g = 7{,}84\ \mathrm{N}\ \checkmark", size=28)],
            False)
        self.next_section("cas-b")
        cas(30, [T("(b) F₀ = 30 N : s'ils restaient collés…", size=26, color=ACCENT),
                 M(r"a = \frac{30}{6} = 5\ \mathrm{m/s^2} \;\Rightarrow\; f = m_1 a = 10\ \mathrm{N}", size=32),
                 M(r"10\ \mathrm{N} > 7{,}84\ \mathrm{N} \;\Rightarrow\; \text{impossible : ça glisse !}", size=30, color=C_NEG)],
            True)
        self.next_section("cas-c")
        cas(40, [T("(c) F₀ = 40 N : glissement, frottement cinétique", size=26, color=ACCENT),
                 M(r"f = \mu_c m_1 g = 3{,}92\ \mathrm{N}", size=30),
                 M(r"a_1 = \frac{3{,}92}{2} = 1{,}96\ \mathrm{m/s^2} \qquad a_2 = \frac{40 - 3{,}92}{4} = 9{,}02\ \mathrm{m/s^2}", size=30),
                 T("le bloc du haut recule par rapport à celui du bas", size=22, color=C_GRIS)],
            True)
        self.wait(1)
        vider(self)
