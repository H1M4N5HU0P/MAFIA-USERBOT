from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from mafiabot import bot, CmdHelp
from mafiabot.utils import admin_cmd, edit_or_reply as eor, sudo_cmd

@mafiabot.on(admin_cmd(pattern="history ?(.*)"))
@mafiabot.on(sudo_cmd(pattern="history ?(.*)", allow_sudo=True))
async def _(mafiaevent):
    if mafiaevent.fwd_from:
        return 
    if not mafiaevent.reply_to_msg_id:
       await eor(mafiaevent, "`Please Reply To A User To Get This Module Work`")
       return
    reply_message = await mafiaevent.get_reply_message() 
    chat = "Sangmatainfo_bot"
    victim = reply_message.sender.id
    if reply_message.sender.bot:
       await eor(mafiaevent, "Need actual users. Not Bots")
       return
    await eor(mafiaevent, "Checking...")
    async with mafiaevent.client.conversation(chat) as conv:
          try:     
              response1 = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
              response2 = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
              response3 = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
              await conv.send_message("/search_id {}".format(victim))
              response1 = await response1 
              response2 = await response2 
              response3 = await response3 
          except YouBlockedUserError: 
              await mafiaevent.reply("Please unblock ( @Sangmatainfo_bot ) ")
              return
          if response1.text.startswith("No records found"):
             await eor(mafiaevent, "User never changed his Username...")
          else: 
             await mafiaevent.delete()
             await mafiaevent.client.send_message(mafiaevent.chat_id, response2.message)

@mafiabot.on(admin_cmd(pattern="unh ?(.*)"))
@mafiabot.on(sudo_cmd(pattern="unh ?(.*)", allow_sudo=True))
async def _(mafiaevent):
    if mafiaevent.fwd_from:
        return 
    if not mafiaevent.reply_to_msg_id:
       await eor(mafiaevent, "`Please Reply To A User To Get This Module Work`")
       return
    reply_message = await mafiaevent.get_reply_message() 
    chat = "Sangmatainfo_bot"
    victim = reply_message.sender.id
    if reply_message.sender.bot:
       await eor(mafiaevent, "Need actual users. Not Bots")
       return
    await eor(mafiaevent, "Checking...")
    async with mafiaevent.client.conversation(chat) as conv:
          try:     
              response1 = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
              response2 = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
              response3 = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
              await conv.send_message("/search_id {}".format(victim))
              response1 = await response1 
              response2 = await response2 
              response3 = await response3 
          except YouBlockedUserError: 
              await mafiaevent.reply("Please unblock ( @Sangmatainfo_bot ) ")
              return
          if response1.text.startswith("No records found"):
             await eor(mafiaevent, "User never changed his Username...")
          else: 
             await mafiaevent.delete()
             await mafiaevent.client.send_message(mafiaevent.chat_id, response3.message)

CmdHelp("history").add_command(
  "history", "<reply to a user>", "Fetches the name history of replied user."
).add_command(
  "unh", "<reply to user>", "Fetches the Username History of replied users."
).add()
