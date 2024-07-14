import WIFI_CONFIG

import uasyncio
from network_manager import NetworkManager

from strip import Strip
from purple import Purple
from queue_handler import QueueHander

NUM_LEDS = 50
pattern = Purple()

strip = Strip.build_rgb(NUM_LEDS, pattern)

def status_handler(mode, status, ip):
    # for i in range(NUM_LEDS):
    #     led_strip.set_rgb(i, 50, 50, 50)
    #     time.sleep(0.02)
    # for i in range(NUM_LEDS):
    #     led_strip.set_rgb(i, 0, 0, 0)
    if status is not None:
        if status:
            print('Wifi connection successful!')
        else:
            print('Wifi connection failed!')
            default_pattern()

try:
    network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
    uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
except Exception as e:
    print(f'Wifi connection failed! {e}')
    default_pattern()

def default_pattern():
    while True:
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, 50, 50, 50)

queue = QueueHander("ledstrip2", strip)
while True:
    queue.check()
    strip.update()