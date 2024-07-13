import plasma
from plasma import plasma_stick
import time
from random import random, uniform

"""
A basic fire effect.
"""

# Set how many LEDs you have
NUM_LEDS = 192

# WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_GRB)

# Start updating the LED strip
led_strip.start()

FADE_UP_SPEED = 0.01
FADE_DOWN_SPEED = 0.01

current_leds = [[uniform(0.8, 1), 1.0, random()] for i in range(NUM_LEDS)]
target_leds = [[uniform(0.8, 1), 1.0, random()] for i in range(NUM_LEDS)]

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
    for i in range(NUM_LEDS):
        if current_leds[i] == target_leds[i]:
            target_leds[i] = [uniform(0.8, 1), 1.0, random()]
    move_to_target()
    display_current()  
