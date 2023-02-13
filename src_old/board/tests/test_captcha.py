import numpy as np
import cv2
from ..flaskr import create_app
from ..flaskr.BotData.Captcha import *
from ..flaskr.BotData.Board import *
from collections import namedtuple

MarkedPos = namedtuple('MarkedPos', 'p1 p2 txt')


def test_create_marked_images():
    def create_marked_images(bot_index: int, suffix: str, markers: [MarkedPos], color):
        img = cv2.imread(get_image_path(bot_index))
        for mark in markers:
            cv2.rectangle(img, mark.p1, mark.p2, color, 2)
            cv2.putText(img, mark.txt, add_points(mark.p1, Point(5, 25)), cv2.FONT_ITALIC, 0.8, color)

        cv2.imwrite(get_image_path(bot_index, suffix), img)

    def get_image_path(bot_index: int, suffix: str = '') -> str:
        if '' == suffix:
            return 'tests/images/source/mockbot_' + str(bot_index) + '.jpeg'
        return 'tests/images/result/mockbot_' + str(bot_index) + '_' + suffix + '.jpeg'

    def point_to_txt(point: PointImg) -> str:
        return str(point.x) + 'x' + str(point.y)

    mf = MarkerFinder([
        ['tests/images/source/pattern_WO.jpeg', 0],
        ['tests/images/source/pattern_WX.jpeg', 1],
        ['tests/images/source/pattern_BO.jpeg', 0],
        ['tests/images/source/pattern_BX.jpeg', 1]
    ], 100)
    gr = GridResolver()

    pattern_example = cv2.imread('tests/images/source/pattern_WO.jpeg')
    pattern_size = PointImg(pattern_example.shape[0], pattern_example.shape[1])
    results_ok = True

    for bot_index in range(1, 9+1):
        img = cv2.imread(get_image_path(bot_index))
        img_size = PointImg(img.shape[0], img.shape[1])

        try:

            # first step: find markers in image and clean them up
            found_marks = mf.find_markers(img)
            markers_tm = [MarkedPos(m.point, add_points(m.point, pattern_size), str(m.marker) + ': ' + point_to_txt(m.point)) for m in found_marks]
            create_marked_images(bot_index, 'markers', markers_tm, (int(255), int(0), int(255)))

            # second step: find the points nearest to center and calculate angel
            # ap = AngelCalculator.get_nearest_to_center(markers)
            ap = AngelCalculator.find_angel_points(found_marks)
            angle_tm = [
                MarkedPos(ap[0], add_points(ap[0], pattern_size), '0: ' + str(int(AngelCalculator.get_angle(ap[0], ap[1], ap[2]))) + ' - ' + point_to_txt(ap[0])),
                MarkedPos(ap[1], add_points(ap[1], pattern_size), '1: ' + str(int(AngelCalculator.get_angle(ap[1], ap[2], ap[0]))) + ' - ' + point_to_txt(ap[1])),
                MarkedPos(ap[2], add_points(ap[2], pattern_size), '2: ' + str(int(AngelCalculator.get_angle(ap[2], ap[0], ap[1]))) + ' - ' + point_to_txt(ap[2])),
            ]
            create_marked_images(bot_index, 'angle', angle_tm, (int(123), int(255), int(123)))

            # third step: resolve grid and return board
            grid = gr.resolve_grid(found_marks, img_size)
            grid_tm = [MarkedPos(g.mark.point, add_points(g.mark.point, pattern_size), str(g.mark.marker) + '' + point_to_txt(g.grid)) for g in grid]
            create_marked_images(bot_index, 'grid', grid_tm, (int(255), int(255), int(0)))

            print(get_image_path(bot_index))

        except RuntimeError:
            print("Failed result images for" + str(bot_index))
            results_ok = False

    assert True == results_ok


