"""Foydalanuvchi ma'lumotlarini SQLite bazasida xavfsiz saqlash.

Baza birinchi ishga tushirishda yaratiladi, mavjud bo'lsa
ma'lumotlar o'chirilmaydi (CREATE TABLE IF NOT EXISTS).
"""

import os
from datetime import datetime, timedelta

import aiosqlite

import config

_baza: aiosqlite.Connection | None = None

SXEMA = """
CREATE TABLE IF NOT EXISTS foydalanuvchilar (
    user_id INTEGER PRIMARY KEY,
    ism TEXT,
    username TEXT,
    yosh INTEGER,
    jins TEXT,
    boy REAL,
    vazn REAL,
    maqsad TEXT,
    faollik TEXT,
    suv_maqsad INTEGER DEFAULT 8,
    qoshilgan TEXT,
    oxirgi_kirish TEXT
);

CREATE TABLE IF NOT EXISTS suv (
    user_id INTEGER NOT NULL,
    sana TEXT NOT NULL,
    stakan INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, sana)
);

CREATE TABLE IF NOT EXISTS faollik (
    user_id INTEGER NOT NULL,
    sana TEXT NOT NULL,
    uyqu REAL,
    qadam INTEGER,
    mashq_daqiqa INTEGER,
    kayfiyat INTEGER,
    PRIMARY KEY (user_id, sana)
);

CREATE TABLE IF NOT EXISTS testlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    kategoriya TEXT,
    togri INTEGER,
    jami INTEGER,
    sana TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS odatlar (
    user_id INTEGER NOT NULL,
    sana TEXT NOT NULL,
    odat TEXT NOT NULL,
    PRIMARY KEY (user_id, sana, odat)
);
"""

# Bazaga yozishga ruxsat etilgan ustunlar
RUXSAT_ETILGAN_USTUNLAR = {
    "ism",
    "username",
    "yosh",
    "jins",
    "boy",
    "vazn",
    "maqsad",
    "faollik",
    "suv_maqsad",
    "oxirgi_kirish",
}


async def init() -> None:
    """Bazani ochadi va jadvallarni tayyorlaydi."""
    global _baza
    yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.DB_FAYL)
    _baza = await aiosqlite.connect(yol)
    _baza.row_factory = aiosqlite.Row
    await _baza.executescript(SXEMA)
    await _baza.commit()


async def yopish() -> None:
    """Bazani yopadi."""
    global _baza
    if _baza is not None:
        await _baza.close()
        _baza = None


def _ulanish() -> aiosqlite.Connection:
    if _baza is None:
        raise RuntimeError("Baza hali ishga tushirilmagan. init() chaqirilishi kerak.")
    return _baza


def bugun(sana: datetime | None = None) -> str:
    """Bugungi sanani YYYY-MM-DD ko'rinishida qaytaradi (Toshkent vaqti)."""
    vaqt = sana or datetime.now(config.TOSHKENT_VAQTI)
    return vaqt.strftime("%Y-%m-%d")


def kun_oldin(kunlar: int) -> str:
    """Bugundan N kun oldingi sanani qaytaradi."""
    return bugun(datetime.now(config.TOSHKENT_VAQTI) - timedelta(days=kunlar))


def hozir() -> str:
    """Hozirgi vaqtni matn ko'rinishida qaytaradi."""
    return datetime.now(config.TOSHKENT_VAQTI).strftime("%Y-%m-%d %H:%M")


async def foydalanuvchini_saqla(user_id: int, ism: str, username: str | None) -> None:
    """Foydalanuvchini bazaga qo'shadi yoki oxirgi kirish vaqtini yangilaydi."""
    ulanish = _ulanish()
    await ulanish.execute(
        """
        INSERT INTO foydalanuvchilar (user_id, ism, username, qoshilgan, oxirgi_kirish)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            ism = excluded.ism,
            username = excluded.username,
            oxirgi_kirish = excluded.oxirgi_kirish
        """,
        (user_id, ism, username, hozir(), hozir()),
    )
    await ulanish.commit()


async def foydalanuvchi(user_id: int) -> aiosqlite.Row | None:
    """Foydalanuvchi yozuvini qaytaradi."""
    ulanish = _ulanish()
    kursor = await ulanish.execute(
        "SELECT * FROM foydalanuvchilar WHERE user_id = ?", (user_id,)
    )
    qator = await kursor.fetchone()
    await kursor.close()
    return qator


async def maydonlarni_yangila(user_id: int, **maydonlar) -> None:
    """Foydalanuvchi profilidagi ruxsat etilgan maydonlarni yangilaydi."""
    toza = {k: v for k, v in maydonlar.items() if k in RUXSAT_ETILGAN_USTUNLAR}
    if not toza:
        return
    ulanish = _ulanish()
    ustunlar = ", ".join(f"{ustun} = ?" for ustun in toza)
    qiymatlar = list(toza.values()) + [user_id]
    await ulanish.execute(
        f"UPDATE foydalanuvchilar SET {ustunlar} WHERE user_id = ?", qiymatlar
    )
    await ulanish.commit()


