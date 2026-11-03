"""Asosiy menyu, yordam, qidiruv va kunlik maslahat bo'limlari."""

import random
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import db
import kb
import utils
from data import hayot, savollar
from handlers.yordamchi import korinishni_yangila

router = Router(name="umumiy")


class QidiruvHolati(StatesGroup):
    kutilmoqda = State()


def kunlik_maslahat_indeksi() -> int:
    """Bugungi maslahat indeksini qaytaradi (har kuni o'zgaradi)."""
    kun = datetime.now(config.TOSHKENT_VAQTI).timetuple().tm_yday
    return kun % len(hayot.KUNLIK_MASLAHATLAR)


def maslahat_klaviaturasi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Boshqa maslahat", callback_data="maslahat_boshqa")
    builder.button(text="✅ Kunlik odatlar", callback_data="odatlar")
    builder.button(text="📊 Haftalik hisobot", callback_data="hisobot")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def maslahat_matni(indeks: int | None = None) -> str:
    index = kunlik_maslahat_indeksi() if indeks is None else indeks
    maslahat = hayot.KUNLIK_MASLAHATLAR[index % len(hayot.KUNLIK_MASLAHATLAR)]
    return (
        "💡 <b>Kunlik sog'lom turmush maslahati</b>\n\n"
        f"🟢 {utils.xavfsiz(maslahat)}\n\n"
        f"ℹ️ {utils.xavfsiz(config.QISQA_OGOHLANTIRISH)}"
    )


def qidiruv_javobi(sorov: str) -> tuple[str, InlineKeyboardMarkup]:
    """Qidiruv natijalarini matn va tugmalar ko'rinishida tayyorlaydi."""
    natijalar = utils.qidirish(sorov, limit=5)

    if not natijalar:
        matn = (
            f"🔍 <b>{utils.xavfsiz(sorov)}</b> bo'yicha hech narsa topilmadi.\n\n"
            "Boshqa kalit so'z bilan urinib ko'ring. Masalan:\n"
            "• «olma», «vitamin C», «temir»\n"
            "• «nonushta», «shakar», «tuz»\n"
            "• «qo'l yuvish», «tish», «tozalik»\n"
            "• «qorin», «cho'zilish», «kardio»"
        )
        tugmalar = [
            ("🥗 Sog'lom ovqatlanish", "ovqat"),
            ("🍎 Meva va sabzavotlar", "ens"),
            ("🔁 Yana qidirish", "qidiruv"),
        ]
        return matn, kb.tugmalar_menyu(tugmalar)

    qismlar = [f"🔍 <b>{utils.xavfsiz(sorov)}</b> bo'yicha topilgan ma'lumotlar:\n"]
    builder = InlineKeyboardBuilder()
    for raqam, yozuv in enumerate(natijalar, start=1):
        bolim = utils.BOLIMLAR.get(yozuv["bolim"], yozuv["bolim"])
        qisqa = yozuv["matn"]
        if len(qisqa) > 230:
            qisqa = qisqa[:227] + "..."
        qismlar.append(f"{raqam}. <b>{utils.xavfsiz(yozuv['sarlavha'])}</b> — <i>{bolim}</i>")
        qismlar.append(utils.xavfsiz(qisqa))
        qismlar.append("")
        if yozuv["callback"]:
            sarlavha = yozuv["sarlavha"]
            builder.button(
                text=f"{raqam}. {sarlavha[:30]}", callback_data=yozuv["callback"]
            )

    builder.button(text="🔁 Yana qidirish", callback_data="qidiruv")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return "\n".join(qismlar).strip(), builder.as_markup()


