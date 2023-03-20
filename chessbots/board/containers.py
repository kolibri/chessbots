from dependency_injector import containers, providers
from chessbots.tool.printer import *
from chessbots.tool.pattern_creator import *
from chessbots.lib.bot.mockbot import *
from chessbots.lib.print_units import *
from chessbots.lib.captcha.position import *
from chessbots.lib.bot import BotManager
from chessbots.lib.bot.data_collector import ChainDataCollector, RobotApiCollector, CaptchaReaderCollector


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        ".blueprints.bots",
        ".blueprints.mockbot",
        ".blueprints.tools",
    ])

    config = {
        'print': {
            'dpi': 600,
            'marker_size': 60
        },
        'bots': {
            'cache_dir': 'build/bots'
        },
        'mockbot': {
            'cache_dir': 'build/mockbot'
        }

    }

    pattern_printer = providers.Factory(
        PatternPrinter,
        dpi=config['print']['dpi'],
        point_size=PrintPixel(config['print']['marker_size'])
    )

    tiled_pattern_printer = providers.Factory(
        TiledPatternPrinter,
        printer=pattern_printer

    )

    board = Pattern8x8With4DataFields().create(800)

    mockbots = providers.Factory(
        MockBots,
        board=board
    )

    mockbot_tester = providers.Factory(
        MockBotTester,
        base_path=config['mockbot']['cache_dir']
    )

    mockbot_picture_creator = providers.Factory(
        MockbotPictureCreator,
        path=config['mockbot']['cache_dir'],
        printer=pattern_printer,
        mockbots=mockbots
    )

    pattern_creator = providers.Factory(Pattern8x8With4DataFields)

    collector = providers.Factory(
        ChainDataCollector,
        collectors=[
            RobotApiCollector(config['bots']['cache_dir']),
            CaptchaReaderCollector(),
        ]
    )

    bot_manager = providers.Factory(
        BotManager,
        cache_dir=config['bots']['cache_dir'],
        collector=collector
    )

