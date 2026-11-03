"""Majburiy kanal obunasi (force join).

Bu modul botdan foydalanish uchun foydalanuvchi kanalga a'zo bo'lishini
talab qiladi. Sozlamalar `config.MAJBURIY_KANAL` va `config.KANAL_HAVOLASI`
orqali boshqariladi.

`MAJBURIY_KANAL` bo'sh bo'lsa — tekshiruv butunlay o'chirilgan bo'ladi va
bot avvalgidek ishlaydi.
"""

import logging

from aiogram import BaseMiddleware, Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, ChatMemberUpdated, InlineKeyboardMarkup

import config
import kb
from handlers.yordamchi import korinishni_yangila

router = Router(name="obuna")
logger = logging.getLogger(__name__)

# Bot kanalga administrator qilib qo'shilganda kanal ID sini yozib qo'yadigan fayl.
KANAL_FAYL = "kanal_id.txt"

# A'zo hisoblanadigan holatlar.
AZOLIK_HOLATLARI = {"creator", "administrator", "member"}


async def obuna_tekshir(bot: Bot, user_id: int) -> bool:
    """Foydalanuvchi majburiy kanalga a'zo ekanligini tekshiradi.

    Kanal sozlamagan yoki tekshirish imkonsiz bo'lsa — True qaytaradi
    (foydalanuvchini bloklab qo'ymaslik uchun).
    """
    if not config.MAJBURIY_KANAL:
        return True
    try:
        azo = await bot.get_chat_member(config.MAJBURIY_KANAL, user_id)
    except TelegramBadRequest as xato:
        logger.warning("Kanal a'zoligini tekshirishda xatolik: %s", xato)
        return True
    if azo.status in AZOLIK_HOLATLARI:
        return True
    if azo.status == "restricted":
        return bool(getattr(azo, "is_member", False))
    return False


def obuna_matni() -> str:
    return (
        "📢 <b>Botdan foydalanish uchun kanalga obuna bo'ling</b>\n\n"
        "Assalomu alaykum! Botning barcha bo'limlaridan foydalanish uchun "
        "quyidagi kanalimizga a'zo bo'ling.\n\n"
        "1️⃣ «📢 Kanalga obuna bo'lish» tugmasini bosing.\n"
        "2️⃣ Kanalga a'zo bo'ling.\n"
        "3️⃣ «✅ Obunani tekshirish» tugmasini bosing.\n\n"
        "Shundan so'ng botning barcha funksiyalari ochiladi. 💚"
    )


def obuna_klaviaturasi() -> InlineKeyboardMarkup:
    from aiogram.utils.keyboard import InlineKeyboardBuilder

    builder = InlineKeyboardBuilder()
    builder.button(text="📢 Kanalga obuna bo'lish", url=config.KANAL_HAVOLASI)
    builder.button(text="✅ Obunani tekshirish", callback_data="obuna_tekshir")
    builder.adjust(1)
    return builder.as_markup()


class ObunaMiddleware(BaseMiddleware):
    """Har bir xabar va tugmadan oldin kanal obunasini tekshiradi."""

    async def __call__(self, handler, event, data):
        if not config.MAJBURIY_KANAL:
            return await handler(event, data)

        foydalanuvchi = data.get("event_from_user")
        if foydalanuvchi is None:
            return await handler(event, data)

        # Adminlar tekshiruvsiz o'tadi.
        if foydalanuvchi.id in config.ADMIN_ID:
            return await handler(event, data)

        # Obunani tekshirish tugmasining o'zi doim o'tishi kerak.
        if isinstance(event, CallbackQuery) and event.data == "obuna_tekshir":
            return await handler(event, data)

        if await obuna_tekshir(data["bot"], foydalanuvchi.id):
            return await handler(event, data)

        # Obuna yo'q: tugma bosilsa ogohlantirish, matn bo'lsa ko'rsatma yuboriladi.
        if isinstance(event, CallbackQuery):
            await event.answer(
                "⚠️ Avval kanalga obuna bo'ling!", show_alert=True
            )
            return None

        await event.answer(obuna_matni(), reply_markup=obuna_klaviaturasi())
        return None


@router.callback_query(F.data == "obuna_tekshir")
async def obuna_tekshir_callback(callback: CallbackQuery, bot: Bot) -> None:
    if await obuna_tekshir(bot, callback.from_user.id):
        await korinishni_yangila(
            callback,
            "✅ <b>Rahmat! Obuna tasdiqlandi.</b>\n\n"
            "Endi botning barcha bo'limlaridan foydalanishingiz mumkin. 💚\n\n"
            "Kerakli bo'limni tanlang 👇",
            kb.bosh_menyu(),
        )
        await callback.answer("Obuna tasdiqlandi ✅")
    else:
        await callback.answer(
            "❌ Siz hali kanalga a'zo bo'lmagansiz.\n\n"
            "Avval «📢 Kanalga obuna bo'lish» tugmasi orqali a'zo bo'ling, "
            "so'ng qaytadan «✅ Obunani tekshirish» tugmasini bosing.",
            show_alert=True,
        )


@router.my_chat_member()
async def bot_azoligi_ozgardi(update: ChatMemberUpdated) -> None:
    """Bot kanalga administrator qilib qo'shilganda kanal ID sini saqlab qo'yadi.

    Bu kanalning raqamli ID sini qo'lda qidirmaslik uchun qulaylik.
    """
    chat = update.chat
    yangi_holat = update.new_chat_member.status
    if chat.type == "channel" and yangi_holat in ("administrator", "creator"):
        try:
            with open(KANAL_FAYL, "w", encoding="utf-8") as fayl:
                fayl.write(str(chat.id))
        except OSError:
            pass
        logger.info("Kanal aniqlandi: %s | ID: %s", chat.title, chat.id)
