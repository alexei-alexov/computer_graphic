import pygame
import sys
import time
from math import sin, cos, pi, sqrt

colors = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0)
}


def deg_to_rad(deg):
    """
    Convert degrees to radians
    """
    return deg * pi / 180


class Point(object):
    """
    This is basic part of my world of graphic
    """
    def __init__(self, x, y, z, angle=-90, visible=True):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.visible = visible

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


class Line(object):

    def __init__(self, p1, p2, color=(0, 0, 0)):
        self.p1 = p1
        self.p2 = p2
        self.color = color

    def render(self, screen):
        pygame.draw.line(screen, self.color,
                         self.p1.convert(), self.p2.convert())


class Polygon(object):

    def __init__(self, points):
        self.points = points

    def render(self, screen):
        length = len(self.points)
        for i in range(length):
            point_one = self.points[i]
            point_two = self.points[(i+1) % length]
            if point_one.visible and point_two.visible:
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    self.points[i].convert(),
                    self.points[(i+1) % length].convert()
                )
            else:
                pygame.draw.line(
                    screen,
                    (255, 0, 0),
                    self.points[i].convert(),
                    self.points[(i+1) % length].convert()
                )

    def is_inside(self, point):
        n = len(self.points)
        inside = False
        p1x, p1y = self.points[0].convert()
        for i in range(n+1):
            p2x, p2y = self.points[i % n].convert()
            if point.y > min(p1y, p2y):
                if point.y <= max(p1y, p2y):
                    if point.x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (point.y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or point.x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside


class FivePointPrism(object):

    def __init__(self, x, y, z, r=40, shx=0, shy=200, shz=0, color=(0, 0, 0)):
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
        # self.refresh_lines()
        self.refresh_polygons()

    def get_base(self, x, y, z, r):
        return [
            Point(x + r * cos(deg_to_rad(i * (360 / 5))),
                  y, z + r * sin(deg_to_rad(i * (360 / 5)))) for i in range(5)
        ]

    def refresh_polygons(self):
        self.polygons = [
            Polygon(self.bottom_base),
            Polygon(self.top_base),
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
                ])
            )
            self.check_visible_points()

    def refresh_lines(self):
        self.lines = [
            # bottom figure
            Line(self.bottom_base[0], self.bottom_base[1]),
            Line(self.bottom_base[1], self.bottom_base[2]),
            Line(self.bottom_base[2], self.bottom_base[3]),
            Line(self.bottom_base[3], self.bottom_base[4]),
            Line(self.bottom_base[4], self.bottom_base[0]),
            # top figure
            Line(self.top_base[0], self.top_base[1]),
            Line(self.top_base[1], self.top_base[2]),
            Line(self.top_base[2], self.top_base[3]),
            Line(self.top_base[3], self.top_base[4]),
            Line(self.top_base[4], self.top_base[0]),
            # connectors
            Line(self.top_base[0], self.bottom_base[0]),
            Line(self.top_base[1], self.bottom_base[1]),
            Line(self.top_base[2], self.bottom_base[2]),
            Line(self.top_base[3], self.bottom_base[3]),
            Line(self.top_base[4], self.bottom_base[4]),
        ]
        self.check_visible_points()

    def check_visible_points(self):
        # this function set point state to visible or not
        for point in self.bottom_base + self.top_base:
            for polygon in self.polygons:
                point.visible = not polygon.is_inside(point)

    def render(self, screen):
        for poly in self.polygons:
            poly.render(screen)

    def rotate_x(self, deg):
        for point in self.bottom_base:
            point.rotate_x(self.x, self.y, self.z, deg)
        for point in self.top_base:
            point.rotate_x(self.x, self.y, self.z, deg)

    def rotate_y(self, deg):
        for point in self.bottom_base:
            point.rotate_y(self.x, self.y, self.z, deg)
        for point in self.top_base:
            point.rotate_y(self.x, self.y, self.z, deg)

    def rotate_z(self, deg):
        for point in self.bottom_base:
            point.rotate_z(self.x, self.y, self.z, deg)
        for point in self.top_base:
            point.rotate_z(self.x, self.y, self.z, deg)

sc_w = 800
sc_h = 600
xc = sc_w / 2
yc = sc_h / 2


def draw_text(screen, color, x, y, text):
    global font
    screen.blit(font.render(text, False, color), (x, y))


def multiply(point, matrix):
    return Point(
        matrix[1][1]*point.x + matrix[1][2]*point.y + matrix[1][3]*point.z,
        matrix[2][1]*point.x + matrix[2][2]*point.y + matrix[2][3]*point.z,
        matrix[3][1]*point.x + matrix[3][2]*point.y + matrix[3][3]*point.z
    )


def draw_dashed_line(screen, color, start, end):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
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
    font = pygame.font.Font(None, 14)
    screen = pygame.display.set_mode((sc_w, sc_h))
    screen.fill((255, 255, 255))
    setup_coordinate_lines()

    prism = FivePointPrism(200, 200, 0)
    prism2 = FivePointPrism(400, 200, 0)
    prism3 = FivePointPrism(300, 400, 0)
    while True:
        screen.fill((255, 255, 255))
        draw_coordinate_lines(screen)
        prism.render(screen)
        prism2.render(screen)
        prism3.render(screen)
        prism.rotate_y(5)
        prism2.rotate_x(5)
        prism3.rotate_z(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()
        time.sleep(0.1)
