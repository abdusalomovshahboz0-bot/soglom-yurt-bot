"""AI sog'liq bo'yicha ma'rifiy yordamchi.

Tashqi AI xizmati uchun kalit (.env dagi AI_API_KEY) mavjud bo'lsa, savol
unga yuboriladi. Kalit bo'lmasa yoki xizmat javob bermasa, bot o'zining
lokal bilim bazasidan (qidiruv) javob tayyorlaydi.
"""

import aiohttp
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import kb
import utils
from handlers.yordamchi import korinishni_yangila

router = Router(name="ai")

QISQA = utils.xavfsiz(config.QISQA_OGOHLANTIRISH)

# AI xizmatiga yuboriladigan tizim ko'rsatmasi (faqat ma'rifiy yordam)
TIZIM_KORSATMASI = (
    "Siz «SOG'LOM YURT | Salomatlik maktabi» botining ma'rifiy yordamchisiz. "
    "Faqat o'zbek tilida (lotin yozuvi) javob bering. Sog'lom turmush tarzi, "
    "muvozanatli ovqatlanish, meva-sabzavotlar foydasi, mashqlar, gigiyena, "
    "suv, uyqu va umumiy salomatlik bo'yicha foydali, umumiy va xavfsiz "
    "ma'lumot bering. Tashxis qo'ymang, dori-darmon nomini yoki dozasini "
    "aytmang, davolash rejasini tuzmang. Javobni qisqa va tushunarli qilib, "
    "kerak bo'lsa shifokorga murojaat qilishni eslatib qo'ying."
)

TAYYOR_SAVOLLAR = [
    "Kuniga qancha suv ichish foydali?",
    "Sog'lom nonushta qanday bo'ladi?",
    "Uyqu sifatini yaxshilash uchun nima qilish kerak?",
    "Ertalabki mashqlar qanday foyda beradi?",
    "Qo'l yuvish nima uchun muhim?",
    "Vitamin C qaysi meva va sabzavotlarda ko'p?",
]


class AiHolati(StatesGroup):
    kutilmoqda = State()


def ai_matni() -> str:
    return (
        "🤖 <b>AI sog'liq yordamchisi</b>\n\n"
        "Savolingizni oddiy so'zlar bilan yozing — yordamchi sog'lom turmush "
        "tarzi bo'yicha ma'rifiy ma'lumot beradi.\n\n"
        "Quyidagi tayyor savollardan birini tanlashingiz yoki o'z savolingizni "
        "yozishingiz mumkin 👇\n\n"
        "❌ Bot tashxis qo'ymaydi va dori tavsiya qilmaydi.\n"
        "ℹ️ Jiddiy shikoyat bo'lsa, shifokorga murojaat qiling."
    )


def ai_klaviaturasi() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for indeks, savol in enumerate(TAYYOR_SAVOLLAR):
        builder.button(text=f"❔ {savol}", callback_data=f"ai_savol:{indeks}")
    builder.button(text="🔍 Bilim bazasidan qidirish", callback_data="qidiruv")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())
    return builder.as_markup()


