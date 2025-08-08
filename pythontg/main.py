# async_bot.py
import os
import random
import io
import pandas as pd
import aiofiles
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram.utils import executor

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Set TELEGRAM_BOT_TOKEN in environment or .env")

df = pd.read_csv("jokes.csv")
jokes = df["text"].dropna().astype(str).tolist()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def make_anekdot_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("/anekdot"))
    return kb


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    first = message.from_user.first_name or ""
    last = message.from_user.last_name or ""
    if last:
        text = f"Привет, <b>{first} {last}</b>, если ты напишешь /anekdot, то я скину тебе рандомный анекдот"
    else:
        text = f"Привет, <b>{first}</b>, если ты напишешь /anekdot, то я скину тебе рандомный анекдот"

    await message.answer(text, parse_mode="HTML", reply_markup=make_anekdot_keyboard())


@dp.message_handler(commands=["anekdot"])
async def cmd_anekdot(message: types.Message):
    joke = random.choice(jokes) if jokes else "No jokes available"
    await message.answer(joke, parse_mode="HTML", reply_markup=make_anekdot_keyboard())


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_message(message: types.Message):
    try:
        print(message.from_user.username, message.text)
        kb = make_anekdot_keyboard()

        gif_path = "beer.gif"
        if not os.path.exists(gif_path):
            await message.answer("GIF not found on server.", reply_markup=kb)
            return

        async with aiofiles.open(gif_path, "rb") as f:
            data = await f.read()

        bio = io.BytesIO(data)
        bio.name = "beer.gif"
        input_file = InputFile(bio, filename="beer.gif")

        await bot.send_video(
            chat_id=message.chat.id,
            video=input_file,
            caption="Here's something for you",
            reply_markup=kb,
        )
    except Exception as e:
        try:
            await message.reply(
                f"{message.from_user.first_name}, полегче а то взорвусь"
            )
        except Exception:
            pass


if __name__ == "__main__":
    skip_updates = True
    executor.start_polling(dp, skip_updates=True)
