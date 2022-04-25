import os
from flask import (
    Flask, render_template
)
from . import bots
from . import tools


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

    app.register_blueprint(bots.bp)
    app.register_blueprint(tools.bp)

    @app.route("/")
    def index():
        return render_template('index.html')

    return app
