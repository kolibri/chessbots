import cv2
import numpy as np
from PIL import Image, ImageDraw


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
        self.stroke_width = 1

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
            self.draw_digit(d[1], d[2], True).\
                crop((digit_size, digit_size, digit_size * 3, digit_size * 3)).\
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
