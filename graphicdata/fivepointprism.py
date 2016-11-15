from math import sin, cos

import pygame

from point import Point
from polygon import Polygon
from gfunc import deg_to_rad


class FivePointPrism(object):

    def __init__(self, x, y, z, r=40, shx=0, shy=200, shz=0,
                 angle_x=0, angle_y=0, angle_z=0, color=(0, 0, 0)):
        self.r = r
        self.shx = shx
        self.shy = shy
        self.shz = shz
        self.color = color
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z
        self.change_coordinates(x, y, z)
        self.rotate_x(self.angle_x)
        self.rotate_y(self.angle_y)
        self.rotate_z(self.angle_z)

    def change_coordinates(self, nx, ny, nz):
        self.x = nx
        self.y = ny
        self.z = nz
        self.bottom_base = self.get_base(
            self.x + self.shx / 2, self.y + self.shy / 2, self.z + self.shz / 2, self.r)
        self.top_base = self.get_base(
            self.x - self.shx / 2, self.y - self.shy / 2, self.z - self.shz / 2, self.r)
        self.refresh_polygons()

    def get_base(self, x, y, z, r):
        return [
            Point(x + r * cos(deg_to_rad(i * (360 / 5))),
                  y, z + r * sin(deg_to_rad(i * (360 / 5)))) for i in range(5)
        ]

    def refresh_polygons(self):
        self.polygons = [
            Polygon(self.bottom_base, color_fill=self.color),
            Polygon(self.top_base, color_fill=self.color),
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
                ], color_fill=self.color)
            )

    def render(self, screen):
        for poly in self.polygons:
            poly.render(screen)

    def rotate_x(self, deg):
        self.angle_x = (self.angle_x + deg) % 360
        for poly in self.polygons:
            poly.rotate_x(self.x, self.y, self.z, self.angle_x)

    def rotate_y(self, deg):
        self.angle_y = (self.angle_y + deg) % 360
        for poly in self.polygons:
            poly.rotate_y(self.x, self.y, self.z, self.angle_y)

    def rotate_z(self, deg):
        self.angle_z = (self.angle_z + deg) % 360
        for poly in self.polygons:
            poly.rotate_z(self.x, self.y, self.z, self.angle_z)