# --- Suv hisoblagichi ---


async def suv_ol(user_id: int, sana: str | None = None) -> int:
    """Kunlik ichilgan stakan suv sonini qaytaradi."""
    ulanish = _ulanish()
    kursor = await ulanish.execute(
        "SELECT stakan FROM suv WHERE user_id = ? AND sana = ?",
        (user_id, sana or bugun()),
    )
    qator = await kursor.fetchone()
    await kursor.close()
    return int(qator["stakan"]) if qator else 0


async def suv_qosh(user_id: int, miqdor: int = 1, sana: str | None = None) -> int:
    """Suv miqdorini o'zgartiradi (manfiy bo'lishi mumkin) va yangi qiymatni qaytaradi."""
    kun = sana or bugun()
    ulanish = _ulanish()
    hozirgi = await suv_ol(user_id, kun)
    yangi = max(0, min(30, hozirgi + miqdor))
    await ulanish.execute(
        """
        INSERT INTO suv (user_id, sana, stakan) VALUES (?, ?, ?)
        ON CONFLICT(user_id, sana) DO UPDATE SET stakan = excluded.stakan
        """,
        (user_id, kun, yangi),
    )
    await ulanish.commit()
    return yangi


async def suv_hisobot(user_id: int, kunlar: int = 7) -> dict:
    """Oxirgi N kun uchun suv statistikasi."""
    ulanish = _ulanish()
    boshlanish = kun_oldin(kunlar - 1)
    kursor = await ulanish.execute(
        """
        SELECT sana, stakan FROM suv
        WHERE user_id = ? AND sana >= ?
        ORDER BY sana
        """,
        (user_id, boshlanish),
    )
    qatorlar = await kursor.fetchall()
    await kursor.close()
    jami = sum(int(q["stakan"]) for q in qatorlar)
    kunlar_soni = len(qatorlar) or 1
    return {
        "jami": jami,
        "ortacha": round(jami / kunlar_soni, 1),
        "kunlar": qatorlar,
    }


# --- Faollik va uyqu ---


async def faollik_ol(user_id: int, sana: str | None = None) -> aiosqlite.Row | None:
    """Belgilangan kundagi faollik yozuvini qaytaradi."""
    ulanish = _ulanish()
    kursor = await ulanish.execute(
        "SELECT * FROM faollik WHERE user_id = ? AND sana = ?",
        (user_id, sana or bugun()),
    )
    qator = await kursor.fetchone()
    await kursor.close()
    return qator


async def faollik_yoz(user_id: int, sana: str | None = None, **maydonlar) -> None:
    """Uyqu, qadam, mashq daqiqasi yoki kayfiyatni saqlaydi."""
    ruxsat = {"uyqu", "qadam", "mashq_daqiqa", "kayfiyat"}
    toza = {k: v for k, v in maydonlar.items() if k in ruxsat}
    if not toza:
        return
    kun = sana or bugun()
    ulanish = _ulanish()
    await ulanish.execute(
        "INSERT OR IGNORE INTO faollik (user_id, sana) VALUES (?, ?)", (user_id, kun)
    )
    ustunlar = ", ".join(f"{ustun} = ?" for ustun in toza)
    qiymatlar = list(toza.values()) + [user_id, kun]
    await ulanish.execute(
        f"UPDATE faollik SET {ustunlar} WHERE user_id = ? AND sana = ?", qiymatlar
    )
    await ulanish.commit()


async def faollik_royxati(user_id: int, kunlar: int = 7) -> list[aiosqlite.Row]:
    """Oxirgi N kunlik faollik yozuvlari."""
    ulanish = _ulanish()
    boshlanish = kun_oldin(kunlar - 1)
    kursor = await ulanish.execute(
        """
        SELECT * FROM faollik
        WHERE user_id = ? AND sana >= ?
        ORDER BY sana
        """,
        (user_id, boshlanish),
    )
    qatorlar = await kursor.fetchall()
    await kursor.close()
    return list(qatorlar)


# --- Testlar ---


