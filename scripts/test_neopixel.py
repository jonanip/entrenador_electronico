import board
import neopixel
import time


if __name__ == "__main__":
    pixel = neopixel.NeoPixel(pin=board.D18, n=5, pixel_order=neopixel.RGBW)
    pixel[3] = (50, 50, 0, 0)
    pixel[0] = (0, 50, 0, 0)
    pixel[1] = (50, 0, 0, 0)
    time.sleep(10)