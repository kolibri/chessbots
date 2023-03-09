import random

import cv2
import numpy as np
from flask import Blueprint
from chessbots.tool.pattern_creator import Pattern8x8With4DataFields
from chessbots.tool.printer import *
from chessbots.tool.mockbot import *
from chessbots.lib.captcha.captcha_reader import *
from dependency_injector.wiring import inject, Provide
from chessbots.board.containers import Container

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
    creator.create('00', pattern_creator.create(800), Point(0, 0), Point(16, 16))
    creator.create('01', pattern_creator.create(800), Point(16, 16), Point(16, 16), 45)
    creator.create('02', pattern_creator.create(800), Point(42, 13), Point(16, 16), 90)
    creator.create('03', pattern_creator.create(800), Point(322, 384), Point(16, 16), 180)
    creator.create('04', pattern_creator.create(800), Point(123, 123), Point(16, 16), 123)
    creator.create('05', pattern_creator.create(800), Point(123, 456), Point(16, 16), 78)
    creator.create('06', pattern_creator.create(800), Point(423, 225), Point(16, 16), 38)
    creator.create('07', pattern_creator.create(800), Point(253, 613), Point(16, 16), 276)
    creator.create('08', pattern_creator.create(800), Point(253, 273), Point(16, 16), 48)
    creator.create('09', pattern_creator.create(800), Point(587, 243), Point(16, 16), 271)


@bp.cli.command('test_captcha_to_txt')
@inject
def test_captcha_to_txt(
    captcha_reader: CaptchaReader = Provide[Container.captcha_reader]
):
    pictures = ['build/mockbot/mockbot_0' + str(i) + '.jpg' for i in range(0, 10)]

    for picture in pictures:
        board, angle = captcha_reader.resolve(picture)
        print(board.txt())
        print(angle)

