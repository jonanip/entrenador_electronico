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
from adafruit_led_animation.helper import PixelMap
from entrenador_electronico.source.Connections import Connections
from entrenador_electronico.source.components import Components, BaseComponent
import time
import threading
from typing import List
import numpy as np


class LedMapper(threading.Thread):
    counter = 0
    component_board_led_number = 63
    tension_board_led_number = 63
    leds_in_row = 21
    number_of_rows_per_board = 3
    component_phase = True
    connection_phase = False

    def __init__(self):
        super().__init__()
        self.pixel = neopixel.NeoPixel(pin=board.D18, n=126, pixel_order=neopixel.GRB)

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
        current_pixels = PixelMap(self.pixel, pins, individual_pixels=True)
        blink = Blink(current_pixels, speed=speed, color=led_color)
        while id == LedMapper.counter:
            blink.animate()

    def stop_lights(self):
        self.running = False

    # @staticmethod
    # def map_local_id_to_led_id(vec: List, board="component"):
    #     for local_id in vec:

    @staticmethod
    def map_local_id_to_led_id(value):
        value = value + 1
        rest_id = value % LedMapper.number_of_rows_per_board
        n_id = np.floor(value / LedMapper.number_of_rows_per_board)
        if value < LedMapper.component_board_led_number:
            if rest_id == 0:
                return int(n_id)
            elif rest_id == 1:
                return int(LedMapper.leds_in_row * 2 - n_id - 1)
            elif rest_id == 2:
                return int(LedMapper.leds_in_row * 2 + n_id)

        if value > LedMapper.component_board_led_number:
            value -= LedMapper.component_board_led_number
            rest_id = value % LedMapper.number_of_rows_per_board
            n_id = np.floor(value / LedMapper.number_of_rows_per_board)
            if rest_id == 0:
                return int(n_id + LedMapper.component_board_led_number)
            elif rest_id == 1:
                return int(LedMapper.leds_in_row * 2 - n_id - 1 + LedMapper.component_board_led_number)
            elif rest_id == 2:
                return int(LedMapper.leds_in_row * 2 + n_id + LedMapper.component_board_led_number)

    def lights_in_order(self):
        for pin in range(0, 63):
            led_pin = LedMapper.map_local_id_to_led_id(pin)
            self.pixel[led_pin] = (50, 0, 0)
            self.pixel.show()
            time.sleep(0.5)

    def lights_off(self):
        solid_off = Solid(self.pixel, color=(0, 0, 0))
        solid_off.animate()

    def lights_off_specific_pins(self, pins):
        pins = [LedMapper.map_local_id_to_led_id(pin) for pin in pins]
        sub_pixel_component = PixelMap(self.pixel, pins, individual_pixels=True)
        solid_off = Solid(self.pixel, color=(0, 0, 0))
        solid_off.animate()

    def update_main_board_lights(self):
        """Controls the main board component lights"""
        self.lights_off()
        id = LedMapper.counter
        solid_lights = []
        component: BaseComponent
        # Start the lights of the circuit
        for component_id in Components.components:
            component = Components.components[component_id]
            if component.__class__.__name__ == "BatteryComponent":
                continue
            if component.__class__.__name__ == "ConnectionComponent":
                continue
            pins = list(range(component.get_pins[0][1], component.get_pins[1][1] + 1))
            if component.board == "main board":
                pins = np.array(pins) + LedMapper.component_board_led_number
            pins = [LedMapper.map_local_id_to_led_id(pin) for pin in pins]

            sub_pixel_component = PixelMap(self.pixel, pins, individual_pixels=True)

            solid_light = Solid(sub_pixel_component, color=component.led_color)
            solid_lights.append(solid_light)
        while LedMapper.component_phase and LedMapper.counter == id:
            for solid_light in solid_lights:
                solid_light.animate()
