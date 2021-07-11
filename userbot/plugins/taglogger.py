from telethon import custom, events
from telethon.tl.types import Channel
from telethon.utils import get_display_name

from userbot.Config import Config

if Config.TAG_LOGGER:
    tagger = int(Config.TAG_LOGGER)

if Config.TAG_LOGGER:

    @bot.on(
        events.NewMessage(
            incoming=True,
            blacklist_chats=Config.UB_BLACK_LIST_CHAT,
            func=lambda e: (e.mentioned),
        )
    )
    async def all_messages_catcher(event):
        # the bot might not have the required access_hash to mention the
        # appropriate PM
        await event.forward_to(Var.TG_BOT_USER_NAME_BF_HER)

        # construct message
        # the message format is stolen from @MasterTagAlertBot
        ammoca_message = ""

        h1m4n5hu0p = await event.client.get_entity(event.sender_id)
        if h1m4n5hu0p.bot or h1m4n5hu0p.verified or h1m4n5hu0p.support:
            return

        h1m4n5hu0pm = f"[{get_display_name(h1m4n5hu0p)}](tg://user?id={h1m4n5hu0p.id})"

        where_ = await event.client.get_entity(event.chat_id)

        where_m = get_display_name(where_)
        button_text = "See the tag 📬"

        if isinstance(where_, Channel):
            message_link = f"https://t.me/c/{where_.id}/{event.id}"
        else:
            # not an official link,
            # only works in DrKLO/Telegram,
            # for some reason
            message_link = f"tg://openmessage?chat_id={where_.id}&message_id={event.id}"
            # Telegram is weird :\

        ammoca_message += f"{h1m4n5hu0pm} `just tagged you...` \nWhere?\nIn [{where_m}]({message_link})\n__Tap to go the tagged msg__📬🚶"
        if tagger is not None:
            await bot.send_message(
                entity=tagger,
                message=ammoca_message,
                link_preview=False,
                buttons=[[custom.Button.url(button_text, message_link)]],
                silent=True,
            )
        else:
            return
