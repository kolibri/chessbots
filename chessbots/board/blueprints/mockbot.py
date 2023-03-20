from flask import (Blueprint, jsonify, send_from_directory)
from chessbots.lib.bot.mockbot import *

from flask import Flask

from chessbots.lib.bot.mockbot import MockBots
from dependency_injector.wiring import inject, Provide
from chessbots.board.containers import Container


bp = Blueprint('mockbot', __name__, url_prefix='/mockbot')
app = Flask(__name__)


@bp.route('/<string:name>', methods=['GET'])
@inject
def get_show(name: str, mockbots: MockBots = Provide[Container.mockbots]):
    if not mockbots.has(name):
        return jsonify({
            'url': url_for('mockbot.get_show', name=name, _external=True),
            'state': 'offline',
        })
    bot = mockbots.get(name)
    return jsonify(bot.data())


@bp.route('/<string:name>/position.jpeg', methods=['GET'])
@inject
def get_picture(name: str, mockbots: MockBots = Provide[Container.mockbots]):
    if not mockbots.has(name):
        return jsonify('not found'), 404
    bot = mockbots.get(name)
    return send_from_directory('/app/build/mockbot', bot.picture())
