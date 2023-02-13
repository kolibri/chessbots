from collections import namedtuple

Point = namedtuple('Point', 'x y')
PointImg = namedtuple('PointImg', 'x y')
PointGrid = namedtuple('PointGrid', 'x y')


def add_points(point_a: Point, point_b: Point) -> Point:
    return Point(point_a.x + point_b.x, point_a.y + point_b.y)


def sub_points(point_a: Point, point_b: Point) -> Point:
    return add_points(point_a, Point(point_b.x * -1, point_b.y * -1))


def abs_point(p: Point) -> Point:
    return Point(abs(p.x), abs(p.y))


def mult_point(point_a: Point, factor) -> Point:
    return Point(point_a.x * factor, point_a.y * factor)


def point_in_area(point: Point, area: [Point, Point]) -> bool:
    return area[0].x < point[0] < area[1].x and area[0].y < point[1] < area[1].y
