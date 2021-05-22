# modified and developed by @mrconfused
import html
import asyncio
import base64
import io
import math
import random
import urllib.request
import cloudscraper
from os import remove
from userbot.utils import admin_cmd, sudo_cmd, delete_mafia, edit_or_reply
import emoji as mafiaemoji
import requests
from userbot.cmdhelp import CmdHelp
from bs4 import BeautifulSoup as bs
from PIL import Image
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaPhoto,
)

combot_stickers_url = "https://combot.org/telegram/stickers?q="

EMOJI_SEN = [
    "Можно отправить несколько смайлов в одном сообщении, однако мы рекомендуем использовать не больше одного или двух на каждый стикер.",
    "You can list several emoji in one message, but I recommend using no more than two per sticker",
    "Du kannst auch mehrere Emoji eingeben, ich empfehle dir aber nicht mehr als zwei pro Sticker zu benutzen.",
    "Você pode listar vários emojis em uma mensagem, mas recomendo não usar mais do que dois por cada sticker.",
    "Puoi elencare diverse emoji in un singolo messaggio, ma ti consiglio di non usarne più di due per sticker.",
]

KANGING_STR = [
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!..",
    "hehe me stel ur stikér\nhehe.",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so my pacc looks cool",
    "Imprisoning this sticker...",
    "Mr.Steal Your Sticker is stealing this sticker... ",
]


def verify_cond(mafiaarray, text):
    return any(i in text for i in mafiaarray)


def pack_name(userid, pack, is_anim):
    if is_anim:
        return f"mafiauserbot_{userid}_{pack}_anim"
    return f"mafiauserbot_{userid}_{pack}"


def char_is_emoji(character):
    return character in mafiaemoji.UNICODE_EMOJI["en"]


def pack_nick(username, pack, is_anim):
    if Config.CUSTOM_STICKER_PACK_NAME:
        if is_anim:
            packnick = f"{Config.CUSTOM_STICKER_PACK_NAME} Vol.{pack} (Animated)"
        else:
            packnick = f"{Config.CUSTOM_STICKER_PACK_NAME} Vol.{pack}"
    else:
        if is_anim:
            packnick = f"@{username} Vol.{pack} (Animated)"
        else:
            packnick = f"@{username} Vol.{pack}"
    return packnick


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)
    return image


async def newpacksticker(
    mafiaevent,
    conv,
    cmd,
    args,
    pack,
    packnick,
    stfile,
    emoji,
    packname,
    is_anim,
    otherpack=False,
    pkang=False,
):
    await conv.send_message(cmd)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packnick)
    await conv.get_response()
    mafia = base64.b64decode("OHg5WlAzUWhfd1UyWW1FMQ==")
    await args.client.send_read_acknowledge(conv.chat_id)
    if is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        remove("AnimatedSticker.tgs")
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
    rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.text):
        await mafiaevent.edit(
            f"Failed to add sticker, use @Stickers bot to add the sticker manually.\n**error :**{rsp}"
        )
        return
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/publish")
    if is_anim:
        await conv.get_response()
        await conv.send_message(f"<{packnick}>")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message("/skip")
    try:
        mafia = Get(mafia)
        await mafiaevent.client(mafia)
    except BaseException:
        pass
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message(packname)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return otherpack, packname, emoji
    return pack, packname


async def add_to_pack(
    mafiaevent,
    conv,
    args,
    packname,
    pack,
    userid,
    username,
    is_anim,
    stfile,
    emoji,
    cmd,
    pkang=False,
):
    await conv.send_message("/addsticker")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packname)
    x = await conv.get_response()
    while ("50" in x.text) or ("120" in x.text):
        try:
            val = int(pack)
            pack = val + 1
        except ValueError:
            pack = 1
        packname = pack_name(userid, pack, is_anim)
        packnick = pack_nick(username, pack, is_anim)
        await mafiaevent.edit(
            f"`Switching to Pack {str(pack)} due to insufficient space`"
        )
        await conv.send_message(packname)
        x = await conv.get_response()
        if x.text == "Invalid pack selected.":
            return await newpacksticker(
                mafiaevent,
                conv,
                cmd,
                args,
                pack,
                packnick,
                stfile,
                emoji,
                packname,
                is_anim,
                otherpack=True,
                pkang=pkang,
            )
    if is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        remove("AnimatedSticker.tgs")
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
    rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.text):
        await mafiaevent.edit(
            f"Failed to add sticker, use @Stickers bot to add the sticker manually.\n**error :**{rsp}"
        )
        return
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/done")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return packname, emoji
    return pack, packname


