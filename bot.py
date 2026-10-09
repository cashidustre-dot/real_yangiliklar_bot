
import os
import asyncio
import logging
from pathlib import Path

from telegram import Bot
from telegram.error import TelegramError

# ============================================================
# LOG
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ============================================================
# TELEGRAM SOZLAMALARI
# ============================================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    "@realqulaylikm39",
)

# Railway Variables bo'limiga oldingi reklama matnini kiriting.
PREVIOUS_AD_TEXT = os.getenv(
    "PREVIOUS_AD_TEXT",
    "",
).strip()

# Loyihadagi mavjud flyer rasmi.
FLYER_PATH = os.getenv(
    "FLYER_PATH",
    "real_restarant_menyu.png",
)

# ============================================================
# TEKSHIRUV
# ============================================================

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN topilmadi! "
        "Railway Variables bo'limini tekshiring."
    )

if not PREVIOUS_AD_TEXT:
    raise RuntimeError(
        "PREVIOUS_AD_TEXT topilmadi! "
        "Railway Variables bo'limiga oldingi reklama "
        "matnini kiriting."
    )

# ============================================================
# TELEGRAMGA REKLAMA YUBORISH
# ============================================================

async def send_restaurant_ad():
    logger.info("=" * 55)
    logger.info("REAL RESTAURANT BOT ISHLADI — AI O'CHIRILGAN")
    logger.info("Oldingi reklama matni ishlatiladi")
    logger.info("=" * 55)

    try:
        async with Bot(token=TELEGRAM_BOT_TOKEN) as bot:

            flyer = Path(FLYER_PATH)

            if flyer.is_file():
                # Mavjud flyer va oldingi matn yuboriladi.
                with flyer.open("rb") as photo:
                    await bot.send_photo(
                        chat_id=TELEGRAM_CHAT_ID,
                        photo=photo,
                        caption=PREVIOUS_AD_TEXT[:1024],
                    )

                # Matn 1024 belgidan uzun bo'lsa,
                # qolgan qismi alohida xabar bo'lib ketadi.
                if len(PREVIOUS_AD_TEXT) > 1024:
                    await bot.send_message(
                        chat_id=TELEGRAM_CHAT_ID,
                        text=PREVIOUS_AD_TEXT[1024:],
                    )

                logger.info("Reklama va flyer yuborildi.")

            else:
                # Flyer topilmasa, matnning o'zi yuboriladi.
                await bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=PREVIOUS_AD_TEXT,
                )

                logger.warning(
                    "Flyer topilmadi: %s. "
                    "Faqat reklama matni yuborildi.",
                    flyer,
                )

        logger.info("REKLAMA MUVAFFAQIYATLI YUBORILDI")

    except TelegramError:
        logger.exception("Telegram xatosi yuz berdi.")
        raise

    except Exception:
        logger.exception("Reklama yuborishda xato yuz berdi.")
        raise

    logger.info("BOT ISHI YAKUNLANDI")


def main():
    asyncio.run(send_restaurant_ad())


if __name__ == "__main__":
    main()
