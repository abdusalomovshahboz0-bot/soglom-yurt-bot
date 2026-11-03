"""100 ta savoldan iborat o'quv testlari tizimi."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
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
from data import savollar
from handlers.yordamchi import korinishni_yangila

router = Router(name="testlar")

QISQA = utils.xavfsiz(config.QISQA_OGOHLANTIRISH)
HARFLAR = ("A", "B", "C", "D", "E", "F")
BARCHASI = "barchasi"


class TestHolati(StatesGroup):
    faol = State()


def _kategoriya_nomi(kalit: str) -> str:
    if kalit == BARCHASI:
        return "🧭 Barcha yo'nalishlar"
    return savollar.KATEGORIYALAR.get(kalit, kalit)


def test_menyusi() -> InlineKeyboardMarkup:
    """Test yo'nalishini tanlash klaviaturasi."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"🧭 Barcha savollar ({len(savollar.SAVOLLAR)} ta)",
        callback_data=f"test_kategoriya:{BARCHASI}",
    )
    for kalit, nom in savollar.KATEGORIYALAR.items():
        soni = sum(1 for s in savollar.SAVOLLAR if s["kategoriya"] == kalit)
        builder.button(text=f"{nom} ({soni} ta)", callback_data=f"test_kategoriya:{kalit}")
    builder.button(text="🏆 Natijalarim", callback_data="test_natijalar")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


def test_sarlavhasi() -> str:
    return (
        "📝 <b>Sog'liq bo'yicha o'quv testlari</b>\n\n"
        f"Bilim bazasida jami <b>{len(savollar.SAVOLLAR)}</b> ta savol mavjud. "
        "Har bir savolda to'g'ri javob izohi bilan ko'rsatiladi.\n\n"
        "Yo'nalishni tanlang 👇\n\n"
        f"ℹ️ {QISQA}"
    )


def _savol_korinishi(indekslar: list[int], pos: int) -> tuple[str, InlineKeyboardMarkup]:
    """Bitta savol ekranini tayyorlaydi."""
    savol = savollar.SAVOLLAR[indekslar[pos]]
    jami = len(indekslar)
    chiziq = utils.progress_bar(pos, jami)

    matn = (
        f"📝 <b>{pos + 1}-savol / {jami}</b>\n"
        f"{chiziq}\n\n"
        f"{utils.xavfsiz(savol['savol'])}"
    )

    builder = InlineKeyboardBuilder()
    for indeks, variant in enumerate(savol["variantlar"]):
        harf = HARFLAR[indeks] if indeks < len(HARFLAR) else str(indeks + 1)
        builder.button(
            text=f"{harf}) {variant}", callback_data=f"javob:{pos}:{indeks}"
        )
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="menyu"))
    return matn, builder.as_markup()


def _baholash(foiz: int) -> str:
    if foiz >= 90:
        return "🏆 Ajoyib natija!"
    if foiz >= 70:
        return "🥇 Yaxshi natija!"
    if foiz >= 50:
        return "👍 O'rtacha natija."
    return "💪 Yana mashq qilish foydali."


async def _testni_yakunlash(
    callback: CallbackQuery, kategoriya: str, jami: int, togri: int
) -> tuple[str, InlineKeyboardMarkup]:
    """Test natijasini saqlaydi va yakuniy ekranni qaytaradi."""
    await db.test_yoz(callback.from_user.id, kategoriya, togri, jami)
    foiz = round(togri * 100 / jami) if jami else 0
    matn = (
        "🏁 <b>Test yakunlandi!</b>\n\n"
        f"🗂 Yo'nalish: <b>{utils.xavfsiz(_kategoriya_nomi(kategoriya))}</b>\n"
        f"✅ To'g'ri javoblar: <b>{togri}/{jami}</b>\n"
        f"📊 Natija: <b>{foiz}%</b>\n\n"
        f"{utils.progress_bar(togri, jami)}\n\n"
        f"{_baholash(foiz)}\n\n"
        "Natijangiz saqlandi va «🏆 Natijalarim» bo'limida ko'rinadi.\n\n"
        f"ℹ️ {QISQA}"
    )
    return matn, kb.test_yakun_klaviaturasi()


