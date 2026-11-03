"""Haftalik sog'lom turmush tarzi hisoboti."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import db
import kb
import utils
from handlers.yordamchi import korinishni_yangila

router = Router(name="hisobot")

QISQA = utils.xavfsiz(config.QISQA_OGOHLANTIRISH)


def hisobot_klaviaturasi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💧 Suv hisoblagichi", callback_data="suv")
    builder.button(text="😴 Uyqu va faollik", callback_data="uyqu")
    builder.button(text="✅ Kunlik odatlar", callback_data="odatlar")
    builder.button(text="👤 Profilim", callback_data="profil")
    builder.adjust(2, 2)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def _baholash(ball: int) -> str:
    if ball >= 85:
        return "🏆 Zo'r hafta! Sog'lom odatlaringiz mustahkam."
    if ball >= 65:
        return "🥇 Yaxshi hafta. Yana bir oz kuch qoldi!"
    if ball >= 40:
        return "👍 O'rtacha hafta. Ba'zi odatlarni kuchaytirish mumkin."
    return "💪 Boshlanish yaxshi. Kichik qadamlar bilan davom eting."


async def _hisobot_korinishi(user_id: int) -> tuple[str, InlineKeyboardMarkup]:
    foydalanuvchi = await db.foydalanuvchi(user_id)
    maqsad = 8
    if foydalanuvchi is not None and foydalanuvchi["suv_maqsad"]:
        maqsad = int(foydalanuvchi["suv_maqsad"])

    suv = await db.suv_hisobot(user_id, 7)
    yozuvlar = await db.faollik_royxati(user_id, 7)
    odat = await db.odat_hisobot(user_id, 7)
    stat = await db.test_statistika(user_id)

    suv_kunlari = {q["sana"]: int(q["stakan"]) for q in suv["kunlar"]}
    faollik_kunlari = {y["sana"]: y for y in yozuvlar}
    odat_kunlari = odat["kunlar"]

    # Kunlik jadval
    qatorlar = ["📊 <b>Haftalik hisobot (7 kun)</b>\n"]
    for oraliq in range(6, -1, -1):
        sana = db.kun_oldin(oraliq)
        stakan = suv_kunlari.get(sana, 0)
        yozuv = faollik_kunlari.get(sana)
        uyqu = yozuv["uyqu"] if yozuv is not None else None
        mashq = yozuv["mashq_daqiqa"] if yozuv is not None else None
        soni = odat_kunlari.get(sana, 0)

        belgi = "🟢" if stakan >= maqsad else ("🟡" if stakan else "⚪️")
        qatorlar.append(
            f"{belgi} {utils.sana_chiroyli(sana)} ({utils.hafta_kuni(sana)})\n"
            f"     💧 {stakan}/{maqsad} | 💤 {utils.tanishtir_qiymat(uyqu, ' soat')} | "
            f"🏋️ {utils.tanishtir_qiymat(mashq, ' daq')} | ✅ {soni}"
        )

    # Umumiy ko'rsatkichlar
    uyqu_qiymatlari = [float(y["uyqu"]) for y in yozuvlar if y["uyqu"]]
    uyqu_orta = (
        round(sum(uyqu_qiymatlari) / len(uyqu_qiymatlari), 1) if uyqu_qiymatlari else None
    )
    mashq_kunlari = sum(
        1 for y in yozuvlar if y["mashq_daqiqa"] and y["mashq_daqiqa"] >= 20
    )
    qadam_jami = sum(int(y["qadam"] or 0) for y in yozuvlar)
    odat_orta = round(odat["jami"] / 7, 1)

    qatorlar.append("\n📈 <b>Umumiy ko'rsatkichlar</b>")
    qatorlar.append(f"• 💧 Suv: kuniga o'rtacha {suv['ortacha']} stakan (jami {suv['jami']})")
    if uyqu_orta is not None:
        qatorlar.append(f"• 💤 Uyqu: kuniga o'rtacha {uyqu_orta} soat")
    else:
        qatorlar.append("• 💤 Uyqu: ma'lumot yo'q")
    qatorlar.append(f"• 🏋️ Mashq: {mashq_kunlari} kun (20+ daqiqa)")
    qatorlar.append(f"• 👟 Qadamlar: jami {qadam_jami}")
    qatorlar.append(f"• ✅ Odatlar: kuniga o'rtacha {odat_orta} ta")
    if stat["soni"]:
        qatorlar.append(f"• 📝 Testlar: {stat['soni']} ta, natija {stat['foiz']}%")

    # Ball hisoblash (har bir yo'nalish 25 balldan)
    suv_ball = 25 * min(1.0, suv["ortacha"] / maqsad) if maqsad else 0.0
    if uyqu_orta is None:
        uyqu_ball = 0.0
    elif 7 <= uyqu_orta <= 9:
        uyqu_ball = 25.0
    else:
        uyqu_ball = 15.0
    faollik_ball = 25 * min(1.0, mashq_kunlari / 5)
    odat_ball = 25 * min(1.0, odat_orta / 6)
    umumiy = round(suv_ball + uyqu_ball + faollik_ball + odat_ball)

    qatorlar.append(f"\n🎯 <b>Sog'lom turmush bahosi: {umumiy}/100</b>")
    qatorlar.append(utils.progress_bar(umumiy, 100))
    qatorlar.append(f"{_baholash(umumiy)}")
    qatorlar.append("")
    qatorlar.append(f"ℹ️ {QISQA}")

    return "\n".join(qatorlar), hisobot_klaviaturasi()


@router.message(Command("hisobot"))
async def hisobot_buyrugi(message: Message) -> None:
    matn, markup = await _hisobot_korinishi(message.from_user.id)
    await message.answer(matn, reply_markup=markup)


@router.callback_query(F.data == "hisobot")
async def hisobot_callback(callback: CallbackQuery) -> None:
    matn, markup = await _hisobot_korinishi(callback.from_user.id)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()
