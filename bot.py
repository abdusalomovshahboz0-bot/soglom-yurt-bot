"""«SOG'LOM YURT | Salomatlik maktabi» Telegram boti.

Ishga tushirish:
    pip install -r requirements.txt
    python bot.py

Bot tokeni .env faylidan (BOT_TOKEN) o'qiladi va kodda saqlanmaydi.
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, ErrorEvent, Message

import config
import db
import kb
import vebxizmat
from handlers import (
    admin,
    ai,
    harakat,
    hisobot,
    obuna,
    odatlar,
    ovqatlanish,
    profil,
    salomatlik,
    testlar,
    umumiy,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

BUYRUQLAR = [
    BotCommand(command="start", description="Botni ishga tushirish"),
    BotCommand(command="menyu", description="Asosiy menyu"),
    BotCommand(command="ovqat", description="Sog'lom ovqatlanish"),
    BotCommand(command="mashq", description="Mashq va gigiyena"),
    BotCommand(command="suv", description="Suv hisoblagichi"),
    BotCommand(command="faollik", description="Uyqu va faollik"),
    BotCommand(command="kalkulyator", description="BMI va kaloriya"),
    BotCommand(command="test", description="O'quv testlari"),
    BotCommand(command="natijalar", description="Test natijalari"),
    BotCommand(command="odatlar", description="Kunlik odatlar"),
    BotCommand(command="ai", description="AI yordamchi"),
    BotCommand(command="profil", description="Profil va natijalar"),
    BotCommand(command="hisobot", description="Haftalik hisobot"),
    BotCommand(command="qidir", description="Bilim bazasidan qidirish"),
    BotCommand(command="maslahat", description="Kunlik maslahat"),
    BotCommand(command="help", description="Yordam"),
]

dp = Dispatcher()

# Majburiy kanal obunasi: har qanday xabar va tugmadan oldin tekshiriladi.
# config.MAJBURIY_KANAL bo'sh bo'lsa tekshiruv o'chirilgan bo'ladi.
_obuna_tekshiruvi = obuna.ObunaMiddleware()
dp.message.middleware(_obuna_tekshiruvi)
dp.callback_query.middleware(_obuna_tekshiruvi)

# Routerlar ro'yxatga olinadi. Har bir router o'z handlerlarini birinchi bo'lib
# tekshiradi, shuning uchun tartib muhim.
dp.include_router(obuna.router)
dp.include_router(umumiy.router)
dp.include_router(ovqatlanish.router)
dp.include_router(harakat.router)
dp.include_router(salomatlik.router)
dp.include_router(odatlar.router)
dp.include_router(testlar.router)
dp.include_router(ai.router)
dp.include_router(profil.router)
dp.include_router(hisobot.router)
dp.include_router(admin.router)

# Oxirgi zaxira router: hech bir bo'limga mos kelmagan matnlar shu yerga tushadi.
# Foydalanuvchi oddiy so'z yozsa ham, bot uni bilim bazasidan qidirib topadi.
zaxira = Router(name="zaxira")
dp.include_router(zaxira)


@zaxira.message(F.text)
async def erkin_matn(message: Message) -> None:
    matn = (message.text or "").strip()
    if not matn:
        return
    if matn.startswith("/"):
        await message.answer(
            "🤔 Bu buyruq topilmadi.\n\n"
            "Kerakli bo'limni asosiy menyudan tanlang 👇",
            reply_markup=kb.bosh_menyu(),
        )
        return
    javob, markup = umumiy.qidiruv_javobi(matn)
    await message.answer(javob, reply_markup=markup)


@zaxira.message()
async def boshqa_xabar(message: Message) -> None:
    await message.answer(
        "📎 Bu turdagi xabarni qayta ishlay olmayman.\n\n"
        "Iltimos, savolingizni matn ko'rinishida yozing yoki menyudan foydalaning 👇",
        reply_markup=kb.bosh_menyu(),
    )


@dp.errors()
async def xatoliklarni_uslash(event: ErrorEvent) -> bool:
    """Kutilmagan xatoliklarni ushlab, botning ishlashini davom ettiradi."""
    logger.exception("Xatolik yuz berdi: %s", event.exception)

    xabar = event.update.message
    if xabar is None and event.update.callback_query is not None:
        xabar = event.update.callback_query.message
    if xabar is not None:
        try:
            await xabar.answer(
                "⚠️ Kechirasiz, kutilmagan xatolik yuz berdi. "
                "Iltimos, qaytadan urinib ko'ring."
            )
        except Exception:  # xabar yuborish ham imkonsiz bo'lishi mumkin
            pass
    return True


async def main() -> None:
    if not config.BOT_TOKEN:
        raise SystemExit(
            "❌ BOT_TOKEN topilmadi. Iltimos, .env faylida BOT_TOKEN ni belgilang."
        )

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.set_my_commands(BUYRUQLAR)
    await bot.delete_webhook(drop_pending_updates=True)
    await db.init()

    # Bulut muhitida (masalan Render) PORT o'zgaruvchisi beriladi — shunda
    # bot ichida kichik veb-qatlam ishga tushadi va serverni uxlab qolishdan
    # saqlaydi. Lokal Windows'da PORT bo'lmaydi, shu sabab bu blok ishlamaydi.
    port = (os.getenv("PORT") or "").strip()
    if port.isdigit():
        asyncio.create_task(vebxizmat.ishga_tushir(int(port)))

    logger.info("Bot ishga tushdi: %s", config.BOT_NOMI)
    try:
        await dp.start_polling(bot)
    finally:
        await db.yopish()
        await bot.session.close()
        logger.info("Bot to'xtatildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as xato:
        if str(xato):
            print(xato)
