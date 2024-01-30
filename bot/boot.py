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
import mcp23017

class Logger:
    def __init__(self):
        self.msg = []

    def log(self, msg: str):
        self.msg.append(msg)

    def get_log(self) -> str:
        return '\n'.join(self.msg)

class Motor:
    def __init__(self, pins):
        self.mapped_pins = pins #[machine.Pin(pin, machine.Pin.OUT) for pin in pins]
        self.sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

    def move(self):
        print('move)')
        while True:
            for step in self.sequence:
                for i in range(len(self.mapped_pins)):
                    self.mapped_pins[i].output(step[i])
                    time.sleep(0.001)

class Chessbot:
    def __init__(self, config, mcp: MCP23017, log: Log):
        print('INIT')
        self.wifi_ssid = config.wifi['ssid']
        self.wifi_pass = config.wifi['pass']
        self.data = config.bot
        self.log = log
        self.mcp = mcp
        self.log.log('inititialized')
        self.motor1 = Motor([mcp[0], mcp[1], mcp[2], mcp[3]])
        self.motor2 = Motor([mcp[4], mcp[5], mcp[6], mcp[7]])
        #self.motor2 = Motor([12,16,3,1])

    def boot(self):
        connection = self.connect_wifi()

        if False is connection:
            print('no connection, no service')
            exit(1)

        camera.init(0, format=camera.JPEG)

        self.data['url'] = connection[0]
        self.data['live_image'] = 'http://' + connection[0] + '/position.jpeg'
        self.log.log('booted')

    def get_data(self):
        return self.data

    def move(self):
        #self.motor1.move()
        self.motor2.move()
        return 'foo'
#        raw = yield from req.reader.readexactly(int(req.headers[b"Content-Length"]))
#        raw = raw.decode('UTF-8')
#        sequence = json.loads(raw)


        # print('gise', sequence)
        # print('sese', self.sequence)

    def picture(self):
        return camera.capture()

    def connect_wifi(self):
        print('connecting starts')
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


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''
print('Hello start')

i2c = machine.SoftI2C(scl=machine.Pin(14), sda=machine.Pin(15))
print(i2c.scan())
mcp = mcp23017.MCP23017(i2c, 0x20)


log = Logger()
chessbot = Chessbot(config, mcp, log)
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
        data = chessbot.move()
    else:
        print('!post -> data')
        data = chessbot.get_data()
        data['state'] = 'online'
        chessbot.move()

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

@app.route("/log")
def position(req, resp):
    yield from picoweb.start_response(resp, 'text/plain', headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
    })
    yield from resp.awrite(log.get_log())



# rtc = machine.RTC()
# print(rtc.datetime())

#pin = machine.Pin(0, machine.Pin.OUT)
#pin.on()


app.run(debug=True, host='0.0.0.0', port=80)
