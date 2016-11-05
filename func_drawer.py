#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from math import cos, sin, log, pi

import pygame


class Utiler(object):
    """
    This class provides method to draw basis
    also it holds zoom and center of coordinates
    """
    SW = 100
    SH = 800
    ZOOM = 500
    E = 0.001
    CX = SW / 2
    CY = SH / 4 * 3
    COLOR = (255, 255, 255)

    def draw_basis(self, screen):

        self.SW, self.SH = screen.get_size()
        self.CX = self.SW / 2
        self.CY = self.SH / 4 * 3

        EF = self.ZOOM * self.E
        # horizontal basis line
        pygame.draw.line(
            screen, self.COLOR, (0, self.CY), (self.SW, self.CY))
        for i in range(int(self.SW / EF)):
            base_right_x = self.CX + i * EF
            base_left_x = self.CX - i * EF
            pygame.draw.line(
                screen, self.COLOR,
                (base_right_x, self.CY - 1), (base_right_x, self.CY + 1))
            pygame.draw.line(
                screen, self.COLOR,
                (base_left_x, self.CY - 1), (base_left_x, self.CY + 1))
        # vertical basis line
        pygame.draw.line(
            screen, self.COLOR, (self.CX, 0), (self.CX, self.SH))
        for i in range(int(self.SH / EF)):
            base_top_y = self.CY + i * EF
            base_bottom_y = self.CY - i * EF
            pygame.draw.line(
                screen, self.COLOR,
                (self.CX - 1, base_top_y), (self.CX + 1, base_top_y))
            pygame.draw.line(
                screen, self.COLOR,
                (self.CX - 1, base_bottom_y), (self.CX + 1, base_bottom_y))
        pygame.display.flip()


class FunctionDrawer(object):
    """
    This class draw given function
    """

    def __init__(self, func, color=(255, 0, 0), width=1):
        self.func = func
        self.color = color
        self.width = width

    def get_line(self, x, E, ZOOM, CX, CY):
        x1 = x
        y1 = self.func(x1)
        x2 = x + E
        y2 = self.func(x2)
        x1 = x1 * ZOOM + CX
        y1 = CY - y1 * ZOOM
        x2 = x2 * ZOOM + CX
        y2 = CY - y2 * ZOOM
        return (x1, y1), (x2, y2)

    def draw(self, screen, utiler, a, b):
        """
        This method draw func when x from a to b
        """
        ZOOM = utiler.ZOOM
        E = utiler.E
        CX = utiler.CX
        CY = utiler.CY

        length = int((b - a) / E)
        print a, b, length
        for i in range(length):
            try:
                p1, p2 = self.get_line(a + i * E, E, ZOOM, CX, CY)
                pygame.draw.line(
                    screen,
                    self.color,
                    p1, p2,
                    self.width)

            except Exception, error:
                pass
        pygame.display.flip()


class FunctionDrawerPolar(FunctionDrawer):

    def get_line(self, fi, E, ZOOM, CX, CY):
        """
        Get line in polar coordinate system
        """
        ZOOM *= E
        fi1 = fi
        p1 = self.func(fi1)
        fi2 = fi + E
        p2 = self.func(fi2)
        x1 = ZOOM * (p1 * cos(fi1)) + CX
        y1 = CY - p1 * sin(fi1) * ZOOM
        x2 = ZOOM * (p2 * cos(fi2)) + CX
        y2 = CY - p2 * sin(fi2) * ZOOM
        # print x1, y1, x2, y2
        return (x1, y1), (x2, y2)


class FunctionDrawerParametrised(FunctionDrawer):

    """
    This class draw given function
    """

    def __init__(self, func_x, func_y, color=(255, 0, 0), width=1):
        self.func_x = func_x
        self.func_y = func_y
        self.color = color
        self.width = width

    def get_line(self, t, E, ZOOM, CX, CY):
        ZOOM *= E
        x1 = self.func_x(t)
        y1 = self.func_y(t)
        t2 = t + E
        x2 = self.func_x(t2)
        y2 = self.func_y(t2)
        x1 = x1 * ZOOM + CX
        y1 = CY - y1 * ZOOM
        x2 = x2 * ZOOM + CX
        y2 = CY - y2 * ZOOM
        return (x1, y1), (x2, y2)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    utiler = Utiler()
    utiler.draw_basis(screen)

    def func1(x):
        return x + 1 / x

    def func2(x):
        return 1 + 1 / x

    def func3(x):
        return 100 * cos(log(x)) + 150

    def func4_x(t):
        return 110 * cos(t) - 5 * cos(11 * t)

    def func4_y(t):
        return 110 * sin(t) - 5 * sin(11 * t)

    # f1 = FunctionDrawer(func1, width=2)
    # f1.draw(screen, utiler, -500, 500)
    # f2 = FunctionDrawer(func2, (0, 255, 0))
    # f2.draw(screen, utiler, -500, 500)

    # # 6.28
    # # polar system
    # f3 = FunctionDrawerPolar(func3, (255, 255, 255))
    # f3.draw(screen, utiler, 0, 6.28)
    # # parametrised
    f4 = FunctionDrawerParametrised(func4_x, func4_y, (255, 255, 255))
    f4.draw(screen, utiler, 0, 6.28)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()
        time.sleep(0.1)
