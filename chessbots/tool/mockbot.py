from chessbots.lib.pattern import Pattern
from chessbots.lib.point_helper import *
from .printer import PatternPrinter
import os


class MockbotPictureCreator:
    def __init__(self, path: str, printer: PatternPrinter):
        self.path = path
        self.printer = printer

    def create(self, name: str, board: Pattern, pos: Point, size: Point, rotation: int = 0):
        # enlarge size so we can rotate
        raw_size = add_points(size, Point(size.y, size.x))
        raw_pos = sub_points(pos, Point(int(size.y/2), int(size.x/2)))

        raw_pattern = board.create_snapshot(raw_pos, raw_size)
        raw_img = self.printer.create_image(raw_pattern)

        actual_size = self.printer.calculate_size(board.create_snapshot(Point(0, 0), size))
        actual_size = Point(actual_size[0], actual_size[1])

        width, height = raw_img.size
        center = Point(int(width/2), int(height/2))
        box1 = sub_points(center, mult_point(actual_size, 0.5))
        box2 = add_points(center, mult_point(actual_size, 0.5))
        print(actual_size, box1,box2)

        img = raw_img.rotate(rotation).crop((box1.x, box1.y, box2.x, box2.y))

        img.convert('RGB').save(os.path.join(self.path, 'mockbot_' + name + '.jpg'))
