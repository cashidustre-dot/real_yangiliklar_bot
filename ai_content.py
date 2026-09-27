import os
import base64
import tempfile
from datetime import datetime, timezone

from openai import OpenAI


# =========================================================
# SOZLAMALAR
# =========================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY topilmadi!")

client = OpenAI(api_key=OPENAI_API_KEY)


RESTAURANT_NAME = "REAL RESTAURANT"

ADDRESS = "M39 yo‘li, 991-km"

PHONE_1 = "+998 91 564 40 00"
PHONE_2 = "+998 97 124 01 10"


# =========================================================
# REKLAMA KATEGORIYALARI
# =========================================================
#
# Cron har 2 soatda ishlaydi.
# UTC vaqtiga qarab kategoriya avtomatik almashadi.
# Shuning uchun Railway konteyneri qayta ishga tushsa ham
# birinchi kategoriyaga qaytib qolmaydi.
#

CATEGORIES = [
    {
        "name": "Jizzax somsa",
        "emoji": "🥟",
        "description": (
            "Jizzax somsasi — katta, dumaloq va to‘yimli somsa."
        ),
    },

    {
        "name": "Milliy osh",
        "emoji": "🍚",
        "description": (
            "An'anaviy o‘zbek oshini reklama qil."
        ),
    },

    {
        "name": "Kabob",
        "emoji": "🍢",
        "description": (
            "Mazali va ishtaha ochadigan kabobni reklama qil."
        ),
    },

    {
        "name": "Lag‘mon",
        "emoji": "🍜",
        "description": (
            "Lag‘monni asosiy reklama mahsuloti sifatida ko‘rsat."
        ),
    },

    {
        "name": "Jiz",
        "emoji": "🥩",
        "description": (
            "Jiz taomini issiq, mazali va ishtaha ochadigan "
            "restoran taomi sifatida reklama qil."
        ),
    },

    {
        "name": "Boshqa milliy taomlar",
        "emoji": "🍽️",
        "description": (
            "REAL RESTAURANTdagi turli milliy taomlarni "
            "umumiy tarzda reklama qil."
        ),
    },

    {
        "name": "Yevropa salatlari",
        "emoji": "🥗",
        "description": (
            "Yevropa uslubidagi salatlarni reklama qil."
        ),
    },

    {
        "name": "Mayonezli salatlar",
        "emoji": "🥗",
        "description": (
            "Mayonezli salatlarni asosiy reklama mavzusi qil."
        ),
    },

    {
        "name": "Desertlar",
        "emoji": "🍰",
        "description": (
            "Shirinlik va desertlarni reklama qil."
        ),
    },

    {
        "name": "Kofe",
        "emoji": "☕",
        "description": (
            "Kofe, yoqimli suhbat va dam olish kayfiyatini "
            "reklama qil."
        ),
    },
]


# =========================================================
# KATEGORIYANI TANLASH
# =========================================================

def get_current_category():
    """
    Cron har 2 soatda ishga tushadi.
    UTC soatiga qarab kategoriya tanlanadi.

    Masalan:
    00:00 -> Somsa
    02:00 -> Osh
    04:00 -> Kabob
    06:00 -> Lag‘mon
    ...
    """

    now = datetime.now(timezone.utc)

    slot = now.hour // 2

    index = slot % len(CATEGORIES)

    return CATEGORIES[index]


# =========================================================
# AI REKLAMA MATNI
# =========================================================

