"""4.6 — Le poids apparent : une personne de 70 kg sur une balance dans un ascenseur.

N = m (g + a_y) : 686 N au repos, 826 N en accélérant vers le haut, 546 N en freinant,
0 N si le câble casse (chute libre).

    python -m manim -pql chapitres/physique-ch4-dynamique-1/009-poids-apparent/scene.py PoidsApparent
"""

from shared.physique import *

m, g = 70.0, 9.8
K = 0.0022  # unités écran par newton
PHASES = [
    # (texte, a_y réelle (m/s²), a écran, durée)
    ("ascenseur au repos", 0.0, 0.0, 1.8),
    ("démarre vers le haut : a = +2 m/s²", 2.0, 0.2, 2.2),
    ("monte à vitesse constante", 0.0, 0.0, 2.0),
    ("freine en montant : a = −2 m/s²", -2.0, -0.2, 2.2),
    ("le câble casse : chute libre, a = −g", -g, -1.0, 1.6),
]


class PoidsApparent(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 4 · section 4.6", "Le poids apparent",
                    "Pourquoi on se sent plus lourd quand l'ascenseur démarre")
        titre = bandeau("Une personne de 70 kg sur une balance, dans un ascenseur")
        self.play(FadeIn(titre))

        etat = {"a_reel": 0.0}
        horloge = ValueTracker(0)
        Y0 = -1.6

        def y_cabine(t):
            """Position de la cabine : intégration exacte, phase par phase."""
            y, v = Y0, 0.0
            for _, _, a, d in PHASES:
                dt = min(max(t, 0.0), d)
                y += v * dt + 0.5 * a * dt * dt
                v += a * dt
                t -= d
                if t <= 0:
                    break
            return y

        cab = VGroup(Rectangle(width=2.4, height=3.2, color=C_GRIS, stroke_width=4))
        balance = Rectangle(width=1.1, height=0.18, color=C_TEXTE, fill_opacity=0.8, stroke_width=0)
        perso = VGroup(Circle(radius=0.2, color=ACCENT, fill_opacity=0.8),
                       RoundedRectangle(width=0.5, height=1.0, corner_radius=0.15, color=ACCENT, fill_opacity=0.6))
        perso.arrange(DOWN, buff=0.05)
        cable = Line(UP * 4.2, UP * 1.6, color=C_TEXTE, stroke_width=3)

        def flotte():
            return 0.25 if etat["a_reel"] <= -g + 1e-6 else 0.0

        X = -3.4

        def cabine():
            y = y_cabine(horloge.get_value())
            c = cab.copy().move_to([X, y, 0])
            bal = balance.copy().move_to([X, y - 1.5, 0])
            p = perso.copy().next_to(bal, UP, buff=0.02 + flotte())
            gr = VGroup(c, bal, p)
            if etat["a_reel"] > -g + 1e-6:
                gr.add(cable.copy().put_start_and_end_on([X, 3.0, 0], [X, y + 1.6, 0]))
            N = m * (g + etat["a_reel"])
            pc = p.get_center()
            gr.add(fleche(pc + LEFT * 0.45, pc + LEFT * 0.45 + DOWN * m * g * K, C_FORCE, width=5))
            if N > 1:
                gr.add(fleche(pc + RIGHT * 0.45 + DOWN * 0.6, pc + RIGHT * 0.45 + DOWN * 0.6 + UP * N * K, C_FORCE, width=5))
            if abs(etat["a_reel"]) > 0.01:
                gr.add(fleche(c.get_right() + RIGHT * 0.4, c.get_right() + RIGHT * 0.4 + UP * (0.25 * etat["a_reel"] if abs(etat["a_reel"]) < 5 else -1.3), C_ACC, width=6))
            return gr

        scene_cab = always_redraw(cabine)
        leg = VGroup(M(r"m\vec g", size=28, color=C_FORCE), M(r"\vec N", size=28, color=C_FORCE),
                     M(r"\vec a", size=28, color=C_ACC)).arrange(RIGHT, buff=0.6).move_to([X, -3.6, 0])
        self.add(scene_cab)
        self.play(FadeIn(leg))

        affiche = Compteur(r"\text{balance : } N =", lambda: m * (g + etat["a_reel"]), r"\mathrm{N}",
                           decimales=0, size=36, couleur_nombre=C_FORCE)
        affiche.move_to(RIGHT * 3.0 + UP * 2.1)
        formule = encadre(VGroup(M(r"N - mg = m a_y", size=36), M(r"N = m\,(g + a_y)", size=40, color=C_FORCE))
                          .arrange(DOWN, buff=0.2)).move_to(RIGHT * 3.0 + DOWN * 0.1)
        info = T("la balance affiche N, la force qu'elle exerce :\nc'est le poids APPARENT. Le vrai poids mg = 686 N ne change pas.",
                 size=20, color=C_GRIS).move_to(RIGHT * 3.0 + DOWN * 1.7)
        limiter(info, 7.2)
        self.play(FadeIn(affiche), FadeIn(formule), FadeIn(info))
        phase_txt = T(PHASES[0][0], size=26, color=ACCENT).move_to(RIGHT * 3.0 + DOWN * 2.8)
        self.play(FadeIn(phase_txt))
        for k, (txt, a_reel, a_ecran, duree) in enumerate(PHASES):
            if k > 0:
                nouveau = T(txt, size=26, color=C_NEG if a_reel <= -g else ACCENT).move_to(RIGHT * 3.0 + DOWN * 2.8)
                limiter(nouveau, 7.2)
                self.play(ReplacementTransform(phase_txt, nouveau), run_time=0.4)
                phase_txt = nouveau
            etat["a_reel"] = a_reel
            self.play(horloge.animate.set_value(horloge.get_value() + duree), run_time=duree, rate_func=linear)
            self.wait(1.2)
        apesanteur = T("N = 0 : la personne « flotte ».\nC'est l'apesanteur des astronautes en orbite (chapitre 5).",
                       size=22, color=C_NEG).move_to(RIGHT * 3.0 + DOWN * 2.8)
        limiter(apesanteur, 7.2)
        self.play(ReplacementTransform(phase_txt, apesanteur))
        self.wait(5)
        vider(self)