async def test_yoz(user_id: int, kategoriya: str, togri: int, jami: int) -> None:
    """Test natijasini saqlaydi."""
    ulanish = _ulanish()
    await ulanish.execute(
        """
        INSERT INTO testlar (user_id, kategoriya, togri, jami, sana)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, kategoriya, togri, jami, bugun()),
    )
    await ulanish.commit()


async def test_statistika(user_id: int) -> dict:
    """Testlar bo'yicha umumiy statistika."""
    ulanish = _ulanish()
    kursor = await ulanish.execute(
        """
        SELECT COUNT(*) AS soni,
               COALESCE(SUM(togri), 0) AS togri,
               COALESCE(SUM(jami), 0) AS jami
        FROM testlar WHERE user_id = ?
        """,
        (user_id,),
    )
    qator = await kursor.fetchone()
    await kursor.close()
    jami = int(qator["jami"])
    return {
        "soni": int(qator["soni"]),
        "togri": int(qator["togri"]),
        "jami": jami,
        "foiz": round(int(qator["togri"]) * 100 / jami) if jami else 0,
    }


async def test_natijalari(user_id: int, limit: int = 5) -> list[aiosqlite.Row]:
    """Oxirgi test natijalari."""
    ulanish = _ulanish()
    kursor = await ulanish.execute(
        """
        SELECT kategoriya, togri, jami, sana FROM testlar
        WHERE user_id = ? ORDER BY id DESC LIMIT ?
        """,
        (user_id, limit),
    )
    qatorlar = await kursor.fetchall()
    await kursor.close()
    return list(qatorlar)


# --- Kunlik odatlar ro'yxati ---


async def odat_holati(user_id: int, sana: str | None = None) -> set[str]:
    """Belgilangan kunda bajarilgan odatlar to'plami."""
    ulanish = _ulanish()
    kursor = await ulanish.execute(
        "SELECT odat FROM odatlar WHERE user_id = ? AND sana = ?",
        (user_id, sana or bugun()),
    )
    qatorlar = await kursor.fetchall()
    await kursor.close()
    return {q["odat"] for q in qatorlar}


async def odat_almashtir(user_id: int, odat: str, sana: str | None = None) -> bool:
    """Odat belgisini yoqadi yoki o'chiradi. Yangi holatni qaytaradi."""
    kun = sana or bugun()
    ulanish = _ulanish()
    mavjud = await odat_holati(user_id, kun)
    if odat in mavjud:
        await ulanish.execute(
            "DELETE FROM odatlar WHERE user_id = ? AND sana = ? AND odat = ?",
            (user_id, kun, odat),
        )
        natija = False
    else:
        await ulanish.execute(
            "INSERT INTO odatlar (user_id, sana, odat) VALUES (?, ?, ?)",
            (user_id, kun, odat),
        )
        natija = True
    await ulanish.commit()
    return natija


async def odat_hisobot(user_id: int, kunlar: int = 7) -> dict:
    """Oxirgi N kun uchun bajarilgan odatlar statistikasi."""
    ulanish = _ulanish()
    boshlanish = kun_oldin(kunlar - 1)
    kursor = await ulanish.execute(
        """
        SELECT sana, COUNT(*) AS soni FROM odatlar
        WHERE user_id = ? AND sana >= ?
        GROUP BY sana ORDER BY sana
        """,
        (user_id, boshlanish),
    )
    qatorlar = await kursor.fetchall()
    await kursor.close()
    return {
        "kunlar": {q["sana"]: int(q["soni"]) for q in qatorlar},
        "jami": sum(int(q["soni"]) for q in qatorlar),
    }


# --- Admin statistikasi ---


async def _bitta(sql: str, parametrlar: tuple = ()) -> int:
    """Bitta butun sonli qiymat qaytaruvchi yordamchi so'rov."""
    ulanish = _ulanish()
    kursor = await ulanish.execute(sql, parametrlar)
    qator = await kursor.fetchone()
    await kursor.close()
    return int(qator[0]) if qator and qator[0] is not None else 0


async def statistika() -> dict:
    """Bot bo'yicha umumiy ko'rsatkichlar (faqat admin uchun)."""
    kun = bugun()
    hafta = kun_oldin(6)
    return {
        "jami_soni": await _bitta("SELECT COUNT(*) FROM foydalanuvchilar"),
        "bugun_qoshilgan": await _bitta(
            "SELECT COUNT(*) FROM foydalanuvchilar WHERE qoshilgan LIKE ?", (kun + "%",)
        ),
        "bugun_faol": await _bitta(
            "SELECT COUNT(*) FROM foydalanuvchilar WHERE oxirgi_kirish LIKE ?", (kun + "%",)
        ),
        "hafta_faol": await _bitta(
            "SELECT COUNT(*) FROM foydalanuvchilar WHERE oxirgi_kirish >= ?", (hafta,)
        ),
        "suv_ichganlar": await _bitta(
            "SELECT COUNT(*) FROM suv WHERE sana = ? AND stakan > 0", (kun,)
        ),
        "suv_stakan": await _bitta(
            "SELECT COALESCE(SUM(stakan), 0) FROM suv WHERE sana = ?", (kun,)
        ),
        "faollik_bugun": await _bitta("SELECT COUNT(*) FROM faollik WHERE sana = ?", (kun,)),
        "test_jami": await _bitta("SELECT COUNT(*) FROM testlar"),
        "test_bugun": await _bitta("SELECT COUNT(*) FROM testlar WHERE sana = ?", (kun,)),
        "odat_bugun": await _bitta("SELECT COUNT(*) FROM odatlar WHERE sana = ?", (kun,)),
    }
