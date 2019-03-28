import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    """

    """
    def __init__(self, xy):
        self._x = xy[0] or 0.0
        self._y = xy[1] or 0.0

    x = property()
    y = property()

    @x.getter
    def get_x(self):
        return self._x

    @y.getter
    def get_y(self):
        return self._y

    def __add__(self, other):
        return Vec2d(self._x + other[0], self._y + other[1])

    def __str__(self):
        return f"x = {self._x}, y = {self._y}"

    def __sub__(self, other):
        return Vec2d(self._x - other[0], self._y - other[1])

    def __mul__(self, k):
        return Vec2d(self._x * k, self._y * k)

    @staticmethod
    def vec_len(vec):
        return len(vec)

    def int_pair(self):
        return int(self._x), int(self._y)


class Polyline:
    """
    """
    def __init__(self, points=None, speeds=None, screenDim=SCREEN_DIM):
        self.points = points or []
        self.speeds = speeds or []
        self.gameDisplay = pygame.display.set_mode(screenDim)

    def set_point(self, point=None, speed=None):
        self.points.append(point or Vec2d())
        self.speeds.append(speed or 0)

    def get_point(self, alpha, deg=None):
        if deg is None:
            deg = len(self.points) - 1
        if deg == 0:
            return self.points[0]
        return (self.points[deg] * alpha) + self.get_point(self.points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, count=None):
        if not count:
            return self.points
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(i * alpha))
        return res

    # Персчитывание координат опорных точек
    def set_points(self):
        for p in range(Vec2d.vec_len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].get_x > SCREEN_DIM[0] or self.points[p].get_x < 0:
                self.speeds[p] = (- self._speeds[p][0], self.speeds[p][1])
            if self.points[p].get_y > SCREEN_DIM[1] or self.points[p].get_y < 0:
                self.speeds[p] = (self.speeds[p][0], -self.speeds[p][1])

    # "Отрисовка" точек
    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, Vec2d.vec_len(self.points) - 1):
                pygame.draw.line(self.gameDisplay, color, (int(self.points[p_n].get_x), int(self.points[p_n].get_y)),
                                 (int(self.points[p_n + 1].get_x), int(self.points[p_n + 1].get_y)), width)
        elif style == "points":
            for p in self.points:
                pygame.draw.circle(self.gameDisplay, color, p.int_pair(), width)


class Knot(Polyline):
    """

    """

    def __init__(self, points=None, speeds=None, screenDim=SCREEN_DIM):
        super().__init__(points, speeds, screenDim)

    def set_points(self, steps=None):
        super().set_points()
        self.points = self.get_knot(steps or 0)

    def get_knot(self, count):
        points = self.get_points()
        if Vec2d.vec_len(points) < 3:
            return []
        res = []
        for i in range(-2, Vec2d.vec_len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2] * 0.5))

            res.extend(self.get_points(ptn, count))
        return res


# Отрисовка справки
def draw_help(gameDisplay, steps):
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    knot = Knot(screenDim=SCREEN_DIM)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot = Knot(screenDim=SCREEN_DIM)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.set_point(Vec2d(event.pos), (random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        knot.draw_points()
        knot.draw_points("line", 3, color)

        # draw_points(points)

        if not pause:
            knot.set_points(steps)
            # knot.draw_points("line", 3, color)
        if show_help:
            draw_help(gameDisplay=gameDisplay, steps=steps)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)


if __name__ == "__main__":
    main()
