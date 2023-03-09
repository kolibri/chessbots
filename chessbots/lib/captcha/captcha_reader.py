import cv2
from collections import namedtuple

from chessbots.lib.pattern import Pattern as Board
from chessbots.lib.pattern import txt_to_matrix
from chessbots.lib.point_helper import *

from typing import NamedTuple


def in_tolerance(value, target: int, tolerance: int):
    return target - tolerance < value < target + tolerance


class Drawable(NamedTuple):
    pos: Point
    size: int
    color: tuple[int, int, int]
    value: str


class GridPoint(NamedTuple):
    grid_pos: Point
    expected_pos: Point
    raw: Drawable


def draw_positions(img, positions: [Drawable]):
    output = img.copy()

    for pos in positions:
        color = pos.color
        cv2.circle(output, pos.pos, pos.size, color, 2)

        cv2.putText(output, pos.value, add_points(pos.pos, Point(2, 2)), cv2.FONT_ITALIC, 0.6, color)

    return output


class MarkerFinder:
    def __init__(self, outer_range: [int, int], inner_range: [int, int]):
        self.outer_range = outer_range
        self.inner_range = inner_range

    def find_markers(self, img):
        def find_with_size(img, min_size: int, max_size: int):
            def fits_size(marker) -> bool:
                box = marker[1]
                return min_size < box[2] < max_size and min_size < box[3] < max_size

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            found = []
            for i in contours:
                contours_poly = cv2.approxPolyDP(i, 3, True)
                box = cv2.boundingRect(contours_poly)
                pos, radius = cv2.minEnclosingCircle(contours_poly)
                found.append([
                    Point(int(pos[0]), int(pos[1])),
                    box,  # do not remove, needed for size check
                    int(radius),
                ])

            return [m for m in found if fits_size(m)]

        def get_mark_value(mark):
            x1, y1, x2, y2 = mark[1]
            snapshot = img[x1:x1 + x2, y1:y1 + y2]
            # print(x1, y1, x2, y2, snapshot)
            sn_marks = find_with_size(snapshot, self.inner_range[0], self.inner_range[1])
            if 0 == len(sn_marks):
                return '0'
            return '1'

        def create_drawable(m) -> Drawable:
            color = (50, 50, 50)
            value = get_mark_value(m)
            if "1" == value:
                color = (200, 200, 200)

            dra = Drawable(
                pos=m[0],
                size=m[2],
                value=value,
                color=color
            )
            # print(dra)
            return dra

        return [create_drawable(m) for m in find_with_size(img, self.outer_range[0], self.outer_range[1])]


