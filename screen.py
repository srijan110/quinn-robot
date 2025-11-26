import time
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont, ImageOps

def init_oled(max_retries=5):
    i2c = None
    oled = None

    for attempt in range(1, max_retries + 1):
        try:
            if i2c is None:
                i2c = busio.I2C(board.SCL, board.SDA)

            oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)
            return oled  # success

        except OSError as e:
            time.sleep(0.01)

    raise RuntimeError("OLED failed after retries.")

def show_image(img_path):
    oled = init_oled()
    oled.fill(0)
    oled.show()

    img = Image.open(img_path)
    img = img.resize((64, 64)) 

    r, g, b, a = img.split()

    img = a.point(lambda p: 255 if p > 0 else 0).convert("1")

    canvas = Image.new("1", (128, 64))
    canvas.paste(img, (32, 0))

    oled.image(canvas)
    oled.show()

if __name__ == "__main__":
    show_image("assets/normal.png")
