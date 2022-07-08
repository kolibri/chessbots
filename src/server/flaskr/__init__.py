import os
from flask import (Flask, render_template, send_from_directory)


class GameManager:
    @staticmethod
    def get_pgn():
        pgn = '[Event "Simultaneous"]\n[Site "Budapest HUN"]\n[Date "1934.??.??"]\n[EventDate "?"]\n[Round "?"]\n[Result "1-0"]\n[White "Esteban Canal"]\n[Black "NN"]\n[ECO "B01"]\n[WhiteElo "?"]\n[BlackElo "?"]\n[PlyCount "27"]\n\n\n1.e4 d5 2.exd5 Qxd5 3.Nc3 Qa5 4.d4 c6 5.Nf3 Bg4 6.Bf4 e6 7.h3\nBxf3 8.Qxf3 Bb4 9.Be2 Nd7 10.a3 O-O-O 11.axb4 Qxa1+ 12.Kd2\nQxh1 13.Qxc6+ bxc6 14.Ba6# 1-0'
        return pgn

game_manager = GameManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # app.register_blueprint(tools.bp)  # just to remember how to import blueprints ;)

    @app.route("/")
    def index():
        return render_template('index.html', manager=game_manager)

    @app.route("/favicon.png")
    def favicon():
        return send_from_directory('static', 'favicon.png')

    return app
