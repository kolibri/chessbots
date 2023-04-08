import random

from chessbots.lib.captcha.image import DrawPoint
from chessbots.lib.pattern import Pattern as Board
from chessbots.lib.pattern import txt_to_matrix
from chessbots.lib.filesystem import *
from chessbots.lib.point_helper import *
from chessbots.lib.captcha.image import ImageHandler, DrawPoint
from chessbots.lib.captcha.marker import MarkerResult
from chessbots.lib.captcha.grid import resolve_markers_to_grid
from chessbots.lib.captcha.position import resolve_board_to_position


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


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class Captcha:
    def __init__(self, filename: str):
        self.filename = filename
        self.grid_tolerance = 16

        self.marker_radius_min_o = 17
        self.marker_radius_max_o = 26
        self.marker_radius_min_i = 8
        self.marker_radius_max_i = 12

        self.grid_size = 32

        self.img_handler = ImageHandler(self.filename)

        self.marker_result = MarkerResult(
            self.img_handler.get_work_img(),
            self.marker_radius_min_o,
            self.marker_radius_max_o,
            self.marker_radius_min_i,
            self.marker_radius_max_i
        )

        self.markers = self.marker_result.markers

        self.angle, self.grid, self.angle_points, self.grid_txt = resolve_markers_to_grid(
            self.markers,
            int(self.grid_size / 2),
            self.grid_tolerance
        )

        self.position = Point(-1, -1)
        self.position_rotation = -1
        self.rotation = -1
        self.position_checks = []

        if 0 < len(self.grid):
            self.board = Board(txt_to_matrix(self.grid_txt))
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

    def draw_debug_images(self) -> [str]:
        marks_raw = [DrawPoint(c.pos, c.radius, str(c.radius), random_color()) for c in self.marker_result.raw_contours_pos_angle]
        marks_in_range = [DrawPoint(c.pos, c.radius, str(c.radius), random_color()) for c in self.marker_result.filtered_contours]
        marks_outer = [DrawPoint(c.pos, c.radius, str(c.radius), random_color()) for c in self.marker_result.outer_shells]
        marks_inner = [DrawPoint(c.pos, c.radius, str(c.radius), random_color()) for c in self.marker_result.inner_shells]
        marks_pos = [DrawPoint(m.pos, m.radius, m.pos.txt, value_color(m.value)) for m in self.markers]
        marker_value = [DrawPoint(m.pos, 10, '', value_color(m.value, True)) for m in self.markers]

        grid_points = [DrawPoint(gp.marker.pos, gp.marker.radius, gp.grid_pos.txt, value_color(gp.marker.value)) for gp in self.grid]
        grid_expect = [DrawPoint(gp.expected_pos, gp.marker.radius, gp.expected_pos.txt, value_color(gp.marker.value)) for gp in self.grid]

        # a, c, b = self.angle_points  # note: a center b
        # ap = [
        #     DrawPoint(c, 15, c.txt, [90, 90, 200], True),  # red, 0 center
        #     DrawPoint(a, 15, a.txt, [90, 200, 90], True),  # green 1 x
        #     DrawPoint(b, 15, b.txt, [200, 90, 90], True),  # blue 2 y
        # ]

        def foo_tmp(foo: MarkerResult):
            dwps = []
            for c, vic in foo.raw_markers:
                color = random_color()
                dwps.append(DrawPoint(c.pos, c.radius, str(c.radius), color))
                for ic in vic[1]:
                    dwps.append(DrawPoint(ic.pos, ic.radius, str(ic.radius), color))
            return dwps

        images = [
            ['marks_0raw', marks_raw],
            ['marks_1in_range', marks_in_range],
            ['marks_2outer', marks_outer],
            ['marks_3inner', marks_inner],
            ['marks_4find_value', foo_tmp(self.marker_result)],
            ['marks_5pos', marks_pos],
            ['marks_6value', marker_value],

            ['grid_points', grid_points],
            ['grid_expect', grid_expect],
            # ['grid_angle', ap],
        ]

        for ti in images:
            self.img_handler.draw_points(self.filename + '_' + ti[0] + '.jpg', ti[1])
            # self._draw_points_to_file(ti[0], ti[1])

        self.img_handler.write_work_img(self.filename + '_work_threshold.jpg')
        dump_txt(self.filename + '_result.txt', self.board.txt() + '\n\npos: ' + self.position.txt + '\nrot: ' + str(self.angle))

        files = [m[0] for m in images]
        files.append('work_threshold')
        return files

