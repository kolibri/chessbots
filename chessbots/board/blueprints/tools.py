from flask import (render_template)
import random

import cv2
import numpy as np
from flask import Blueprint
from chessbots.tool.pattern_creator import Pattern8x8With4DataFields
from chessbots.lib.pattern import *
from chessbots.tool.printer import *
from chessbots.lib.captcha import Captcha
from chessbots.lib.captcha.grid import create_angel_points
from chessbots.lib.captcha.position import *
from dependency_injector.wiring import inject, Provide
from chessbots.board.containers import Container
from chessbots.lib.bot.mockbot import *
from chessbots.lib.filesystem import *

bp = Blueprint('script', __name__)


@bp.cli.command('pattern_test')
@inject
def pattern_test(pattern_creator: Pattern8x8With4DataFields = Provide[Container.pattern_creator]):

    board = pattern_creator.create(800)
    text_file = open("build/board_pattern.txt", "w")
    text_file.write(Pattern(txt_to_matrix(board.txt())).txt())
    text_file.close()


@bp.cli.command('board_print')
@inject
def board_print(
        printer: TiledPatternPrinter = Provide[Container.tiled_pattern_printer],
        pattern_creator: Pattern8x8With4DataFields = Provide[Container.pattern_creator]
):
    board = pattern_creator.create(800)
    printer.save_to_files(board, 10, 'build/print/board_print_')


@bp.cli.command('mockbot_pictures')
@inject
def mockbot_pictures(
        mock_picture_creator: MockbotPictureCreator = Provide[Container.mockbot_picture_creator],
):
    mock_picture_creator.create()


@bp.cli.command('test_get_angle_points')
@inject
def test_get_angle_points(

):
    angle_data = [
        # ['', [Point(0, 0), Point(1, 0), Point(1, 0)]],
        # ['', [Point(1, 0), Point(0, 0), Point(1, 0)]],
        # ['', [Point(1, 0), Point(1, 0), Point(0, 0)]],

        # ['', [Point(0, 0), Point(0, 1), Point(0, 1)]],
        # ['', [Point(0, 1), Point(0, 0), Point(0, 1)]],
        # ['', [Point(0, 1), Point(0, 1), Point(0, 0)]],

        ['010010', [Point(0, 0), Point(0, 1), Point(1, 0)]],
        ['010010', [Point(0, 0), Point(1, 0), Point(0, 1)]],

        ['101101', [Point(1, 1), Point(0, 1), Point(1, 0)]],
        ['101101', [Point(1, 1), Point(1, 0), Point(0, 1)]],

        ['000111', [Point(0, 1), Point(0, 0), Point(1, 1)]],
        ['000111', [Point(0, 1), Point(1, 1), Point(0, 0)]],

        ['111000', [Point(1, 0), Point(1, 1), Point(0, 0)]],
        ['111000', [Point(1, 0), Point(0, 0), Point(1, 1)]],

        # ['', [Point(450, 450), Point(450, 510), Point(510, 450)]],
        # ['', [Point(449, 450), Point(509, 449), Point(450, 510)]],

        # ['', [Point(0, 0), Point(0, 1), Point(1, 1)]],
        # ['', [Point(0, 0), Point(1, 1), Point(1, 0)]],
        # ['', [Point(0, 0), Point(-1, 0), Point(0, -1)]],
        # ['', [Point(0, 0), Point(0, -1), Point(-1, 0)]],
    ]
    # for ex, c, a, b in angle_data:
        # ac = get_angle(b, c, a)
        # print('test get_angle', int(ac) == ex, ac, ex, c.txt, a.txt, b.txt)


    data = [
        ['000110', [Point(437, 478), Point(480, 437), Point(521, 481), Point(478, 522), Point(396, 435), Point(439, 394), Point(525, 397), Point(392, 519), Point(565, 440), Point(434, 563)]],
    ]


    for ex, d in angle_data:
        try:
            a, b, c = create_angel_points(d)

            rs = ''.join([''.join([str(m.x) + str(m.y) for m in [a, b, c]])])

            print(ex, rs, rs == ex, a.txt, b.txt, c.txt, get_angle(c, b, a))
        except RuntimeError:
            print('error')

    for ex, d in data:
        a, b, c = create_angel_points(d)
        rs = ''.join([''.join([str(m.x) + str(m.y) for m in [a, b, c]])])

        print(ex, rs, rs == ex, a.txt, b.txt, c.txt, get_angle(c, b, a))

        print(a.txt, b.txt, c.txt, get_angle(c, b, a))


@bp.cli.command('test_captcha')
@inject
def test_captcha(
        mockbots: MockBots = Provide[Container.mockbots],
        mockbot_tester: MockBotTester = Provide[Container.mockbot_tester],
):

    result = [mockbot_tester.test_captcha(bot) for bot in mockbots.bots]
    dump_txt('build/mockbot/_test_result.html', render_template('mockbots.html.j2', result=result))

