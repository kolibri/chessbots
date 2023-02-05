import os.path

import cv2
import numpy as np
from PIL import Image, ImageDraw

transparent = (0, 255, 255, 0)
grey = (127, 127, 127, 255)


def create_path(filename: str):
    return 'flaskr/static/images/' + filename


def get_field_color(index: int, row_length: int = 100, segments: int = 10) -> bool:
    mod = int(row_length / segments)
    x = int((index % row_length) / mod)
    y = int((index // row_length) / mod)
    field_index = x + y * segments
    is_white = 0 == (field_index % 10) % 2
    return is_white if 0 == (field_index // 10) % 2 else not is_white  # to differentiate between even and off rows


def get_foreground_color(is_white_field: bool) -> tuple[int, int, int]:
    return (192, 192, 192) if is_white_field else (64, 64, 64)


def get_background_color(is_white_field: bool) -> tuple[int, int, int]:
    return (255, 255, 255) if is_white_field else (0, 0, 0)


class BoardImageCreator:
    def __init__(self, pixels_per_side: int, tiles_per_side: int = 100):
        self.size = pixels_per_side
        self.tiles_per_side = tiles_per_side
        self.tile_size = int(self.size / tiles_per_side)
        self.stroke_width = int((self.size / 2000))

    def save_img(self, file_path) -> Image:
        self.render().convert('RGB').save(file_path)

    def save_pattern_files(self, base_path):
        digit_size = int(self.tile_size / 16)
        data = [
            ['WO', '0', True],
            ['BO', '0', False],
            ['WX', '1', True],
            ['BX', '1', False]
        ]
        for d in data:
            self.draw_digit(d[1], d[2], True). \
                crop((digit_size, digit_size, digit_size * 3, digit_size * 3)). \
                convert('RGB').save(base_path + 'pattern_' + str(d[0]) + '.jpeg')

    def save_mockbot_files(self, base_path: str, data: []):
        def create_rotated_crop(x, y, deg):
            img = cv2.imread(base_path + 'test_board.jpeg')
            cs = int(img.shape[0] / 10)
            vp = 2
            image_center = tuple(np.array(img.shape[1::-1]) / 2)
            rot_mat = cv2.getRotationMatrix2D(image_center, deg, 1.0)
            rotated = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
            x1 = int(x * cs)
            x2 = int(x1 + cs * vp)
            y1 = int(y * cs)
            y2 = int(y1 + cs * vp)
            return rotated[y1:y2, x1:x2]

        self.render().convert('RGB').save(base_path + 'test_board.jpeg')

        for d in data:
            cv2.imwrite(base_path + 'mockbot_' + d[0] + '.jpeg', create_rotated_crop(d[1], d[2], d[3]))

    # def safe_print_slices(self):
    # board = self.render()
    # board.save(file_path)

    # i = 5
    # sn_size = int(self.size / i)
    # img = cv2.imread(file_path)
    # for x in range(0, i):
    #     for y in range(0, i):
    #         x1 = x * sn_size
    #         x2 = (x+1) * sn_size
    #         y1 = y * sn_size
    #         y2 = (y+1) * sn_size
    #         tmp = img[x1:x2, y1:y2]
    #
    #         cv2.imwrite(file_path + 'print_part' + str(x) + 'x' + str(y) + '.jpeg', tmp)
    #         # tmp.save(base_path + 'print_part' + str(x) + 'x' + str(y) + '.jpeg')
    # rotated[y1:y2, x1:x2]

    def render(self) -> Image:
        img = Image.new('RGBA', (self.size, self.size), 'green')
        '''
        the trick with this loop:
        iterate over all fields once and calculate row and column
        column: i % 10 (rest of division by 10)
        row:    i // 10 (rounded down the result of division by 10)
        Then multiply field position with tile_size to get position in the pixel grid
        '''
        for i in range(0, self.tiles_per_side * self.tiles_per_side):
            tile = self.render_tile(i, get_field_color(i, self.tiles_per_side, 10))
            img.paste(tile, (i % self.tiles_per_side * self.tile_size, i // self.tiles_per_side * self.tile_size))

        return img

    def render_tile(self, identifier: int, is_white: bool) -> Image:
        tile = self.draw_empty_tile(is_white)
        p = int(self.tile_size / 4)
        bin_string = '{0:016b}'.format(identifier)  # transform id to binary with 16 digits (e.g.: '0000000000000001')
        # this loop works the same as the on in self.render(), except with a 4x4 field
        for digit_index in range(len(bin_string)):
            digit = bin_string[digit_index]
            digit_img = self.draw_digit(digit, is_white)
            tile.paste(digit_img, (digit_index % 4 * p, digit_index // 4 * p), digit_img)

        return tile

    def draw_empty_tile(self, is_white_field: bool) -> Image:
        tile = Image.new('RGBA', (self.tile_size, self.tile_size), get_background_color(is_white_field))

        return tile

    def draw_digit(self, digit: str, is_white_field: bool, with_bg: bool = False) -> Image:
        size = int(self.tile_size / 4)  # 16 digits, so we have a 4 * 4 matrix
        p = int(size / 4)  # positioning helper. (p,p): top left corner, (p*3, p*3): bottom right corner
        color = get_foreground_color(is_white_field)
        bg_color = (0, 0, 0, 0) if not with_bg else get_background_color(is_white_field)
        img = Image.new('RGBA', (size, size), bg_color)
        draw = ImageDraw.Draw(img)

        if '0' == digit:
            draw.ellipse((p, p, p * 3, p * 3), outline=color, width=self.stroke_width)
        else:
            draw.ellipse((p, p, p * 3, p * 3), fill=color, width=self.stroke_width)
        return img


class Unit:
    def __init__(self, unit: float) -> None:
        self.unit = unit

    def to_pixel(self, dpi: int) -> int:
        return int(self.unit)


class MilliMeter(Unit):
    def to_pixel(self, dpi: int) -> int:
        return int((self.unit / 25.4) * dpi)


class Inch(Unit):
    def to_pixel(self, dpi: int) -> int:
        return int(self.unit * dpi)


class UltimateBoardImageMaker:
    def __init__(self, dpi: int, size: Unit, point_size: Unit, captcha_size: int):
        self.dpi = dpi
        self.size = self._convert_to_pixel(size)
        self.point_size = self._convert_to_pixel(point_size)
        self.captcha_size = captcha_size
        self.point_count = self.size / self.point_size
        self.captcha_count = self.point_count / self.captcha_size
        if not self.point_count.is_integer():
            print('Warning: point count is not an int!')
        if not self.captcha_count.is_integer():
            print('Warning: captcha count is not an int!')
        self.point_count = int(self.point_count)
        self.captcha_count = int(self.captcha_count)

    def _convert_to_pixel(self, unit: Unit):
        return unit.to_pixel(self.dpi)

    def to_file(self, path: str):
        img = self.render()

        img.convert('RGB').save(path)

    def part_to_file(self, path: str, pos: (int, int), size: (int, int)):
        img = self.render_part(pos, size)

        img.convert('RGB').save(path)

    def all_parts_to_files(self, base_path: str, grid_size: int):
        part_count = self.captcha_count / grid_size
        if not part_count.is_integer():
            print('Warning: part count is not int')
        part_count = int(part_count)

        for ix in range(0, part_count):
            for iy in range(0, part_count):
                full_path = os.path.join(base_path, 'test_' + str(ix) + 'x' + str(iy) + '.jpg')
                self.part_to_file(full_path, (ix * grid_size, iy * grid_size), (grid_size, grid_size))

    def render(self):
        img = Image.new('RGBA', (self.size, self.size), 'blue')

        current_captcha = 0
        for cx in range(0, self.captcha_count):
            for cy in range(0, self.captcha_count):
                captcha = self._render_captcha_at(cx, cy)
                img.paste(captcha, (cx * self.point_size * self.captcha_size, cy * self.point_size * self.captcha_size))
                current_captcha = current_captcha + 1
        return img

    def _render_captcha_at(self, x: int, y: int):
        return self._render_captcha(self._get_captcha_index(x, y))

    def _get_captcha_index(self, x: int, y: int):
        return x + y * self.captcha_count

    def render_part(self, pos: (int, int), size: (int, int)):
        size_px_x = size[0] * self.point_size * self.captcha_size
        size_px_y = size[1] * self.point_size * self.captcha_size
        img = Image.new('RGBA', (size_px_x, size_px_y), 'blue')
        for px in range(0, size[0]):
            for py in range(0, size[1]):
                captcha = self._render_captcha_at(px + pos[0], py + pos[1])
                img.paste(
                    captcha,
                    (
                        px * self.point_size * self.captcha_size,
                        py * self.point_size * self.captcha_size
                    )
                )
        return img

    def _render_captcha(self, index):
        # for 8x8 matrix with index less than 16bits
        # four 4x4 fields:
        # 0,0 : normal, left to right
        # 1,0 : normal, right to left
        # 0,1 : inverted, left to right
        # 1,1 : inverted, right to left
        def draw_digit(digit: str) -> Image:
            p = int(self.point_size / 5)
            color = grey
            # color = (255, 0, 0, 255)
            img = Image.new('RGBA', (self.point_size, self.point_size), transparent)
            draw = ImageDraw.Draw(img)

            e_xy = (p, p, p * 4, p * 4)
            stroke = int(p * 0.6)
            if '0' == digit:
                draw.ellipse(e_xy, outline=color, width=stroke)
            else:
                draw.ellipse(e_xy, fill=color, width=stroke)
            return img

        def draw_single_captcha(index: str):

            captcha_width = int(self.point_size * self.captcha_size / 2)

            tile = Image.new('RGBA', (captcha_width, captcha_width), transparent)

            for digit_index in range(len(index)):
                digit = index[digit_index]
                digit_img = draw_digit(digit)
                tile.paste(
                    digit_img,
                    (
                        digit_index % int(self.captcha_size / 2) * self.point_size,
                        digit_index // int(self.captcha_size / 2) * self.point_size
                    ),
                    digit_img
                )

            return tile

        bs = '{0:016b}'
        s = bs.format(index)
        # si = s
        sr = s
        sir = s
        si = s.replace('0', 'n').replace('1', '0').replace('n', '1')
        sr = s[::-1]
        sir = si[::-1]

        i = draw_single_captcha(s)
        ii = draw_single_captcha(si)
        ir = draw_single_captcha(sr)
        iir = draw_single_captcha(sir)

        captcha_width = self.point_size * self.captcha_size
        half = int(captcha_width / 2)
        tile = Image.new('RGBA', (captcha_width, captcha_width), transparent)
        tile.paste(i, (0, half), i)
        tile.paste(ir, (half, 0), ir)
        tile.paste(ii, (0, 0), ii)
        tile.paste(iir, (half, half), iir)
        return tile

    def _render_captcha_simple(self, index):
        def draw_digit(digit: str) -> Image:
            p = int(self.point_size / 5)
            color = grey
            # color = (255, 0, 0, 255)
            img = Image.new('RGBA', (self.point_size, self.point_size), transparent)
            draw = ImageDraw.Draw(img)

            e_xy = (p, p, p * 4, p * 4)
            stroke = int(p * 0.6)
            if '0' == digit:
                draw.ellipse(e_xy, outline=color, width=stroke)
            else:
                draw.ellipse(e_xy, fill=color, width=stroke)
            return img

        captcha_width = self.point_size * self.captcha_size
        tile = Image.new('RGBA', (captcha_width, captcha_width), transparent)

        bs = '{0:0' + str(self.captcha_size * self.captcha_size) + 'b}'
        bin_string = bs.format(index)
        for digit_index in range(len(bin_string)):
            digit = bin_string[digit_index]
            digit_img = draw_digit(digit)
            tile.paste(
                digit_img,
                (
                    digit_index % self.captcha_size * self.point_size,
                    digit_index // self.captcha_size * self.point_size
                ),
                digit_img
            )

        return tile


class UltimateBoardImageMaker2:
    def __init__(self, dpi: int, total_width: Unit, tile_per_side: int, marker_size, padding, captcha_size: int):
        self.dpi = dpi
        self.total_width = total_width
        self.tile_per_side = tile_per_side
        self.marker_size = marker_size
        self.padding = padding
        self.captcha_size = captcha_size

    def _convert_to_pixel(self, unit: Unit):
        return unit.to_pixel(self.dpi)

    def create_complete(self, result_path):
        padding = self._convert_to_pixel(self.padding)
        total_size_px = self._convert_to_pixel(self.total_width)
        size_px = total_size_px - padding * 2

        img = Image.new('RGBA', (size_px, size_px), 'blue')

        # create tiles
        tile_width = int(size_px / self.tile_per_side)
        is_white = False
        for tx in range(0, self.tile_per_side):
            for ty in range(0, self.tile_per_side):
                # print(tx, ty, is_white, tile_width, size_px)
                bg_color = get_background_color(is_white)
                is_white = not is_white
                tile = Image.new('RGBA', (tile_width, tile_width), bg_color)
                img.paste(tile, (tx * tile_width, ty * tile_width))
            is_white = not is_white
        filename = 'complete_' + str(self.dpi) + 'dpi.jpeg'

        captcha_width, marker_width, marker_count, captcha_count = self._get_captcha_size()

        identifier = 333
        for mx in range(0, captcha_count):
            for my in range(0, captcha_count):
                captcha = self.render_captcha(identifier)
                identifier = identifier + 1
                img.paste(captcha, (mx * captcha_width, my * captcha_width), captcha)

        total_img = Image.new('RGBA', (total_size_px, total_size_px), 'green')
        total_img.paste(img, (padding, padding))
        total_img.convert('RGB').save(os.path.join(result_path, filename))

    def render_captcha(self, identifier: int):
        def draw_digit(size: int, digit: str) -> Image:
            p = int(size / 6)  # positioning helper. (p,p): top left corner, (p*3, p*3): bottom right corner
            color = grey
            # color = (255, 0, 0, 255)
            img = Image.new('RGBA', (size, size), transparent)
            draw = ImageDraw.Draw(img)
            stroke = int(p / 2)

            if '0' == digit:
                draw.ellipse((p, p, p * 5, p * 5), outline=color, width=stroke)
            else:
                draw.ellipse((p, p, p * 5, p * 5), fill=color, width=stroke)
            return img

        captcha_width, marker_width, *_ = self._get_captcha_size()

        tile = Image.new('RGBA', (captcha_width, captcha_width), transparent)

        bs = '{0:0' + str(self.captcha_size * self.captcha_size) + 'b}'
        bin_string = bs.format(identifier)
        for digit_index in range(len(bin_string)):
            digit = bin_string[digit_index]
            digit_img = draw_digit(marker_width, digit)
            tile.paste(
                digit_img,
                (
                    digit_index % self.captcha_size * marker_width,
                    digit_index // self.captcha_size * marker_width
                ),
                digit_img
            )

        return tile

    def _get_tile_sizes(self):
        padding = self._convert_to_pixel(self.padding)
        total_size_px = self._convert_to_pixel(self.total_width)
        size_px = total_size_px - padding * 2

        return [size_px, total_size_px, padding]

    def _get_captcha_size(self):
        size_px, *_ = self._get_tile_sizes()
        marker_width = self._convert_to_pixel(self.marker_size)
        captcha_width = self.captcha_size * marker_width
        marker_count = int(size_px / marker_width)
        if 0 != size_px % marker_width:
            # print('WARNING: size_px / marker_size did to result in int')
            pass

        captcha_count = int(marker_count / self.captcha_size)
        if 0 != marker_count % self.captcha_size:
            # print('WARNING: marker_count / captcha_size did to result in int')
            pass

        return captcha_width, marker_width, marker_count, captcha_count
