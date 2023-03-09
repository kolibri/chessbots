from flask import (Blueprint, jsonify, url_for, send_from_directory)
from flask import Flask
from chessbots.lib.bot.mockbot import *

bp = Blueprint('mockbot', __name__, url_prefix='/mockbot')
app = Flask(__name__)


@bp.route('/<string:name>', methods=['GET'])
def get_show(name: str):
    if not MockBots().has(name):
        return jsonify({
            'url': url_for('mockbot.get_show', name=name, _external=True),
            'state': 'offline',
        })
    bot = MockBots().get(name)
    return jsonify(bot.data())


@bp.route('/<string:name>/position.jpeg', methods=['GET'])
def get_picture(name: str):
    bot = MockBots().get(name)
    return send_from_directory('/app/build/mockbot', bot.picture())
