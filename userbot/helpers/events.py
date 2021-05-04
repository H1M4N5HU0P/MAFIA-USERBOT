# credits goes ro catbot
from telethon.tl.types import MessageEntityMentionName

from userbot.Config import Config
from userbot.utils import delete_mafia


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in Config.SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id


async def get_user_from_event(event, mafiaevent=None, secondgroup=None):
    if mafiaevent is None:
        mafiaevent = event
    if secondgroup:
        args = event.pattern_match.group(2).split(" ", 1)
    else:
        args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.from_id is None and not event.is_private:
            await delete_mafia(mafiaevent, "`Well that's an anonymous admin !`")
            return None, None
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await delete_mafia(mafiaevent, "`Pass the user's username, id or reply!`", 5)
            return None, None
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await delete_mafia(mafiaevent, "`Couldn't fetch user to procced further`", 5)
            return None, None
    return user_obj, extra
