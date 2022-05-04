from PIL import Image, ImageDraw


class Print:
    def __init__(self):
        self.size_mm = 2000
        self.dpi = 300
        #self_size_pixel =

        self.size = 2000
        self.tile_size = int(self.size/10)

    def render(self) -> Image:
        img = Image.new('RGBA', (self.size, self.size), 'green')
        is_white = True
        i = 0

        for x in range(0, 10):
            for y in range(0, 10):
                tile = self.render_tile(i, x, y, is_white)
                img.paste(tile, (x*self.tile_size, y*self.tile_size))
                i = i + 1
                is_white = not is_white
            is_white = not is_white
        return img

    def render_tile(self, identifier, pos_x, pos_y, is_white):
        tile = Image.new('RGBA', (self.tile_size, self.tile_size), 'white' if is_white else 'black')
        color = self.get_foreground_color(is_white)
        align_bar_width = int(self.tile_size/100)

        draw = ImageDraw.Draw(tile)
        draw.line(
            (
                int(self.tile_size / 4),# - align_bar_width / 2),
                int(self.tile_size / 4),# + align_bar_width / 2),
                int(self.tile_size / 4 * 3),# + align_bar_width / 2),
                int(self.tile_size / 4),# + align_bar_width / 2),
            ),
            fill=color,
            width=align_bar_width
        )

        draw.line(
            (
                int(self.tile_size / 2),# - align_bar_width / 2),
                int(self.tile_size / 4),# + align_bar_width / 2),
                int(self.tile_size / 2),# - align_bar_width / 2),
                int(self.tile_size / 4 * 3),# + align_bar_width / 2),
            ),
            fill=color,
            width=align_bar_width
        )


        bin_string = '{0:016b}'.format(identifier)
        #print(bin_string)

        for digit_index in range(len(bin_string)):
            digit = bin_string[digit_index]
            digit_img = self.draw_zero(is_white) if '0' == digit else self.draw_one(is_white)
            tile.paste(
                digit_img,
                (
                    digit_index % 4 * int(self.tile_size/4),
                    digit_index // 4 * int(self.tile_size/4)
                ),
                digit_img
            )

        return tile

    def draw_zero(self, is_white_field):
        size = int(self.tile_size/4)
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse(
            (
                int(size / 4),
                int(size / 4),
                int(size / 4 * 3),
                int(size / 4 * 3),
            ),
            outline=self.get_foreground_color(is_white_field)
        )
        return img

    def draw_one(self, is_white_field):
        size = int(self.tile_size/4)
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.line(
            (
                int(size/4),
                int(size/4),
                int(size/4*3),
                int(size/4*3),
            ),
            fill=self.get_foreground_color(is_white_field),
            width=2  # todo: get the stroke width more central
        )

        draw.line(
            (
                int(size/4*3),
                int(size/4),
                int(size/4),
                int(size/4*3),
            ),
            fill=self.get_foreground_color(is_white_field),
            width=2  # todo: get the stroke width more central
        )
        return img

    def get_foreground_color(self, is_white_field):
        return (192, 192, 192) if is_white_field else (64, 64, 64)
