import math
import time
import cv2
import numpy as np
import random
from matplotlib import pyplot as plt


import json
import os
import requests
from os import listdir
from os.path import isfile, join

from flask import (Blueprint, request, jsonify, url_for, send_from_directory)
from werkzeug.datastructures import MultiDict

from .board.bots.bot import Bot as BaseBot

bp = Blueprint('bots', __name__, url_prefix='/bots')


def get_path(file_name=None):
    if file_name is None:
        return os.path.join('flaskr', 'bot_cache')
    return os.path.join('flaskr', 'bot_cache', file_name)


def read_json(file_path: str):
    with open(file_path) as infile:
        return json.load(infile)


def draw_outline(img, point1, point2, color):
    cv2.rectangle(img, point1, point2, color, 1)


class BotManager:
    @staticmethod
    def get_all() -> list[BaseBot]:
        files = [f for f in listdir(get_path()) if isfile(join(get_path(), f))]
        bots = [BotManager.create_bot(f) for f in files if f.endswith('.json')]
        return bots

    @staticmethod
    def create_bot(file_name: str) -> BaseBot:
        data = read_json(get_path(file_name))
        return BaseBot(data.get('url'), data)

    @staticmethod
    def filter(values: "MultiDict[str, str]") -> list[BaseBot]:
        def compare(bot: BaseBot, asserts) -> bool:
            for k,v in asserts.items():
                if bot.data.get(k) != v:
                    return False
            return True

        return [bot for bot in BotManager.get_all() if (compare(bot, values))]

    @staticmethod
    def register(urls):
        bots = [collect(BaseBot(url, {})) for url in urls]
        return bots


def collect(bot: BaseBot) -> BaseBot:
    #print(bot)
    #bot = BaseBot(bot.host_name, bot.data)
    #return bot

    collectors = [RegisterDataCollector(), PositionDataCollector()]
    for collector in collectors:
        data = collector.get_data(bot)
        bot: BaseBot = BaseBot(bot.host_name, data)
        bot.save(get_path(None))
    return bot


class RegisterDataCollector:
    def get_data(self, bot: BaseBot):
        try:
            data = requests.get(bot.host_name).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            data = {'state': 'offline', 'url': bot.host_name}

        if 'live_image' in data:
            img_cache_path = get_path(bot.id + '_position.png')
            try:
                r = requests.get(data.get('live_image'))
                open(img_cache_path, 'wb').write(r.content)
                data['position_local_filename'] = img_cache_path
            except requests.exceptions.RequestException as e:
                print('failed to load image: ' + data['live_image'])

        return data


def find_matches(img, match_paths):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    matches = []
    for match_path in match_paths:
        template = cv2.imread(match_path, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            # print(pt)
            match = (pt, (pt[0] + w, pt[1] + h))
            matches.append(match)
    #print(matches)
    return matches


def find_rotated_matches(img, match_paths):
    rot_matches = []
    for rot in range(0, 360):
        matches = []
        img = rotate_img(img, rot)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for match_path in match_paths:
            template = cv2.imread(match_path, 0)

            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                # print(pt)
                match = (pt, (pt[0] + w, pt[1] + h))
                cv2.imwrite(get_path('position_ocv_' + str(rot) + '.png'), img)
                matches.append(match)

        rot_matches.append([rot, len(matches), matches])
        heighest = max((i[1] for i in rot_matches))
        # print(matches)
    return rot_matches


def rotate_img(img, deg):
    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, deg, 1.0)
    rotated = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return rotated


class PositionDataCollector:
    def get_data(self, bot: BaseBot):
        if bot.data['state'] != 'online':
            return bot.data
        data = bot.data
        #print(data)
        img = cv2.imread(data['position_local_filename'])

        rot = find_rotated_matches(img, ['flaskr/static/images/pattern_WR.png', 'flaskr/static/images/pattern_BR.png'])
        print(rot)
        wos = find_matches(img, ['flaskr/static/images/pattern_WO.png'])
        wxs = find_matches(img, ['flaskr/static/images/pattern_WX.png'])
        bos = find_matches(img, ['flaskr/static/images/pattern_BO.png'])
        bxs = find_matches(img, ['flaskr/static/images/pattern_BX.png'])

        # color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        matches = [(0, 0, int(m[0][0]), int(m[0][1])) for m in wos] + \
                  [(1, 0, int(m[0][0]), int(m[0][1])) for m in wxs] + \
                  [(0, 1, int(m[0][0]), int(m[0][1])) for m in bos] + \
                  [(1, 1, int(m[0][0]), int(m[0][1])) for m in bxs]

