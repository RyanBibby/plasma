import plasma
import WIFI_CONFIG
import uasyncio
from network_manager import NetworkManager
from plasma import plasma_stick
from random import uniform
import time
from umqtt.simple import MQTTClient
"""
A festive sparkly effect. Play around with BACKGROUND_COLOUR and SPARKLE_COLOUR for different effects!
"""

# Set how many LEDs you have
NUM_LEDS = 192

# How many sparkles? [bigger number = more sparkles]
SPARKLE_INTENSITY = 0.005

# Change your colours here! RGB colour picker: https://g.co/kgs/k2Egjk
BACKGROUND_COLOUR = [50, 50, 50]
SPARKLE_COLOUR = [77, 119, 230]
SPARKLE_COLOUR = [225 // 3, 0, 0]
BACKGROUND_COLOUR = [255 // 3 , 128 // 3, 0]


# BACKGROUND_COLOUR = [50, 50, 0]
# SPARKLE_COLOUR = [255, 255, 0]
# how quickly current colour changes to target colour [1 - 255]
FADE_UP_SPEED = 1
FADE_DOWN_SPEED = 1

r = 0
g = 0
b = 0
status = True

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

def spooky_rainbows():
    while True:
        for i in range(NUM_LEDS):
                led_strip.set_rgb(i, 50, 50, 50)

def display_current():
    # paint our current LED colours to the strip
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, current_leds[i][0], current_leds[i][1], current_leds[i][2])


def move_to_target():
    # nudge our current colours closer to the target colours
    for i in range(NUM_LEDS):
        for c in range(3):  # 3 times, for R, G & B channels
            if current_leds[i][c] < target_leds[i][c]:
                current_leds[i][c] = min(current_leds[i][c] + FADE_UP_SPEED, target_leds[i][c])  # increase current, up to a maximum of target
            elif current_leds[i][c] > target_leds[i][c]:
                current_leds[i][c] = max(current_leds[i][c] - FADE_DOWN_SPEED, target_leds[i][c])  # reduce current, down to a minimum of target
                
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

# Create a list of [r, g, b] values that will hold current LED colours, for display
current_leds = [[255 // 3 , 128 // 3, 0] for i in range(NUM_LEDS)]
# Create a list of [r, g, b] values that will hold target LED colours, to move towards
target_leds = [[0] * 3 for i in range(NUM_LEDS)]

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
state_topic = "ledstrip1/state"
brightness_command_topic = "ledstrip1/brightness/set"
rgb_command_topic = "ledstrip1/color/set"

client = MQTTClient('LED Strip 1', '192.168.1.88', 1883, 'ryan', 'panda')
client.set_callback(sub)
client.connect()
client.subscribe("ledstrip1/#")


client.publish(state_topic, "ON")
while True:
    prev_status = status
    client.check_msg()
    if status:
        if prev_status != status:
            client.publish(state_topic, "ON")
            print("ON NOW")
        for i in range(NUM_LEDS):
            # randomly add sparkles
            if SPARKLE_INTENSITY > uniform(0, 1):
                # set a target to start a sparkle
                target_leds[i] = SPARKLE_COLOUR
            # for any sparkles that have achieved max sparkliness, reset them to background
            if current_leds[i] == target_leds[i]:
                target_leds[i] = BACKGROUND_COLOUR
        move_to_target()   # nudge our current colours closer to the target colours
        display_current()  # display current colours to strip
    else:
        if prev_status != status:
            client.publish(state_topic, "OFF")
            print("OFF NOW")
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, 0, 0, 0)
    