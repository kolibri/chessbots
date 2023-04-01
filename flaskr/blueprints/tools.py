from flask import (render_template)

from flask import Blueprint

from chessbots.lib.mockbot import MockBots, MockBot
from chessbots.tool.pattern_creator import Pattern8x8With4DataFields
from chessbots.lib.pattern import *
from chessbots.tool.printer import *
from chessbots.lib.captcha import Captcha
from chessbots.lib.captcha.grid import create_angel_points
from dependency_injector.wiring import inject, Provide
from flaskr.containers import Container
from chessbots.lib.filesystem import *
import os
bp = Blueprint('script', __name__)


@bp.cli.command('pattern_test')
@inject
def pattern_test():
    board = Pattern8x8With4DataFields().create(800)
    text_file = open("build/board_pattern.txt", "w")
    text_file.write(Pattern(txt_to_matrix(board.txt())).txt())
    text_file.close()


@bp.cli.command('board_print')
@inject
def board_print(
        printer: TiledPatternPrinter = Provide[Container.tiled_pattern_printer],
):
    board = Pattern8x8With4DataFields().create(800)
    printer.save_to_files(board, 10, 'build/print/board_print_')


@bp.cli.command('create_mockbot')
@inject
def create_mockbot(
        mockbots: MockBots = Provide[Container.mockbots],
):
    bot_set = [
        ['test', 'wk', Point(0, 0), 0]
    ]

    for bot in bot_set:
        mockbots.add(*bot)


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


# @bp.cli.command('test_captcha')
# @inject
# def test_captcha(
#         mockbots: MockBots = Provide[Container.mockbots],
# ):
#     def test_captcha(bot: MockBot):
#         result_filename = os.path.join('build/mockbot', 'a' + bot.name + '_position_result.html')
#
#         if os.path.isfile(result_filename):
#             print('Already calculated, skip')
#             return
#
#         captcha = Captcha(os.path.join('build/mockbot', bot.picture()))
#         captcha.draw_debug_images()
#         # print('mockbot test', bot.name, captcha.flaskr.txt(), captcha.position.txt)
#
#         exp_pos = Point(bot.pos.x // 4, bot.pos.y // 4).add(Point(1, 1))
#         pos_tol = Point(1, 1)
#         test_result_position = captcha.position.in_area([exp_pos.sub(pos_tol), exp_pos.add(pos_tol)])
#
#         ang_tol = 1
#         ang_act = captcha.rotation
#         ang_exp = bot.angle
#         test_result_angle = ang_exp - ang_tol < ang_act < ang_exp + ang_tol
#         print(test_result_position, test_result_angle, bot.name, exp_pos, captcha.position, exp_pos.sub(pos_tol), exp_pos.add(pos_tol), 'a', ang_exp, ang_act)
#
#         dump_txt(
#             result_filename,
#             render_template(
#                 'mockbots_result.html.j2',
#                 bot=bot,
#                 captcha=captcha,
#                 res=test_result_position,
#                 ang_res=test_result_position,
#                 target_pos=exp_pos
#             )
#         )
#
#         return bot, captcha, test_result_position, test_result_angle, exp_pos
#
#     for bot in mockbots.bots:
#         test_captcha(bot)
#
#     base_dir = 'build/mockbot'
#     files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f)) and f.endswith('_position_result.html')]
#     files.sort()
#     print(files)
#     contents = [read_txt(os.path.join(base_dir, f)) for f in files]
#     dump_txt('build/mockbot/_test_result.html', render_template('mockbots.html.j2', result=contents))

