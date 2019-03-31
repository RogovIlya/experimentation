import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    """
    класс 2-мерных векторов
    """

    def __init__(self, args):
        self._x = args[0] or 0
        self._y = args[1] or 0

    x = property()
    y = property()

    @x.getter
    def get_x(self):
        return self._x

    @y.getter
    def get_y(self):
        return self._y

    def __add__(self, other):
        return Vec2d((self._x + other.get_x, self._y + other.get_y))

    def __str__(self):
        return f"(x = {self._x}, y = {self._y})"

    def __repr__(self):
        return self.__str__()

    def __sub__(self, other):
        return Vec2d((self._x - other.get_x, self._y - other.get_y))

    def __mul__(self, k):
        return Vec2d((self._x * k, self._y * k))

    def __len__(self):
        return int(math.sqrt(self._x * self._x + self._y * self._y))

    def int_pair(self):
        return int(self._x), int(self._y)


class Polyline:
    """
    класс замкнутых ломаных
    """

    def __init__(self, points=None, speeds=None, screenDim=SCREEN_DIM):
        self.points = points or []
        self.speeds = speeds or []
        self.gameDisplay = pygame.display.set_mode(screenDim)

    def add_point(self, point=None, speed=None):
        self.points.append(point or Vec2d())
        self.speeds.append(speed or 0)

    def __str__(self):
        return f"points = {self.points}"

    # Персчитывание координат опорных точек
    def set_points(self, points, speeds):
        print(f"poinets = {points}, speeds = {speeds}")
        for p in range(len(points)):
            points[p] = points[p] + speeds[p]
            if points[p].get_x > SCREEN_DIM[0] or points[p].get_x < 0:
                speeds[p] = Vec2d((- speeds[p].get_x, speeds[p].get_y))
            if points[p].get_y > SCREEN_DIM[1] or points[p].get_y < 0:
                speeds[p] = Vec2d((speeds[p].get_x, -speeds[p].get_y))
        self.points = points

    # "Отрисовка" точек
    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        print(f"pints={self.points}")
        if style == "line":
            # print("draw line")
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(self.gameDisplay, color, self.points[p_n].int_pair(),
                                 self.points[p_n + 1].int_pair(), width)
        elif style == "points":
            # print("draw points")
            for p in self.points:
                pygame.draw.circle(self.gameDisplay, color, p.int_pair(), width)


class Knot(Polyline):
    """
     потомок класса Polyline
    """

    def __init__(self, points=None, speeds=None, screenDim=SCREEN_DIM):
        super().__init__(points, speeds, screenDim)

    # Сглаживание ломаной
    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + Knot.get_point(points, alpha, deg - 1) * (1 - alpha)

    @staticmethod
    def get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot.get_point(base_points, i * alpha))
        return res

    @classmethod
    def get_knot(cls, points, count):
        # points = self.points
        if len(points) < 3:
            return Knot()
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)

            res.extend(Knot.get_points(ptn, count))
        return Knot(res)


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


# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                    knot = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(Vec2d(event.pos))
                speeds.append(Vec2d((random.random() * 2, random.random() * 2)))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        polyline = Polyline(points, speeds)
        polyline.draw_points()
        knot = Knot.get_knot(points, steps)
        knot.draw_points("line", 3, color)

        if not pause:
            polyline.set_points(points, speeds)
        if show_help:
            draw_help(gameDisplay, steps)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
