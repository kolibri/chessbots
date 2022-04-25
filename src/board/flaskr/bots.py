import json
import os
import requests
from os import listdir
from os.path import isfile, join

from flask import (
    Blueprint, request, jsonify
)
from werkzeug.datastructures import MultiDict

from .board.bots.bot import Bot as BaseBot

bp = Blueprint('bots', __name__, url_prefix='/bots')


def get_path(file_name=None):
    if file_name is None:
        return os.path.join('flaskr', 'bot_cache')
    return os.path.join('flaskr', 'bot_cache', file_name)


def read_json(file_path):
    with open(file_path) as infile:
        return json.load(infile)


class BotManager:
    @staticmethod
    def get_all() -> list[BaseBot]:
        files = [f for f in listdir(get_path()) if isfile(join(get_path(), f))]
        bots = [BotManager.create_bot(f) for f in files if f.endswith('.json')]
        return bots

    @staticmethod
    def create_bot(file_name: str) -> BaseBot:
        data = read_json(get_path(file_name))
        return BaseBot(data.get('url'), data)

    @staticmethod
    def filter(values: "MultiDict[str, str]") -> list[BaseBot]:
        def compare(bot: BaseBot, asserts) -> bool:
            for k,v in asserts.items():
                print(k,v)
                if bot.data.get(k) != v:
                    return False
            return True

        return [bot for bot in BotManager.get_all() if (compare(bot, values))]

    @staticmethod
    def register(urls):
        bots = [BotManager.register_bot(url) for url in urls]
        return bots

    @staticmethod
    def register_bot(url: str) -> BaseBot:
        try:
            data = requests.get(url).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            data = {'state': 'offline', 'url': url}

        bot = BaseBot(data.get('url'), data)

        with open(get_path(bot.id + '.json'), 'w') as outfile:
            json.dump(bot.data, outfile)

        if 'position_image' in bot.data:
            try:
                r = requests.get(bot.data.get('position_image'))
                open(get_path(bot.id + '_position_image.png'), 'wb').write(r.content)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print('failed to load image: ' + bot.data.position_image)
        return bot

'''
use query parameter for simple filtering
e.g.:
/bots/?state=online
/bots/?state=online&piece=wk
/bots/?id=herzbube
'''
@bp.route('/', methods=['GET'])
def get_index():
    bots = BotManager.filter(request.args)
    return jsonify([bot.data for bot in bots])

'''
json payload:
["http://0.0.0.0:8037","http://0.0.0.0:8031/tools/mockbot"]
'''
@bp.route('/register', methods=['POST'])
def post_register():
    BotManager.register(request.json)
    return 'bot registered'

