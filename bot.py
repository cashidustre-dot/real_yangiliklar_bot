import os
import asyncio
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN topilmadi!")

if not CHAT_ID:
    raise RuntimeError("TELEGRAM_CHAT_ID topilmadi!")


async def send_news():
    bot = Bot(token=TOKEN)

    message = """
🤖 REAL RESTAURANT — TEST

Assalomu alaykum! 👋

Bu avtomatik test xabari.

⏰ Bot har 2 daqiqada xabar yuborishni tekshiryapti.

📍 M39 yo‘li, 991-km
🍽️ REAL RESTAURANT
"""

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

    print("✅ Xabar yuborildi!")


async def main():
    while True:
        try:
            await send_news()
        except Exception as e:
            print("❌ Xatolik:", e)

        # TEST: 2 daqiqa kutadi
        await asyncio.sleep(2 * 60)


if __name__ == "__main__":
    asyncio.run(main())