'''
def test_angel_calculator():
    ac = AngelCalculator()
    assert 90 == ac.get_angle(PointImg(1, 0), PointImg(0, 0), PointImg(0, 1))
    assert [

               PointImg(x=162, y=212),
               PointImg(x=212, y=212),
               PointImg(x=212, y=162),

               # PointImg(x=162, y=62),  # 0, 143.13629868066312],
               # PointImg(x=112, y=62),  # 0, 163.67040050051813],
               # PointImg(x=162, y=12),  # 0, 191.80198122021577],

           ] == ac.find_angel_points([
        [PointImg(x=162, y=162), 0, 53.74011537017761],
        [PointImg(x=212, y=212), 0, 16.97056274847714],
        [PointImg(x=262, y=212), 0, 63.150613615387776],
        [PointImg(x=312, y=212), 0, 112.64102272262978],
        [PointImg(x=362, y=212), 0, 162.4438364481706],
        [PointImg(x=312, y=112), 0, 142.43595051811886],
        [PointImg(x=362, y=112), 0, 184.35834670553976],
        [PointImg(x=212, y=162), 0, 39.84971769034255],
        [PointImg(x=262, y=162), 0, 72.71863585079137],
        [PointImg(x=112, y=212), 0, 88.81441324469807],
        [PointImg(x=162, y=212), 0, 39.84971769034255],
    ])


def test_grid_resolver_to_text():
    mf = MarkerFinder([
        ['tests/images/source/pattern_WO.jpeg', 0],
        ['tests/images/source/pattern_WX.jpeg', 1],
        ['tests/images/source/pattern_BO.jpeg', 0],
        ['tests/images/source/pattern_BX.jpeg', 1]
    ])
    gr = GridResolver()
    img_path = 'tests/images/source/mockbot_01.jpeg'
    img = cv2.imread(img_path)

    markers = mf.find_markers(img)
    result = gr.grid_to_txt(gr.resolve_grid(markers, PointImg(img.shape[0], img.shape[1])))

    assert '00000000\n00000000\n00000000\n00000001\n00000000\n00000000\n00000000\n10101011\n' == result


def test_captcha():
    def assert_snippet_is_board(snippet_path: str, board_txt: str, rotation: float):
        templates = [
            ['tests/images/source/pattern_WO.jpeg', 0],
            ['tests/images/source/pattern_WX.jpeg', 1],
            ['tests/images/source/pattern_BO.jpeg', 0],
            ['tests/images/source/pattern_BX.jpeg', 1]
        ]
        tol = 3
        captcha = Captcha(snippet_path, templates)
        board, angle = captcha.resolve()

        assert board_txt == board.txt()

        if 90 < angle + tol:
            assert 90 + tol > angle > 90 - tol
        else:
            assert 0 + tol > angle > 0 - tol

    # Note:
    # even if source image is rotated, we just need the angle the captcha is tilted. via Board, we get the orientation
    tests = [
        [
            'tests/images/source/mockbot_01.jpeg',
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
        # [
        #     'tests/images/source/mockbot_02.jpeg',
        #     '\n'.join([
        #         '00100000',
        #         '00010010',
        #         '00000001',
        #         '00010000',
        #         '00110001',
        #         '00000011',
        #         '00000000',
        #         '00010000',
        #     ]),
        #     0
        # ],
    ]
    for t in tests:
        assert_snippet_is_board(t[0], t[1], t[2])

'''


