import random

import cv2
from collections import namedtuple

from chessbots.lib.pattern import Pattern as Board, txt_to_matrix
from chessbots.lib.pattern import txt_to_matrix
from chessbots.lib.point_helper import *
from chessbots.lib.filesystem import *

from typing import NamedTuple


def not_negative(val: int | float):
    if 0 > val:
        return 0
    return val


def in_tolerance(value, target: int, tolerance: int):
    return target - tolerance < value < target + tolerance


def value_color(value, check_mode: bool = False):
    if '1' == value:
        if check_mode:
            return 123, 123, 123
        return 64, 64, 64
    elif '0' == value:
        if check_mode:
            return 255, 255, 255
        return 192, 192, 192
    return 123, 0, 123


class Drawable(NamedTuple):
    pos: Point
    size: int
    color: tuple[int, int, int]
    value: str


class DrawPoint:
    def __init__(self, pos: Point, radius: int, value: str, color: [int, int, int], fill: bool = False):
        self.pos = pos
        self.radius = radius
        self.value = value
        self.color = color
        self.fill = fill

    def draw_on(self, img):
        thickness = 3
        if self.fill:
            thickness = -1
        cv2.circle(img, self.pos.raw, self.radius, self.color, thickness)
        cv2.putText(img, self.value, add_points(self.pos, Point(2, 2)).raw, cv2.FONT_ITALIC, 0.4, (10, 10, 10))


def draw_points_on(img, filename: str, points: [DrawPoint]):
    output = img.copy()
    for point in points:
        point.draw_on(output)
    cv2.imwrite(filename, output)


class DummyMarker:
    def __init__(self, pos: Point):
        self.pos = pos
        self.radius = 0
        self.value = '2'


class Marker(DummyMarker):
    def __init__(self, contour, img):
        contours_poly = cv2.approxPolyDP(contour, 3, True)
        self.outer_range = [19, 3]  # target_radius, tolerance
        self.inner_range = [10, 3]  # target_radius, tolerance
        self.grid_size = 16
        center_tol = 5
        self.center_tolerance = [Point(-center_tol, -center_tol), Point(center_tol, center_tol)]
        self.box_tolerance = 2
        self.box = cv2.boundingRect(contours_poly)
        pos, radius = cv2.minEnclosingCircle(contours_poly)
        self.pos = Point(int(pos[0]), int(pos[1]))
        self.radius = int(radius)
        self.img = img
        self.value = '2'
        self.raw_center_circles = []
        self.center_circles = []
        self.valid_size = in_tolerance(self.radius, *self.outer_range)
        if self.valid_size:
            x1 = int(not_negative(self.pos.x - self.radius + self.box_tolerance))
            y1 = int(not_negative(self.pos.y - self.radius + self.box_tolerance))
            x2 = int(not_negative(self.pos.x + self.radius - self.box_tolerance))
            y2 = int(not_negative(self.pos.y + self.radius - self.box_tolerance))
            self.snapshot = self.img[y1:y2, x1:x2]
            # self.snapshot = self.img[self.box[1]:self.box[3], self.box[0]:self.box[2]]
            if 0 != len(self.snapshot):
                self.raw_center_circles = find_inner_markers(self.snapshot, self.radius)
                self.center_circles = [c for c in self.raw_center_circles if in_tolerance(c.radius, *self.inner_range)]
                self.center_circles = [c for c in self.raw_center_circles if
                                       point_in_area(sub_points(c.pos, Point(self.radius, self.radius)),
                                                     self.center_tolerance)]

            if 0 < len(self.center_circles):
                self.value = '0'
            if 0 == len(self.center_circles):
                self.value = '1'

    # def draw_position(self, img):


class GridPoint(NamedTuple):
    grid_pos: Point
    expected_pos: Point
    marker: DummyMarker


class Pointbox(NamedTuple):
    x0: int
    y0: int
    x1: int
    y1: int


# def draw_positions(img, positions: [Drawable]):
#     output = img.copy()
#
#     for pos in positions:
#         color = pos.color
#         cv2.circle(output, pos.pos, pos.size, color, 1)
#         cv2.putText(output, pos.value, add_points(pos.pos, Point(2, 2)), cv2.FONT_ITALIC, 0.4, color)
#
#     return output


