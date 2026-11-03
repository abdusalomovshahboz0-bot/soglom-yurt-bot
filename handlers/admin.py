"""Admin statistikasi: foydalanuvchilar va faollik ko'rsatkichlari."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import db
from handlers.yordamchi import korinishni_yangila

router = Router(name="admin")


def _klaviatura() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Yangilash", callback_data="admin_statistika")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="menyu"))
    return builder.as_markup()


async def _statistika_matni() -> str:
    s = await db.statistika()
    return (
        "📊 <b>Bot statistikasi</b>\n\n"
        "👥 <b>Foydalanuvchilar</b>\n"
        f"• Jami: <b>{s['jami_soni']}</b> ta\n"
        f"• Bugun qo'shilgan: <b>{s['bugun_qoshilgan']}</b> ta\n"
        f"• Bugun faol: <b>{s['bugun_faol']}</b> ta\n"
        f"• Oxirgi 7 kunda faol: <b>{s['hafta_faol']}</b> ta\n\n"
        "💧 <b>Suv (bugun)</b>\n"
        f"• Ichgan foydalanuvchilar: <b>{s['suv_ichganlar']}</b> ta\n"
        f"• Jami stakan: <b>{s['suv_stakan']}</b> ta\n\n"
        "🏃 <b>Faollik (bugun)</b>\n"
        f"• Ma'lumot kiritganlar: <b>{s['faollik_bugun']}</b> ta\n\n"
        "📝 <b>Testlar</b>\n"
        f"• Bugun topshirilgan: <b>{s['test_bugun']}</b> ta\n"
        f"• Jami topshirilgan: <b>{s['test_jami']}</b> ta\n\n"
        "✅ <b>Odatlar</b>\n"
        f"• Bugun bajarilgan: <b>{s['odat_bugun']}</b> ta\n\n"
        f"🕒 {db.hozir()}"
    )


@router.message(Command("statistika"))
async def statistika_buyrugi(message: Message) -> None:
    foydalanuvchi_id = message.from_user.id

    if not config.ADMIN_ID:
        await message.answer(
            "ℹ️ Admin hali sozlanmagan.\n\n"
            f"Sizning Telegram ID: <code>{foydalanuvchi_id}</code>\n\n"
            "Uni <b>.env</b> faylidagi <code>ADMIN_ID</code> ga yozib, "
            "botni qayta ishga tushiring."
        )
        return

    if foydalanuvchi_id not in config.ADMIN_ID:
        await message.answer("⛔ Bu buyruq faqat bot administratori uchun.")
        return

    await message.answer(await _statistika_matni(), reply_markup=_klaviatura())


@router.callback_query(lambda c: c.data == "admin_statistika")
async def statistika_yangilash(callback: CallbackQuery) -> None:
    if callback.from_user.id not in config.ADMIN_ID:
        await callback.answer("⛔ Ruxsat yo'q", show_alert=True)
        return
    await korinishni_yangila(callback, await _statistika_matni(), _klaviatura())
    await callback.answer("Yangilandi ✅")
