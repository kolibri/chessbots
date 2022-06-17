from os.path import isfile, join
from werkzeug.datastructures import MultiDict
from os import listdir

from .Bot import Bot


class Bots:
    def __init__(self, dir, collectors):
        self.cache_dir = dir
        self.bots = self.__load(self.cache_dir)
        self.collectors = collectors

    def add(self, urls: [str]):
        bots = [Bot(url, {}) for url in urls]
        # self.bots = self.bots + bots
        for bot in bots:
            bot.save(self.cache_dir)

    def update(self, filters: "MultiDict[str, str]") -> [Bot]:
        bots = []
        for bot in self.filter(filters):
            for c in self.collectors:
                bot = Bot(bot.host_name, c.get_data(bot))
            bots.append(bot)
        return bots

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
        files = [f for f in listdir(base_dir) if isfile(base_dir + f)]
        return [Bot.from_file(join(base_dir, f)) for f in files if f.endswith('.json')]
