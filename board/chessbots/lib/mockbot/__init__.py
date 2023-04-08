import os
from typing import NamedTuple

import PIL.Image
from flask import url_for

from chessbots.lib.pattern import Pattern
from chessbots.lib.point_helper import Point, add_points, sub_points, mult_point
from chessbots.tool.printer import PatternPrinter
from chessbots.lib.filesystem import *


class MockBot(NamedTuple):
    name: str
    piece: str
    pos: Point
    angle: float
    pattern: Pattern
    size: Point
    img: PIL.Image.Image

    def data(self):
        return {
            'url': self.url(),
            'name': self.name,
            'state': 'online',
            'piece': self.piece,
            'pos_pic': url_for('mockbot.get_picture', name=self.name, _external=True),
        }

    def safefile_data(self):
        return {
            'name': self.name,
            'piece': self.piece,
            'pos': self.pos.raw,
            'angle': self.angle,
        }

    def mockbot_data(self):
        return {
            'url': self.url(),
            'name': self.name,
            'piece': self.piece,
            'pos': self.pos.raw,
            'angle': self.angle
        }

    def url(self):
        return url_for('mockbot.get_show', name=self.name, _external=True)


class MockbotFactory:
    def __init__(self, printer: PatternPrinter, base_board: Pattern):
        self.printer = printer
        self.base_board = base_board
        self.sn_size = Point(16, 16)

    def create(self, name: str, piece: str, pos: Point, angle: int):
        size = Point(16, 16)
        board = self.base_board.create_snapshot(pos, self.sn_size)
        for i in range(0, angle // 90):
            board = board.rotate()

        img = self.__create_img(pos, angle, board)
        bot = MockBot(name, piece, pos, angle, board, self.sn_size, img)
        return bot

    def __create_img(self, pos, angle, pattern) -> PIL.Image.Image:
        '''
        @todo: use new board printer here
        '''
        size = self.sn_size
        enlarged_size = size.mult(2)
        snapshot_pos = pos.sub(size.mult(0.5).to_ints())

        enlarged_pattern = self.base_board.create_snapshot(snapshot_pos, enlarged_size)
        enlarged_img = self.printer.create_image(enlarged_pattern)

        actual_size = Point(*self.printer.calculate_size(pattern))

        width, height = enlarged_img.size
        center = Point(int(width / 2), int(height / 2))
        box1 = center.sub(actual_size.mult(0.5))
        box2 = center.add(actual_size.mult(0.5))
        img = enlarged_img.rotate(angle).crop((box1.x, box1.y, box2.x, box2.y))
        # img = img.resize((1024, 768))
        img = img.resize((1024, 1024))
        return img

    def load(self, data):
        return self.create(data['name'], data['piece'], Point(*data['pos']), int(data['angle']))


class MockBots:
    def __init__(self, data_dir: str, factory: MockbotFactory):
        self.factory = factory
        self.data_dir = data_dir

        self.bots = self.__load()

    def add(self, name: str, piece: str, pos: Point, angle: int) -> MockBot:
        bot = self.factory.create(name, piece, pos, angle)
        dump_json(os.path.join(self.data_dir, 'mockbot_' + bot.name + '.json'), bot.safefile_data())
        return bot

    def __load(self):
        def check_path(f: str):
            return os.path.isfile(os.path.join(self.data_dir, f)) \
                and f.startswith('mockbot_') \
                and f.endswith('.json') \

        mockbot_files = [os.path.join(self.data_dir, f) for f in os.listdir(self.data_dir) if check_path(f)]
        return [self.factory.load(read_json(mbf)) for mbf in mockbot_files]

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
