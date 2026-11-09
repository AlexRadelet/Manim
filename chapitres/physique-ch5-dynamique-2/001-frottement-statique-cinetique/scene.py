"""5.1 — Frottement statique et cinétique.

On pousse de plus en plus fort un bloc (N = 20 N, μs = 0,4, μc = 0,25) :
f_s suit F_app jusqu'à μs N = 8 N, puis le bloc part et f tombe à μc N = 5 N.

    python -m manim -pql chapitres/physique-ch5-dynamique-2/001-frottement-statique-cinetique/scene.py FrottementStatiqueCinetique
"""

from shared.physique import *

N_, MUS, MUC = 20.0, 0.4, 0.25
FSMAX, FC = MUS * N_, MUC * N_
K = 0.18


def frottement(F, glisse):
    return FC if glisse else min(F, FSMAX)


class FrottementStatiqueCinetique(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 5 · section 5.1", "Le frottement",
                    "Pourquoi c'est plus dur de démarrer que de continuer")

        # --- 1. On pousse de plus en plus fort -------------------------------------------
        self.next_section("pousser")
        titre = bandeau("On pousse un bloc de plus en plus fort", "N = 20 N, μs = 0,4, μc = 0,25")
        self.play(FadeIn(titre))
        sol = Line([-6.8, -0.4, 0], [0.3, -0.4, 0], color=C_SOL, stroke_width=8)
        F = ValueTracker(0)
        etat = {"glisse": False, "x": -4.6, "v": 0.0, "t": None}
        pos = ValueTracker(-4.6)
        b = always_redraw(lambda: bloc("", 1.3, 0.9).move_to([pos.get_value(), 0.05, 0]))
        fapp = always_redraw(lambda: fleche(b.get_left() + LEFT * (F.get_value() * K + 1e-3), b.get_left(), C_FORCE, width=6))
        # le frottement s'exerce au contact, et s'oppose au glissement : vers la GAUCHE
        ffr = always_redraw(lambda: fleche(b.get_bottom() + DOWN * 0.15,
                                           b.get_bottom() + DOWN * 0.15 + LEFT * (1e-3 + K * frottement(F.get_value(), etat["glisse"])),
                                           ACCENT, width=6))
        lapp = always_redraw(lambda: M(r"\vec F_{app}", size=28, color=C_FORCE).next_to(fapp, UP, buff=0.08))
        lfr = always_redraw(lambda: M(r"\vec f", size=28, color=ACCENT).next_to(ffr, DOWN, buff=0.08))
        self.play(Create(sol), FadeIn(b))
        self.add(fapp, ffr, lapp, lfr)

        ax = Axes(x_range=[0, 12, 2], y_range=[0, 10, 2], x_length=5.2, y_length=3.6,
                  axis_config={"color": C_GRIS, "include_numbers": True, "font_size": 20}, tips=False)
        ax.move_to(RIGHT * 3.9 + UP * 0.2)
        lx = M(r"F_{app}\ (\mathrm{N})", size=24, color=C_FORCE).next_to(ax.x_axis, DOWN, buff=0.45)
        ly = M(r"f\ (\mathrm{N})", size=24, color=ACCENT).next_to(ax.y_axis, UP, buff=0.1)
        self.play(Create(ax), FadeIn(lx), FadeIn(ly))
        courbe = always_redraw(lambda: VGroup(
            ax.plot(lambda x: x, x_range=[0, max(min(F.get_value(), FSMAX), 1e-3)], color=ACCENT, stroke_width=4),
            *([DashedLine(ax.c2p(FSMAX, FSMAX), ax.c2p(FSMAX, FC), color=ACCENT, stroke_width=3),
               ax.plot(lambda x: FC, x_range=[FSMAX, F.get_value()], color=ACCENT, stroke_width=4)]
              if etat["glisse"] else [])))
        point = always_redraw(lambda: Dot(ax.c2p(F.get_value(), frottement(F.get_value(), etat["glisse"])), color=ACCENT))
        self.add(courbe, point)
        cpt = VGroup(Compteur(r"F_{app} =", lambda: F.get_value(), r"\mathrm{N}", decimales=1, size=30, couleur_nombre=C_FORCE),
                     Compteur(r"f =", lambda: frottement(F.get_value(), etat["glisse"]), r"\mathrm{N}", decimales=1, size=30,
                              couleur_nombre=ACCENT)).arrange(RIGHT, buff=0.8).move_to(LEFT * 3.3 + UP * 2.2)
        self.play(FadeIn(cpt))
        self.play(F.animate.set_value(4), run_time=2.5, rate_func=linear)
        s1 = T("le bloc ne bouge pas : f_s = F_app\n(le frottement s'adapte)", size=22, color=C_GRIS).move_to(LEFT * 3.3 + DOWN * 1.6)
        self.play(FadeIn(s1))
        self.play(F.animate.set_value(FSMAX), run_time=2.5, rate_func=linear)
        seuil = T("seuil : f_s(max) = μs N = 8 N", size=24, color=ACCENT).move_to(LEFT * 3.3 + DOWN * 1.6)
        self.play(ReplacementTransform(s1, seuil))
        self.wait(1)
        etat["glisse"] = True
        t = ValueTracker(0)
        pos.add_updater(lambda m: m.set_value(-4.6 + 0.5 * 0.35 * t.get_value() ** 2))
        self.add(pos)
        self.play(F.animate.set_value(9), t.animate.set_value(3.5), run_time=3.5, rate_func=linear)
        pos.clear_updaters()
        glisse = T("ça glisse : f tombe à f_c = μc N = 5 N\n(plus besoin de pousser aussi fort)", size=22, color=C_VIT)
        glisse.move_to(LEFT * 3.3 + DOWN * 1.6)
        self.play(ReplacementTransform(seuil, glisse))
        lois = VGroup(M(r"f_s \le \mu_s N", size=36, color=ACCENT), M(r"f_c = \mu_c N", size=36, color=ACCENT),
                      T("μ sans unité ; en général μc < μs", size=20, color=C_GRIS)).arrange(RIGHT, buff=0.6)
        lois = encadre(lois).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(lois))
        self.wait(5)
        vider(self)

        # --- 2. D'où vient le frottement --------------------------------------------------------
        self.next_section("asperites")
        titre = bandeau("Les lois du frottement (empiriques)", "Léonard de Vinci 1508, Amontons 1699, Coulomb 1781")
        self.play(FadeIn(titre))
        lois = VGroup(
            T("1.  proportionnel à la force normale N", size=26),
            T("2.  indépendant de l'aire APPARENTE de contact", size=26),
            T("3.  indépendant de la vitesse (frottement cinétique)", size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 1.5)
        for l in lois:
            self.play(FadeIn(l, shift=RIGHT * 0.2))
            self.wait(0.6)
        rng = np.random.default_rng(4)
        xs = np.linspace(-5, 5, 61)
        rb = 0.18 * rng.random(len(xs))
        rh = 0.18 * rng.random(len(xs))
        for k in (9, 31, 50):  # trois « sommets » qui vont se toucher
            rb[k], rh[k] = 0.42, 0.42
        bas_y = -1.6 + rb
        haut_y = -0.3 - rh
        surf_h = VMobject(color=C_POS, stroke_width=3).set_points_as_corners([[x, y, 0] for x, y in zip(xs, haut_y)])
        surf_b = VMobject(color=C_SOL, stroke_width=3).set_points_as_corners([[x, y, 0] for x, y in zip(xs, bas_y)])
        bloc_h = VGroup(surf_h, Line([-5, haut_y[0], 0], [-5, 0.3, 0], color=C_POS), Line([5, haut_y[-1], 0], [5, 0.3, 0], color=C_POS))
        decal = min(haut_y - bas_y)
        contacts = VGroup(*[Dot([x, yb, 0], radius=0.09, color=C_NEG) for x, yb, yh in zip(xs, bas_y, haut_y)
                            if yh - yb - decal < 0.02])
        self.play(Create(surf_b), Create(bloc_h))
        self.play(bloc_h.animate.shift(DOWN * decal))
        self.play(FadeIn(contacts))
        zoom = T("au microscope : les surfaces ne se touchent qu'au sommet des aspérités (10⁻⁵ à 10⁻⁴ mm)\n"
                 "→ aire réelle de contact jusqu'à 10 000 fois plus petite que l'aire apparente",
                 size=20, color=C_GRIS).to_edge(DOWN, buff=0.5)
        limiter(zoom, 13)
        self.play(FadeIn(zoom))
        self.wait(5)
        vider(self)