def test_marker_finder_can_filter_doubles():
    mf = MarkerFinder([
        ['tests/images/source/pattern_WO.jpeg', 0],
        ['tests/images/source/pattern_WX.jpeg', 1],
        ['tests/images/source/pattern_BO.jpeg', 0],
        ['tests/images/source/pattern_BX.jpeg', 1]
    ], 5)

    assert [
               [PointImg(x=12, y=12), 0, 265.87214972614186],
               [PointImg(x=62, y=12), 0, 233.21234958723778],
               [PointImg(x=112, y=12), 0, 207.57649192526594]

           ] == mf.filter_overlapping([
        [PointImg(x=12, y=12), 0, 265.87214972614186],
        [PointImg(x=12, y=12), 0, 265.87214972614186],
        [PointImg(x=62, y=12), 0, 233.21234958723778],
        [PointImg(x=112, y=12), 0, 207.57649192526594]
    ], [])

    result = mf.filter_overlapping([
        [PointImg(x=12, y=12), 0, 265.87214972614186],
        [PointImg(x=62, y=12), 0, 233.21234958723778],
        [PointImg(x=112, y=12), 0, 207.57649192526594],
        [PointImg(x=162, y=12), 0, 191.80198122021577],
        [PointImg(x=12, y=62), 0, 233.21234958723778],
        [PointImg(x=62, y=62), 0, 195.16147160748713],
        [PointImg(x=112, y=62), 0, 163.67040050051813],
        [PointImg(x=162, y=62), 0, 143.13629868066312],
        [PointImg(x=12, y=112), 0, 207.57649192526594],
        [PointImg(x=62, y=112), 0, 163.67040050051813],
        [PointImg(x=112, y=112), 0, 124.45079348883236],
        [PointImg(x=162, y=112), 0, 95.85405573057407],
        [PointImg(x=12, y=162), 0, 191.80198122021577],
        [PointImg(x=62, y=162), 0, 143.13629868066312],
        [PointImg(x=112, y=162), 0, 95.85405573057407],
        [PointImg(x=162, y=162), 0, 53.74011537017761],
        [PointImg(x=212, y=212), 0, 16.97056274847714],
        [PointImg(x=262, y=212), 0, 63.150613615387776],
        [PointImg(x=312, y=212), 0, 112.64102272262978],
        [PointImg(x=362, y=212), 0, 162.4438364481706],
        [PointImg(x=212, y=262), 0, 63.150613615387776],
        [PointImg(x=262, y=262), 0, 87.68124086713189],
        [PointImg(x=312, y=262), 0, 128.01562404644207],
        [PointImg(x=362, y=262), 0, 173.4589288563722],
        [PointImg(x=212, y=312), 0, 112.64102272262978],
        [PointImg(x=262, y=312), 0, 128.01562404644207],
        [PointImg(x=312, y=312), 0, 158.39191898578665],
        [PointImg(x=362, y=312), 0, 196.9466932954194],
        [PointImg(x=262, y=362), 0, 173.4589288563722],
        [PointImg(x=212, y=361), 1, 161.4465855941215],
        [PointImg(x=312, y=361), 1, 196.1249601657066],
        [PointImg(x=362, y=361), 1, 228.39658491317246],
        [PointImg(x=211, y=362), 1, 162.3730273167314],
        [PointImg(x=212, y=362), 1, 162.4438364481706],
        [PointImg(x=213, y=362), 1, 162.5207679036744],
        [PointImg(x=311, y=362), 1, 196.3797341886377],
        [PointImg(x=312, y=362), 1, 196.9466932954194],
        [PointImg(x=313, y=362), 1, 197.51708786836647],
        [PointImg(x=361, y=362), 1, 228.39658491317246],
        [PointImg(x=362, y=362), 1, 229.1025971044414],
        [PointImg(x=363, y=362), 1, 229.8107917396396],
        [PointImg(x=212, y=363), 1, 163.44112089679268],
        [PointImg(x=312, y=363), 1, 197.77006851391846],
        [PointImg(x=362, y=363), 1, 229.8107917396396],
        [PointImg(x=212, y=12), 0, 188.38258942906586],
        [PointImg(x=262, y=12), 0, 197.9595918363139],
        [PointImg(x=312, y=12), 0, 218.8332698654389],
        [PointImg(x=362, y=12), 0, 248.16929705344293],
        [PointImg(x=212, y=62), 0, 138.52075656738234],
        [PointImg(x=262, y=62), 0, 151.28780519261954],
        [PointImg(x=312, y=62), 0, 177.73013250431114],
        [PointImg(x=362, y=62), 0, 212.8097742116184],
        [PointImg(x=212, y=112), 0, 88.81441324469807],
        [PointImg(x=262, y=112), 0, 107.64757312638311],
        [PointImg(x=312, y=112), 0, 142.43595051811886],
        [PointImg(x=362, y=112), 0, 184.35834670553976],
        [PointImg(x=212, y=162), 0, 39.84971769034255],
        [PointImg(x=262, y=162), 0, 72.71863585079137],
        [PointImg(x=312, y=162), 0, 118.27087553578015],
        [PointImg(x=12, y=212), 0, 188.38258942906586],
        [PointImg(x=62, y=212), 0, 138.52075656738234],
        [PointImg(x=112, y=212), 0, 88.81441324469807],
        [PointImg(x=162, y=212), 0, 39.84971769034255],
        [PointImg(x=12, y=262), 0, 197.9595918363139],
        [PointImg(x=62, y=262), 0, 151.28780519261954],
        [PointImg(x=112, y=262), 0, 107.64757312638311],
        [PointImg(x=162, y=262), 0, 72.71863585079137],
        [PointImg(x=12, y=312), 0, 218.8332698654389],
        [PointImg(x=62, y=312), 0, 177.73013250431114],
        [PointImg(x=112, y=312), 0, 142.43595051811886],
        [PointImg(x=162, y=312), 0, 118.27087553578015],
        [PointImg(x=62, y=362), 0, 212.8097742116184],
        [PointImg(x=162, y=362), 0, 166.39711535961192],
        [PointImg(x=362, y=161), 1, 166.6283289239858],
        [PointImg(x=361, y=162), 1, 165.42369842317032],
        [PointImg(x=362, y=162), 1, 166.39711535961192],
        [PointImg(x=363, y=162), 1, 167.37084572887835],
        [PointImg(x=362, y=163), 1, 166.1715980545412],
        [PointImg(x=12, y=361), 1, 247.51767613647314],
        [PointImg(x=112, y=361), 1, 183.48024416813925],
        [PointImg(x=11, y=362), 1, 248.92770034690795],
        [PointImg(x=12, y=362), 1, 248.16929705344293],
        [PointImg(x=13, y=362), 1, 247.41261083461367],
        [PointImg(x=111, y=362), 1, 184.83776670366908],
        [PointImg(x=112, y=362), 1, 184.35834670553976],
        [PointImg(x=113, y=362), 1, 183.88311504866346],
        [PointImg(x=12, y=363), 1, 248.82323042674292],
        [PointImg(x=112, y=363), 1, 185.23768515072737]
    ], [])

    assert [
               [PointImg(x=12, y=12), 0, 265.87214972614186],
               [PointImg(x=62, y=12), 0, 233.21234958723778],
               [PointImg(x=112, y=12), 0, 207.57649192526594],
               [PointImg(x=162, y=12), 0, 191.80198122021577],
               [PointImg(x=12, y=62), 0, 233.21234958723778],
               [PointImg(x=62, y=62), 0, 195.16147160748713],
               [PointImg(x=112, y=62), 0, 163.67040050051813],
               [PointImg(x=162, y=62), 0, 143.13629868066312],
               [PointImg(x=12, y=112), 0, 207.57649192526594],
               [PointImg(x=62, y=112), 0, 163.67040050051813],
               [PointImg(x=112, y=112), 0, 124.45079348883236],
               [PointImg(x=162, y=112), 0, 95.85405573057407],
               [PointImg(x=12, y=162), 0, 191.80198122021577],
               [PointImg(x=62, y=162), 0, 143.13629868066312],
               [PointImg(x=112, y=162), 0, 95.85405573057407],
               [PointImg(x=162, y=162), 0, 53.74011537017761],
               [PointImg(x=212, y=212), 0, 16.97056274847714],
               [PointImg(x=262, y=212), 0, 63.150613615387776],
               [PointImg(x=312, y=212), 0, 112.64102272262978],
               [PointImg(x=362, y=212), 0, 162.4438364481706],
               [PointImg(x=212, y=262), 0, 63.150613615387776],
               [PointImg(x=262, y=262), 0, 87.68124086713189],
               [PointImg(x=312, y=262), 0, 128.01562404644207],
               [PointImg(x=362, y=262), 0, 173.4589288563722],
               [PointImg(x=212, y=312), 0, 112.64102272262978],
               [PointImg(x=262, y=312), 0, 128.01562404644207],
               [PointImg(x=312, y=312), 0, 158.39191898578665],
               [PointImg(x=362, y=312), 0, 196.9466932954194],
               [PointImg(x=262, y=362), 0, 173.4589288563722],
               [PointImg(x=212, y=361), 1, 161.4465855941215],
               [PointImg(x=312, y=361), 1, 196.1249601657066],
               [PointImg(x=362, y=361), 1, 228.39658491317246],
               [PointImg(x=212, y=12), 0, 188.38258942906586],
               [PointImg(x=262, y=12), 0, 197.9595918363139],
               [PointImg(x=312, y=12), 0, 218.8332698654389],
               [PointImg(x=362, y=12), 0, 248.16929705344293],
               [PointImg(x=212, y=62), 0, 138.52075656738234],
               [PointImg(x=262, y=62), 0, 151.28780519261954],
               [PointImg(x=312, y=62), 0, 177.73013250431114],
               [PointImg(x=362, y=62), 0, 212.8097742116184],
               [PointImg(x=212, y=112), 0, 88.81441324469807],
               [PointImg(x=262, y=112), 0, 107.64757312638311],
               [PointImg(x=312, y=112), 0, 142.43595051811886],
               [PointImg(x=362, y=112), 0, 184.35834670553976],
               [PointImg(x=212, y=162), 0, 39.84971769034255],
               [PointImg(x=262, y=162), 0, 72.71863585079137],
               [PointImg(x=312, y=162), 0, 118.27087553578015],
               [PointImg(x=12, y=212), 0, 188.38258942906586],
               [PointImg(x=62, y=212), 0, 138.52075656738234],
               [PointImg(x=112, y=212), 0, 88.81441324469807],
               [PointImg(x=162, y=212), 0, 39.84971769034255],
               [PointImg(x=12, y=262), 0, 197.9595918363139],
               [PointImg(x=62, y=262), 0, 151.28780519261954],
               [PointImg(x=112, y=262), 0, 107.64757312638311],
               [PointImg(x=162, y=262), 0, 72.71863585079137],
               [PointImg(x=12, y=312), 0, 218.8332698654389],
               [PointImg(x=62, y=312), 0, 177.73013250431114],
               [PointImg(x=112, y=312), 0, 142.43595051811886],
               [PointImg(x=162, y=312), 0, 118.27087553578015],
               [PointImg(x=62, y=362), 0, 212.8097742116184],
               [PointImg(x=162, y=362), 0, 166.39711535961192],
               [PointImg(x=362, y=161), 1, 166.6283289239858],
               [PointImg(x=12, y=361), 1, 247.51767613647314],
               [PointImg(x=112, y=361), 1, 183.48024416813925]

           ] == result

