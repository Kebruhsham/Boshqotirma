import re
import asyncio
import requests
import instaloader
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# ⚠️ Tokenni o'z bot tokening bilan almashtir
TOKEN = "7792059702:AAE0VGDHnm2oZq73lF_g_m2WkK7F2mPG_VA"

# ✅ Botni yangi usulda ishga tushirish
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# 📥 Instagramdan yuklash uchun instaloader
L = instaloader.Instaloader()

# 📌 Video yuklash funksiyasi
def download_instagram_video(url: str, filename: str):
    shortcode = url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    if not post.is_video:
        raise Exception("Bu post video emas!")

    video_url = post.video_url
    response = requests.get(video_url)

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename

# 📨 Foydalanuvchi xabarini tutish
@dp.message(F.text)
async def handle_instagram_link(message: Message):
    url_pattern = r"(https?://(www\.)?instagram\.com/[^\s]+)"
    match = re.search(url_pattern, message.text)

    if match:
        insta_url = match.group(1)
        await message.answer("Video yuklanmoqda...")

        try:
            filename = f"{insta_url.split('/')[-2]}.mp4"
            download_instagram_video(insta_url, filename)

            video = FSInputFile(filename)
            await message.answer_video(video)

            os.remove(filename)

        except Exception as e:
            
            await message.answer(f"❌ Xatolik yuz berdi:\n<code>{e}</code>")
    else:
        await message.answer("Video havolasini yuboring.")

# 🚀 Botni ishga tushurish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
