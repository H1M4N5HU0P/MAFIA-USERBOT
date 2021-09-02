import datetime
from mafiabot import *
from .config import Config
from .helpers import *
from mafiabot.utils import *
from mafiabot.random_strings import *
from mafiabot.version import __mafia__
from telethon import version


MAFIA_USER = bot.me.first_name
himanshu = bot.uid
mafia_mention = f"[{MAFIA_USER}](tg://user?id={himanshu})"
mafia_logo = "./himanshu/image/mafiabot_logo.jpg"
cjb = "./himanshu/image/cjb.jpg"
restlo = "./himanshu/image/rest.jpeg"
shuru = "./image/shuru.jpg"
hl = Config.HANDLER
shl = Config.SUDO_HANDLER
mafia_ver = __mafia__
tel_ver = version.__version__

async def get_user_id(ids):
    if str(ids).isdigit():
        userid = int(ids)
    else:
        userid = (await bot.get_entity(ids)).id
    return userid

sudos = Config.SUDO_USERS
if sudos:
    is_sudo = "True"
else:
    is_sudo = "False"

abus = Config.ABUSE
if abus == "ON":
    abuse_m = "Enabled"
else:
    abuse_m ="Disabled"

START_TIME = datetime.datetime.now()
uptime = f"{str(datetime.datetime.now() - START_TIME).split('.')[0]}"
my_channel = Config.MY_CHANNEL or "MafiaBot_Support"
my_group = Config.MY_GROUP or "MAFIABOT_CHIT_CHAT"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

chnl_link = "https://t.me/MafiaBot_Support"
mafia_channel = f"[𝙼𝙰𝙵𝙸𝙰 𝚄𝙿𝙳𝙰𝚃𝙴𝚂]({chnl_link})"
grp_link = "https://t.me/MAFIABOT_CHIT_CHAT"
mafia_grp = f"[𝙼𝙰𝙵𝙸𝙰𝙱𝙾𝚃 𝙲𝙷𝙰𝚃]({grp_link})"

WELCOME_FORMAT = """**Use these fomats in your welcome note to make them attractive.**
  {mention} :  To mention the user
  {title} : To get chat name in message
  {count} : To get group members
  {first} : To use user first name
  {last} : To use user last name
  {fullname} : To use user full name
  {userid} : To use userid
  {username} : To use user username
  {my_first} : To use my first name
  {my_fullname} : To use my full name
  {my_last} : To use my last name
  {my_mention} : To mention myself
  {my_username} : To use my username
"""
