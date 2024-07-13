import WIFI_CONFIG
from network_manager import NetworkManager
import uasyncio
import urequests
import time
import plasma
from plasma import plasma_stick
from machine import Pin
from umqtt.simple import MQTTClient

# Set how many LEDs you have
NUM_LEDS = 50
def status_handler(mode, status, ip):
    # reports wifi connection status
    print(mode, status, ip)
    print('Connecting to wifi...')
    # # flash while connecting
    # for i in range(NUM_LEDS):
    #     led_strip.set_rgb(i, 255, 255, 255)
    #     time.sleep(0.02)
    # for i in range(NUM_LEDS):
    #     led_strip.set_rgb(i, 0, 0, 0)
    if status is not None:
        if status:
            print('Wifi connection successful!')
        else:
            print('Wifi connection failed!')
            # if no wifi connection, you get spooky rainbows. Bwahahaha!
            # spooky_rainbows()


def spooky_rainbows():
    print('SPOOKY RAINBOWS!')
    HUE_START = 180  # orange
    HUE_END = 240  # green
    SPEED = 0.6  # bigger = faster (harder, stronger)

    distance = 0.0
    direction = SPEED
    while True:
        for i in range(NUM_LEDS):
            # generate a triangle wave that moves up and down the LEDs
            j = max(0, 1 - abs(distance - i) / (NUM_LEDS / 3))
            hue = HUE_START + j * (HUE_END - HUE_START)

            led_strip.set_hsv(i, hue / 360, 1.0, 0.8)

        # reverse direction at the end of colour segment to avoid an abrupt change
        distance += direction
        if distance > NUM_LEDS:
            direction = - SPEED
        if distance < 0:
            direction = SPEED

        time.sleep(0.01)


def hex_to_rgb(hex):
    # converts a hex colour code into RGB
    h = hex.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return r, g, b


# set up the Pico W's onboard LED
pico_led = Pin('LED', Pin.OUT)

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)

# start updating the LED strip
led_strip.start()

# set up wifi
try:
    network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
    uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
except Exception as e:
    print(f'Wifi connection failed! {e}')
    # if no wifi, then you get...
    spooky_rainbows()


command_topic = "ledstrip1/switch"
brightness_command_topic = "ledstrip1/brightness/set"
rgb_command_topic = "ledstrip1/color/set"

r = 100
g = 100
b = 100
brightness = .5
status = True

def sub(topic, msg):
    global r, g, b, brightness, status

    stopic = topic.decode("utf-8")
    smsg = msg.decode("utf-8")
    
    if stopic == rgb_command_topic:
        tr,tg,tb = (smsg.split(","))
        r = int(int(tr) / 4)
        g = int(int(tg) / 4)
        b = int(int(tb) / 4)
    elif stopic == brightness_command_topic:
        brightness = float(smsg)/255
    elif stopic == command_topic:
        if smsg == "ON":
            status = True
        else:
            status = False 

print("Loading")
client = MQTTClient('LED Strip 1', '192.168.1.88', 1883, 'ryan', 'panda')
client.set_callback(sub)
client.connect()
client.subscribe("ledstrip1/#")

while True:
    client.check_msg()

    print(r)
    print(g)
    print(b)
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, r, g, b)

