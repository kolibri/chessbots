import cv2
import numpy as np
from PIL import Image, ImageDraw


def create_path(filename: str):
    return 'flaskr/static/images/' + filename


def get_field_color(index: int) -> bool:
    row_length = 100
    segments = 10

    x = (index % row_length) // segments
    y = index // (row_length * segments)
    index = x + y * segments
    is_white = 0 == (index % 10) % 2  # change color each column
    return is_white if 0 == (index // 10) % 2 else not is_white  # to differentiate between even and off rows


def get_foreground_color(is_white_field: bool) -> tuple[int, int, int]:
    return (192, 192, 192) if is_white_field else (64, 64, 64)


def get_background_color(is_white_field: bool) -> tuple[int, int, int]:
    return (255, 255, 255) if is_white_field else (0, 0, 0)


class PrintCreator:
    def __init__(self):
        size_mm = 2000
        dpi = 10
        # self.size = int((size_mm / 25.4) * dpi)
        self.size = size_mm * dpi
        self.tile_size = int(self.size / 100)
        self.stroke_width = 2

    def save_img(self, base_path) -> Image:
        board = self.render()
        board.save(base_path + 'print_board.png')

        i = 5

        sn_size = int(self.size / i)
        img = cv2.imread(base_path + 'test_board.png')
        for x in range(0, i):
            for y in range(0, i):
                x1 = x * sn_size
                x2 = (x+1) * sn_size
                y1 = y * sn_size
                y2 = (y+1) * sn_size
                tmp = img[x1:x2, y1:y2]

                cv2.imwrite(base_path + 'print_part' + str(x) + 'x' + str(y) + '.png', tmp)
                # tmp.save(base_path + 'print_part' + str(x) + 'x' + str(y) + '.png')

        # rotated[y1:y2, x1:x2]

        self.render().save(base_path + 'print_board.png')

    def render(self) -> Image:
        img = Image.new('RGBA', (self.size, self.size), 'green')
        '''
        the trick with this loop:
        iterate over all fields once and calculate row and column
        column: i % 10 (rest of division by 10)
        row:    i // 10 (rounded down the result of division by 10)
        Then multiply field position with tile_size to get position in the pixel grid
        '''
        for i in range(0, 100 * 100):
            tile = self.render_tile(i, get_field_color(i))
            img.paste(tile, (i % 100 * self.tile_size, i // 100 * self.tile_size))

        return img

    def render_tile(self, identifier: int, is_white: bool) -> Image:
        tile = self.draw_empty_tile_with_align_bar(is_white)
        p = int(self.tile_size / 4)
        bin_string = '{0:016b}'.format(identifier)  # transform id to binary with 16 digits (e.g.: '0000000000000001')
        # this loop works the same as the on in self.render(), except with a 4x4 field
        for digit_index in range(len(bin_string)):
            digit = bin_string[digit_index]
            digit_img = self.draw_digit(digit, is_white)
            tile.paste(digit_img, (digit_index % 4 * p, digit_index // 4 * p), digit_img)

        return tile

    def draw_empty_tile_with_align_bar(self, is_white_field: bool) -> Image:
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



class TestImageCreator:
    def __init__(self):
        size_mm = 200
        dpi = 300
        # self.size = int(size_mm / 25.4 * dpi)
        self.size = 2000
        self.tile_size = int(self.size / 10)
        self.stroke_width = 2

    def render(self) -> Image:
        img = Image.new('RGBA', (self.size, self.size), 'green')
        '''
        the trick with this loop:
        iterate over all fields once and calculate row and column
        column: i % 10 (rest of division by 10)
        row:    i // 10 (rounded down the result of division by 10)
        Then multiply field position with tile_size to get position in the pixel grid
        '''
        for i in range(0, 100):
            tile = self.render_tile(i, get_field_color(i))
            img.paste(tile, (i % 10 * self.tile_size, i // 10 * self.tile_size))

        return img

    def render_tile(self, identifier: int, is_white: bool) -> Image:
        tile = self.draw_empty_tile_with_align_bar(is_white)
        p = int(self.tile_size / 4)
        bin_string = '{0:016b}'.format(identifier)  # transform id to binary with 16 digits (e.g.: '0000000000000001')
        # this loop works the same as the on in self.render(), except with a 4x4 field
        for digit_index in range(len(bin_string)):
            digit = bin_string[digit_index]
            digit_img = self.draw_digit(digit, is_white)
            tile.paste(digit_img, (digit_index % 4 * p, digit_index // 4 * p), digit_img)

        return tile

    def draw_empty_tile_with_align_bar(self, is_white_field: bool) -> Image:
        tile = Image.new('RGBA', (self.tile_size, self.tile_size), get_background_color(is_white_field))
        draw = ImageDraw.Draw(tile)
        p = int(self.tile_size / 4)  # position helper. (p,p): top left corner, (p*2, p*2): center of field
        color = get_foreground_color(is_white_field)

        #draw.line((int(p*1.75), int(p*1.75), int(p * 2.25), int(p*1.75)), fill=color, width=self.stroke_width)  # horizontal line
        #draw.line((int(p * 2), int(p *1.75), int(p * 2), int(p * 2.25)), fill=color, width=self.stroke_width)  # vertical line

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
            # first the \, then the /
#            draw.line((p, p, p * 3, p * 3), fill=color, width=self.stroke_width)
#            draw.line((p * 3, p, p, p * 3), fill=color, width=self.stroke_width)
        return img

    def write_pattern_files(self, base_path):
        digit_size = int(self.tile_size / 16)
        data = [
            ['WO', '0', True],
            ['BO', '0', False],
            ['WX', '1', True],
            ['BX', '1', False]
        ]
        for d in data:
            self.draw_digit(d[1], d[2], True).\
                crop((digit_size, digit_size, digit_size * 3, digit_size * 3)).\
                save(base_path + 'pattern_' + str(d[0]) + '.png')

    def write_test_files(self, base_path: str):
        def create_rotated_crop(x, y, deg):
            img = cv2.imread(base_path + 'test_board.png')
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

        self.render().save(base_path + 'test_board.png')
        data = [
            ['00', 3, 1, 37],
            ['01', 0, 0, 0],
            ['02', 2, 3, 90],
            ['03', 3, 2, 180],
            ['04', 1, 5, 270],
            ['05', 1, 7, 123],
            ['06', 7, 3, 10],
            ['07', 3, 1, 222],
            ['08', 4, 9, 300],
            ['09', 2, 5, 115]
        ]

        for d in data:
            cv2.imwrite(base_path + 'mockbot_' + d[0] + '.png', create_rotated_crop(d[1], d[2], d[3]))

