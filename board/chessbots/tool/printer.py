from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw
from chessbots.lib.print_units import *
from chessbots.lib.pattern import *
from chessbots.lib.point_helper import *
import numpy as np
from textwrap import wrap
from typing import NamedTuple


def get_gray(val: int) -> [int, int, int, int]:
    return val, val, val, 255


class PatternPrinter:
    '''
    legacy, only used for mockbot currently.
    '''
    def __init__(self, dpi: int, point_size: PrintPixel):
        self.dpi = dpi
        self.point_size = point_size.to_pixel(self.dpi)
        self.color_trans = (0, 0, 0, 0)
        self.color_bg = (0, 0, 0, 0)
        self.color_fg = (127, 127, 127, 255)
        # self.color_trans = (255, 255, 255, 255)
        # self.color_bg = (255, 255, 255, 255)
        # self.color_fg = (127, 127, 127, 255)

    def create_image(self, pattern: Pattern) -> Image:
        return self._render(pattern)

    def calculate_size(self, pattern: Pattern):
        return [i*self.point_size for i in pattern.size().raw]

    def save_to_file(self, pattern: Pattern, path: str):
        self._render(pattern).convert('RGB').save(path)

    def _render(self, pattern: Pattern) -> Image:
        def render_digit(digit):
            p = int(self.point_size / 5)
            # color = (255, 0, 0, 255)
            img = Image.new('RGBA', (self.point_size, self.point_size), self.color_trans)
            draw = ImageDraw.Draw(img)

            e_xy = (p, p, p * 4, p * 4)
            stroke = int(p * 0.8)
            if '0' == digit:
                draw.ellipse(e_xy, outline=self.color_fg, width=stroke)
            else:
                draw.ellipse(e_xy, fill=self.color_fg, width=stroke)
            return img
        pattern = pattern.mirror().rotate()
        size = pattern.size()
        img = Image.new('RGBA', [i*self.point_size for i in size.raw], self.color_bg)

        matrix = pattern.matrix
        for y in range(0, size.x):
            for x in range(0, size.y):
                img.paste(
                    render_digit(matrix[x][y]),
                    (x * self.point_size, y * self.point_size)
                )
        return img


def bits_to_pattern(bits: str) -> Pattern:
    return Pattern(txt_to_matrix('\n'.join(wrap(bits, 4))))


class PrintCaptcha(NamedTuple):
    captcha: Image
    pos: Point


