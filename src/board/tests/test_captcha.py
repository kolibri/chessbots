import cv2
from ..flaskr import create_app
from ..flaskr.BotData.Captcha import *
from ..flaskr.BotData.Board import *


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


def test_marker_finder_can_filter_doubles():
    mf = MarkerFinder([
        ['flaskr/static/images/pattern/pattern_WO.jpeg', 0],
        ['flaskr/static/images/pattern/pattern_WX.jpeg', 1],
        ['flaskr/static/images/pattern/pattern_BO.jpeg', 0],
        ['flaskr/static/images/pattern/pattern_BX.jpeg', 1]
    ])

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


def test_marker_finder_can_find_marks():
    mf2 = MarkerFinder([
        ['flaskr/static/images/pattern/pattern_WO.jpeg', 0],
        ['flaskr/static/images/pattern/pattern_WX.jpeg', 1],
        ['flaskr/static/images/pattern/pattern_BO.jpeg', 0],
        ['flaskr/static/images/pattern/pattern_BX.jpeg', 1]
    ])
    # @todo: this list is not quite filtered, as it looks o_O
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

           ] == mf2.find_markers(cv2.imread('flaskr/static/images/mockbot/mockbot_01.jpeg'))


def test_grid_resolver_resolves_to_grid():
    mf = MarkerFinder([
        ['flaskr/static/images/pattern/pattern_WO.jpeg', 0],
        ['flaskr/static/images/pattern/pattern_WX.jpeg', 1],
        ['flaskr/static/images/pattern/pattern_BO.jpeg', 0],
        ['flaskr/static/images/pattern/pattern_BX.jpeg', 1]
    ])
    gr = GridResolver()
    img_path = 'flaskr/static/images/mockbot/mockbot_01.jpeg'
    img = cv2.imread(img_path)

    markers = mf.find_markers(img)
    result = gr.resolve_grid(markers, PointImg(img.shape[0], img.shape[1]))

    assert [
               [PointGrid(x=-4, y=-4), [PointImg(x=12, y=12), 0, 265.87214972614186], Point(x=12, y=12)],
               [PointGrid(x=-4, y=-3), [PointImg(x=62, y=12), 0, 233.21234958723778], Point(x=62, y=12)],
               [PointGrid(x=-4, y=-2), [PointImg(x=112, y=12), 0, 207.57649192526594], Point(x=112, y=12)],
               [PointGrid(x=-4, y=-1), [PointImg(x=162, y=12), 0, 191.80198122021577], Point(x=162, y=12)],
               [PointGrid(x=-4, y=0), [PointImg(x=212, y=12), 0, 188.38258942906586], Point(x=212, y=12)],
               [PointGrid(x=-4, y=1), [PointImg(x=262, y=12), 0, 197.9595918363139], Point(x=262, y=12)],
               [PointGrid(x=-4, y=2), [PointImg(x=312, y=12), 0, 218.8332698654389], Point(x=312, y=12)],
               [PointGrid(x=-4, y=3), [PointImg(x=362, y=12), 0, 248.16929705344293], Point(x=362, y=12)],
               [PointGrid(x=-3, y=-4), [PointImg(x=12, y=62), 0, 233.21234958723778], Point(x=12, y=62)],
               [PointGrid(x=-3, y=-3), [PointImg(x=62, y=62), 0, 195.16147160748713], Point(x=62, y=62)],
               [PointGrid(x=-3, y=-2), [PointImg(x=112, y=62), 0, 163.67040050051813], Point(x=112, y=62)],
               [PointGrid(x=-3, y=-1), [PointImg(x=162, y=62), 0, 143.13629868066312], Point(x=162, y=62)],
               [PointGrid(x=-3, y=0), [PointImg(x=212, y=62), 0, 138.52075656738234], Point(x=212, y=62)],
               [PointGrid(x=-3, y=1), [PointImg(x=262, y=62), 0, 151.28780519261954], Point(x=262, y=62)],
               [PointGrid(x=-3, y=2), [PointImg(x=312, y=62), 0, 177.73013250431114], Point(x=312, y=62)],
               [PointGrid(x=-3, y=3), [PointImg(x=362, y=62), 0, 212.8097742116184], Point(x=362, y=62)],
               [PointGrid(x=-2, y=-4), [PointImg(x=12, y=112), 0, 207.57649192526594], Point(x=12, y=112)],
               [PointGrid(x=-2, y=-3), [PointImg(x=62, y=112), 0, 163.67040050051813], Point(x=62, y=112)],
               [PointGrid(x=-2, y=-2), [PointImg(x=112, y=112), 0, 124.45079348883236], Point(x=112, y=112)],
               [PointGrid(x=-2, y=-1), [PointImg(x=162, y=112), 0, 95.85405573057407], Point(x=162, y=112)],
               [PointGrid(x=-2, y=0), [PointImg(x=212, y=112), 0, 88.81441324469807], Point(x=212, y=112)],
               [PointGrid(x=-2, y=1), [PointImg(x=262, y=112), 0, 107.64757312638311], Point(x=262, y=112)],
               [PointGrid(x=-2, y=2), [PointImg(x=312, y=112), 0, 142.43595051811886], Point(x=312, y=112)],
               [PointGrid(x=-2, y=3), [PointImg(x=362, y=112), 0, 184.35834670553976], Point(x=362, y=112)],
               [PointGrid(x=-1, y=-4), [PointImg(x=12, y=162), 0, 191.80198122021577], Point(x=12, y=162)],
               [PointGrid(x=-1, y=-3), [PointImg(x=62, y=162), 0, 143.13629868066312], Point(x=62, y=162)],
               [PointGrid(x=-1, y=-2), [PointImg(x=112, y=162), 0, 95.85405573057407], Point(x=112, y=162)],
               [PointGrid(x=-1, y=-1), [PointImg(x=162, y=162), 0, 53.74011537017761], Point(x=162, y=162)],
               [PointGrid(x=-1, y=0), [PointImg(x=212, y=162), 0, 39.84971769034255], Point(x=212, y=162)],
               [PointGrid(x=-1, y=1), [PointImg(x=262, y=162), 0, 72.71863585079137], Point(x=262, y=162)],
               [PointGrid(x=-1, y=2), [PointImg(x=312, y=162), 0, 118.27087553578015], Point(x=312, y=162)],
               [PointGrid(x=-1, y=3), [PointImg(x=362, y=161), 1, 166.6283289239858], Point(x=362, y=162)],
               [PointGrid(x=0, y=-4), [PointImg(x=12, y=212), 0, 188.38258942906586], Point(x=12, y=212)],
               [PointGrid(x=0, y=-3), [PointImg(x=62, y=212), 0, 138.52075656738234], Point(x=62, y=212)],
               [PointGrid(x=0, y=-2), [PointImg(x=112, y=212), 0, 88.81441324469807], Point(x=112, y=212)],
               [PointGrid(x=0, y=-1), [PointImg(x=162, y=212), 0, 39.84971769034255], Point(x=162, y=212)],
               [PointGrid(x=0, y=0), [PointImg(x=212, y=212), 0, 16.97056274847714], Point(x=212, y=212)],
               [PointGrid(x=0, y=1), [PointImg(x=262, y=212), 0, 63.150613615387776], Point(x=262, y=212)],
               [PointGrid(x=0, y=2), [PointImg(x=312, y=212), 0, 112.64102272262978], Point(x=312, y=212)],
               [PointGrid(x=0, y=3), [PointImg(x=362, y=212), 0, 162.4438364481706], Point(x=362, y=212)],
               [PointGrid(x=1, y=-4), [PointImg(x=12, y=262), 0, 197.9595918363139], Point(x=12, y=262)],
               [PointGrid(x=1, y=-3), [PointImg(x=62, y=262), 0, 151.28780519261954], Point(x=62, y=262)],
               [PointGrid(x=1, y=-2), [PointImg(x=112, y=262), 0, 107.64757312638311], Point(x=112, y=262)],
               [PointGrid(x=1, y=-1), [PointImg(x=162, y=262), 0, 72.71863585079137], Point(x=162, y=262)],
               [PointGrid(x=1, y=0), [PointImg(x=212, y=262), 0, 63.150613615387776], Point(x=212, y=262)],
               [PointGrid(x=1, y=1), [PointImg(x=262, y=262), 0, 87.68124086713189], Point(x=262, y=262)],
               [PointGrid(x=1, y=2), [PointImg(x=312, y=262), 0, 128.01562404644207], Point(x=312, y=262)],
               [PointGrid(x=1, y=3), [PointImg(x=362, y=262), 0, 173.4589288563722], Point(x=362, y=262)],
               [PointGrid(x=2, y=-4), [PointImg(x=12, y=312), 0, 218.8332698654389], Point(x=12, y=312)],
               [PointGrid(x=2, y=-3), [PointImg(x=62, y=312), 0, 177.73013250431114], Point(x=62, y=312)],
               [PointGrid(x=2, y=-2), [PointImg(x=112, y=312), 0, 142.43595051811886], Point(x=112, y=312)],
               [PointGrid(x=2, y=-1), [PointImg(x=162, y=312), 0, 118.27087553578015], Point(x=162, y=312)],
               [PointGrid(x=2, y=0), [PointImg(x=212, y=312), 0, 112.64102272262978], Point(x=212, y=312)],
               [PointGrid(x=2, y=1), [PointImg(x=262, y=312), 0, 128.01562404644207], Point(x=262, y=312)],
               [PointGrid(x=2, y=2), [PointImg(x=312, y=312), 0, 158.39191898578665], Point(x=312, y=312)],
               [PointGrid(x=2, y=3), [PointImg(x=362, y=312), 0, 196.9466932954194], Point(x=362, y=312)],
               [PointGrid(x=3, y=-4), [PointImg(x=12, y=361), 1, 247.51767613647314], Point(x=12, y=362)],
               [PointGrid(x=3, y=-3), [PointImg(x=62, y=362), 0, 212.8097742116184], Point(x=62, y=362)],
               [PointGrid(x=3, y=-2), [PointImg(x=112, y=361), 1, 183.48024416813925], Point(x=112, y=362)],
               [PointGrid(x=3, y=-1), [PointImg(x=162, y=362), 0, 166.39711535961192], Point(x=162, y=362)],
               [PointGrid(x=3, y=0), [PointImg(x=212, y=361), 1, 161.4465855941215], Point(x=212, y=362)],
               [PointGrid(x=3, y=1), [PointImg(x=262, y=362), 0, 173.4589288563722], Point(x=262, y=362)],
               [PointGrid(x=3, y=2), [PointImg(x=312, y=361), 1, 196.1249601657066], Point(x=312, y=362)],
               [PointGrid(x=3, y=3), [PointImg(x=362, y=361), 1, 228.39658491317246], Point(x=362, y=362)]

           ] == result


