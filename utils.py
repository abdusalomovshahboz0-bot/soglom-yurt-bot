"""Yordamchi funksiyalar: qidiruv, matn va hisob-kitoblar."""

import html
from datetime import datetime

import config
from data import ensiklopediya, hayot, ovqatlanish, savollar


def xavfsiz(matn) -> str:
    """HTML uchun xavfsiz matn qaytaradi (dinamik matnlarni himoyalaydi)."""
    return html.escape(str(matn), quote=False)


# O'zbek yozuvidagi turli apostrof belgilari
APOSTROFLAR = "ʻʼ‘’`´‘"

BOLIMLAR = {
    "ovqatlanish": "🥗 Ovqatlanish",
    "mevalar": "🍎 Mevalar",
    "sabzavotlar": "🥕 Sabzavotlar",
    "tabiiy": "🌾 Tabiiy mahsulotlar",
    "odatlar": "✅ Kunlik odatlar",
    "gigiyena": "🧼 Gigiyena",
    "mashqlar": "🏋️ Mashqlar",
    "savollar": "📝 Test savollari",
}


def matnni_tozalash(matn: str) -> str:
    """Matnni qidiruvga moslashtiradi (kichik harf, apostroflar bir xil)."""
    natija = matn.lower()
    for belgi in APOSTROFLAR:
        natija = natija.replace(belgi, "'")
    return natija


def _kalitlar(matn: str) -> list[str]:
    """Matndan qidiruv so'zlarini ajratadi."""
    tozalangan = matnni_tozalash(matn)
    for belgi in ",.;:!?()[]«»\"“”/\\—–-":
        tozalangan = tozalangan.replace(belgi, " ")
    return [soz for soz in tozalangan.split() if len(soz) > 2]


def _indeksni_qur() -> list[dict]:
    """Barcha bo'limlar bo'yicha qidiruv indeksini tuzadi."""
    yozuvlar: list[dict] = []

    def qosh(sarlavha: str, matn: str, bolim: str, callback: str | None) -> None:
        yozuvlar.append(
            {
                "sarlavha": sarlavha,
                "matn": matn,
                "bolim": bolim,
                "callback": callback,
                "sozlar": _kalitlar(sarlavha + " " + matn),
            }
        )

    for indeks, element in enumerate(ovqatlanish.TAMOYILLAR):
        qosh(element["sarlavha"], element["matn"], "ovqatlanish", f"tamoyil:{indeks}")
    for indeks, element in enumerate(ovqatlanish.RATSION):
        qosh(element["sarlavha"], element["matn"], "ovqatlanish", f"ratsion:{indeks}")
    for indeks, element in enumerate(ovqatlanish.TABIIY_MAHSULOTLAR):
        qosh(
            element["nom"],
            element["foyda"] + " " + element["istehmol"],
            "tabiiy",
            f"tabiiy:{indeks}",
        )
    for indeks, element in enumerate(ensiklopediya.MEVALAR):
        qosh(
            element["nom"],
            element["vitaminlar"] + ". " + element["foyda"] + " " + element["istehmol"],
            "mevalar",
            f"meva:{indeks}",
        )
    for indeks, element in enumerate(ensiklopediya.SABZAVOTLAR):
        qosh(
            element["nom"],
            element["vitaminlar"] + ". " + element["foyda"] + " " + element["istehmol"],
            "sabzavotlar",
            f"sabzavot:{indeks}",
        )
    for indeks, element in enumerate(hayot.KUNLIK_ODATLAR):
        qosh(element["nom"], element["matn"], "odatlar", f"odat:{indeks}")
    for indeks, element in enumerate(hayot.GIGIYENA):
        qosh(element["sarlavha"], element["matn"], "gigiyena", f"gigiyena:{indeks}")
    for indeks, element in enumerate(hayot.ERTALABKI_MASHQ):
        qosh(
            element["nom"],
            " ".join(element["qadamlar"]) + " " + element["foyda"],
            "mashqlar",
            f"ertalab:{indeks}",
        )
    for indeks, element in enumerate(hayot.UY_MASHQLARI):
        qosh(
            element["nom"],
            " ".join(element["mashqlar"]) + " " + element["foyda"],
            "mashqlar",
            f"uymashq:{indeks}",
        )
    for element in savollar.SAVOLLAR:
        qosh(element["savol"], element["izoh"], "savollar", None)

    return yozuvlar


INDEKS: list[dict] = _indeksni_qur()


def qidirish(sorov: str, limit: int = 5) -> list[dict]:
    """Bilim bazasidan so'rovga mos natijalarni qaytaradi."""
    sorov_sozlari = _kalitlar(sorov)
    if not sorov_sozlari:
        return []

    natijalar = []
    for yozuv in INDEKS:
        yozuv_sozlari = set(yozuv["sozlar"])
        sarlavha_sozlari = set(_kalitlar(yozuv["sarlavha"]))
        ball = 0
        for soz in sorov_sozlari:
            if soz in sarlavha_sozlari:
                ball += 4
            elif soz in yozuv_sozlari:
                ball += 2
            else:
                # Qisman mos kelish (masalan "sabzav" - "sabzavotlar")
                for mavjud in yozuv_sozlari:
                    if mavjud.startswith(soz) or soz.startswith(mavjud):
                        ball += 1
                        break
        if ball > 0:
            natijalar.append((ball, yozuv))

    natijalar.sort(key=lambda juft: (-juft[0], len(juft[1]["sarlavha"])))
    return [yozuv for _, yozuv in natijalar[:limit]]


