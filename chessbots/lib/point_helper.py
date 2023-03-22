from collections import namedtuple
import math
from typing import Self

# Point = namedtuple('Point', 'x y')
Color = namedtuple('Color', 'r g b')


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.raw = self.x, self.y
        self.txt = str(self.x) + 'x' + str(self.y)

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return self.txt

    def add(self, other: Self):
        return Point(self.x + other.x, self.y + other.y)

    def sub(self, other: Self):
        return Point(self.x - other.x, self.y - other.y)

    def mult(self, factor: int):
        return Point(self.x * factor, self.y * factor)

    def in_area(self, area: [Self, Self]):
        return area[0].x < self.x < area[1].x and area[0].y < self.y < area[1].y

    def distance(self, other: Self):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def angle(self, a: Self, c: Self) -> float:
        return math.degrees(math.atan2(c.y - self.y, c.x - self.x) - math.atan2(a.y - self.y, a.x - self.x))

    def flip(self) -> Self:
        return Point(self.y, self.x)


def add_points(point_a: Point, point_b: Point) -> Point:
    return point_a.add(point_b)


def sub_points(point_a: Point, point_b: Point) -> Point:
    return point_a.sub(point_b)


def mult_point(point_a: Point, factor) -> Point:
    return point_a.mult(factor)


def point_in_area(point: Point, area: [Point, Point]) -> bool:
    return point.in_area(area)


def get_angle(a: Point, b: Point, c: Point) -> float:
    return b.angle(a, c)
    # ang = math.degrees(math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x))
    # return ang
    # ang = ang + 360 if ang < 0 else ang
    # return 360 - ang if ang > 180 else ang


def get_distance(from_point: Point, to_point: Point):
    return from_point.distance(to_point)
