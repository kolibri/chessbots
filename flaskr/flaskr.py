import os
from flask import (
    Flask, render_template, send_from_directory
)

from flaskr.blueprints import bots
from flaskr.blueprints import tools
from flaskr.blueprints import mockbot
from flaskr.blueprints import board
from flaskr.blueprints import dashboard


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
    app.register_blueprint(board.bp)
    app.register_blueprint(dashboard.bp)

    @app.route("/")
    def index():
        return render_template('index.html.j2')

    @app.route("/favicon.png")
    def favicon():
        return send_from_directory('public', 'favicon.png')

    @app.route("/hc")
    def health_check():
        return 'ok'

    return app
