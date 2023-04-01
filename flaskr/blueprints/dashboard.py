from flask import (Blueprint, render_template)
from flask import Flask

from chessbots.lib.bot.mockbot import MockBots
from dependency_injector.wiring import inject, Provide
from flaskr.containers import Container

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
app = Flask(__name__)


@bp.route('/', methods=['GET'])
@inject
def get_dashboard(mockbots: MockBots = Provide[Container.mockbots]):
    return render_template('dashboard.html.j2', mockbots=[bot.url() for bot in mockbots.bots])


@bp.route('/new', methods=['GET'])
@inject
def get_dashboard_new():
    return render_template('dashboard_new.html.j2')

