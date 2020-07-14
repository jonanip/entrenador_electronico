import board
import neopixel
import time


if __name__ == "__main__":
    pixel = neopixel.NeoPixel(pin=board.D18, n=12, pixel_order=neopixel.RGB)
    pixel[0] = (10, 0, 0, 0)
    pixel[1] = (10, 0, 0, 0)
    pixel[2] = (10, 0, 0, 0)
    pixel[3] = (10, 0, 0, 0)
    pixel[4] = (10, 0, 0, 0)
    pixel[5] = (10, 0, 0, 0)
    pixel[6] = (10, 0, 0, 0)
    pixel[7] = (10, 0, 0, 0)
    pixel.show()
    time.sleep(10)