"""
All nessesary function for graphic
"""
from math import sin, cos, pi, sqrt

import pygame


def deg_to_rad(deg):
    """
    Convert degrees to radians
    """
    return deg * pi / 180


def draw_text(screen, color, x, y, text):
    font = pygame.font.Font(None, 14)
    screen.blit(font.render(text, False, color), (x, y))


def multiply(point, matrix):
    return Point(
        matrix[1][1]*point.x + matrix[1][2]*point.y + matrix[1][3]*point.z,
        matrix[2][1]*point.x + matrix[2][2]*point.y + matrix[2][3]*point.z,
        matrix[3][1]*point.x + matrix[3][2]*point.y + matrix[3][3]*point.z
    )


def draw_dashed_line(screen, color, start, end):
    dx = - start[0] + end[0]
    dy = - start[1] + end[1]
    length = int(sqrt(dx*dx + dy*dy))
    if length != 0:
        slope_x = dx / length
        slope_y = dy / length
    else:
        slope_x = 0
        slope_y = 0

    dash_length = 5
    for index in range(0, length / dash_length, 2):
        tstart = (start[0] + (slope_x * index * dash_length),
                  start[1] + (slope_y * index * dash_length))
        tend = (start[0] + (slope_x * (index + 1) * dash_length),
                start[1] + (slope_y * (index + 1) * dash_length))
        pygame.draw.line(screen, color, tstart, tend, 1)
