import math
from abc import ABC, abstractmethod


class Base(ABC):

    def __init__(self, data, result):
        self.data = data
        self.result = result

    def get_answer(self):
        return [int(x >= 0.5) for x in self.data]

    def get_score(self):
        ans = self.get_answer()
        return sum([int(x == y) for (x, y) in zip(ans, self.result)]) \
               / len(ans)

    @abstractmethod
    def abstract_method(self, x, y):
        pass

    def get_loss(self):
        return [self.abstract_method(x, y) for (x, y) in zip(self.data, self.result)]


class A(Base):

    def abstract_method(self, x, y):
        return (x - y) * (x - y)

    def init(self, data, result):
        super().__init__(data, result)

    def get_loss(self):
        return sum(super().get_loss())


class B(Base):

    def abstract_method(self, x, y):
        print(f"X = {x}, Y = {y}")
        return y * math.log(x) + (1 - y) * math.log(1 - x)

    def init(self, data, result):
        super().__init__(data, result)

    def get_loss(self):
        return -sum(super().get_loss())

    def get_res(self, ans):
        return [int(x == 1 and y == 1) for (x, y) in zip(ans, self.result)]

    def get_pre(self):
        ans = self.get_answer()
        res = self.get_res(ans)
        print(f"get_pre ans = {ans}, res = {res}")
        return sum(res) / sum(ans)

    def get_rec(self):
        ans = self.get_answer()
        res = self.get_res(ans)
        print(f" get_rec ans = {ans}, res = {res}")
        return sum(res) / sum(self.result)

    def get_score(self):
        pre = self.get_pre()
        rec = self.get_rec()
        print(f"get_pre pre = {pre}, rec = {rec}")
        return 2 * pre * rec / (pre + rec)


class C(Base):

    def abstract_method(self, x, y):
        return abs(x - y)

    def init(self, data, result):
        super().__init__(data, result)

    def get_loss(self):
        return sum(super().get_loss())


if __name__ == "__main__":
    a = A([1, 2, 3, 4], [4, 5, 6])
    b = B([0.1, 0.8, 0.7], [4, 1, 6])
    c = C([1, 2, 3, 4], [4, 5, 6])

    result = a.get_loss()
    print(result)
    result = a.get_score()
    print(result)

    result = b.get_loss()
    print(result)
    result = b.get_score()
    print(result)

    result = c.get_loss()
    print(result)
    result = c.get_score()
    print(result)
