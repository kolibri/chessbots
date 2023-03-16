import random

import cv2
from collections import namedtuple


from chessbots.lib.pattern import Pattern as Board, txt_to_matrix
from chessbots.lib.pattern import txt_to_matrix
from chessbots.lib.point_helper import *
from chessbots.lib.filesystem import *

from typing import NamedTuple


def not_negative(val: int):
    if 0 > val:
        return 0
    return val


def in_tolerance(value, target: int, tolerance: int):
    return target - tolerance < value < target + tolerance


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


def draw_single_marker(img, pos: Point, radius: int, value: str, color: [int, int, int], fill: bool = False):
    thicknes = 1
    if fill:
        thicknes = -1
    cv2.circle(img, pos.raw(), radius, color, thicknes)
    cv2.putText(img, value, add_points(pos, Point(2, 2)).raw(), cv2.FONT_ITALIC, 0.4, color)


class Marker:
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
                self.center_circles = [c for c in self.raw_center_circles if point_in_area(sub_points(c.pos, Point(self.radius, self.radius)), self.center_tolerance)]

            if 0 < len(self.center_circles):
                self.value = '0'
            if 0 == len(self.center_circles):
                self.value = '1'

    # def draw_position(self, img):


class DummyMarker(Marker):
    def __init__(self, pos: Point):
        self.pos = pos
        self.radius = 0
        self.value = '2'


class GridPoint(NamedTuple):
    grid_pos: Point
    expected_pos: Point
    marker: Marker


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


def resolve(markers: [Drawable], tolerance: int) -> [str, float, [GridPoint], [Point, Point, Point]]:
    def resolve_grid(markers: [Drawable], t_point: Point, area_size: Point) -> [GridPoint]:
        def find_angel_points(markers: [Drawable]) -> [PointImg, PointImg, PointImg]:
            with_distance = [[mark, get_distance(mark.pos, center)] for mark in markers]
            sorted_markers = sorted(with_distance, key=lambda x: x[1])
            points = [m[0].pos for m in sorted_markers[0:3]]
            # print('points', points)
            if in_tolerance(get_angle(points[0], points[1], points[2]), 90, 10):
                # print('pointsa')
                return [points[0], points[1], points[2]]
            if in_tolerance(get_angle(points[1], points[2], points[0]), 90, 10):
                # print('pointsb')
                return [points[1], points[2], points[0]]
            if in_tolerance(get_angle(points[2], points[0], points[1]), 90, 10):
                # print('pointsc')
                return [points[2], points[0], points[1]]
            # print('points', points, with_distance)
            raise RuntimeError('Could not find three dots with 90 degree angle o_O')

        def create_grid_point(grid_point: Point, position: Point, markers: [Marker], t_point: Point) -> GridPoint:
            for marker in markers:
                area = [sub_points(position, t_point), add_points(position, t_point)]
                if point_in_area(marker.pos, area):
                    return GridPoint(grid_pos=grid_point, expected_pos=position, marker=marker)
            return GridPoint(grid_point, position, DummyMarker(position))  # here we set the value for "not found"

        # this might be not so good, as we did not check for the middle angle(?)
        angle = find_angel_points(markers)
        grid_max = 16
        result = []
        base_mod_x = sub_points(angle[1], angle[0])
        base_mod_y = sub_points(angle[1], angle[2])
        # print(('angle', angle, base_mod_x, base_mod_y))

        for y in range(-grid_max, grid_max):
            for x in range(-grid_max, grid_max):
                mod_x = mult_point(base_mod_x, x)
                mod_y = mult_point(base_mod_y, y)
                expected_pos = add_points(angle[1], add_points(mod_x, mod_y))
                # print('ep', x, y, mod_x, mod_y, expected_pos)
                if area_size.x >= expected_pos.x >= 0 and area_size.y >= expected_pos.y >= 0:
                    result.append(create_grid_point(Point(y, x), expected_pos, markers, t_point))
        return result, get_angle(angle[0], angle[1], Point(angle[0].x, angle[1].y)), angle

    width = max([d.pos.x for d in markers])
    height = max([d.pos.y for d in markers])
    area_size = Point(width, height)
    # center = Point(int(width / 2), int(height / 2))
    center = mult_point(area_size, 0.5)
    t_point = Point(tolerance, tolerance)
    grid, angle, angle_points = resolve_grid(markers, t_point, area_size)
    # grid_txt = grid_to_txt(grid)
    # grid_txt = Board(txt_to_matrix(grid_txt)).flip().txt()
    # return grid_txt, angle, grid, angle_points
    return angle, grid, angle_points


def grid_to_txt(grid: [GridPoint]):
    max_x = max([g.grid_pos.x for g in grid]) + 1
    max_y = max([g.grid_pos.y for g in grid]) + 1
    min_x = min([g.grid_pos.x for g in grid])
    min_y = min([g.grid_pos.y for g in grid])

    res = ''
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            if PointGrid(x, y) in [g.grid_pos for g in grid]:
                index = [g.grid_pos for g in grid].index(PointGrid(x, y))
                cell = grid[index]
                res = res + str(cell.marker.value)
            else:
                # print('TWO', PointGrid(x, y), max_x, max_y, min_x, min_y, grid )
                res = res + '2'
        res = res + '\n'
    return res