class MarkerInner:
    def __init__(self, contour, original: int):
        self.tol = 4
        self.original = original
        contours_poly = cv2.approxPolyDP(contour, 3, True)
        self.box = cv2.boundingRect(contours_poly)
        pos, radius = cv2.minEnclosingCircle(contours_poly)
        self.pos = Point(int(pos[0]), int(pos[1]))
        self.radius = int(radius)
        # self.valid =


def find_contours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    return contours


def find_inner_markers(img, original: int):
    return [MarkerInner(contour, original) for contour in find_contours(img)]


def find_markers(img):
    return [Marker(contour, img) for contour in find_contours(img)]


def find_angel_points(markers: [Point]) -> [Point, Point, Point]:
    width = max([d.x for d in markers])
    height = max([d.y for d in markers])
    area_size = Point(width, height)
    center = mult_point(area_size, 0.5)

    with_distance = [[mark, get_distance(mark, center)] for mark in markers]
    sorted_markers = sorted(with_distance, key=lambda x: x[1])

    p1 = sorted_markers[0][0]

    with_distance_to_p1 = [[mark[0], get_distance(mark[0], p1)] for mark in sorted_markers[1:]]
    sorted_markers = sorted(with_distance_to_p1, key=lambda x: x[1])

    p2_remaining = sorted_markers
    p2_s = [m for m in p2_remaining if m[0].x <= p1.x and m[0].y < p1.y]
    # print(p2_s)
    if not p2_s:
        raise RuntimeError('no markers in area for second spot')
    p2 = p2_s[0][0]

    def check_point_for_angle(angle, p1, p2):
        # print('fixed', angle, angle % 90, p1, p2)
        fa_dir = -1 if angle < 0 else 1

        # fixed_angle = angle % 90
        #
        # if fixed_angle == 0:
        #     return p1.y >= p2.y
        if angle < 45:
            return p1.x <= p2.x and p1.y <= p2.y
        return p1.x <= p2.x and p1.y <= p2.y

    p1_p2_angle = get_angle(p2, p1, Point(p1.x, p2.y))

    p3_remaining = [m for m in p2_remaining if m[0] != p2]
    p3_s = [m for m in p3_remaining if check_point_for_angle(p1_p2_angle, m[0], p1)]
    if not p3_s:
        raise RuntimeError('no markers in area for third spot')
    p3 = p3_s[0][0]

    p3_mod = sub_points(p2, p1)
    if p1_p2_angle == 0:
        p3 = sub_points(p1, Point(p3_mod.y, p3_mod.x * -1))
    else:
        p3 = add_points(p1, Point(p3_mod.y * -1, p3_mod.x * 1))


    points = [p2, p1, p3]
    print(
        'soma',
        p1_p2_angle,
        p1_p2_angle % 90,
        [p.txt for p in points],
        get_angle(p2, p1, p3) % 90,
        get_angle(p3, p1, p2) % 90,
        get_angle(p1, p2, p3) % 90,
        get_angle(p3, p2, p1) % 90,
        get_angle(p1, p3, p2) % 90,
        get_angle(p2, p3, p1) % 90,
        'p1r',
        [[m[0].txt, m[1]] for m in sorted_markers[:10]],
        'p2r',
        [[m[0].txt, m[1]] for m in p2_remaining[:10]],
        'p3r',
        [[m[0].txt, m[1]] for m in p3_remaining[:10]],
    )
    tol = 3
    return points
    if in_tolerance(abs(get_angle(p2, p1, p3)) % 90, 90, tol):
        return p2, p1, p3
    if in_tolerance(get_angle(p2, p1, p3) % 90, -90, tol):
        return p2, p1, p3
    if in_tolerance(abs(get_angle(p1, p2, p3)) % 90, 90, tol):
        return p3, p2, p1
    if in_tolerance(get_angle(p1, p2, p3) % 90, -90, tol):
        return p3, p2, p1
    if in_tolerance(abs(get_angle(p1, p3, p2)) % 90, 90, tol):
        return p2, p3, p1
    if in_tolerance(get_angle(p1, p3, p2) % 90, -90, tol):
        return p2, p3, p1

    # print('points', points)
    angle_tolerance = 92
    if in_tolerance(get_angle(points[0], points[1], points[2]), 0, angle_tolerance):
        print('pointsa')
        return [points[1], points[0], points[2]]
    if in_tolerance(get_angle(points[1], points[2], points[0]), 0, angle_tolerance):
        print('pointsb')
        return [points[2], points[0], points[1]]
    if in_tolerance(get_angle(points[2], points[0], points[1]), 0, angle_tolerance):
        print('pointsc')
        return [points[0], points[2], points[1]]
    # print('points', points, with_distance)
    raise RuntimeError('Could not find three dots with 90 degree angle o_O')


