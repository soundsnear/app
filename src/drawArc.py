from PIL import Image, ImageDraw, ImageFont

display_height = 128
display_width = display_height
resize_alias_factor = 2


def RAF(value):
    return value * resize_alias_factor

arc_width = RAF(11)
arc_margin = RAF(20)
arc_size = RAF(108)
number_margin = RAF(45)
TEXT_FUDGE_VERTICAL=-10

background_arc_color=(66, 66, 66)
volume_arc_color=(30, 144, 255)
text_color=(255, 252, 127)
pi_font = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font = ImageFont.truetype(pi_font, 70)


def drawVolume(percent, number):
    img = Image.new('RGBA', (RAF(display_height),
                    RAF(display_width)), (0, 0, 0, 210))
    draw = ImageDraw.Draw(img)

    draw.arc([(arc_margin, arc_margin), (arc_size, arc_size)],
             start=0, end=360, fill=background_arc_color, width=arc_width)

    if percent != 0 :
        end = ((360 * percent) + 270)
        if end < 1:
            end = 360 - end
        if end == 270:
            end = 269.9

        draw.arc([(arc_margin, arc_margin), (arc_size, arc_size)],
                start=270, end=end, fill=volume_arc_color, width=arc_width)

    text =  str(number)
    _, _, w, h = draw.textbbox((0, -TEXT_FUDGE_VERTICAL), text, font=font)
    W=RAF(display_width)
    H=RAF(display_height)
    draw.text(((W-w)/2, (H-h)/2), text, font=font, fill=text_color)

    img = img.resize((display_height, display_height), resample=Image.Resampling.LANCZOS)

    return img
