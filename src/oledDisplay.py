from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1351
from pathlib import Path
from PIL import Image
import requests
import io
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

serial = spi(device=1, port=0, gpio_DC=27, gpio_RST=22, bus_speed_hz=16000000)
device = ssd1351(serial, bgr=True, width=128, height=128, persist=False)


def timestamp():
    return datetime.timestamp(datetime.now())


full_brightness=255
dim_brightness=full_brightness//6
def brighten_screen():
    device.contrast(full_brightness)

def turn_off_screen():
    device.hide()

def dim_screen():
    device.contrast(dim_brightness)

DIM_SCREEN_AFTER_SECONDS=60
SLEEP_SCREEN_AFTER_SECONDS=60 * 10

last_updated=None
def handle_screen_timeout():
    if last_updated is None:
        return
    now=timestamp()
    if now - last_updated > SLEEP_SCREEN_AFTER_SECONDS:
        turn_off_screen()
    elif now - last_updated > DIM_SCREEN_AFTER_SECONDS:
        dim_screen()

scheduler = BackgroundScheduler()
scheduler.add_job(handle_screen_timeout, CronTrigger(minute='*'))
scheduler.start()

last_displayed_image = None
curently_displaying_image = None
def blank_image():
    return Image.new('RGBA', (device.height, device.width), (0, 0, 0, 0))


def display_image_overlay(image):
    global last_updated
    last_updated=timestamp()
    device.show()
    brighten_screen()
    global curently_displaying_image
    img = curently_displaying_image.copy() if curently_displaying_image is not None else blank_image()
    img.paste(image, (0, 0), image)
    device.display(img.convert(device.mode))

def restore_last_image():
    global last_displayed_image
    print(f'restoring last image {last_displayed_image}')
    if last_displayed_image :
         device.display(curently_displaying_image)

def display_image_url(image_url):
    global last_updated
    global curently_displaying_image
    global last_displayed_image
    last_updated=timestamp()

    device.show()
    brighten_screen()

    if image_url != curently_displaying_image:
        response = requests.get(image_url)
        file_handle = io.BytesIO(response.content)
        img = Image.open(file_handle).convert("RGBA") \
            .resize((device.height,device.width), Image.Resampling.LANCZOS) \
            .transform(device.size, Image.Transform.AFFINE, (1, 0, 0, 0, 1, 0), Image.Resampling.BILINEAR) \
            .convert(device.mode)
        curently_displaying_image = img
        last_displayed_image = img
        device.display(img)

if __name__ == "__main__":
    try:
        image_url = 'https://media.istockphoto.com/id/961208196/photo/wild-brown-bear-cub-closeup.jpg?s=612x612&w=0&k=20&c=xj5iyHym1-Nn-L5g2hMgvsOykxnubR2fQA2NJnIugzY='
        display_image_url(image_url)
    except KeyboardInterrupt:
        pass

