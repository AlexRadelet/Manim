"""2.7 — Chute libre verticale.

Scène 1 : ChuteLibreGalilee — tous les corps tombent avec la même accélération ; a_y = −g toujours.
Scène 2 : BalleLanceeDuToit — exemple du cours : balle lancée vers le haut à 12 m/s d'un toit de 40 m.
          Les questions (a)…(e) sont traitées dans l'ordre CHRONOLOGIQUE : (c), (d), (e), (a), (b).

    manim -pql chapitres/physique-ch2-cinematique-1d/008-chute-libre/scene.py ChuteLibreGalilee
    manim -pql chapitres/physique-ch2-cinematique-1d/008-chute-libre/scene.py BalleLanceeDuToit
"""

from shared.physique import *

G = 9.8
Y0, VY0 = 40.0, 12.0
T_SOL = (VY0 + np.sqrt(VY0 ** 2 + 2 * G * Y0)) / G  # 4,33 s


def y_de_t(t):
    return Y0 + VY0 * t - 0.5 * G * t * t


def v_de_t(t):
    return VY0 - G * t


class ChuteLibreGalilee(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.7", "La chute libre",
                    "Un mouvement sous le seul effet de la gravité")
        titre = bandeau("Galilée : tous les corps tombent pareil",
                        "en un même lieu, sans résistance de l'air")
        self.play(FadeIn(titre))
        sol = Line(LEFT * 6, RIGHT * 6, color=C_SOL, stroke_width=6).move_to(DOWN * 3.2)
        grosse = Circle(radius=0.55, color=C_POS, fill_opacity=0.9).move_to(LEFT * 2.5 + UP * 2.2)
        petite = Circle(radius=0.15, color=ACCENT, fill_opacity=0.9).move_to(RIGHT * 0 + UP * 2.2)
        plume = VGroup(Line(ORIGIN, UP * 0.5, color=C_TEXTE, stroke_width=2),
                       *[Line(UP * k * 0.08, UP * k * 0.08 + RIGHT * 0.15 + UP * 0.1,
                              color=C_TEXTE, stroke_width=2) for k in range(1, 6)],
                       *[Line(UP * k * 0.08, UP * k * 0.08 + LEFT * 0.15 + UP * 0.1,
                              color=C_TEXTE, stroke_width=2) for k in range(1, 6)])
        plume.move_to(RIGHT * 2.5 + UP * 2.2)
        objets = VGroup(grosse, petite, plume)
        for o in objets:  # mêmes points de départ : le bas de chaque objet à la même hauteur
            o.align_to(UP * 0.8, DOWN)
        noms = VGroup(T("boule de bowling", size=20), T("bille", size=20), T("plume", size=20))
        for n, o in zip(noms, objets):
            n.next_to(o, UP, buff=0.15)
        vide = T("(dans le vide)", size=22, color=C_GRIS).move_to(RIGHT * 5 + UP * 1.6)
        self.play(Create(sol), FadeIn(objets), FadeIn(noms), FadeIn(vide))
        self.wait()
        self.play(FadeOut(noms))
        hauteur = 0.8 - (-3.2)
        self.play(objets.animate.shift(DOWN * hauteur),
                  rate_func=rate_functions.ease_in_quad, run_time=1.8)
        ens = T("…elles arrivent ENSEMBLE", size=30, color=ACCENT).move_to(UP * 0.8)
        self.play(FadeIn(ens))
        self.wait(2)
        self.play(FadeOut(VGroup(objets, sol, ens, vide)))

        # a_y = −g
        self.next_section("a-egal-moins-g")
        axe = Arrow(DOWN * 2.6, UP * 2.6, buff=0, color=C_GRIS, stroke_width=4).move_to(LEFT * 4.5 + DOWN * 0.3)
        ly = M("y", size=34, color=C_GRIS).next_to(axe, UP, buff=0.1)
        bille = particule().move_to(LEFT * 3.5 + UP * 0.3)
        fa = fleche(bille.get_center() + RIGHT * 0.35, bille.get_center() + RIGHT * 0.35 + DOWN * 1.3, C_ACC)
        la = M("a_y = -g", size=34, color=C_ACC).next_to(fa, RIGHT, buff=0.15)
        self.play(GrowArrow(axe), FadeIn(ly), FadeIn(bille), GrowArrow(fa), FadeIn(la))
        infos = VGroup(
            M(r"g \approx 9{,}8\ \mathrm{m/s^2}", size=38),
            T("axe y vers le HAUT  →  a_y = −g", size=26, color=C_ACC),
            T("que la balle monte, s'arrête ou descende :\nl'accélération vaut TOUJOURS −g",
              size=24, color=ACCENT),
            T("→ la chute libre est un MRUA", size=26),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 1.6 + UP * 0.4)
        for i in infos:
            self.play(FadeIn(i, shift=UP * 0.1))
            self.wait(0.8)
        self.wait(2)
        self.play(FadeOut(infos))
        eqs = VGroup(
            M(r"v_y = v_{y0} - g t", size=34),
            M(r"y = y_0 + \tfrac12 (v_{y0} + v_y)\, t", size=34),
            M(r"y = y_0 + v_{y0} t - \tfrac12 g t^2", size=34),
            M(r"v_y^2 = v_{y0}^2 - 2g (y - y_0)", size=34),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        nums = VGroup(*[M(f"(2.{k})", size=24, color=C_GRIS).next_to(e, RIGHT, buff=0.4)
                        for k, e in zip(range(15, 19), eqs)])
        bloc = encadre(VGroup(eqs, nums)).move_to(RIGHT * 1.6 + UP * 0.2)
        rem = T("= les 4 équations du MRUA avec x → y et a_x → −g", size=22, color=C_GRIS)
        rem.next_to(bloc, DOWN, buff=0.3)
        self.play(FadeIn(bloc))
        self.play(FadeIn(rem))
        self.wait(5)
        vider(self)


class BalleLanceeDuToit(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.7 · exemple", "Une balle lancée d'un toit",
                    "v₀ = 12 m/s vers le haut, depuis un toit de 40 m")
        titre = bandeau("Une balle lancée d'un toit")
        self.play(FadeIn(titre))

        Y_SOL, ECH = -2.95, 0.112  # écran : y = Y_SOL + ECH * hauteur

        def ye(h):
            return Y_SOL + ECH * h

        # --- décor ----------------------------------------------------------------
        sol = Line([-6.9, Y_SOL, 0], [-2.2, Y_SOL, 0], color=C_SOL, stroke_width=6)
        immeuble = Rectangle(width=1.4, height=ECH * 40, color=C_GRIS, fill_opacity=0.35,
                             stroke_width=2).move_to([-4.3, ye(20), 0])
        fenetres = VGroup(*[Square(0.18, color=C_GRIS, fill_opacity=0.4, stroke_width=0)
                            .move_to([-4.3 + dx, ye(h), 0])
                            for h in range(5, 40, 6) for dx in (-0.35, 0, 0.35)])
        axe = NumberLine(x_range=[0, 50, 10], length=ECH * 50, rotation=PI / 2,
                         include_numbers=True, font_size=20, color=C_GRIS,
                         label_direction=LEFT)
        axe.move_to([-6.2, ye(25), 0])
        ly = M(r"y\ (\mathrm{m})", size=24, color=C_GRIS).next_to(axe, UP, buff=0.1)
        xb = -3.35
        t = ValueTracker(0)
        balle = always_redraw(lambda: particule().move_to([xb, ye(y_de_t(t.get_value())), 0]))
        fv = always_redraw(lambda: fleche(
            balle.get_center() + RIGHT * 0.3,
            balle.get_center() + RIGHT * 0.3 + UP * 0.06 * v_de_t(t.get_value()), C_VIT,
            width=5, tip=0.18))
        fa = always_redraw(lambda: fleche(
            balle.get_center() + RIGHT * 0.6,
            balle.get_center() + RIGHT * 0.6 + DOWN * 0.06 * G, C_ACC, width=5, tip=0.18))
        self.play(Create(sol), FadeIn(immeuble), FadeIn(fenetres), Create(axe), FadeIn(ly))
        self.play(FadeIn(balle), GrowArrow(fv), GrowArrow(fa))
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=C_VIT, stroke_width=5),
                            M("v_y", size=26, color=C_VIT)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, color=C_ACC, stroke_width=5),
                            M("a_y = -g", size=26, color=C_ACC)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.5).next_to(titre, RIGHT, buff=0.8)

        # --- graphe y(t), aligné sur les hauteurs de la scène ------------------------
        ax = Axes(x_range=[0, 4.6, 1], y_range=[0, 50, 10], x_length=6.3, y_length=ECH * 50,
                  axis_config={"color": C_GRIS, "include_numbers": True, "font_size": 20},
                  tips=False)
        ax.shift(np.array([-0.4, Y_SOL, 0]) - np.array(ax.c2p(0, 0)))
        lt = M(r"t\ (\mathrm{s})", size=24, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        courbe = always_redraw(lambda: ax.plot(y_de_t, x_range=[0, max(t.get_value(), 1e-3)],
                                               color=C_POS, stroke_width=4))
        lien = always_redraw(lambda: DashedLine(balle.get_center(),
                                                ax.c2p(t.get_value(), y_de_t(t.get_value())),
                                                color=C_GRIS, stroke_width=1.5,
                                                dash_length=0.08))
        compteurs = VGroup(
            Compteur("t =", lambda: t.get_value(), r"\mathrm{s}", decimales=2, size=28),
            Compteur("y =", lambda: y_de_t(t.get_value()), r"\mathrm{m}", decimales=1, size=28),
            Compteur("v_y =", lambda: v_de_t(t.get_value()), r"\mathrm{m/s}", decimales=1,
                     size=28, couleur_nombre=C_VIT, signe=True),
        ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.15).set_x(2.9)
        self.play(Create(ax), FadeIn(lt), FadeIn(leg), FadeIn(compteurs))
        self.add(courbe, lien)
        self.wait()

        panneau_pos = RIGHT * 1.75 + DOWN * 1.3

        def panneau(*lignes):
            g = VGroup(*lignes).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            limiter(g, 3.7)
            if g.height > 2.75:
                g.scale_to_fit_height(2.75)
            b = encadre(g, color=C_GRIS, buff=0.15)
            return b.move_to(panneau_pos)

        def marque(tt, texte, direction=UP):
            p = ax.c2p(tt, y_de_t(tt))
            d = Dot(p, color=ACCENT, radius=0.07)
            l = T(texte, size=18, color=ACCENT).next_to(p, direction, buff=0.12)
            return VGroup(d, l)

        donnees = panneau(T("Données (axe y vers le haut, origine au sol)", size=20, color=C_GRIS),
                          M(r"y_0 = 40\ \mathrm{m}\quad v_{y0} = +12\ \mathrm{m/s}\quad a_y = -9{,}8\ \mathrm{m/s^2}",
                            size=28))
        self.play(FadeIn(donnees))
        self.wait(3)

        # (c) sommet
        self.next_section("sommet")
        t_som = VY0 / G
        self.play(FadeOut(donnees), t.animate.set_value(t_som), run_time=2.5,
                  rate_func=rate_functions.ease_out_quad)
        m1 = marque(t_som, "sommet", UP)
        piege = T("v = 0 …\nmais a = −g !", size=20, color=C_ACC).next_to(balle, RIGHT, buff=0.95).shift(DOWN * 0.55)
        p1 = panneau(T("(c) Hauteur maximale : v_y = 0", size=22, color=ACCENT),
                     M(r"0 = 12^2 - 2(9{,}8)(y - 40) \Rightarrow y = 47{,}3\ \mathrm{m}", size=28),
                     M(r"0 = 12 - 9{,}8\,t \Rightarrow t = 1{,}22\ \mathrm{s}", size=28))
        self.play(FadeIn(m1), FadeIn(p1), FadeIn(piege))
        self.wait(4)

        # (d) repasse au niveau du toit
        self.next_section("toit")
        t_toit = 2 * VY0 / G
        self.play(FadeOut(p1), FadeOut(piege), t.animate.set_value(t_toit), run_time=2.5,
                  rate_func=rate_functions.ease_in_quad)
        m2 = marque(t_toit, "toit", RIGHT)
        p2 = panneau(T("(d) Retour au niveau du toit : y = 40 m", size=22, color=ACCENT),
                     M(r"40 = 40 + 12t - 4{,}9t^2 \Rightarrow t = 0 \text{ ou } 2{,}45\ \mathrm{s}",
                       size=28),
                     T("v_y = −12 m/s : même vitesse qu'au départ,\nmais vers le bas (symétrie)",
                       size=20, color=C_GRIS))
        self.play(FadeIn(m2), FadeIn(p2))
        self.wait(4)

        # (e) 15 m sous le toit
        self.next_section("moins-15")
        t_25 = (VY0 + np.sqrt(VY0 ** 2 + 2 * G * 15)) / G
        self.play(FadeOut(p2), t.animate.set_value(t_25), run_time=1.5, rate_func=linear)
        m3 = marque(t_25, "y = 25 m", RIGHT)
        p3 = panneau(T("(e) 15 m sous le toit : y = 25 m", size=22, color=ACCENT),
                     M(r"25 = 40 + 12t - 4{,}9t^2", size=28),
                     M(r"\Rightarrow t = 3{,}36\ \mathrm{s}\quad(\text{ou } -0{,}91\ \mathrm{s} : "
                       r"\text{rejeté})", size=28))
        self.play(FadeIn(m3), FadeIn(p3))
        self.wait(4)

        # (a) et (b) le sol
        self.next_section("sol")
        self.play(FadeOut(p3), t.animate.set_value(T_SOL), run_time=1.2, rate_func=linear)
        m4 = marque(T_SOL, "sol", UP + LEFT * 0.3)
        p4 = panneau(T("(a) Vitesse au sol : y = 0", size=22, color=ACCENT),
                     M(r"v_y^2 = 12^2 - 2(9{,}8)(0 - 40) = 928", size=28),
                     M(r"v_y = -30{,}5\ \mathrm{m/s}", size=28, color=C_VIT),
                     T("on garde la racine négative : elle descend", size=18, color=C_GRIS),
                     T("(b) Durée du vol", size=22, color=ACCENT),
                     M(r"-30{,}5 = 12 - 9{,}8\,t \Rightarrow t = 4{,}34\ \mathrm{s}", size=28))
        self.play(FadeIn(m4), FadeIn(p4))
        self.wait(6)
        vider(self)
