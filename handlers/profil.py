"""Foydalanuvchi profili, natijalar va yutuqlar."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import db
import kb
import utils
from data import hayot
from handlers.yordamchi import korinishni_yangila

router = Router(name="profil")

QISQA = utils.xavfsiz(config.QISQA_OGOHLANTIRISH)

FAOLLIK_NOMLARI = {
    "kam": "🪑 Kam harakat",
    "yengil": "🚶 Yengil faollik",
    "orta": "🏃 O'rtacha faollik",
    "yuqori": "🏋️ Yuqori faollik",
}


def profil_klaviaturasi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⚖️ BMI va kaloriya", callback_data="kalkulyator")
    builder.button(text="💧 Suv hisoblagichi", callback_data="suv")
    builder.button(text="😴 Uyqu va faollik", callback_data="uyqu")
    builder.button(text="✅ Kunlik odatlar", callback_data="odatlar")
    builder.button(text="📝 Testlar", callback_data="testlar")
    builder.button(text="📊 Haftalik hisobot", callback_data="hisobot")
    builder.adjust(2, 2, 2)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def _yutuqlar(
    foydalanuvchi,
    stat: dict,
    suv_jami: int,
    bajarilgan: set[str],
    yozuvlar: list,
    maqsad: int,
) -> list[str]:
    yutuqlar: list[str] = []

    if (
        foydalanuvchi is not None
        and foydalanuvchi["boy"]
        and foydalanuvchi["vazn"]
        and foydalanuvchi["yosh"]
    ):
        yutuqlar.append("🎯 Profil ma'lumotlari to'ldirilgan")
    if stat["soni"] >= 1:
        yutuqlar.append("📝 Birinchi test topshirildi")
    if stat["soni"] >= 5:
        yutuqlar.append("🏆 5 ta test topshirildi")
    if stat["jami"] >= 10 and stat["foiz"] >= 80:
        yutuqlar.append("🥇 Testlarda 80%+ natija")
    if len(bajarilgan) >= 5:
        yutuqlar.append("✅ Bugun 5+ odat bajarildi")
    if maqsad and suv_jami >= maqsad * 3:
        yutuqlar.append("💧 Suv maqsadi bir necha kun bajarildi")

    mashq_kunlari = sum(
        1 for y in yozuvlar if y["mashq_daqiqa"] and y["mashq_daqiqa"] >= 20
    )
    if mashq_kunlari >= 3:
        yutuqlar.append("🏋️ Haftada 3+ kun mashq")

    uyqu_qiymatlari = [float(y["uyqu"]) for y in yozuvlar if y["uyqu"]]
    if uyqu_qiymatlari:
        orta_uyqu = sum(uyqu_qiymatlari) / len(uyqu_qiymatlari)
        if 7 <= orta_uyqu <= 9:
            yutuqlar.append("😴 Sog'lom uyqu rejimi")

    if not yutuqlar:
        yutuqlar.append("Boshlang: suv, mashq va testlardan foydalaning 💪")
    return yutuqlar


async def _profil_korinishi(user_id: int) -> tuple[str, InlineKeyboardMarkup]:
    foydalanuvchi = await db.foydalanuvchi(user_id)
    stat = await db.test_statistika(user_id)
    suv = await db.suv_hisobot(user_id, 7)
    bajarilgan = await db.odat_holati(user_id)
    yozuvlar = await db.faollik_royxati(user_id, 7)

    maqsad = 8
    if foydalanuvchi is not None and foydalanuvchi["suv_maqsad"]:
        maqsad = int(foydalanuvchi["suv_maqsad"])

    if foydalanuvchi is None:
        matn = (
            "👤 <b>Profil</b>\n\n"
            "Ma'lumotlar topilmadi. Iltimos, /start buyrug'ini yuboring."
        )
        return matn, kb.bosh_menyu()

    qatorlar = ["👤 <b>Shaxsiy profil</b>\n"]
    qatorlar.append(f"🪪 Ism: <b>{utils.xavfsiz(foydalanuvchi['ism'] or '—')}</b>")
    if foydalanuvchi["username"]:
        qatorlar.append(f"🔗 Username: @{utils.xavfsiz(foydalanuvchi['username'])}")

    # Asosiy ko'rsatkichlar
    if foydalanuvchi["yosh"]:
        qatorlar.append(f"🎂 Yosh: <b>{foydalanuvchi['yosh']}</b>")
    if foydalanuvchi["jins"]:
        qatorlar.append(f"⚧ Jins: <b>{utils.xavfsiz(foydalanuvchi['jins'])}</b>")
    if foydalanuvchi["boy"]:
        qatorlar.append(f"📏 Bo'y: <b>{utils.tanishtir_qiymat(foydalanuvchi['boy'], ' sm')}</b>")
    if foydalanuvchi["vazn"]:
        qatorlar.append(f"⚖️ Vazn: <b>{utils.tanishtir_qiymat(foydalanuvchi['vazn'], ' kg')}</b>")
    if foydalanuvchi["faollik"]:
        nom = FAOLLIK_NOMLARI.get(foydalanuvchi["faollik"], foydalanuvchi["faollik"])
        qatorlar.append(f"🏃 Faollik: <b>{utils.xavfsiz(nom)}</b>")

    # BMI
    if foydalanuvchi["boy"] and foydalanuvchi["vazn"]:
        bmi = utils.bmi_hisoblash(float(foydalanuvchi["boy"]), float(foydalanuvchi["vazn"]))
        toifa, _ = utils.bmi_toifasi(bmi)
        qatorlar.append(f"\n📊 BMI: <b>{bmi}</b> — <b>{utils.xavfsiz(toifa)}</b>")

    # Suv
    bugungi_suv = await db.suv_ol(user_id)
    qatorlar.append("\n💧 <b>Suv (7 kun)</b>")
    qatorlar.append(
        f"• Bugun: {bugungi_suv}/{maqsad} stakan\n"
        f"• O'rtacha: {suv['ortacha']} stakan/kun\n"
        f"• Jami: {suv['jami']} stakan"
    )

    # Uyqu va faollik
    uyqu_qiymatlari = [float(y["uyqu"]) for y in yozuvlar if y["uyqu"]]
    mashq_jami = sum(int(y["mashq_daqiqa"] or 0) for y in yozuvlar)
    qadam_jami = sum(int(y["qadam"] or 0) for y in yozuvlar)
    qatorlar.append("\n😴 <b>Uyqu va faollik (7 kun)</b>")
    if uyqu_qiymatlari:
        qatorlar.append(f"• O'rtacha uyqu: {round(sum(uyqu_qiymatlari) / len(uyqu_qiymatlari), 1)} soat")
    else:
        qatorlar.append("• O'rtacha uyqu: —")
    qatorlar.append(f"• Mashq: {mashq_jami} daqiqa")
    qatorlar.append(f"• Qadamlar: {qadam_jami} qadam")

    # Odatlar
    qatorlar.append(
        f"\n✅ <b>Kunlik odatlar</b>: bugun {len(bajarilgan)}/{len(hayot.KUNLIK_ODATLAR)} ta bajarildi"
    )

    # Testlar
    qatorlar.append("\n📝 <b>Testlar</b>")
    if stat["soni"]:
        qatorlar.append(
            f"• Topshirilgan: {stat['soni']} ta\n"
            f"• Umumiy natija: {stat['foiz']}%"
        )
    else:
        qatorlar.append("• Hali test topshirilmagan")

    # Yutuqlar
    yutuqlar = _yutuqlar(foydalanuvchi, stat, suv["jami"], bajarilgan, yozuvlar, maqsad)
    qatorlar.append("\n🏅 <b>Yutuqlar</b>")
    qatorlar.extend(f"• {yutuq}" for yutuq in yutuqlar)

    qatorlar.append("")
    qatorlar.append(f"ℹ️ {QISQA}")
    return "\n".join(qatorlar), profil_klaviaturasi()


@router.message(Command("profil"))
async def profil_buyrugi(message: Message) -> None:
    matn, markup = await _profil_korinishi(message.from_user.id)
    await message.answer(matn, reply_markup=markup)


@router.callback_query(F.data == "profil")
async def profil_callback(callback: CallbackQuery) -> None:
    matn, markup = await _profil_korinishi(callback.from_user.id)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()
