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
    angle: float
    pattern: Pattern
    size: Point

    def data(self):
        return {
            'url': self.url(),
            'name': self.name,
            'state': 'online',
            'piece': self.piece,
            'pos_pic': url_for('mockbot.get_picture', name=self.name, _external=True),
        }

    def url(self):
        return url_for('mockbot.get_show', name=self.name, _external=True)

    def picture(self):
        return 'mockbot_' + self.name + '.jpg'


def create_mockbot(board: Pattern, name: str, piece: str, pos: Point, angle: int) -> MockBot:
    size = Point(16, 16)
    board = board.create_snapshot(pos, size)
    for i in range(0, angle // 90):
        board = board.rotate()
    return MockBot(name, piece, pos, angle, board, size)


class MockBots:
    def __init__(self, board: Pattern):
        self.board = board

        # rotations = range(0, 360, 45)
        # rotations = [0]
        # x_range = range(0, 4, 1)
        # y_range = range(0, 4, 1)
        #
        # points = [Point(120, 120)]
        # points = []
        # for x in x_range:
        #     for y in y_range:
        #         points.append(Point(x, y))


        # def from_pos_and_rot(pos: Point, rot: int):
        #     return create_mockbot(self.board, str(pos) + 'r' + str(rot), '', pos, rot)
        #
        # self.bots = []
        # for at_pos in points:
        #     for rot in rotations:
        #         self.bots.append(from_pos_and_rot(at_pos, rot))
        self.bots = self.__create_standard_set()

    def __create_standard_set(self):
        return [
            create_mockbot(self.board, 'mb_jk', 'wp', Point(1, 1).mult(80).add(Point(0, 0)), 123),
            create_mockbot(self.board, 'mb_wk', 'wk', Point(5, 1).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wq', 'wq', Point(4, 1).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wb0', 'wb', Point(3, 1).mult(80).add(Point(40, 40)), 40),
            create_mockbot(self.board, 'mb_wb1', 'wb', Point(6, 1).mult(80).add(Point(40, 40)), 320),
            create_mockbot(self.board, 'mb_wn0', 'wn', Point(2, 1).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wn1', 'wn', Point(7, 1).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wr0', 'wr', Point(1, 1).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wr1', 'wr', Point(8, 1).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wp0', 'wp', Point(1, 2).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wp1', 'wp', Point(2, 2).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wp2', 'wp', Point(3, 2).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wp3', 'wp', Point(4, 2).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wp4', 'wp', Point(5, 2).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wp5', 'wp', Point(6, 2).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wp6', 'wp', Point(7, 2).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_wp7', 'wp', Point(8, 2).mult(80).add(Point(40, 40)), 0),

            create_mockbot(self.board, 'mb_bk', 'bk', Point(5, 8).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bq', 'bq', Point(4, 8).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bb0', 'bb', Point(3, 8).mult(80).add(Point(40, 40)), 40),
            create_mockbot(self.board, 'mb_bb1', 'bb', Point(6, 8).mult(80).add(Point(40, 40)), 320),
            create_mockbot(self.board, 'mb_bn0', 'bn', Point(2, 8).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bn1', 'bn', Point(7, 8).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_br0', 'br', Point(1, 8).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_br1', 'br', Point(8, 8).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bp0', 'bp', Point(1, 7).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bp1', 'bp', Point(2, 7).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bp2', 'bp', Point(3, 7).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bp3', 'bp', Point(4, 7).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bp4', 'bp', Point(5, 7).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bp5', 'bp', Point(6, 7).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bp6', 'bp', Point(7, 7).mult(80).add(Point(40, 40)), 0),
            create_mockbot(self.board, 'mb_bp7', 'bp', Point(8, 7).mult(80).add(Point(40, 40)), 0),
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
    def __init__(self, path: str, printer: PatternPrinter, mockbots: MockBots):
        self.path = path
        self.printer = printer
        self.mockbots = mockbots

    def create(self):
        for bot in self.mockbots.bots:
            img = self.create_for_bot(bot)
            path = os.path.join(self.path, 'mockbot_' + bot.name + '.jpg')

            print('save to', path, bot.name)
            dump_txt(path + '__target.txt',
                     bot.pattern.txt() + '\n@' + str(bot.pos.x) + 'x' + str(bot.pos.y) + ' a' + str(bot.angle))
            img.convert('RGB').save(path)

    def create_for_bot(self, bot: MockBot):
        size = bot.size
        # enlarge size so we can rotate
        enlarged_size = add_points(size, Point(size.y, size.x))
        snapshot_pos = sub_points(bot.pos, Point(int(size.y / 2), int(size.x / 2)))

        enlarged_pattern = self.mockbots.board.create_snapshot(snapshot_pos, enlarged_size)
        enlarged_img = self.printer.create_image(enlarged_pattern)

        actual_size = Point(*self.printer.calculate_size(bot.pattern))

        width, height = enlarged_img.size
        center = Point(int(width / 2), int(height / 2))
        box1 = sub_points(center, mult_point(actual_size, 0.5))
        box2 = add_points(center, mult_point(actual_size, 0.5))
        img = enlarged_img.rotate(bot.angle).crop((box1.x, box1.y, box2.x, box2.y))
        return img
