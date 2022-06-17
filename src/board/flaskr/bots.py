import os
from flask import (Blueprint, request, jsonify, url_for, send_from_directory)
from flask import Flask, current_app

from .BotData.BotManager import Bots
from .BotData.DataCollector.RobotSensorsCollector import RobotSensorsCollector
from .BotData.DataCollector.PositionDataCollector import PositionDataCollector

bp = Blueprint('bots', __name__, url_prefix='/bots')
app = Flask(__name__)


def get_bots(app) -> Bots:
    cache_path = app.config['BOTCACHE_DIR']
    static_path = app.config['STATIC_DIR']
    return Bots(
        cache_path,
        [
            RobotSensorsCollector(cache_path),
            PositionDataCollector(cache_path, static_path)
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
    return jsonify([bot.data for bot in bots.filter(request.args)])

'''
use query parameter for simple filtering
e.g.:
/bots/?state=online
/bots/?state=online&piece=wk
/bots/?id=herzbube
'''
@bp.route('/update', methods=['POST'])
def post_update():
    bots = get_bots(current_app)
    return jsonify([bot.data for bot in bots.update(request.args)])


'''
json payload:
["http://0.0.0.0:8037","http://0.0.0.0:8031/tools/mockbot"]
'''
@bp.route('/register', methods=['POST'])
def post_register():
    bots = get_bots(current_app)
    bots.add(request.json)
    return 'bot registered'


'''
more or less debug routes
'''
@bp.route('/cacheview/<string:name>/cam.png', methods=['GET'])
def cam_cache(name: str):
    return send_from_directory('static/bot_cache/', name + '_position.png')


@bp.route('/cacheview/<string:name>/matches.png', methods=['GET'])
def ocv_cache(name: str):
    return send_from_directory('static/bot_cache/', name + '_matches.png')
