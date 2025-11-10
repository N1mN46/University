from dotenv import load_dotenv
from telethon import TelegramClient
import os

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
client = TelegramClient('bot_session', api_id, api_hash)


TARGET_GROUP_ID = -5037125315 

async def main():
    # Отримання усіх користувачів у групі
    print(f"Отримуємо користувачів з групи (ID: {TARGET_GROUP_ID})...")
    
    
    async for user in client.iter_participants(TARGET_GROUP_ID):

        if not user.deleted:
            last_name = user.last_name if user.last_name else ""
            print(f"ID: {user.id}, Ім'я: {user.first_name} {last_name}")

    print("\n--- Список користувачів завершено ---") 

    print("Відправляємо тестове повідомлення 'me' (тобто вам)...")
    message = "Дароу усі йоу."
    await client.send_message(TARGET_GROUP_ID, message)
    print("Повідомлення успішно надіслано!")


# Ваша оригінальна структура запуску. Вона повністю робоча.
with client:
    client.loop.run_until_complete(main())