async def _tashqi_ai(sorov: str) -> str | None:
    """Tashqi AI xizmatidan javob oladi (kalit mavjud bo'lsa)."""
    manzil = config.AI_MANZIL.rstrip("/") + "/chat/completions"
    sarlavhalar = {
        "Authorization": f"Bearer {config.AI_KALIT}",
        "Content-Type": "application/json",
    }
    tanasi = {
        "model": config.AI_MODEL,
        "messages": [
            {"role": "system", "content": TIZIM_KORSATMASI},
            {"role": "user", "content": sorov},
        ],
        "temperature": 0.4,
        "max_tokens": 700,
    }
    vaqt_chegarasi = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=vaqt_chegarasi) as sessiya:
        async with sessiya.post(
            manzil, json=tanasi, headers=sarlavhalar
        ) as javob:
            if javob.status != 200:
                return None
            malumot = await javob.json()
    try:
        return malumot["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        return None


def _bilim_bazasidan(sorov: str) -> tuple[str, InlineKeyboardMarkup]:
    """Lokal bilim bazasidan javob tayyorlaydi."""
    natijalar = utils.qidirish(sorov, limit=3)

    if not natijalar:
        matn = (
            "🤖 <b>AI yordamchi</b>\n\n"
            f"«{utils.xavfsiz(sorov)}» bo'yicha bilim bazamdan aniq ma'lumot "
            "topilmadi.\n\n"
            "Boshqacha so'z bilan urinib ko'ring. Masalan:\n"
            "• «suv», «nonushta», «vitamin C»\n"
            "• «uyqu», «gigiyena», «qorin mashqi»\n"
            "• «olma», «sabzi», «baliq»\n\n"
            f"ℹ️ {QISQA}"
        )
        tugmalar = [
            ("🥗 Sog'lom ovqatlanish", "ovqat"),
            ("🍎 Meva va sabzavotlar", "ens"),
            ("🔁 Yana savol berish", "ai"),
        ]
        return matn, kb.tugmalar_menyu(tugmalar)

    qismlar = [
        "🤖 <b>AI yordamchi</b>\n",
        f"«{utils.xavfsiz(sorov)}» bo'yicha topilgan ma'lumotlar:\n",
    ]
    builder = InlineKeyboardBuilder()
    for raqam, yozuv in enumerate(natijalar, start=1):
        bolim = utils.BOLIMLAR.get(yozuv["bolim"], yozuv["bolim"])
        qisqa = yozuv["matn"]
        if len(qisqa) > 220:
            qisqa = qisqa[:217] + "..."
        qismlar.append(
            f"{raqam}. <b>{utils.xavfsiz(yozuv['sarlavha'])}</b> — <i>{bolim}</i>"
        )
        qismlar.append(utils.xavfsiz(qisqa))
        qismlar.append("")
        if yozuv["callback"]:
            builder.button(
                text=f"{raqam}. {yozuv['sarlavha'][:30]}",
                callback_data=yozuv["callback"],
            )

    builder.button(text="🔁 Yana savol berish", callback_data="ai")
    builder.adjust(1)
    builder.row(kb.asosiy_menyu_tugmasi())

    qismlar.append(f"ℹ️ {QISQA}")
    return "\n".join(qismlar).strip(), builder.as_markup()


async def _ai_javobi(sorov: str) -> tuple[str, InlineKeyboardMarkup]:
    """Savolga javob qaytaradi: avval tashqi AI, bo'lmasa lokal baza."""
    sorov = (sorov or "").strip()
    if not sorov:
        return ai_matni(), ai_klaviaturasi()

    if config.AI_KALIT:
        try:
            javob = await _tashqi_ai(sorov)
        except Exception:
            javob = None
        if javob:
            matn = (
                "🤖 <b>AI yordamchi javobi</b>\n\n"
                f"{utils.xavfsiz(javob)}\n\n"
                f"ℹ️ {QISQA}"
            )
            builder = InlineKeyboardBuilder()
            builder.button(text="🔁 Yana savol berish", callback_data="ai")
            builder.button(text="🔍 Bilim bazasidan qidirish", callback_data="qidiruv")
            builder.adjust(1)
            builder.row(kb.asosiy_menyu_tugmasi())
            return matn, builder.as_markup()

    return _bilim_bazasidan(sorov)


@router.message(Command("ai"))
async def ai_buyrugi(message: Message, state: FSMContext) -> None:
    qismlar = (message.text or "").split(maxsplit=1)
    if len(qismlar) == 2 and qismlar[1].strip():
        await state.clear()
        matn, markup = await _ai_javobi(qismlar[1])
        await message.answer(matn, reply_markup=markup)
        return

    await state.set_state(AiHolati.kutilmoqda)
    await message.answer(ai_matni(), reply_markup=kb.bekor_klaviaturasi())
    await message.answer("Savolingizni yozib yuboring 👇")


@router.callback_query(F.data == "ai")
async def ai_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AiHolati.kutilmoqda)
    await korinishni_yangila(
        callback,
        "🤖 <b>AI sog'liq yordamchisi</b>\n\n"
        "Savolingizni yozib yuboring. Yoki quyidagi tayyor savollardan birini "
        "tanlang 👇",
        ai_klaviaturasi(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ai_savol:"))
async def ai_savol_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    qismlar = (callback.data or "").split(":")
    if len(qismlar) != 2 or not qismlar[1].isdigit():
        await callback.answer("Savol topilmadi", show_alert=True)
        return
    indeks = int(qismlar[1])
    if not 0 <= indeks < len(TAYYOR_SAVOLLAR):
        await callback.answer("Savol topilmadi", show_alert=True)
        return

    sorov = TAYYOR_SAVOLLAR[indeks]
    await callback.answer("Javob tayyorlanmoqda...")
    matn, markup = await _ai_javobi(sorov)
    await korinishni_yangila(callback, matn, markup)


@router.message(AiHolati.kutilmoqda, F.text)
async def ai_matnli_savol(message: Message, state: FSMContext) -> None:
    matn, markup = await _ai_javobi(message.text or "")
    await state.clear()
    await message.answer(matn, reply_markup=markup)