class BoardPrinter:
    FC_REST: int = -1
    FC_WHITE: int = 0
    FC_BLACK: int = 1
    DPI: int = 600
    SIZE_IN_MARKERS: int = 800
    MARKER_PIXEL_SIZE: int = int(DPI / 10)
    FIELDS_PER_SIDE: int = 10
    CAPTCHA_SIZE: int = 8
    C_BLACK: int = 0
    C_WHITE: int = 255
    C_REST: int = 223
    C_MARK: int = 127

    def __init__(self):
        if 0 != self.SIZE_IN_MARKERS % self.CAPTCHA_SIZE:
            print('Board print error: boardsize is not divisible by markersize', self.SIZE_IN_MARKERS, self.CAPTCHA_SIZE)
        if 0 != self.SIZE_IN_MARKERS % self.FIELDS_PER_SIDE:
            print('Board print error: boardsize is not divisible by field size', self.SIZE_IN_MARKERS, self.FIELDS_PER_SIDE)

    @staticmethod
    def to_file(img: Image, path: str):
        img.convert('RGB').save(path)

    def get_full(self):
        captchas_per_side = int(self.SIZE_IN_MARKERS / self.CAPTCHA_SIZE)
        captcha_count = captchas_per_side * captchas_per_side
        captchas = [PrintCaptcha(self._render_captcha_field(c), self.int_to_pos(c).mult(self.MARKER_PIXEL_SIZE * self.CAPTCHA_SIZE)) for c in range(0, captcha_count)]

        full_size = self.SIZE_IN_MARKERS * self.MARKER_PIXEL_SIZE
        full_img = Image.new('RGBA', (full_size, full_size), (0, 0, 0, 0))
        [full_img.paste(c.captcha, c.pos.raw) for c in captchas]
        return full_img

    def _render_captcha_field(self, value: int) -> Image:
        def render_digit(digit):
            p = int(self.MARKER_PIXEL_SIZE / 5)
            # color = (255, 0, 0, 255)
            img = Image.new('RGBA', (self.MARKER_PIXEL_SIZE, self.MARKER_PIXEL_SIZE), color_bg)
            draw = ImageDraw.Draw(img)

            e_xy = (p, p, p * 4, p * 4)
            stroke = int(p * 0.8)
            if '0' == digit:
                draw.ellipse(e_xy, outline=color_mk, width=stroke)
            else:
                draw.ellipse(e_xy, fill=color_mk, width=stroke)
            return img

        color_bg = self.get_field_color(value)
        color_mk = get_gray(self.C_MARK)

        pattern = self._create_captcha(value)
        pattern = pattern.mirror().rotate()
        size = pattern.size()
        img = Image.new('RGBA', size.mult(self.MARKER_PIXEL_SIZE).raw, color_bg)

        matrix = pattern.matrix
        for y in range(0, size.x):
            for x in range(0, size.y):
                img.paste(
                    render_digit(matrix[x][y]),
                    (x * self.MARKER_PIXEL_SIZE, y * self.MARKER_PIXEL_SIZE)
                )
        return img

    def get_chess_tile(self, pos: Point) -> Image:
        '''
        @param pos: from top left -> bottom right
        '''
        grid_mod = int(self.SIZE_IN_MARKERS / self.CAPTCHA_SIZE / 10)
        sn_pos = pos.mult(grid_mod)
        sn_size = Point(grid_mod, grid_mod)
        return self.get_snapshot(sn_pos, sn_size)

    def chess_tile_to_pdf(self, pos: Point, path: str):
        BoardPrinter.tile_to_pdf(self.get_chess_tile(pos), path, pos.txt)

    @staticmethod
    def tile_to_pdf(tile: Image, path: str, text: str):
        my_canvas = canvas.Canvas(path)
        my_canvas.drawString(10, 10, text)
        BoardPrinter.to_file(tile, path + '.jpg')
        my_canvas.drawImage(path + '.jpg', 9, 30, width=576, height=576)
        my_canvas.save()


    def get_test_tile(self):
        return self.get_snapshot(Point(5, 15), Point(10, 10))

    def get_test_tile_pdf(self, path: str):
        self.tile_to_pdf(self.get_test_tile(), path, 'test @5,15[10,10]')

    def get_snapshot(self, pos: Point, size: Point):
        captchas = []
        for ax in range(pos.x, pos.x + size.x):
            for ay in range(pos.y, pos.y + size.y):
                point = Point(ax, ay)
                value = self.pos_to_int(point)
                captchas.append(PrintCaptcha(
                    self._render_captcha_field(value),
                    point.sub(pos).mult(self.MARKER_PIXEL_SIZE * self.CAPTCHA_SIZE)
                ))
        snapshot_size = size.mult(self.MARKER_PIXEL_SIZE * self.CAPTCHA_SIZE)
        snapshot_img = Image.new('RGBA', snapshot_size.raw, (0, 0, 0, 0))
        [snapshot_img.paste(c.captcha, c.pos.raw) for c in captchas]
        return snapshot_img


    def _create_captcha(self, index: int):
        bs = '{0:014b}'
        bits = bs.format(index)
        bits_inverted = invert_zero_one(bits)

        fields = [
            [
                bits_to_pattern('0' + bits + '0').matrix,
                bits_to_pattern('1' + bits_inverted + '0').fliplr().matrix,
            ], [
                bits_to_pattern('0' + bits_inverted + '1').flipud().matrix,
                bits_to_pattern('1' + bits + '1').flip().matrix,
            ]
        ]

        return Pattern(self._combine(fields))

    @staticmethod
    def _combine(patterns):
        return np.concatenate([np.concatenate(rows, axis=1) for rows in patterns], axis=0)

    def int_to_pos(self, val: int) -> Point:
        size = int(self.SIZE_IN_MARKERS / self.CAPTCHA_SIZE)
        return Point(val % size, val // size)

    def pos_to_int(self, pos: Point) -> int:
        size = int(self.SIZE_IN_MARKERS / self.CAPTCHA_SIZE)
        return int(pos.y * size + pos.x)
        # return Point(val % size, val // size)

    # to_int = int(pos.y * 100 + pos.x)

    def get_field_color(self, captcha_value: int):
        size = 10 # int(self.SIZE_IN_MARKERS / self.CAPTCHA_SIZE / 10)
        pos = self.int_to_pos(captcha_value).div_abs(size)
        # print(size, pos.raw, self.int_to_pos(captcha_value).raw, captcha_value)
        if 0 == pos.x or 0 == pos.y or size-1 == pos.x or size-1 == pos.y:
            return get_gray(self.C_REST)

        return get_gray(self.C_WHITE) if pos.x % 2 == pos.y % 2 else get_gray(self.C_BLACK)