# def test_marker_finder_can_find_marks():
#     mf2 = MarkerFinder([
#         ['tests/images/source/pattern_WO.jpeg', 0],
#         ['tests/images/source/pattern_WX.jpeg', 1],
#         ['tests/images/source/pattern_BO.jpeg', 0],
#         ['tests/images/source/pattern_BX.jpeg', 1]
#     ])
#     # @todo: this list is not quite filtered, as it looks o_O
#     assert [
#                Mark(PointImg(x=12, y=12), 0, 265.87214972614186),
#                Mark(PointImg(x=62, y=12), 0, 233.21234958723778),
#                Mark(PointImg(x=112, y=12), 0, 207.57649192526594),
#                Mark(PointImg(x=162, y=12), 0, 191.80198122021577),
#                Mark(PointImg(x=12, y=62), 0, 233.21234958723778),
#                Mark(PointImg(x=62, y=62), 0, 195.16147160748713),
#                Mark(PointImg(x=112, y=62), 0, 163.67040050051813),
#                Mark(PointImg(x=162, y=62), 0, 143.13629868066312),
#                Mark(PointImg(x=12, y=112), 0, 207.57649192526594),
#                Mark(PointImg(x=62, y=112), 0, 163.67040050051813),
#                Mark(PointImg(x=112, y=112), 0, 124.45079348883236),
#                Mark(PointImg(x=162, y=112), 0, 95.85405573057407),
#                Mark(PointImg(x=12, y=162), 0, 191.80198122021577),
#                Mark(PointImg(x=62, y=162), 0, 143.13629868066312),
#                Mark(PointImg(x=112, y=162), 0, 95.85405573057407),
#                Mark(PointImg(x=162, y=162), 0, 53.74011537017761),
#                Mark(PointImg(x=212, y=212), 0, 16.97056274847714),
#                Mark(PointImg(x=262, y=212), 0, 63.150613615387776),
#                Mark(PointImg(x=312, y=212), 0, 112.64102272262978),
#                Mark(PointImg(x=362, y=212), 0, 162.4438364481706),
#                Mark(PointImg(x=212, y=262), 0, 63.150613615387776),
#                Mark(PointImg(x=262, y=262), 0, 87.68124086713189),
#                Mark(PointImg(x=312, y=262), 0, 128.01562404644207),
#                Mark(PointImg(x=362, y=262), 0, 173.4589288563722),
#                Mark(PointImg(x=212, y=312), 0, 112.64102272262978),
#                Mark(PointImg(x=262, y=312), 0, 128.01562404644207),
#                Mark(PointImg(x=312, y=312), 0, 158.39191898578665),
#                Mark(PointImg(x=362, y=312), 0, 196.9466932954194),
#                Mark(PointImg(x=262, y=362), 0, 173.4589288563722),
#                Mark(PointImg(x=212, y=361), 1, 161.4465855941215),
#                Mark(PointImg(x=312, y=361), 1, 196.1249601657066),
#                Mark(PointImg(x=362, y=361), 1, 228.39658491317246),
#                Mark(PointImg(x=212, y=12), 0, 188.38258942906586),
#                Mark(PointImg(x=262, y=12), 0, 197.9595918363139),
#                Mark(PointImg(x=312, y=12), 0, 218.8332698654389),
#                Mark(PointImg(x=362, y=12), 0, 248.16929705344293),
#                Mark(PointImg(x=212, y=62), 0, 138.52075656738234),
#                Mark(PointImg(x=262, y=62), 0, 151.28780519261954),
#                Mark(PointImg(x=312, y=62), 0, 177.73013250431114),
#                Mark(PointImg(x=362, y=62), 0, 212.8097742116184),
#                Mark(PointImg(x=212, y=112), 0, 88.81441324469807),
#                Mark(PointImg(x=262, y=112), 0, 107.64757312638311),
#                Mark(PointImg(x=312, y=112), 0, 142.43595051811886),
#                Mark(PointImg(x=362, y=112), 0, 184.35834670553976),
#                Mark(PointImg(x=212, y=162), 0, 39.84971769034255),
#                Mark(PointImg(x=262, y=162), 0, 72.71863585079137),
#                Mark(PointImg(x=312, y=162), 0, 118.27087553578015),
#                Mark(PointImg(x=12, y=212), 0, 188.38258942906586),
#                Mark(PointImg(x=62, y=212), 0, 138.52075656738234),
#                Mark(PointImg(x=112, y=212), 0, 88.81441324469807),
#                Mark(PointImg(x=162, y=212), 0, 39.84971769034255),
#                Mark(PointImg(x=12, y=262), 0, 197.9595918363139),
#                Mark(PointImg(x=62, y=262), 0, 151.28780519261954),
#                Mark(PointImg(x=112, y=262), 0, 107.64757312638311),
#                Mark(PointImg(x=162, y=262), 0, 72.71863585079137),
#                Mark(PointImg(x=12, y=312), 0, 218.8332698654389),
#                Mark(PointImg(x=62, y=312), 0, 177.73013250431114),
#                Mark(PointImg(x=112, y=312), 0, 142.43595051811886),
#                Mark(PointImg(x=162, y=312), 0, 118.27087553578015),
#                Mark(PointImg(x=62, y=362), 0, 212.8097742116184),
#                Mark(PointImg(x=162, y=362), 0, 166.39711535961192),
#                Mark(PointImg(x=362, y=161), 1, 166.6283289239858),
#                Mark(PointImg(x=12, y=361), 1, 247.51767613647314),
#                Mark(PointImg(x=112, y=361), 1, 183.48024416813925)
#
#            ] == mf2.find_markers(cv2.imread('tests/images/source/mockbot_01.jpeg'))


