from math import sin, cos

import pygame

from point import Point
from polygon import Polygon
from gfunc import deg_to_rad


class FivePointPrismFilled(object):

    # 1 - OK
    # 2 - OK

    colors = [
        (125, 125, 255), (255, 255, 0), (255, 0, 255), (0, 255, 0), (0, 0, 255)
    ]

    def __init__(self, x, y, z, r=40,
                 shx=40, shy=200, shz=40, angle=119, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.shx = shx
        self.shy = shy
        self.shz = shz
        self.color = color
        self.angle = angle
        self.bottom_base = self.get_base(
            self.x + shx / 2, self.y + shy / 2, self.z + shz / 2, self.r)
        self.top_base = self.get_base(
            self.x - shx / 2, self.y - shy / 2, self.z - shz / 2, self.r)
        self.refresh_polygons()
        self.rotate_y(angle)

    def get_base(self, x, y, z, r):
        return [
            Point(x + r * cos(deg_to_rad(i * (360 / 5))),
                  y, z + r * sin(deg_to_rad(i * (360 / 5)))) for i in range(5)
        ]

    def refresh_polygons(self):
        self.polygons = [
            Polygon(self.bottom_base)
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
                ], True, self.colors[i])
            )
        self.polygons.append(Polygon(self.top_base, True, (255, 0, 0)))

    def _refresh_visible(self):
        if self.angle > 1:
            self.polygons[5].visible = False
        if self.angle > 14:
            self.polygons[3].visible = True
        if self.angle > 27:
            self.polygons[1].visible = False
        if self.angle > 39:
            self.polygons[4].visible = True
        if self.angle > 49:
            self.polygons[2].visible = False
        if self.angle > 61:
            self.polygons[5].visible = True
        if self.angle > 71:
            self.polygons[3].visible = False
        if self.angle > 83:
            self.polygons[1].visible = True
        if self.angle > 95:
            self.polygons[4].visible = False
        if self.angle > 108:
            self.polygons[2].visible = True

    def render(self, screen):
        # print self.angle
        if self.need_refresh:
            self.need_refresh = False
            self._refresh_visible()
        for poly in self.polygons:
            poly.render(screen)

    def rotate_y(self, deg):
        self.angle = (self.angle + deg) % 120
        for poly in self.polygons:
            poly.rotate_y(self.x, self.y, self.z, deg)
        self.need_refresh = True
