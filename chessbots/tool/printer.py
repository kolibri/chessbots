from PIL import Image, ImageDraw
from chessbots.lib.pattern import Pattern
from chessbots.lib.print_units import *
from chessbots.lib.point_helper import *


class PatternPrinter:
    def __init__(self, dpi: int, point_size: PrintPixel):
        self.dpi = dpi
        self.point_size = point_size.to_pixel(self.dpi)
        self.color_trans = (255, 255, 255, 0)
        self.color_bg = (255, 255, 255, 0)
        self.color_fg = (127, 127, 127, 255)

    def create_image(self, pattern: Pattern):
        return self._render(pattern)

    def calculate_size(self, pattern: Pattern):
        return [i*self.point_size for i in pattern.size().raw]

    def save_to_file(self, pattern: Pattern, path: str):
        self._render(pattern).convert('RGB').save(path)

    def _render(self, pattern: Pattern):
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
        for y in range(size.y):
            for x in range(size.x):
                img.paste(
                    render_digit(matrix[x][y]),
                    (x * self.point_size, y * self.point_size)
                )
        return img


class TiledPatternPrinter:
    def __init__(self, printer: PatternPrinter):
        self.printer = printer

    def save_to_files(self, pattern: Pattern, grid_size: int, base_path: str):

        for x in range(0, 1):
            for y in range(0, 1):
                sn_size = Point(int(pattern.size()[0] / grid_size), int(pattern.size()[1] / grid_size))
                self.printer.save_to_file(
                    pattern.create_snapshot(Point(x * sn_size.x, y * sn_size.y), sn_size),
                    base_path + str(x) + 'x' + str(y) + '.jpg'
                )