def test_grid_resolver_to_text():
    mf = MarkerFinder([
        ['flaskr/static/images/pattern/pattern_WO.jpeg', 0],
        ['flaskr/static/images/pattern/pattern_WX.jpeg', 1],
        ['flaskr/static/images/pattern/pattern_BO.jpeg', 0],
        ['flaskr/static/images/pattern/pattern_BX.jpeg', 1]
    ])
    gr = GridResolver()
    img_path = 'flaskr/static/images/mockbot/mockbot_01.jpeg'
    img = cv2.imread(img_path)

    markers = mf.find_markers(img)
    result = gr.grid_to_txt(gr.resolve_grid(markers, PointImg(img.shape[0], img.shape[1])))

    assert '00000000\n00000000\n00000000\n00000001\n00000000\n00000000\n00000000\n10101011\n' == result


def test_captcha():
    def assert_snippet_is_board(snippet_path: str, board_txt: str, rotation: float):
        templates = [
            ['flaskr/static/images/pattern/pattern_WO.jpeg', 0],
            ['flaskr/static/images/pattern/pattern_WX.jpeg', 1],
            ['flaskr/static/images/pattern/pattern_BO.jpeg', 0],
            ['flaskr/static/images/pattern/pattern_BX.jpeg', 1]
        ]
        tol = 2
        captcha = Captcha(snippet_path, templates)
        expected_board = Board(txt_to_matrix(board_txt))
        angle = captcha.get_captcha_angel()
        board = captcha.get_board()

        assert rotation - tol < angle < rotation + tol
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
            ]), 90  # @todo: should be 90
        ],
    ]
    for t in tests:
        assert_snippet_is_board(t[0], t[1], t[2])
