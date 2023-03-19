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

    def flip(self) -> Self:
        return Point(self.y, self.x)
    # def txt(self) -> str:
    #     return str(self.x) + 'x' + str(self.y)


def get_direction(a, b) -> Point:
    return Point(
        -1 if a.y < b.y else 1,
        -1 if a.x < b.x else 1
    )


def add_points(point_a: Point, point_b: Point) -> Point:
    return Point(point_a.x + point_b.x, point_a.y + point_b.y)


def sub_points(point_a: Point, point_b: Point) -> Point:
    return add_points(point_a, Point(point_b.x * -1, point_b.y * -1))


def abs_point(p: Point) -> Point:
    return Point(abs(p.x), abs(p.y))


def mult_point(point_a: Point, factor) -> Point:
    return Point(int(point_a.x * factor), int(point_a.y * factor))


def point_in_area(point: Point, area: [Point, Point]) -> bool:
    return area[0].x < point.x < area[1].x and area[0].y < point.y < area[1].y


def get_angle(a: Point, b: Point, c: Point) -> float:
    ang = math.degrees(math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x))
    return ang
    ang = ang + 360 if ang < 0 else ang
    return 360 - ang if ang > 180 else ang


def get_distance(from_point: Point, to_point: Point):
    return math.sqrt((from_point.x - to_point.x) ** 2 + (from_point.y - to_point.y) ** 2)
