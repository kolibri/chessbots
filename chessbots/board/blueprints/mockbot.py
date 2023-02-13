from flask import (Blueprint, jsonify, url_for, send_from_directory)
from flask import Flask

bp = Blueprint('mockbot', __name__, url_prefix='/mockbot')
app = Flask(__name__)


@bp.route('/<string:name>', methods=['GET'])
def get_show(name: str):
    ids = {'01': 'herzbube', '02': 'pikass', '03': 'kreuzvier', '04': 'karodame', '05': 'pikacht',
           '06': 'karozehn', '07': 'kreuzsieben', '08': 'herzzehn', '09': 'kreuzbube'}
    pieces = {'01': 'wk', '02': 'bq', '03': 'wb', '04': 'bk', '05': 'bs',
              '06': 'br', '07': 'ws', '08': 'wp', '09': 'bp'}
    return jsonify(
        {
            'url': url_for('mockbot.get_show', name=name, _external=True),
            'name': ids.get(name),
            'state': 'online',
            'piece': pieces.get(name),
            'live_image': url_for('mockbot.get_picture', name=name, _external=True),
        }
    )


@bp.route('/<string:name>/position.jpeg', methods=['GET'])
def get_picture(name: str):
    return send_from_directory('/app/build/mockbot', 'mockbot_' + name + '.jpg')
