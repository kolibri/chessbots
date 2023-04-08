from flask import (Blueprint, jsonify)
from flask import Flask

from chessbots.lib.board import *
from dependency_injector.wiring import inject, Provide
from flaskr.containers import Container

bp = Blueprint('board', __name__, url_prefix='/board')
app = Flask(__name__)


@bp.route('/', methods=['GET'])
@inject
def get_board(board: Board = Provide[Container.game_board]):
    data = {
        'fen': board.game.fen,
        'playable': board.playable,
        'board': {
            'pieces': [p.to_json() for p in board.pieces],
            'rest_bots': [b.to_json() for b in board.rest_bots],
        },
        'bots': [b.to_json() for b in board.bot_repo.get()]
    }

    return jsonify(data), 200