class GridResolver:
    def __init__(self):
        self.tolerance = 16
        self.t_point = Point(self.tolerance, self.tolerance)

    def resolve(self, markers: [Drawable]) -> [str, float, [GridPoint], [Point, Point, Point]]:
        def resolve_grid(markers: [Drawable]) -> [GridPoint]:
            def find_angel_points(markers: [Drawable]) -> [PointImg, PointImg, PointImg]:
                with_distance = [[mark, get_distance(mark.pos, center)] for mark in markers]
                sorted_markers = sorted(with_distance, key=lambda x: x[1])
                points = [m[0].pos for m in sorted_markers[0:3]]
                # print('points', points)
                if in_tolerance(get_angle(points[0], points[1], points[2]), 90, 10):
                    return [points[0], points[1], points[2]]
                if in_tolerance(get_angle(points[1], points[2], points[0]), 90, 10):
                    return [points[1], points[2], points[0]]
                if in_tolerance(get_angle(points[2], points[0], points[1]), 90, 10):
                    return [points[2], points[0], points[1]]
                raise RuntimeError('Could not find three dots with 90 degree angle o_O')

            def create_grid_point(grid_point: Point, position: PointImg, markers: [Drawable]) -> GridPoint:
                for marker in markers:
                    area = [sub_points(position, self.t_point), add_points(position, self.t_point)]
                    if point_in_area(marker.pos, area):
                        return GridPoint(grid_pos=grid_point, expected_pos=position, raw=marker)
                return GridPoint(grid_point, position, Drawable(pos=Point(0, 0), size=0, color=(0, 0, 0),
                                                                value='2'))  # here we set the value for "not found"

            width = max([d.pos.x for d in markers])
            height = max([d.pos.y for d in markers])
            area_max = Point(width, height)

            # this might be not so good, as we did not check for the middle angle(?)
            angle = find_angel_points(markers)
            grid_max = 16
            result = []
            base_mod_x = sub_points(angle[1], angle[0])
            base_mod_y = sub_points(angle[1], angle[2])
            # print(('angle', angle, base_mod_x, base_mod_y))

            for x in range(-grid_max, grid_max):
                for y in range(-grid_max, grid_max):
                    mod_x = mult_point(base_mod_x, x)
                    mod_y = mult_point(base_mod_y, y)
                    expected_pos = add_points(angle[1], add_points(mod_x, mod_y))
                    # print('ep', x, y, mod_x, mod_y, expected_pos)
                    if area_max.x >= expected_pos.x >= 0 and area_max.y >= expected_pos.y >= 0:
                        result.append(create_grid_point(Point(x, y), expected_pos, markers))
            return result, get_angle(angle[0], angle[1], Point(angle[0].x, angle[1].y)), angle

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
                        res = res + str(cell.raw.value)
                    else:
                        # print('TWO', PointGrid(x, y), max_x, max_y, min_x, min_y, grid )
                        res = res + '2'
                res = res + '\n'
            return res

        width = max([d.pos.x for d in markers])
        height = max([d.pos.y for d in markers])
        center = Point(int(width / 2), int(height / 2))

        grid, angle, angle_points = resolve_grid(markers)
        grid_txt = grid_to_txt(grid)
        return grid_txt, angle, grid, angle_points


class CaptchaReader:
    def __init__(self, marker_finder: MarkerFinder, grid_resolver: GridResolver, debug: bool):
        self.marker_finder = marker_finder
        self.grid_resolver = grid_resolver
        self.debug = debug

    def resolve(self, filename):
        def debug_marks(img, name: str, marks: [Drawable]):
            marked = draw_positions(img, marks)
            cv2.imwrite(name, marked)

        img = cv2.imread(filename)
        markers = self.marker_finder.find_markers(img)
        if self.debug:
            debug_marks(img, filename + '_marked.jpg', markers)

        grid, angle, grid_, angle_points = self.grid_resolver.resolve(markers)

        # print(angle)
        if self.debug:
            m = [Drawable(pos=d.pos, size=d.size, color=d.color,
                          value=str(d.pos.x) + 'x' + str(d.pos.y)) for d in markers]
            debug_marks(img, filename + '_pos.jpg', m)
            m = [Drawable(pos=d.raw.pos, size=d.raw.size, color=d.raw.color,
                          value=str(d.grid_pos.x) + 'x' + str(d.grid_pos.y)) for d in grid_]
            debug_marks(img, filename + '_grid.jpg', m)
            m = [Drawable(pos=d.raw.pos, size=d.raw.size, color=d.raw.color,
                          value=d.raw.value) for d in grid_]
            debug_marks(img, filename + '_solved.jpg', m)
            m = [Drawable(pos=d.expected_pos, size=self.grid_resolver.tolerance, color=d.raw.color,
                          value=str(d.expected_pos.x) + 'x' + str(d.expected_pos.y)) for d in grid_]
            debug_marks(img, filename + '_expect.jpg', m)
            m = [Drawable(pos=d, size=3, color=(123, 123, 123),
                          value=str(d.x) + 'x' + str(d.y)) for d in angle_points]
            print(angle_points)
            debug_marks(img, filename + '_angle.jpg', m)

            # print(m)
            with open(filename + '_board.txt', 'w') as f:
                f.write(grid)
                f.write('\n')
                f.write(str(angle))
                f.close()

        board = Board(txt_to_matrix(grid))
        return board, angle
