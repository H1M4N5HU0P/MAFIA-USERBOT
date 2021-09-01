#credit goes to Hellboy & @D3_krish
#This plugin modified by @D3_krish for MafiaBot

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.phone import CreateGroupCallRequest
from telethon.tl.functions.phone import DiscardGroupCallRequest
from telethon.tl.functions.phone import GetGroupCallRequest
from telethon.tl.functions.phone import InviteToGroupCallRequest

from . import *


async def getvc(event):
    chat_ = await event.client(GetFullChannelRequest(event.chat_id))
    _chat = await event.client(GetGroupCallRequest(chat_.full_chat.call))
    return _chat.call

def all_users(a, b):
    for c in range(0, len(a), b):
        yield a[c : c + b]


@bot.on(admin_cmd(pattern="startvc$"))
@bot.on(sudo_cmd(pattern="startvc$", allow_sudo=True))
async def _(event):
    try:
        await event.client(CreateGroupCallRequest(event.chat_id))
        await eor(event, "**🔊 Voice Chat Started Successfully**")
    except Exception as e:
        await eor(event, f"`{str(e)}`")


@bot.on(admin_cmd(pattern="endvc$"))
@bot.on(sudo_cmd(pattern="endvc$", allow_sudo=True))
async def _(event):
    try:
        await bot(DiscardGroupCallRequest(await getvc(event)))
        await eor(event, "**❌ Voice Chat Ended Successfully !!**")
    except Exception as e:
        await eor(event, f"`{str(e)}`")


@bot.on(admin_cmd(pattern="vcinvite$"))
@bot.on(sudo_cmd(pattern="vcinvite$", allow_sudo=True))
async def _(event):
    mafia = await eor(event, "`👥 Inviting Users To Join Voice Chat....`")
    users = []
    i = 0
    async for j in event.client.iter_participants(event.chat_id):
        if not j.bot:
            users.append(j.id)
    mafiaboy_ = list(all_users(users, 6))
    for k in mafiaboy_:
        try:
            await bot(InviteToGroupCallRequest(call=await getvc(event), users=k))
            i += 6
        except BaseException:
            pass
    await mafia.edit(f"**👥 Invited {i} Users to  JoinVoice Chat**")

CmdHelp("voicechat").add_command(
  "startvc", None, "Starts the voice chat in Group."
).add_command(
  "endvc", None, "Ends the voice chat  group."
).add_command(
  "vcinvite", None, "Invites members of the group to voice chat."
).add()
