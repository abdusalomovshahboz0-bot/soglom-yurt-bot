"""Suv hisoblagichi, uyqu-faollik kuzatuvi va BMI/kaloriya kalkulyatori."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import db
import kb
import utils
from handlers.yordamchi import korinishni_yangila

router = Router(name="salomatlik")

QISQA = utils.xavfsiz(config.QISQA_OGOHLANTIRISH)
STANDART_SUV_MAQSADI = 8


class SuvHolati(StatesGroup):
    maqsad = State()


class FaollikHolati(StatesGroup):
    uyqu = State()
    qadam = State()
    mashq = State()
    kayfiyat = State()


class KalkulyatorHolati(StatesGroup):
    boy = State()
    vazn = State()
    yosh = State()


def _son(matn: str) -> float | None:
    """Matndan sonni ajratib oladi (vergul va nuqta bilan ham)."""
    tozalangan = (matn or "").strip().replace(",", ".")
    tozalangan = "".join(belgi for belgi in tozalangan if belgi.isdigit() or belgi == ".")
    if not tozalangan:
        return None
    try:
        return float(tozalangan)
    except ValueError:
        return None


def _suv_maqsadi(foydalanuvchi) -> int:
    if foydalanuvchi is not None and foydalanuvchi["suv_maqsad"]:
        return int(foydalanuvchi["suv_maqsad"])
    return STANDART_SUV_MAQSADI


# --- Suv hisoblagichi ---


def suv_klaviaturasi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ 1 stakan qo'shish", callback_data="suv_qosh")
    builder.button(text="➖ 1 stakan ayirish", callback_data="suv_kamayt")
    builder.button(text="🎯 Maqsadni o'zgartirish", callback_data="suv_maqsad")
    builder.button(text="📊 7 kunlik natija", callback_data="suv_hisobot")
    builder.adjust(2, 1, 1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def suv_matni(stakan: int, maqsad: int) -> str:
    foiz = round(stakan * 100 / maqsad) if maqsad else 0
    chiziq = utils.progress_bar(stakan, maqsad)
    if stakan >= maqsad:
        holat = "🎉 Ajoyib! Bugungi suv maqsadiga erishdingiz."
    elif foiz >= 50:
        holat = "👍 Yaxshi ketmoqda, davom eting!"
    else:
        holat = "💪 Yana suv ichishni unutmang."
    return (
        "💧 <b>Kunlik suv hisoblagichi</b>\n\n"
        f"Bugun ichilgan: <b>{stakan}</b> stakan\n"
        f"Maqsad: <b>{maqsad}</b> stakan ({foiz}%)\n\n"
        f"{chiziq}\n\n"
        f"{holat}\n\n"
        "ℹ️ 1 stakan ≈ 200 ml. Suv miqdorini asta-sekin oshirib borish tavsiya etiladi.\n"
        f"ℹ️ {QISQA}"
    )


async def _suv_korinishi(user_id: int) -> tuple[str, InlineKeyboardMarkup]:
    foydalanuvchi = await db.foydalanuvchi(user_id)
    maqsad = _suv_maqsadi(foydalanuvchi)
    stakan = await db.suv_ol(user_id)
    return suv_matni(stakan, maqsad), suv_klaviaturasi()


@router.message(Command("suv"))
async def suv_buyrugi(message: Message) -> None:
    matn, markup = await _suv_korinishi(message.from_user.id)
    await message.answer(matn, reply_markup=markup)


@router.callback_query(F.data == "suv")
async def suv_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    matn, markup = await _suv_korinishi(callback.from_user.id)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data == "suv_qosh")
async def suv_qosh(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    foydalanuvchi = await db.foydalanuvchi(user_id)
    maqsad = _suv_maqsadi(foydalanuvchi)
    stakan = await db.suv_qosh(user_id, 1)
    matn, markup = suv_matni(stakan, maqsad), suv_klaviaturasi()
    await korinishni_yangila(callback, matn, markup)
    if stakan == maqsad:
        await callback.answer("🎉 Maqsadga erishdingiz!")
    elif stakan > maqsad:
        await callback.answer("Maqsaddan oshdi 👍")
    else:
        await callback.answer(f"Yana {maqsad - stakan} stakan qoldi")


@router.callback_query(F.data == "suv_kamayt")
async def suv_kamayt(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    foydalanuvchi = await db.foydalanuvchi(user_id)
    maqsad = _suv_maqsadi(foydalanuvchi)
    stakan = await db.suv_qosh(user_id, -1)
    matn, markup = suv_matni(stakan, maqsad), suv_klaviaturasi()
    await korinishni_yangila(callback, matn, markup)
    await callback.answer("Kamaytirildi")


@router.callback_query(F.data == "suv_maqsad")
async def suv_maqsad(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SuvHolati.maqsad)
    await korinishni_yangila(
        callback,
        "🎯 <b>Kunlik suv maqsadi</b>\n\n"
        "Kuniga necha stakan suv ichishni maqsad qilib belgilaymiz?\n"
        "4 dan 20 gacha son kiriting (1 stakan ≈ 200 ml).",
        kb.bekor_klaviaturasi(),
    )
    await callback.answer()


@router.message(SuvHolati.maqsad, F.text)
async def suv_maqsad_qiymati(message: Message, state: FSMContext) -> None:
    qiymat = _son(message.text or "")
    if qiymat is None or not 4 <= qiymat <= 20:
        await message.answer(
            "❌ Iltimos, 4 dan 20 gacha butun son kiriting. Masalan: <b>8</b>",
            reply_markup=kb.bekor_klaviaturasi(),
        )
        return
    await db.maydonlarni_yangila(message.from_user.id, suv_maqsad=int(qiymat))
    await state.clear()
    matn, markup = await _suv_korinishi(message.from_user.id)
    await message.answer("✅ Maqsad saqlandi.\n\n" + matn, reply_markup=markup)


@router.callback_query(F.data == "suv_hisobot")
async def suv_hisobot(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    foydalanuvchi = await db.foydalanuvchi(user_id)
    maqsad = _suv_maqsadi(foydalanuvchi)
    hisobot = await db.suv_hisobot(user_id, 7)

    qatorlar = ["💧 <b>Oxirgi 7 kunlik suv natijalari</b>\n"]
    kunlar = {q["sana"]: int(q["stakan"]) for q in hisobot["kunlar"]}
    for oraliq in range(6, -1, -1):
        sana = db.kun_oldin(oraliq)
        stakan = kunlar.get(sana, 0)
        belgi = "🟢" if stakan >= maqsad else ("🟡" if stakan else "⚪️")
        qatorlar.append(
            f"{belgi} {utils.sana_chiroyli(sana)} ({utils.hafta_kuni(sana)}): "
            f"{stakan}/{maqsad} stakan"
        )
    qatorlar.append("")
    qatorlar.append(f"📊 Kunlik o'rtacha: <b>{hisobot['ortacha']}</b> stakan")
    qatorlar.append(f"🧮 Jami: <b>{hisobot['jami']}</b> stakan")
    qatorlar.append("")
    qatorlar.append(f"ℹ️ {QISQA}")

    builder = InlineKeyboardBuilder()
    builder.button(text="💧 Hisoblagichga qaytish", callback_data="suv")
    builder.button(text="📊 Haftalik hisobot", callback_data="hisobot")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())

    await korinishni_yangila(callback, "\n".join(qatorlar), builder.as_markup())
    await callback.answer()


# --- Uyqu va faollik kuzatuvi ---


def faollik_klaviaturasi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌙 Uyqu soatini kiritish", callback_data="uyqu_kirit")
    builder.button(text="👟 Qadamlar soni", callback_data="qadam_kirit")
    builder.button(text="🏋️ Mashq daqiqasi", callback_data="mashq_kirit")
    builder.button(text="🙂 Kayfiyatni belgilash", callback_data="kayfiyat_kirit")
    builder.button(text="📊 7 kunlik ko'rsatkichlar", callback_data="faollik_hisobot")
    builder.adjust(2, 2, 1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def _kayfiyat_matni(qiymat) -> str:
    nomlar = {
        1: "😔 Past",
        2: "😐 O'rtacha",
        3: "🙂 Yaxshi",
        4: "😃 Juda yaxshi",
        5: "🤩 Ajoyib",
    }
    if qiymat is None:
        return "—"
    return nomlar.get(int(qiymat), "—")


def faollik_matni(foydalanuvchi_ismi: str, yozuv) -> str:
    uyqu = yozuv["uyqu"] if yozuv is not None else None
    qadam = yozuv["qadam"] if yozuv is not None else None
    mashq = yozuv["mashq_daqiqa"] if yozuv is not None else None
    kayfiyat = yozuv["kayfiyat"] if yozuv is not None else None

    uyqu_holati = ""
    if uyqu is not None:
        if uyqu < 6:
            uyqu_holati = " (kam — 7-9 soat tavsiya etiladi)"
        elif uyqu <= 9:
            uyqu_holati = " (yaxshi ✅)"
        else:
            uyqu_holati = " (uzoq — 7-9 soat tavsiya etiladi)"

    return (
        f"😴 <b>Uyqu va faollik kuzatuvi</b>\n"
        f"👤 {utils.xavfsiz(foydalanuvchi_ismi)}\n\n"
        f"🌙 Uyqu: <b>{utils.tanishtir_qiymat(uyqu, ' soat')}</b>{uyqu_holati}\n"
        f"👟 Qadamlar: <b>{utils.tanishtir_qiymat(qadam)}</b>\n"
        f"🏋️ Mashq: <b>{utils.tanishtir_qiymat(mashq, ' daqiqa')}</b>\n"
        f"🙂 Kayfiyat: <b>{_kayfiyat_matni(kayfiyat)}</b>\n\n"
        "🟢 Maqsad: kuniga 7-9 soat uyqu, 6000+ qadam, 30 daqiqa faollik.\n\n"
        f"ℹ️ {QISQA}"
    )


async def _faollik_korinishi(user_id: int) -> tuple[str, InlineKeyboardMarkup]:
    foydalanuvchi = await db.foydalanuvchi(user_id)
    yozuv = await db.faollik_ol(user_id)
    ism = foydalanuvchi["ism"] if foydalanuvchi is not None else "Foydalanuvchi"
    return faollik_matni(ism, yozuv), faollik_klaviaturasi()


@router.message(Command("faollik"))
async def faollik_buyrugi(message: Message) -> None:
    matn, markup = await _faollik_korinishi(message.from_user.id)
    await message.answer(matn, reply_markup=markup)


@router.callback_query(F.data == "uyqu")
async def uyqu_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    matn, markup = await _faollik_korinishi(callback.from_user.id)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data == "uyqu_kirit")
async def uyqu_kirit(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FaollikHolati.uyqu)
    await korinishni_yangila(
        callback,
        "🌙 <b>Uyqu davomiyligi</b>\n\n"
        "Kechagi tunda necha soat uxlaganingizni kiriting (3 dan 14 gacha).\n"
        "Masalan: <b>7.5</b> yoki <b>8</b>",
        kb.bekor_klaviaturasi(),
    )
    await callback.answer()


@router.message(FaollikHolati.uyqu, F.text)
async def uyqu_qiymati(message: Message, state: FSMContext) -> None:
    qiymat = _son(message.text or "")
    if qiymat is None or not 3 <= qiymat <= 14:
        await message.answer(
            "❌ 3 dan 14 gacha son kiriting. Masalan: <b>7.5</b>",
            reply_markup=kb.bekor_klaviaturasi(),
        )
        return
    await db.faollik_yoz(message.from_user.id, uyqu=round(qiymat, 1))
    await state.clear()
    matn, markup = await _faollik_korinishi(message.from_user.id)
    await message.answer("✅ Uyqu saqlandi.\n\n" + matn, reply_markup=markup)


@router.callback_query(F.data == "qadam_kirit")
async def qadam_kirit(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FaollikHolati.qadam)
    await korinishni_yangila(
        callback,
        "👟 <b>Qadamlar soni</b>\n\n"
        "Bugun necha qadam bosganingizni kiriting (0 dan 100000 gacha).\n"
        "Masalan: <b>7500</b>",
        kb.bekor_klaviaturasi(),
    )
    await callback.answer()


@router.message(FaollikHolati.qadam, F.text)
async def qadam_qiymati(message: Message, state: FSMContext) -> None:
    qiymat = _son(message.text or "")
    if qiymat is None or not 0 <= qiymat <= 100000:
        await message.answer(
            "❌ 0 dan 100000 gacha son kiriting. Masalan: <b>7500</b>",
            reply_markup=kb.bekor_klaviaturasi(),
        )
        return
    await db.faollik_yoz(message.from_user.id, qadam=int(qiymat))
    await state.clear()
    matn, markup = await _faollik_korinishi(message.from_user.id)
    await message.answer("✅ Qadamlar saqlandi.\n\n" + matn, reply_markup=markup)


@router.callback_query(F.data == "mashq_kirit")
async def mashq_kirit(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FaollikHolati.mashq)
    await korinishni_yangila(
        callback,
        "🏋️ <b>Mashq daqiqasi</b>\n\n"
        "Bugun necha daqiqa jismoniy mashq qildingiz (0 dan 600 gacha).\n"
        "Masalan: <b>30</b>",
        kb.bekor_klaviaturasi(),
    )
    await callback.answer()


@router.message(FaollikHolati.mashq, F.text)
async def mashq_qiymati(message: Message, state: FSMContext) -> None:
    qiymat = _son(message.text or "")
    if qiymat is None or not 0 <= qiymat <= 600:
        await message.answer(
            "❌ 0 dan 600 gacha son kiriting. Masalan: <b>30</b>",
            reply_markup=kb.bekor_klaviaturasi(),
        )
        return
    await db.faollik_yoz(message.from_user.id, mashq_daqiqa=int(qiymat))
    await state.clear()
    matn, markup = await _faollik_korinishi(message.from_user.id)
    await message.answer("✅ Mashq vaqti saqlandi.\n\n" + matn, reply_markup=markup)


@router.callback_query(F.data == "kayfiyat_kirit")
async def kayfiyat_kirit(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FaollikHolati.kayfiyat)
    builder = InlineKeyboardBuilder()
    for qiymat, nom in (
        (1, "😔 Past"),
        (2, "😐 O'rtacha"),
        (3, "🙂 Yaxshi"),
        (4, "😃 Juda yaxshi"),
        (5, "🤩 Ajoyib"),
    ):
        builder.button(text=nom, callback_data=f"kayfiyat:{qiymat}")
    builder.adjust(2)
    builder.row(kb.asosiy_menyu_tugmasi())
    await korinishni_yangila(
        callback,
        "🙂 <b>Bugungi kayfiyatingiz qanday?</b>\n\nHolatingizni tanlang 👇",
        builder.as_markup(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("kayfiyat:"))
async def kayfiyat_saqlash(callback: CallbackQuery, state: FSMContext) -> None:
    qismlar = (callback.data or "").split(":")
    if len(qismlar) != 2 or not qismlar[1].isdigit():
        await callback.answer("Qiymat topilmadi", show_alert=True)
        return
    await db.faollik_yoz(callback.from_user.id, kayfiyat=int(qismlar[1]))
    await state.clear()
    matn, markup = await _faollik_korinishi(callback.from_user.id)
    await korinishni_yangila(callback, "✅ Kayfiyat saqlandi.\n\n" + matn, markup)
    await callback.answer("Saqlandi")


@router.callback_query(F.data == "faollik_hisobot")
async def faollik_hisobot(callback: CallbackQuery) -> None:
    yozuvlar = await db.faollik_royxati(callback.from_user.id, 7)
    kunlar = {q["sana"]: q for q in yozuvlar}
    qatorlar = ["📊 <b>Oxirgi 7 kunlik ko'rsatkichlar</b>\n"]
    uyqu_qiymatlari = []
    for oraliq in range(6, -1, -1):
        sana = db.kun_oldin(oraliq)
        yozuv = kunlar.get(sana)
        if yozuv is None:
            qatorlar.append(f"⚪️ {utils.sana_chiroyli(sana)}: ma'lumot yo'q")
            continue
        uyqu = yozuv["uyqu"]
        if uyqu is not None:
            uyqu_qiymatlari.append(float(uyqu))
        qatorlar.append(
            f"🟢 {utils.sana_chiroyli(sana)}: 💤 {utils.tanishtir_qiymat(uyqu, ' soat')} | "
            f"👟 {utils.tanishtir_qiymat(yozuv['qadam'])} | "
            f"🏋️ {utils.tanishtir_qiymat(yozuv['mashq_daqiqa'], ' daq')}"
        )
    qatorlar.append("")
    if uyqu_qiymatlari:
        qatorlar.append(
            f"🌙 O'rtacha uyqu: <b>{round(sum(uyqu_qiymatlari) / len(uyqu_qiymatlari), 1)} soat</b>"
        )
    qatorlar.append(f"ℹ️ {QISQA}")

    builder = InlineKeyboardBuilder()
    builder.button(text="😴 Kuzatuvga qaytish", callback_data="uyqu")
    builder.button(text="📊 Haftalik hisobot", callback_data="hisobot")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    await korinishni_yangila(callback, "\n".join(qatorlar), builder.as_markup())
    await callback.answer()


# --- BMI va kaloriya kalkulyatori ---


def kalkulyator_natijasi(malumot: dict) -> tuple[str, InlineKeyboardMarkup]:
    boy = float(malumot["boy"])
    vazn = float(malumot["vazn"])
    yosh = int(malumot["yosh"])
    jins = malumot["jins"]
    maqsad = malumot["maqsad"]
    faollik = malumot["faollik"]

    bmi = utils.bmi_hisoblash(boy, vazn)
    toifa, maslahat = utils.bmi_toifasi(bmi)
    past_vazn, yuqori_vazn = utils.sog_lom_vazn_oraligi(boy)
    bmr = utils.bmr_hisoblash(jins, vazn, boy, yosh)
    kaloriya = utils.kunlik_kaloriya(bmr, faollik, maqsad)
    suv = utils.suv_me_yori(vazn)

    matn = (
        "⚖️ <b>Shaxsiy sog'liq ko'rsatkichlari</b>\n\n"
        f"👤 Boy: <b>{boy:g} sm</b> | Vazn: <b>{vazn:g} kg</b>\n"
        f"🎂 Yosh: <b>{yosh}</b> | Jins: <b>{utils.xavfsiz(jins)}</b>\n"
        f"🏃 Faollik: <b>{utils.xavfsiz(kaloriya['faollik_nomi'])}</b>\n\n"
        f"📊 <b>BMI (tana massasi indeksi):</b> {bmi}\n"
        f"🟢 Holat: <b>{utils.xavfsiz(toifa)}</b> — {utils.xavfsiz(maslahat)}\n"
        f"⚖️ Sog'lom vazn oralig'i: <b>{past_vazn} - {yuqori_vazn} kg</b>\n\n"
        f"🔥 Bazal metabolizm (BMR): <b>{round(bmr)} kkal</b>\n"
        f"🍽 Vaznni saqlash uchun: <b>{kaloriya['saqlash']} kkal/kun</b>\n"
        f"🎯 Maqsad ({utils.xavfsiz(kaloriya['maqsad_nomi'])}): "
        f"<b>{kaloriya['tavsiya']} kkal/kun</b>\n"
        f"   Taxminiy oraliq: {kaloriya['past']} - {kaloriya['yuqori']} kkal\n\n"
        f"💧 Kunlik suv tavsiyasi: <b>{suv} stakan</b> (taxminan)\n\n"
        f"ℹ️ {utils.xavfsiz(config.QISQA_OGOHLANTIRISH)}"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="💧 Suv maqsadiga qo'llash", callback_data="suv_maqsad_qollash")
    builder.button(text="🔁 Qayta hisoblash", callback_data="kalkulyator_qayta")
    builder.button(text="👤 Profilim", callback_data="profil")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return matn, builder.as_markup()


def jins_klaviaturasi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👨 Erkak", callback_data="jins:Erkak")
    builder.button(text="👩 Ayol", callback_data="jins:Ayol")
    builder.adjust(2)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def maqsad_klaviaturasi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⚖️ Vaznni saqlash", callback_data="maqsad:saqlash")
    builder.button(text="📉 Vaznni kamaytirish", callback_data="maqsad:kamaytirish")
    builder.button(text="📈 Vaznni oshirish", callback_data="maqsad:oshirish")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def faollik_darajasi_klaviaturasi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🪑 Kam harakat (o'tirib ishlash)", callback_data="faollik:kam")
    builder.button(text="🚶 Yengil faollik (haftada 1-3 mashq)", callback_data="faollik:yengil")
    builder.button(text="🏃 O'rtacha faollik (haftada 3-5 mashq)", callback_data="faollik:orta")
    builder.button(text="🏋️ Yuqori faollik (haftada 6-7 mashq)", callback_data="faollik:yuqori")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


async def _natijani_korsat(callback: CallbackQuery, malumot: dict) -> None:
    """Hisob-kitob natijasini ko'rsatadi va profilga saqlaydi."""
    await db.maydonlarni_yangila(
        callback.from_user.id,
        yosh=int(malumot["yosh"]),
        jins=malumot["jins"],
        boy=float(malumot["boy"]),
        vazn=float(malumot["vazn"]),
        maqsad=malumot["maqsad"],
        faollik=malumot["faollik"],
    )
    matn, markup = kalkulyator_natijasi(malumot)
    await korinishni_yangila(callback, matn, markup)


