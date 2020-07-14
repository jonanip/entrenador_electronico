from config import config
try:
    import board
    import neopixel
    config.general.led_system = True
except NotImplementedError:
    config.general.led_system = False

from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.solid import Solid



class LedMapper:
    def __init__(self):
        self.pixel = neopixel.NeoPixel(pin=board.D18, n=12, pixel_order=neopixel.GRB)

    def solid_light(self, color="red", pins=[]):
        led_color = config.led_colors[color]
        solid = Solid(self.pixel, color=led_color)
        solid.animate()

    def pulse_light(self, color="red", speed=0.5, pins=[]):
        led_color = config.led_colors[color]
        for pin in pins:
            target_pix = self.pixel[pin]
            pulse = Pulse(target_pix, speed=speed, color=led_color)
            pulse.animate()