async def _natijalar_korinishi(user_id: int) -> tuple[str, InlineKeyboardMarkup]:
    stat = await db.test_statistika(user_id)
    builder = InlineKeyboardBuilder()

    if not stat["soni"]:
        matn = (
            "🏆 <b>Natijalarim</b>\n\n"
            "Hali test topshirmagansiz. Testlar bilimingizni sinashga va "
            "foydali ma'lumotlarni eslab qolishga yordam beradi.\n\n"
            "Boshlash uchun «📝 Testni boshlash» tugmasini bosing 👇"
        )
        builder.button(text="📝 Testni boshlash", callback_data="testlar")
        builder.adjust(1)
        builder.row(kb.asosiy_menyu_tugmasi())
        return matn, builder.as_markup()

    qatorlar = [
        "🏆 <b>Test natijalarim</b>\n",
        f"📝 Topshirilgan testlar: <b>{stat['soni']}</b> ta",
        f"✅ Jami to'g'ri javoblar: <b>{stat['togri']}/{stat['jami']}</b>",
        f"📊 Umumiy natija: <b>{stat['foiz']}%</b>\n",
        utils.progress_bar(stat["togri"], stat["jami"]),
        "",
        "🕘 <b>Oxirgi natijalar:</b>",
    ]

    natijalar = await db.test_natijalari(user_id, 5)
    for qator in natijalar:
        foiz = round(int(qator["togri"]) * 100 / int(qator["jami"])) if qator["jami"] else 0
        qatorlar.append(
            f"• {utils.sana_chiroyli(qator['sana'])} — "
            f"{utils.xavfsiz(_kategoriya_nomi(qator['kategoriya']))}: "
            f"{qator['togri']}/{qator['jami']} ({foiz}%)"
        )
    qatorlar.append("")
    qatorlar.append(f"ℹ️ {QISQA}")

    builder.button(text="📝 Yana test topshirish", callback_data="testlar")
    builder.button(text="✅ Kunlik odatlar", callback_data="odatlar")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return "\n".join(qatorlar), builder.as_markup()


