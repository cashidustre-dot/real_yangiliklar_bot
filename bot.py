import os
import asyncio
import base64
import tempfile
from openai import OpenAI
from telegram import Bot

# =========================
# SOZLAMALAR
# =========================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN topilmadi!")

if not CHAT_ID:
    raise RuntimeError("TELEGRAM_CHAT_ID topilmadi!")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY topilmadi!")

telegram_bot = Bot(token=TELEGRAM_TOKEN)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# =========================
# RESTAURANT MA'LUMOTLARI
# =========================

RESTAURANT_NAME = "REAL RESTAURANT"

ADDRESS = "M39 yo‘li, 991-km"

PHONE_1 = "+998 91 564 40 00"
PHONE_2 = "+998 97 124 01 10"


# Har safar boshqa mavzu
TOPICS = [
    "katta Jizzax somsasi",
    "milliy osh",
    "mazali milliy taomlar",
    "oilaviy dam olish",
    "M39 yo‘lida qulay restoran",
    "issiq va yangi tayyorlangan taomlar",
    "choy va suhbat",
    "REAL RESTAURANT xizmatlari",
]


topic_index = 0


# =========================
# AI REKLAMA MATNI
# =========================

def create_ad_text(topic):

    prompt = f"""
Sen REAL RESTAURANT uchun professional reklama yozuvchisisan.

Restoran:
{RESTAURANT_NAME}

Manzil:
{ADDRESS}

Telefon:
{PHONE_1}
{PHONE_2}

Bugungi reklama mavzusi:
{topic}

MUHIM:
REAL RESTAURANT katta Jizzax somsasi bilan mashhur.
Jizzax somsasi katta, dumaloq, to‘yimli va ishtaha ochadigan
taom sifatida tasvirlansin.

Qisqa, chiroyli va odamni restoranga tashrif buyurishga
qiziqtiradigan Telegram reklama yoz.

Reklamada quyidagilar bo‘lsin:
🍽️ restoran nomi
🔥 asosiy reklama
📍 manzil
📞 telefonlar

Haqiqatga mos bo‘lmagan chegirma yoki aksiya o‘ylab topma.

Faqat reklama matnini qaytar.
"""

    response = openai_client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text.strip()


# =========================
# AI FLYER YARATISH
# =========================

def create_flyer(topic):

    prompt = f"""
Create a professional Uzbek restaurant advertising flyer.

Restaurant:
REAL RESTAURANT

Location:
M39 yo‘li, 991-km

Phone:
+998 91 564 40 00
+998 97 124 01 10

Main advertising topic:
{topic}

IMPORTANT:
REAL RESTAURANT serves authentic large Jizzakh somsa.
The Jizzakh somsa should be LARGE, ROUND, golden-brown,
thick and very appetizing.

Create a premium modern restaurant advertisement.
Use a realistic food-photography style.
Make the food look fresh, hot and delicious.

The flyer should be suitable for Telegram.
Use an attractive composition and different visual style
from previous advertisements.

Do not invent discounts or prices.
Do not add fake information.

Include:
REAL RESTAURANT
M39 yo‘li, 991-km
+998 91 564 40 00
+998 97 124 01 10
"""

    result = openai_client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json

    image_bytes = base64.b64decode(image_base64)

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    )

    temp_file.write(image_bytes)
    temp_file.close()

    return temp_file.name


# =========================
# TELEGRAMGA YUBORISH
# =========================

async def send_advertisement():

    global topic_index

    topic = TOPICS[topic_index]

    print(f"🤖 AI reklama tayyorlamoqda: {topic}")

    # AI matn
    ad_text = create_ad_text(topic)

    print("📝 Reklama matni tayyor.")

    # AI flyer
    flyer_path = create_flyer(topic)

    print("🖼️ Flyer tayyor.")

    try:

        # Avval flyer
        with open(flyer_path, "rb") as photo:

            await telegram_bot.send_photo(
                chat_id=CHAT_ID,
                photo=photo,
                caption=ad_text
            )

        print("✅ Flyer va reklama Telegramga yuborildi!")

    finally:

        # Vaqtinchalik rasmni o‘chirish
        try:
            os.remove(flyer_path)
        except:
            pass

    # Keyingi safar boshqa mavzu
    topic_index = (topic_index + 1) % len(TOPICS)


# =========================
# ASOSIY ISH
# =========================

async def main():

    print("🚀 REAL RESTAURANT AI BOT ISHLADI!")

    while True:

        try:

            await send_advertisement()

        except Exception as error:

            print("❌ XATOLIK:")
            print(error)

        print("⏰ Keyingi reklama 2 soatdan keyin.")

        # 2 SOAT
        await asyncio.sleep(2 * 60 * 60)


if __name__ == "__main__":
    asyncio.run(main())