@router.message(Command("kalkulyator"))
async def kalkulyator_buyrugi(message: Message, state: FSMContext) -> None:
    await state.clear()
    foydalanuvchi = await db.foydalanuvchi(message.from_user.id)
    if (
        foydalanuvchi is not None
        and foydalanuvchi["boy"]
        and foydalanuvchi["vazn"]
        and foydalanuvchi["yosh"]
    ):
        malumot = {
            "boy": foydalanuvchi["boy"],
            "vazn": foydalanuvchi["vazn"],
            "yosh": foydalanuvchi["yosh"],
            "jins": foydalanuvchi["jins"] or "Erkak",
            "maqsad": foydalanuvchi["maqsad"] or "saqlash",
            "faollik": foydalanuvchi["faollik"] or "orta",
        }
        matn, markup = kalkulyator_natijasi(malumot)
        await message.answer(matn, reply_markup=markup)
        return
    await state.set_state(KalkulyatorHolati.boy)
    await message.answer(
        "⚖️ <b>BMI va kaloriya kalkulyatori</b>\n\n"
        "Bo'yingizni santimetrda kiriting (100 dan 250 gacha).\n"
        "Masalan: <b>175</b>",
        reply_markup=kb.bekor_klaviaturasi(),
    )


@router.callback_query(F.data == "kalkulyator")
async def kalkulyator_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    foydalanuvchi = await db.foydalanuvchi(callback.from_user.id)
    if (
        foydalanuvchi is not None
        and foydalanuvchi["boy"]
        and foydalanuvchi["vazn"]
        and foydalanuvchi["yosh"]
    ):
        malumot = {
            "boy": foydalanuvchi["boy"],
            "vazn": foydalanuvchi["vazn"],
            "yosh": foydalanuvchi["yosh"],
            "jins": foydalanuvchi["jins"] or "Erkak",
            "maqsad": foydalanuvchi["maqsad"] or "saqlash",
            "faollik": foydalanuvchi["faollik"] or "orta",
        }
        matn, markup = kalkulyator_natijasi(malumot)
        await korinishni_yangila(callback, matn, markup)
        await callback.answer()
        return

    await state.set_state(KalkulyatorHolati.boy)
    await korinishni_yangila(
        callback,
        "⚖️ <b>BMI va kaloriya kalkulyatori</b>\n\n"
        "Bu hisob-kitob 4 bosqichdan iborat.\n\n"
        "1️⃣ Bo'yingizni santimetrda kiriting (100-250).\nMasalan: <b>175</b>",
        kb.bekor_klaviaturasi(),
    )
    await callback.answer()


