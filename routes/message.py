import logging
import os
import aiohttp

from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.framework.labeler import BotLabeler

from db.repository import get_user, add_user, add_chat, add_message, get_messages, delete_messages

bl = BotLabeler()


@bl.message(CommandRule(command_text="summary", prefixes=["/"]))
async def send_summary(message: Message):
    chat_id = await add_chat(message.peer_id)

    messages = await get_messages(chat_id)
    reversed_messages = list(reversed(messages))

    if not reversed_messages:
        await message.answer("Переписка пуста. Нечего анализировать.")
        return
        
    chat_log = ""
    for msg in reversed_messages:
        if not msg.text:
            continue
        author = msg.first_name or msg.username or f"User{msg.user_id}"
        chat_log += f"{author}: {msg.text}\n"
        
    if not chat_log.strip():
        await message.answer("Нет текстовых сообщений для анализа.")
        return

    prompt = f"Сделай краткое саммари (выжимку) переписки в чате. Пиши по-русски, кратко, без лишних формальностей:\n\n{chat_log}"
    
    api_key = os.getenv("DEEPSEEK_TOKEN")
    if not api_key:
        return
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты полезный AI-ассистент, который делает качественное и краткое саммари переписок."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.deepseek.com/chat/completions", json=payload, headers=headers) as resp:
                data = await resp.json()
                if "choices" in data and len(data["choices"]) > 0:
                    summary = data["choices"][0]["message"]["content"]
                    await message.answer(summary)
                else:
                    await message.answer("Ошибка: Deepseek не вернул ожидаемый формат ответа.")
                    logging.error(f"Deepseek Response Error: {data}")
    except Exception as e:
        await message.answer(f"Произошла ошибка при вызове API: {e}")
        logging.error(f"Deepseek Exception: {e}")

@bl.message(CommandRule(command_text="clear"))
async def clear_messages(message: Message):
    chat_id = await add_chat(message.peer_id)
    await delete_messages(chat_id)
    return "История сообщений успешно очищена"

@bl.message()
async def save_message(message: Message):
    user_id = message.from_id
    peer_id = message.peer_id
    user = await get_user(user_id)

    if user is None:
        vk_user = (await message.ctx_api.users.get(user_ids=[user_id]))[0]

        await add_user(
            peer_id=user_id,
            username=vk_user.screen_name,
            first_name=vk_user.first_name,
            last_name=vk_user.last_name
        )

        user = await get_user(user_id)

    chat_id = await add_chat(peer_id)

    await add_message(chat_id, user.id, message.text)
