from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.framework.labeler import BotLabeler

from db.models import UserModel

bl = BotLabeler()
@bl.message(CommandRule(command_text="help"))
async def send_help(_):
    return "Бот выводит краткую информацию о сообщениях в чате при вызове команды /summary"