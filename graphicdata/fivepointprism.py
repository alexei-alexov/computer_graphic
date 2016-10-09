from math import sin, cos

import pygame

from point import Point
from polygon import Polygon
from gfunc import deg_to_rad


class FivePointPrism(object):

    def __init__(self, x, y, z, r=40, shx=0, shy=200, shz=0, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.shx = shx
        self.shy = shy
        self.shz = shz
        self.color = color
        self.bottom_base = self.get_base(
            self.x + shx / 2, self.y + shy / 2, self.z + shz / 2, self.r)
        self.top_base = self.get_base(
            self.x - shx / 2, self.y - shy / 2, self.z - shz / 2, self.r)
        self.refresh_polygons()

    def get_base(self, x, y, z, r):
        return [
            Point(x + r * cos(deg_to_rad(i * (360 / 5))),
                  y, z + r * sin(deg_to_rad(i * (360 / 5)))) for i in range(5)
        ]

    def refresh_polygons(self):
        self.polygons = [
            Polygon(self.bottom_base),
            Polygon(self.top_base),
        ]
        length = len(self.bottom_base)
        for i in range(length):
            j = (i + 1) % length
            self.polygons.append(
                Polygon([
                    self.bottom_base[i],
                    self.bottom_base[j],
                    self.top_base[j],
                    self.top_base[i],
                ])
            )

    def render(self, screen):
        for poly in self.polygons:
            poly.render(screen)

    def rotate_x(self, deg):
        for poly in self.polygons:
            poly.rotate_x(self.x, self.y, self.z, deg)

    def rotate_y(self, deg):
        for poly in self.polygons:
            poly.rotate_y(self.x, self.y, self.z, deg)

    def rotate_z(self, deg):
        for poly in self.polygons:
            poly.rotate_z(self.x, self.y, self.z, deg)
