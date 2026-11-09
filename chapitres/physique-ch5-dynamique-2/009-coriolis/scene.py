"""5.4 — Vitesse angulaire et force de Coriolis.

Une rondelle est lancée sans frottement depuis le centre d'un disque qui tourne (sens antihoraire)
vers une personne P au bord. Vue du sol : ligne droite. Vue du disque : trajectoire courbée vers la DROITE.
a_Coriolis = 2 ω v (perpendiculaire à v).

    python -m manim -pql chapitres/physique-ch5-dynamique-2/009-coriolis/scene.py Coriolis
"""

from shared.physique import *

W = 0.55     # ω (rad/s, unités d'écran)
R = 2.4
V = 1.0
T_FIN = R / V


def u(a):
    return np.array([np.cos(a), np.sin(a), 0])


class Coriolis(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 5 · section 5.4", "La force de Coriolis",
                    "Lancer droit sur un manège… et rater sa cible")

        # --- 1. Vitesse angulaire -------------------------------------------------------------
        self.next_section("omega")
        titre = bandeau("D'abord : la vitesse angulaire ω")
        self.play(FadeIn(titre))
        C = LEFT * 3.4 + DOWN * 0.5
        cercle = Circle(radius=2.0, color=C_GRIS).move_to(C)
        ang = ValueTracker(0.3)
        rayon = always_redraw(lambda: Line(C, C + 2.0 * u(ang.get_value()), color=C_TEXTE))
        ray0 = Line(C, C + 2.0 * u(0.3), color=C_GRIS, stroke_width=2)
        balayage = always_redraw(lambda: Sector(radius=2.0, start_angle=0.3, angle=ang.get_value() - 0.3 + 1e-4,
                                                arc_center=C, color=ACCENT, fill_opacity=0.25, stroke_width=0))
        arc = always_redraw(lambda: Arc(radius=2.0, start_angle=0.3, angle=ang.get_value() - 0.3 + 1e-4, arc_center=C,
                                        color=ACCENT, stroke_width=6))
        self.play(Create(cercle), Create(ray0), FadeIn(rayon))
        self.add(balayage, arc)
        self.play(ang.animate.set_value(1.5), run_time=2.5, rate_func=linear)
        ls = M("s", size=30, color=ACCENT).move_to(C + 2.35 * u(0.9))
        lth = M(r"\Delta\theta", size=28, color=ACCENT).move_to(C + 0.8 * u(0.9))
        self.play(FadeIn(ls), FadeIn(lth))
        eqs = VGroup(M(r"|\Delta\theta| = \frac{s}{r}\ \ (\mathrm{rad})", size=34),
                     M(r"\omega = \frac{|\Delta\theta|}{\Delta t}\ \ (\mathrm{rad/s})", size=34),
                     M(r"v = \omega\, r", size=44, color=C_VIT)).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.4)
        for e in eqs:
            self.play(FadeIn(e, shift=UP * 0.1))
            self.wait(0.6)
        note = T("même ω pour tous les points du disque,\nmais plus on est loin du centre, plus v est grand",
                 size=20, color=C_GRIS).next_to(eqs, DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(3)
        vider(self)

        # --- 2. Deux points de vue ----------------------------------------------------------------
        self.next_section("deux-vues")
        titre = bandeau("La rondelle lancée vers P", "disque tournant dans le sens antihoraire, sans frottement")
        self.play(FadeIn(titre))
        sep = Line(UP * 2.9, DOWN * 3.9, color=C_GRIS, stroke_width=2)
        tg = T("vue du sol (inertiel)", size=24, color=C_VIT).move_to([-3.55, 2.45, 0])
        td = T("vue du disque (tournant)", size=24, color=C_NEG).move_to([3.55, 2.45, 0])
        self.play(Create(sep), FadeIn(tg), FadeIn(td))
        Cg, Cd = np.array([-3.55, -0.75, 0]), np.array([3.55, -0.75, 0])
        t = ValueTracker(0)

        def disque(c, a):
            return VGroup(Circle(radius=R, color=C_GRIS, fill_opacity=0.08),
                          *[Line(ORIGIN, R * u(k * PI / 4), color=C_GRIS, stroke_width=1) for k in range(8)]
                          ).move_to(c).rotate(a, about_point=c)

        dg = always_redraw(lambda: disque(Cg, W * t.get_value()))
        dd = disque(Cd, 0)
        Pg = always_redraw(lambda: VGroup(Dot(Cg + R * u(PI / 2 + W * t.get_value()), radius=0.13, color=C_POS),
                                          T("P", size=22, color=C_POS).move_to(Cg + (R + 0.3) * u(PI / 2 + W * t.get_value()))))
        Pd = VGroup(Dot(Cd + R * UP, radius=0.13, color=C_POS), T("P", size=22, color=C_POS).move_to(Cd + (R + 0.3) * UP))
        rg = always_redraw(lambda: Dot(Cg + V * t.get_value() * UP, radius=0.1, color=ACCENT).set_z_index(3))
        rd = always_redraw(lambda: Dot(Cd + V * t.get_value() * u(PI / 2 - W * t.get_value()), radius=0.1, color=ACCENT).set_z_index(3))
        trg = TracedPath(rg.get_center, stroke_color=ACCENT, stroke_width=4)
        trd = TracedPath(rd.get_center, stroke_color=ACCENT, stroke_width=4)
        self.play(FadeIn(dg), FadeIn(dd), FadeIn(Pg), FadeIn(Pd), FadeIn(rg), FadeIn(rd))
        self.add(trg, trd)
        self.play(t.animate.set_value(T_FIN), run_time=4, rate_func=linear)
        cg = T("ligne droite (aucune force)…\nmais P a tourné entre-temps", size=20, color=C_VIT).move_to([-3.55, -3.55, 0])
        cd = T("trajectoire déviée vers la DROITE :\nforce de Coriolis (fictive)", size=20, color=C_NEG).move_to([3.55, -3.55, 0])
        self.play(FadeIn(cg), FadeIn(cd))
        self.wait(4)
        vider(self)

        # --- 3. La formule et les exemples ------------------------------------------------------------
        self.next_section("formule")
        titre = bandeau("Combien dévie-t-elle ?")
        self.play(FadeIn(titre))
        eqs = VGroup(
            T("pendant t' = R / v', le point P parcourt s = ω R t'", size=24, color=C_GRIS),
            T("vu du disque, tout se passe comme une accélération a' perpendiculaire à v :", size=24, color=C_GRIS),
            M(r"s \approx \tfrac12 a' t'^2 \;\Rightarrow\; a' = 2\,\omega\, v", size=44, color=C_ACC),
            T("disque antihoraire → déviation vers la droite ; horaire → vers la gauche", size=24),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.6)
        limiter(eqs, 12.8)
        for e in eqs:
            self.play(FadeIn(e, shift=UP * 0.1))
            self.wait(0.8)
        ex = T("Sur Terre (qui tourne) : déviation des tirs à longue portée, et des vents\n"
               "→ sens de rotation des cyclones, opposé dans les deux hémisphères.", size=22, color=ACCENT)
        ex.to_edge(DOWN, buff=0.9)
        limiter(ex, 12.8)
        self.play(FadeIn(ex))
        resume = T("Dans un référentiel tournant : a = a' + 2ωv' + ω²R  (Coriolis + centrifuge)",
                   size=20, color=C_GRIS).to_edge(DOWN, buff=0.3)
        limiter(resume, 12.8)
        self.play(FadeIn(resume))
        self.wait(5)
        vider(self)
