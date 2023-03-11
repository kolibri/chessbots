from flask import (url_for)
from chessbots.lib.pattern import Pattern
from chessbots.lib.point_helper import *
from chessbots.tool.printer import PatternPrinter
import os
from typing import NamedTuple


class MockBot(NamedTuple):
    name: str
    piece: str
    pos: Point
    # size: Point
    angle: float

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
            # todo convert pos to real position on board
            MockBot('hk', 'k', Point(31*8 + 5, 76*8+2), 276),
            MockBot('mj', '', Point(29*8, 76*8), 112),
            MockBot('k7', 'p', Point(32*8, 32*8), 90),
            MockBot('pd', 'b', Point(0, 0), 0),
            MockBot('pj', 'R', Point(4*8+3, 7*8+7), 0),
            MockBot('pk', 'Q', Point(8*8, 16*8), 0),
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

    def create(self, bot: MockBot, board: Pattern):
        size = Point(16, 16)
        # enlarge size so we can rotate
        raw_size = add_points(size, Point(size.y, size.x))
        raw_pos = sub_points(bot.pos, Point(int(size.y/2), int(size.x/2)))

        raw_pattern = board.create_snapshot(raw_pos, raw_size)
        raw_img = self.printer.create_image(raw_pattern)

        actual_size = self.printer.calculate_size(board.create_snapshot(Point(0, 0), size))
        actual_size = Point(actual_size[0], actual_size[1])

        width, height = raw_img.size
        center = Point(int(width/2), int(height/2))
        box1 = sub_points(center, mult_point(actual_size, 0.5))
        box2 = add_points(center, mult_point(actual_size, 0.5))

        img = raw_img.rotate(bot.angle).crop((box1.x, box1.y, box2.x, box2.y))

        path = os.path.join(self.path, 'mockbot_' + bot.name + '.jpg')
        print('save to', path, bot)
        img.convert('RGB').save(path)
