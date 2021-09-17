import re

from mafiabot import bot
from mafiabot.utils import admin_cmd, sudo_cmd, edit_or_reply
from mafiabot.cmdhelp import CmdHelp
from mafiabot.helpers.functions import deEmojify
from userbot.Config import Config
from . import *

@bot.on(admin_cmd(pattern="anime(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="anime(?: |$)(.*)", allow_sudo=True))
async def nope(h1m4n5hu0p):
    mafia = h1m4n5hu0p.pattern_match.group(1)
    if not mafia:
        if h1m4n5hu0p.is_reply:
            (await h1m4n5hu0p.get_reply_message()).message
        else:
            await edit_or_reply(h1m4n5hu0p, "`Sir please give some query to search and download it for you..!`"
            )
            return

    troll = await bot.inline_query("animedb_bot", f"{(deEmojify(mafia))}")

    await troll[0].click(
        h1m4n5hu0p.chat_id,
        reply_to=h1m4n5hu0p.reply_to_msg_id,
        silent=True if h1m4n5hu0p.is_reply else False,
        hide_via=True,
    )
    await h1m4n5hu0p.delete()
    

CmdHelp("anime").add_command(
  "anime", "<anime name>", "Searches for the given anime and sends the details."
).add()
