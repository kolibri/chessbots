from flask import (Blueprint, render_template, jsonify, url_for, send_from_directory)

bp = Blueprint('tools', __name__, url_prefix='/tools')


@bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('tool/dashboard.html')


@bp.route('/mockbot/<string:name>', methods=['GET'])
def mockbot(name: str):
    ids = {'01': 'herzbube', '02': 'pikass', '03': 'kreuzvier', '04': 'karodame', '05': 'pikacht', '06': 'karozehn', '07': 'kreuzsieben', '08': 'herzzehn', '09': 'kreuzbube'}
    pieces = {'01': 'wk', '02': 'bq', '03': 'wb', '04': 'bk', '05': 'bs', '06': 'br', '07': 'ws', '08': 'wp', '09': 'bp'}
    return jsonify(
        {
            'url': url_for('tools.mockbot', name=name, _external=True),
            'name': ids.get(name),
            'state': 'online',
            'piece': pieces.get(name),
            'live_image': url_for('tools.mockbot_picture', name=name, _external=True),
            'motors': {
                'left': {
                    'pins': {
                        'pinA': '0',
                        'pinB': '0',
                        'pinPwm': '0'
                    }
                },
                'right': {
                    'pins': {
                        'pinA': '0',
                        'pinB': '0',
                        'pinPwm': '0'
                    }
                }
            }
        }
    )


@bp.route('/mockbot/<string:name>/position.jpeg', methods=['GET'])
def mockbot_picture(name: str):
    return send_from_directory('static/images', 'mockbot_' + name + '.jpeg')


@bp.route('/mockbot/<string:name>/', methods=['POST'])
def mockbot_move(name: str):
    return send_from_directory('static/images', 'mockbot_' + name + '.jpeg')


@bp.route('/test_board', methods=['GET'])
def view_test_board():
    return send_from_directory('static/images', 'test_board.png')

