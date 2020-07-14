import board
import neopixel

if __name__ == "__main__":
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
    pixels[0] = (10, 0, 0)
    pixels.show()
    print("done")