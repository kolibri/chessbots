import cv2
from flask import (render_template)
from reportlab.pdfgen import canvas

from flask import Blueprint

from chessbots.lib.mockbot import *
from chessbots.tool.pattern_creator import Pattern8x8With4DataFields
from chessbots.tool.printer import *
from chessbots.lib.captcha import *
from chessbots.lib.captcha.marker import *
from dependency_injector.wiring import inject, Provide
from flaskr.containers import Container
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
def board_print():

    printer = BoardPrinter()
    for x in range(0, 2): # 10 for all
        for y in range(0, 3): # 10 for all
            p = Point(x, y)
            printer.chess_tile_to_pdf(p, os.path.join('build/print/', 'tile_' + p.txt + '.pdf'))

    printer.get_test_tile_pdf(os.path.join('build/print/', 'tile_test.pdf'))


@bp.cli.command('test_new_printer')
def test_new_printer():
    printer = BoardPrinter()
    BoardPrinter.to_file(printer.get_test_tile(), 'build/test_tile.jpg')

    def inverte(imagem):
        return 255 - imagem

    treshs = [230, 40, 140]

    img = cv2.imread('build/test_tile.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = inverte(img)
    _, img = cv2.threshold(img, treshs[0], 255, cv2.THRESH_TOZERO_INV)
    cv2.imwrite('build/test_thresh_0.jpg', img)
    _, img = cv2.threshold(img, treshs[1], 255, cv2.THRESH_TOZERO)
    cv2.imwrite('build/test_thresh_1.jpg', img)
    img = inverte(img)
    cv2.imwrite('build/test_thresh_2.jpg', img)
    _, img = cv2.threshold(img, treshs[2], 255, cv2.THRESH_BINARY)
    cv2.imwrite('build/test_thresh.jpg', img)

    BoardPrinter.to_file(printer.get_snapshot(Point(9, 19), Point(2, 2)), 'build/test_snapshot.jpg')

    captcha = Captcha('build/test_snapshot.jpg')
    captcha.draw_debug_images()


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


@bp.cli.command('test_captcha')
@inject
def test_captcha():
    filename = 'build/live/l00001.jpg'
    captcha = Captcha(filename)
    captcha.draw_debug_images()

    print('result', captcha.position, captcha.angle)

