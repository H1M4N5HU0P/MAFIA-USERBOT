# Making it easy....
# thanks to @ranger_op for idea
# codes by @mrconfused
# catuserbot
# thanks to catuserbot
import os

try:
    pass
except:
    os.system("pip install colour")
import asyncio
import re
import time

import PIL.ImageOps
import requests
from bs4 import BeautifulSoup
from PIL import Image
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import Channel, PollAnswer
from validators.url import url
from emoji import get_emoji_regexp

MARGINS = [50, 150, 250, 350, 450]


# For using gif , animated stickers and videos in some parts , this
# function takes  take a screenshot and stores ported from userge

def utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset

# gban

async def admin_groups(mafia):
    mafiagroups = []
    async for dialog in mafia.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            mafiagroups.append(entity.id)
    return mafiagroups

async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name,
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        logger.info(e_response)
        logger.info(t_response)
        return None


# https://github.com/Nekmo/telegram-upload/blob/master/telegram_upload/video.py#L26


async def cult_small_video(video_file, output_directory, start_time, end_time):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + "/" + str(round(time.time())) + ".mp4"
    file_genertor_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name,
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        logger.info(e_response)
        logger.info(t_response)
        return None


async def make_gif(event, file):
    chat = "@tgstogifbot"
    async with event.client.conversation(chat) as conv:
        try:
            await silently_send_message(conv, "/start")
            await event.client.send_file(chat, file)
            response = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if response.text.startswith("Send me an animated sticker!"):
                return "`This file is not supported`"
            response = response if response.media else await conv.get_response()
            mafiaresponse = response if response.media else await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            mafiafile = await event.client.download_media(mafiaresponse, "./temp")
            return await unzip(mafiafile)
        except YouBlockedUserError:
            return "Unblock @tgstogifbot"


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


async def thumb_from_audio(audio_path, output):
    await runcmd(f"ffmpeg -i {audio_path} -filter:v scale=500:500 -an {output}")


async def simpmusic(simp, QUALITY):
    search = simp
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }
    html = requests.get(
        "https://www.youtube.com/results?search_query=" + search, headers=headers
    ).text
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        if "/watch?v=" in link.get("href"):
            # May change when Youtube Website may get updated in the future.
            video_link = link.get("href")
            break
    video_link = "http://www.youtube.com/" + video_link
    command = (
        "youtube-dl --extract-audio --audio-format mp3 --audio-quality "
        + QUALITY
        + " "
        + video_link
    )
    os.system(command)


song_dl = "youtube-dl --force-ipv4 --write-thumbnail -o './temp/%(title)s.%(ext)s' --extract-audio --audio-format mp3 --audio-quality {QUALITY} {video_link}"
thumb_dl = "youtube-dl --force-ipv4 -o './temp/%(title)s.%(ext)s' --write-thumbnail --skip-download {video_link}"
video_dl = "youtube-dl --force-ipv4 --write-thumbnail  -o './temp/%(title)s.%(ext)s' -f '[filesize<20M]' {video_link}"
name_dl = (
    "youtube-dl --force-ipv4 --get-filename -o './temp/%(title)s.%(ext)s' {video_link}"
)


async def simpmusicvideo(simp):
    search = simp
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }
    html = requests.get(
        "https://www.youtube.com/results?search_query=" + search, headers=headers
    ).text
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        if "/watch?v=" in link.get("href"):
            # May change when Youtube Website may get updated in the future.
            video_link = link.get("href")
            break
    video_link = "http://www.youtube.com/" + video_link
    command = 'youtube-dl -f "[filesize<20M]" ' + video_link
    os.system(command)

async def unzip(downloaded_file_name):
    with zipfile.ZipFile(downloaded_file_name, "r") as zip_ref:
        zip_ref.extractall("./temp")
    downloaded_file_name = os.path.splitext(downloaded_file_name)[0]
    return f"{downloaded_file_name}.gif"

# convertion..


