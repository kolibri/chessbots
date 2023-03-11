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
        creator: MockbotPictureCreator = Provide[Container.mockbot_picture_creator],
        pattern_creator: Pattern8x8With4DataFields = Provide[Container.pattern_creator]
):
    for bot in MockBots().bots:
        creator.create(bot, pattern_creator.create(800))


@bp.cli.command('test_captcha_to_txt')
@inject
def test_captcha_to_txt(
        captcha_reader: CaptchaReader = Provide[Container.captcha_reader]
):
    for bot in MockBots().bots:
        path = os.path.join('build/mockbot/', bot.picture())
        board, angle = captcha_reader.resolve(path)
        # print(board.txt())
        # print(angle)


@bp.cli.command('test_txt_to_position')
@inject
def test_txt_to_position(
        captcha_reader: CaptchaReader = Provide[Container.captcha_reader],
        captcha_resolver: CaptchaResolver = Provide[Container.captcha_resolver],
):
    for bot in MockBots().bots:
        path = os.path.join('build/mockbot/', bot.picture())
        print(bot.picture())
        board, angle = captcha_reader.resolve(path)
        position, raw = captcha_resolver.resolve(board.txt())
        dbg = render_template('txt_to_pos.txt', pos=position, raw=raw, bot=bot, board=board)
        dump_txt(path + '_board_.txt', board.txt())
        dump_txt(path + '_txt_to_pos.txt', dbg)

        solved = [p.guess.solved for p in position]
        solved_set = list(set(solved))
        if 1 == len(solved_set):
            solved_pos = solved_set[0]
            solved_pos = Point(solved_pos.y, solved_pos.x) # fix
            result = bot.pos == solved_pos
            print('compare bot:', result, bot.pos, solved_pos)

        # print('bot:', bot.name, [[m.value, m.matching, m.position, m.snapshot.txt()] for m in position])        # print('position: ', bot.picture(), board.txt(), position)
