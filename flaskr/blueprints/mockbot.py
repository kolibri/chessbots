from flask import (Blueprint, jsonify, send_file, url_for, request)
from io import BytesIO
from flask import Flask

from chessbots.lib.mockbot import MockBots, MockbotPictureCreator
from dependency_injector.wiring import inject, Provide
from flaskr.containers import Container
from chessbots.lib.point_helper import Point

bp = Blueprint('mockbot', __name__, url_prefix='/mockbot')
app = Flask(__name__)


@bp.route('/', methods=['GET'])
@inject
def get_list(mockbots: MockBots = Provide[Container.mockbots]):
    data = [bot.mockbot_data() for bot in mockbots.bots]

    return jsonify(data)


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


@bp.route('/', methods=['POST'])
@inject
def post_add(mockbots: MockBots = Provide[Container.mockbots]):
    data = request.json
    bot = mockbots.add(data['name'], data['piece'], Point(*data['pos']), int(data['angle']))
    return jsonify(bot.data())


@bp.route('/<string:name>/position.jpeg', methods=['GET'])
@inject
def get_picture(
        name: str,
        mockbots: MockBots = Provide[Container.mockbots],
):
    if not mockbots.has(name):
        return jsonify('not found'), 404
    bot = mockbots.get(name)
    img = bot.img
    img_io = BytesIO()
    img.convert('RGB').save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
