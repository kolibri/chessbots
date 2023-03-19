from flask import (render_template)
import random

import cv2
import numpy as np
from flask import Blueprint
from chessbots.tool.pattern_creator import Pattern8x8With4DataFields
from chessbots.tool.printer import *
from chessbots.lib.captcha.captcha_reader import *
from chessbots.lib.captcha.captcha_resolver import *
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
            a, b, c = find_angel_points(d)

            rs = ''.join([''.join([str(m.x) + str(m.y) for m in [a, b, c]])])

            print(ex, rs, rs == ex, a.txt, b.txt, c.txt, get_angle(c, b, a))
        except RuntimeError:
            print('error')

    for ex, d in data:
        a, b, c = find_angel_points(d)
        rs = ''.join([''.join([str(m.x) + str(m.y) for m in [a, b, c]])])

        print(ex, rs, rs == ex, a.txt, b.txt, c.txt, get_angle(c, b, a))

        print(a.txt, b.txt, c.txt, get_angle(c, b, a))


@bp.cli.command('test_captcha_to_txt')
@inject
def test_captcha_to_txt(
        mockbots: MockBots = Provide[Container.mockbots],
):
    def assert_result(captcha, bot) -> str:
        if captcha.result.txt() == bot.pattern.txt():
            return '.'
        elif captcha.result.find_matches(bot.pattern.create_snapshot(Point(4, 4), Point(8, 8))):
            return ':'
        return 'F'

    def test_mockbots(bots: MockBots):
        output = ''
        failed = []
        raw = []
        for bot in bots.bots:
            path = os.path.join('build/mockbot/', bot.picture())
            captcha = CaptchaResult(path)
            captcha.draw_debug_images()
            # result = assert_result(captcha, bot)

            # output = output + result
            # if 'F' == result:
            #     failed.append([bot, captcha])
            raw.append([bot, captcha, assert_result(captcha, bot), bot.pattern.create_snapshot(Point(4, 4), Point(8, 8))])
            # print('{:.4f}'.format(captcha.angle), captcha.grid_dirs)
        return output, failed, raw

    test_sum, failed, raw = test_mockbots(mockbots)
    dbg = render_template('mockbots.html', test_sum=test_sum, result=failed, raw=raw)
    dump_txt('build/mockbot/_test_result.html', dbg)

    print(test_sum)
    print([[f[0].name, f[0].pattern.create_snapshot(Point(4, 4), Point(8, 8)).txt(), f[1].grid_dirs] for f in failed])


# @bp.cli.command('test_txt_to_position')
# @inject
# def test_txt_to_position(
#         captcha_reader: CaptchaReader = Provide[Container.captcha_reader],
#         captcha_resolver: CaptchaResolver = Provide[Container.captcha_resolver],
# ):
#     for bot in MockBots().bots:
#         path = os.path.join('build/mockbot/', bot.picture())
#         print(bot.picture())
#         board, angle = captcha_reader.resolve(path)
#         solutions, position, raw = captcha_resolver.resolve(board.txt())
#         dbg = render_template('txt_to_pos.txt', solutions=solutions, result=position, raw=raw, bot=bot, board=board)
#         dump_txt(path + '_board_.txt', board.txt())
#         dump_txt(path + '_txt_to_pos.txt', dbg)
#
#         # solved = [p.solve() for p in solutions]¹
#         # solved_set = list(set(solved))
#         # if 1 == len(solved_set):
#         #     solved_pos = solved_set[0]
#         #     solved_pos = Point(solved_pos.y, solved_pos.x) # fix
#         #     result = bot.pos == solved_pos
#         #     print('compare bot:', result, bot.pos, solved_pos)
#
#         # print('bot:', bot.name, [[m.value, m.matching, m.position, m.snapshot.txt()] for m in position])        # print('position: ', bot.picture(), board.txt(), position)
