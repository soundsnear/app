from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1351
from pathlib import Path
from PIL import Image

root_image_path="/home/tyler/playground/luma.examples/examples/images"
filename="ab67616d00001e02cdf367607728e48fc580a6f9"
filename="pi_logo.png"

def main():
    img_path = str(Path(__file__).resolve().parent.joinpath(root_image_path, filename))
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)
    device.display(logo)

    return
    background = Image.new("RGBA", device.size, "white")
    posn = ((device.width - logo.width) // 2, 0)
    times=0
    while True:
        for angle in range(0, 360, 2):
            rot = logo.rotate(angle, resample=Image.BILINEAR)
            img = Image.composite(logo, fff, rot)
            background.paste(logo, posn)
            if times == 0:
              device.display(background.convert(device.mode))
              times=1

if __name__ == "__main__":
    try:
        serial = spi(device=1, port=0, gpio_DC=27, gpio_RST=22, bus_speed_hz=16000000)
        device = ssd1351(serial, bgr=True, width=128, height=128)
        main()
    except KeyboardInterrupt:
        pass

