import pygame

from point import Point

from gfunc import draw_dashed_line


class Line(object):

    def __init__(self, p1, p2, color=(0, 0, 0), visible=True):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.visible = visible

    def render(self, screen):
        if self.visible:
            pygame.draw.line(screen, self.color,
                             self.p1.convert(), self.p2.convert())
        else:
            draw_dashed_line(screen, self.color,
                             self.p1.convert(), self.p2.convert())
