# native
import sys
import time
from math import sin, cos, pi, sqrt
# 3rd party
import pygame
# own
from graphicdata import *

colors = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0)
}

sc_w = 800
sc_h = 600
xc = sc_w / 2
yc = sc_h / 2


def setup_coordinate_lines():
    global xc
    global yc
    global colors
    global xL, yL, zL
    L = 100
    p0 = Point(xc, yc, 0)
    px = Point(xc + L, yc, 0)
    py = Point(xc, yc - L, 0)
    pz = Point(xc, yc, L)
    xL = Line(p0, px, colors['red'])
    yL = Line(p0, py, colors['green'])
    zL = Line(p0, pz, colors['blue'])


def draw_coordinate_lines(screen):
    global xL, yL, zL
    draw_text(screen, colors['red'], 5, 0, "X")
    draw_text(screen, colors['green'], 5, 15, "Y")
    draw_text(screen, colors['blue'], 5, 30, "Z")
    xL.render(screen)
    yL.render(screen)
    zL.render(screen)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((sc_w, sc_h))
    screen.fill((255, 255, 255))
    setup_coordinate_lines()

    prism = FivePointPrismFilled(200, 200, 0)
    prism2 = FivePointPrism(400, 200, 0)
    prism3 = FivePointPrism(300, 400, 0)

    while True:
        screen.fill((255, 255, 255))
        draw_coordinate_lines(screen)
        # prism2.rotate_x(45)
        # prism3.rotate_z(45)
        prism.rotate_y(1)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_5:
                    prism.rotate_y(5)
                elif event.key == pygame.K_1:
                    prism.rotate_y(1)
                print prism.angle
            if event.type == pygame.QUIT:
                sys.exit()
        prism.render(screen)
        prism2.render(screen)
        prism3.render(screen)
        pygame.display.flip()
        time.sleep(0.1)
