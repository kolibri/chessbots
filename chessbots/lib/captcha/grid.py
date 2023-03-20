from chessbots.lib.point_helper import *
from chessbots.lib.captcha.marker import DummyMarker, Marker
from typing import NamedTuple


class GridPoint(NamedTuple):
    grid_pos: Point
    expected_pos: Point
    marker: DummyMarker


def resolve_markers_to_grid(markers: [Marker], grid_size: int, tolerance: int) -> [str, float, [GridPoint], [Point, Point, Point]]:
    t_point = Point(tolerance, tolerance)
    width = max([d.pos.x for d in markers])
    height = max([d.pos.y for d in markers])
    area_size = Point(width, height)

    angle_points = create_angel_points([m.pos for m in markers], area_size)
    angle = get_angle(angle_points[0], angle_points[1], Point(angle_points[0].x, angle_points[1].y))
    # angle magic to 90?
    angle = angle + 360 if angle < 0 else angle
    angle = 360 - angle if angle > 180 else angle

    result = []
    base_mod_x = sub_points(angle_points[1], angle_points[0])
    base_mod_y = sub_points(angle_points[1], angle_points[2])

    grid_y_min = grid_size * -1
    grid_y_max = grid_size
    grid_x_min = grid_size * -1
    grid_x_max = grid_size

    y_range = Point(grid_y_min, grid_y_max)
    x_range = Point(grid_x_min, grid_x_max)

    for y in range(*y_range.raw):
        for x in range(*x_range.raw):
            mod_x = mult_point(base_mod_x, x * -1)
            mod_y = mult_point(base_mod_y, y * -1)

            expected_pos = add_points(angle_points[1], add_points(mod_x, mod_y))
            if area_size.x >= expected_pos.x >= 0 and area_size.y >= expected_pos.y >= 0:
                target = Point(-x, y)
                result.append(create_grid_point(target, expected_pos, markers, t_point))
    return angle, result, angle_points, grid_to_txt(result)


def create_grid_point(target: Point, position: Point, markers: [Marker], t_point: Point) -> GridPoint:
    for marker in markers:
        area = [sub_points(position, t_point), add_points(position, t_point)]
        if point_in_area(marker.pos, area):
            return GridPoint(target, position, marker)
    return GridPoint(target, position, DummyMarker(position))  # here we set the value for "not found"


def create_angel_points(markers: [Point], area_size: Point) -> [Point, Point, Point]:
    def get_with_distance_sorted(markers: [Point], reference_point: Point):
        with_distance = [[mark, get_distance(mark, reference_point)] for mark in markers]
        return sorted(with_distance, key=lambda x: x[1])

    marks_from_center = get_with_distance_sorted(markers, mult_point(area_size, 0.5))
    p1 = marks_from_center[0][0]
    marks_from_p1 = get_with_distance_sorted([m[0] for m in marks_from_center][1:], p1)

    marks_from_p1_filtered = [m for m in marks_from_p1 if m[0].x <= p1.x and m[0].y < p1.y]
    if not marks_from_p1_filtered:
        # print('markers', [m.txt for m in markers[:5]], 'mp1', [m[0].txt for m in marks_from_p1[:5]])
        raise RuntimeError('no markers in area for second spot')
    p2 = marks_from_p1_filtered[0][0]

    angle = get_angle(p2, p1, Point(p1.x, p2.y))
    p3_mod = sub_points(p2, p1)
    if angle == 0:
        p3 = sub_points(p1, Point(p3_mod.y, p3_mod.x * -1))
    else:
        p3 = add_points(p1, Point(p3_mod.y * -1, p3_mod.x * 1))

    return p2, p1, p3


def grid_to_txt(grid: [GridPoint]):
    max_x = max([g.grid_pos.x for g in grid]) + 1
    max_y = max([g.grid_pos.y for g in grid]) + 1
    min_x = min([g.grid_pos.x for g in grid])
    min_y = min([g.grid_pos.y for g in grid])

    res = ''
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            if Point(x, y).txt in [g.grid_pos.txt for g in grid]:
                index = [g.grid_pos.txt for g in grid].index(Point(x, y).txt)
                cell = grid[index]
                res = res + str(cell.marker.value)
            else:
                res = res + '2'
        res = res + '\n'
    return res
