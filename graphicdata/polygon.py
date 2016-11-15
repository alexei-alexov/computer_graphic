import pygame

from point import Point


class Polygon(object):

    def __init__(self, points, visible=True, color_fill=None, color_line=None):
        self.points = points
        self.color = color_fill
        self.line_color = color_line
        self.rotated = False
        self.visible = visible
        self._make_raw_points()

    def render(self, screen):
        if not self.visible:
            return

        if self.rotated:
            self.rotated = False
            self._make_raw_points()
        length = len(self.points)
        if self.color:
            width = 0
            color = self.color
        else:
            width = 1
            color = (0, 0, 0)
        pygame.draw.polygon(screen, color, self.raw_points, width)

    def _make_raw_points(self):
        self.raw_points = [p.convert() for p in self.points]

    def rotate_x(self, x, y, z, deg):
        for p in self.points:
            p.rotate_x(x, y, z, deg)
        self.rotated = True

    def rotate_y(self, x, y, z, deg):
        for p in self.points:
            p.rotate_y(x, y, z, deg)
        self.rotated = True

    def rotate_z(self, x, y, z, deg):
        for p in self.points:
            p.rotate_z(x, y, z, deg)
        self.rotated = True
