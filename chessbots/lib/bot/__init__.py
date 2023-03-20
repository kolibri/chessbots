from __future__ import annotations
from werkzeug.datastructures import MultiDict
import os
import hashlib
from chessbots.lib.filesystem import read_json, dump_json


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
