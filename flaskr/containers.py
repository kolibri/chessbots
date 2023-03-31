from dependency_injector import containers, providers
from chessbots.lib.board import *
from chessbots.tool.printer import *
from chessbots.tool.pattern_creator import *
from chessbots.lib.bot.mockbot import *
from chessbots.lib.print_units import *
from chessbots.lib.bot import *


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
        'bots': {'cache_dir': 'build/bots'},
        'mockbot': {'cache_dir': 'build/mockbot'}

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

    mockbots = providers.Factory(
        MockBots,
        board=Pattern8x8With4DataFields().create(800)
    )

    mockbot_picture_creator = providers.Factory(
        MockbotPictureCreator,
        path=config['mockbot']['cache_dir'],
        printer=pattern_printer,
        mockbots=mockbots
    )

    bot_manager = providers.Factory(
        BotManager,
        data_dir=config['bots']['cache_dir'],
    )

    bot_repository = providers.Factory(
        BotRepository,
        bot_manager=bot_manager,
    )

    game_board = providers.Factory(
        Board,
        bot_repo=bot_repository,
        game=Game()
    )

