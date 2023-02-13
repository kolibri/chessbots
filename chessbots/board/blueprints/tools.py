import cv2
import numpy as np
from flask import Blueprint
from chessbots.tool.pattern_creator import Pattern8x8With4DataFields
from chessbots.tool.printer import *
from chessbots.tool.mockbot import *
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
    creator.create('03', pattern_creator.create(800), Point(42, 13), Point(16, 16), 90)
    creator.create('03', pattern_creator.create(800), Point(322, 384), Point(16, 16), 180)
    creator.create('04', pattern_creator.create(800), Point(123, 123), Point(16, 16), 123)
    creator.create('05', pattern_creator.create(800), Point(123, 456), Point(16, 16), 78)
    creator.create('06', pattern_creator.create(800), Point(423, 225), Point(16, 16), 38)
    creator.create('07', pattern_creator.create(800), Point(253, 613), Point(16, 16), 276)
    creator.create('08', pattern_creator.create(800), Point(253, 273), Point(16, 16), 48)
    creator.create('09', pattern_creator.create(800), Point(587, 243), Point(16, 16), 271)


@bp.cli.command('circle_finder_tuner')
@inject
def circle_finder_tuner():
    def find_markers(img, first, p1, p2, min, max, dist):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # threshold
        ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # findcontours
        # cnts = cv2.findContours(threshed, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        mids = []
        for i in contours:
            M = cv2.moments(i)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                mids.append(Point(cx, cy))

        return mids


    def _mark_positions(img, pos: [[int, int, int]]):
        color = (255, 0, 255)
        output = img.copy()
        for p in pos:
            # print(p)
            cv2.rectangle(output, list(sub_points(p, Point(10, 10))), list(add_points(p, Point(10, 10))), (0, 128, 255), -1)

        return output

    picture = 'build/mockbot/mockbot_01.jpg'


    pic = cv2.imread(picture)
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    cv2.imwrite('build/mockbot/blur.jpg', gray_blurred)

    sets = [
        [1, 50, 10, 30, 45, 15],
    ]

    for set in sets:
        img = cv2.imread(picture)
        markers = find_markers(img, *set)
        print('markers', markers[0])
        # image_copy = img.copy()
        # cv2.drawContours(image=image_copy, contours=markers, contourIdx=-1, color=(0, 255, 0), thickness=2,
        #                  lineType=cv2.LINE_AA)

        marked_img = _mark_positions(img, markers)
        cv2.imwrite(picture + str(set) + '.jpg', marked_img)
