# boot.py
import time
import config
import network
import utime
import ntptime
import machine
import json
import camera
import picoweb


class Chessbot:
    def __init__(self, config):
        self.wifi_ssid = config.wifi['ssid']
        self.wifi_pass = config.wifi['pass']
        self.data = config.bot
        self.motors = Motors(config.motors)

    def boot(self):
        connection = self.connect_wifi()

        if False is connection:
            print('no connection, no service')
            exit(1)

        camera.init(0, format=camera.JPEG)

        self.data['url'] = connection[0]
        self.data['live_image'] = 'http://' + connection[0] + '/position.jpeg'
        self.data['motors'] = {}

    def get_data(self):
        return self.data

    def move(self, req):
        raw = yield from req.reader.readexactly(int(req.headers[b"Content-Length"]))
        raw = raw.decode('UTF-8')
        sequence = json.loads(raw)

        self.motors.move(sequence)

        print('gise', sequence)
        print('sese', self.sequence)

    def picture(self):
        return camera.capture()

    def connect_wifi(self):
        sta_if = network.WLAN(network.STA_IF)
        start = utime.time()
        timed_out = False

        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(self.wifi_ssid, self.wifi_pass)
            while not sta_if.isconnected() and \
                    not timed_out:
                if utime.time() - start >= 20:
                    timed_out = True
                else:
                    pass

        if sta_if.isconnected():
            ntptime.settime()
            print('network config:', sta_if.ifconfig())
            return sta_if.ifconfig()
        else:
            print('internet not available')
            return False


class Motor:
    def __init__(self, pins):
        print(pins)
        self.pin_a = machine.Pin(pins[0], machine.Pin.OUT)
        self.pin_b = machine.Pin(pins[1], machine.Pin.OUT)
        self.pin_a.off()
        self.pin_b.off()

    def set_state(self, state: int):
        self.pin_a.off()
        self.pin_b.off()
        if -1 == state:
            self.pin_a.on()
        elif 1 == state:
            self.pin_b.on()


class Motors:
    def __init__(self, config):
        self.left = Motor(config['left'])
        self.right = Motor(config['right'])
        self.speed = machine.Pin(config['speed'], machine.Pin.OUT)
        self.speed.on()
        #self.speed = machine.PWM(machine.Pin(config['speed']))
        self.interval_duration = 5

    def move(self, sequence):
        for s in sequence:
            self.set_state(s[0], s[1])
            time.sleep(s[2] * self.interval_duration)
        self.set_state(0, 0)

    def set_state(self, lv, rv):
        self.left.set_state(lv)
        self.right.set_state(rv)


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''
chessbot = Chessbot(config)
chessbot.boot()
app = picoweb.WebApp(__name__)


@app.route("/")
def index(req, resp):
    data = {}
    print('method: ', req.method)
    if req.method == "OPTIONS":
        print('options -> empty')
    elif req.method == "POST":
        print('post -> move')
        data = chessbot.move(req)
    else:
        print('!post -> data')
        data = chessbot.get_data()
        data['state'] = 'online'

    yield from picoweb.start_response(resp, 'application/json', headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT",
        "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    })
    yield from resp.awrite(json.dumps(data))


@app.route("/position.jpeg")
def position(req, resp):
    yield from picoweb.start_response(resp, "image/jpeg")
    yield from resp.awrite(chessbot.picture())


# rtc = machine.RTC()
# print(rtc.datetime())

pin = machine.Pin(0, machine.Pin.OUT)
pin.on()

app.run(debug=True, host='0.0.0.0', port=80)
