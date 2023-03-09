from flask import (url_for)
from chessbots.lib.pattern import Pattern
from chessbots.lib.point_helper import *
from chessbots.tool.printer import PatternPrinter
import os


class MockBot:
    def __init__(self, name: str, piece: str, pos: Point, size: Point, angle: float):
        self.name = name
        self.piece = piece
        self.pos = pos
        self.size = size
        self.angle = angle

    def data(self):
        return {
            'url': self.url(),
            'name': self.name,
            'state': 'online',
            'piece': self.piece,
            'live_image': url_for('mockbot.get_picture', name=self.name, _external=True),
        }

    def url(self):
        return url_for('mockbot.get_show', name=self.name, _external=True)

    def picture(self):
        return 'mockbot_' + self.name + '.jpg'

    def create(self):
        pass


class MockBots:
    def __init__(self):
        self.bots = [
            MockBot('hk', 'k', Point(253, 613), Point(16, 16), 276),
            MockBot('pk', 'Q', Point(16, 16), Point(16, 16), 210),
            MockBot('pq', 'R', Point(42, 13), Point(16, 16), 60),
            MockBot('pj', 'b', Point(0, 0), Point(16, 16), 0),
            MockBot('mj', '', Point(117, 306), Point(16, 16), 112),
        ]

    def has(self, name: str) -> bool:
        for bot in self.bots:
            if name == bot.name:
                return True
        return False

    def get(self, name: str) -> MockBot:
        for bot in self.bots:
            if name == bot.name:
                return bot
        raise RuntimeError('Mockbot not found: ' + name)


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

        img = raw_img.rotate(rotation).crop((box1.x, box1.y, box2.x, box2.y))

        path = os.path.join(self.path, 'mockbot_' + name + '.jpg')
        print('save to', path, pos, size, rotation)
        img.convert('RGB').save(path)
