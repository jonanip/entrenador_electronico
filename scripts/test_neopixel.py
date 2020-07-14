import board
import neopixel
import time


if __name__ == "__main__":
    pixel = neopixel.NeoPixel(pin=board.D18, n=5,  brightness=0.2, pixel_order=ORDER)
    pixel[0] = (10, 0, 0, 10)
    time.sleep(10)