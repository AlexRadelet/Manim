"""3.1 — La première loi de Newton (principe d'inertie).

1. Aristote vs Galilée : avec frottement le palet s'arrête, sans frottement il ne s'arrête jamais.
2. La loi, encadrée.
3. Exemples du cours : la balle au bout d'une corde qu'on lâche, les étincelles d'une meule.

    manim -pql chapitres/physique-ch3-mouvement-2d/001-premiere-loi-newton/scene.py PremiereLoiNewton
"""

from shared.physique import *


class PremiereLoiNewton(Scene):
    def construct(self):
        carte_titre(self, "Chapitre 3 · section 3.1", "La première loi de Newton",
                    "Faut-il une force pour garder un objet en mouvement ?")

        # --- 1. Aristote vs Galilée ---------------------------------------------------
        self.next_section("aristote-galilee")
        titre = bandeau("Aristote (~350 av. J.-C.) vs Galilée (~1600)")
        self.play(FadeIn(titre))
        y1, y2 = 1.0, -2.0
        sol1 = Rectangle(width=13, height=0.25, color=C_SOL, fill_opacity=0.8, stroke_width=0)
        sol1.move_to([0, y1 - 0.37, 0])
        hachures = VGroup(*[Line([x, y1 - 0.25, 0], [x - 0.2, y1 - 0.5, 0], color=C_GRIS,
                                 stroke_width=2) for x in np.arange(-6.3, 6.5, 0.35)])
        glace = Rectangle(width=13, height=0.25, color=PRIMARY, fill_opacity=0.35, stroke_width=0)
        glace.move_to([0, y2 - 0.37, 0])
        l1 = T("avec frottement (sol rugueux)", size=22, color=C_GRIS).next_to(sol1, DOWN, buff=0.15)
        l2 = T("sans frottement (glace parfaite)", size=22, color=PRIMARY).next_to(glace, DOWN, buff=0.15)
        p1 = Square(0.5, color=ACCENT, fill_opacity=0.9).move_to([-6, y1, 0])
        p2 = Square(0.5, color=ACCENT, fill_opacity=0.9).move_to([-6, y2, 0])
        self.play(FadeIn(sol1), FadeIn(hachures), FadeIn(glace), FadeIn(l1), FadeIn(l2),
                  FadeIn(p1), FadeIn(p2))
        pousse = T("même poussée au départ, puis on lâche", size=24).move_to(UP * 2.4)
        self.play(FadeIn(pousse))

        t = ValueTracker(0)
        v0, dec, tstop = 3.0, 1.5, 2.0  # avec frottement : s'arrête après 2 s

        def x1(tt):
            tt = min(tt, tstop)
            return -6 + v0 * tt - 0.5 * dec * tt * tt

        def x2(tt):
            return -6 + v0 * tt

        p1.add_updater(lambda m: m.set_x(x1(t.get_value())))
        p2.add_updater(lambda m: m.set_x(x2(t.get_value())))
        self.play(t.animate.set_value(4.0), run_time=4, rate_func=linear)
        strobo = VGroup(*[Square(0.5, color=ACCENT, fill_opacity=0.25, stroke_width=1)
                          .move_to([x1(k * 0.4), y1, 0]) for k in range(11)],
                        *[Square(0.5, color=ACCENT, fill_opacity=0.25, stroke_width=1)
                          .move_to([x2(k * 0.4), y2, 0]) for k in range(11)])
        self.play(FadeIn(strobo, lag_ratio=0.05))
        self.play(FadeOut(pousse))
        c1 = T("Aristote : « les corps tendent naturellement vers le repos »", size=22,
               color=C_GRIS).move_to([0, y1 + 0.9, 0])
        c2 = T("Galilée : sans frottement, il garderait sa vitesse… pour toujours (inertie)",
               size=22, color=ACCENT).move_to([0, y2 + 0.9, 0])
        limiter(c2, 13)
        self.play(FadeIn(c1))
        self.wait(2)
        self.play(FadeIn(c2))
        espac = T("images à intervalles égaux : écarts égaux = vitesse constante",
                  size=20, color=C_GRIS).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(espac))
        self.wait(2)
        cle = T("Ce qui arrête le palet, ce n'est pas « le mouvement qui s'use » :\n"
                "c'est une FORCE, le frottement.", size=26, color=C_TEXTE)
        cle = encadre(cle).move_to(ORIGIN + DOWN * 0.5)
        self.play(FadeIn(cle))
        self.wait(4)
        p1.clear_updaters()
        p2.clear_updaters()
        vider(self)

        # --- 2. La loi ----------------------------------------------------------------
        self.next_section("enonce")
        titre = bandeau("Newton (1687) généralise l'idée de Galilée")
        loi = VGroup(
            T("Première loi de Newton", size=30, color=ACCENT, weight=BOLD),
            T("Tout corps conserve son état de repos ou de mouvement rectiligne uniforme,\n"
              "à moins que des forces extérieures ayant une résultante non nulle\n"
              "n'agissent sur lui et le contraignent à changer d'état.", size=24),
        ).arrange(DOWN, buff=0.35)
        loi = encadre(loi).move_to(UP * 0.6)
        traduction = VGroup(
            T("Autrement dit :", size=24, color=C_GRIS),
            T("forces qui s'annulent (ou aucune force)  →  v = constante (vecteur !)", size=24,
              color=C_VIT),
            T("pour CHANGER la vitesse (grandeur ou direction), il faut une force", size=24,
              color=C_ACC),
        ).arrange(DOWN, buff=0.18).next_to(loi, DOWN, buff=0.5)
        self.play(FadeIn(titre), FadeIn(loi))
        self.wait(3)
        for tr in traduction:
            self.play(FadeIn(tr, shift=UP * 0.1))
            self.wait(1)
        self.wait(3)
        vider(self)

        # --- 3. La balle au bout d'une corde -----------------------------------------------
        self.next_section("corde")
        titre = bandeau("On lâche la corde : où part la balle ?")
        self.play(FadeIn(titre))
        centre = LEFT * 2.5 + DOWN * 0.4
        R, w = 1.8, 2.2
        ang = ValueTracker(-PI / 2)
        main = Dot(centre, radius=0.12, color=C_GRIS)
        cercle = DashedVMobject(Circle(radius=R, color=C_GRIS).move_to(centre), num_dashes=40)

        def pos_corde():
            a = ang.get_value()
            return centre + R * np.array([np.cos(a), np.sin(a), 0])

        balle = always_redraw(lambda: particule(r=0.16).move_to(pos_corde()))
        corde = always_redraw(lambda: Line(centre, pos_corde(), color=C_TEXTE, stroke_width=2))
        self.play(FadeIn(main), Create(cercle), FadeIn(corde), FadeIn(balle))
        self.play(ang.animate.set_value(-PI / 2 + 4 * PI), run_time=4 * PI / w * 0.6,
                  rate_func=linear)
        # lâcher au sommet (angle = π/2) : la vitesse est alors horizontale, vers la gauche
        self.play(ang.animate.set_value(PI / 2 + 4 * PI), run_time=PI / w * 0.6,
                  rate_func=linear)
        p_lacher = pos_corde()
        balle.clear_updaters()
        self.remove(corde)
        lacher = T("on lâche !", size=24, color=ACCENT).next_to(p_lacher, UP, buff=0.25)
        tangente = DashedLine(p_lacher + RIGHT * 3, p_lacher + LEFT * 4.2, color=C_VIT,
                              stroke_width=2)
        self.add(lacher)
        self.play(balle.animate.move_to(p_lacher + LEFT * 4.0), run_time=4.0 / (R * w) / 0.6,
                  rate_func=linear)
        self.play(Create(tangente))
        reponse = VGroup(
            T("Elle part en ligne droite,\nselon la TANGENTE au cercle.", size=26, color=C_VIT),
            T("Plus de corde = plus de force vers le centre\n→ plus rien ne change sa vitesse.",
              size=22, color=C_GRIS),
            T("(l'air et la gravité finiront par courber\nla trajectoire, mais plus tard)",
              size=20, color=C_GRIS),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.8 + DOWN * 0.3)
        for r in reponse:
            self.play(FadeIn(r, shift=UP * 0.1))
            self.wait(1)
        piege = T("Piège classique : NON, elle ne continue pas à tourner,\n"
                  "et elle ne part pas vers l'extérieur (radialement).", size=22, color=C_NEG)
        piege.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(piege))
        self.wait(4)
        vider(self)

        # --- 4. Les étincelles d'une meule ----------------------------------------------------
        self.next_section("meule")
        titre = bandeau("Même chose pour les étincelles d'une meule")
        self.play(FadeIn(titre))
        cm, Rm = RIGHT * 1.5 + UP * 0.5, 1.6
        meule = VGroup(Circle(radius=Rm, color=C_GRIS, fill_opacity=0.35),
                       *[Line(ORIGIN, Rm * np.array([np.cos(a), np.sin(a), 0]), color=C_GRIS)
                         for a in np.linspace(0, 2 * PI, 8, endpoint=False)]).move_to(cm)
        self.play(FadeIn(meule))
        rot = Rotate(meule, angle=-6 * PI, about_point=cm, run_time=6.3, rate_func=linear)
        # rotation horaire : en bas à droite, la surface file vers le bas-gauche ; on
        # émet depuis plusieurs points proches, chacun suit SA tangente.
        etincelles = VGroup()
        rng = np.random.default_rng(3)
        anims = []
        for k in range(26):
            a = -PI / 2 + 0.5 + rng.uniform(-0.15, 0.15)  # autour du bas-droite
            p = cm + Rm * np.array([np.cos(a), np.sin(a), 0])
            tang = np.array([np.sin(a), -np.cos(a), 0])  # rotation horaire
            L = rng.uniform(2.2, 3.4)
            s = Line(p, p + tang * L, color=ACCENT, stroke_width=3)
            etincelles.add(s)
            anims.append(Succession(Wait(k * 0.2), ShowPassingFlash(s.copy(), time_width=0.4,
                                                                     run_time=1.0)))
        self.play(rot, *anims)
        trace = VGroup(*[s.copy().set_stroke(opacity=0.35, width=2) for s in etincelles[:8]])
        rayon = DashedLine(cm, cm + Rm * np.array([np.cos(-PI / 2 + 0.5), np.sin(-PI / 2 + 0.5), 0]),
                           color=C_TEXTE)
        self.play(FadeIn(trace), Create(rayon))
        txt = T("Chaque étincelle s'échappe en ligne droite\n"
                "selon la tangente au point où elle quitte la meule.", size=24, color=ACCENT)
        txt.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(txt))
        self.wait(4)
        vider(self)
