from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1351
from pathlib import Path
from PIL import Image
import time

root_image_path="/home/tyler/playground/luma.examples/examples/images"
filename="ab67616d00001e02cdf367607728e48fc580a6f9"
#filename="pi_logo.png"

def main():
    img_path = str(Path(__file__).resolve().parent.joinpath(root_image_path, filename))
    img = Image.open(img_path).convert("RGBA") \
      .resize((device.height,device.width), Image.Resampling.LANCZOS) \
      .transform(device.size, Image.Transform.AFFINE, (1, 0, 0, 0, 1, 0), Image.Resampling.BILINEAR) \
      .convert(device.mode)

    while True:
        # Image display
        device.display(img)
        time.sleep(5)


if __name__ == "__main__":
    try:
        serial = spi(device=1, port=0, gpio_DC=27, gpio_RST=22, bus_speed_hz=16000000)
        device = ssd1351(serial, bgr=True, width=128, height=128)
        main()
    except KeyboardInterrupt:
        pass

