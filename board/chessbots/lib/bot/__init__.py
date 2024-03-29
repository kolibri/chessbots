from flask import (url_for)
from chessbots.lib.captcha import Captcha
import requests
from collections import namedtuple
import os
from chessbots.lib.filesystem import *
from chessbots.lib.point_helper import Point
from typing import NamedTuple
from chessbots.lib.pattern import Pattern


class BotHttpData:
    def __init__(self, name, piece, pos_pic_url, pos_pic_path, pos_pic_cache_url):
        self.name = name
        self.piece = piece
        self.pos_pic_url = pos_pic_url
        self.pos_pic_path = pos_pic_path
        self.pos_pic_cache_url = pos_pic_cache_url

    def to_json(self):
        return {
            'name': self.name,
            'piece': self.piece,
            'pos_pic_url': self.pos_pic_url,
            'pos_pic_path': self.pos_pic_path,
            'pos_pic_cache_url': self.pos_pic_cache_url,
        }

    @staticmethod
    def from_json(data):
        return BotHttpData(data['name'], data['piece'], data['pos_pic_url'], data['pos_pic_path'], data['pos_pic_cache_url'])


class CaptchaData:
    def __init__(self, pos: Point, rotation):
        self.pos = pos
        self.rotation = rotation

    def to_json(self):
        return {
            'pos': self.pos.raw,
            'rotation': self.rotation,
        }

    @staticmethod
    def from_json(data):
        return CaptchaData(Point(*data['pos']), data['rotation'])


class DebugData:
    def __init__(self, imgs: [str, str]):
        self.imgs = imgs

    def to_json(self):
        return {
            'imgs': self.imgs
        }

    @staticmethod
    def from_json(data):
        return DebugData(data['imgs'])



Filter = namedtuple('Filter', 'key value')


class Bot:
    http_data: BotHttpData = None
    captcha_data: CaptchaData = None
    debug: DebugData = None

    def __init__(self, url: str):
        self.url = url

    def to_json(self):
        return {
            'url': self.url,
            'slug': self.slug(),
            'http_data': self.http_data.to_json() if self.http_data else {},
            'captcha_data': self.captcha_data.to_json() if self.captcha_data else {},
            'debug': self.debug.to_json() if self.debug else {}
        }

    def slug(self) -> str:
        return self.url \
            .replace('https', '') \
            .replace('http', '') \
            .replace('://', '') \
            .replace(':', '_') \
            .replace('/', '_')  # todo: to regex

    def filter(self, filters: [Filter]) -> bool:
        for key, value in filters:
            match key:
                case 'url':
                    if self.url != value:
                        return False
                case 'slug':
                    if self.slug() != value:
                        return False
                case 'name':
                    if self.http_data.name != value:
                        return False
                case 'piece':
                    if self.http_data.piece != value:
                        return False
        return True


