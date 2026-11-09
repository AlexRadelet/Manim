from manim import *

class Pith(Scene):
    def construct(self):

        circ = Circle(radius = 3.4, color=RED)

        self.play(Create(circ))