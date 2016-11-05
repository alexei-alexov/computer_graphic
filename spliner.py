#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from math import cos, sin, log, pi

from numpy import matrix, array
from numpy.linalg import inv
import pygame


class Splinner(object):
    """
    This class make interpolation
    """

    def interpolate(self, base_table):
        """
        Return interpolated points
        """
        length = len(base_table)
        a = base_table[0][0]
        b = base_table[length-1][0]
        h = (b - a) / 4
        hl = (b - a) / (5 * (length - 1))
        step = 0.2

        B = [3*(base_table[i][1] - 2*base_table[i+1][1] + base_table[i+2][1]) for i in xrange(0, length-2)]
        A = []
        for i in xrange(length-2):
            A.append([4 if i == j else 1 if abs(j - i) == 1 else 0 for j in xrange(length-2)])
        A = array(A)
        Ainv = inv(A)
        Bv = Ainv.dot(B)

        cb = [0] + Bv.tolist() + [0]
        ca = [1.0 / 3 * (cb[i+1] - cb[i]) for i in xrange(length-1)]
        cc = [base_table[i+1][1] - base_table[i][1] - ca[i] - cb[i] for i in xrange(length-1)]
        cd = [base_table[i][1] for i in xrange(length-1)]
        table = []

        sections = int(1 / step)
        for base_row in xrange(length-1):
            for row in xrange(sections):
                t = row * step
                x = round(a + hl * (sections * base_row + row), 3)
                y = round(ca[base_row] * t ** 3 + cb[base_row] * t ** 2 + cc[base_row] * t + cd[base_row], 3)
                table.append([x, y])
        table.append([b, ca[length-2] + cb[length-2] + cc[length-2] + cd[length-2]])

        return table

class Utiler(object):
    """
    This class provides method to draw basis
    also it holds zoom and center of coordinates
    """
    SW = 0
    SH = 0
    ZOOMX = 100
    ZOOMY = 1
    BASIS_X_FREQ = 1
    BASIS_Y_FREQ = 20
    CX = 600
    CY = 500
    COLOR = (255, 255, 255)

    def draw_basis(self, screen):

        self.SW, self.SH = screen.get_size()
        self.CX = self.SW / 2
        self.CY = self.SH / 4 * 3


        # horizontal basis line
        pygame.draw.line(
            screen, self.COLOR, (0, self.CY), (self.SW, self.CY))
        for i in range(int(self.SW / self.ZOOMX * self.BASIS_X_FREQ)):
            base_right_x = self.CX + i * self.ZOOMX * self.BASIS_X_FREQ
            base_left_x = self.CX - i * self.ZOOMX * self.BASIS_X_FREQ
            pygame.draw.line(
                screen, self.COLOR,
                (base_right_x, self.CY - 1), (base_right_x, self.CY + 1))
            pygame.draw.line(
                screen, self.COLOR,
                (base_left_x, self.CY - 1), (base_left_x, self.CY + 1))
        # vertical basis line
        pygame.draw.line(
            screen, self.COLOR, (self.CX, 0), (self.CX, self.SH))
        for i in range(int(self.SH / self.ZOOMY * self.BASIS_Y_FREQ)):
            base_top_y = self.CY + i * self.ZOOMY * self.BASIS_Y_FREQ
            base_bottom_y = self.CY - i * self.ZOOMY * self.BASIS_Y_FREQ
            pygame.draw.line(
                screen, self.COLOR,
                (self.CX - 1, base_top_y), (self.CX + 1, base_top_y))
            pygame.draw.line(
                screen, self.COLOR,
                (self.CX - 1, base_bottom_y), (self.CX + 1, base_bottom_y))
        pygame.display.flip()


class FunctionDrawerTable(object):
    """
    This class draw given function
    """

    def __init__(self, table, color=(255, 255, 255), width=1):
        self.table = table
        self.color = color
        self.width = width

    def draw(self, screen, utiler):
        """
        This method draw func when x from a to b
        """

        length = len(self.table) - 1
        for i in xrange(length):
            p_1 = (
                round(self.table[i][0] * utiler.ZOOMX + utiler.CX),
                round(-self.table[i][1] * utiler.ZOOMY + utiler.CY)
            )
            p_2 = (
                round(self.table[i+1][0] * utiler.ZOOMX + utiler.CX),
                round(-self.table[i+1][1] * utiler.ZOOMY + utiler.CY)
            )
            pygame.draw.line(
                screen,
                self.color,
                p_1,
                p_2,
                self.width)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    utiler = Utiler()
    utiler.draw_basis(screen)

    table = [[1.5, 80],
             [1.58, 100.224],
             [1.66, 118.192],
             [1.74, 131.648],
             [1.82, 138.336],
             [1.9, 136],
             [1.98, 123,664],
             [2.06, 105.472],
             [2.14, 86.848],
             [2.22, 73.216],
             [2.3, 70],
             [2.38, 80.744],
             [2.46, 101.472],
             [2.54, 126.328],
             [2.62, 149.456],
             [2.7, 165],
             [2.78, 168.528],
             [2.86, 161.304],
             [2.94, 146.016],
             [3.02, 125.352],
             [3.1, 102]]

    base_table = [[1.5, 80], [1.9, 136], [2.3, 70], [2.7, 165], [3.1, 102]]
    intr = Splinner()
    f2 = FunctionDrawerTable(intr.interpolate(base_table), (255, 0, 0))
    f = FunctionDrawerTable(table, (255, 255, 255))
    f.draw(screen, utiler)
    f2.draw(screen, utiler)
    pygame.draw.line(screen, (255, 255, 150), (utiler.CX, utiler.CY), (utiler.CX + 10, utiler.CY), 1)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()
        time.sleep(0.1)
