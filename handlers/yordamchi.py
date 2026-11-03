"""Handler modullari uchun umumiy yordamchi funksiyalar."""

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardMarkup


async def korinishni_yangila(
    callback: CallbackQuery, matn: str, markup: InlineKeyboardMarkup | None = None
) -> None:
    """Callback tugmasi bosilganda xabarni yangilaydi.

    Xabarni tahrirlash imkoni bo'lmasa (eski xabar, bir xil matn va h.k.)
    yangi xabar yuboriladi - shu bilan bot hech qachon xato bermaydi.
    """
    xabar = callback.message
    if xabar is None:
        return
    try:
        await xabar.edit_text(matn, reply_markup=markup)
    except TelegramBadRequest as xato:
        if "message is not modified" in str(xato).lower():
            return
        try:
            await xabar.answer(matn, reply_markup=markup)
        except TelegramBadRequest:
            return
