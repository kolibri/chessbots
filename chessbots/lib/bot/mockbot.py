from flask import (url_for)
from chessbots.lib.pattern import Pattern
from chessbots.lib.point_helper import *
from chessbots.tool.printer import PatternPrinter
from chessbots.lib.filesystem import *
import os
from typing import NamedTuple


class MockBot(NamedTuple):
    name: str
    piece: str
    pos: Point
    # size: Point
    angle: float
    pattern: Pattern
    size: Point

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
    def __init__(self, board: Pattern):
        def create_mockbot(name: str, piece: str, pos: Point, angle: int, grid_rot: int) -> MockBot:
            size = Point(16, 16)
            board = self.board.create_snapshot(pos, size)
            for i in range(0, grid_rot):
                board = board.rotate()
            return MockBot(name, piece, pos, angle, board, size)

        self.board = board

        generated = []
        for rotation in range(0, 360, 1):
            # if 46 == rotation:
            if 0 <= rotation % 45 < 5:
                rot_steps = rotation // 90
                rot_mod = rotation // 90
                generated.append(create_mockbot('r' + str(rotation), '', Point(0, 0), rotation, rot_mod))

        self.bots = [
            # create_mockbot('hk', 'k', Point(31 * 8 + 5, 76 * 8 + 2), 15, 0),
            # create_mockbot('mj', '', Point(29 * 8, 76 * 8), -15, 0),
            # create_mockbot('ma', '', Point(0, 0), -2, 0),
            # create_mockbot('mb', '', Point(0, 0), 2, 0),
            # create_mockbot('mc', '', Point(0, 0), 45, 0),
            # create_mockbot('k7', 'p', Point(32 * 8, 32 * 8), 90, 1),
            # create_mockbot('pd', 'b', Point(0, 0), 0, 0),
            # create_mockbot('pj', 'R', Point(4 * 8 + 3, 7 * 8 + 7), 0, 0),
            # create_mockbot('pk', 'Q', Point(8 * 8, 16 * 8), 0, 0),
        ]
        self.bots = generated

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
    def __init__(self, path: str, printer: PatternPrinter, mockbots: MockBots):
        self.path = path
        self.printer = printer
        self.mockbots = mockbots

    def create(self):
        for bot in self.mockbots.bots:
            self.create_for_bot(bot)

    def create_for_bot(self, bot: MockBot):
        size = bot.size
        # enlarge size so we can rotate
        enlarged_size = add_points(size, Point(size.y, size.x))
        snapshot_pos = sub_points(bot.pos, Point(int(size.y / 2), int(size.x / 2)))

        enlarged_pattern = self.mockbots.board.create_snapshot(snapshot_pos, enlarged_size)
        enlarged_img = self.printer.create_image(enlarged_pattern)

        actual_pattern = bot.pattern
        actual_size = Point(*self.printer.calculate_size(actual_pattern))

        width, height = enlarged_img.size
        center = Point(int(width / 2), int(height / 2))
        box1 = sub_points(center, mult_point(actual_size, 0.5))
        box2 = add_points(center, mult_point(actual_size, 0.5))
        img = enlarged_img.rotate(bot.angle).crop((box1.x, box1.y, box2.x, box2.y))
        path = os.path.join(self.path, 'mockbot_' + bot.name + '.jpg')

        print('save to', path, bot)
        dump_txt(path + '__target.txt', actual_pattern.txt() + '\n@' + str(bot.pos.x) + 'x' + str(bot.pos.y) + ' a' + str(bot.angle))
        img.convert('RGB').save(path)
