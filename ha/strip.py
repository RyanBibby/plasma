import plasma
from plasma import plasma_stick
class Strip:

    @staticmethod
    def build_rgb(number_of_leds, pattern):
        return Strip(number_of_leds, pattern, plasma.COLOR_ORDER_RGB)

    def __init__(self, number_of_leds, pattern, color_order):
        self.pixels = plasma.WS2812(number_of_leds, 0, 0, plasma_stick.DAT, color_order=color_order)
        self.number_of_leds = number_of_leds
        self.pattern = pattern
        self.on = True

    def pattern(self, pattern):
        self.pattern = pattern

    def turn_on(self):
        print("Turning on")
        self.on = True

    def turn_off(self):
        print("Turning off")
        self.on = False

    def update(self):
        if self.on:
            self.pattern.display()
        else:
            print("Off")
            for i in range(self.number_of_leds):
                self.pixels.set_rgb(i, 0, 0, 0)