def convert_toimage(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("./temp/temp.jpg", "jpeg")
    os.remove(image)
    return "./temp/temp.jpg"


async def convert_tosticker(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("./temp/temp.webp", "webp")
    os.remove(image)
    return "./temp/temp.webp"


async def invert_colors(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(endname)


async def flip_image(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.flip(image)
    inverted_image.save(endname)


async def grayscale(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.grayscale(image)
    inverted_image.save(endname)


async def mirror_file(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.mirror(image)
    inverted_image.save(endname)


async def solarize(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.solarize(image, threshold=128)
    inverted_image.save(endname)


# pranks....
# source - https://nekobot.xyz/api


async def iphonex(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={text}").json()
    h1m4n5hu0p = r.get("message")
    mafiaurl = url(h1m4n5hu0p)
    if not mafiaurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(h1m4n5hu0p).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def baguette(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=baguette&url={text}"
    ).json()
    h1m4n5hu0p = r.get("message")
    mafiaurl = url(h1m4n5hu0p)
    if not mafiaurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(h1m4n5hu0p).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def threats(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=threats&url={text}").json()
    h1m4n5hu0p = r.get("message")
    mafiaurl = url(h1m4n5hu0p)
    if not mafiaurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(h1m4n5hu0p).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def lolice(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=lolice&url={text}").json()
    h1m4n5hu0p = r.get("message")
    mafiaurl = url(h1m4n5hu0p)
    if not mafiaurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(h1m4n5hu0p).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trash(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=trash&url={text}").json()
    h1m4n5hu0p = r.get("message")
    mafiaurl = url(h1m4n5hu0p)
    if not mafiaurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(h1m4n5hu0p).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def awooify(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=awooify&url={text}").json()
    h1m4n5hu0p = r.get("message")
    mafiaurl = url(h1m4n5hu0p)
    if not mafiaurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(h1m4n5hu0p).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trap(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trap&name={text1}&author={text2}&image={text3}"
    ).json()
    h1m4n5hu0p = r.get("message")
    mafiaurl = url(h1m4n5hu0p)
    if not mafiaurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(h1m4n5hu0p).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def phcomment(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=phcomment&image={text1}&text={text2}&username={text3}"
    ).json()
    h1m4n5hu0p = r.get("message")
    mafiaurl = url(h1m4n5hu0p)
    if not mafiaurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(h1m4n5hu0p).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


# tweets...
# source - https://nekobot.xyz/api


async def trumptweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def changemymind(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def kannagen(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


async def moditweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=narendramodi"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def miatweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=miakhalifa"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"

async def dani(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=dani_daniels___"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"

async def papputweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=rahulgandhi"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def sunnytweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=sunnyleone"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def sinstweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=johnnysins"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def taklatweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=Mahatma_Gandhi_"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


# no offense pliz -_-


async def tweets(text1, text2):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}"
    ).json()
    wew = r.get("message")
    hburl = url(wew)
    if not hburl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


# sticker text

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)



# http://effbot.org/imagingbook/imageops.html
# https://stackoverflow.com/questions/2498875/how-to-invert-colors-of-image-with-pil-python-imaging/38378828


async def invert_colors(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(endname)


async def flip_image(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.flip(image)
    inverted_image.save(endname)


async def grayscale(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.grayscale(image)
    inverted_image.save(endname)


async def mirror_file(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.mirror(image)
    inverted_image.save(endname)


async def solarize(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.solarize(image, threshold=128)
    inverted_image.save(endname)


async def add_frame(imagefile, endname, x, color):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.expand(image, border=x, fill=color)
    inverted_image.save(endname)


async def crop(imagefile, endname, x):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.crop(image, border=x)
    inverted_image.save(endname)


# for stickertxt
async def waifutxt(text, chat_id, reply_to_id, bot, borg):
    animus = [
        0,
        1,
        2,
        3,
        4,
        9,
        15,
        20,
        22,
        27,
        29,
        32,
        33,
        34,
        37,
        38,
        41,
        42,
        44,
        45,
        47,
        48,
        51,
        52,
        53,
        55,
        56,
        57,
        58,
        61,
        62,
        63,
    ]
    sticcers = await bot.inline_query("stickerizerbot", f"#{choice(animus)}{text}")
    mafia = await sticcers[0].click("me", hide_via=True)
    if mafia:
        await bot.send_file(int(chat_id), mafia, reply_to=reply_to_id)
        await mafia.delete()


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in Config.SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id


async def clippy(borg, msg, chat_id, reply_to_id):
    chat = "@clippy"
    async with borg.conversation(chat) as conv:
        try:
            msg = await conv.send_file(msg)
            pic = await conv.get_response()
            await borg.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await kakashi.edit("Please unblock @clippy and try again")
            return
        await borg.send_file(
            chat_id,
            pic,
            reply_to=reply_to_id,
        )
    await borg.delete_messages(conv.chat_id, [msg.id, pic.id])


def higlighted_text(
    input_img,
    text,
    output_img,
    background="black",
    foreground="white",
    transparency=255,
    align="center",
    direction=None,
    text_wrap=2,
    font_name=None,
    font_size=60,
    linespace="+2",
    rad=20,
    position=(0, 0),
):
    templait = Image.open(input_img)
    # resize image
    source_img = templait.convert("RGBA").resize((1024, 1024))
    w, h = source_img.size
    if font_name is None:
        font_name = "userbot/helpers/styles/impact.ttf"
    font = ImageFont.truetype(font_name, font_size)
    ew, eh = position
    # get text size
    tw, th = font.getsize(text)
    width = 50 + ew
    hight = 30 + eh
    # wrap the text & save in a list
    mask_size = int((w / text_wrap) + 50)
    input_text = "\n".join(wrap(text, int((40.0 / w) * mask_size)))
    list_text = input_text.splitlines()
    # create image with correct size and black background
    if direction == "upwards":
        list_text.reverse()
        operator = "-"
        hight = h - (th + int(th / 1.2)) + eh
    else:
        operator = "+"
    for i, items in enumerate(list_text):
        x, y = (font.getsize(list_text[i])[0] + 50, int(th * 2 - (th / 2)))
        # align masks on the image....left,right & center
        if align == "center":
            width_align = "((mask_size-x)/2)"
        elif align == "left":
            width_align = "0"
        elif align == "right":
            width_align = "(mask_size-x)"
        clr = ImageColor.getcolor(background, "RGBA")
        if transparency == 0:
            mask_img = Image.new(
                "RGBA", (x, y), (clr[0], clr[1], clr[2], 0)
            )  # background
            mask_draw = ImageDraw.Draw(mask_img)
            mask_draw.text((25, 8), list_text[i], foreground, font=font)
        else:
            mask_img = Image.new(
                "RGBA", (x, y), (clr[0], clr[1], clr[2], transparency)
            )  # background
            # put text on mask
            mask_draw = ImageDraw.Draw(mask_img)
            mask_draw.text((25, 8), list_text[i], foreground, font=font)
            # remove corner (source- https://stackoverflow.com/questions/11287402/how-to-round-corner-a-logo-without-white-backgroundtransparent-on-it-using-pi)
            circle = Image.new("L", (rad * 2, rad * 2), 0)
            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, rad * 2, rad * 2), transparency)
            alpha = Image.new("L", mask_img.size, transparency)
            mw, mh = mask_img.size
            alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
            alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, mh - rad))
            alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (mw - rad, 0))
            alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (mw - rad, mh - rad))
            mask_img.putalpha(alpha)
        # put mask_img on source image & trans remove the corner white
        trans = Image.new("RGBA", source_img.size)
        trans.paste(
            mask_img,
            (
                (int(width) + int(eval(f"{width_align}"))),
                (eval(f"{hight} {operator}({y*i}+({int(linespace)*i}))")),
            ),
        )
        source_img = Image.alpha_composite(source_img, trans)
    source_img.save(output_img, "png")


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return get_emoji_regexp().sub("", inputString)


