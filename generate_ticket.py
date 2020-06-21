from io import BytesIO

import requests

from PIL import Image, ImageDraw, ImageFont


TEMPLATE_PATH ='files/base.png'
FONT_PATH = 'files/Roboto-Italic.ttf'
FONT_SIZE = 30

BLACK = (0, 0, 0, 255)
NAME_OFFSET = (250, 175)
EMAIL_OFFSET = (250, 208)

AVATAR_SIZE = 100
AVATAR_OFFSET = (65, 190)


def generate_ticket(name, email):
    base = Image.open(TEMPLATE_PATH)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)

    response = requests.get(url=f'https://api.adorable.io/avatars/{AVATAR_SIZE}/{email}')
    avatar_file_like = BytesIO(response.content)
    avatar = Image.open(avatar_file_like)

    base.paste(avatar, AVATAR_OFFSET)
    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file

