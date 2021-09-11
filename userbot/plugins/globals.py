import asyncio
import random
import html

from telethon import events
from telethon.events import ChatAction
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, ChannelParticipantsAdmins, ChatBannedRights, MessageEntityMentionName, MessageMediaPhoto
from telethon.errors.rpcerrorlist import UserIdInvalidError, MessageTooLongError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, EditPhotoRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location

from userbot.helpers.extras import delete_mafia as eod
from userbot.helpers.extras import edit_or_reply as eor

from userbot.plugins.sql_helper.gban_sql import is_gbanned, gbaner, ungbaner, all_gbanned
from userbot.plugins.sql_helper.gvar_sql import gvarstat
from userbot.plugins.sql_helper import gmute_sql as gsql
from . import *


MAFIA_NAME = str(ALIVE_NAME) if ALIVE_NAME else "Mafia User"
h1m4n5hu0p = bot.uid

gbanpic = "./H1M4N5HU0P/mafiabot_logo.jpg"
gmutepic = "./H1M4N5HU0P/mafiabot_logo.jpg"

async def get_full_user(event):  
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await eor(event, "Need a user to do this...")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await eor(event, f"**ERROR !!**\n\n`{str(err)}`")           
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj



@bot.on(admin_cmd(pattern="ggpromote ?(.*)"))
@bot.on(sudo_cmd(pattern="gpromote ?(.*)", allow_sudo=True))
async def _(mafiaevent):
    i = 0
    sender = await mafiaevent.get_sender()
    me = await mafiaevent.client.get_me()
    mafia = await eor(mafiaevent, "`Promoting globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await mafiaevent.get_chat()
    if mafiaevent.is_private:
        user = mafiaevent.chat
        rank = mafiaevent.pattern_match.group(1)
    else:
        mafiaevent.chat.title
    try:
        user, rank = await get_full_user(mafiaevent)
    except:
        pass
    if me == user:
       k = await mafia.edit("You can't promote yourself...")
       return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await mafia.edit("**ERROR !!**")
    if user:
        telchanel = [d.entity.id
                     for d in await mafiaevent.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=False,
                               invite_users=True,
                                change_info=False,
                                 ban_users=True,
                                  delete_messages=True,
                                   pin_messages=True)
        for x in telchanel:
          try:
             await mafiaevent.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await mafia.edit(f"**Promoting User in :**  `{i}` Chats...")
          except:
             pass
    else:
        await mafia.edit(f"**Reply to a user !!**")
    await mafia.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Promoted Globally In** `{i}` **Chats !!**"
    )
    await bot.send_message(Config.MAFIABOT_LOGGER, f"#GPROMOTE \n\n**Globally Promoted User :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`")


@bot.on(admin_cmd(pattern="ggdemote ?(.*)"))
@bot.on(sudo_cmd(pattern="gdemote ?(.*)", allow_sudo=True))
async def _(mafiaevent):
    i = 0
    sender = await mafiaevent.get_sender()
    me = await mafiaevent.client.get_me()
    mafia = await eor(mafiaevent, "`Demoting Globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await mafiaevent.get_chat()
    if mafiaevent.is_private:
        user = mafiaevent.chat
        rank = mafiaevent.pattern_match.group(1)
    else:
        mafiaevent.chat.title
    try:
        user, rank = await get_full_user(mafiaevent)
    except:
        pass
    if me == user:
       k = await mafia.edit("You can't Demote yourself !!")
       return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await mafia.edit("**ERROR !!**")
    if user:
        telchanel = [d.entity.id
                     for d in await mafiaevent.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=None,
                               invite_users=None,
                                change_info=None,
                                 ban_users=None,
                                  delete_messages=None,
                                   pin_messages=None)
        for x in telchanel:
          try:
             await mafiaevent.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await mafia.edit(f"**Demoting Globally In Chats :** `{i}`")
          except:
             pass
    else:
        await mafia.edit(f"**Reply to a user !!**")
    await mafia.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Demoted Globally In** `{i}` **Chats !!**"
    )
    await bot.send_message(Config.MAFIABOT_LOGGER, f"#GDEMOTE \n\n**Globally Demoted :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`")


