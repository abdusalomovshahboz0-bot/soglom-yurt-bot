"""Telegram inline klaviaturalari va sahifalash tizimi."""

from typing import Callable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config

# Sahifalanadigan bo'limlar: "prefix" -> funksiya(sahifa) -> (matn, markup)
SAHIFALAR: dict[str, Callable[[int], tuple[str, InlineKeyboardMarkup]]] = {}


def sahifa_royxat(prefix: str):
    """Sahifa ko'rsatuvchi funksiyani ro'yxatga oluvchi dekorator."""

    def orash(funksiya: Callable[[int], tuple[str, InlineKeyboardMarkup]]):
        SAHIFALAR[prefix] = funksiya
        return funksiya

    return orash


def asosiy_menyu_tugmasi() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="menyu")


def bosh_menyu() -> InlineKeyboardMarkup:
    """Botning asosiy menyusi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🥗 Sog'lom ovqatlanish", callback_data="ovqat")
    builder.button(text="🍎 Meva va sabzavotlar", callback_data="ens")
    builder.button(text="🏋️ Mashq va gigiyena", callback_data="harakat")
    builder.button(text="💧 Suv hisoblagichi", callback_data="suv")
    builder.button(text="😴 Uyqu va faollik", callback_data="uyqu")
    builder.button(text="⚖️ BMI va kaloriya", callback_data="kalkulyator")
    builder.button(text="📝 Testlar (100 savol)", callback_data="testlar")
    builder.button(text="🤖 AI yordamchi", callback_data="ai")
    builder.button(text="✅ Kunlik odatlar", callback_data="odatlar")
    builder.button(text="💡 Kunlik maslahat", callback_data="maslahat")
    builder.button(text="👤 Profil va natijalar", callback_data="profil")
    builder.button(text="📊 Haftalik hisobot", callback_data="hisobot")
    builder.button(text="🔍 Qidiruv", callback_data="qidiruv")
    builder.button(text="ℹ️ Bot haqida", callback_data="haqida")
    builder.button(text="❓ Yordam", callback_data="yordam")
    builder.button(text="⚠️ Tibbiy ogohlantirish", callback_data="ogohlantirish")
    builder.adjust(2)
    return builder.as_markup()


def tugmalar_menyu(
    tugmalar: list[tuple[str, str]],
    ortga: str | None = "menyu",
    ortga_matni: str = "⬅️ Orqaga",
    ustun: int = 1,
) -> InlineKeyboardMarkup:
    """Oddiy tugmalar menyusi."""
    builder = InlineKeyboardBuilder()
    for matn, callback in tugmalar:
        builder.button(text=matn, callback_data=callback)
    if tugmalar:
        builder.adjust(ustun)
    if ortga:
        builder.row(
            asosiy_menyu_tugmasi()
            if ortga == "menyu"
            else InlineKeyboardButton(text=ortga_matni, callback_data=ortga)
        )
        if ortga != "menyu":
            builder.row(asosiy_menyu_tugmasi())
    return builder.as_markup()


def sahifali_royxat(
    elementlar: list[tuple[str, str]],
    prefix: str,
    sahifa: int = 0,
    har_sahifa: int | None = None,
    ortga: str = "menyu",
    ortga_matni: str = "🏠 Asosiy menyu",
) -> InlineKeyboardMarkup:
    """Ko'p elementli ro'yxatni sahifalab ko'rsatadi."""
    har_sahifa = har_sahifa or config.SAHIFA_HAJMI
    jami_sahifa = max(1, -(-len(elementlar) // har_sahifa))
    sahifa = max(0, min(sahifa, jami_sahifa - 1))

    builder = InlineKeyboardBuilder()
    boshlanish = sahifa * har_sahifa
    for matn, callback in elementlar[boshlanish : boshlanish + har_sahifa]:
        builder.button(text=matn, callback_data=callback)
    if elementlar:
        builder.adjust(1)

    if jami_sahifa > 1:
        navigatsiya = []
        if sahifa > 0:
            navigatsiya.append(
                InlineKeyboardButton(
                    text="⬅️ Oldingi", callback_data=f"pg:{prefix}:{sahifa - 1}"
                )
            )
        navigatsiya.append(
            InlineKeyboardButton(
                text=f"📄 {sahifa + 1}/{jami_sahifa}", callback_data="sahifa_bosh"
            )
        )
        if sahifa + 1 < jami_sahifa:
            navigatsiya.append(
                InlineKeyboardButton(
                    text="Keyingi ➡️", callback_data=f"pg:{prefix}:{sahifa + 1}"
                )
            )
        builder.row(*navigatsiya)

    builder.row(
        asosiy_menyu_tugmasi()
        if ortga == "menyu"
        else InlineKeyboardButton(text=ortga_matni, callback_data=ortga)
    )
    return builder.as_markup()


def element_klaviaturasi(
    prefix: str, indeks: int, jami: int, ortga: str, ortga_matni: str
) -> InlineKeyboardMarkup:
    """Ro'yxat elementlari orasida oldinga/orqaga yurish klaviaturasi."""
    builder = InlineKeyboardBuilder()
    if jami > 1:
        builder.row(
            InlineKeyboardButton(
                text="⬅️ Oldingi", callback_data=f"{prefix}:{(indeks - 1) % jami}"
            ),
            InlineKeyboardButton(text=f"{indeks + 1}/{jami}", callback_data="sahifa_bosh"),
            InlineKeyboardButton(
                text="Keyingi ➡️", callback_data=f"{prefix}:{(indeks + 1) % jami}"
            ),
        )
    builder.row(
        asosiy_menyu_tugmasi()
        if ortga == "menyu"
        else InlineKeyboardButton(text=ortga_matni, callback_data=ortga)
    )
    if ortga != "menyu":
        builder.row(asosiy_menyu_tugmasi())
    return builder.as_markup()


def variantlar_klaviaturasi(
    variantlar: list[str],
    savol_indeksi: int,
    harflar: tuple[str, ...] = ("A", "B", "C", "D", "E", "F"),
) -> InlineKeyboardMarkup:
    """Test savoli variantlarining klaviaturasi."""
    builder = InlineKeyboardBuilder()
    for indeks, variant in enumerate(variantlar):
        harf = harflar[indeks] if indeks < len(harflar) else str(indeks + 1)
        builder.button(
            text=f"{harf}) {variant}", callback_data=f"javob:{savol_indeksi}:{indeks}"
        )
    builder.adjust(1)
    return builder.as_markup()


def test_yakun_klaviaturasi() -> InlineKeyboardMarkup:
    """Test tugagach ko'rsatiladigan tugmalar."""
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Yana test", callback_data="testlar")
    builder.button(text="🏆 Natijalarim", callback_data="test_natijalar")
    builder.button(text="✅ Kunlik odatlar", callback_data="odatlar")
    builder.adjust(1)
    builder.row(asosiy_menyu_tugmasi())
    return builder.as_markup()


def ha_yoq_klaviaturasi(callback: str, ortga: str = "menyu") -> InlineKeyboardMarkup:
    """Tasdiqlash klaviaturasi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Ha", callback_data=callback)
    builder.button(text="❌ Yo'q", callback_data=ortga)
    builder.adjust(2)
    return builder.as_markup()


def bekor_klaviaturasi() -> InlineKeyboardMarkup:
    """Kiritishni bekor qilish tugmasi."""
    builder = InlineKeyboardBuilder()
    builder.row(asosiy_menyu_tugmasi())
    return builder.as_markup()


def indeksni_ol(callback_data: str, jami: int) -> int | None:
    """Callback ma'lumotidan element indeksini xavfsiz ajratib oladi."""
    qismlar = callback_data.split(":")
    if len(qismlar) != 2 or not qismlar[1].isdigit():
        return None
    indeks = int(qismlar[1])
    return indeks if 0 <= indeks < jami else None
