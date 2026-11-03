"""Ertalabki mashqlar, uy mashqlari va shaxsiy gigiyena bo'limlari."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import kb
import utils
from data import hayot
from handlers.yordamchi import korinishni_yangila

router = Router(name="harakat")

QISQA = utils.xavfsiz(config.QISQA_OGOHLANTIRISH)

HARAKAT_SARLAVHA = (
    "🏋️ <b>Mashq va gigiyena</b>\n\n"
    "Ertalabki yengil mashqlar, uy sharoitidagi mashqlar va kundalik "
    "gigiyena qoidalari.\n\n"
    "🟢 Mashqni boshlashdan oldin 2-3 daqiqa yengil qizish mashqlarini bajaring.\n"
    "🟢 Har bir mashqni o'zingizga mos tezlikda, nafasni ushlab qolmasdan bajaring.\n\n"
    "Bo'limni tanlang 👇"
)


def harakat_menyusi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🏃 Ertalabki mashqlar", callback_data="harakat_ertalab")
    builder.button(text="🏋️ Uy mashqlari", callback_data="harakat_uy")
    builder.button(text="🧼 Shaxsiy gigiyena", callback_data="harakat_gigiyena")
    builder.button(text="📈 Faollikni kiritish", callback_data="uyqu")
    builder.button(text="🔍 Qidiruv", callback_data="qidiruv")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


@router.message(Command("mashq"))
async def mashq_buyrugi(message: Message) -> None:
    await message.answer(HARAKAT_SARLAVHA, reply_markup=harakat_menyusi())


@router.callback_query(F.data == "harakat")
async def harakat_callback(callback: CallbackQuery) -> None:
    await korinishni_yangila(callback, HARAKAT_SARLAVHA, harakat_menyusi())
    await callback.answer()


# --- Sahifalanadigan ro'yxatlar ---


@kb.sahifa_royxat("ertalab")
def ertalab_sahifasi(sahifa: int) -> tuple[str, InlineKeyboardMarkup]:
    elementlar = [
        (element["nom"], f"ertalab:{indeks}")
        for indeks, element in enumerate(hayot.ERTALABKI_MASHQ)
    ]
    matn = (
        "🏃 <b>Ertalabki mashqlar</b>\n\n"
        "Kunning boshida 5-10 daqiqa harakat qilish tetiklik beradi 👇"
    )
    return matn, kb.sahifali_royxat(
        elementlar, "ertalab", sahifa, ortga="harakat", ortga_matni="⬅️ Orqaga"
    )


@kb.sahifa_royxat("uymashq")
def uymashq_sahifasi(sahifa: int) -> tuple[str, InlineKeyboardMarkup]:
    elementlar = [
        (f"{element['nom']} ({element['daraja']})", f"uymashq:{indeks}")
        for indeks, element in enumerate(hayot.UY_MASHQLARI)
    ]
    matn = (
        "🏋️ <b>Uy mashqlari</b>\n\n"
        "Qo'shimcha jihozlarsiz bajariladigan mashqlar. Darajangizga mosini tanlang 👇"
    )
    return matn, kb.sahifali_royxat(
        elementlar, "uymashq", sahifa, ortga="harakat", ortga_matni="⬅️ Orqaga"
    )


@kb.sahifa_royxat("gigiyena")
def gigiyena_sahifasi(sahifa: int) -> tuple[str, InlineKeyboardMarkup]:
    elementlar = [
        (element["sarlavha"], f"gigiyena:{indeks}")
        for indeks, element in enumerate(hayot.GIGIYENA)
    ]
    matn = (
        "🧼 <b>Shaxsiy gigiyena</b>\n\n"
        "Kundalik tozalik qoidalari. Mavzuni tanlang 👇"
    )
    return matn, kb.sahifali_royxat(
        elementlar, "gigiyena", sahifa, ortga="harakat", ortga_matni="⬅️ Orqaga"
    )


@router.callback_query(F.data == "harakat_ertalab")
async def harakat_ertalab(callback: CallbackQuery) -> None:
    matn, markup = ertalab_sahifasi(0)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data == "harakat_uy")
async def harakat_uy(callback: CallbackQuery) -> None:
    matn, markup = uymashq_sahifasi(0)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data == "harakat_gigiyena")
async def harakat_gigiyena(callback: CallbackQuery) -> None:
    matn, markup = gigiyena_sahifasi(0)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


# --- Batafsil ma'lumotlar ---


@router.callback_query(F.data.startswith("ertalab:"))
async def ertalab_detali(callback: CallbackQuery) -> None:
    jami = len(hayot.ERTALABKI_MASHQ)
    indeks = kb.indeksni_ol(callback.data or "", jami)
    if indeks is None:
        await callback.answer("Mashq topilmadi", show_alert=True)
        return
    element = hayot.ERTALABKI_MASHQ[indeks]
    qadamlar = "\n".join(
        f"{raqam}. {utils.xavfsiz(qadam)}"
        for raqam, qadam in enumerate(element["qadamlar"], start=1)
    )
    matn = (
        f"🏃 <b>{utils.xavfsiz(element['nom'])}</b>\n\n"
        f"⏱ <b>Davomiyligi:</b> {utils.xavfsiz(element['davomiylik'])}\n\n"
        f"<b>Bajarish tartibi:</b>\n{qadamlar}\n\n"
        f"🟢 <b>Foydasi:</b> {utils.xavfsiz(element['foyda'])}\n\n"
        f"ℹ️ {QISQA}"
    )
    await korinishni_yangila(
        callback,
        matn,
        kb.element_klaviaturasi("ertalab", indeks, jami, "harakat_ertalab", "⬅️ Ro'yxatga qaytish"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("uymashq:"))
async def uymashq_detali(callback: CallbackQuery) -> None:
    jami = len(hayot.UY_MASHQLARI)
    indeks = kb.indeksni_ol(callback.data or "", jami)
    if indeks is None:
        await callback.answer("Mashq topilmadi", show_alert=True)
        return
    element = hayot.UY_MASHQLARI[indeks]
    mashqlar = "\n".join(
        f"{raqam}. {utils.xavfsiz(mashq)}"
        for raqam, mashq in enumerate(element["mashqlar"], start=1)
    )
    matn = (
        f"🏋️ <b>{utils.xavfsiz(element['nom'])}</b>\n\n"
        f"📊 <b>Daraja:</b> {utils.xavfsiz(element['daraja'])}\n"
        f"⏱ <b>Davomiyligi:</b> {utils.xavfsiz(element['davomiylik'])}\n\n"
        f"<b>Mashqlar:</b>\n{mashqlar}\n\n"
        f"🟢 <b>Foydasi:</b> {utils.xavfsiz(element['foyda'])}\n\n"
        f"⚠️ <b>Ehtiyot choralari:</b> {utils.xavfsiz(element['ehtiyot'])}\n\n"
        f"ℹ️ {QISQA}"
    )
    await korinishni_yangila(
        callback,
        matn,
        kb.element_klaviaturasi("uymashq", indeks, jami, "harakat_uy", "⬅️ Ro'yxatga qaytish"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("gigiyena:"))
async def gigiyena_detali(callback: CallbackQuery) -> None:
    jami = len(hayot.GIGIYENA)
    indeks = kb.indeksni_ol(callback.data or "", jami)
    if indeks is None:
        await callback.answer("Mavzu topilmadi", show_alert=True)
        return
    element = hayot.GIGIYENA[indeks]
    matn = (
        f"🧼 <b>{utils.xavfsiz(element['sarlavha'])}</b>\n\n"
        f"{utils.xavfsiz(element['matn'])}\n\n"
        f"ℹ️ {QISQA}"
    )
    await korinishni_yangila(
        callback,
        matn,
        kb.element_klaviaturasi(
            "gigiyena", indeks, jami, "harakat_gigiyena", "⬅️ Ro'yxatga qaytish"
        ),
    )
    await callback.answer()
