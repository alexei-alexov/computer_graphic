#!/usr/bin/env python
# -*- utf-8 -*-
import sys
import random
import time

import pygame

from graphicdata import *
from fractaler import DragonDrawer


class Consts(object):

    SCREEN_WIDTH = -1
    SCREEN_HEIGHT = -1

    PRISMS_MAX_WIDTH = 50
    PRISMS_MAX_HEIGHT = 50

    PRISMS_MAX_WSPD = 6.0
    PRISMS_MIN_WSPD = -6.0

    PRISMS_MAX_HSPD = 6.0
    PRISMS_MIN_HSPD = -6.0

    @classmethod
    def set_screen(cls, sc_w, sc_h):
        cls.SCREEN_WIDTH = sc_w
        cls.SCREEN_HEIGHT = sc_h
        cls.PRISMS_MAX_X = cls.SCREEN_WIDTH - cls.PRISMS_MAX_WIDTH
        cls.PRISMS_MAX_Y = cls.SCREEN_HEIGHT - cls.PRISMS_MAX_HEIGHT


def genX():
    """
    Return possible prims`s coordinate X to be created in it
    """
    global Consts
    return random.random() * (Consts.PRISMS_MAX_X)


def genHSPD():
    """
    Return prism`s horizontal speed
    """
    global Consts
    return round(Consts.PRISMS_MIN_WSPD + random.random() * (Consts.PRISMS_MAX_WSPD + abs(Consts.PRISMS_MIN_WSPD)), 3)


def genY():
    """
    Return possible Y coordinate
    """
    global Consts
    return random.random() * (Consts.PRISMS_MAX_Y)

def getRotate():
    return random.choice([-0.5, -0.2, -1, 0, 1, 0.5, 0.2])

def genVSPD():
    """
    Return prism`s vertical speed
    """
    global Consts
    return round(Consts.PRISMS_MIN_HSPD + random.random() * (Consts.PRISMS_MAX_HSPD + abs(Consts.PRISMS_MIN_HSPD)), 3)


def genZ():
    return -40 + random.random() * 80


def move_prisms(prisms):
    global Consts
    for i in xrange(len(prisms)):
        prism = prisms[i]
        if i == 0:
            print ">> ", prism.angle_y

        prism.change_coordinates(prism.x + prism.hspd, prism.y + prism.vspd, prism.z)
        prism.rotate_x(prism.aspd_x)
        prism.rotate_y(prism.aspd_y)
        prism.rotate_z(prism.aspd_z)

        if prism.x < 0 or prism.x > Consts.PRISMS_MAX_X:
            prism.hspd *= -1

        if prism.y < 0 or prism.y > Consts.PRISMS_MAX_Y:
            prism.vspd *= -1


def getR():
    return round(10 + random.random() * 40.0)


def getShiftXZ():
    return round(-40 + random.random() * 80.0)


def getShiftY():
    return round(50 + random.random() * 250.0)


def getAngle():
    return round(-25 + random.random() * 25.0)


def getColor():
    return (round(random.random() * 255.0), round(random.random() * 255.0), round(random.random() * 255.0))


def getPoint():
    return random.randrange(0, Consts.SCREEN_WIDTH)


def getPointY():
    return random.randrange(0, Consts.SCREEN_HEIGHT) - (Consts.SCREEN_WIDTH - Consts.SCREEN_HEIGHT)


def getFractalSurface():
    surface = pygame.Surface((int(Consts.SCREEN_WIDTH), int(Consts.SCREEN_WIDTH)))
    surface.fill((0, 0, 0))

    for i in xrange(8):
        dragon = DragonDrawer(surface, random.choice([4, 5, 6, 7, 8, 9, 10]), getColor(), random.choice([3, 4, 5, 8, 10]))
        dragon.draw(getPoint(), getPoint(), getPoint(), getPoint())
    return surface


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    Consts.set_screen(*screen.get_size())

    prisms = []

    fractalSurface = getFractalSurface()

    for i in xrange(20):
        prisms.append(FivePointPrism(genX(), genY(), genZ(), getR(),
                                     getShiftXZ(), getShiftY(), getShiftXZ(),
                                     getAngle(), getAngle(), getAngle(), getColor()))
        prisms[i].hspd = genHSPD()
        prisms[i].vspd = genVSPD()
        prisms[i].aspd_x = getRotate()
        prisms[i].aspd_y = getRotate()
        prisms[i].aspd_z = getRotate()
        # print prisms[i].hspd
        # print prisms[i].vspd


    while True:
        screen.fill((255, 255, 255))

        screen.blit(fractalSurface, (0, 0))

        for prism in prisms:
            prism.render(screen)

        move_prisms(prisms)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            if event.type == pygame.QUIT:
                sys.exit(0)

        time.sleep(0.01)
