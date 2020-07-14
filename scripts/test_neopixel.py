import board
import neopixel

if __name__ == "__main__":
    pixel = neopixel.NeoPixel(board.D0, 1, pixel_order=neopixel.RGBW)
    pixel[0] = (30, 0, 20, 10)