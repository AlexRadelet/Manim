"""5.2 — La « force centripète » n'est pas une force de plus : c'est le rôle joué par T, N ou f.

1. Trois exemples côte à côte : corde (tension), paroi (normale), voiture (frottement).
2. La pièce sur le disque : μs minimal = 4π²r / (T² g), la masse n'intervient pas.

    python -m manim -pql chapitres/physique-ch5-dynamique-2/004-force-centripete/scene.py ForceCentripete
"""

from shared.physique import *


def u(a):
    return np.array([np.cos(a), np.sin(a), 0])


class ForceCentripete(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 5 · section 5.2", "La dynamique du mouvement circulaire",
                    "Pour tourner, il faut une force vers le centre")

        # --- 1. Qui joue le rôle de force centripète ? ----------------------------------------
        self.next_section("trois-exemples")
        titre = bandeau("Σ F vers le centre = m v² / r", "mais QUELLE force tire vers le centre ?")
        self.play(FadeIn(titre))
        ang = ValueTracker(0)
        cas = [(-4.6, "corde", r"\vec T", "la tension de la corde"),
               (0.0, "paroi", r"\vec N", "la normale de la paroi"),
               (4.6, "voiture", r"\vec f", "le frottement sur les pneus")]
        R = 1.4
        y0 = 0.4
        for x, nom, lab, txt in cas:
            c = np.array([x, y0, 0])
            cercle = Circle(radius=R, color=C_GRIS, stroke_width=2).move_to(c)
            extra = VGroup()
            if nom == "paroi":
                extra = Circle(radius=R + 0.15, color=C_SOL, stroke_width=10).move_to(c)
            if nom == "voiture":
                extra = Annulus(inner_radius=R - 0.3, outer_radius=R + 0.3, color=C_GRIS, fill_opacity=0.2,
                                stroke_width=0).move_to(c)

            def obj(c=c, nom=nom, lab=lab):
                p = c + R * u(ang.get_value())
                g = VGroup()
                if nom == "corde":
                    g.add(Line(c, p, color=C_TEXTE, stroke_width=2), Dot(c, color=C_GRIS))
                    g.add(Dot(p, radius=0.13, color=ACCENT))
                elif nom == "paroi":
                    g.add(Square(0.3, color=ACCENT, fill_opacity=0.8).move_to(p))
                else:
                    g.add(Rectangle(width=0.22, height=0.42, color=PRIMARY, fill_opacity=0.9)
                          .rotate(ang.get_value()).move_to(p))
                g.add(fleche(p, p - 0.9 * u(ang.get_value()), C_FORCE, width=6))
                g.add(M(lab, size=26, color=C_FORCE).move_to(p - 0.45 * u(ang.get_value()) + 0.3 * u(ang.get_value() + PI / 2)))
                return g

            o = always_redraw(obj)
            l = T(txt, size=20, color=C_FORCE).move_to(c + DOWN * (R + 0.75))
            self.add(extra, cercle, o)
            self.play(FadeIn(extra), Create(cercle), FadeIn(o), FadeIn(l), run_time=0.7)
        self.play(ang.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        cle = encadre(T("La force centripète n'est PAS une force à ajouter au diagramme :\n"
                        "c'est le nom de la résultante vers le centre (T, N, f, poids…).",
                        size=22, color=ACCENT)).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(cle), ang.animate.set_value(2 * PI + PI / 2), run_time=1.2, rate_func=linear)
        self.play(ang.animate.set_value(4 * PI), run_time=3, rate_func=linear)
        self.wait(3)
        vider(self)

        # --- 2. La pièce sur le disque -------------------------------------------------------------
        self.next_section("piece-disque")
        titre = bandeau("Exemple : une pièce posée au bord d'un disque qui tourne",
                        "quel coefficient de frottement minimal pour qu'elle ne glisse pas ?")
        self.play(FadeIn(titre))
        c = np.array([-3.6, -0.6, 0])
        R = 2.0
        disque = Circle(radius=R, color=C_GRIS, fill_opacity=0.15).move_to(c)
        rayons = VGroup(*[Line(c, c + R * u(a), color=C_GRIS, stroke_width=1) for a in np.linspace(0, 2 * PI, 6, endpoint=False)])
        rot = VGroup(disque, rayons)
        ang = ValueTracker(0)
        piece = always_redraw(lambda: Circle(radius=0.16, color=ACCENT, fill_opacity=0.9).move_to(c + (R - 0.25) * u(ang.get_value())))
        ffr = always_redraw(lambda: fleche(c + (R - 0.25) * u(ang.get_value()), c + (R - 1.15) * u(ang.get_value()), ACCENT, width=6))
        lf = always_redraw(lambda: M(r"\vec f_s", size=26, color=ACCENT).move_to(c + (R - 0.7) * u(ang.get_value()) + 0.3 * u(ang.get_value() + PI / 2)))
        rayons.add_updater(lambda m, dt: m.rotate(dt * 1.2, about_point=c))
        self.play(FadeIn(rot))
        self.add(piece, ffr, lf)
        self.play(ang.animate.set_value(2 * PI), run_time=2 * PI / 1.2, rate_func=linear)
        eqs = VGroup(
            T("seul le frottement statique tire la pièce vers le centre :", size=20, color=C_GRIS),
            M(r"f_s = \frac{m v^2}{r} \qquad N = m g", size=32),
            T("à la limite du glissement, f_s = μs N :", size=20, color=C_GRIS),
            M(r"\mu_s\,m g = \frac{m v^2}{r} \;\Rightarrow\; \mu_s = \frac{v^2}{r g}", size=32),
            M(r"v = \frac{2\pi r}{T} \;\Rightarrow\; \mu_s = \frac{4\pi^2 r}{T^2 g}", size=36, color=ACCENT),
            T("la masse s'est simplifiée : grosse ou petite pièce, même résultat", size=20, color=C_VIT),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.2 + DOWN * 0.3)
        limiter(eqs, 6.8)
        for e in eqs:
            self.play(FadeIn(e, shift=UP * 0.1), ang.animate.increment_value(1.2 * 1.0), run_time=1.0, rate_func=linear)
            self.wait(0.4)
        self.play(ang.animate.increment_value(2 * PI), run_time=2 * PI / 1.2, rate_func=linear)
        rotor = T("Même raisonnement pour le « rotor » (fête foraine) : là, c'est N qui est centripète\n"
                  "et le frottement qui retient le poids  →  μs = T² g / (4π² r).",
                  size=20, color=C_GRIS).to_edge(DOWN, buff=0.2)
        limiter(rotor, 13)
        self.play(FadeIn(rotor))
        self.wait(4)
        rayons.clear_updaters()
        vider(self)
