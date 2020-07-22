import board
import neopixel
import time


if __name__ == "__main__":
    pixel = neopixel.NeoPixel(pin=board.D18, n=12, pixel_order=neopixel.GRB)
    pixel[0] = (1, 1, 0,)
    pixel[1] = (1, 0, 1,)
    pixel[2] = (1, 0, 0,)
    pixel[3] = (1, 2, 0,)
    pixel[4] = (1, 0, 2,)
    pixel[5] = (0, 2, 2,)
    pixel[6] = (1, 0, 0,)
    pixel[7] = (0, 1, 0,)
    pixel[8] = (0, 0, 1,)
    pixel.show()
    time.sleep(10)