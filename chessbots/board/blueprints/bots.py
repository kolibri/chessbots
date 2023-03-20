from flask import (Blueprint, request, render_template, jsonify)
from flask import Flask

from chessbots.lib.bot import Bot, BotManager
from chessbots.lib.bot.mockbot import MockBots
from dependency_injector.wiring import inject, Provide
from chessbots.board.containers import Container

bp = Blueprint('bots', __name__, url_prefix='/bots')
app = Flask(__name__)


@bp.route('/', methods=['GET'])
@inject
def get_index(bots: BotManager = Provide[Container.bot_manager]):
    """
    use query parameter for simple filtering
    e.g.:
    /bots/?state=online
    /bots/?state=online&piece=wk
    /bots/?id=herzbube
    """
    return jsonify([bot.data for bot in bots.filter(request.args)]), 200


@bp.route('/', methods=['PATCH'])
@inject
def post_update(bots: BotManager = Provide[Container.bot_manager]):
    """
    use query parameter for simple filtering
    e.g.:
    /bots/?state=online
    /bots/?state=online&piece=wk
    /bots/?id=herzbube
    """
    return jsonify([bot.data for bot in bots.update(request.args)]), 200


@bp.route('/register', methods=['POST'])
@inject
def post_register(bots: BotManager = Provide[Container.bot_manager]):
    """
    json payload:
    ["http://0.0.0.0:8037","http://0.0.0.0:8031/tools/mockbot"]
    """
    return jsonify([bot.data for bot in bots.add(request.json)]), 200


@bp.route('/dashboard', methods=['GET'])
@inject
def get_dashboard(mockbots: MockBots = Provide[Container.mockbots]):
    return render_template('dashboard.html', mockbots=[bot.url() for bot in mockbots.bots])