@router.callback_query(F.data == "kalkulyator_qayta")
async def kalkulyator_qayta(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(KalkulyatorHolati.boy)
    await korinishni_yangila(
        callback,
        "1️⃣ Bo'yingizni santimetrda kiriting (100-250).\nMasalan: <b>175</b>",
        kb.bekor_klaviaturasi(),
    )
    await callback.answer()


@router.message(KalkulyatorHolati.boy, F.text)
async def kalkulyator_boy(message: Message, state: FSMContext) -> None:
    qiymat = _son(message.text or "")
    if qiymat is None or not 100 <= qiymat <= 250:
        await message.answer(
            "❌ Bo'yni 100 dan 250 gacha santimetrda kiriting. Masalan: <b>175</b>",
            reply_markup=kb.bekor_klaviaturasi(),
        )
        return
    await state.update_data(boy=qiymat)
    await state.set_state(KalkulyatorHolati.vazn)
    await message.answer(
        "2️⃣ Vazningizni kilogrammda kiriting (25-300).\nMasalan: <b>70</b>",
        reply_markup=kb.bekor_klaviaturasi(),
    )


@router.message(KalkulyatorHolati.vazn, F.text)
async def kalkulyator_vazn(message: Message, state: FSMContext) -> None:
    qiymat = _son(message.text or "")
    if qiymat is None or not 25 <= qiymat <= 300:
        await message.answer(
            "❌ Vaznni 25 dan 300 gacha kilogrammda kiriting. Masalan: <b>70</b>",
            reply_markup=kb.bekor_klaviaturasi(),
        )
        return
    await state.update_data(vazn=qiymat)
    await state.set_state(KalkulyatorHolati.yosh)
    await message.answer(
        "3️⃣ Yoshingizni kiriting (5-100).\nMasalan: <b>30</b>",
        reply_markup=kb.bekor_klaviaturasi(),
    )


@router.message(KalkulyatorHolati.yosh, F.text)
async def kalkulyator_yosh(message: Message, state: FSMContext) -> None:
    qiymat = _son(message.text or "")
    if qiymat is None or not 5 <= qiymat <= 100:
        await message.answer(
            "❌ Yoshni 5 dan 100 gacha kiriting. Masalan: <b>30</b>",
            reply_markup=kb.bekor_klaviaturasi(),
        )
        return
    await state.update_data(yosh=int(qiymat))
    await message.answer(
        "4️⃣ Jinsingizni tanlang 👇", reply_markup=jins_klaviaturasi()
    )


@router.callback_query(F.data.startswith("jins:"))
async def jins_tanlash(callback: CallbackQuery, state: FSMContext) -> None:
    jins = (callback.data or "").split(":", 1)[-1]
    if jins not in {"Erkak", "Ayol"}:
        await callback.answer("Qiymat noto'g'ri", show_alert=True)
        return
    await state.update_data(jins=jins)
    await callback.message.answer(
        f"Jins: <b>{utils.xavfsiz(jins)}</b>\n\nMaqsadingizni tanlang 👇",
        reply_markup=maqsad_klaviaturasi(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("maqsad:"))
async def maqsad_tanlash(callback: CallbackQuery, state: FSMContext) -> None:
    maqsad = (callback.data or "").split(":", 1)[-1]
    if maqsad not in utils.MAQSADLAR:
        await callback.answer("Qiymat noto'g'ri", show_alert=True)
        return
    await state.update_data(maqsad=maqsad)
    await callback.message.answer(
        f"Maqsad: <b>{utils.xavfsiz(utils.MAQSADLAR[maqsad][0])}</b>\n\n"
        "Kunlik faollik darajangizni tanlang 👇",
        reply_markup=faollik_darajasi_klaviaturasi(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("faollik:"))
async def faollik_tanlash(callback: CallbackQuery, state: FSMContext) -> None:
    faollik = (callback.data or "").split(":", 1)[-1]
    if faollik not in utils.FAOLLIK_DARAJALARI:
        await callback.answer("Qiymat noto'g'ri", show_alert=True)
        return

    malumotlar = await state.get_data()
    jins = malumotlar.get("jins") or "Erkak"
    maqsad = malumotlar.get("maqsad") or "saqlash"
    boy = malumotlar.get("boy")
    vazn = malumotlar.get("vazn")
    yosh = malumotlar.get("yosh")

    if not (boy and vazn and yosh):
        await callback.answer("Ma'lumotlar to'liq emas, qaytadan boshlang", show_alert=True)
        await state.clear()
        return

    await state.clear()
    await _natijani_korsat(
        callback,
        {
            "boy": boy,
            "vazn": vazn,
            "yosh": yosh,
            "jins": jins,
            "maqsad": maqsad,
            "faollik": faollik,
        },
    )
    await callback.answer("Hisoblandi")


@router.callback_query(F.data == "suv_maqsad_qollash")
async def suv_maqsad_qollash(callback: CallbackQuery) -> None:
    foydalanuvchi = await db.foydalanuvchi(callback.from_user.id)
    if foydalanuvchi is None or not foydalanuvchi["vazn"]:
        await callback.answer(
            "Avval vazn ma'lumotini kiriting", show_alert=True
        )
        return
    yangi_maqsad = utils.suv_me_yori(float(foydalanuvchi["vazn"]))
    await db.maydonlarni_yangila(callback.from_user.id, suv_maqsad=yangi_maqsad)
    await callback.answer(f"✅ Suv maqsadi {yangi_maqsad} stakanga o'zgartirildi")
