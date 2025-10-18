import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

app = FastAPI()

class NotifyRequest(BaseModel):
    telegram_id: int
    message: str

@app.post("/notify")
async def notify_user(data: NotifyRequest):
    try:
        await bot.send_message(chat_id=data.telegram_id, text=data.message)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@dp.message()
async def start_command(message: Message):
    user_id = message.from_user.id
    await message.answer(f"Привет! Твой Telegram ID: {user_id}. Открой приложение по ссылке: http://localhost:5174")

async def main():
    # Start FastAPI server in background
    config = uvicorn.Config(app, host="0.0.0.0", port=8001)
    server = uvicorn.Server(config)
    await asyncio.gather(
        dp.start_polling(bot),
        server.serve()
    )

if __name__ == "__main__":
    asyncio.run(main())