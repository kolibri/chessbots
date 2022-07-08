import cv2
from ..flaskr import create_app
from ..flaskr.BotData.Captcha import Captcha
from ..flaskr.BotData.Board import *


def test_captcha():
    def assert_snippet_is_board(snippet_path: str, board_txt: str, rotation: float):
        templates = [
            ['flaskr/static/images/pattern/pattern_WO.jpeg', 0],
            ['flaskr/static/images/pattern/pattern_WX.jpeg', 1],
            ['flaskr/static/images/pattern/pattern_BO.jpeg', 0],
            ['flaskr/static/images/pattern/pattern_BX.jpeg', 1]
        ]
        captcha = Captcha(snippet_path, templates)
        expected_board = Board(txt_to_matrix(board_txt))
        angle, board = captcha.resolve()

        assert angle == rotation
        assert board.txt() == expected_board.txt()

    tests = [
        [
            'flaskr/static/images/mockbot/mockbot_01.jpeg',
            '\n'.join([
                '00000000',
                '00000000',
                '00000000',
                '00000001',
                '00000000',
                '00000000',
                '00000000',
                '10101011',
            ]), 0
        ],
        [
            'flaskr/static/images/mockbot/mockbot_02.jpeg',
            '\n'.join([
                '00100000',
                '00010010',
                '00000001',
                '00010000',
                '00110001',
                '00000011',
                '00000000',
                '00010000',
            ]), 0
        ],
    ]
    for t in tests:
        assert_snippet_is_board(t[0], t[1], t[2])