def progress_bar(qiymat: float, jami: float, uzunlik: int | None = None) -> str:
    """Vizual ko'rsatkich chizig'ini tayyorlaydi."""
    uzunlik = uzunlik or config.PROGRESS_UZUNLIGI
    if jami <= 0:
        return "▫️" * uzunlik
    nisbat = max(0.0, min(1.0, qiymat / jami))
    tolgan = int(round(nisbat * uzunlik))
    return "🟩" * tolgan + "⬜" * (uzunlik - tolgan)


def sana_chiroyli(sana: str) -> str:
    """2026-11-03 -> 03.11.2026"""
    try:
        return datetime.strptime(sana, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        return sana


def hafta_kuni(sana: str) -> str:
    """Sanani hafta kuni nomi bilan qaytaradi."""
    nomlar = [
        "Dushanba",
        "Seshanba",
        "Chorshanba",
        "Payshanba",
        "Juma",
        "Shanba",
        "Yakshanba",
    ]
    try:
        indeks = datetime.strptime(sana, "%Y-%m-%d").weekday()
    except ValueError:
        return sana
    return nomlar[indeks]


def tanishtir_qiymat(qiymat, birlik: str = "") -> str:
    """Bo'sh qiymatlarni chiroyli ko'rsatadi."""
    if qiymat is None:
        return "—"
    if isinstance(qiymat, float) and qiymat.is_integer():
        qiymat = int(qiymat)
    return f"{qiymat}{birlik}"


# --- Sog'liq hisob-kitoblari (umumiy formulalar asosida) ---


def bmi_hisoblash(boy_sm: float, vazn_kg: float) -> float:
    """Tana massasi indeksini hisoblaydi."""
    boy_m = boy_sm / 100
    return round(vazn_kg / (boy_m * boy_m), 1)


def bmi_toifasi(bmi: float) -> tuple[str, str]:
    """BMI bo'yicha toifa va maslahat qaytaradi."""
    if bmi < 18.5:
        return "Kam vazn", "Ozroq kaloriyali va to'yimli ovqatlanishga e'tibor bering."
    if bmi < 25:
        return "Normal vazn", "Ajoyib! Hozirgi sog'lom odatlaringizni davom ettiring."
    if bmi < 30:
        return "Ortiqcha vazn", "Kunlik faollikni oshirish va porsiyani nazorat qilish foydali."
    return "Semizlik", "Shifokor bilan maslahatlashib, bosqichma-bosqich reja tuzish tavsiya etiladi."


def bmr_hisoblash(jins: str, vazn_kg: float, boy_sm: float, yosh: int) -> float:
    """Bazal metabolizm tezligini hisoblaydi (Mifflin-St Jeor formulasi)."""
    asosiy = 10 * vazn_kg + 6.25 * boy_sm - 5 * yosh
    return round(asosiy + (5 if jins == "Erkak" else -161))


FAOLLIK_DARAJALARI = {
    "kam": ("Kam harakat", 1.2),
    "yengil": ("Yengil faollik", 1.375),
    "orta": ("O'rtacha faollik", 1.55),
    "yuqori": ("Yuqori faollik", 1.725),
}

MAQSADLAR = {
    "saqlash": ("Vaznni saqlash", 1.0),
    "kamaytirish": ("Vaznni kamaytirish", 0.85),
    "oshirish": ("Vaznni oshirish", 1.15),
}


def kunlik_kaloriya(bmr: float, faollik_kaliti: str, maqsad_kaliti: str) -> dict:
    """Kunlik kaloriya me'yorini hisoblaydi."""
    faollik_nomi, koeffitsiyent = FAOLLIK_DARAJALARI.get(
        faollik_kaliti, FAOLLIK_DARAJALARI["orta"]
    )
    maqsad_nomi, maqsad_koeffitsiyent = MAQSADLAR.get(
        maqsad_kaliti, MAQSADLAR["saqlash"]
    )
    saqlash = round(bmr * koeffitsiyent)
    tavsiya = round(saqlash * maqsad_koeffitsiyent)
    return {
        "faollik_nomi": faollik_nomi,
        "maqsad_nomi": maqsad_nomi,
        "saqlash": saqlash,
        "tavsiya": tavsiya,
        "past": round(tavsiya * 0.9),
        "yuqori": round(tavsiya * 1.1),
    }


def sog_lom_vazn_oraligi(boy_sm: float) -> tuple[float, float]:
    """Bo'yga mos sog'lom vazn oralig'i (BMI 18.5 - 24.9)."""
    boy_m = boy_sm / 100
    return round(18.5 * boy_m * boy_m, 1), round(24.9 * boy_m * boy_m, 1)


def suv_me_yori(vazn_kg: float | None) -> int:
    """Vaznga qarab kunlik suv me'yorini stakanda qaytaradi (200 ml stakan)."""
    if not vazn_kg:
        return 8
    millilitr = vazn_kg * 30
    return max(6, min(14, round(millilitr / 200)))