# def test_grid_resolver_resolves_to_grid():
#     mf = MarkerFinder([
#         ['tests/images/source/pattern_WO.jpeg', 0],
#         ['tests/images/source/pattern_WX.jpeg', 1],
#         ['tests/images/source/pattern_BO.jpeg', 0],
#         ['tests/images/source/pattern_BX.jpeg', 1]
#     ])
#     gr = GridResolver()
#     img_path = 'tests/images/source/mockbot_01.jpeg'
#     img = cv2.imread(img_path)
#
#     markers = mf.find_markers(img)
#     result = gr.resolve_grid(markers, PointImg(img.shape[0], img.shape[1]))
#
#     assert [
#                [PointGrid(x=-4, y=-4), Mark(PointImg(x=12, y=12), 0, 265.87214972614186), Point(x=12, y=12)],
#                [PointGrid(x=-4, y=-3), Mark(PointImg(x=62, y=12), 0, 233.21234958723778), Point(x=62, y=12)],
#                [PointGrid(x=-4, y=-2), Mark(PointImg(x=112, y=12), 0, 207.57649192526594), Point(x=112, y=12)],
#                [PointGrid(x=-4, y=-1), Mark(PointImg(x=162, y=12), 0, 191.80198122021577), Point(x=162, y=12)],
#                [PointGrid(x=-4, y=0), Mark(PointImg(x=212, y=12), 0, 188.38258942906586), Point(x=212, y=12)],
#                [PointGrid(x=-4, y=1), Mark(PointImg(x=262, y=12), 0, 197.9595918363139), Point(x=262, y=12)],
#                [PointGrid(x=-4, y=2), Mark(PointImg(x=312, y=12), 0, 218.8332698654389), Point(x=312, y=12)],
#                [PointGrid(x=-4, y=3), Mark(PointImg(x=362, y=12), 0, 248.16929705344293), Point(x=362, y=12)],
#                [PointGrid(x=-3, y=-4), Mark(PointImg(x=12, y=62), 0, 233.21234958723778), Point(x=12, y=62)],
#                [PointGrid(x=-3, y=-3), Mark(PointImg(x=62, y=62), 0, 195.16147160748713), Point(x=62, y=62)],
#                [PointGrid(x=-3, y=-2), Mark(PointImg(x=112, y=62), 0, 163.67040050051813), Point(x=112, y=62)],
#                [PointGrid(x=-3, y=-1), Mark(PointImg(x=162, y=62), 0, 143.13629868066312), Point(x=162, y=62)],
#                [PointGrid(x=-3, y=0), Mark(PointImg(x=212, y=62), 0, 138.52075656738234), Point(x=212, y=62)],
#                [PointGrid(x=-3, y=1), Mark(PointImg(x=262, y=62), 0, 151.28780519261954), Point(x=262, y=62)],
#                [PointGrid(x=-3, y=2), Mark(PointImg(x=312, y=62), 0, 177.73013250431114), Point(x=312, y=62)],
#                [PointGrid(x=-3, y=3), Mark(PointImg(x=362, y=62), 0, 212.8097742116184), Point(x=362, y=62)],
#                [PointGrid(x=-2, y=-4), Mark(PointImg(x=12, y=112), 0, 207.57649192526594), Point(x=12, y=112)],
#                [PointGrid(x=-2, y=-3), Mark(PointImg(x=62, y=112), 0, 163.67040050051813), Point(x=62, y=112)],
#                [PointGrid(x=-2, y=-2), Mark(PointImg(x=112, y=112), 0, 124.45079348883236), Point(x=112, y=112)],
#                [PointGrid(x=-2, y=-1), Mark(PointImg(x=162, y=112), 0, 95.85405573057407), Point(x=162, y=112)],
#                [PointGrid(x=-2, y=0), Mark(PointImg(x=212, y=112), 0, 88.81441324469807), Point(x=212, y=112)],
#                [PointGrid(x=-2, y=1), Mark(PointImg(x=262, y=112), 0, 107.64757312638311), Point(x=262, y=112)],
#                [PointGrid(x=-2, y=2), Mark(PointImg(x=312, y=112), 0, 142.43595051811886), Point(x=312, y=112)],
#                [PointGrid(x=-2, y=3), Mark(PointImg(x=362, y=112), 0, 184.35834670553976), Point(x=362, y=112)],
#                [PointGrid(x=-1, y=-4), Mark(PointImg(x=12, y=162), 0, 191.80198122021577), Point(x=12, y=162)],
#                [PointGrid(x=-1, y=-3), Mark(PointImg(x=62, y=162), 0, 143.13629868066312), Point(x=62, y=162)],
#                [PointGrid(x=-1, y=-2), Mark(PointImg(x=112, y=162), 0, 95.85405573057407), Point(x=112, y=162)],
#                [PointGrid(x=-1, y=-1), Mark(PointImg(x=162, y=162), 0, 53.74011537017761), Point(x=162, y=162)],
#                [PointGrid(x=-1, y=0), Mark(PointImg(x=212, y=162), 0, 39.84971769034255), Point(x=212, y=162)],
#                [PointGrid(x=-1, y=1), Mark(PointImg(x=262, y=162), 0, 72.71863585079137), Point(x=262, y=162)],
#                [PointGrid(x=-1, y=2), Mark(PointImg(x=312, y=162), 0, 118.27087553578015), Point(x=312, y=162)],
#                [PointGrid(x=-1, y=3), Mark(PointImg(x=362, y=161), 1, 166.6283289239858), Point(x=362, y=162)],
#                [PointGrid(x=0, y=-4), Mark(PointImg(x=12, y=212), 0, 188.38258942906586), Point(x=12, y=212)],
#                [PointGrid(x=0, y=-3), Mark(PointImg(x=62, y=212), 0, 138.52075656738234), Point(x=62, y=212)],
#                [PointGrid(x=0, y=-2), Mark(PointImg(x=112, y=212), 0, 88.81441324469807), Point(x=112, y=212)],
#                [PointGrid(x=0, y=-1), Mark(PointImg(x=162, y=212), 0, 39.84971769034255), Point(x=162, y=212)],
#                [PointGrid(x=0, y=0), Mark(PointImg(x=212, y=212), 0, 16.97056274847714), Point(x=212, y=212)],
#                [PointGrid(x=0, y=1), Mark(PointImg(x=262, y=212), 0, 63.150613615387776), Point(x=262, y=212)],
#                [PointGrid(x=0, y=2), Mark(PointImg(x=312, y=212), 0, 112.64102272262978), Point(x=312, y=212)],
#                [PointGrid(x=0, y=3), Mark(PointImg(x=362, y=212), 0, 162.4438364481706), Point(x=362, y=212)],
#                [PointGrid(x=1, y=-4), Mark(PointImg(x=12, y=262), 0, 197.9595918363139), Point(x=12, y=262)],
#                [PointGrid(x=1, y=-3), Mark(PointImg(x=62, y=262), 0, 151.28780519261954), Point(x=62, y=262)],
#                [PointGrid(x=1, y=-2), Mark(PointImg(x=112, y=262), 0, 107.64757312638311), Point(x=112, y=262)],
#                [PointGrid(x=1, y=-1), Mark(PointImg(x=162, y=262), 0, 72.71863585079137), Point(x=162, y=262)],
#                [PointGrid(x=1, y=0), Mark(PointImg(x=212, y=262), 0, 63.150613615387776), Point(x=212, y=262)],
#                [PointGrid(x=1, y=1), Mark(PointImg(x=262, y=262), 0, 87.68124086713189), Point(x=262, y=262)],
#                [PointGrid(x=1, y=2), Mark(PointImg(x=312, y=262), 0, 128.01562404644207), Point(x=312, y=262)],
#                [PointGrid(x=1, y=3), Mark(PointImg(x=362, y=262), 0, 173.4589288563722), Point(x=362, y=262)],
#                [PointGrid(x=2, y=-4), Mark(PointImg(x=12, y=312), 0, 218.8332698654389), Point(x=12, y=312)],
#                [PointGrid(x=2, y=-3), Mark(PointImg(x=62, y=312), 0, 177.73013250431114), Point(x=62, y=312)],
#                [PointGrid(x=2, y=-2), Mark(PointImg(x=112, y=312), 0, 142.43595051811886), Point(x=112, y=312)],
#                [PointGrid(x=2, y=-1), Mark(PointImg(x=162, y=312), 0, 118.27087553578015), Point(x=162, y=312)],
#                [PointGrid(x=2, y=0), Mark(PointImg(x=212, y=312), 0, 112.64102272262978), Point(x=212, y=312)],
#                [PointGrid(x=2, y=1), Mark(PointImg(x=262, y=312), 0, 128.01562404644207), Point(x=262, y=312)],
#                [PointGrid(x=2, y=2), Mark(PointImg(x=312, y=312), 0, 158.39191898578665), Point(x=312, y=312)],
#                [PointGrid(x=2, y=3), Mark(PointImg(x=362, y=312), 0, 196.9466932954194), Point(x=362, y=312)],
#                [PointGrid(x=3, y=-4), Mark(PointImg(x=12, y=361), 1, 247.51767613647314), Point(x=12, y=362)],
#                [PointGrid(x=3, y=-3), Mark(PointImg(x=62, y=362), 0, 212.8097742116184), Point(x=62, y=362)],
#                [PointGrid(x=3, y=-2), Mark(PointImg(x=112, y=361), 1, 183.48024416813925), Point(x=112, y=362)],
#                [PointGrid(x=3, y=-1), Mark(PointImg(x=162, y=362), 0, 166.39711535961192), Point(x=162, y=362)],
#                [PointGrid(x=3, y=0), Mark(PointImg(x=212, y=361), 1, 161.4465855941215), Point(x=212, y=362)],
#                [PointGrid(x=3, y=1), Mark(PointImg(x=262, y=362), 0, 173.4589288563722), Point(x=262, y=362)],
#                [PointGrid(x=3, y=2), Mark(PointImg(x=312, y=361), 1, 196.1249601657066), Point(x=312, y=362)],
#                [PointGrid(x=3, y=3), Mark(PointImg(x=362, y=361), 1, 228.39658491317246), Point(x=362, y=362)]
#
#            ] == result
