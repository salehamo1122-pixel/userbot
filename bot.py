import os
import asyncio
from telethon import TelegramClient, events
from datetime import datetime
import pytz

API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_USER_ID = int(os.environ.get('ADMIN_USER_ID'))

client = TelegramClient('userbot', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    if event.sender_id != ADMIN_USER_ID:
        return
    
    if event.raw_text.startswith('.timeprofile on'):
        await event.reply('🕐 ساعت پروفایل فعال شد!')
    elif event.raw_text.startswith('.timeprofile off'):
        await event.reply('❌ ساعت پروفایل غیرفعال شد!')

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("ربات روشن شد!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())