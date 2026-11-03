"""Kunlik sog'lom odatlar ro'yxati va kuzatuvi."""

from aiogram import F, Router
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
import kb
import utils
from data import hayot
from handlers.yordamchi import korinishni_yangila

router = Router(name="odatlar")

QISQA = utils.xavfsiz(config.QISQA_OGOHLANTIRISH)


def odat_klaviaturasi(bajarilgan: set[str]) -> InlineKeyboardMarkup:
    """Odatlar ro'yxatini belgilash klaviaturasi."""
    builder = InlineKeyboardBuilder()
    for indeks, odat in enumerate(hayot.KUNLIK_ODATLAR):
        belgi = "✅" if odat["nom"] in bajarilgan else "⬜"
        builder.button(
            text=f"{belgi} {odat['emoji']} {odat['nom']}",
            callback_data=f"odat:{indeks}",
        )
    builder.adjust(1)
    builder.row(
        InlineKeyboardButton(text="📊 7 kunlik natija", callback_data="odat_hisobot")
    )
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def odat_matni(bajarilgan: set[str], ism: str) -> str:
    """Odatlar ekranining matni."""
    nomlar = {odat["nom"] for odat in hayot.KUNLIK_ODATLAR}
    jami = len(nomlar)
    soni = len(bajarilgan & nomlar)
    chiziq = utils.progress_bar(soni, jami)

    if soni >= jami:
        holat = "🎉 Ajoyib! Bugun barcha odatlarni bajardingiz."
    elif soni >= max(1, jami // 2):
        holat = "👍 Yaxshi natija, davom eting!"
    else:
        holat = "💪 Kichik qadamlar ham muhim — bugundan boshlang."

    return (
        "✅ <b>Kunlik sog'lom odatlar</b>\n\n"
        f"👤 {utils.xavfsiz(ism)}\n"
        f"Bajarildi: <b>{soni}/{jami}</b>\n\n"
        f"{chiziq}\n\n"
        f"{holat}\n\n"
        "Bajargan odatingizni tugma orqali belgilang 👇\n"
        f"ℹ️ {QISQA}"
    )


async def _odat_korinishi(user_id: int, ism: str | None = None) -> tuple[str, InlineKeyboardMarkup]:
    foydalanuvchi = await db.foydalanuvchi(user_id)
    if ism is None:
        ism = foydalanuvchi["ism"] if foydalanuvchi is not None else "Foydalanuvchi"
    bajarilgan = await db.odat_holati(user_id)
    return odat_matni(bajarilgan, ism), odat_klaviaturasi(bajarilgan)


@router.message(Command("odatlar"))
async def odatlar_buyrugi(message: Message) -> None:
    matn, markup = await _odat_korinishi(
        message.from_user.id, message.from_user.full_name
    )
    await message.answer(matn, reply_markup=markup)


@router.callback_query(F.data == "odatlar")
async def odatlar_callback(callback: CallbackQuery) -> None:
    matn, markup = await _odat_korinishi(callback.from_user.id)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data.startswith("odat:"))
async def odat_almashtirish(callback: CallbackQuery) -> None:
    qismlar = (callback.data or "").split(":")
    if len(qismlar) != 2 or not qismlar[1].isdigit():
        await callback.answer("Odat topilmadi", show_alert=True)
        return
    indeks = int(qismlar[1])
    if not 0 <= indeks < len(hayot.KUNLIK_ODATLAR):
        await callback.answer("Odat topilmadi", show_alert=True)
        return

    odat = hayot.KUNLIK_ODATLAR[indeks]["nom"]
    yoqilgan = await db.odat_almashtir(callback.from_user.id, odat)
    matn, markup = await _odat_korinishi(callback.from_user.id)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer("✅ Belgilandi" if yoqilgan else "⬜ Belgidan olindi")


@router.callback_query(F.data == "odat_hisobot")
async def odat_hisobot(callback: CallbackQuery) -> None:
    hisobot = await db.odat_hisobot(callback.from_user.id, 7)
    jami_odat = len(hayot.KUNLIK_ODATLAR)
    kunlar = hisobot["kunlar"]

    qatorlar = ["📊 <b>Oxirgi 7 kunlik odatlar natijasi</b>\n"]
    for oraliq in range(6, -1, -1):
        sana = db.kun_oldin(oraliq)
        soni = kunlar.get(sana, 0)
        chiziq = utils.progress_bar(soni, jami_odat, 8)
        qatorlar.append(
            f"{utils.sana_chiroyli(sana)}: {chiziq} {soni}/{jami_odat}"
        )
    qatorlar.append("")
    qatorlar.append(f"🧮 Jami bajarilgan odat: <b>{hisobot['jami']}</b> ta")
    qatorlar.append("")
    qatorlar.append(f"ℹ️ {QISQA}")

    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Odatlarni belgilash", callback_data="odatlar")
    builder.button(text="📊 Haftalik hisobot", callback_data="hisobot")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())

    await korinishni_yangila(callback, "\n".join(qatorlar), builder.as_markup())
    await callback.answer()