def create_ad_text(category):
    category_name = category["name"]
    emoji = category["emoji"]
    description = category["description"]

    prompt = f"""
Sen REAL RESTAURANT uchun professional Telegram reklama
matnlarini yozadigan tajribali reklama copywriterisan.

RESTORAN:
{RESTAURANT_NAME}

MANZIL:
{ADDRESS}

TELEFON:
{PHONE_1}
{PHONE_2}

BUGUNGI REKLAMA KATEGORIYASI:
{category_name}

TAOM TAVSIFI:
{description}

MUHIM QOIDALAR:

1. Faqat BUGUNGI kategoriya asosiy reklama mavzusi bo‘lsin.

2. Agar kategoriya "Kofe" bo‘lsa,
   somsa, osh yoki kabob haqida asosiy reklama yozma.

3. Agar kategoriya "Yevropa salatlari" bo‘lsa,
   flyer va matnda salat asosiy mavzu bo‘lsin.

4. Agar kategoriya "Mayonezli salatlar" bo‘lsa,
   aynan shu turdagi salatlar asosiy mavzu bo‘lsin.

5. Agar kategoriya "Desertlar" bo‘lsa,
   desert va shirinliklar asosiy mavzu bo‘lsin.

6. Faqat mavjudligi aytilgan taomlardan foydalan.

7. Narx, aksiya, chegirma, sovg‘a yoki boshqa
   tasdiqlanmagan ma'lumotni o‘ylab topma.

8. Restoran nomi, manzil va telefon raqamlarini
   reklamaning oxirida aniq ko‘rsat.

9. Matn tabiiy o‘zbek tilida bo‘lsin.

10. Reklama juda uzun bo‘lmasin.

11. Odamni REAL RESTAURANTga tashrif buyurishga
    qiziqtiradigan iliq va ishtaha ochadigan uslubdan foydalan.

12. Har safar bir xil jumlalarni takrorlama.

FORMAT:

{emoji} Sarlavha

2-4 qisqa jumladan iborat reklama.

📍 {ADDRESS}
📞 {PHONE_1}
📞 {PHONE_2}

Faqat tayyor Telegram reklama matnini qaytar.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return response.output_text.strip()


# =========================================================
# AI FLYER
# =========================================================

def create_flyer(category):
    category_name = category["name"]
    emoji = category["emoji"]
    description = category["description"]

    prompt = f"""
Create a professional premium food advertising flyer
for a real Uzbek restaurant.

RESTAURANT:
REAL RESTAURANT

LOCATION:
M39 yo‘li, 991-km

PHONE:
+998 91 564 40 00
+998 97 124 01 10

TODAY'S MAIN CATEGORY:
{category_name}

CATEGORY DESCRIPTION:
{description}

VERY IMPORTANT:

The flyer MUST visually focus on today's category.

Today's category is:
{category_name}

Do NOT automatically put Jizzakh somsa into the image.

Do NOT use somsa as the main food unless today's category
is exactly "Jizzax somsa".

If today's category is:
- Osh → show Uzbek plov as the main food.
- Kabob → show appetizing grilled kebab as the main food.
- Lag‘mon → show lag‘mon as the main food.
- Jiz → show jiz as the main food.
- Boshqa milliy taomlar → show a tasteful selection of
  Uzbek national dishes.
- Yevropa salatlari → show fresh European-style salads.
- Mayonezli salatlar → show appetizing mayonnaise-based salads.
- Desertlar → show beautiful desserts and sweets.
- Kofe → show attractive coffee and a pleasant cafe atmosphere.
- Jizzax somsa → show a large, round, golden Jizzakh somsa.

Do not mix unrelated foods as the main subject.

The selected category must be visually dominant.

STYLE:
- realistic professional food photography
- premium restaurant advertising
- appetizing
- fresh and warm
- elegant composition
- suitable for Telegram
- modern Uzbek restaurant atmosphere
- high quality
- natural realistic food

TEXT ON FLYER:

REAL RESTAURANT

M39 yo‘li, 991-km

+998 91 564 40 00
+998 97 124 01 10

Do not invent prices.
Do not invent discounts.
Do not invent promotions.
Do not invent dishes that were not mentioned.

Make the selected category visually obvious.
"""

    result = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1024x1024",
    )

    image_base64 = result.data[0].b64_json

    image_bytes = base64.b64decode(image_base64)

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png",
    )

    temp_file.write(image_bytes)
    temp_file.close()

    return temp_file.name


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    category = get_current_category()

    print("====================================")
    print("REAL RESTAURANT AI CONTENT")
    print("====================================")
    print(f"Kategoriya: {category['name']}")

    text = create_ad_text(category)

    print("\nREKLAMA:")
    print(text)

    print("\nFlyer tayyorlanmoqda...")

    flyer = create_flyer(category)

    print(f"Flyer: {flyer}")
