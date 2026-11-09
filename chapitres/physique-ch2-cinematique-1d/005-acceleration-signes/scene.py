"""2.5 — L'accélération : définition, et surtout les 4 cas de signes (A, B, C, D du cours).

Message clé : « décélérer » ne veut PAS dire « a < 0 ».
v et a de même signe -> |v| augmente ; signes opposés -> |v| diminue.

    manim -pql chapitres/physique-ch2-cinematique-1d/005-acceleration-signes/scene.py SignesAcceleration
"""

from shared.physique import *

CAS = [
    # lettre, x0, v0, a, description
    ("A", 1.0, 1.0, 1.6, "v > 0, a > 0"),
    ("B", 1.0, 5.0, -1.6, "v > 0, a < 0"),
    ("C", 9.0, -1.0, -1.6, "v < 0, a < 0"),
    ("D", 9.0, -5.0, 1.6, "v < 0, a > 0"),
]
DUREE = 2.5
EV, EA = 0.3, 0.45  # échelles des flèches (unités écran par m/s et par m/s²)


class SignesAcceleration(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 2 · section 2.5", "L'accélération",
                    "Accélérer, freiner… et le piège des signes")

        # --- 1. Définitions ---------------------------------------------------
        self.next_section("definitions")
        titre = bandeau("L'accélération mesure comment la VITESSE change")
        d1 = VGroup(T("accélération moyenne", size=26, color=C_ACC),
                    M(r"a_{x\,\mathrm{moy}} = \frac{\Delta v_x}{\Delta t}", size=44))
        d2 = VGroup(T("accélération instantanée", size=26, color=C_ACC),
                    M(r"a_x = \frac{dv_x}{dt} = \frac{d^2x}{dt^2}", size=44))
        for d in (d1, d2):
            d.arrange(DOWN, buff=0.25)
        VGroup(d1, d2).arrange(RIGHT, buff=1.6).move_to(UP * 0.6)
        unite = M(r"[a] = \frac{\mathrm{m/s}}{\mathrm{s}} = \mathrm{m/s^2}", size=36,
                  color=C_GRIS).move_to(DOWN * 1.3)
        lien = T("Même logique qu'avant, un étage plus haut :\n"
                 "a = pente de la courbe v(t), comme v = pente de la courbe x(t)",
                 size=24, color=C_GRIS).move_to(DOWN * 2.6)
        self.play(FadeIn(titre), FadeIn(d1))
        self.play(FadeIn(d2))
        self.play(Write(unite))
        self.play(FadeIn(lien))
        self.wait(4)
        vider(self)

        # --- 2. Les quatre cas -------------------------------------------------
        self.next_section("quatre-cas")
        titre = bandeau("Quatre cas possibles", "flèche verte = vitesse, flèche rose = accélération")
        self.play(FadeIn(titre))
        t = ValueTracker(0)
        lignes = VGroup()
        etats = []
        ys = [1.5, 0.15, -1.2, -2.55]
        for (lettre, x0, v0, a, desc), y in zip(CAS, ys):
            nl = NumberLine(x_range=[0, 10, 1], length=6.5, color=C_GRIS,
                            include_tip=True, tip_width=0.15, tip_height=0.15)
            nl.move_to([0.2, y, 0])
            lab = VGroup(T(lettre, size=34, color=ACCENT, weight=BOLD),
                         T(desc, size=22)).arrange(RIGHT, buff=0.3)
            lab.next_to(nl, LEFT, buff=0.5)

            def pos(tt, x0=x0, v0=v0, a=a):
                return x0 + v0 * tt + 0.5 * a * tt * tt

            def vit(tt, v0=v0, a=a):
                return v0 + a * tt

            bille = always_redraw(lambda nl=nl, pos=pos: particule(r=0.11)
                                  .move_to(nl.n2p(pos(t.get_value()))))
            fv = always_redraw(lambda nl=nl, pos=pos, vit=vit: fleche(
                nl.n2p(pos(t.get_value())) + UP * 0.3,
                nl.n2p(pos(t.get_value())) + UP * 0.3 + RIGHT * EV * vit(t.get_value()),
                C_VIT, width=5, tip=0.16))
            fa = always_redraw(lambda nl=nl, pos=pos, a=a: fleche(
                nl.n2p(pos(t.get_value())) + DOWN * 0.3,
                nl.n2p(pos(t.get_value())) + DOWN * 0.3 + RIGHT * EA * a,
                C_ACC, width=5, tip=0.16))
            lignes.add(VGroup(nl, lab))
            etats.append((nl, pos, vit, a, v0, bille, fv, fa, y))
            self.play(Create(nl), FadeIn(lab), FadeIn(bille), FadeIn(fv), FadeIn(fa),
                      run_time=0.8)
        self.wait(2)
        self.play(t.animate.set_value(DUREE), run_time=4, rate_func=linear)
        self.wait()

        # images stroboscopiques : l'espacement montre si ça accélère ou freine
        strobo = VGroup()
        for nl, pos, vit, a, v0, *_ in etats:
            for k in range(6):
                tt = k * DUREE / 5
                strobo.add(Dot(nl.n2p(pos(tt)), radius=0.07, color=ACCENT).set_opacity(0.45))
        note = T("Points = positions toutes les 0,5 s", size=20, color=C_GRIS)
        note.to_corner(UR, buff=0.45)
        self.play(t.animate.set_value(0), run_time=0.6)
        self.play(FadeIn(strobo, lag_ratio=0.05), FadeIn(note), run_time=1.5)
        self.play(t.animate.set_value(DUREE), run_time=4, rate_func=linear)

        verdicts = VGroup()
        for nl, pos, vit, a, v0, bille, fv, fa, y in etats:
            meme = (a > 0) == (v0 > 0)
            v = T("|v| augmente\n→ accélère" if meme else "|v| diminue\n→ décélère",
                  size=22, color=C_VIT if meme else C_NEG)
            v.move_to([5.75, y, 0])
            verdicts.add(v)
        for v in verdicts:
            self.play(FadeIn(v, shift=LEFT * 0.2), run_time=0.6)
        self.wait(2)
        regle = encadre(T("v et a de même signe → ça accélère    "
                          "signes opposés → ça freine", size=24))
        regle.to_edge(DOWN, buff=0.12)
        piege = T("Cas D : a > 0 et pourtant la particule freine !", size=24, color=ACCENT)
        self.play(FadeOut(note), Indicate(lignes[3][1], color=ACCENT))
        piege.next_to(titre, DOWN, buff=0.15).align_to(titre, LEFT)
        self.play(FadeIn(piege))
        self.wait(2)
        self.play(FadeOut(VGroup(*[e[5] for e in etats], *[e[6] for e in etats],
                                 *[e[7] for e in etats])), lignes.animate.shift(UP * 0.25),
                  strobo.animate.shift(UP * 0.25), verdicts.animate.shift(UP * 0.25))
        self.play(FadeIn(regle))
        self.wait(5)
        vider(self)

        # --- 3. Les mêmes cas sur un graphe v(t) -------------------------------
        self.next_section("graphe-vt")
        titre = bandeau("Les mêmes cas sur le graphe de v(t)",
                        "le signe de v se lit sur la hauteur, le signe de a sur la pente")
        ax = Axes(x_range=[0, 2 * PI + 0.3, PI / 2], y_range=[-3.5, 3.5, 1], x_length=9,
                  y_length=5, axis_config={"color": C_GRIS}).move_to(DOWN * 0.6 + LEFT * 0.8)
        lv = M("v_x", size=32, color=C_GRIS).next_to(ax.y_axis, UP, buff=0.1)
        lt = M("t", size=32, color=C_GRIS).next_to(ax.x_axis, RIGHT, buff=0.1)
        f = lambda x: 3 * np.sin(x)
        g = ax.plot(f, x_range=[0, 2 * PI], color=C_VIT, stroke_width=5)
        self.play(FadeIn(titre), Create(ax), FadeIn(lv), FadeIn(lt), Create(g))
        zones = VGroup()
        infos = [("A", "v>0, a>0", C_VIT), ("B", "v>0, a<0", C_NEG),
                 ("C", "v<0, a<0", C_VIT), ("D", "v<0, a>0", C_NEG)]
        for k, (lettre, s, c) in enumerate(infos):
            x0, x1 = k * PI / 2, (k + 1) * PI / 2
            zone = ax.get_area(g, x_range=[x0, x1], color=c, opacity=0.25)
            y_txt = 3.0 if k < 2 else -3.0
            l = VGroup(T(lettre, size=30, color=ACCENT, weight=BOLD), T(s, size=20))
            l.arrange(DOWN, buff=0.08).move_to(ax.c2p((x0 + x1) / 2, y_txt + (0.3 if k < 2 else -0.3)))
            zones.add(VGroup(zone, l))
        legende = VGroup(T("vert : accélère", size=22, color=C_VIT),
                         T("rouge : décélère", size=22, color=C_NEG)).arrange(DOWN, aligned_edge=LEFT)
        legende.to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        tt = ValueTracker(0.15)

        def tangente():
            x = tt.get_value()
            p = np.array(ax.c2p(x, f(x)))
            u = np.array(ax.c2p(1, 3 * np.cos(x))) - np.array(ax.c2p(0, 0))
            u = u / np.linalg.norm(u)
            return Line(p - u * 1.1, p + u * 1.1, color=C_ACC, stroke_width=4)

        tang = always_redraw(tangente)
        pt = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), f(tt.get_value())), color=ACCENT))
        for z in zones:
            self.play(FadeIn(z), run_time=0.8)
        self.play(FadeIn(legende))
        lab_tang = T("tangente rose :\nsa pente = a", size=22, color=C_ACC)
        lab_tang.next_to(legende, DOWN, buff=0.4, aligned_edge=LEFT)
        VGroup(legende, lab_tang).to_edge(RIGHT, buff=0.3)
        self.play(FadeIn(tang), FadeIn(pt), FadeIn(lab_tang))
        self.play(tt.animate.set_value(2 * PI - 0.15), run_time=8, rate_func=linear)
        self.wait(4)
        vider(self)
