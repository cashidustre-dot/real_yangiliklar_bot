import os
import asyncio
import logging
import tempfile

from telegram import Bot
from telegram.error import TelegramError

from ai_content import (
    get_current_category,
    create_ad_text,
    create_flyer,
)


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

# Railway Variables ichida TELEGRAM_CHAT_ID bo'lsa shuni ishlatadi.
#
# Agar o'zgaruvchi bo'lmasa:
# @realqulaylikm39 ishlatiladi.
#
# Guruh uchun odatda -100xxxxxxxxxx ko'rinishidagi ID kerak bo'ladi.
#
TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    "@realqulaylikm39",
)


# ============================================================
# TEKSHIRUV
# ============================================================

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN topilmadi! "
        "Railway → Variables bo'limiga tokenni kiriting."
    )


# ============================================================
# ASOSIY VAZIFA
# ============================================================

async def send_restaurant_ad():
    """
    Railway Cron bir marta ishga tushirganda:

    1. Kategoriya tanlanadi
    2. AI reklama matnini yaratadi
    3. AI flyer yaratadi
    4. Telegramga yuboradi
    5. Jarayon tugaydi

    Keyingi ishga tushirishni Railway Cron amalga oshiradi.
    """

    logger.info("=" * 60)
    logger.info("REAL RESTAURANT AI BOT ISHLADI")
    logger.info("=" * 60)

    # --------------------------------------------------------
    # 1. BUGUNGI KATEGORIYA
    # --------------------------------------------------------

    category = get_current_category()

    category_name = category["name"]

    logger.info(
        "Bugungi reklama kategoriyasi: %s",
        category_name,
    )

    # --------------------------------------------------------
    # 2. AI REKLAMA MATNI
    # --------------------------------------------------------

    logger.info(
        "AI reklama matnini tayyorlamoqda..."
    )

    ad_text = create_ad_text(category)

    logger.info(
        "Reklama matni tayyor."
    )

    # --------------------------------------------------------
    # 3. AI FLYER
    # --------------------------------------------------------

    logger.info(
        "AI flyer tayyorlamoqda..."
    )

    flyer_path = None

    try:

        flyer_path = create_flyer(category)

        logger.info(
            "Flyer tayyor: %s",
            flyer_path,
        )

        # ----------------------------------------------------
        # 4. TELEGRAM
        # ----------------------------------------------------

        logger.info(
            "Telegramga yuborilmoqda..."
        )

        async with Bot(
            token=TELEGRAM_BOT_TOKEN
        ) as bot:

            # Telegram caption maksimal uzunligi sababli
            # juda uzun matn bo'lsa qisqartiramiz.
            caption = ad_text[:1000]

            await bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=open(
                    flyer_path,
                    "rb",
                ),
                caption=caption,
            )

        logger.info(
            "✅ Flyer va reklama Telegramga yuborildi!"
        )

    except TelegramError as error:

        logger.error(
            "❌ Telegram xatosi: %s",
            error,
        )

        raise

    except Exception as error:

        logger.exception(
            "❌ Reklama yuborishda xato: %s",
            error,
        )

        raise

    finally:

        # ----------------------------------------------------
        # VAQTINCHALIK FAYLNI O'CHIRISH
        # ----------------------------------------------------

        if flyer_path:

            try:

                if os.path.exists(flyer_path):
                    os.remove(flyer_path)

                    logger.info(
                        "Vaqtinchalik flyer fayli o'chirildi."
                    )

            except Exception as error:

                logger.warning(
                    "Flyer faylini o'chirib bo'lmadi: %s",
                    error,
                )

    logger.info("=" * 60)
    logger.info(
        "REAL RESTAURANT AI BOT ISHI YAKUNLANDI"
    )
    logger.info("=" * 60)


# ============================================================
# START
# ============================================================

def main():

    asyncio.run(
        send_restaurant_ad()
    )


if __name__ == "__main__":

    main()
