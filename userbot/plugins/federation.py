# Plugin to show the feds you are banned in.
# Kangers keep credits
# By @Surv_ivor
# fixed some issues by @H1M4N5HU0P

import os
import asyncio
from telethon.errors import ChatAdminRequiredError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.users import GetFullUserRequest

from mafiabot.utils import admin_cmd, edit_or_reply, sudo_cmd
from userbot.Config import Config
from . import *

from userbot.cmdhelp import CmdHelp

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Mafia User"

mafia = bot.uid


bots = "@MissRose_bot"

BOTLOG_CHATID = Config.MAFIABOT_LOGGER

MAFIABOT_LOGGER = os.environ.get("MAFIABOT_LOGGER", None)
if MAFIABOT_LOGGER:
    MAFIABOT_LOGGER = int(MAFIABOT_LOGGER)


@bot.on(admin_cmd("fstat ?(.*)"))
@bot.on(sudo_cmd("fstat ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1):
        sysarg = event.pattern_match.group(1)
    else:
        sysarg = ""
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
        getuser = str(replied_user.user.id)
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedstat " + getuser + " " + sysarg)
                fedstat = await conv.get_response()
                if "file" in fedstat.text:
                    await fedstat.click(0)
                    reply = await conv.get_response()
                    await asyncio.sleep(5)
                    await event.client.forward_messages(event.chat_id, reply)
                else:
                    await asyncio.sleep(5)
                    await event.client.forward_messages(event.chat_id, fedstat)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_bot `and retry!")
    else:
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedstat " + sysarg)
                fedstat = await conv.get_response()
                if "file" in fedstat.text:
                    await fedstat.click(0)
                    reply = await conv.get_response()
                    await asyncio.sleep(5)
                    await event.client.forward_messages(event.chat_id, reply)
                else:
                    await asyncio.sleep(5)
                    await event.client.forward_messages(event.chat_id, fedstat)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_Bot `and try again!")


@bot.on(admin_cmd("roseinfo ?(.*)"))
@bot.on(sudo_cmd("roseinfo ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1):
        sysarg = event.pattern_match.group(1)
    else:
        sysarg = ""
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
        getuser = str(replied_user.user.id)
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/info " + getuser)
                audio = await conv.get_response()                
                await event.client.forward_messages(event.chat_id, audio)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_bot `and retry!")
    else:
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/info " + sysarg)
                audio = await conv.get_response()                
                await event.client.forward_messages(event.chat_id, audio)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_Bot `and try again!")


@bot.on(admin_cmd("fedinfo ?(.*)"))
@bot.on(sudo_cmd("fedinfo ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    sysarg = event.pattern_match.group(1)
    if sysarg == "" and not event.reply_to_msg_id:
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedinfo")
                fedinfo = await conv.get_response()
                await asyncio.sleep(1)
                await event.client.forward_messages(event.chat_id, fedinfo)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_bot `and retry!")
    else:
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedinfo " + sysarg)
                fedinfo = await conv.get_response()
                await asyncio.sleep(1)
                await event.client.forward_messages(event.chat_id, fedinfo)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_Bot `and try again!")


@bot.on(admin_cmd("myfeds ?(.*)"))
@bot.on(sudo_cmd("myfeds ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    async with event.client.conversation(bots) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/myfeds")
            myfed = await conv.get_response()
            if "file" in myfed.text:
                await myfed.click(0)
                reply = await conv.get_response()
                await asyncio.sleep(1)
                await event.client.forward_messages(event.chat_id, reply)
            else:
                await asyncio.sleep(1)
                await event.client.forward_messages(event.chat_id, myfed)
                await event.delete()
        except YouBlockedUserError:
            await event.edit("**Error:** `unblock` @MissRose_Bot `and try again!")


@bot.on(admin_cmd(pattern=r"plist ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"plist ?(.*)", allow_sudo=True))
async def get_users(show):
    await show.delete()
    if not show.text[0].isalpha() and show.text[0] not in ("/"):
        if not show.is_group:
            await show.edit("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = "id,reason"
        try:
            if not show.pattern_match.group(1):
                async for user in show.client.iter_participants(show.chat_id):
                    if not user.deleted and user.id != bot.uid:
                        mentions += f"\n{user.id},⚠️Porn / Porn Group Member//AntiPornFed #Massban🔞🛑"
                    elif user.id != bot.uid:
                        mentions += f"\n{user.id},⚠️Porn / Porn Group Member//AntiPornFed #Massban🔞🛑"
            else:
                searchq = show.pattern_match.group(1)
                async for user in show.client.iter_participants(
                    show.chat_id, search=f"{searchq}"
                ):
                    if not user.deleted and user.id != bot.uid:
                        mentions += f"\n{user.id},⚠️Porn / Porn Group Member//AntiPornFed #Massban🔞🛑"
                    elif user.id != bot.uid:
                        mentions += f"\n{user.id},⚠️Porn / Porn Group Member//AntiPornFed #Massban🔞🛑"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        file = open("userslist.csv", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            BOTLOG_CHATID,
            "userslist.csv",
            caption="Group Members in {}".format(title),
            reply_to=show.id,
        )


@bot.on(admin_cmd(pattern=r"blist ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"blist ?(.*)", allow_sudo=True))
async def get_users(show):
    await show.delete()
    if not show.text[0].isalpha() and show.text[0] not in ("/"):
        if not show.is_group:
            await show.edit("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = "id,reason"
        try:
            if not show.pattern_match.group(1):
                async for user in show.client.iter_participants(show.chat_id):
                    if not user.deleted and user.id != bot.uid:
                        mentions += f"\n{user.id},⚠️Suspicious/Btc Scammer/Fraudulent activities #Massban🛑"
                    elif user.id != bot.uid:
                        mentions += f"\n{user.id},⚠️Suspicious/Btc Scammer/Fraudulent activities #Massban🛑"
            else:
                searchq = show.pattern_match.group(1)
                async for user in show.client.iter_participants(
                    show.chat_id, search=f"{searchq}"
                ):
                    if not user.deleted and user.id != bot.uid:
                        mentions += f"\n{user.id},⚠️Suspicious/Btc Scammer/Fraudulent activities #Massban🛑"
                    elif user.id != bot.uid:
                        mentions += f"\n{user.id},⚠️Suspicious/Btc Scammer/Fraudulent activities #Massban🛑"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        file = open("userslist.csv", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            BOTLOG_CHATID,
            "userslist.csv",
            caption="Group Members in {}".format(title),
            reply_to=show.id,
        )


@bot.on(admin_cmd(pattern="bgban ?(.*)"))
@bot.on(sudo_cmd(pattern="bgban ?(.*)", allow_sudo=True))
async def _(event):
    if MAFIABOT_LOGGER is None:
        await event.edit("ENV VAR is not set. This module will not work.")
        return
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        if r.forward:
            r_sender_id = r.forward.sender_id or r.sender_id
        else:
            r_sender_id = r.sender_id
        await event.client.send_message(
            MAFIABOT_LOGGER,
            "/gban [user](tg://user?id={}) {}".format(r_sender_id, reason),
        )
    await event.delete()


@bot.on(admin_cmd(pattern="bungban ?(.*)"))
@bot.on(sudo_cmd(pattern="bungban ?(.*)", allow_sudo=True))
async def _(event):
    if MAFIABOT_LOGGER is None:
        await event.edit("ENV VAR is not set. This module will not work.")
        return
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        r_sender_id = r.sender_id
        await event.client.send_message(
            MAFIABOT_LOGGER,
            "/ungban [user](tg://user?id={}) {}".format(r_sender_id, reason),
        )
    await event.delete()


import asyncio

#  (c)2020 Telebot
#
# You may not use this plugin without proper authorship and consent from @TelebotSupport
#
import os

FBAN_GROUP_ID = os.environ.get("FBAN_GROUP_ID", None)
if FBAN_GROUP_ID:
    FBAN_GROUP_ID = int(FBAN_GROUP_ID)
EXCLUDE_FED = os.environ.get("EXCLUDE_FED", None)

# By @HeisenbergTheDanger, @its_xditya
@bot.on(admin_cmd("superfban ?(.*)"))
@bot.on(sudo_cmd("superfban ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit(f"Starting superfban By [{DEFAULTUSER}](tg://user?id={mafia}) 😈")
    fedList = []
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message, "fedlist"
            )
            await asyncio.sleep(6)
            file = open(downloaded_file_name, "r")
            lines = file.readlines()
            for line in lines:
                try:
                    fedList.append(line[:36])
                except:
                    pass
            arg = event.text.split(" ", maxsplit=2)
            if len(arg) > 2:
                FBAN = arg[1]
                REASON = arg[2]
            else:
                FBAN = arg[1]
                REASON = " #MassBanned "
        else:
            FBAN = previous_message.sender_id
            REASON = event.text.split(" ", maxsplit=1)[1]
            if REASON.strip() == "":
                REASON = " #MassBanned "
    else:
        arg = event.text.split(" ", maxsplit=2)
        if len(arg) > 2:
            FBAN = arg[1]
            REASON = arg[2]
        else:
            FBAN = arg[1]
            REASON = " #MassBanned "
    try:
        int(FBAN)
        if int(FBAN) == 1118936839 or int(FBAN) == 630654925 or int(FBAN) == 719195224 or int(FBAN) == 1212368262 or int(FBAN) == 1425926469:
            await event.edit("Something Went wrong!")
            return
    except:
        if (
            FBAN == "@Surv_ivor"
            or FBAN == "@Sur_ivor"
            or FBAN == "@HeisenbergTheDanger"
            or FBAN == "@xditya"
            or FBAN == "@Bhomik16"
            or FBAN == "@H1M4N5HU0P"
            or FBAN == "@Pacifist_Op"
    
        ):
            await event.edit("Hey Nigga, You can't superfban your father😏")
            return
    if FBAN_GROUP_ID:
        chat = FBAN_GROUP_ID
    else:
        chat = await event.get_chat()
    if not len(fedList):
        for a in range(3):
            async with event.client.conversation("@MissRose_bot") as bot_conv:
                await bot_conv.send_message("/start")
                await bot_conv.send_message("/myfeds")
                await asyncio.sleep(3)
                response = await bot_conv.get_response()
                await asyncio.sleep(3)
                if "make a file" in response.text:
                    await asyncio.sleep(6)
                    await response.click(0)
                    await asyncio.sleep(6)
                    fedfile = await bot_conv.get_response()
                    await asyncio.sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await event.client.download_media(
                            fedfile, "fedlist"
                        )
                        await asyncio.sleep(6)
                        file = open(downloaded_file_name, "r")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except:
                                pass
                    else:
                        return
                if len(fedList) == 0:
                    await event.edit(f"Something went wrong. Retrying ({a+1}/3)...")
                else:
                    break
        else:
            await event.edit(f"Error")
        if "You can only use fed commands once every 5 minutes" in response.text:
            await event.edit("Try again after 5 mins.")
            return
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True

            elif In:
                tempFedId += x
        if len(fedList) == 0:
            await event.edit("Something went wrong.")
            return
    await event.edit(f"Fbaning in {len(fedList)} feds by [{DEFAULTUSER}](tg://user?id={mafia}) 😈")
    try:
        await event.client.send_message(chat, f"/start")
    except:
        await event.edit("FBAN_GROUP_ID is incorrect.")
        return
    await asyncio.sleep(3)
    if EXCLUDE_FED:
        excludeFed = EXCLUDE_FED.split("|")
        for n in range(len(excludeFed)):
            excludeFed[n] = excludeFed[n].strip()
    exCount = 0
    for fed in fedList:
        if EXCLUDE_FED and fed in excludeFed:
            await event.client.send_message(chat, f"{fed} Excluded.")
            exCount += 1
            continue
        await event.client.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await event.client.send_message(chat, f"/fban {FBAN} {REASON} \n\n#SUPERFBAN_BY_MAFIABOT")
        await asyncio.sleep(3)
    await event.edit(f"SuperFBan Completed. Affected {len(fedList) - exCount} feds by [{DEFAULTUSER}](tg://user?id={mafia}) 😈")


# By @HeisenbergTheDanger, @its_xditya
@bot.on(admin_cmd("superunfban ?(.*)"))
@bot.on(sudo_cmd("superunfban ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit(f"Starting a superunfban by [{DEFAULTUSER}](tg://user?id={mafia}) ⚡")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        FBAN = previous_message.sender_id
    else:
        FBAN = event.pattern_match.group(1)

    if FBAN_GROUP_ID:
        chat = FBAN_GROUP_ID
    else:
        chat = await event.get_chat()
    fedList = []
    for a in range(3):
        async with event.client.conversation("@MissRose_bot") as bot_conv:
            await bot_conv.send_message("/start")
            await bot_conv.send_message("/myfeds")
            response = await bot_conv.get_response()
            if "make a file" in response.text:
                await asyncio.sleep(1)
                await response.click(0)
                fedfile = await bot_conv.get_response()
                if fedfile.media:
                    downloaded_file_name = await event.client.download_media(
                        fedfile, "fedlist"
                    )
                    file = open(downloaded_file_name, "r")
                    lines = file.readlines()
                    for line in lines:
                        fedList.append(line[:36])
                else:
                    return
                if len(fedList) == 0:
                    await event.edit(f"Something went wrong. Retrying ({a+1}/3)...")
                else:
                    break
    else:
        await event.edit(f"Error")
    if "You can only use fed commands once every 5 minutes" in response.text:
        await event.edit("Try again after 5 mins.")
        return
    In = False
    tempFedId = ""
    for x in response.text:
        if x == "`":
            if In:
                In = False
                fedList.append(tempFedId)
                tempFedId = ""
            else:
                In = True

        elif In:
            tempFedId += x

    await event.edit(f"UnFbaning in {len(fedList)} feds by [{DEFAULTUSER}](tg://user?id={mafia}) ⚡")
    try:
        await event.client.send_message(chat, f"/start")
    except:
        await event.edit("FBAN_GROUP_ID is incorrect.")
        return
    await asyncio.sleep(3)
    for fed in fedList:
        await event.client.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await event.client.send_message(chat, f"/unfban {FBAN} \n\n#SUPERUNFBAN_BY_MAFIABOT")
        await asyncio.sleep(3)
    await event.edit(f"SuperUnFBan Completed. Affected {len(fedList)} feds by [{DEFAULTUSER}](tg://user?id={mafia}) ⚡")
    
CmdHelp("federation").add_command(
  "fstat", "<username/user id>", "to get fban info"
).add_command(
  "roseinfo", "<username/user id>", "to get user info"
).add_command(
  "fedinfo", "<fed id>", "to get fed info"
).add_command(
  "myfeds", None, "to get my fed admin list file"
).add_command(
  "plist", None, "to get group porn list file in your logs channel"
).add_command(
  "blist", None, "to get group blacklist file in your logs channel"
).add_command(
  "bgban", "<username/user id> <reason>", "to bgban user"
).add_command(
  "bungban", "<username/user id> <reason>", "to unbgban "
).add_command(
  "superfban", "<username/user id> <reason>", "to superfban in your admin feds"
).add_command(
  "superunfban", "<username/user id> <reason> <text>", "to superunfban in your admin feds"
).add()