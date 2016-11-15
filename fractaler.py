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


class DragonDrawer(object):
    """
    This class draw given function
    """

    def __init__(self, screen, n, color=(255, 0, 0), width=1):
        self.screen = screen
        self.n = n
        self.color = color
        self.width = width


    def draw_dragon(self, x1, y1, x2, y2, n):

        if n == 0:
            return

        k = 1 - float(n) / self.n

        color = (self.color[0] * k,
                 self.color[1] * k,
                 self.color[2] * k)
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), self.width)

        xn = (x1 + x2) / 2 + (y2 - y1) / 2
        yn = (y1 + y2) / 2 - (x2 - x1) / 2

        self.draw_dragon(x2, y2, xn, yn, n-1)
        self.draw_dragon(x1, y1, xn, yn, n-1)

    def draw(self, x1, y1, x2, y2):
        """
        This method draw func when x from a to b
        """
        self.draw_dragon(x1, y1, x2, y2, self.n)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    dragon = DragonDrawer(screen, 10, (255, 255, 255))
    dragon.draw(500, 300, 800, 600)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()
        time.sleep(0.1)
