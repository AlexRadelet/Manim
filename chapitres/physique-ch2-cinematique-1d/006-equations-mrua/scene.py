"""2.6 — MRUA : d'où viennent les 4 équations, et comment choisir la bonne.

Scène 1 : EquationsMRUA   — démonstration graphique (aire sous v(t)) + tableau « grandeur absente ».
Scène 2 : ExempleAutomobile — exemple 1 du cours (0 -> 30 m/s en 10 s).

    manim -pql chapitres/physique-ch2-cinematique-1d/006-equations-mrua/scene.py EquationsMRUA
    manim -pql chapitres/physique-ch2-cinematique-1d/006-equations-mrua/scene.py ExempleAutomobile
"""

from shared.physique import *

V0, A, TF = 2.0, 1.5, 4.0
VF = V0 + A * TF

EQUATIONS = [
    (r"v_x = v_{x0} + a_x t", "2.11", "x - x_0"),
    (r"x = x_0 + \tfrac{1}{2}(v_{x0} + v_x)\,t", "2.12", "a_x"),
    (r"x = x_0 + v_{x0} t + \tfrac{1}{2} a_x t^2", "2.13", "v_x"),
    (r"v_x^2 = v_{x0}^2 + 2a_x (x - x_0)", "2.14", "t"),
]
GRANDEURS = ["x - x_0", "v_{x0}", "v_x", "a_x", "t"]


def tableau_mrua() -> VGroup:
    """Tableau : quelle grandeur est ABSENTE de chaque équation."""
    entetes = VGroup(*[M(g, size=32, color=ACCENT) for g in GRANDEURS])
    lignes = VGroup()
    for tex, num, absente in EQUATIONS:
        eq = M(tex, size=32)
        n = M(f"({num})", size=24, color=C_GRIS)
        marques = VGroup(*[
            M(r"\times", size=40, color=C_NEG) if g == absente
            else M(r"\checkmark", size=32, color=C_VIT)
            for g in GRANDEURS])
        lignes.add(VGroup(VGroup(n, eq).arrange(RIGHT, buff=0.2), marques))
    largeur_eq = max(l[0].width for l in lignes) + 0.4
    col_x = [largeur_eq + 0.9 * k for k in range(len(GRANDEURS))]
    for k, e in enumerate(entetes):
        e.move_to([col_x[k], 0, 0])
    for i, l in enumerate(lignes):
        y = -0.85 * (i + 1)
        l[0].move_to([0, y, 0], aligned_edge=LEFT)
        for k, mq in enumerate(l[1]):
            mq.move_to([col_x[k], y, 0])
    sep = Line([-0.1, -0.42, 0], [col_x[-1] + 0.5, -0.42, 0], color=C_GRIS, stroke_width=2)
    tab = VGroup(entetes, lignes, sep)
    tab.move_to(ORIGIN)
    return tab