class BotManager:
    URL_FILE = 'url.txt'
    HTTP_FILE = 'http.json'
    CAPTCHA_FILE = 'captcha.json'
    DEBUG_FILE = 'debug.json'
    POSPIC_FILE = 'position.jpeg'
    CACHE_FILES = [
        URL_FILE,
        HTTP_FILE,
        CAPTCHA_FILE,
        DEBUG_FILE,
    ]

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.bots = []

    def create(self, url: str) -> Bot:
        bot = self.update(Bot(url))
        self.__ensure_bot_dir(bot)
        return bot

    def load_from_cache(self, path: str) -> Bot:
        base = self.data_dir

        url_path = os.path.join(base, path, self.URL_FILE)
        http_data_path = os.path.join(base, path, self.HTTP_FILE)
        captcha_data_path = os.path.join(base, path, self.CAPTCHA_FILE)
        debug_data_path = os.path.join(base, path, self.DEBUG_FILE)

        bot = Bot(read_txt(url_path))
        if os.path.isfile(http_data_path):
            bot.http_data = BotHttpData.from_json(read_json(http_data_path))
        if os.path.isfile(captcha_data_path):
            bot.captcha_data = CaptchaData.from_json(read_json(captcha_data_path))
        if os.path.isfile(debug_data_path):
            bot.debug = DebugData.from_json(read_json(debug_data_path))
            print('dbg loaded', bot.debug.imgs)
        return bot

    def update(self, bot: Bot) -> Bot:
        try:
            bot_dir = self.__get_bot_dir(bot)
            self.__ensure_bot_dir(bot)

            try:
                data = requests.get(bot.url).json()
            except requests.exceptions.RequestException as e:
                return bot

            http_pic_path = os.path.join(bot_dir, self.POSPIC_FILE)
            try:
                r = requests.get(data.get('pos_pic'))
                dump_binary(http_pic_path, r.content)
            except requests.exceptions.RequestException as e:
                print('cannot retrieve image for bot:', bot.url, 'response:', data)

            bot.http_data = BotHttpData(
                data.get('name'),
                data.get('piece'),
                data.get('pos_pic'),
                http_pic_path,
                url_for('bots.get_cache_image', bot_name=bot.slug(), img_type='raw', _external=True)
            )

            if os.path.isfile(http_pic_path):
                captcha = Captcha(http_pic_path)
                captcha.draw_debug_images()
                bot.captcha_data = CaptchaData(captcha.position, captcha.rotation)

                debug_imgs = [[f, url_for('bots.get_cache_image', bot_name=bot.slug(), img_type=f, _external=True)] for f in captcha.draw_debug_images()]

                bot.debug = DebugData(debug_imgs)
        except Exception as e:
            print(e)

        self.__save(bot)
        return bot

    def load_bots_from_cache(self) -> [Bot]:
        def check_path(f: str):
            base = self.data_dir
            return os.path.isdir(os.path.join(base, f)) \
                and f.startswith('bot_') \
                and os.path.isfile(os.path.join(base, f, 'url.txt'))

        bot_dirs = [f for f in os.listdir(self.data_dir) if check_path(f)]
        return [self.load_from_cache(p) for p in bot_dirs]

    def __save(self, bot: Bot):
        bot_dir = self.__get_bot_dir(bot)
        self.__ensure_bot_dir(bot)
        cfs = [os.path.join(bot_dir, f) for f in self.CACHE_FILES]
        try:
            [os.remove(f) for f in cfs if os.path.isfile(f)]
        except Exception as e:
            print('could not delete cache file', e)
        dump_txt(os.path.join(bot_dir, self.URL_FILE), bot.url)
        if bot.http_data:
            dump_json(os.path.join(bot_dir, self.HTTP_FILE), bot.http_data.to_json())
        if bot.captcha_data:
            dump_json(os.path.join(bot_dir, self.CAPTCHA_FILE), bot.captcha_data.to_json())
        if bot.debug:
            print('ASDTFGSFTGNGNB')
            dump_json(os.path.join(bot_dir, self.DEBUG_FILE), bot.debug.to_json())

    def __ensure_bot_dir(self, bot: Bot):
        bot_dir = self.__get_bot_dir(bot)
        if os.path.isdir(bot_dir):
            return
        else:
            if os.path.exists(bot_dir):
                os.remove(bot_dir)
        os.mkdir(self.__get_bot_dir(bot))

    def __get_bot_dir(self, bot: Bot) -> str:
        return os.path.join(self.data_dir, 'bot_' + bot.slug())


class BotRepository:
    def __init__(self, bot_manager: BotManager):
        self.bot_manager = bot_manager
        self.bots = self.bot_manager.load_bots_from_cache()

    def get(self, filter: [Filter] = None) -> [Bot]:
        return self.__filtered(filter)

    def update(self, filter: [Filter] = None) -> [Bot]:
        return [self.bot_manager.update(bot) for bot in self.__filtered(filter)]

    def add_bots(self, urls: [str]) -> [Bot]:
        for u in urls:
            self.bots.append(self.bot_manager.create(u))
        return self.bots

    def __filtered(self, filters: [Filter] = None) -> [Bot]:
        if not filters:
            return self.bots
        filters = list(filters)
        if filters and 0 < len(filters):
            return [bot for bot in self.bots if bot.filter(filters)]
        return self.bots