@bot.on(admin_cmd(pattern=r"ggban ?(.*)"))
@bot.on(sudo_cmd(pattern=r"gban ?(.*)", allow_sudo=True))
async def _(event):
    mafia = await eor(event, "`Gbanning...`")
    reason = ""
    reply = await event.get_reply_message()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = (await event.get_chat()).id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await eod(mafia, "**To gban a user i need a userid or reply to his/her message!!**")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == h1m4n5hu0p:
        return await eod(mafia, "🥴 **Nashe me hai kya lawde ‽**")
    if str(userid) in MAFIA_ID:
        return await eod(mafia, "😑 **GBan my creator ?¿ Really‽**")
    if is_gbanned(userid):
        return await eod(
            mafia,
            "This kid is already gbanned and added to my **Gban Watch!!**",
        )
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(gfuck.id, userid, view_messages=False)
                chats += 1
                await mafia.edit(f"**Gbanning...** \n**Chats :** __{chats}__")
            except BaseException:
                pass
    gbaner(userid)
    a = gvarstat("BAN_PIC")
    if a is not None:
        b = a.split(" ")
        c = [gbanpic]
        for d in b:
            c.append(d)
        gbpic = random.choice(c)
    else:
        gbpic = gbanpic
    gmsg = f"🥴 [{name}](tg://user?id={userid}) **beta majdur ko khodna 😪 aur** [{MAFIA_NAME}](tg://user?id={h1m4n5hu0p}) **ko chodna... Kabhi sikhana nhi!! 😏**\n\n📍 Added to Gban Watch!!\n**🔰 Total Chats :**  `{chats}`"
    if reason != "":
        gmsg += f"\n**🔰 Reason :**  `{reason}`"
    ogmsg = f"[{name}](tg://user?id={userid}) **Is now GBanned by** [{MAFIA_NAME}](tg://user?id={h1m4n5hu0p}) **in**  `{chats}`  **Chats!! 😏**\n\n**📍 Also Added to Gban Watch!!**"
    if reason != "":
        ogmsg += f"\n**🔰 Reason :**  `{reason}`"
    if Config.ABUSE == "ON":
        await bot.send_file(event.chat_id, gbpic, caption=gmsg)
        await mafia.delete()
    else:
        await mafia.edit(ogmsg)


