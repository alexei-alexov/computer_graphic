import pygame

from point import Point


class Line(object):

    def __init__(self, p1, p2, color=(0, 0, 0)):
        self.p1 = p1
        self.p2 = p2
        self.color = color

    def render(self, screen):
        pygame.draw.line(screen, self.color,
                         self.p1.convert(), self.p2.convert())
