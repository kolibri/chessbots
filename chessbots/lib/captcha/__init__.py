import cv2
from chessbots.lib.pattern import Pattern as Board
from chessbots.lib.pattern import txt_to_matrix
from chessbots.lib.point_helper import *
from chessbots.lib.filesystem import *
from chessbots.lib.captcha.marker import find_markers
from chessbots.lib.captcha.grid import resolve_markers_to_grid
from chessbots.lib.captcha.position import resolve_board_to_position
from typing import NamedTuple


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


class Captcha:
    def __init__(self, filename: str):
        self.filename = filename

        self.outer_mark_tolerance = [17, 21]
        self.inner_mark_tolerance = [7, 13]
        self.grid_tolerance = 16

        self.img = cv2.imread(filename)
        self.markers = find_markers(self.img)
        self.markers = [m for m in self.markers if m.valid_size]

        self.angle, self.grid, self.angle_points, self.grid_txt = resolve_markers_to_grid(self.markers, 16, self.grid_tolerance)

        self.board = Board(txt_to_matrix(self.grid_txt))
        self.position = Point(-1, -1)
        self.position_checks = []

        self.position, self.position_rotation, self.position_checks = resolve_board_to_position(self.board)

        match self.position_rotation:
            case 0:
                self.rotation = 90 - self.angle
            case 1:
                self.rotation = 360 - self.angle
            case 2:
                self.rotation = 270 - self.angle
            case 3:
                self.rotation = 180 - self.angle

    def draw_debug_images(self):
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
                       in self.grid]
        grid_expect = [DrawPoint(gp.expected_pos, gp.marker.radius, gp.expected_pos.txt, value_color(gp.marker.value))
                       for gp in self.grid]

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
            self._draw_points_to_file(ti[0], ti[1])

        dump_txt(self.filename + '_result.txt', self.board.txt() + '\n' + str(self.angle))
        dump_txt(self.filename + '_raw_grid.txt', self.grid_txt + '\n@' + ' a' + str(self.angle))

    def _draw_points_to_file(self, name: str, points: [DrawPoint]):
        filename = self.filename + '_' + name + '.jpg'
        output = self.img.copy()
        for point in points:
            point.draw_on(output)
        cv2.imwrite(filename, output)
