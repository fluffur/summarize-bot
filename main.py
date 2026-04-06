import logging
import os

from db.pool import init_db, close_db
from routes import labelers

from vkbottle.bot import Bot

logging.basicConfig(level=logging.INFO)

bot = Bot(os.getenv("BOT_TOKEN"))

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)


async def startup_task():
    logging.info("Startup")
    await init_db()


async def shutdown_task():
    await close_db()


bot.loop_wrapper.on_startup.append(startup_task())
bot.loop_wrapper.on_shutdown.append(shutdown_task())

if __name__ == "__main__":
    bot.run_forever()
