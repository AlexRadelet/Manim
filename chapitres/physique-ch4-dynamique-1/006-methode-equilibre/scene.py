"""4.5 — Méthode de résolution + exemple d'équilibre.

Bloc de 5 kg poussé avec 30 N à 40° sous l'horizontale ; une corde l'empêche de glisser.
-> T = 23,0 N ; N = 68,3 N.

    python -m manim -pql chapitres/physique-ch4-dynamique-1/006-methode-equilibre/scene.py MethodeEquilibre
"""

from shared.physique import *

ANG = np.radians(40)
F, P = 30.0, 49.0
T_ = F * np.cos(ANG)
N_ = P + F * np.sin(ANG)
K = 0.03  # unités écran par newton


class MethodeEquilibre(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 4 · section 4.5", "Résoudre un problème de dynamique",
                    "Une méthode en 6 étapes, toujours la même")

        # --- 1. La méthode ----------------------------------------------------------------
        self.next_section("methode")
        titre = bandeau("La méthode")
        self.play(FadeIn(titre))
        etapes = VGroup(*[T(s, size=26) for s in [
            "1.  Un schéma clair et assez grand.",
            "2.  Toutes les forces exercées SUR chaque corps par des objets extérieurs.",
            "3.  Un repère d'inertie : un axe dans le sens de l'accélération.",
            "4.  Un diagramme des forces par corps (le corps = un point).",
            "5.  La 2e loi de Newton, composante par composante.",
            "6.  Le résultat est-il plausible ? (unités, ordre de grandeur, cas limites)",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        limiter(etapes, 12.5).move_to(DOWN * 0.2)
        for e in etapes:
            self.play(FadeIn(e, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(0.6)
        cle = T("L'étape qui fait tout : le diagramme des forces (4).", size=24, color=ACCENT).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cle), Indicate(etapes[3], color=ACCENT))
        self.wait(3)
        vider(self)

        # --- 2. Le schéma ---------------------------------------------------------------------
        self.next_section("schema")
        titre = bandeau("Exemple : un bloc de 5 kg qui ne bouge pas",
                        "poussé avec 30 N à 40° sous l'horizontale ; une corde l'empêche de glisser")
        self.play(FadeIn(titre))
        table = Line(LEFT * 6.8, LEFT * 0.4, color=C_SOL, stroke_width=8).shift(DOWN * 1.6)
        mur = Rectangle(width=0.3, height=2.4, color=C_GRIS, fill_opacity=0.6, stroke_width=0)
        mur.move_to(LEFT * 0.55 + DOWN * 0.4)
        b = bloc(r"5\ \mathrm{kg}", 1.6, 1.1, size=28).next_to(table, UP, buff=0).shift(LEFT * 1.0)
        corde = Line(b.get_right(), [mur.get_left()[0], b.get_y(), 0], color=C_TEXTE, stroke_width=3)
        d = np.array([-np.cos(ANG), -np.sin(ANG), 0])
        Q = b.get_corner(UR)
        bras = fleche(Q - d * 1.8, Q, C_FORCE, width=7)
        lbras = M(r"F = 30\ \mathrm{N}", size=28, color=C_FORCE).next_to(bras.get_start(), UP, buff=0.1)
        angle = Arc(radius=0.7, start_angle=0, angle=ANG, arc_center=Q, color=ACCENT)
        horiz = DashedLine(Q, Q + RIGHT * 1.1, color=C_GRIS, stroke_width=2)
        lang = M(r"40^\circ", size=24, color=ACCENT).next_to(angle, RIGHT, buff=0.08)
        self.play(Create(table), FadeIn(mur), FadeIn(b), Create(corde))
        self.play(GrowArrow(bras), FadeIn(lbras), Create(horiz), Create(angle), FadeIn(lang))
        self.wait(2)

        # --- 3. Le diagramme des forces -----------------------------------------------------------
        self.next_section("diagramme")
        O = np.array([3.8, -0.6, 0])
        axes = VGroup(Arrow(O + LEFT * 2.6, O + RIGHT * 2.6, buff=0, color=C_GRIS, stroke_width=2, tip_length=0.15),
                      Arrow(O + DOWN * 2.2, O + UP * 2.6, buff=0, color=C_GRIS, stroke_width=2, tip_length=0.15))
        lax = VGroup(M("x", size=26, color=C_GRIS).next_to(axes[0], RIGHT, buff=0.05),
                     M("y", size=26, color=C_GRIS).next_to(axes[1], UP, buff=0.05))
        pt = particule().move_to(O)
        diag_titre = T("diagramme des forces sur le bloc", size=22, color=C_GRIS).move_to(O + UP * 2.6 + LEFT * 2.4)
        self.play(FadeIn(diag_titre), Create(axes), FadeIn(lax), FadeIn(pt))
        fP = force(O, DOWN * P * K, r"\vec P", direction=RIGHT)
        fN = force(O, UP * N_ * K, r"\vec N", direction=RIGHT)
        fT = force(O, RIGHT * T_ * K, r"\vec T", direction=UP)
        fF = force(O, d * F * K, r"\vec F", direction=DOWN)
        for f in (fP, fN, fT, fF):
            self.play(GrowArrow(f[0]), FadeIn(f[1]), run_time=0.7)
        cx = DashedLine(O, O + np.array([d[0], 0, 0]) * F * K, color=C_FORCE, stroke_width=2)
        cy = DashedLine(O + np.array([d[0], 0, 0]) * F * K, O + d * F * K, color=C_FORCE, stroke_width=2)
        lcx = M(r"F\cos 40^\circ", size=22, color=C_FORCE).next_to(cx, UP, buff=0.08)
        lcy = M(r"F\sin 40^\circ", size=22, color=C_FORCE).next_to(cy, LEFT, buff=0.08)
        self.play(Create(cx), Create(cy), FadeIn(lcx), FadeIn(lcy))
        self.wait(2)

        # --- 4. Les équations -----------------------------------------------------------------------
        self.next_section("equations")
        self.play(FadeOut(VGroup(table, mur, b, corde, bras, lbras, angle, lang, horiz)))
        eqs = VGroup(
            T("Équilibre : la somme des forces est nulle", size=22, color=C_GRIS),
            M(r"\sum F_x = T - F\cos 40^\circ = 0", size=32),
            M(r"\sum F_y = N - F\sin 40^\circ - P = 0", size=32),
            M(r"T = 30\cos 40^\circ = 23{,}0\ \mathrm{N}", size=34, color=ACCENT),
            M(r"N = 49 + 30\sin 40^\circ = 68{,}3\ \mathrm{N}", size=34, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(LEFT * 3.4 + DOWN * 0.1)
        limiter(eqs, 6.4)
        for e in eqs:
            self.play(FadeIn(e, shift=UP * 0.1))
            self.wait(0.8)
        plaus = T("Plausible ? N > P : normal, F appuie le bloc contre la table.", size=22, color=C_VIT)
        plaus.to_edge(DOWN, buff=0.3)
        limiter(plaus, 13)
        self.play(FadeIn(plaus))
        self.wait(5)
        vider(self)