class CaptchaResult:
    def __init__(self, filename, outer_mark_tolerance: [int, int], inner_mark_tolerance: [int, int],
                 grid_tolerance: int, center_tolerance: int):
        self.filename = filename
        self.outer_mark_tolerance = outer_mark_tolerance
        self.inner_mark_tolerance = inner_mark_tolerance
        self.grid_tolerance = grid_tolerance

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
        # board = board
        a0, a1, a2 = self.angle_points
        self.grid_dirs = [
            'd' if a0.y < a2.y else 'u',
            'l' if a0.x < a1.x else 'r',
        ]
        self.result = self.resolve_result()

    def resolve_result(self):
        board = Board(txt_to_matrix(self.grid_txt))
        oboard = board
        grid_dirs = ''.join(self.grid_dirs)
        #  print('--', ''.join(self.grid_dirs))
        if 'dl' == grid_dirs:
            # print('ur', self.filename)
            board = board.flipud().rotate().rotate().rotate()
        if 'dr' == grid_dirs:
            # print('dr', self.filename)
            board = board.flip()
        if 'ul' == grid_dirs:
            # print('ul', self.filename)
            board = board
        if 'ur' == grid_dirs:
            # print('ur', self.filename, )
            board = board.fliplr().rotate().rotate().rotate()

        fixangle = self.angle
        if fixangle == 0:
            oboard = oboard.flip()
        elif fixangle == 45:
            if 'dl' == grid_dirs:
                oboard = oboard.flipud().rotate().rotate().rotate().fliplr()
            else:
                oboard = oboard #.flipud().rotate().rotate().rotate()
            # and 'ul' != grid_dirs:
            # oboard = oboard.fliplr()
            # if 'ul' != grid_dirs:
            #     board.fliplr()
        elif fixangle < 45:
            print(self.filename, 'fixangle < 45', fixangle)
            oboard = oboard.flip().rotate().rotate().rotate()
        else:
            oboard = oboard.fliplr().rotate().rotate().rotate()

        return oboard

    # def debug_marks(self, name: str, marks: [Drawable]):
    #     marked = draw_positions(self.img, marks)
    #     cv2.imwrite(self.filename + name, marked)

    def draw_markers(self, name: str, marks: [Marker, str], draw_inner: bool = False):
        output = self.img.copy()
        for marker, value in marks:
            color = (123, 0, 123)
            if '1' == marker.value:
                color = (64, 64, 64)
            if '0' == marker.value:
                color = (192, 192, 192)

            # print('center', marker.pos, value)
            draw_single_marker(output, marker.pos, marker.radius, value, color)
            # cv2.circle(output, marker.pos, marker.radius, color, 1)
            # cv2.putText(output, value, add_points(marker.pos, Point(2, 2)), cv2.FONT_ITALIC, 0.4, color)

            if draw_inner and marker.raw_center_circles:

                for cc in marker.raw_center_circles:
                    point = add_points(cc.pos, sub_points(marker.pos, Point(marker.radius, marker.radius)))
                    draw_single_marker(output, point, cc.radius, str(cc.radius), color)
                    # cv2.circle(output, point, cc.radius, color, 1)
                    # cv2.putText(output, str(cc.radius), add_points(point, Point(2, 2)), cv2.FONT_ITALIC, 0.4, color)

        cv2.imwrite(self.filename + '_' + name + '.jpg', output)

    def draw_debug_images(self):
        self.draw_markers('pos', [[m, str(m.pos.x) + 'x' + str(m.pos.y)] for m in self.markers])
        self.draw_markers('grid', [[gp.marker, str(gp.grid_pos.x) + 'x' + str(gp.grid_pos.y)] for gp in self.raw_grid])
        self.draw_markers('markers', [[m, str(m.pos.x) + 'x' + str(m.pos.y)] for m in self.markers], True)
        b, a, c = self.angle_points # note: a center b
        angle_img = self.img.copy()
        # red, 0 center
        draw_single_marker(angle_img, a, 20, str(a.x) + 'x' + str(a.y), [0, 0, 200], True)
        # green 1 x
        draw_single_marker(angle_img, b, 20, str(b.x) + 'x' + str(b.y), [0, 200, 0], True)
        # blue 2 y
        draw_single_marker(angle_img, c, 20, str(c.x) + 'x' + str(c.y), [200, 0, 0], True)
        # print('abc', a, b, c)
        cv2.imwrite(self.filename + '_angle.jpg', angle_img)

        dump_txt(self.filename + '_result.txt', self.result.txt() + '\n' + str(self.angle))
        dump_txt(self.filename + '_raw_grid.txt', self.grid_txt + '\n@' + str(self.grid_dirs) + ' a' + str(self.angle))
        # self.debug_marks('_solved.jpg',
        #                  [Drawable(pos=d.raw.pos, size=d.raw.size, color=d.raw.color, value=d.raw.value) for d in
        #                   self.raw_grid])
        # self.debug_marks('_expect.jpg', [Drawable(pos=d.expected_pos, size=self.grid_tolerance, color=d.raw.color,
        #                                           value=str(d.expected_pos.x) + 'x' + str(d.expected_pos.y)) for d in
        #                                  self.raw_grid])
        # self.debug_marks('_rawraw.jpg', self.ims)
