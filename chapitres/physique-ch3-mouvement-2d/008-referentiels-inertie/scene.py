"""3.6 — Les référentiels d'inertie.

Un wagon roule à vitesse constante, une balle est posée dedans (sans frottement).
1. Vu depuis la route (S) : balle et wagon avancent à +u, l'arbre est immobile.
2. Vu depuis le wagon (S') : balle immobile, l'arbre recule à −u.
   -> dans les deux, rien n'accélère sans force : S et S' sont inertiels.
3. Le wagon freine : dans S', la balle part vers l'avant SANS force -> S' n'est plus inertiel.
   Dans S, rien d'étrange : la balle continue simplement à +u (1re loi).

    manim -pql chapitres/physique-ch3-mouvement-2d/008-referentiels-inertie/scene.py ReferentielsInertie
"""

from shared.physique import *

U = 1.5          # vitesse du wagon (unités écran / s)
X0 = -4.0        # position initiale du wagon (monde)
T_FREIN = 7.0    # début du freinage
B = 1.0          # décélération
DEMI = 1.75      # demi-longueur du wagon
R_B = 0.2        # rayon de la balle
Y_SOL, Y_PLANCHER = -2.2, -1.75


def x_wagon(t):
    if t <= T_FREIN:
        return X0 + U * t
    tau = min(t - T_FREIN, U / B)
    return X0 + U * T_FREIN + U * tau - 0.5 * B * tau * tau


def x_balle(t):
    """Pas de frottement : la balle garde +u jusqu'à toucher la paroi avant."""
    if t <= T_FREIN:
        return x_wagon(t)
    libre = X0 + U * t
    butee = x_wagon(t) + DEMI - R_B - 0.08
    return min(libre, butee)


