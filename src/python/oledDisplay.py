from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1351
from pathlib import Path
from PIL import Image
import time
import requests
import io

serial = spi(device=1, port=0, gpio_DC=27, gpio_RST=22, bus_speed_hz=16000000)
device = ssd1351(serial, bgr=True, width=128, height=128)
 

def display_image_url(image_url):
    r = requests.get(image_url)
    file_handle = io.BytesIO(r.content)
    img = Image.open(file_handle).convert("RGBA") \
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

