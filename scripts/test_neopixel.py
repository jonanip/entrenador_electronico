import board
import neopixel
import time


if __name__ == "__main__":
    pixel = neopixel.NeoPixel(pin=board.D18, n=12, pixel_order=neopixel.GRB)
    pixel[0] = (10, 10, 0,)
    pixel[1] = (10, 0, 10,)
    pixel[2] = (10, 0, 0,)
    pixel[3] = (10, 20, 0,)
    pixel[4] = (10, 0, 20,)
    pixel[5] = (0, 20, 20,)
    pixel[6] = (10, 0, 0,)
    pixel[7] = (0, 10, 0,)
    pixel[8] = (0, 0, 10,)
    pixel.show()
    time.sleep(10)