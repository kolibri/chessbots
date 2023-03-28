from flask import (url_for)
from chessbots.lib.pattern import Pattern
from chessbots.lib.point_helper import *
from chessbots.tool.printer import PatternPrinter
from chessbots.lib.filesystem import *
import os
from typing import NamedTuple
from chessbots.lib.captcha import Captcha


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
            'live_image': url_for('mockbot.get_picture', name=self.name, _external=True),
        }

    def url(self):
        return url_for('mockbot.get_show', name=self.name, _external=True)

    def picture(self):
        return 'mockbot_' + self.name + '.jpg'


class MockBotTester:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def test_captcha(self, bot: MockBot):
        captcha = Captcha(os.path.join(self.base_path, bot.picture()))
        captcha.draw_debug_images()
        # print('mockbot test', bot.name, captcha.board.txt(), captcha.position.txt)

        board_pos = Point(bot.pos.x // 4, bot.pos.y // 4).add(Point(1, 1))
        tolerance = Point(1, 1)
        test_result_position = captcha.position.in_area([board_pos.sub(tolerance), board_pos.add(tolerance)])

        ang_tol = 1
        ang_act = captcha.rotation
        ang_exp = bot.angle
        test_result_angle = ang_exp - ang_tol < ang_act < ang_exp + ang_tol
        print(test_result_position, test_result_angle, bot.name, board_pos, captcha.position, board_pos.sub(tolerance), board_pos.add(tolerance), 'a', ang_exp, ang_act)

        return bot, captcha, test_result_position, test_result_angle, board_pos


def create_mockbot(board: Pattern, name: str, piece: str, pos: Point, angle: int) -> MockBot:
    size = Point(16, 16)
    board = board.create_snapshot(pos, size)
    for i in range(0, angle // 90):
        board = board.rotate()
    return MockBot(name, piece, pos, angle, board, size)


class MockBots:
    def __init__(self, board: Pattern):
        self.board = board

        rotations = range(0, 360, 15)
        # rotations = [0, 45, 135]
        x_range = range(0+16, 4+16, 1)
        y_range = range(0+16, 4+16, 1)

        points = [Point(18, 19)]
        # points = []
        # for x in x_range:
        #     for y in y_range:
        #         points.append(Point(x, y))


        def from_pos_and_rot(pos: Point, rot: int):
            return create_mockbot(self.board, str(pos) + 'r' + str(rot), '', pos, rot)

        self.bots = []
        for at_pos in points:
            for rot in rotations:
                self.bots.append(from_pos_and_rot(at_pos, rot))

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
