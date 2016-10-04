import pygame

from point import Point


class Polygon(object):

    def __init__(self, points):
        self.points = points

    def render(self, screen):
        length = len(self.points)
        for i in range(length):
            pygame.draw.line(
                screen,
                (0, 0, 0),
                self.points[i].convert(),
                self.points[(i+1) % length].convert()
            )
