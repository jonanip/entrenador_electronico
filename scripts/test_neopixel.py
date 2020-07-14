import board
import neopixel

if __name__ == "__main__":
    pixel = neopixel.NeoPixel(pin=board.D18, n=5, pixel_order=neopixel.RGBW)
    pixel[0] = (30, 0, 20, 10)