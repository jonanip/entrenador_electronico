import board
import neopixel
import time


if __name__ == "__main__":
    pixel = neopixel.NeoPixel(pin=board.D18, n=2, pixel_order=neopixel.RGBW)
    pixel[0] = (50, 50, 0)
    pixel[1] = (0, 0, 50)
    pixel.show()

    time.sleep(10)