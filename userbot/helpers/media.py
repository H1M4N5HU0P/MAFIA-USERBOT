import os
from typing import Optional

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

from .utils import edit_or_reply, delete_mafia, runcmd

async def media_to_pic(event, reply):
    mediatype = media_type(reply)
    if mediatype not in ["Photo", "Round Video", "Gif", "Sticker", "Video"]:
        await delete_mafia(
            event,
            "`In the replied message. I cant extract any image to procced further reply to proper media`",
        )
        return None
    mafiamedia = await reply.download_media(file="./temp")
    mafiaevent = await edit_or_reply(event, f"`Transfiguration Time! Converting....`")
    mafiafile = os.path.join("./temp/", "meme.png")
    if mediatype == "Sticker":
        if mafiamedia.endswith(".tgs"):
            await runcmd(
                f"lottie_convert.py --frame 0 -if lottie -of png '{mafiamedia}' '{mafiafile}'"
            )
        elif mafiamedia.endswith(".webp"):
            im = Image.open(mafiamedia)
            im.save(mafiafile)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        extractMetadata(createParser(mafiamedia))
        await runcmd(f"rm -rf '{mafiafile}'")
        await take_screen_shot(mafiamedia, 0, mafiafile)
        if not os.path.exists(mafiafile):
            await delete_mafia(
                mafiaevent, f"`Sorry. I can't extract a image from this {mediatype}`"
            )
            return None
    else:
        im = Image.open(mafiamedia)
        im.save(mafiafile)
    await runcmd(f"rm -rf '{mafiamedia}'")
    return [mafiaevent, mafiafile, mediatype]


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    thumb_image_path = path or os.path.join(
        "./temp/", f"{os.path.basename(video_file)}.jpg"
    )
    command = f"ffmpeg -ss {duration} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        print(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None