@bot.on(admin_cmd(pattern=r"unggban ?(.*)"))
@bot.on(sudo_cmd(pattern=r"ungban ?(.*)", allow_sudo=True))
async def _(event):
    mafia = await eor(event, "`Ungban in progress...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(mafia, "`Reply to a user or give their userid... `")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if not is_gbanned(userid):
        return await eod(mafia, "`User is not gbanned.`")
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(gfuck.id, userid, view_messages=True)
                chats += 1
                await mafia.edit(f"**Ungban in progress...** \n**Chats :** __{chats}__")
            except BaseException:
                pass
    ungbaner(userid)
    await mafia.edit(
        f"📍 [{name}](tg://user?id={userid}) **is now Ungbanned from `{chats}` chats and removed from Gban Watch!!**",
    )


@bot.on(admin_cmd(pattern="listggban$"))
@bot.on(sudo_cmd(pattern="listgban$", allow_sudo=True))
async def already(event):
    hmm = await eor(event, "`Fetching Gbanned users...`")
    gbanned_users = all_gbanned()
    GBANNED_LIST = "**Gbanned Users :**\n"
    if len(gbanned_users) > 0:
        for user in gbanned_users:
            hel = user.chat_id
            mafia = int(hel)
            try:
                tity = await event.client.get_entity(mafia)
                name = tity.first_name
            except ValueError:
                name = "User"
            GBANNED_LIST += f"📍 [{name}](tg://user?id={mafia}) (`{mafia}`)\n"
    else:
        GBANNED_LIST = "No Gbanned Users!!"
    await hmm.edit(GBANNED_LIST)


@bot.on(events.ChatAction)
async def _(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        if is_gbanned(str(user.id)):
            if chat.admin_rights:
                try:
                    await event.client.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
                    gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    await event.reply(gban_watcher)
                except BaseException:
                    pass


@bot.on(admin_cmd(pattern=r"ggkick ?(.*)"))
@bot.on(sudo_cmd(pattern=r"gkick ?(.*)", allow_sudo=True))
async def gkick(event):
    mafia = await eor(event, "`Kicking globally...`")
    reply = await event.get_reply_message()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(mafia, "`Reply to some msg or add their id.`")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == h1m4n5hu0p:
        return await eod(mafia, "**🥴 Nashe me hai kya lawde!!**")
    if str(userid) in MAFIA_ID:
        return await eod(mafia, "**😪 I'm not going to gkick my developer!!**")
    async for gkick in event.client.iter_dialogs():
        if gkick.is_group or gkick.is_channel:
            try:
                await bot.kick_participant(gkick.id, userid)
                chats += 1
                await mafia.edit(f"**Kicking globally...** \n**Chats :** __{chats}__")
            except BaseException:
                pass
    a = gvarstat("BAN_PIC")
    if a is not None:
        b = a.split(" ")
        c = [gbanpic]
        for d in b:
            c.append(d)
        gbpic = random.choice(c)
    else:
        gbpic = gbanpic
    gkmsg = f"🏃 **Globally Kicked** [{name}](tg://user?id={userid})'s butts !! \n\n📝 **Chats :**  `{chats}`"
    if Config.ABUSE == "ON":
        await bot.send_file(event.chat_id, gbpic, caption=gkmsg, reply_to=reply)
        await mafia.delete()
    else:
        await mafia.edit(gkmsg)


@bot.on(admin_cmd(pattern=r"ggmute ?(\d+)?"))
@bot.on(sudo_cmd(allow_sudo=True, pattern=r"gmute ?(\d+)?"))
async def gm(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await eor(event, "`Trying to gmute user...`")
        await asyncio.sleep(2)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(event, "Need a user to gmute. Reply or give userid to gmute them..")
    name = (await event.client.get_entity(userid)).first_name
    event.chat_id
    await event.get_chat()
    if gsql.is_gmuted(userid, "gmute"):
        return await eod(event, "This kid is already Gmuted.")
    try:
        if str(userid) in MAFIA_ID:
            return await eod(event, "**Sorry I'm not going to gmute them..**")
    except:
        pass
    try:
        gsql.gmute(userid, "gmute")
    except Exception as e:
        await eod(event, "Error occured!\nError is " + str(e))
    else:
        if Config.ABUSE == "ON":
            await bot.send_file(event.chat_id, gmutepic, caption=f"**(~‾▿‾)~ Chup [Madarchod](tg://user?id={userid}) ....**", reply_to=reply)
            await event.delete()
        else:
            await eor(event, "**Globally Muted [{name}](tg://user?id={userid}) !!**\n\n__Kid struggling to speak__ ♪～(´ε｀ )")
        


@bot.on(admin_cmd(outgoing=True, pattern=r"unggmute ?(\d+)?"))
@bot.on(sudo_cmd(allow_sudo=True, pattern=r"ungmute ?(\d+)?"))
async def endgmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await eor(event, "`Trying to ungmute !!`")
        await asyncio.sleep(2)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(event,"Please reply to a user or add their into the command to ungmute them.")
    name = (await event.client.get_entity(userid)).first_name
    event.chat_id
    if not gsql.is_gmuted(userid, "gmute"):
        return await eod(event, "I don't remember I gmuted him...")
    try:
        gsql.ungmute(userid, "gmute")
    except Exception as e:
        await eod(event, "Error occured!\nError is " + str(e))
    else:
        await eor(event, f"**Unmuted [{name}](tg://user?id={userid}) Globally !!**")


@command(incoming=True)
async def watcher(event):
    if gsql.is_gmuted(event.sender_id, "ggmute"):
        await event.delete()