class ReferentielsInertie(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.6", "Les référentiels d'inertie",
                    "Mouvement ou repos… par rapport à quoi ?")

        t = ValueTracker(0)
        vue = ValueTracker(0)  # 0 = vu de la route (S), 1 = vu du wagon (S')
        decal = ValueTracker(0)  # recadrage de la caméra « route » (pour garder le wagon à l'écran)

        def ecran(x_monde):
            return (x_monde - vue.get_value() * x_wagon(t.get_value())
                    - (1 - vue.get_value()) * decal.get_value())

        sol = Line([-7.2, Y_SOL, 0], [7.2, Y_SOL, 0], color=C_SOL, stroke_width=6)

        def arbres():
            g = VGroup()
            for xm in np.arange(-30, 60, 3.2):
                xs = ecran(xm)
                if -7.6 < xs < 7.6:
                    tronc = Rectangle(width=0.15, height=0.5, color=C_SOL, fill_opacity=1,
                                      stroke_width=0).move_to([xs, Y_SOL + 0.25, 0])
                    feuil = Triangle(color=C_VIT, fill_opacity=0.7, stroke_width=0)
                    feuil.scale(0.55).move_to([xs, Y_SOL + 0.95, 0])
                    g.add(tronc, feuil)
            return g

        def wagon():
            xs = ecran(x_wagon(t.get_value()))
            caisse = Rectangle(width=2 * DEMI, height=1.1, stroke_width=0, fill_color=BACKGROUND,
                               fill_opacity=1).move_to([xs, Y_PLANCHER + 0.55, 0])
            plancher = Line([xs - DEMI, Y_PLANCHER, 0], [xs + DEMI, Y_PLANCHER, 0], color=C_POS,
                            stroke_width=6)
            av = Line([xs + DEMI, Y_PLANCHER, 0], [xs + DEMI, Y_PLANCHER + 1.1, 0], color=C_POS,
                      stroke_width=6)
            ar = Line([xs - DEMI, Y_PLANCHER, 0], [xs - DEMI, Y_PLANCHER + 1.1, 0], color=C_POS,
                      stroke_width=6)
            roues = VGroup(*[Circle(radius=0.18, color=C_GRIS, stroke_width=4)
                             .move_to([xs + d, Y_SOL + 0.2, 0]) for d in (-1.1, 1.1)])
            return VGroup(caisse, plancher, av, ar, roues)

        balle = always_redraw(lambda: Circle(radius=R_B, color=ACCENT, fill_opacity=1)
                              .move_to([ecran(x_balle(t.get_value())), Y_PLANCHER + R_B + 0.03, 0]))
        arb = always_redraw(arbres)
        wag = always_redraw(wagon)

        etiquette_vue = always_redraw(lambda: T(
            "Vu depuis la ROUTE (référentiel S)" if vue.get_value() < 0.5
            else "Vu depuis le WAGON (référentiel S')", size=26,
            color=ACCENT).move_to(RIGHT * 3.6 + UP * 2.55))

        titre = bandeau("Une balle posée dans un wagon",
                        "le wagon roule à vitesse constante u ; pas de frottement")
        self.play(FadeIn(titre), Create(sol), FadeIn(arb), FadeIn(wag), FadeIn(balle))
        self.play(FadeIn(etiquette_vue))

        # --- 1. Vu de la route --------------------------------------------------------------
        self.next_section("vu-route")
        fl_u = always_redraw(lambda: VGroup(
            fleche([ecran(x_wagon(t.get_value())) - 0.7, 0.2, 0],
                   [ecran(x_wagon(t.get_value())) + 0.7, 0.2, 0], C_VIT),
            M("+u", size=30, color=C_VIT).move_to([ecran(x_wagon(t.get_value())), 0.55, 0]))
            if vue.get_value() < 0.5 else VGroup())
        self.play(FadeIn(fl_u))
        self.play(t.animate.set_value(3), run_time=3, rate_func=linear)
        obs1 = VGroup(T("balle : v = +u, constante", size=22, color=ACCENT),
                      T("arbre : v = 0", size=22, color=C_VIT),
                      T("→ aucune accélération, aucune force : 1re loi OK", size=22)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 3.0 + UP * 1.7)
        self.play(FadeIn(obs1))
        self.wait(2)

        # --- 2. Vu du wagon ------------------------------------------------------------------
        self.next_section("vu-wagon")
        self.play(FadeOut(obs1), FadeOut(fl_u))
        self.remove(fl_u)
        self.play(vue.animate.set_value(1), t.animate.set_value(4), run_time=1.5, rate_func=smooth)
        fl_arbre = VGroup(fleche([-1.6, 0.2, 0], [-3.0, 0.2, 0], C_VIT),
                          M("-u", size=30, color=C_VIT).move_to([-2.3, 0.55, 0])).shift(RIGHT * 4.6)
        txt_arbre = T("les arbres défilent", size=20, color=C_VIT).next_to(fl_arbre, UP, buff=0.1)
        self.play(FadeIn(fl_arbre), FadeIn(txt_arbre))
        self.play(t.animate.set_value(6.5), run_time=2.5, rate_func=linear)
        obs2 = VGroup(T("balle : v = 0 (au repos)", size=22, color=ACCENT),
                      T("arbres : v = −u, constante", size=22, color=C_VIT),
                      T("→ là aussi : 1re loi OK", size=22)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(LEFT * 3.4 + UP * 1.6)
        self.play(FadeIn(obs2))
        self.wait(2)
        defi = encadre(VGroup(
            T("Référentiel d'inertie", size=26, color=ACCENT, weight=BOLD),
            T("un corps soumis à une force résultante nulle\nreste au repos ou garde une vitesse constante",
              size=22),
            T("tout référentiel à vitesse constante par rapport\nà un référentiel d'inertie en est un aussi",
              size=20, color=C_GRIS),
        ).arrange(DOWN, buff=0.15))
        defi.move_to(UP * 1.2)
        self.play(FadeOut(obs2), FadeOut(fl_arbre), FadeOut(txt_arbre), FadeIn(defi))
        self.wait(5)
        self.play(FadeOut(defi))

        # --- 3. Le wagon freine (vu du wagon) ---------------------------------------------------
        self.next_section("freinage-wagon")
        t.set_value(T_FREIN - 0.5)
        frein = T("Le wagon FREINE…", size=30, color=C_NEG).move_to(UP * 1.6)
        self.play(FadeIn(frein))
        self.play(t.animate.set_value(T_FREIN + 2.2), run_time=4, rate_func=linear)
        bizarre = VGroup(
            T("Dans le wagon, la balle part vers l'avant…", size=24, color=ACCENT),
            T("…alors que RIEN ne la pousse !", size=24, color=ACCENT),
            T("La 1re loi ne marche plus : S' n'est PAS un référentiel d'inertie.", size=24, color=C_NEG),
        ).arrange(DOWN, buff=0.15).move_to(UP * 1.2)
        limiter(bizarre, 12)
        self.play(FadeOut(frein))
        self.play(FadeIn(bizarre[0]))
        self.play(FadeIn(bizarre[1]))
        self.play(FadeIn(bizarre[2]))
        self.wait(4)
        self.play(FadeOut(bizarre))

        # --- 4. Même freinage, vu de la route ------------------------------------------------------
        self.next_section("freinage-route")
        decal.set_value(x_wagon(T_FREIN) + 1.5)  # le wagon commence à freiner en x = -1,5 à l'écran
        self.play(vue.animate.set_value(0), t.animate.set_value(T_FREIN - 0.6), run_time=1.5)
        explic = T("Vu de la route : la balle continue simplement à +u (inertie),\n"
                   "c'est le wagon qui ralentit sous elle.", size=24, color=C_VIT).move_to(UP * 1.4)
        self.play(FadeIn(explic))
        self.play(t.animate.set_value(T_FREIN + 2.2), run_time=4, rate_func=linear)
        self.wait(2)
        terre = T("La Terre tourne (sur elle-même, autour du Soleil) : elle n'est pas parfaitement\n"
                  "inertielle, mais pour des expériences de labo, c'est une excellente approximation.",
                  size=20, color=C_GRIS).to_edge(DOWN, buff=0.3)
        limiter(terre, 13)
        self.play(FadeIn(terre))
        self.wait(5)
        vider(self)