@bot.on(admin_cmd(outgoing=True, pattern="kang ?(.*)"))
@bot.on(sudo_cmd(pattern="kang ?(.*)", allow_sudo=True))
async def kang(args):
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None
    message = await args.get_reply_message()
    user = await args.client.get_me()
    if not user.username:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            username = user.first_name
        except UnicodeDecodeError:
            username = f"mafia_{user.id}"
    else:
        username = user.username
    userid = user.id
    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            mafiaevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await args.client.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            mafiaevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await args.client.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            mafiaevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            await args.client.download_file(
                message.media.document, "AnimatedSticker.tgs"
            )

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await delete_mafia(args, "`Unsupported File!`")
            return
    else:
        await delete_mafia(args, "`I can't kang that...`")
        return
    if photo:
        splat = ("".join(args.text.split(maxsplit=1)[1:])).split()
        emoji = emoji if emojibypass else "馃槀"
        pack = 1
        if len(splat) == 2:
            if char_is_emoji(splat[0][0]):
                if char_is_emoji(splat[1][0]):
                    return await mafiaevent.edit("check `.info stickers`")
                pack = splat[1]  # User sent both
                emoji = splat[0]
            elif char_is_emoji(splat[1][0]):
                pack = splat[0]  # User sent both
                emoji = splat[1]
            else:
                return await mafiaevent.edit("check `.info stickers`")
        elif len(splat) == 1:
            if char_is_emoji(splat[0][0]):
                emoji = splat[0]
            else:
                pack = splat[0]
        packnick = pack_nick(username, pack, is_anim)
        packname = pack_name(userid, pack, is_anim)
        cmd = "/newpack"
        stfile = io.BytesIO()
        if is_anim:
            cmd = "/newanimated"
        else:
            image = await resize_photo(photo)
            stfile.name = "sticker.png"
            image.save(stfile, "PNG")
        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")
        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with args.client.conversation("Stickers") as conv:
                packname, emoji = await add_to_pack(
                    mafiaevent,
                    conv,
                    args,
                    packname,
                    pack,
                    userid,
                    username,
                    is_anim,
                    stfile,
                    emoji,
                    cmd,
                )
            await delete_mafia(
                mafiaevent,
                f"`Sticker kanged successfully!\
                    \nYour Pack is` [here](t.me/addstickers/{packname}) `and emoji for the kanged sticker is {emoji}`",
                parse_mode="md",
                time=10,
            )
        else:
            await mafiaevent.edit("`Brewing a new Pack...`")
            async with args.client.conversation("Stickers") as conv:
                otherpack, packname, emoji = await newpacksticker(
                    mafiaevent,
                    conv,
                    cmd,
                    args,
                    pack,
                    packnick,
                    stfile,
                    emoji,
                    packname,
                    is_anim,
                )
            if otherpack:
                await delete_mafia(
                    mafiaevent,
                    f"`Sticker kanged to a Different Pack !\
                    \nAnd Newly created pack is` [here](t.me/addstickers/{packname}) `and emoji for the kanged sticker is {emoji}`",
                    parse_mode="md",
                    time=10,
                )
            else:
                await delete_mafia(
                    mafiaevent,
                    f"`Sticker kanged successfully!\
                    \nYour Pack is` [here](t.me/addstickers/{packname}) `and emoji for the kanged sticker is {emoji}`",
                    parse_mode="md",
                    time=10,
                )


@bot.on(admin_cmd(pattern="pkang ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="pkang ?(.*)", allow_sudo=True))
async def pack_kang(event):
    if event.fwd_from:
        return
    user = await event.client.get_me()
    if user.username:
        username = user.username
    else:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            username = user.first_name
        except UnicodeDecodeError:
            username = f"mafia_{user.id}"
    photo = None
    userid = user.id
    is_anim = False
    emoji = None
    reply = await event.get_reply_message()
    mafia = base64.b64decode("OHg5WlAzUWhfd1UyWW1FMQ==")
    if not reply or media_type(reply) is None or media_type(reply) != "Sticker":
        return await delete_mafia(
            event, "`reply to any sticker to send all stickers in that pack`"
        )
    try:
        stickerset_attr = reply.document.attributes[1]
        mafiaevent = await edit_or_reply(
            event, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        return await delete_mafia(
            event, "`This is not a sticker. Reply to a sticker.`", 5
        )
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                )
            )
        )
    except Exception:
        return await delete_mafia(
            mafiaevent,
            "`I guess this sticker is not part of any pack. So, i cant kang this sticker pack try kang for this sticker`",
        )
    kangst = 1
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            )
        )
    )
    noofst = get_stickerset.set.count
    blablapacks = []
    blablapacknames = []
    pack = None
    for message in reqd_sticker_set.documents:
        if "image" in message.mime_type.split("/"):
            await edit_or_reply(
                mafiaevent,
                f"`This sticker pack is kanging now . Status of kang process : {kangst}/{noofst}`",
            )
            photo = io.BytesIO()
            await event.client.download_file(message, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.attributes
            ):
                emoji = message.attributes[1].alt
        elif "tgsticker" in message.mime_type:
            await edit_or_reply(
                mafiaevent,
                f"`This sticker pack is kanging now . Status of kang process : {kangst}/{noofst}`",
            )
            await event.client.download_file(message, "AnimatedSticker.tgs")
            attributes = message.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            is_anim = True
            photo = 1
        else:
            await delete_mafia(mafiaevent, "`Unsupported File!`")
            return
        if photo:
            splat = ("".join(event.text.split(maxsplit=1)[1:])).split()
            emoji = emoji or "馃槀"
            if pack is None:
                pack = 1
                if len(splat) == 1:
                    pack = splat[0]
                elif len(splat) > 1:
                    return await delete_mafia(
                        mafiaevent,
                        "`Sorry the given name cant be used for pack or there is no pack with that name`",
                    )
            try:
                mafia = Get(mafia)
                await event.client(mafia)
            except BaseException:
                pass
            packnick = pack_nick(username, pack, is_anim)
            packname = pack_name(userid, pack, is_anim)
            cmd = "/newpack"
            stfile = io.BytesIO()
            if is_anim:
                cmd = "/newanimated"
            else:
                image = await resize_photo(photo)
                stfile.name = "sticker.png"
                image.save(stfile, "PNG")
            response = urllib.request.urlopen(
                urllib.request.Request(f"http://t.me/addstickers/{packname}")
            )
            htmlstr = response.read().decode("utf8").split("\n")
            if (
                "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
                in htmlstr
            ):
                async with event.client.conversation("Stickers") as conv:
                    pack, mafiapackname = await newpacksticker(
                        mafiaevent,
                        conv,
                        cmd,
                        event,
                        pack,
                        packnick,
                        stfile,
                        emoji,
                        packname,
                        is_anim,
                        pkang=True,
                    )
            else:
                async with event.client.conversation("Stickers") as conv:
                    pack, mafiapackname = await add_to_pack(
                        mafiaevent,
                        conv,
                        event,
                        packname,
                        pack,
                        userid,
                        username,
                        is_anim,
                        stfile,
                        emoji,
                        cmd,
                        pkang=True,
                    )
            if mafiapackname not in blablapacks:
                blablapacks.append(mafiapackname)
                blablapacknames.append(pack)
        kangst += 1
        await asyncio.sleep(2)
    result = "`This sticker pack is kanged into the following your sticker pack(s):`\n"
    for i in enumerate(blablapacks):
        result += "  鈥?  [pack {}](t.me/addstickers/{})".format(blablapacknames[i], blablapacks[i])
    await mafiaevent.edit(result)


