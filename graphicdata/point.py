"""
This module contains point
"""
from math import sin, cos

import pygame

from gfunc import deg_to_rad


class Point(object):
    """
    This is basic part of my world of graphic
    """
    def __init__(self, x, y, z, angle=-90):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle

    def convert(self):
        return (
            self.x - self.z * cos(deg_to_rad(self.angle)),
            self.y - self.z * sin(deg_to_rad(self.angle)))

    def render(self, screen):
        screen.set_at(self.convert(), (0, 0, 0))

    def _centrise(self, xc, yc, zc):
        self.x -= xc
        self.y -= yc
        self.z -= zc

    def _uncentrise(self, xc, yc, zc):
        self.x += xc
        self.y += yc
        self.z += zc

    def rotate_x(self, xc, yc, zc, deg):
        self._centrise(xc, yc, zc)
        rad = deg_to_rad(deg)

        rsin = sin(rad)
        rcos = cos(rad)
        nx = self.x
        ny = self.y * rcos - self.z * rsin
        nz = self.y * rsin + self.z * rcos

        self.x = nx
        self.y = ny
        self.z = nz

        self._uncentrise(xc, yc, zc)

    def rotate_y(self, xc, yc, zc, deg):
        self._centrise(xc, yc, zc)
        rad = deg_to_rad(deg)

        rsin = sin(rad)
        rcos = cos(rad)
        nx = self.x * rcos + self.z * rsin
        ny = self.y
        nz = self.z * rcos - self.x * rsin

        self.x = nx
        self.y = ny
        self.z = nz

        self._uncentrise(xc, yc, zc)

    def rotate_z(self, xc, yc, zc, deg):
        self._centrise(xc, yc, zc)
        rad = deg_to_rad(deg)

        rsin = sin(rad)
        rcos = cos(rad)
        nx = self.x * rcos - self.y * rsin
        ny = self.y * rcos + self.x * rsin
        nz = self.z

        self.x = nx
        self.y = ny
        self.z = nz

        self._uncentrise(xc, yc, zc)

    def __repr__(self):
        return "(" + str(self.x) + " " + str(self.y) + " " + str(self.z) + ")"
