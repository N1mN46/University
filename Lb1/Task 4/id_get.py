from dotenv import load_dotenv
from telethon import TelegramClient
import os
import asyncio

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# Використовуємо іншу назву сесії, щоб не плутати
client = TelegramClient('find_id_session', api_id, api_hash)

async def find_chat_ids():
    print("Входимо в акаунт, щоб отримати список чатів...")
    await client.start()
    
    print("Ваші останні 15 діалогів:")
    
    # Отримуємо 15 останніх діалогів
    async for dialog in client.iter_dialogs(limit=15):
        # dialog.id - це те, що нам потрібно
        # dialog.name - це назва чату/користувача
        print(f"Назва: {dialog.name}  |  ID: {dialog.id}")

    print("\nЗнайдіть потрібну групу та скопіюйте її ID (зазвичай від'ємне число).")

# Використовуємо сучасний спосіб запуску
if __name__ == "__main__":
    asyncio.run(find_chat_ids())