##        for match in rot:
#            draw_outline(img, (match[0][0], match[0][1]), (match[1][0], match[1][1]), (125, 125, 125))

        for match in matches:
            draw_outline(img, (match[2], match[3]), (match[2]+20, match[3]+20), (125, 125, 125))

        data['matches'] = matches
        data['rotation'] = PositionDataCollector.detect_rotation(matches)
        data['ocv_image'] = url_for('bots.ocv_cache', name=bot.id, _external=True)
        data['cache_image'] = url_for('bots.cam_cache', name=bot.id, _external=True)

        img_cache_path = get_path(bot.id + '_position_ocv.png')
        cv2.imwrite(img_cache_path, img)

        return data

    @staticmethod
    def detect_rotation(points):

        #point = points[0]
        point = points.pop(0)

        ds = [math.sqrt((point[2] - p[2])**2 + (point[3] - p[3])**2) for p in points]
        min_val = min(ds)
        min_ind = ds.index(min_val) + 1
        nearest_point = points[min_ind]

        y = abs(nearest_point[3] - point[3])
        x = abs(nearest_point[2] - point[2])
        theta = math.atan(y / x)
        theta = 180 * theta / math.pi

        #print('rota', theta, point, nearest_point, points)

        return theta


'''
# imported notes
def getPosition(imagePath):
    img = cv2.imread('images/' + imagePath)

    
    alignbars = findMatches(img, ['images/match_alignbars_white.png', 'images/match_alignbars_black.png'])
    zeros     = findMatches(img, ['images/match_zero_white.png',      'images/match_zero_black.png'])
    checks    = findMatches(img, ['images/match_check_white.png',     'images/match_check_black.png'])


    print(alignbars)

#    for bar in alignbars:
#        drawOutline(img, bar[0],bar[1],(240, 26, 2))
#
#    for bar in zeros:
#        drawOutline(img, bar[0],bar[1],(50, 62, 168))
#
#    for bar in checks:
#        drawOutline(img, bar[0],bar[1],(171, 201, 172))


    for alignbar in alignbars:
        barzeros = findMatchesByAlignbar(img, alignbar, zeros)
        barchecks = findMatchesByAlignbar(img, alignbar, checks)

        color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        for bar in barzeros:
            drawOutline(img, bar[0], bar[1], color)

        color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        for bar in barchecks:
            drawOutline(img, bar[0], bar[1], color)
        #print(len(barzeros) + len(barchecks))

    cv2.imwrite('out/' + imagePath, img)


def findMatchesByAlignbar(img, marker, matches):
    tolerance = 3
    field_size = img.shape[0] / 2
    markerOffset = [field_size / 4, field_size / 3] # <-- change here both to 4, when board_test.png updated..

    areaMin = [marker[0][0] - markerOffset[0], marker[0][1] - markerOffset[1]]
    areaMax = [areaMin[0] + field_size, areaMin[1] + field_size]

    filtered = []

    for match in matches:
        if(  
            match[0][0] > areaMin[0] - tolerance and
            match[0][1] > areaMin[1] - tolerance and
            match[1][0] < areaMax[0] + tolerance and
            match[1][1] < areaMax[1] + tolerance
        ):
          filtered.append(match)  
    return filtered


def findMatches(img, matchPaths):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    matches = []
    for matchPath in matchPaths:
        template = cv2.imread(matchPath,0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        
        for pt in zip(*loc[::-1]):
            #print(pt)
            match = (pt, (pt[0] + w, pt[1] + h))
            matches.append(match)

    return matches


def drawOutline(img, point1, point2, color):
    cv2.rectangle(img, point1, point2, color, 1)

    
getPosition('board_snippet_002.png')
'''






'''
use query parameter for simple filtering
e.g.:
/bots/?state=online
/bots/?state=online&piece=wk
/bots/?id=herzbube
'''
@bp.route('/', methods=['GET'])
def get_index():
    bots = BotManager.filter(request.args)
    return jsonify([bot.data for bot in bots])

'''
use query parameter for simple filtering
e.g.:
/bots/?state=online
/bots/?state=online&piece=wk
/bots/?id=herzbube
'''
@bp.route('/update', methods=['GET'])
def get_update():
    bots = BotManager.filter(request.args)
    return jsonify([bot.data for bot in bots])

'''
json payload:
["http://0.0.0.0:8037","http://0.0.0.0:8031/tools/mockbot"]
'''
@bp.route('/register', methods=['POST'])
def post_register():
    BotManager.register(request.json)
    return 'bot registered'


'''
more or less debug routes
'''
@bp.route('/cacheview/<string:name>/cam.png', methods=['GET'])
def cam_cache(name: str):
    return send_from_directory('bot_cache/', name + '_position.png')


@bp.route('/cacheview/<string:name>/ocv.png', methods=['GET'])
def ocv_cache(name: str):
    return send_from_directory('bot_cache/', name + '_position_ocv.png')