@router.message(Command("start"))
async def start_buyrugi(message: Message, state: FSMContext) -> None:
    await state.clear()
    foydalanuvchi = message.from_user
    await db.foydalanuvchini_saqla(
        foydalanuvchi.id, foydalanuvchi.full_name, foydalanuvchi.username
    )
    matn = (
        f"Assalomu alaykum, <b>{utils.xavfsiz(foydalanuvchi.full_name)}</b>!\n\n"
        f"🟢 <b>{config.BOT_NOMI}</b> botiga xush kelibsiz.\n\n"
        "Bu bot sog'lom turmush tarzini o'rganish uchun yaratilgan:\n"
        "🥗 sog'lom va muvozanatli ovqatlanish\n"
        "🍎 meva-sabzavotlar ensiklopediyasi (vitaminlar va foyda)\n"
        "🏋️ ertalabki mashqlar va uy mashqlari\n"
        "🧼 shaxsiy gigiyena qoidalari\n"
        "💧 suv hisoblagichi va 😴 uyqu-faollik kuzatuvi\n"
        "⚖️ BMI va kunlik kaloriya kalkulyatori\n"
        f"📝 {len(savollar.SAVOLLAR)} ta o'quv testi va 🤖 AI yordamchi\n\n"
        "Kerakli bo'limni tanlang 👇"
    )
    await message.answer(matn, reply_markup=kb.bosh_menyu())


