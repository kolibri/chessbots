from dependency_injector import containers, providers
from chessbots.tool.printer import *
from chessbots.tool.pattern_creator import *
from chessbots.lib.print_units import *
from chessbots.lib.bot import BotManager, ChainDataCollector, RobotApiCollector


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        ".blueprints.bots",
        ".blueprints.tools",
    ])

    config = {
        'print': {
            'dpi': 600,
            'marker_size': 60
        },
        'bots': {
            'cache_dir': 'build/bots'
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

    pattern_creator = providers.Factory(Pattern8x8With4DataFields)
    collector = providers.Factory(
        ChainDataCollector,
        collectors=[
            RobotApiCollector(config['bots']['cache_dir']),
        ]
    )

    bot_manager = providers.Factory(
        BotManager,
        cache_dir=config['bots']['cache_dir'],
        collector=collector
    )
