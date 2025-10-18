import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_telegram_message(chat_id: str, text: str):
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN not set")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    print(f"Sending to chat_id: {chat_id}, text: {text}")
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print("Message sent successfully")