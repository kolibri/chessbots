import io

from flask import (
    Blueprint, render_template, jsonify, url_for, send_from_directory, send_file
)
from .board.print import Print


bp = Blueprint('tools', __name__, url_prefix='/tools')


@bp.route('/board_print', methods=['GET'])
def board_print():
    print = Print()
    img = print.render()
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

#    return send_from_directory('static', 'board_print.html')


@bp.route('/mockbot/<string:name>', methods=['GET'])
def mockbot(name: str):
    ids = {'01': 'herzbube', '02': 'pikass', '03': 'kreuzvier', '04': 'karodame'}
    pieces = {'01': 'wk', '02': 'bp', '03': 'wb', '04': 'bk'}
    return jsonify(
        {
            'url': url_for('tools.mockbot', name=name, _external=True),
            'id': ids.get(name),
            'state': 'online',
            'piece': pieces.get(name),
            'position_image': url_for('tools.mockbot_picture', name=name, _external=True),
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


@bp.route('/mockbot/<string:name>_position_image.png', methods=['GET'])
def mockbot_picture(name: str):
    pass
    return send_from_directory('static/mockbot', 'pi' + name + '.png')


@bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('tool/dashboard.html')

