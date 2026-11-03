"""Bepul bulut xizmatlarida (masalan Render) botni 24/7 ushlab turish qatlami.

Bepul tarifdagi serverlar bir necha daqiqa harakatsizlikdan so'ng "uxlaydi".
Bu modul bot ichida kichik HTTP server ishga tushiradi va uni vaqti-vaqti bilan
o'zi chaqirib turadi — shu bilan server uxlab qolmaydi.

Muhim: bu qatlam faqat `PORT` muhit o'zgaruvchisi mavjud bo'lganda ishga
tushadi (bulut muhitida). Lokal Windows'da `PORT` bo'lmagani uchun bot
avvalgidek, hech qanday o'zgarishsiz ishlaydi.
"""

import asyncio
import logging
import os

from aiohttp import ClientSession, web

logger = logging.getLogger(__name__)

# Necha sekundda bir marta o'zini "uyg'otadi" (bepul tarif ~15 daqiqada uxlaydi).
UYGOTISH_ORALIGI = 10 * 60


async def _sogliq(request: web.Request) -> web.Response:
    """Server tirikligini bildiruvchi javob (health-check)."""
    return web.Response(text="OK")


async def _uygotib_tur(url: str) -> None:
    """Belgilangan manzilga davriy so'rov yuborib, serverni uyg'oq tutadi."""
    async with ClientSession() as sessiya:
        while True:
            await asyncio.sleep(UYGOTISH_ORALIGI)
            try:
                async with sessiya.get(url, timeout=30) as javob:
                    await javob.read()
            except Exception as xato:  # noqa: BLE001
                logger.warning("O'zini uyg'otishda xatolik: %s", xato)


async def ishga_tushir(port: int) -> None:
    """Veb-qatlamni ishga tushiradi va uyg'oq tutish tsiklini boshlaydi."""
    ilova = web.Application()
    ilova.router.add_get("/", _sogliq)
    ilova.router.add_get("/health", _sogliq)

    runner = web.AppRunner(ilova)
    await runner.setup()
    sayt = web.TCPSite(runner, "0.0.0.0", port)
    await sayt.start()
    logger.info("Veb-qatlam %s portida ishga tushdi.", port)

    tashqi = (os.getenv("RENDER_EXTERNAL_URL") or "").strip()
    if tashqi:
        manzil = tashqi.rstrip("/") + "/health"
        asyncio.create_task(_uygotib_tur(manzil))
        logger.info("O'zini uyg'otish yoqildi: %s", manzil)
