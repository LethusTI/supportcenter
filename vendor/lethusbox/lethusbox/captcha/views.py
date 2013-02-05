
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.http import HttpResponse, Http404
from mongoengine.django.shortcuts import get_document_or_404

import os
import random
import re
import tempfile

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import Image
    import ImageDraw
    import ImageFont

NON_DIGITS_RX = re.compile('[^\d]')
DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
CAPTCHA_FONT_PATH = os.path.join(DATA_PATH, "font.ttf")

from .models import CaptchaStore
from .constants import *

def noise_arcs(draw, image):
    size = image.size
    draw.arc([-20, -20, size[0], 20], 0, 295, fill=CAPTCHA_FOREGROUND_COLOR)
    draw.line([-20, 20, size[0] + 20, size[1] - 20], fill=CAPTCHA_FOREGROUND_COLOR)
    draw.line([-20, 0, size[0] + 20, size[1]], fill=CAPTCHA_FOREGROUND_COLOR)
    return draw

def noise_dots(draw, image):
    size = image.size
    for p in range(int(size[0] * size[1] * 0.1)):
        draw.point((random.randint(0, size[0]), random.randint(0, size[1])), fill=CAPTCHA_FOREGROUND_COLOR)
    return draw

def post_smooth(image):
    try:
        import ImageFilter
    except ImportError:
        from PIL import ImageFilter
    return image.filter(ImageFilter.SMOOTH)

def captcha_image(request, key):
    store = get_document_or_404(CaptchaStore, hashkey=key)
    text = store.response

    font = ImageFont.truetype(CAPTCHA_FONT_PATH, CAPTCHA_FONT_SIZE)

    size = font.getsize(text)
    size = (size[0] * 2, int(size[1] * 1.2))
    image = Image.new('RGB', size, CAPTCHA_BACKGROUND_COLOR)

    try:
        PIL_VERSION = int(NON_DIGITS_RX.sub('', Image.VERSION))
    except:
        PIL_VERSION = 116
    xpos = 2

    charlist = []

    for char in text:
        if char in CAPTCHA_PUNCTUATION and len(charlist) >= 1:
            charlist[-1] += char
        else:
            charlist.append(char)

    for char in charlist:
        fgimage = Image.new('RGB', size, CAPTCHA_FOREGROUND_COLOR)
        charimage = Image.new('L', font.getsize(' %s ' % char), '#000000')
        chardraw = ImageDraw.Draw(charimage)
        chardraw.text((0, 0), ' %s ' % char, font=font, fill='#ffffff')

        if CAPTCHA_LETTER_ROTATION:
            if PIL_VERSION >= 116:
                charimage = charimage.rotate(random.randrange(*CAPTCHA_LETTER_ROTATION), expand=0, resample=Image.BICUBIC)

            else:
                charimage = charimage.rotate(random.randrange(*CAPTCHA_LETTER_ROTATION), resample=Image.BICUBIC)

        charimage = charimage.crop(charimage.getbbox())
        maskimage = Image.new('L', size)

        maskimage.paste(charimage, (xpos, 4, xpos + charimage.size[0], 4 + charimage.size[1]))
        size = maskimage.size
        image = Image.composite(fgimage, image, maskimage)
        xpos = xpos + 2 + charimage.size[0]

    image = image.crop((0, 0, xpos + 1, size[1]))
    draw = ImageDraw.Draw(image)

    draw = noise_arcs(draw, image)
    draw = noise_dots(draw, image)
    image = post_smooth(image)

    out = StringIO()
    image.save(out, "PNG")
    out.seek(0)

    response = HttpResponse()
    response['Content-Type'] = 'image/png'
    response.write(out.read())

    return response