@router.message(Command("test"))
async def test_buyrugi(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(test_sarlavhasi(), reply_markup=test_menyusi())


@router.callback_query(F.data == "testlar")
async def testlar_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await korinishni_yangila(callback, test_sarlavhasi(), test_menyusi())
    await callback.answer()


@router.callback_query(F.data.startswith("test_kategoriya:"))
async def test_boshlash(callback: CallbackQuery, state: FSMContext) -> None:
    kalit = (callback.data or "").split(":", 1)[-1]

    if kalit == BARCHASI:
        indekslar = list(range(len(savollar.SAVOLLAR)))
    elif kalit in savollar.KATEGORIYALAR:
        indekslar = [
            indeks
            for indeks, savol in enumerate(savollar.SAVOLLAR)
            if savol["kategoriya"] == kalit
        ]
    else:
        await callback.answer("Yo'nalish topilmadi", show_alert=True)
        return

    if not indekslar:
        await callback.answer("Bu yo'nalishda savollar topilmadi", show_alert=True)
        return

    await state.set_state(TestHolati.faol)
    await state.update_data(kategoriya=kalit, savollar=indekslar, pos=0, togri=0)

    matn, markup = _savol_korinishi(indekslar, 0)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer("Test boshlandi. Omad! 🍀")


@router.callback_query(F.data.startswith("javob:"))
async def javob_berish(callback: CallbackQuery, state: FSMContext) -> None:
    malumot = await state.get_data()
    indekslar = malumot.get("savollar")
    pos = malumot.get("pos")
    togri = int(malumot.get("togri", 0))
    kategoriya = malumot.get("kategoriya", BARCHASI)

    if not indekslar or pos is None:
        await state.clear()
        await callback.answer(
            "Test sessiyasi topilmadi. Iltimos, qaytadan boshlang.", show_alert=True
        )
        return

    qismlar = (callback.data or "").split(":")
    if len(qismlar) != 3 or not qismlar[1].isdigit() or not qismlar[2].isdigit():
        await callback.answer("Javob topilmadi", show_alert=True)
        return

    sorov_pos = int(qismlar[1])
    variant = int(qismlar[2])

    if sorov_pos != pos:
        await callback.answer("Bu savol allaqachon javoblangan", show_alert=True)
        return

    savol = savollar.SAVOLLAR[indekslar[pos]]
    variantlar = savol["variantlar"]
    if not 0 <= variant < len(variantlar):
        await callback.answer("Variant topilmadi", show_alert=True)
        return

    togri_javob = int(savol["javob"])
    togri_bolgan = variant == togri_javob
    if togri_bolgan:
        togri += 1

    keyingi = pos + 1
    await state.update_data(pos=keyingi, togri=togri)

    # Test tugadi
    if keyingi >= len(indekslar):
        await state.clear()
        matn, markup = await _testni_yakunlash(callback, kategoriya, len(indekslar), togri)
        await korinishni_yangila(callback, matn, markup)
        await callback.answer("✅ To'g'ri!" if togri_bolgan else "❌ Noto'g'ri")
        return

    sarlavha = "✅ <b>To'g'ri javob!</b>" if togri_bolgan else "❌ <b>Noto'g'ri javob.</b>"
    togri_harf = HARFLAR[togri_javob] if togri_javob < len(HARFLAR) else str(togri_javob + 1)
    variant_harf = HARFLAR[variant] if variant < len(HARFLAR) else str(variant + 1)

    matn = (
        f"{sarlavha}\n\n"
        f"{utils.xavfsiz(savol['savol'])}\n\n"
        f"🟢 To'g'ri javob: <b>{togri_harf}) {utils.xavfsiz(variantlar[togri_javob])}</b>\n"
    )
    if not togri_bolgan:
        matn += f"🔴 Sizning javobingiz: {variant_harf}) {utils.xavfsiz(variantlar[variant])}\n"
    matn += (
        f"\n💡 {utils.xavfsiz(savol['izoh'])}\n\n"
        f"📊 Hisob: <b>{togri}</b> ta to'g'ri javob"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="➡️ Keyingi savol", callback_data=f"test_keyingi:{keyingi}")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="menyu"))

    await korinishni_yangila(callback, matn, builder.as_markup())
    await callback.answer("✅ To'g'ri!" if togri_bolgan else "❌ Noto'g'ri")


@router.callback_query(F.data.startswith("test_keyingi:"))
async def keyingi_savol(callback: CallbackQuery, state: FSMContext) -> None:
    malumot = await state.get_data()
    indekslar = malumot.get("savollar")
    if not indekslar:
        await state.clear()
        await callback.answer(
            "Test sessiyasi topilmadi. Iltimos, qaytadan boshlang.", show_alert=True
        )
        return

    qismlar = (callback.data or "").split(":")
    if len(qismlar) != 2 or not qismlar[1].isdigit():
        await callback.answer("Savol topilmadi", show_alert=True)
        return

    pos = int(qismlar[1])
    if not 0 <= pos < len(indekslar):
        await callback.answer("Savol topilmadi", show_alert=True)
        return

    matn, markup = _savol_korinishi(indekslar, pos)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.callback_query(F.data == "test_natijalar")
async def test_natijalar(callback: CallbackQuery) -> None:
    matn, markup = await _natijalar_korinishi(callback.from_user.id)
    await korinishni_yangila(callback, matn, markup)
    await callback.answer()


@router.message(Command("natijalar"))
async def natijalar_buyrugi(message: Message) -> None:
    matn, markup = await _natijalar_korinishi(message.from_user.id)
    await message.answer(matn, reply_markup=markup)


@router.message(TestHolati.faol, F.text)
async def test_davomida_matn(message: Message) -> None:
    await message.answer(
        "📝 Test davom etmoqda. Javobni quyidagi tugmalar orqali tanlang.\n"
        "Testdan chiqish uchun «🏠 Asosiy menyu» tugmasini bosing.",
        reply_markup=kb.bekor_klaviaturasi(),
    )
