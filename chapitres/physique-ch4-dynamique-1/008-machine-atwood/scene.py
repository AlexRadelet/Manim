"""4.5 — Exemple 3 : la machine d'Atwood (m1 = 3 kg, m2 = 5 kg).

-> a = (m2 − m1) g / (m1 + m2) = 2,45 m/s² ; T = 36,8 N ; m1 g < T < m2 g.

    python -m manim -pql chapitres/physique-ch4-dynamique-1/008-machine-atwood/scene.py MachineAtwood
"""

from shared.physique import *

m1, m2, g = 3.0, 5.0, 9.8
A = (m2 - m1) * g / (m1 + m2)
T_ = m1 * (g + A)
K = 0.025


class MachineAtwood(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 4 · section 4.5 · exemple 3", "La machine d'Atwood",
                    "Deux blocs, une corde, une poulie")
        titre = bandeau("m₁ = 3 kg et m₂ = 5 kg, reliés par une corde sur une poulie",
                        "corde sans masse, poulie légère et sans frottement")
        self.play(FadeIn(titre))

        cx, cy, R = -3.6, 1.35, 0.6
        support = Line([cx - 1.2, cy + 0.95, 0], [cx + 1.2, cy + 0.95, 0], color=C_GRIS, stroke_width=6)
        attache = Line([cx, cy + 0.95, 0], [cx, cy, 0], color=C_GRIS, stroke_width=3)
        poulie = Circle(radius=R, color=C_GRIS, stroke_width=4).move_to([cx, cy, 0])
        d = ValueTracker(0)  # descente de m2 (unités écran)
        y1 = lambda: -1.5 + d.get_value()
        y2 = lambda: -1.5 - d.get_value()
        b1 = always_redraw(lambda: bloc(r"m_1", 0.9, 0.9, color=PRIMARY).move_to([cx - R, y1(), 0]))
        b2 = always_redraw(lambda: bloc(r"m_2", 1.0, 1.15, color=ACCENT).move_to([cx + R, y2(), 0]))
        c1 = always_redraw(lambda: Line([cx - R, cy, 0], [cx - R, y1() + 0.45, 0], color=C_TEXTE, stroke_width=3))
        c2 = always_redraw(lambda: Line([cx + R, cy, 0], [cx + R, y2() + 0.575, 0], color=C_TEXTE, stroke_width=3))
        self.play(Create(support), Create(attache), Create(poulie))
        self.play(FadeIn(b1), FadeIn(b2), Create(c1), Create(c2))
        q = T("Lequel descend ? Avec quelle accélération ?", size=26, color=ACCENT).move_to(RIGHT * 3.0 + UP * 1.8)
        self.play(FadeIn(q))
        self.wait()
        self.play(d.animate.set_value(1.0), run_time=2.0, rate_func=lambda x: x * x)
        self.wait()
        self.play(d.animate.set_value(0), FadeOut(q), run_time=1)

        # --- forces ---------------------------------------------------------------------------
        self.next_section("forces")
        f1T = force([cx - R - 0.15, y1() + 0.45, 0], UP * T_ * K, r"\vec T", direction=LEFT, size=26)
        f1P = force([cx - R - 0.15, y1() - 0.45, 0], DOWN * m1 * g * K, r"m_1\vec g", direction=LEFT, size=26)
        f2T = force([cx + R + 0.15, y2() + 0.575, 0], UP * T_ * K, r"\vec T{\,}'", direction=RIGHT, size=26)
        f2P = force([cx + R + 0.15, y2() - 0.575, 0], DOWN * m2 * g * K, r"m_2\vec g", direction=RIGHT, size=26)
        for f in (f1T, f1P, f2T, f2P):
            self.play(GrowArrow(f[0]), FadeIn(f[1]), run_time=0.6)
        hyp = VGroup(T("corde sans masse : T = T'", size=22),
                     T("corde inextensible : même |a| pour les deux", size=22),
                     T("m₁ monte, m₂ descend : on oriente chaque axe\ndans le sens de SON accélération", size=22, color=ACCENT)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 3.0 + UP * 1.6)
        limiter(hyp, 7.0)
        for h in hyp:
            self.play(FadeIn(h, shift=UP * 0.1))
            self.wait(0.6)
        self.wait(2)

        # --- équations ----------------------------------------------------------------------------
        self.next_section("equations")
        self.play(FadeOut(hyp))
        eqs = VGroup(
            M(r"\text{bloc 1 : } T - m_1 g = m_1 a", size=32),
            M(r"\text{bloc 2 : } m_2 g - T = m_2 a", size=32),
            T("on additionne : T disparaît", size=22, color=C_GRIS),
            M(r"a = \frac{m_2 - m_1}{m_1 + m_2}\,g = \frac{2}{8}\,9{,}8 = 2{,}45\ \mathrm{m/s^2}", size=32, color=C_ACC),
            M(r"T = m_1 (g + a) = 3 \times 12{,}25 = 36{,}8\ \mathrm{N}", size=32, color=C_FORCE),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.0 + UP * 0.6)
        limiter(eqs, 7.4)
        for e in eqs:
            self.play(FadeIn(e, shift=UP * 0.1))
            self.wait(0.7)
        verif = encadre(VGroup(
            M(r"m_1 g = 29{,}4\ \mathrm{N} \;<\; T = 36{,}8\ \mathrm{N} \;<\; m_2 g = 49\ \mathrm{N}", size=30),
            T("plausible : T soulève m₁ mais retient m₂ sans l'arrêter", size=20, color=C_GRIS),
        ).arrange(DOWN, buff=0.15), color=C_VIT)
        limiter(verif, 7.4).move_to(RIGHT * 3.0 + DOWN * 2.5)
        self.play(FadeIn(verif))
        piege = T("Piège : T ≠ m₂ g ! Si c'était le cas, m₂ ne tomberait pas.", size=22, color=C_NEG)
        limiter(piege, 7.0).move_to(RIGHT * 3.0 + DOWN * 3.55)
        self.play(FadeIn(piege))
        self.wait(5)
        vider(self)
