"""2.2 — Déplacement vs distance parcourue, vitesse moyenne vs vitesse scalaire moyenne.

Exemple du cours : la particule part de A (x = 2 m), va jusqu'à x = 9 m,
revient en B (x = 6 m), le tout en 4 s.

    manim -pql chapitres/physique-ch2-cinematique-1d/001-deplacement-distance/scene.py DeplacementDistance
"""

from shared.physique import *


class DeplacementDistance(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.2", "Déplacement ≠ distance parcourue",
                    "Deux grandeurs qui se ressemblent… mais pas du tout")

        # --- L'axe -----------------------------------------------------------
        self.next_section("axe")
        titre = bandeau("Une particule sur l'axe des x", "axe orienté positivement vers la droite")
        axe = NumberLine(x_range=[-2, 10.7, 1], length=11.8, include_numbers=True,
                         font_size=26, color=C_GRIS, include_tip=True, tip_width=0.2,
                         tip_height=0.2).shift(UP * 0.6)
        unite = M(r"x\ (\mathrm{m})", size=30, color=C_GRIS).next_to(axe, RIGHT, buff=0.15)
        self.play(FadeIn(titre), Create(axe), FadeIn(unite))

        p = lambda x: axe.n2p(x)
        bille = particule().move_to(p(2))
        lab_a = T("A", size=28, color=ACCENT).move_to(p(2) + DOWN * 0.7)
        self.play(FadeIn(bille, scale=0.5), FadeIn(lab_a))
        self.wait()

        # --- Le trajet réel --------------------------------------------------
        self.next_section("trajet")
        h1, h2 = 0.55, 1.05
        aller = fleche(p(2) + UP * h1, p(9) + UP * h1, ACCENT, width=4)
        retour = fleche(p(9) + UP * h2, p(6) + UP * h2, ACCENT, width=4)
        l_aller = T("7 m", size=26, color=ACCENT).next_to(aller, UP, buff=0.08)
        l_retour = T("3 m", size=26, color=ACCENT).next_to(retour, UP, buff=0.08)
        self.play(bille.animate.move_to(p(9)), GrowArrow(aller), run_time=2.2,
                  rate_func=smooth)
        self.play(FadeIn(l_aller))
        self.play(bille.animate.move_to(p(6)), GrowArrow(retour), run_time=1.4)
        lab_b = T("B", size=28, color=ACCENT).move_to(p(6) + DOWN * 0.7)
        self.play(FadeIn(l_retour), FadeIn(lab_b))
        self.wait()

        dist = VGroup(
            T("Distance parcourue", size=30, color=ACCENT, weight=BOLD),
            M(r"7\ \mathrm{m} + 3\ \mathrm{m} = 10\ \mathrm{m}", size=42),
            T("longueur du trajet réel\nscalaire, toujours ≥ 0", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.2).move_to(LEFT * 3.6 + DOWN * 2.5)
        self.play(FadeIn(dist[0]), Write(dist[1]))
        self.play(FadeIn(dist[2]))
        self.wait(2)

        # --- Le déplacement ---------------------------------------------------
        self.next_section("deplacement")
        dx = fleche(p(2) + DOWN * 1.1, p(6) + DOWN * 1.1, C_POS, width=7)
        l_dx = M(r"\Delta x", size=36, color=C_POS).next_to(dx, RIGHT, buff=0.15)
        self.play(GrowArrow(dx), FadeIn(l_dx))
        depl = VGroup(
            T("Déplacement", size=30, color=C_POS, weight=BOLD),
            M(r"\Delta x = x_f - x_i = 6 - 2 = +4\ \mathrm{m}", size=42),
            T("seulement départ → arrivée\nvecteur : le signe donne le sens", size=22,
              color=C_GRIS),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.4 + DOWN * 2.5)
        self.play(FadeIn(depl[0]), Write(depl[1]))
        self.play(FadeIn(depl[2]))
        self.wait(1)
        neq = M(r"10\ \mathrm{m} \neq 4\ \mathrm{m}", size=44, color=ACCENT)
        neq.move_to(DOWN * 3.6)
        self.play(Write(neq))
        self.wait(3)

        # --- Les deux vitesses moyennes -------------------------------------
        self.next_section("vitesses")
        self.play(FadeOut(VGroup(dist, depl, neq)))
        duree = T("Le trajet de A à B dure Δt = 4 s", size=28).move_to(DOWN * 1.45)
        self.play(FadeIn(duree))
        vs = VGroup(
            T("Vitesse scalaire moyenne", size=26, color=ACCENT, weight=BOLD),
            M(r"\frac{\text{distance}}{\Delta t} = \frac{10\ \mathrm{m}}{4\ \mathrm{s}}"
              r" = 2{,}5\ \mathrm{m/s}", size=40),
            T("toujours positive", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.2)
        vm = VGroup(
            T("Vitesse moyenne (selon x)", size=26, color=C_VIT, weight=BOLD),
            M(r"v_{x\,\mathrm{moy}} = \frac{\Delta x}{\Delta t} = \frac{+4\ \mathrm{m}}{4\ \mathrm{s}}"
              r" = +1\ \mathrm{m/s}", size=40),
            T("même signe que Δx → indique le sens", size=22, color=C_GRIS),
        ).arrange(DOWN, buff=0.2)
        VGroup(vs, vm).arrange(RIGHT, buff=1.0).move_to(DOWN * 2.95)
        limiter(VGroup(vs, vm), 13.4)
        self.play(FadeIn(vs[0]), Write(vs[1]))
        self.play(FadeIn(vs[2]))
        self.wait()
        self.play(FadeIn(vm[0]), Write(vm[1]))
        self.play(FadeIn(vm[2]))
        self.wait(4)

        # --- Cas particulier : retour au point de départ ---------------------
        self.next_section("retour")
        self.play(FadeOut(VGroup(duree, vs, vm, aller, retour, l_aller, l_retour, dx, l_dx,
                                 lab_b)))
        sous = T("Et si la particule revient à son point de départ ?", size=28,
                 color=ACCENT).move_to(DOWN * 1.7)
        self.play(FadeIn(sous), bille.animate.move_to(p(2)))
        aller2 = fleche(p(2) + UP * h1, p(8) + UP * h1, ACCENT, width=4)
        retour2 = fleche(p(8) + UP * h2, p(2) + UP * h2, ACCENT, width=4)
        self.play(bille.animate.move_to(p(8)), GrowArrow(aller2), run_time=1.8)
        self.play(bille.animate.move_to(p(2)), GrowArrow(retour2), run_time=1.8)
        res = VGroup(
            M(r"\text{distance} = 6 + 6 = 12\ \mathrm{m}", size=38, color=ACCENT),
            M(r"\Delta x = 2 - 2 = 0\ \mathrm{m}", size=38, color=C_POS),
            M(r"\Rightarrow\ v_{x\,\mathrm{moy}} = 0", size=42, color=C_VIT),
        ).arrange(RIGHT, buff=0.8).move_to(DOWN * 2.6)
        for r in res:
            self.play(Write(r))
        self.wait(1)
        conclu = T("On a beaucoup roulé… mais en moyenne, on n'est allé nulle part !",
                   size=24, color=C_GRIS).move_to(DOWN * 3.3)
        self.play(FadeIn(conclu))
        self.wait(4)
        vider(self)
