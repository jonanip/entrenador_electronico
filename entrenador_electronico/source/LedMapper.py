from config import config
try:
    import board
    import neopixel
    config.general.led_system = True
except NotImplementedError:
    config.general.led_system = False

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.solid import Solid
import time
import threading


class LedMapper(threading.Thread):
    counter = 0
    def __init__(self):
        super().__init__()
        self.pixel = neopixel.NeoPixel(pin=board.D18, n=12, pixel_order=neopixel.GRB)

    def solid_light(self, color="red", pins=[]):
        led_color = config.led_colors[color]
        solid = Solid(self.pixel, color=led_color)
        solid.animate()

    def pulse_light(self, color="red", speed=1.0, pins=[]):
        led_color = config.led_colors[color]
        pulse = Pulse(self.pixel, speed=speed, color=led_color)
        while True:
            pulse.animate()
        # for pin in pins:
        #     target_pix = self.pixel[pin]
        #     pulse = Pulse(target_pix, speed=speed, color=led_color)
        #     pulse.animate()

    def blink_light(self, color="red", pins=None, speed=1):
        id = LedMapper.counter
        led_color = config.led_colors[color]
        current_pixels = []
        blinks = []
        for pin in pins:
            blink = Blink(self.pixel[pin], speed=speed, color=led_color)
            blinks.append(blink)
        while id == LedMapper.counter:
            for blink in blinks:
                blink.animate()

    def stop_lights(self):
        self.running = False
