from typing import List


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.x, self.y}"

    __str__ = __repr__


class Rectangle:

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return "{" + f"{self.p1.x}, {self.p1.y}, {self.p2.x}, {self.p2.y}" + "}"

    __str__ = __repr__

    def cross_square(self, other_p1: Point, other_p2: Point):
        if other_p2.x < self.p1.x or self.p2.x < other_p1.x:
            return False
        if other_p2.y < self.p1.y or self.p2.y < other_p1.y:
            return False
        return True


class Compartment(Rectangle):

    def __init__(self, name: str, p1: Point, p2: Point, damage_limit: int):
        super().__init__(p1, p2)
        self.name = name
        self.damage_limit = damage_limit

    def __repr__(self):
        return (f"{self.name}: " + "{" + f"{self.p1.x}, {self.p1.y}, {self.p2.x}, {self.p2.y}, {self.damage_limit}"
                + "}")

    __str__ = __repr__


class Empty(Rectangle):

    def __init__(self, p1: Point, p2: Point):
        super().__init__(p1, p2)


class Hit(Rectangle):

    def __init__(self, p1: Point, p2: Point, damage: int):
        super().__init__(p1, p2)
        self.damage = damage

    def __repr__(self):
        return "{" + f"{self.p1.x}, {self.p1.y}, {self.p2.x}, {self.p2.y}" + "} " + str(self.damage)


class Ship:

    def __init__(self, N, M, H, L, C, empties, compartments):
        self.N: int = N + 1
        self.M: int = M + 1
        self.H: int = H
        self.L: int = L
        self.C: int = C
        self.empties: List[Empty] = empties
        self.compartments: List[Compartment] = compartments
        self.xy: BIT2D = BIT2D(N + 1, M + 1)
        self.x: BIT2D = BIT2D(N + 1, M + 1)
        self.y: BIT2D = BIT2D(N + 1, M + 1)
        self.i: BIT2D = BIT2D(N + 1, M + 1)
        self.__default_empties = len(self.empties)
        self.destroyed = False

    def __repr__(self):
        return f"{self.N, self.M, self.H, self.L, self.C, self.empties, self.compartments}"

    __str__ = __repr__

    def get_BIT_view(self, name: str):
        bit = None
        match name:
            case "xy":
                bit = self.xy
            case "y":
                bit = self.y
            case "x":
                bit = self.x
            case "i":
                bit = self.i
        res = [[0 for _ in range(self.N)] for _ in range(self.M)]
        for i in range(self.N):
            for j in range(self.M):
                res[j][i] = bit.get_prefix_sum(Point(i, j))

        print(name)

        for i in range(self.M):
            print(res[i])
        print()

    def update(self, p1: Point, p2: Point, c: int):
        self.xy.update_r(p1, p2, c)
        self.x.update_r(p1, p2, -c * (p1.y - 1))
        self.x.update_r(Point(p1.x, p2.y + 1), Point(p2.x, self.M), c * (p2.y - p1.y + 1))
        self.y.update_r(p1, p2, -c * (p1.x - 1))
        self.y.update_r(Point(p2.x + 1, p1.y), Point(self.N, p2.y), c * (p2.x - p1.x + 1))
        self.i.update_r(p1, p2, c * (p1.x - 1) * (p1.y - 1))
        self.i.update_r(Point(p2.x + 1, p1.y), Point(self.N, p2.y), -c * (p1.y - 1) * (p2.x - p1.x + 1))
        self.i.update_r(Point(p1.x, p2.y + 1), Point(p2.x, self.M), -c * (p1.x - 1) * (p2.y - p1.y + 1))
        self.i.update_r(Point(p2.x + 1, p2.y + 1), Point(self.N, self.M), c * (p2.x - p1.x + 1) * (p2.y - p1.y + 1))
        # self.get_BIT_view("xy")
        # self.get_BIT_view("x")
        # self.get_BIT_view("y")
        # self.get_BIT_view("i")
        # input()

    def sum_p(self, p):
        a = self.xy.get_prefix_sum(p)
        b = self.x.get_prefix_sum(p)
        c = self.y.get_prefix_sum(p)
        d = self.i.get_prefix_sum(p)
        return a * p.x * p.y + b * p.x + c * p.y + d

    def sum_square(self, p1, p2):
        return self.sum_p(p2) + self.sum_p(Point(p1.x - 1, p1.y - 1)) - self.sum_p(Point(p1.x - 1, p2.y)) - self.sum_p(
            Point(p2.x, p1.y - 1))

    # def get_message(self, ):


class BIT2D:

    def __init__(self, N: int, M: int):
        self.s = [[0 for _ in range(N)] for _ in range(M)]
        self.N = N
        self.M = M

    @staticmethod
    def f(x):
        return x & (x + 1)

    @staticmethod
    def g(x):
        return x | (x + 1)

    def update_p(self, p: Point, val: int):
        x = p.x

        while x < self.N:
            y = p.y
            while y < self.M:
                self.s[y][x] += val
                y = self.g(y)
            x = self.g(x)

    def get_prefix_sum(self, p: Point):
        ans = 0

        y = p.y

        while y >= 0:
            x = p.x
            while x >= 0:
                ans += self.s[y][x]
                x = self.f(x) - 1
            y = self.f(y) - 1
        return ans

    def sum_r(self, p1: Point, p2: Point):
        tmp_p1 = Point(p1.x, p2.y)
        tmp_p2 = Point(p2.x, p1.y)
        s1 = self.get_prefix_sum(p2)
        s2 = self.get_prefix_sum(tmp_p1)
        s3 = self.get_prefix_sum(tmp_p2)
        s4 = self.get_prefix_sum(p1)
        return s1 - s2 - s3 + s4

    def get_val(self, p: Point):
        if p.x == 0 and p.y == 0:
            return self.get_prefix_sum(Point(0, 0))
        if p.x == 0:
            return self.get_prefix_sum(p) - self.get_prefix_sum(Point(p.x, p.y - 1))
        if p.y == 0:
            return self.get_prefix_sum(p) - self.get_prefix_sum(Point(p.x - 1, p.y))
        return self.sum_r(Point(p.x - 1, p.y - 1), p)

    def update_r(self, p1: Point, p2: Point, val: int):
        p2 = Point(p2.x + 1, p2.y + 1)
        self.update_p(p2, val)
        self.update_p(Point(p1.x, p2.y), -val)
        self.update_p(Point(p2.x, p1.y), -val)
        self.update_p(p1, val)

    def __repr__(self):
        return self.s.__str__().replace("],", "],\n")

    __str__ = __repr__
