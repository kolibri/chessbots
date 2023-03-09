import random

import cv2
import numpy as np
from flask import Blueprint
from chessbots.tool.pattern_creator import Pattern8x8With4DataFields
from chessbots.tool.printer import *
from chessbots.lib.captcha.captcha_reader import *
from dependency_injector.wiring import inject, Provide
from chessbots.board.containers import Container
from chessbots.lib.bot.mockbot import *

bp = Blueprint('script', __name__)


@bp.cli.command('pattern_test')
@inject
def pattern_test(pattern_creator: Pattern8x8With4DataFields = Provide[Container.pattern_creator]):
    board = pattern_creator.create(800)

    text_file = open("build/board_pattern.txt", "w")
    text_file.write(board.txt())
    text_file.close()


@bp.cli.command('board_print')
@inject
def board_print(
        printer: TiledPatternPrinter = Provide[Container.tiled_pattern_printer],
        pattern_creator: Pattern8x8With4DataFields = Provide[Container.pattern_creator]
):
    board = pattern_creator.create(800)
    printer.save_to_files(board, 10, 'build/board_print_')


@bp.cli.command('mockbot_pictures')
@inject
def mockbot_pictures(
        creator: MockbotPictureCreator = Provide[Container.mockbot_picture_creator],
        pattern_creator: Pattern8x8With4DataFields = Provide[Container.pattern_creator]
):
    for bot in MockBots().bots:
        creator.create(bot.name, pattern_creator.create(800), bot.pos, bot.size, bot.angle)


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
