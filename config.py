"""Bot konfiguratsiyasi, doimiylar va umumiy matnlar."""

import os
from datetime import timedelta, timezone

from dotenv import load_dotenv

load_dotenv()

# --- Maxfiy ma'lumotlar (faqat .env faylidan o'qiladi) ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DB_FAYL = os.getenv("DB_FAYL", "soglom_yurt.db").strip()

# --- Admin(lar): /statistika buyrug'ini ko'ra oladigan Telegram ID lar ---
# .env faylida ADMIN_ID=123456789 (bir nechta bo'lsa vergul bilan: 111,222)
ADMIN_ID: set[int] = {
    int(qism)
    for qism in os.getenv("ADMIN_ID", "").replace(" ", "").split(",")
    if qism.strip().isdigit()
}

# --- Ixtiyoriy: tashqi AI xizmati (kalit bo'lmasa bot o'z bilim bazasidan javob beradi) ---
AI_KALIT = os.getenv("AI_API_KEY", "").strip()
AI_MANZIL = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").strip()
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini").strip()

# --- Majburiy kanal obunasi (force join) ---
# Botdan foydalanish uchun foydalanuvchi shu kanalga a'zo bo'lishi shart.
# MAJBURIY_KANAL bo'sh bo'lsa — obuna tekshiruvi o'chirilgan bo'ladi.
# Qo'llab-quvvatlanadi: raqamli ID (-1001234567890) yoki @username (@kanalim).
# Bot kanalga administrator qilib qo'shilsa, ID avtomatik aniqlanadi.
MAJBURIY_KANAL = os.getenv("MAJBURIY_KANAL", "").strip()
KANAL_HAVOLASI = os.getenv(
    "KANAL_HAVOLASI", "https://t.me/SoglomYurtEducation"
).strip()

# --- Ko'rinish ---
BOT_NOMI = "SOG'LOM YURT | Salomatlik maktabi"
SAHIFA_HAJMI = 6
PROGRESS_UZUNLIGI = 10

TOSHKENT_VAQTI = timezone(timedelta(hours=5))

TIBBIY_OGOHLANTIRISH = (
    "⚠️ Tibbiy ogohlantirish\n\n"
    "Bu bot faqat sog'lom turmush tarzi bo'yicha ma'rifiy ma'lumot beradi.\n"
    "• Tashxis qo'yilmaydi va davolash tavsiya etilmaydi.\n"
    "• Dori-darmonlar haqida maslahat berilmaydi.\n"
    "• Botdagi ma'lumotlar shifokor maslahatini almashtirmaydi.\n"
    "• Sog'lig'ingizda muammo bo'lsa, mutaxassis shifokorga murojaat qiling.\n\n"
    "Har qanday mashq yoki parhezni boshlashdan oldin o'z holatingizni hisobga oling."
)

QISQA_OGOHLANTIRISH = (
    "ℹ️ Bu ma'lumot ma'rifiy xarakterga ega, tashxis va davolash o'rnini bosmaydi."
)
