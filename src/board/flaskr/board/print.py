from PIL import Image, ImageDraw


class Print:
    def __init__(self):
        size_mm = 200
        dpi = 300
        self.size = int(size_mm / 25.4 * dpi)
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

        draw.line((p, p, p * 3, p), fill=color, width=self.stroke_width)  # horizontal line
        draw.line((p * 2, p, p * 2, p * 3), fill=color, width=self.stroke_width)  # vertical line

        return tile

    def draw_digit(self, digit: str, is_white_field: bool) -> Image:
        size = int(self.tile_size / 4)  # 16 digits, so we have a 4 * 4 matrix
        p = int(size / 4)  # positioning helper. (p,p): top left corner, (p*3, p*3): bottom right corner
        color = get_foreground_color(is_white_field)
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if '0' == digit:
            draw.ellipse((p, p, p * 3, p * 3), outline=color, width=self.stroke_width)
        else:
            # first the \, then the /
            draw.line((p, p, p * 3, p * 3), fill=color, width=self.stroke_width)
            draw.line((p * 3, p, p, p * 3), fill=color, width=self.stroke_width)

        return img


def get_field_color(index: int) -> bool:
    is_white = 0 == (index % 10) % 2  # change color each column
    return is_white if 0 == (index // 10) % 2 else not is_white  # to differentiate between even and off rows


def get_foreground_color(is_white_field: bool) -> tuple[int, int, int]:
    return (192, 192, 192) if is_white_field else (64, 64, 64)


def get_background_color(is_white_field: bool) -> tuple[int, int, int]:
    return (255, 255, 255) if is_white_field else (0, 0, 0)
