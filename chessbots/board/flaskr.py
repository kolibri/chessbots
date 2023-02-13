import os
from flask import (
    Flask, render_template, send_from_directory
)

from chessbots.board.blueprints import bots
from chessbots.board.blueprints import tools
from chessbots.board.blueprints import mockbot


from flask import Flask

from .containers import Container


def create_app(test_config=None):
    container = Container()

    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder='public',

    )
    app.container = container

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(bots.bp)
    app.register_blueprint(tools.bp)
    app.register_blueprint(mockbot.bp)

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/favicon.png")
    def favicon():
        return send_from_directory('public', 'favicon.png')

    @app.route("/hc")
    def health_check():
        return 'ok'

    return app
