import pyaztro
from userbot.utils import admin_cmd, sudo_cmd
from userbot import bot
from userbot.cmdhelp import CmdHelp

ASTRO = ""

Credit = "This Modules is property of mafia userbot, Don't remove this line. this module created by Kittu @A_viyu"

@bot.on(admin_cmd(pattern="hs ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="hs ?(.*)", allow_sudo=True))
async def astro(e):
    msg = await e.reply("Fetching data...")
    if not e.pattern_match.group(1):
        x = ASTRO
        if not x:
            await msg.edit("Not Found.")
            return
    else:
        x = e.pattern_match.group(1)
    horoscope = pyaztro.Aztro(sign=x)
    mood = horoscope.mood
    lt = horoscope.lucky_time
    desc = horoscope.description
    col = horoscope.color
    com = horoscope.compatibility
    ln = horoscope.lucky_number

    result = (
        f"**Horoscope for `{x}`**:\n"
        f"**Mood :** `{mood}`\n"
        f"**Lucky Time :** `{lt}`\n"
        f"**Lucky Color :** `{col}`\n"
        f"**Lucky Number :** `{ln}`\n"
        f"**Compatibility :** `{com}`\n"
        f"**Description :** `{desc}`\n"
    )

    await msg.edit(result)

    if "Kittu" in Credit:
        pass
    else: 
        await e.reply("This Module is made by @A_Viyu you nigga give him credit.")




CmdHelp("horoscope").add_command(
"hs", "<sign>", "Usage: it will show horoscope of daily of your sign\nList of all signs - aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius and pisces."
).add()
