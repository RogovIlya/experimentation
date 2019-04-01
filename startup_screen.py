import pygame
import random
import math


class Vec2d:
    """
    класс 2-мерных векторов
    """

    def __init__(self, args=(0, 0)):
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

    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return (self._x * other.get_x) + (self._y * other.get_y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vec2d((self._x * other, self._y * other))

    def __len__(self):
        return int(math.sqrt(self._x * self._x + self._y * self._y))

    def int_pair(self):
        return int(self._x), int(self._y)


class Polyline:
    """
    класс замкнутых ломаных
    """

    def __init__(self, points=None, speeds=None):
        self.points = points or []
        self.speeds = speeds or []

    def add_point(self, point=None, speed=None):
        self.points.append(point or Vec2d())
        self.speeds.append(speed or Vec2d())

    def __str__(self):
        return f"points = {self.points}"

    # Персчитывание координат опорных точек
    def set_points(self, screenDim,  rate):
        for p in range(len(self.points)):
            self.points[p] += self.speeds[p] * rate
            if self.points[p].get_x > screenDim[0] or self.points[p].get_x < 0:
                self.speeds[p] = Vec2d((- self.speeds[p].get_x, self.speeds[p].get_y))
            if self.points[p].get_y > screenDim[1] or self.points[p].get_y < 0:
                self.speeds[p] = Vec2d((self.speeds[p].get_x, -self.speeds[p].get_y))

    # "Отрисовка" точек
    def draw_points(self, gameDisplay, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, self.points[p_n].int_pair(),
                                 self.points[p_n + 1].int_pair(), width)
        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color, p.int_pair(), width)

    def remove_last_point(self):
        self.points.remove(self.points[-1])
        self.speeds.remove(self.speeds[-1])


class Knot(Polyline):
    """
     РїРѕС‚РѕРјРѕРє РєР»Р°СЃСЃР° Polyline
    """

    def __init__(self, points=None, speeds=None):
        super().__init__(points, speeds)

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
        if len(points) < 3:
            return Knot()
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)

            res.extend(Knot.get_points(base_points=ptn, count=count))
        return Knot(res)


class App:

    SCREEN_DIM = (800, 600)
    LEFT = 1
    RIGHT = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5

    def __init__(self):
        self.rate = 1.0
        self.rate_step = 0.1
        self.gameDisplay = pygame.display.set_mode(App.SCREEN_DIM)

        self.steps = 35
        self.working = True
        self.points = []
        self.speeds = []
        self.show_help = False
        self.pause = True

        self.hue = 0
        self.color = pygame.Color(0)

        self.polyline = Polyline()

        self.event_button_handler = {
            self.RIGHT: lambda *args: self.polyline.remove_last_point(),
            self.LEFT: lambda *args: self.polyline.add_point(args[0], args[1]),
            self.SCROLL_DOWN: lambda *args: self.reduce_rate(),
            self.SCROLL_UP: lambda *args: self.increase_rate()
        }

    def reduce_rate(self):
        if self.rate > 0.1:
            self.rate = round(self.rate - self.rate_step, 1)

    def increase_rate(self):
        if self.rate < 2.0:
            self.rate = round(self.rate + self.rate_step, 1)

    def draw_help(self):
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Right mouse click", "Remove last point and speed"])
        data.append(["Scroll up mouse", "It increase rate"])
        data.append(["Scroll down mouse", "It reduce rate"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 35 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (400, 100 + 35 * i))

    def run(self):
        pygame.init()
        pygame.display.set_caption("MyScreenSaver")

        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.polyline = Polyline()
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    handler = self.event_button_handler[event.button]
                    handler(Vec2d(event.pos), Vec2d((random.random() * 2, random.random() * 2)))

            self.gameDisplay.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)

            self.polyline.draw_points(self.gameDisplay)

            knot = Knot.get_knot(self.polyline.points, self.steps)
            knot.draw_points(self.gameDisplay, "line", 3, self.color)

            if not self.pause:
                self.polyline.set_points(self.SCREEN_DIM, self.rate)
            if self.show_help:
                self.draw_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
