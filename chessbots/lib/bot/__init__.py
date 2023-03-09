from __future__ import annotations
import requests
from werkzeug.datastructures import MultiDict
import os
import hashlib
from chessbots.lib.filesystem import read_json, dump_json
from chessbots.lib.captcha.captcha_reader import CaptchaReader


class Bot:
    def __init__(self, host_name, data=None):
        self.host_name = host_name
        self.id = hashlib.sha256(self.host_name.encode('utf-8')).hexdigest()[0:8]
        if data is None:
            self.data = {}
        else:
            self.data = data
        self.data['id'] = self.id
        self.data['url'] = self.host_name

    @staticmethod
    def from_file(filename) -> Bot:
        data = read_json(filename)
        return Bot(data.get('url'), data)

    def update(self, data) -> Bot:
        return Bot(self.host_name, self.data | data)

    def save(self, path) -> Bot:
        dump_json((path + '/' + self.id + '.json'), self.data)
        return self


class BotManager:
    def __init__(self, cache_dir: str, collector: BotDataCollector):
        self.cache_dir = cache_dir
        self.collectors = collector
        self.bots = self.__load(self.cache_dir)
        print('bots', self.bots)

    def add(self, urls: [str]) -> [Bot]:
        bots = [Bot(url, {}) for url in urls]
        # self.bots = self.bots + bots
        for bot in bots:
            bot.save(self.cache_dir)
        return bots

    def save(self, filters: "MultiDict[str, str]") -> [Bot]:
        [bot.save(self.cache_dir) for bot in self.filter(filters)]

    def update(self, filters: "MultiDict[str, str]") -> [Bot]:
        self.bots = [bot.update(self.collectors.get_data(bot)) for bot in self.filter(filters)]
        self.save(filters)
        return self.bots

    def filter(self, filters: "MultiDict[str, str]") -> [Bot]:
        def compare(bot: Bot, asserts) -> bool:
            for k, v in asserts.items():
                if bot.data.get(k) != v:
                    return False
            return True

        if 0 == len(filters):
            return self.bots
        return [bot for bot in self.bots if (compare(bot, filters))]

    @staticmethod
    def __load(base_dir: str) -> [Bot]:
        files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f)) and f.endswith('.json')]
        return [Bot.from_file(os.path.join(base_dir, f)) for f in files]


class BotDataCollector:
    def get_data(self, bot: Bot) -> Bot:
        pass


class ChainDataCollector(BotDataCollector):
    def __init__(self, collectors: [BotDataCollector]):
        self.collectors = collectors

    def get_data(self, bot: Bot):
        data = bot.data
        for collector in self.collectors:
            data = data | collector.get_data(bot)
        return data


class RobotApiCollector(BotDataCollector):
    def __init__(self, cache_path: str):
        self.cache_path = cache_path

    def get_data(self, bot: Bot):
        try:
            data = requests.get(bot.host_name).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            data = {'state': 'offline', 'url': bot.host_name}
            print('robot sensor: failed to load bot info', data, e)

        if 'live_image' in data:
            img_cache_path = os.path.join(self.cache_path, bot.id + '_position.jpeg')
            try:
                r = requests.get(data.get('live_image'))
                open(img_cache_path, 'wb').write(r.content)
                data['position_local_filename'] = img_cache_path
            except requests.exceptions.RequestException as e:
                print('robot sensor: failed to load image: ', data['live_image'])
        return data


class CaptchaReaderCollector(BotDataCollector):
    def __init__(self, captcha_reader: CaptchaReader):
        self.captcha_reader = captcha_reader

    def get_data(self, bot: Bot):
        if 'position_local_filename' not in bot.data.keys():
            return bot.data
        data = bot.data
        board, angle = self.captcha_reader.resolve(data['position_local_filename'])
        data['captcha_angle'] = angle
        data['captcha_board'] = board.txt()

        return data