def resolve(markers: [Marker], tolerance: int) -> [str, float, [GridPoint], [Point, Point, Point]]:

    def create_grid_point(grid_point: Point, position: Point, markers: [Marker], t_point: Point) -> GridPoint:
        for marker in markers:
            area = [sub_points(position, t_point), add_points(position, t_point)]
            if point_in_area(marker.pos, area):
                return GridPoint(grid_pos=grid_point, expected_pos=position, marker=marker)
        return GridPoint(grid_point, position, DummyMarker(position))  # here we set the value for "not found"


    def resolve_to_grid_target(pos: Point) -> Point:
        x, y = pos.raw
        a, b = angle_directions

        if 90 == angle:
            # if '-1x1' ==
            return Point(x * a.x * -1, y * b.x * 1)

        # if angle > 45

        mod = Point(
            1 if angle < 45 else -1,
            -1 * b.x
        )

        return Point(y * mod.y, x * mod.x)

    t_point = Point(tolerance, tolerance)
    width = max([d.pos.x for d in markers])
    height = max([d.pos.y for d in markers])
    area_size = Point(width, height)

    # this might be not so good, as we did not check for the middle angle(?)
    angle_points = find_angel_points([m.pos for m in markers])
    angle = get_angle(angle_points[0], angle_points[1], Point(angle_points[0].x, angle_points[1].y))
    # print('angle', angle)
    # angle macig to 90?
    angle = angle + 360 if angle < 0 else angle
    angle = 360 - angle if angle > 180 else angle

    grid_x_size = 16
    result = []
    base_mod_x = sub_points(angle_points[1], angle_points[0])
    base_mod_y = sub_points(angle_points[1], angle_points[2])
    # print(('angle', angle, base_mod_x, base_mod_y))
    read_dir = Point(-1, -1)
    a, c, b = angle_points

    angle_directions = [
        get_direction(c, a),
        get_direction(c, b)
    ]
    angle_directions = [Point(-1 if ad.x < 0 else 1, -1 if ad.y < 0 else 1) for ad in angle_directions]

    direction_rel = add_points(c, add_points(sub_points(a, c), sub_points(b, c)))
    direction = get_direction(c, direction_rel)


    grid_y_min = read_dir.y * grid_x_size
    grid_y_max = read_dir.y * grid_x_size * -1
    grid_x_min = read_dir.x * grid_x_size
    grid_x_max = read_dir.x * grid_x_size * -1

    print('anged', direction.txt, direction_rel.txt, '.', sub_points(a, c).txt, sub_points(b, c).txt, '-', c.txt, a.txt, b.txt, angle)
    y_range = Point(grid_y_min, grid_y_max)
    x_range = Point(grid_x_min, grid_x_max)

    for y in range(*y_range.raw):
        for x in range(*x_range.raw):
            # for x in range(read_dir.x * grid_max, read_dir.x * grid_max * -1):
            mod_x = mult_point(base_mod_x, x * -1)
            mod_y = mult_point(base_mod_y, y * -1)

            expected_pos = add_points(angle_points[1], add_points(mod_x, mod_y))
            if area_size.x >= expected_pos.x >= 0 and area_size.y >= expected_pos.y >= 0:
                target = resolve_to_grid_target(Point(x, y))
                target = Point(-x, y)
                result.append(create_grid_point(target, expected_pos, markers, t_point))
    return angle, result, angle_points






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
                # print('TWO', PointGrid(x, y), max_x, max_y, min_x, min_y, grid )
                res = res + '2'
        res = res + '\n'
    return res


