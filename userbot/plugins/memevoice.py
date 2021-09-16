# Credits to @spechide and his team for @TROLLVOICEBOT
# made by @h1m4n5hu0p_the_badass from the snippets of waifu AKA stickerizerbot....
# kang karega kya madarchod?
# aukaat h bsdk teri...jake baap ka loda chus ke aa....


import re

from userbot import bot
from mafiabot.utils import admin_cmd, sudo_cmd, edit_or_reply
from userbot.cmdhelp import CmdHelp
from userbot.helpers.functions import deEmojify


@bot.on(admin_cmd(pattern="mev(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="mev(?: |$)(.*)", allow_sudo=True))
async def nope(h1m4n5hu0p):
    mafia = h1m4n5hu0p.pattern_match.group(1)
    if not mafia:
        if h1m4n5hu0p.is_reply:
            (await h1m4n5hu0p.get_reply_message()).message
        else:
            await edit_or_reply(h1m4n5hu0p, "`Sir please give some query to search and download it for you..!`"
            )
            return

    troll = await bot.inline_query("TrollVoiceBot", f"{(deEmojify(mafia))}")

    await troll[0].click(
        h1m4n5hu0p.chat_id,
        reply_to=h1m4n5hu0p.reply_to_msg_id,
        silent=True if h1m4n5hu0p.is_reply else False,
        hide_via=True,
    )
    await h1m4n5hu0p.delete()
    

CmdHelp("memevoice").add_command(
  "mev", "<meme txt>", "Searches and uploads the meme in voice format (if any)."
).add()