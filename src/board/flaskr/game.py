import os
from flask import (Blueprint, request, Response, jsonify, url_for, send_from_directory)
from flask import Flask, current_app

from .BotData.BotManager import Bots
from .BotData.DataCollector.RobotSensorsCollector import RobotSensorsCollector
from .BotData.DataCollector.CaptchaDataCollector import CaptchaDataCollector
from .BotData.DataCollector.BoardPositionCollector import BoardPositionCollector
from .Utils.BoardUtils import *

bp = Blueprint('bots', __name__, url_prefix='/bots')
app = Flask(__name__)


def get_bots(app) -> Bots:
    cache_path = app.config['BOTCACHE_DIR']
    static_path = app.config['STATIC_DIR']
    board_size = app.config['BOARD_SIZE_IN_CAPTCHAS']
    return Bots(
        cache_path,
        [
            RobotSensorsCollector(cache_path),
            CaptchaDataCollector(cache_path, static_path),
            BoardPositionCollector(Board(txt_to_matrix(create_txt_board_4x4_bin(board_size))))
        ]
    )


'''
use query parameter for simple filtering
e.g.:
/bots/?state=online
/bots/?state=online&piece=wk
/bots/?id=herzbube
'''
@bp.route('/', methods=['GET'])
def get_index():
    bots = get_bots(current_app)
    return jsonify([bot.data for bot in bots.filter(request.args)]), 200

'''
use query parameter for simple filtering
e.g.:
/bots/?state=online
/bots/?state=online&piece=wk
/bots/?id=herzbube
'''
@bp.route('/', methods=['PATCH'])
def post_update():
    bots = get_bots(current_app)
    return jsonify([bot.data for bot in bots.update(request.args)]), 200


'''
json payload:
["http://0.0.0.0:8037","http://0.0.0.0:8031/tools/mockbot"]
'''
@bp.route('/register', methods=['POST'])
def post_register():
    bots = get_bots(current_app)
    return jsonify([bot.data for bot in bots.add(request.json)]), 205
