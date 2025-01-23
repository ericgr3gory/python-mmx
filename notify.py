import os
from telegram import Bot
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def tele(message):

    try:
        botbotconsole_bot = Bot(token=os.getenv('BOT_TOKEN'))
        await botbotconsole_bot.sendMessage(chat_id=os.getenv('CHAT_ID'), text=message)

    except Exception as e:
        print(e)

def notification(message):
    asyncio.run(tele(message))