class CaptchaResult:
    def __init__(self, filename):
        self.outer_mark_tolerance = [17, 21]
        self.inner_mark_tolerance = [7, 13]
        self.grid_tolerance = 16
        self.filename = filename

        self.img = cv2.imread(filename)
        self.markers = find_markers(self.img)

        self.markers = [m for m in self.markers if m.valid_size]

        angle, raw_grid, angle_points = resolve(self.markers, self.grid_tolerance)
        self.grid_txt = grid_to_txt(raw_grid)
        #
        # self.grid = self.grid_txt
        self.raw_grid = raw_grid
        self.angle = angle
        self.angle_points = angle_points
        a, c, b = self.angle_points
        self.angle_points_details = [
            get_direction(c, a),
            get_direction(c, b),
        ]
        self.angle_points_details = [Point(not_negative(ad.x), not_negative(ad.y)).txt for ad in
                                     self.angle_points_details]

        # board = board
        a, c, b = self.angle_points
        self.grid_dirs = [
            'd' if c.y < a.y else 'u',
            'l' if c.x < b.x else 'r',
        ]
        self.result = self.resolve_result()
        self.errors = self.detect_error()
        if self.errors:
            print(self.errors)

    def detect_error(self):
        a, c, b = self.angle_points
        ad = sub_points(a, c)
        bd = sub_points(b, c)

        direction_rel = add_points(c, add_points(ad, bd))
        direction = get_direction(c, direction_rel)
        direction_x = c.x - direction_rel.x
        direction_y = c.y - direction_rel.y


        errors = []
        if 90 == self.angle:
            pass
            # todo
            # return
        elif self.angle < 45:
            if not (ad.y < 0 < ad.x):
                errors.append('a dir error at < 45 ')
        else:
            if not (ad.x < 0 < ad.y):
                errors.append('a dir error at > 45')

        if not (bd.x > 0 < bd.y):
            errors.append('b dir error')
        if not (0 > direction_y):
            errors.append('dir y error')
        return errors


    def resolve_result(self):
        board = Board(txt_to_matrix(self.grid_txt))
        return board
        grid_dirs = ''.join(self.grid_dirs)

        angle = self.angle
        if angle == 0:
            board = board.flip()
        elif angle == 45:
            if 'dl' == grid_dirs:
                board = board.flipud().rotate().rotate().rotate().fliplr()
            else:
                board = board  # .flipud().rotate().rotate().rotate()
        elif angle < 45:
            if 'ur' == grid_dirs:
                # print('FOOOOOOOOO', self.filename)
                board = board.rotate().fliplr()
            elif 'dr' == grid_dirs:
                board = board.flip().rotate().rotate().rotate()

        elif angle > 45:
            if 'dr' == grid_dirs:
                # print('FOOOOOOOOO', self.filename)
                board = board
            elif 'ur':
                board = board.fliplr().rotate().rotate().rotate()

        return board

    def draw_debug_images(self):
        def create_filename(name) -> str:
            return self.filename + '_' + name + '.jpg'

        def get_marker_points(marks: [DrawPoint]) -> [DrawPoint]:
            drawpoints = []
            # output = self.img.copy()
            for marker in marks:
                color = value_color(marker.value)
                drawpoints.append(DrawPoint(marker.pos, marker.radius, marker.pos.txt, color))
                if marker.raw_center_circles:
                    for cc in marker.raw_center_circles:
                        point = add_points(cc.pos, sub_points(marker.pos, Point(marker.radius, marker.radius)))
                        drawpoints.append(DrawPoint(point, cc.radius, str(cc.radius), color))

            return drawpoints

        marker_pos = [DrawPoint(m.pos, m.radius, m.pos.txt, value_color(m.value)) for m in self.markers]
        marker_values = [DrawPoint(m.pos, 5, m.value, value_color(m.value, True), True) for m in self.markers]
        grid_points = [DrawPoint(gp.marker.pos, gp.marker.radius, gp.grid_pos.txt, value_color(gp.marker.value)) for gp
                       in self.raw_grid]
        grid_expect = [DrawPoint(gp.expected_pos, gp.marker.radius, gp.expected_pos.txt, value_color(gp.marker.value))
                       for gp in self.raw_grid]
        # a b c
        a, c, b = self.angle_points  # note: a center b
        ap = [
            DrawPoint(c, 15, c.txt, [90, 90, 200], True),  # red, 0 center
            DrawPoint(a, 15, a.txt, [90, 200, 90], True),  # green 1 x
            DrawPoint(b, 15, b.txt, [200, 90, 90], True),  # blue 2 y
        ]

        images = [
            ['pos', marker_pos],
            ['value', marker_values],
            ['markers', get_marker_points(self.markers)],
            ['grid', grid_points],
            ['grid_expect', grid_expect],
            ['angle', ap],
        ]

        for ti in images:
            draw_points_on(self.img, create_filename(ti[0]), ti[1])


        dump_txt(self.filename + '_result.txt', self.result.txt() + '\n' + str(self.angle))
        dump_txt(self.filename + '_raw_grid.txt', self.grid_txt + '\n@' + str(self.grid_dirs) + ' a' + str(self.angle))
