import plasma

class Strip:

    @staticmethod
    def build_rgb(number_of_leds, pattern):
        return Strip(number_of_leds, pattern, plasma.COLOR_ORDER_RGB)

    def __init__(self, number_of_leds, pattern, color_order):
        self.pixels = plasma.WS2812(number_of_leds, 0, 0, plasma_stick.DAT, color_order=color_order)
        self.number_of_leds = number_of_leds
        self.pattern = pattern

    def pattern(self, pattern):
        self.pattern = pattern

    def update():
        if QueueHander.handle:
            pattern.display()
        else:
            for i in range(number_of_leds):
                pixels.set_rgb(i, 0, 0, 0)

        # Tell don't ask. Really this strip should be either on or off. 
        # Get told if on or off by queue. Queue can also give pattern name
