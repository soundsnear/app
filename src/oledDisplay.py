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

last_url = None

def display_image_url(image_url):
    if image_url != last_url:
        last_url = image_url
        response = requests.get(image_url)
        file_handle = io.BytesIO(response.content)
        img = Image.open(file_handle).convert("RGBA") \
            .resize((device.height,device.width), Image.Resampling.LANCZOS) \
            .transform(device.size, Image.Transform.AFFINE, (1, 0, 0, 0, 1, 0), Image.Resampling.BILINEAR) \
            .convert(device.mode)

        device.display(img)

if __name__ == "__main__":
    try:
        image_url = 'https://media.istockphoto.com/id/961208196/photo/wild-brown-bear-cub-closeup.jpg?s=612x612&w=0&k=20&c=xj5iyHym1-Nn-L5g2hMgvsOykxnubR2fQA2NJnIugzY='
        display_image_url(image_url)
    except KeyboardInterrupt:
        pass

