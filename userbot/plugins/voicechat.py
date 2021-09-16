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
        await event.edit(event, "**🔊 Voice Chat Started Successfully**")
    except Exception as e:
        await event.edit( f"`{str(e)}`")


@bot.on(admin_cmd(pattern="endvc$"))
@bot.on(sudo_cmd(pattern="endvc$", allow_sudo=True))
async def _(event):
    try:
        await bot(DiscardGroupCallRequest(await getvc(event)))
        await event.edit(event, "**❌ Voice Chat Ended Successfully !!**")
    except Exception as e:
        await event.edit( f"`{str(e)}`")


CmdHelp("voicechat").add_command(
  "startvc", None, "Starts the voice chat in Group."
).add_command(
  "endvc", None, "Ends the voice chat  group."
).add()
