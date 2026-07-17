import os
import asyncio
import pytz
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import InputFile
import io
from PIL import Image, ImageDraw, ImageFont

# گرفتن اطلاعات از محیط Render
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_USER_ID = int(os.environ.get('ADMIN_USER_ID'))

client = TelegramClient('userbot', API_ID, API_HASH)

# تابع ساخت عکس با ساعت
def create_clock_image():
    # ساخت یه عکس ساده
    img = Image.new('RGB', (500, 500), color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # گرفتن زمان ایران
    tz = pytz.timezone('Asia/Tehran')
    now = datetime.now(tz)
    time_str = now.strftime('%H:%M:%S')
    
    # نوشتن ساعت روی عکس
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    d.text((50, 200), time_str, fill=(255, 255, 255), font=font)
    
    # ذخیره در حافظه
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

@client.on(events.NewMessage)
async def handler(event):
    if event.sender_id != ADMIN_USER_ID:
        return
    
    if event.raw_text.startswith('.timeprofile on'):
        await event.reply('🕐 ساعت پروفایل فعال شد!')
        # حلقه تغییر عکس هر دقیقه
        while True:
            try:
                img_bytes = create_clock_image()
                file = InputFile(img_bytes, 'clock.png')
                await client(UpdateProfileRequest(photo=file))
                await asyncio.sleep(60)  # هر ۱ دقیقه
            except Exception as e:
                print(f"خطا: {e}")
                await asyncio.sleep(60)
    
    elif event.raw_text.startswith('.timeprofile off'):
        await event.reply('❌ ساعت پروفایل غیرفعال شد!')
        # برای توقف، ربات رو ری‌استارت کن
        raise KeyboardInterrupt

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("ربات روشن شد!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
