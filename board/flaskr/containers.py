from dependency_injector import containers, providers
from chessbots.lib.board import *
from chessbots.lib.mockbot import *
from chessbots.tool.printer import *
from chessbots.tool.pattern_creator import *
from chessbots.lib.print_units import *
from chessbots.lib.bot import *


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        ".blueprints.bots",
        ".blueprints.mockbot",
        ".blueprints.tools",
        ".blueprints.board",
    ])

    config = {
        'print': {
            'dpi': 600,
            'marker_size': 60
        },
        'board_dir': 'build/bots',
        'mockbot_dir': 'build/mockbot',
        'print_dir': 'build/print', # <-- currently unused

    }

    pattern_printer = providers.Factory(
        PatternPrinter,
        dpi=config['print']['dpi'],
        point_size=PrintPixel(config['print']['marker_size'])
    )

    mockbot_factory = providers.Factory(
        MockbotFactory,
        printer=pattern_printer,
        base_board=Pattern8x8With4DataFields().create(800)
    )
    mockbots = providers.Factory(
        MockBots,
        data_dir=config['mockbot_dir'],
        factory=mockbot_factory,
    )

    bot_manager = providers.Factory(
        BotManager,
        data_dir=config['board_dir'],
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

