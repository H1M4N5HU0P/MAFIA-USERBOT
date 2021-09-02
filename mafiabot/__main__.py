import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest

from mafiabot import LOGS, bot, tbot
from .config import Config
from mafiabot.utils import load_module
from mafiabot.version import __mafia__ as mafiaver
hl = Config.HANDLER
MAFIA_PIC = Config.ALIVE_PIC or "https://telegra.ph/file/e97d640332ce5eadb3f89.mp4"

# let's get the bot ready
async def mafia_bot(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()


# Userbot starter...
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if Config.BOT_USERNAME is not None:
            LOGS.info("Checking Telegram Bot Username...")
            bot.tgbot = TelegramClient(
                "BOT_TOKEN", api_id=Config.APP_ID, api_hash=Config.API_HASH
            ).start(bot_token=Config.BOT_TOKEN)
            LOGS.info("Checking Completed. Proceeding to next step...")
            LOGS.info("Starting MafiaBot"")
            bot.loop.run_until_complete(mafia_bot(Config.BOT_USERNAME))
            LOGS.info("MafiaBot Startup Completed")
        else:
            bot.start()
    except Exception as e:
        LOGS.error(f"BOT_TOKEN - {str(e)}")
        sys.exit()

# imports plugins...
path = "mafiabot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))



# let the party begin...
LOGS.info("𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐁𝐨𝐭 𝐌𝐨𝐝𝐞 !")
tbot.start()
LOGS.info("ʟɛɢɛռɖaʀʏ ᴀғ ᴍᴀғɪᴀʙᴏᴛ")
LOGS.info(
    "MAFIABOT IS ON!!! MAFIABOT VERSION :- {mafiaver} YOUR 𝕄𝔸𝔽𝕀𝔸𝔹𝕆𝕋 IS READY TO USE! FOR CHECK YOUR BOT WORKING OR NOT PLEASE TYPE (.alive/.ping) ENJOY YOUR BOT! JOIN FOR MORE FUTURE UPDATES @MafiaBot_Support .""")
)

# that's life...
async def mafia_is_on():
    try:
        if Config.LOGGER_ID != 0:
            await bot.send_file(
                Config.LOGGER_ID,
                MAFIA_PIC,
                caption=f"༆ʟɛɢɛռɖaʀʏ ᴀғ ᴍᴀғɪᴀʙᴏᴛ༆\n\n**𝚅𝙴𝚁𝚂𝙸𝙾𝙽 ➪ {mafiaver}**\n\n𝐓𝐲𝐩𝐞 .ping or .alive 𝐭𝐨 𝐜𝐡𝐞𝐜𝐤! \n\n𝙹𝙾𝙸𝙽 [𝙼𝙰𝙵𝙸𝙰𝙱𝙾𝚃 𝙲𝙷𝙰𝚃](t.me/MAFIABOT_CHIT_CHAT) 𝚃𝙾 𝚀𝚄𝙴𝚁𝚈 & 𝙹𝙾𝙸𝙽 [𝙼𝙰𝙵𝙸𝙰 𝚄𝙿𝙳𝙰𝚃𝙴𝚂](t.me/MafiaBot_Support) 𝚃𝙾 𝙺𝙽𝙾𝚆 𝚁𝙴𝙶𝚁𝙰𝙳𝙸𝙽𝙶 𝚄𝙿𝙳𝙰𝚃𝙴 𝙰𝙽𝙳 𝙽𝙴𝚆𝚂 𝙰𝙱𝙾𝚄𝚃 𝙼𝙰𝙵𝙸𝙰𝙱𝙾𝚃",
            )
    except Exception as e:
        LOGS.info(str(e))


    try:
        await bot(JoinChannelRequest("@MAFIA_SUPORT"))
    except BaseException:
        pass


bot.loop.create_task(mafia_is_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()