class EquationsMRUA(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.6", "Le MRUA",
                    "Mouvement Rectiligne Uniformément Accéléré : a = constante")

        ax = Axes(x_range=[0, 5, 1], y_range=[0, 9, 1], x_length=6.2, y_length=5.2,
                  axis_config={"color": C_GRIS}).move_to(LEFT * 3.1 + DOWN * 0.45)
        lt = M("t", size=32, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        lv = M("v_x", size=32, color=C_GRIS).next_to(ax.y_axis, UP, buff=0.1)
        col = RIGHT * 3.75

        # --- 1. a constant -> v(t) est une droite ----------------------------
        self.next_section("droite")
        titre = bandeau("a constante → v(t) est une droite")
        self.play(FadeIn(titre), Create(ax), FadeIn(lt), FadeIn(lv))
        notation = VGroup(
            T("Nouvelle notation", size=22, color=C_GRIS),
            M(r"t_i \to 0 \quad t_f \to t \quad x_i \to x_0 \quad v_{xi} \to v_{x0}", size=28,
              color=C_GRIS),
        ).arrange(DOWN, buff=0.15).move_to(col + UP * 2.6)
        self.play(FadeIn(notation))
        droite = ax.plot(lambda t: V0 + A * t, x_range=[0, TF], color=C_VIT, stroke_width=5)
        self.play(Create(droite))
        p0 = ax.c2p(0, V0)
        l_v0 = M("v_{x0}", size=30, color=C_VIT).next_to(p0, LEFT, buff=0.15)
        pf = ax.c2p(TF, VF)
        l_vf = M("v_x", size=30, color=C_VIT).next_to(pf, UP, buff=0.12)
        l_tf = M("t", size=30).next_to(ax.c2p(TF, 0), DOWN, buff=0.15)
        tir = DashedLine(ax.c2p(TF, 0), pf, color=C_GRIS)
        self.play(FadeIn(l_v0), FadeIn(l_vf), FadeIn(l_tf), Create(tir))
        pente = VGroup(DashedLine(ax.c2p(1, V0 + A), ax.c2p(2, V0 + A), color=C_ACC),
                       DashedLine(ax.c2p(2, V0 + A), ax.c2p(2, V0 + 2 * A), color=C_ACC))
        l_pente = M("a_x", size=28, color=C_ACC).next_to(pente[1], RIGHT, buff=0.08)
        self.play(Create(pente), FadeIn(l_pente))
        eq1 = encadre(VGroup(M(EQUATIONS[0][0], size=40), M("(2.11)", size=24, color=C_GRIS))
                      .arrange(RIGHT, buff=0.3))
        eq1.move_to(col + UP * 1.3)
        explic1 = T("« la vitesse de départ\n+ ce qu'on gagne chaque seconde × t »", size=22,
                    color=C_GRIS).next_to(eq1, DOWN, buff=0.25)
        self.play(FadeIn(eq1))
        self.play(FadeIn(explic1))
        self.wait(3)

        # --- 2. Aire = rectangle + triangle -> Merton ------------------------------
        self.next_section("merton")
        self.play(FadeOut(explic1), FadeOut(pente), FadeOut(l_pente), FadeOut(notation),
                  eq1.animate.scale(0.75).move_to(col + UP * 2.7))
        titre2 = bandeau("Le déplacement = l'aire sous v(t)")
        self.play(Transform(titre, titre2))
        rect = Polygon(ax.c2p(0, 0), ax.c2p(TF, 0), ax.c2p(TF, V0), ax.c2p(0, V0),
                       stroke_width=0, fill_color=C_POS, fill_opacity=0.45)
        tri = Polygon(ax.c2p(0, V0), ax.c2p(TF, V0), ax.c2p(TF, VF), stroke_width=0,
                      fill_color=ACCENT, fill_opacity=0.45)
        l_rect = M(r"v_{x0}\,t", size=30).move_to(rect)
        l_tri = M(r"\tfrac12 (v_x - v_{x0})\,t", size=26).move_to(tri.get_center() + DOWN * 0.15 + RIGHT * 0.35)
        self.play(FadeIn(rect), Write(l_rect))
        self.play(FadeIn(tri), Write(l_tri))
        calc = VGroup(
            M(r"x - x_0 = \text{rectangle} + \text{triangle}", size=30),
            M(r"= v_{x0}\,t + \tfrac12 (v_x - v_{x0})\,t", size=30),
            M(r"= \tfrac12 (v_{x0} + v_x)\,t", size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(col + UP * 1.05)
        for c in calc:
            self.play(Write(c))
        merton = encadre(VGroup(M(EQUATIONS[1][0], size=36), M("(2.12)", size=24, color=C_GRIS))
                         .arrange(RIGHT, buff=0.3))
        merton.next_to(calc, DOWN, buff=0.35)
        nom = T("Règle de Merton : vitesse moyenne = moyenne des 2 vitesses", size=20,
                color=C_GRIS).next_to(merton, DOWN, buff=0.15)
        limiter(nom, 6.3)
        self.play(FadeIn(merton), FadeIn(nom))
        self.wait(3)

        # --- 3. On remplace v_x -> équation de la position ----------------------------
        self.next_section("position")
        self.play(FadeOut(calc), FadeOut(nom), merton.animate.scale(0.75).next_to(eq1, DOWN, buff=0.2))
        etapes = VGroup(
            T("dans (2.12), on remplace v_x par (2.11) :", size=22, color=C_GRIS),
            M(r"x = x_0 + \tfrac12 \left(v_{x0} + v_{x0} + a_x t\right) t", size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(col + UP * 0.6)
        self.play(FadeIn(etapes[0]), Write(etapes[1]))
        eq3 = encadre(VGroup(M(EQUATIONS[2][0], size=36), M("(2.13)", size=24, color=C_GRIS))
                      .arrange(RIGHT, buff=0.3))
        eq3.next_to(etapes, DOWN, buff=0.35)
        parab = T("→ x(t) est une parabole", size=22, color=C_POS).next_to(eq3, DOWN, buff=0.15)
        self.play(FadeIn(eq3), FadeIn(parab))
        self.wait(3)

        # --- 4. On élimine t -> v² ----------------------------------------------------
        self.next_section("v-carre")
        self.play(FadeOut(etapes), FadeOut(parab), eq3.animate.scale(0.75).next_to(merton, DOWN, buff=0.2))
        etapes2 = VGroup(
            T("de (2.11) :  t = (v_x − v_x0) / a_x , dans (2.12) :", size=22, color=C_GRIS),
            M(r"x - x_0 = \tfrac12 (v_{x0} + v_x)\,\frac{v_x - v_{x0}}{a_x} = "
              r"\frac{v_x^2 - v_{x0}^2}{2a_x}", size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        limiter(etapes2, 6.4).move_to(col + DOWN * 0.3)
        self.play(FadeIn(etapes2[0]), Write(etapes2[1]))
        eq4 = encadre(VGroup(M(EQUATIONS[3][0], size=36), M("(2.14)", size=24, color=C_GRIS))
                      .arrange(RIGHT, buff=0.3))
        eq4.next_to(etapes2, DOWN, buff=0.35)
        sans_t = T("→ pratique quand on ne connaît pas t", size=22, color=ACCENT)
        sans_t.next_to(eq4, DOWN, buff=0.15)
        self.play(FadeIn(eq4), FadeIn(sans_t))
        self.wait(4)
        vider(self)

        # --- 5. Le tableau qui sert à choisir ----------------------------------------
        self.next_section("tableau")
        titre = bandeau("Quelle équation utiliser ?",
                        "chaque équation contient 4 des 5 grandeurs — une seule est absente")
        tab = tableau_mrua().move_to(UP * 0.1)
        self.play(FadeIn(titre))
        self.play(FadeIn(tab[0]), Create(tab[2]))
        for l in tab[1]:
            self.play(FadeIn(l[0]), LaggedStart(*[FadeIn(m, scale=0.5) for m in l[1]],
                                                 lag_ratio=0.1), run_time=1)
        self.wait()
        croix = VGroup(*[next(m for m, g in zip(l[1], GRANDEURS) if g == e[2])
                         for l, e in zip(tab[1], EQUATIONS)])
        self.play(*[Indicate(c, scale_factor=1.6, color=C_NEG) for c in croix], run_time=1.5)
        methode = VGroup(
            T("1. Liste les grandeurs connues (il en faut 3).", size=24),
            T("2. Repère celle que tu ne connais pas ET ne cherches pas.", size=24),
            T("3. Prends l'équation où elle est absente (×).", size=24, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        for m in methode:
            self.play(FadeIn(m, shift=UP * 0.1))
        self.wait(5)
        vider(self)


class ExempleAutomobile(Scene):
    """Exemple 1 : une auto passe de 0 à 30 m/s en 10 s, puis roule à vitesse constante."""

    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.6 · exemple 1", "Une automobile qui accélère",
                    "Utiliser le tableau pour choisir l'équation")
        titre = bandeau("Une auto accélère de 0 à 30 m/s en 10 s")

        # route + voiture
        route = NumberLine(x_range=[0, 160, 10], length=11, color=C_GRIS, include_numbers=True,
                           numbers_to_include=[0, 50, 100, 150], font_size=20)
        route.move_to(UP * 2.0)
        lab_x = M(r"x\ (\mathrm{m})", size=24, color=C_GRIS).next_to(route, RIGHT, buff=0.1)
        auto = voiture(color=C_POS, largeur=0.8)
        t = ValueTracker(0)
        auto.add_updater(lambda m: m.move_to(route.n2p(1.5 * min(t.get_value(), 10) ** 2) + UP * 0.32))
        horloge = VGroup(
            Compteur("t =", lambda: t.get_value(), r"\mathrm{s}", size=30),
            Compteur("v_x =", lambda: 3 * min(t.get_value(), 10), r"\mathrm{m/s}", size=30,
                     couleur_nombre=C_VIT),
        ).arrange(RIGHT, buff=0.8)
        horloge.next_to(route, DOWN, buff=0.45)
        self.play(FadeIn(titre), Create(route), FadeIn(lab_x), FadeIn(auto), FadeIn(horloge))
        self.play(t.animate.set_value(10), run_time=5, rate_func=linear)
        self.wait()

        donnees = VGroup(
            T("Données", size=24, color=ACCENT, weight=BOLD),
            M(r"v_{x0} = 0 \qquad v_x = 30\ \mathrm{m/s} \qquad t = 10\ \mathrm{s}", size=32),
        ).arrange(RIGHT, buff=0.4).move_to(UP * 0.1)
        self.play(FadeIn(donnees))

        a_txt = VGroup(
            T("(a) a_x ?   x − x₀ inconnu et pas demandé → (2.11)", size=22, color=C_GRIS),
            M(r"a_x = \frac{v_x - v_{x0}}{t} = \frac{30 - 0}{10} = 3\ \mathrm{m/s^2}", size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        b_txt = VGroup(
            T("(b) distance pendant l'accélération → (2.13)", size=22, color=C_GRIS),
            M(r"x = 0 + 0 + \tfrac12 (3)(10)^2 = 150\ \mathrm{m}", size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        VGroup(a_txt, b_txt).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(DOWN * 1.2)
        limiter(VGroup(a_txt, b_txt), 13.4)
        self.play(FadeIn(a_txt[0]), Write(a_txt[1]))
        self.wait(2)
        self.play(FadeIn(b_txt[0]), Write(b_txt[1]))
        self.wait(3)

        # (c)
        self.next_section("c")
        self.play(FadeOut(VGroup(a_txt, b_txt, donnees)))
        zone = Line(route.n2p(1.5 * 100 / 9), route.n2p(1.5 * 400 / 9), color=ACCENT,
                    stroke_width=10).set_opacity(0.7)
        c_q = T("(c) Quelle distance pendant que v passe de 10 à 20 m/s ?", size=26, color=ACCENT)
        c_q.move_to(UP * 0.1)
        self.play(FadeIn(c_q), t.animate.set_value(0), run_time=1)
        self.play(t.animate.set_value(10 / 3), run_time=2, rate_func=linear)
        self.play(t.animate.set_value(20 / 3), Create(zone), run_time=2, rate_func=linear)
        self.wait()
        raison = VGroup(
            M(r"\text{connu : } v_{x0} = 10,\ v_x = 20,\ a_x = 3"
              r"\qquad \text{inconnu et pas demandé : } t", size=30),
            T("t est absent de (2.14) → c'est elle !", size=24, color=ACCENT),
            M(r"v_x^2 = v_{x0}^2 + 2a_x\,\Delta x \ \Rightarrow\ "
              r"\Delta x = \frac{20^2 - 10^2}{2 \cdot 3} = 50\ \mathrm{m}", size=36),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 1.6)
        limiter(raison, 13.2)
        for r in raison:
            self.play(FadeIn(r, shift=UP * 0.1))
            self.wait(1.2)
        self.wait(4)
        vider(self)
