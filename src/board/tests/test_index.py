from ..flaskr import create_app


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

