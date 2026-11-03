"""Sog'lom ovqatlanish, tabiiy mahsulotlar va meva-sabzavotlar ensiklopediyasi."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import kb
import utils
from data import ensiklopediya, ovqatlanish
from handlers.yordamchi import korinishni_yangila

router = Router(name="ovqatlanish")

QISQA = utils.xavfsiz(config.QISQA_OGOHLANTIRISH)


def _element_klaviaturasi(
    prefix: str, indeks: int, jami: int, ortga: str, ortga_matni: str
) -> InlineKeyboardMarkup:
    return kb.element_klaviaturasi(prefix, indeks, jami, ortga, ortga_matni)


def ovqat_menyusi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🥗 Sog'lom ovqatlanish tamoyillari", callback_data="ovqat_tamoyil")
    builder.button(text="🍽 Muvozanatli ratsion", callback_data="ovqat_ratsion")
    builder.button(text="🌾 Tabiiy mahsulotlar", callback_data="ovqat_tabiiy")
    builder.button(text="🍎 Meva va sabzavotlar", callback_data="ens")
    builder.button(text="🔍 Qidiruv", callback_data="qidiruv")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def ens_menyusi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🍎 Mevalar (15 ta)", callback_data="ens_mevalar")
    builder.button(text="🥕 Sabzavotlar (15 ta)", callback_data="ens_sabzavotlar")
    builder.button(text="🔍 Nom yoki vitamin bo'yicha qidirish", callback_data="qidiruv")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ovqat"))
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


@router.message(Command("ovqat"))
async def ovqat_buyrugi(message: Message) -> None:
    await message.answer(OVQAT_SARLAVHA, reply_markup=ovqat_menyusi())


OVQAT_SARLAVHA = (
    "🥗 <b>Sog'lom ovqatlanish</b>\n\n"
    "Bu bo'limda muvozanatli ratsion asoslari, kunlik ovqatlanish tartibi va "
    "tabiiy mahsulotlar haqida ma'lumot beriladi.\n\n"
    "Bo'limni tanlang 👇"
)


@router.callback_query(F.data == "ovqat")
async def ovqat_callback(callback: CallbackQuery) -> None:
    await korinishni_yangila(callback, OVQAT_SARLAVHA, ovqat_menyusi())
    await callback.answer()


@router.callback_query(F.data == "ens")
async def ens_callback(callback: CallbackQuery) -> None:
    await korinishni_yangila(
        callback,
        "🍎 <b>Meva va sabzavotlar ensiklopediyasi</b>\n\n"
        "Har bir mahsulot uchun vitaminlar, sog'liq uchun foyda va iste'mol qilish "
        "bo'yicha amaliy maslahat berilgan.\n\n"
        "Ro'yxatni tanlang yoki qidiruv orqali kerakli mahsulotni toping 👇",
        ens_menyusi(),
    )
    await callback.answer()


# --- Sahifalanadigan ro'yxatlar ---


@kb.sahifa_royxat("tamoyil")
def tamoyil_sahifasi(sahifa: int) -> tuple[str, InlineKeyboardMarkup]:
    elementlar = [
        (element["sarlavha"], f"tamoyil:{indeks}")
        for indeks, element in enumerate(ovqatlanish.TAMOYILLAR)
    ]
    matn = (
        "🥗 <b>Sog'lom ovqatlanish tamoyillari</b>\n\n"
        f"Jami {len(elementlar)} ta mavzu. Mavzuni tanlang 👇"
    )
    return matn, kb.sahifali_royxat(
        elementlar, "tamoyil", sahifa, ortga="ovqat", ortga_matni="⬅️ Orqaga"
    )


@kb.sahifa_royxat("ratsion")
def ratsion_sahifasi(sahifa: int) -> tuple[str, InlineKeyboardMarkup]:
    elementlar = [
        (element["sarlavha"], f"ratsion:{indeks}")
        for indeks, element in enumerate(ovqatlanish.RATSION)
    ]
    matn = (
        "🍽 <b>Muvozanatli ratsion</b>\n\n"
        "Kunlik ovqatlanish tartibi va namunalar. Mavzuni tanlang 👇"
    )
    return matn, kb.sahifali_royxat(
        elementlar, "ratsion", sahifa, ortga="ovqat", ortga_matni="⬅️ Orqaga"
    )


@kb.sahifa_royxat("tabiiy")
def tabiiy_sahifasi(sahifa: int) -> tuple[str, InlineKeyboardMarkup]:
    elementlar = [
        (f"{element['emoji']} {element['nom']}", f"tabiiy:{indeks}")
        for indeks, element in enumerate(ovqatlanish.TABIIY_MAHSULOTLAR)
    ]
    matn = (
        "🌾 <b>Tabiiy mahsulotlar</b>\n\n"
        "Minimal qayta ishlangan, tabiiy mahsulotlar va ularning foydasi 👇"
    )
    return matn, kb.sahifali_royxat(
        elementlar, "tabiiy", sahifa, ortga="ovqat", ortga_matni="⬅️ Orqaga"
    )


@kb.sahifa_royxat("meva")
def meva_sahifasi(sahifa: int) -> tuple[str, InlineKeyboardMarkup]:
    elementlar = [
        (f"{element['emoji']} {element['nom']}", f"meva:{indeks}")
        for indeks, element in enumerate(ensiklopediya.MEVALAR)
    ]
    matn = (
        "🍎 <b>Mevalar ensiklopediyasi</b>\n\n"
        f"Jami {len(elementlar)} ta meva. Ma'lumotni ko'rish uchun nomni tanlang 👇"
    )
    return matn, kb.sahifali_royxat(
        elementlar, "meva", sahifa, ortga="ens", ortga_matni="⬅️ Orqaga"
    )


@kb.sahifa_royxat("sabzavot")
def sabzavot_sahifasi(sahifa: int) -> tuple[str, InlineKeyboardMarkup]:
    elementlar = [
        (f"{element['emoji']} {element['nom']}", f"sabzavot:{indeks}")
        for indeks, element in enumerate(ensiklopediya.SABZAVOTLAR)
    ]
    matn = (
        "🥕 <b>Sabzavotlar ensiklopediyasi</b>\n\n"
        f"Jami {len(elementlar)} ta sabzavot. Ma'lumotni ko'rish uchun nomni tanlang 👇"
    )
    return matn, kb.sahifali_royxat(
        elementlar, "sabzavot", sahifa, ortga="ens", ortga_matni="⬅️ Orqaga"
    )


@router.callback_query(F.data == "ens_mevalar")
async def ens_mevalar(callback: CallbackQuery) -> None:
    matn, markup = meva_sahifasi(0)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data == "ens_sabzavotlar")
async def ens_sabzavotlar(callback: CallbackQuery) -> None:
    matn, markup = sabzavot_sahifasi(0)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data == "ovqat_tamoyil")
async def ovqat_tamoyil(callback: CallbackQuery) -> None:
    matn, markup = tamoyil_sahifasi(0)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data == "ovqat_ratsion")
async def ovqat_ratsion(callback: CallbackQuery) -> None:
    matn, markup = ratsion_sahifasi(0)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data == "ovqat_tabiiy")
async def ovqat_tabiiy(callback: CallbackQuery) -> None:
    matn, markup = tabiiy_sahifasi(0)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


# --- Batafsil ma'lumotlar ---


def _indeksni_ol(callback: CallbackQuery, jami: int) -> int | None:
    return kb.indeksni_ol(callback.data or "", jami)


@router.callback_query(F.data.startswith("tamoyil:"))
async def tamoyil_detali(callback: CallbackQuery) -> None:
    jami = len(ovqatlanish.TAMOYILLAR)
    indeks = _indeksni_ol(callback, jami)
    if indeks is None:
        await callback.answer("Ma'lumot topilmadi", show_alert=True)
        return
    element = ovqatlanish.TAMOYILLAR[indeks]
    matn = (
        f"🥗 <b>{utils.xavfsiz(element['sarlavha'])}</b>\n\n"
        f"{utils.xavfsiz(element['matn'])}\n\n"
        f"ℹ️ {QISQA}"
    )
    await korinishni_yangila(
        callback,
        matn,
        _element_klaviaturasi("tamoyil", indeks, jami, "ovqat", "⬅️ Ro'yxatga qaytish"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ratsion:"))
async def ratsion_detali(callback: CallbackQuery) -> None:
    jami = len(ovqatlanish.RATSION)
    indeks = _indeksni_ol(callback, jami)
    if indeks is None:
        await callback.answer("Ma'lumot topilmadi", show_alert=True)
        return
    element = ovqatlanish.RATSION[indeks]
    matn = (
        f"🍽 <b>{utils.xavfsiz(element['sarlavha'])}</b>\n\n"
        f"{utils.xavfsiz(element['matn'])}\n\n"
        f"ℹ️ {QISQA}"
    )
    await korinishni_yangila(
        callback,
        matn,
        _element_klaviaturasi("ratsion", indeks, jami, "ovqat", "⬅️ Ro'yxatga qaytish"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("tabiiy:"))
async def tabiiy_detali(callback: CallbackQuery) -> None:
    jami = len(ovqatlanish.TABIIY_MAHSULOTLAR)
    indeks = _indeksni_ol(callback, jami)
    if indeks is None:
        await callback.answer("Ma'lumot topilmadi", show_alert=True)
        return
    element = ovqatlanish.TABIIY_MAHSULOTLAR[indeks]
    matn = (
        f"{element['emoji']} <b>{utils.xavfsiz(element['nom'])}</b>\n\n"
        f"🟢 <b>Foydasi:</b> {utils.xavfsiz(element['foyda'])}\n\n"
        f"🥣 <b>Qanday iste'mol qilinadi:</b> {utils.xavfsiz(element['istehmol'])}\n\n"
        f"ℹ️ {QISQA}"
    )
    await korinishni_yangila(
        callback,
        matn,
        _element_klaviaturasi("tabiiy", indeks, jami, "ovqat", "⬅️ Ro'yxatga qaytish"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("meva:"))
async def meva_detali(callback: CallbackQuery) -> None:
    jami = len(ensiklopediya.MEVALAR)
    indeks = _indeksni_ol(callback, jami)
    if indeks is None:
        await callback.answer("Ma'lumot topilmadi", show_alert=True)
        return
    element = ensiklopediya.MEVALAR[indeks]
    matn = _ensiklopediya_matni(element)
    await korinishni_yangila(
        callback,
        matn,
        _element_klaviaturasi("meva", indeks, jami, "ens_mevalar", "⬅️ Ro'yxatga qaytish"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("sabzavot:"))
async def sabzavot_detali(callback: CallbackQuery) -> None:
    jami = len(ensiklopediya.SABZAVOTLAR)
    indeks = _indeksni_ol(callback, jami)
    if indeks is None:
        await callback.answer("Ma'lumot topilmadi", show_alert=True)
        return
    element = ensiklopediya.SABZAVOTLAR[indeks]
    matn = _ensiklopediya_matni(element)
    await korinishni_yangila(
        callback,
        matn,
        _element_klaviaturasi(
            "sabzavot", indeks, jami, "ens_sabzavotlar", "⬅️ Ro'yxatga qaytish"
        ),
    )
    await callback.answer()


def _ensiklopediya_matni(element: dict) -> str:
    return (
        f"{element['emoji']} <b>{utils.xavfsiz(element['nom'])}</b>\n\n"
        f"💊 <b>Vitaminlar va minerallar:</b> {utils.xavfsiz(element['vitaminlar'])}\n\n"
        f"🟢 <b>Sog'liq uchun foydasi:</b> {utils.xavfsiz(element['foyda'])}\n\n"
        f"🥣 <b>Qanday iste'mol qilinadi:</b> {utils.xavfsiz(element['istehmol'])}\n\n"
        f"ℹ️ {QISQA}"
    )