@bot.on(admin_cmd(pattern="stkrinfo$", outgoing=True))
@bot.on(sudo_cmd(pattern="stkrinfo$", allow_sudo=True))
async def get_pack_info(event):
    if not event.is_reply:
        await delete_mafia(event, "`I can't fetch info from nothing, can I ?!`", 5)
        return
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await delete_mafia(event, "`Reply to a sticker to get the pack details`", 5)
        return
    try:
        stickerset_attr = rep_msg.document.attributes[1]
        mafiaevent = await edit_or_reply(
            event, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        await delete_mafia(event, "`This is not a sticker. Reply to a sticker.`", 5)
        return
    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        await mafiaevent.edit("`This is not a sticker. Reply to a sticker.`")
        return
    get_stickerset = await event.client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    OUTPUT = (
        f"**Sticker Title:** `{get_stickerset.set.title}\n`"
        f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n"
        f"**Official:** `{get_stickerset.set.official}`\n"
        f"**Archived:** `{get_stickerset.set.archived}`\n"
        f"**Stickers In Pack:** `{get_stickerset.set.count}`\n"
        f"**Emojis In Pack:**\n{' '.join(pack_emojis)}"
    )
    await mafiaevent.edit(OUTPUT)


@bot.on(admin_cmd(pattern="stickers ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="stickers ?(.*)", allow_sudo=True))
async def cb_sticker(event):
    split = event.pattern_match.group(1)
    if not split:
        await delete_mafia(event, "`Provide some name to search for pack.`", 5)
        return
    mafiaevent = await edit_or_reply(event, "`Searching sticker packs....`")
    scraper = cloudscraper.create_scraper()
    text = scraper.get(combot_stickers_url + split).text
    soup = bs(text, "lxml")
    results = soup.find_all("div", {"class": "sticker-pack__header"})
    if not results:
        await delete_mafia(mafiaevent, "`No results found :(.`", 5)
        return
    reply = f"**Sticker packs found for {split} are :**"
    for pack in results:
        if pack.button:
            packtitle = (pack.find("div", "sticker-pack__title")).get_text()
            packlink = (pack.a).get("href")
            packid = (pack.button).get("data-popup")
            reply += f"\n **鈥? ID: **`{packid}`\n [{packtitle}]({packlink})"
    await mafiaevent.edit(reply)


CmdHelp("stickers").add_command(
  "kang", "<emoji> <number>", "Adds the sticker to desired pack with a custom emoji of your choice. If emoji is not mentioned then default is 馃槑. And if number is not mentioned then Pack will go on serial wise. \n  锟??(1 pack = 120 non-animated stickers)\n  锟??(1 pack = 50 animated stickers)"
).add_command( 
  "pkang", "<number>", "Kang's the entire sticker pack of replied sticker to the specified pack."
).add_command(
  "stickers", "<name>", "shows you the list of non-animated sticker packs with that name."
).add_command(
  "stkrinfo", "<reply to sticker>", "Gets all the info of the sticker pack."
).add()
