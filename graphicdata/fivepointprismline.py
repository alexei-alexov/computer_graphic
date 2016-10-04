from math import sin, cos

import pygame

from point import Point
from line import Line
from gfunc import deg_to_rad, draw_dashed_line


class FivePointPrismLine(object):

    def __init__(self, x, y, z, r=40, shx=0, shy=200, shz=0,
                 angle=0, color=(0, 0, 0)):
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
        self.angle = angle
        self.refresh_lines()
        self.rotate_y(angle)
        self.lines[11].visible = False
        self.lines[9].visible = False
        self.lines[6].visible = False

    def get_base(self, x, y, z, r):
        return [
            Point(x + r * cos(deg_to_rad(i * (360 / 5))),
                  y, z + r * sin(deg_to_rad(i * (360 / 5)))) for i in range(5)
        ]

    def refresh_lines(self):
        self.lines = []
        length = len(self.bottom_base)
        for i in range(length):
            self.lines.append(
                Line(
                    self.bottom_base[i],
                    self.bottom_base[(i+1) % length],
                )
            )
            self.lines.append(
                Line(
                    self.top_base[i],
                    self.top_base[(i+1) % length],
                )
            )
            self.lines.append(
                Line(
                    self.top_base[i],
                    self.bottom_base[i],
                )
            )

    def render(self, screen):
        for line in self.lines:
            line.render(screen)

    def check_visible_lines(self):
        if self.angle > 10:
            self.lines[14].visible = False
            self.lines[12].visible = False
        if self.angle > 40:
            self.lines[11].visible = True
            self.lines[6].visible = True
        if self.angle > 76:
            self.lines[2].visible = False
            self.lines[0].visible = False
        if self.angle > 114:
            self.lines[14].visible = True
            self.lines[9].visible = True
        if self.angle > 150:
            self.lines[5].visible = False
            self.lines[3].visible = False
        if self.angle > 185:
            self.lines[2].visible = True
            self.lines[12].visible = True
        if self.angle > 220:
            self.lines[8].visible = False
            self.lines[6].visible = False
        if self.angle > 255:
            self.lines[5].visible = True
            self.lines[0].visible = True
        if self.angle > 295:
            self.lines[11].visible = False
            self.lines[9].visible = False
        if self.angle > 330:
            self.lines[8].visible = True
            self.lines[3].visible = True

    def rotate_y(self, deg):
        self.angle = (self.angle + deg) % 360
        for point in self.bottom_base:
            point.rotate_y(self.x, self.y, self.z, deg)
        for point in self.top_base:
            point.rotate_y(self.x, self.y, self.z, deg)
        self.check_visible_lines()
