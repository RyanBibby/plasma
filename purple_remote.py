import plasma
import WIFI_CONFIG
import uasyncio
from network_manager import NetworkManager
from plasma import plasma_stick
import time
from umqtt.simple import MQTTClient
from random import random, uniform

"""
A basic fire effect.
"""

def status_handler(mode, status, ip):
    # reports wifi connection status
    print(mode, status, ip)
    print('Connecting to wifi...')
    # flash while connecting
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, 50, 50, 50)
        time.sleep(0.02)
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, 0, 0, 0)
    if status is not None:
        if status:
            print('Wifi connection successful!')
        else:
            print('Wifi connection failed!')
            # if no wifi connection, you get spooky rainbows. Bwahahaha!
            spooky_rainbows()

# Set how many LEDs you have
NUM_LEDS = 192

# WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_GRB)

# Start updating the LED strip
led_strip.start()

def sub(topic, msg):
    global r, g, b, brightness, status

    stopic = topic.decode("utf-8")
    smsg = msg.decode("utf-8")
    
    if stopic == rgb_command_topic:
        print("RGB")
        print(smsg)
        tr,tg,tb = (smsg.split(","))
        r = int(int(tr) / 4)
        g = int(int(tg) / 4)
        b = int(int(tb) / 4)
    elif stopic == brightness_command_topic:
        brightness = float(smsg)/255
    elif stopic == command_topic:
        print("Command")
        print(smsg)
        if smsg == "ON":
            status = True
        else:
            status = False 

try:
    network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
    uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
except Exception as e:
    print(f'Wifi connection failed! {e}')
    # if no wifi, then you get...
    spooky_rainbows()

command_topic = "ledstrip2/switch"
state_topic = "ledstrip2/state"
brightness_command_topic = "ledstrip2/brightness/set"
rgb_command_topic = "ledstrip2/color/set"

FADE_UP_SPEED = 0.01
FADE_DOWN_SPEED = 0.01

current_leds = [[uniform(0.8, 1), 1.0, random()] for i in range(NUM_LEDS)]
target_leds = [[uniform(0.8, 1), 1.0, random()] for i in range(NUM_LEDS)]

status = True

client = MQTTClient('LED Strip 2', '192.168.1.88', 1883, 'ryan', 'panda')
client.set_callback(sub)
client.connect()
client.subscribe("ledstrip2/#")

client.publish(state_topic, "ON")



def spooky_rainbows():
    while True:
        for i in range(NUM_LEDS):
                led_strip.set_rgb(i, 50, 50, 50)

def move_to_target():
    for i in range(NUM_LEDS):
        for c in range(3):
            if current_leds[i][c] < target_leds[i][c]:
                current_leds[i][c] = min(current_leds[i][c] + FADE_UP_SPEED, target_leds[i][c])
            elif current_leds[i][c] > target_leds[i][c]:
                current_leds[i][c] = max(current_leds[i][c] - FADE_DOWN_SPEED, target_leds[i][c])

def display_current():
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, current_leds[i][0], current_leds[i][1], current_leds[i][2])



while True:
    prev_status = status
    client.check_msg()
    if status:
        if prev_status != status:
            client.publish(state_topic, "ON")
            print("ON NOW")
        for i in range(NUM_LEDS):
            if current_leds[i] == target_leds[i]:
                target_leds[i] = [uniform(0.8, 1), 1.0, random()]
        move_to_target()
        display_current()
    else:
        if prev_status != status:
            client.publish(state_topic, "OFF")
            print("OFF NOW")
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, 0, 0, 0)
