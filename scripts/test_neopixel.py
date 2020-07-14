import board
import neopixel
import time


if __name__ == "__main__":
    pixel = neopixel.NeoPixel(pin=board.D18, n=5, pixel_order=neopixel.RGBW)
    pixel[0] = (0, 50, 0, 0, 50, 10, 20, 30, 15)
    time.sleep(10)