@router.message(Command("help"))
async def yordam_buyrugi(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(yordam_matni(), reply_markup=kb.bosh_menyu())


@router.message(Command("menyu"))
async def menyu_buyrugi(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🏠 Asosiy menyu. Kerakli bo'limni tanlang 👇", reply_markup=kb.bosh_menyu())


@router.message(Command("qidir"))
async def qidir_buyrugi(message: Message, state: FSMContext) -> None:
    await state.set_state(QidiruvHolati.kutilmoqda)
    await message.answer(
        "🔍 <b>Qidiruv</b>\n\n"
        "Kalit so'zni yozib yuboring. Masalan: <i>olma</i>, <i>vitamin C</i>, "
        "<i>nonushta</i>, <i>qo'l yuvish</i>, <i>qorin mashqi</i>.\n\n"
        "Bot butun bilim bazasidan (ovqatlanish, meva-sabzavotlar, mashqlar, "
        "gigiyena, test savollari) mos ma'lumotni topib beradi.",
        reply_markup=kb.bekor_klaviaturasi(),
    )


def yordam_matni() -> str:
    return (
        "❓ <b>Yordam</b>\n\n"
        "🔹 <b>Buyruqlar</b>\n"
        "/start — botni ishga tushirish\n"
        "/menyu — asosiy menyu\n"
        "/ovqat — sog'lom ovqatlanish bo'limi\n"
        "/mashq — mashq va gigiyena\n"
        "/suv — suv hisoblagichi\n"
        "/faollik — uyqu va faollik kuzatuvi\n"
        "/kalkulyator — BMI va kaloriya\n"
        "/test — o'quv testlarini boshlash\n"
        "/natijalar — test natijalari\n"
        "/odatlar — kunlik odatlar\n"
        "/ai — AI yordamchi\n"
        "/profil — shaxsiy profil\n"
        "/hisobot — haftalik hisobot\n"
        "/qidir — bilim bazasidan qidirish\n"
        "/maslahat — kunlik maslahat\n"
        "/help — yordam\n\n"
        "🔹 <b>Bo'limlar</b>\n"
        "🥗 <b>Ovqatlanish</b> — tamoyillar, ratsion, tabiiy mahsulotlar\n"
        "🍎 <b>Meva va sabzavotlar</b> — vitaminlar va foyda\n"
        "🏋️ <b>Mashq va gigiyena</b> — ertalabki mashqlar, uy mashqlari\n"
        "💧 <b>Suv</b> — kunlik suv hisoblagichi\n"
        "😴 <b>Uyqu va faollik</b> — uyqu, qadam, mashq va kayfiyat\n"
        "⚖️ <b>BMI va kaloriya</b> — shaxsiy ko'rsatkichlar\n"
        f"📝 <b>Testlar</b> — {len(savollar.SAVOLLAR)} ta o'quv savoli\n"
        "🤖 <b>AI yordamchi</b> — savolingizga javob\n"
        "✅ <b>Kunlik odatlar</b> — odatlar ro'yxati va kuzatuvi\n"
        "� <b>Haftalik hisobot</b> — 7 kunlik umumiy natija\n"
        "�👤 <b>Profil</b> — natijalar va yutuqlar\n\n"
        "🔍 <b>Bilim bazasi</b> — «olma», «vitamin C», «qo'l yuvish» kabi "
        "so'zlar bilan qidirish mumkin. Asosiy menyuga har bir bo'limdagi "
        "«🏠 Asosiy menyu» tugmasi orqali qaytish mumkin."
    )


def haqida_matni() -> str:
    return (
        f"ℹ️ <b>{config.BOT_NOMI}</b>\n\n"
        "Bu bot O'zbekistondagi foydalanuvchilar uchun sog'lom turmush tarzi "
        "bo'yicha ma'rifiy ma'lumot berish maqsadida yaratilgan.\n\n"
        f"📚 Bilim bazasi: {len(hayot.KUNLIK_ODATLAR)} ta kunlik odat, "
        f"{len(hayot.UY_MASHQLARI)} ta uy mashqi, "
        f"{len(hayot.KUNLIK_MASLAHATLAR)} ta maslahat va "
        f"{len(savollar.SAVOLLAR)} ta test savoli.\n"
        "🌐 Til: o'zbek tili (lotin yozuvi)\n"
        "🟢 Dizayn: yashil va oq ranglar, qulay tugmalar\n\n"
        f"{utils.xavfsiz(config.TIBBIY_OGOHLANTIRISH)}"
    )


@router.callback_query(F.data == "menyu")
async def menyu_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await korinishni_yangila(
        callback,
        "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang 👇",
        kb.bosh_menyu(),
    )
    await callback.answer()


@router.callback_query(F.data == "haqida")
async def haqida_callback(callback: CallbackQuery) -> None:
    await korinishni_yangila(callback, haqida_matni(), kb.bosh_menyu())
    await callback.answer()


@router.callback_query(F.data == "yordam")
async def yordam_callback(callback: CallbackQuery) -> None:
    await korinishni_yangila(callback, yordam_matni(), kb.bosh_menyu())
    await callback.answer()


@router.callback_query(F.data == "ogohlantirish")
async def ogohlantirish_callback(callback: CallbackQuery) -> None:
    await korinishni_yangila(
        callback, utils.xavfsiz(config.TIBBIY_OGOHLANTIRISH), kb.bosh_menyu()
    )
    await callback.answer()


@router.message(Command("maslahat"))
async def maslahat_buyrugi(message: Message) -> None:
    await message.answer(maslahat_matni(), reply_markup=maslahat_klaviaturasi())


@router.callback_query(F.data == "maslahat")
async def maslahat_callback(callback: CallbackQuery) -> None:
    await korinishni_yangila(callback, maslahat_matni(), maslahat_klaviaturasi())
    await callback.answer()


@router.callback_query(F.data == "maslahat_boshqa")
async def maslahat_boshqa(callback: CallbackQuery) -> None:
    await korinishni_yangila(
        callback, maslahat_matni(random.randrange(len(hayot.KUNLIK_MASLAHATLAR))),
        maslahat_klaviaturasi(),
    )
    await callback.answer("Yangi maslahat tayyor")


@router.callback_query(F.data == "qidiruv")
async def qidiruv_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(QidiruvHolati.kutilmoqda)
    await korinishni_yangila(
        callback,
        "🔍 <b>Qidiruv</b>\n\n"
        "Kalit so'zni yozib yuboring. Masalan: <i>anor</i>, <i>temir</i>, "
        "<i>suli</i>, <i>tish tozalash</i>, <i>qorin mashqi</i>.",
        kb.bekor_klaviaturasi(),
    )
    await callback.answer()


@router.message(QidiruvHolati.kutilmoqda, F.text)
async def qidiruv_matni(message: Message, state: FSMContext) -> None:
    matn, markup = qidiruv_javobi((message.text or "").strip())
    await state.clear()
    await message.answer(matn, reply_markup=markup)


@router.callback_query(F.data == "sahifa_bosh")
async def sahifa_bosh(callback: CallbackQuery) -> None:
    await callback.answer("Bu sahifa ko'rsatkichi 🙂")


@router.callback_query(F.data.startswith("pg:"))
async def sahifani_almashtirish(callback: CallbackQuery) -> None:
    qismlar = callback.data.split(":")
    if len(qismlar) != 3 or not qismlar[2].isdigit():
        await callback.answer("Sahifa topilmadi", show_alert=True)
        return
    funksiya = kb.SAHIFALAR.get(qismlar[1])
    if funksiya is None:
        await callback.answer("Bo'lim hali tayyor emas", show_alert=True)
        return
    matn, markup = funksiya(int(qismlar[2]))
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()
