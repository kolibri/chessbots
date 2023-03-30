from flask import (Blueprint, request, render_template, jsonify)
from flask import Flask

from chessbots.lib.bot import *
from chessbots.lib.bot.mockbot import MockBots
from dependency_injector.wiring import inject, Provide
from flaskr.containers import Container

bp = Blueprint('bots', __name__, url_prefix='/bots')
app = Flask(__name__)


@bp.route('/', methods=['GET'])
@inject
def get_index(bots: BotRepository = Provide[Container.bot_repository]):
    """
    use query parameter for simple filtering
    e.g.:
    /bots/?state=online
    /bots/?state=online&piece=wk
    /bots/?id=herzbube
    """
    return jsonify([bot.to_json() for bot in bots.get(request.args.items())]), 200


@bp.route('/', methods=['PATCH'])
@inject
def post_update(bots: BotRepository = Provide[Container.bot_repository]):
    """
    use query parameter for simple filtering
    e.g.:
    /bots/?state=online
    /bots/?state=online&piece=wk
    /bots/?id=herzbube
    """
    return jsonify([bot.to_json() for bot in bots.update(request.args.items())]), 200


@bp.route('/register', methods=['POST'])
@inject
def post_register(bots: BotRepository = Provide[Container.bot_repository]):
    """
    json payload:
    ["http://0.0.0.0:8037","http://0.0.0.0:8031/tools/mockbot"]
    """
    return jsonify([bot.to_json() for bot in bots.add_bots(request.json)]), 200


@bp.route('/dashboard', methods=['GET'])
@inject
def get_dashboard(mockbots: MockBots = Provide[Container.mockbots]):
    return render_template('dashboard.html.j2', mockbots=[bot.url() for bot in mockbots.bots])

