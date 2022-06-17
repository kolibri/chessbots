import os
from flask import (
    Flask, render_template, send_from_directory
)
from . import bots
from . import tools
from . import scripts


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

    app.config.update(
        STATIC_DIR='flaskr/static/images/',
        BOTCACHE_DIR='flaskr/bot_cache/',
        BOARD_SIZE_IN_CAPTCHAS=10
    )

    app.register_blueprint(bots.bp)
    app.register_blueprint(tools.bp)
    app.register_blueprint(scripts.bp)

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/favicon.png")
    def favicon():
        return send_from_directory('static', 'favicon.png')

    @app.route("/hc")
    def health_check():
        return 'ok'

    return app
