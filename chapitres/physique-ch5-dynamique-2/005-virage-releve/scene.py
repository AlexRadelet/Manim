"""5.2 — Exemple 3 : le virage relevé (vue en coupe).

(a) Vitesse maximale avec frottement : v² = r g (tan θ + μs) / (1 − μs tan θ)
    r = 900 m, θ = 6° : μs = 0,1 -> 154 km/h ; 0,5 -> 270 km/h ; 0,8 -> 336 km/h
(b) Sans frottement : tan θ = v² / (r g) ; 108 km/h sur r = 900 m -> θ = 6°.
L'angle est EXAGÉRÉ sur le dessin (20°) pour la lisibilité.

    python -m manim -pql chapitres/physique-ch5-dynamique-2/005-virage-releve/scene.py VirageReleve
"""

from shared.physique import *

TH = np.radians(20)  # dessin seulement


class VirageReleve(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 5 · section 5.2 · exemple 3", "Le virage relevé",
                    "Pourquoi les virages d'autoroute sont inclinés")

        # --- 1. Le schéma en coupe -------------------------------------------------------------
        self.next_section("schema")
        titre = bandeau("Un virage relevé, vu en coupe",
                        "le centre du virage est à gauche ; angle exagéré sur le dessin")
        self.play(FadeIn(titre))
        P0 = np.array([-6.4, -2.6, 0])
        L = 6.6
        u = np.array([np.cos(TH), np.sin(TH), 0])
        n = np.array([-np.sin(TH), np.cos(TH), 0])
        route = Polygon(P0, P0 + L * u, np.array([P0[0] + L * np.cos(TH), P0[1], 0]),
                        color=C_SOL, fill_opacity=0.5, stroke_width=0)
        C = P0 + u * 3.6 + n * 0.32
        auto = VGroup(Rectangle(width=1.3, height=0.45, color=PRIMARY, fill_opacity=0.8),
                      RoundedRectangle(width=0.7, height=0.3, corner_radius=0.08, color=PRIMARY, fill_opacity=0.8).shift(UP * 0.33)
                      ).rotate(TH).move_to(C)
        centre = T("← centre du virage", size=22, color=C_GRIS).move_to(LEFT * 4.9 + UP * 1.4)
        arc = Arc(radius=1.0, start_angle=0, angle=TH, arc_center=P0, color=ACCENT)
        lth = M(r"\theta", size=28, color=ACCENT).move_to(P0 + 1.3 * np.array([np.cos(TH / 2), np.sin(TH / 2), 0]))
        self.play(FadeIn(route), FadeIn(auto), FadeIn(centre), Create(arc), FadeIn(lth))
        q = T("À grande vitesse, la voiture a tendance à glisser vers le HAUT (l'extérieur) :\n"
              "le frottement est donc dirigé vers le BAS de la pente.", size=20, color=ACCENT)
        q.move_to(RIGHT * 3.0 + UP * 2.4)
        limiter(q, 7.6)
        self.play(FadeIn(q))
        fP = force(C, DOWN * 1.6, r"m\vec g", direction=RIGHT)
        fN = force(C, n * 1.9, r"\vec N", direction=UP)
        fF = force(C - n * 0.32, -u * 1.0, r"\vec f", color=ACCENT, direction=DOWN)
        for f in (fP, fN, fF):
            self.play(GrowArrow(f[0]), FadeIn(f[1]), run_time=0.7)
        axes = VGroup(DashedLine(C + RIGHT * 1.0, C + LEFT * 2.6, color=C_GRIS, stroke_width=2),
                      DashedLine(C + DOWN * 2.0, C + UP * 2.4, color=C_GRIS, stroke_width=2))
        lax = VGroup(M("x", size=26, color=C_GRIS).next_to(C + LEFT * 2.6, LEFT, buff=0.05),
                     M("y", size=26, color=C_GRIS).next_to(C + UP * 2.4, UP, buff=0.05))
        note = T("axe x HORIZONTAL vers le centre (c'est là qu'est l'accélération),\npas le long de la pente !",
                 size=20, color=C_VIT).next_to(q, DOWN, buff=0.3)
        limiter(note, 7.6)
        self.play(Create(axes), FadeIn(lax), FadeIn(note))
        self.wait(3)

        # --- 2. Les équations ---------------------------------------------------------------------
        self.next_section("equations")
        self.play(FadeOut(q), FadeOut(note))
        eqs = VGroup(
            M(r"\sum F_x = N\sin\theta + f\cos\theta = \frac{m v^2}{r}", size=30),
            M(r"\sum F_y = N\cos\theta - f\sin\theta - m g = 0", size=30),
            T("vitesse maximale : f = f_s(max) = μs N", size=20, color=C_GRIS),
            M(r"v_{max}^2 = r g\,\frac{\tan\theta + \mu_s}{1 - \mu_s\tan\theta}", size=36, color=ACCENT),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.4 + UP * 1.3)
        limiter(eqs, 6.6)
        for e in eqs:
            self.play(FadeIn(e, shift=UP * 0.1))
            self.wait(0.7)
        tab = VGroup(
            T("r = 900 m, θ = 6°", size=22, color=C_GRIS),
            M(r"\mu_s = 0{,}1 \;\rightarrow\; 154\ \mathrm{km/h}", size=28),
            M(r"\mu_s = 0{,}5 \;\rightarrow\; 270\ \mathrm{km/h}", size=28),
            M(r"\mu_s = 0{,}8 \;\rightarrow\; 336\ \mathrm{km/h}", size=28),
        ).arrange(DOWN, buff=0.15)
        tab = encadre(tab, color=C_GRIS).move_to(RIGHT * 1.9 + DOWN * 2.2)
        self.play(FadeIn(tab))
        self.wait(3)
        sans = VGroup(T("(b) sans frottement :", size=22, color=ACCENT),
                      M(r"\tan\theta = \frac{v^2}{r g}", size=34),
                      T("108 km/h, r = 900 m → θ = 6°", size=20, color=C_GRIS)).arrange(DOWN, buff=0.15)
        limiter(sans, 3.0).move_to(RIGHT * 5.3 + DOWN * 2.2)
        self.play(FadeIn(sans))
        self.wait(5)
        vider(self)
