import board
import neopixel
import time


if __name__ == "__main__":
    pixel = neopixel.NeoPixel(pin=board.D18, n=5, pixel_order=neopixel.RGBW)
    pixel[5] = (100, 0, 0, 25)
    time.sleep(10)