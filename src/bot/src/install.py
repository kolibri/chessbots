import network
import utime
import ntptime
import upip
import config


def connect_wifi(config):
    sta_if = network.WLAN(network.STA_IF)
    start = utime.time()
    timed_out = False

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config['ssid'], config['pass'])
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

connect_wifi(config.wifi)

upip.install('picoweb')
#upip.install('bot-ulogging')
upip.install('uasyncio')
