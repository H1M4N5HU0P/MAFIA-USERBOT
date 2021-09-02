import asyncio
import datetime
import importlib
import inspect
import logging
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from time import gmtime, strftime

from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from mafiabot import *
from .helpers import *
from .config import *
from mafiabot.utils import *


# ENV
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from mafiabot.config import Config
else:
    if os.path.exists("Config.py"):
        from Config import Development as Config


# load plugins
def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import mafiabot.utils

        path = Path(f"mafiabot/plugins/{shortname}.py")
        name = "mafiabot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("userbot - Successfully imported " + shortname)
    else:
        import mafiabot.utils

        path = Path(f"mafiabot/plugins/{shortname}.py")
        name = "mafiabot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = bot
        mod.tgbot = bot.tgbot
        mod.command = command
        mod.logger = logging.getLogger(shortname)
        # support for uniborg
        sys.modules["uniborg.util"] = mafiabot.utils
        mod.Config = Config
        mod.borg = bot
        mod.mafiabot = bot
        mod.edit_or_reply = edit_or_reply
        mod.eor = edit_or_reply
        mod.delete_mafia = delete_mafia
        mod.eod = delete_mafia
        mod.Var = Config
        mod.admin_cmd = mafia_cmd
        # support for other userbots
        sys.modules["userbot.utils"] = mafiabot.utils
        sys.modules["userbot"] = mafiabot
        # support for paperplaneextended
        sys.modules["userbot.events"] = mafiabot
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["mafiabot.plugins." + shortname] = mod
        LOGS.info(" plugin - Successfully imported " + shortname)


# remove plugins
def remove_plugin(shortname):
    try:
        try:
            for i in LOAD_PLUG[shortname]:
                bot.remove_event_handler(i)
            del LOAD_PLUG[shortname]

        except BaseException:
            name = f"mafiabot.plugins.{shortname}"

            for i in reversed(range(len(bot._event_builders))):
                ev, cb = bot._event_builders[i]
                if cb.__module__ == name:
                    del bot._event_builders[i]
    except BaseException:
        raise ValueError
