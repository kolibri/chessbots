import os

from flask import (Blueprint, request, jsonify, send_file, send_from_directory)
from flask import Flask

from chessbots.lib.board import *
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


@bp.route('/pic/<string:name>', methods=['GET'])
@inject
def get_cache_image(name: str):
    pathname = os.path.join('/app/build/bots', 'bot_' + name, 'position.jpeg') # @todo: absolute path, move to config
    print(pathname)
    if os.path.isfile(pathname):
        return send_file(pathname)

    return 'not found', 404

@bp.route('/register', methods=['POST'])
@inject
def post_register(bots: BotRepository = Provide[Container.bot_repository]):
    """
    json payload:
    ["http://0.0.0.0:8037","http://0.0.0.0:8031/tools/mockbot"]
    """
    return jsonify([bot.to_json() for bot in bots.add_bots(request.json)]), 200
