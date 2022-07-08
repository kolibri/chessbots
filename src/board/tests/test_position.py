import cv2
from ..flaskr import create_app
from ..flaskr.BotData.Captcha import Captcha
from ..flaskr.BotData.Board import *
from ..flaskr.Utils.BoardUtils import *


def test_position():
    def assert_board_finds_position(board, snapshot, position, field):
        given = Board(txt_to_matrix(snapshot))
        assert board.find_matches(given) == position
        assert board.matches_to_fields(given, 10) == field

    board = Board(txt_to_matrix(create_txt_board_4x4_bin(10)))

    tests = [
        [
            '\n'.join([
                '00000000',
                '00000000',
                '00000000',
                '00000001',
                '00000000',
                '00000000',
                '00000000',
                '10101011',
            ]),
            [((0, 0), 0)],
            [((0, 0), 0)],
        ],
        [
            '\n'.join([
                '00100000',
                '00010010',
                '00000001',
                '00010000',
                '00110001',
                '00000011',
                '00000000',
                '00010000',
            ]),
            [((20, 8), 270)],
            [((5, 2), 270)],
        ]
    ]
    for test in tests:
        assert_board_finds_position(board, test[0], test[1], test[2])
