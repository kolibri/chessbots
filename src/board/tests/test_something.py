import cv2
from ..flaskr import create_app
from ..flaskr.BotData.Captcha import Captcha
from ..flaskr.BotData.Board import *


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_health_check(client):
    response = client.get('/hc')
    assert response.status_code == 200
    assert response.data == b'ok'


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_bots(client, runner):
    result = runner.invoke(args=["script", "cleanup"])
    response = client.get('/bots/')
    assert response.status_code == 200
    assert response.data == b'[]\n'

    response = client.post(
        "/bots/register",
        json=["http://0.0.0.0:8031/tools/mockbot/01",
              "http://0.0.0.0:8031/tools/mockbot/02"])
    assert response.status_code == 205
    assert response.json == [
        {"id": "511b29e3", "url": "http://0.0.0.0:8031/tools/mockbot/01"},
        {"id": "811c9d06", "url": "http://0.0.0.0:8031/tools/mockbot/02"}
    ]
    '''
    # does not work because of http requests to get bot data /:
    response = client.patch("/bots/")
    assert response.status_code == 200
    assert response.json == [
        {"live_image": "http://0.0.0.0:8031/tools/mockbot/01/position.png",
         "motors": {"left": {"pins": {"pinA": "0", "pinB": "0", "pinPwm": "0"}},
                    "right": {"pins": {"pinA": "0", "pinB": "0", "pinPwm": "0"}}}, "name": "herzbube", "piece": "wk",
         "state": "online", "url": "http://0.0.0.0:8031/tools/mockbot/01",
         "position_local_filename": "flaskr/bot_cache/511b29e3_position.png", "id": "511b29e3", "captcha_angle": None,
         "captcha_img_matches": "flaskr/bot_cache/511b29e3_matches.png"},
        {"live_image": "http://0.0.0.0:8031/tools/mockbot/02/position.png",
         "motors": {"left": {"pins": {"pinA": "0", "pinB": "0", "pinPwm": "0"}},
                    "right": {"pins": {"pinA": "0", "pinB": "0", "pinPwm": "0"}}}, "name": "pikass", "piece": "bq",
         "state": "online", "url": "http://0.0.0.0:8031/tools/mockbot/02",
         "position_local_filename": "flaskr/bot_cache/811c9d06_position.png", "id": "811c9d06", "captcha_angle": None,
         "captcha_img_matches": "flaskr/bot_cache/811c9d06_matches.png"}
    ]
    '''
