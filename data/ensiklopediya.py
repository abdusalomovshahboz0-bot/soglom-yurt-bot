"""Oziq-ovqat ensiklopediyasi: mevalar va sabzavotlar haqida qisqa ma'lumot.

Bu modul Telegram orqali ishlaydigan sog'liqni saqlash bo'yicha ta'lim boti uchun
mo'ljallangan. Har bir meva va sabzavot haqida umumiy qabul qilingan ovqatlanish
ma'lumotlari sodda va xavfsiz tilda keltirilgan. Bu yerdagi matnlar faqat ma'lumot
uchun bo'lib, tibbiy maslahat o'rnini bosmaydi.
"""

MEVALAR = [
    {
        "nom": "Olma",
        "emoji": "🍎",
        "vitaminlar": "C, K, kaliy, folat, pektin",
        "foyda": "Olma tarkibida tola va vitaminlar bor, shuning uchun hazm tizimiga yordam beradi. Undagi antioksidantlar organizmni himoya qilishga foydali hisoblanadi. Kundalik ratsionda iste'mol qilinsa, yurak salomatligi uchun yordam beradi.",
        "istehmol": "Olmani yuvib, po'stlog'i bilan yangi holida yeyish yoki nonushtaga qo'shish foydali."
    },
    {
        "nom": "Anor",
        "emoji": "🍎",
        "vitaminlar": "C, K, kaliy, folat",
        "foyda": "Anor tarkibida ko'plab antioksidantlar bor, ular hujayralarni himoya qilishga yordam beradi. U qon aylanish tizimi uchun foydali hisoblanadi. Tarkibida tola bo'lgani uchun hazmga ham yordam beradi.",
        "istehmol": "Anorni yangi uzib yoki sharbati ko'rinishida, shakarsiz iste'mol qilish tavsiya etiladi."
    },
    {
        "nom": "O'rik",
        "emoji": "🍑",
        "vitaminlar": "A, C, kaliy, tola",
        "foyda": "O'rik ko'z salomatligi uchun foydali bo'lgan A vitaminiga boy. Uning tolasi hazm tizimiga yordam beradi. Kaliy tarkibi tufayli suv-tuz balansini saqlashga hissa qo'shadi.",
        "istehmol": "O'rikni mavsumida yangi holida yoki kuniga bir necha dona quritilgan holda iste'mol qilish mumkin."
    },
    {
        "nom": "Quritilgan o'rik",
        "emoji": "🟠",
        "vitaminlar": "A, kaliy, tola, temir",
        "foyda": "Quritilgan o'rik tolaga boy bo'lib, hazm tizimiga yordam beradi. U temir va kaliy manbai sifatida foydali hisoblanadi. Energiya beruvchi tabiiy shirin meva hisoblanadi.",
        "istehmol": "Quritilgan o'rikni kuniga bir necha dona suv bilan birga iste'mol qilish tavsiya etiladi."
    },
    {
        "nom": "Uzum",
        "emoji": "🍇",
        "vitaminlar": "C, K, kaliy, antioksidantlar",
        "foyda": "Uzum tarkibida vitaminlar va antioksidantlar bor, ular organizmni himoya qilishga yordam beradi. U yurak salomatligi uchun foydali hisoblanadi. Suv va tola hisobiga to'ydiruvchi ta'sirga ega.",
        "istehmol": "Uzum yaxshilab yuvib, yangi holida yoki oz miqdorda sharbat sifatida iste'mol qilinadi."
    },
    {
        "nom": "Tarvuz",
        "emoji": "🍉",
        "vitaminlar": "A, C, kaliy, likopen",
        "foyda": "Tarvuz suvga boy bo'lib, organizmni namlashga yordam beradi. Uning likopeni hujayralarni himoya qilishga foydali hisoblanadi. Issiq kunlarda salqinlik beruvchi meva hisoblanadi.",
        "istehmol": "Tarvuzni kesib, yangi holida, afzalroq tushdan keyin iste'mol qilish mumkin."
    },
    {
        "nom": "Qovun",
        "emoji": "🍈",
        "vitaminlar": "A, C, kaliy, folat",
        "foyda": "Qovun A va C vitaminlariga boy bo'lib, immunitetga yordam beradi. U suv va tola tarkibiga ega, hazm uchun foydali hisoblanadi. Yozda tetiklik beruvchi meva sanaladi.",
        "istehmol": "Qovunni yangi holida, boshqa mevalar bilan aralashtirmasdan iste'mol qilish tavsiya etiladi."
    },
    {
        "nom": "Gilos",
        "emoji": "🍒",
        "vitaminlar": "C, A, kaliy, antioksidantlar",
        "foyda": "Gilos tarkibida antioksidantlar bor, ular hujayralarni himoya qilishga yordam beradi. U yengil va shirin meva sifatida foydali hisoblanadi. Kam miqdorda tabiiy shakar beradi.",
        "istehmol": "Gilosni mavsumida yangi holida, kuniga bir hovuch miqdorida iste'mol qilish mumkin."
    },
    {
        "nom": "Olcha",
        "emoji": "🍒",
        "vitaminlar": "C, A, kaliy, tola",
        "foyda": "Olcha C vitaminiga boy bo'lib, immunitetga yordam beradi. Uning tolasi hazm tizimini qo'llab-quvvatlaydi. Nordon ta'mi ishtahani yaxshilashga foydali hisoblanadi.",
        "istehmol": "Olchani yuvib, yangi holida yeyish yoki murabbo uchun ishlatish mumkin."
    },
    {
        "nom": "Nok",
        "emoji": "🍐",
        "vitaminlar": "C, K, kaliy, tola",
        "foyda": "Nok tolaga boy bo'lib, hazm tizimiga yordam beradi. U organizm uchun yumshoq va foydali meva hisoblanadi. Tarkibida suv borligi uni tetiklashtiruvchi qiladi.",
        "istehmol": "Nokni yuvib, po'stlog'i bilan yangi holida iste'mol qilish foydali."
    },
    {
        "nom": "Behi",
        "emoji": "🍐",
        "vitaminlar": "C, A, kaliy, tola",
        "foyda": "Behi tolaga boy bo'lib, hazmga yordam beradi. U vitaminlar manbai sifatida foydali hisoblanadi. Tarkibida tabiiy pektin bo'lgani uchun hazm tizimi uchun foydali.",
        "istehmol": "Behini pishirib yoki kompot shaklida iste'mol qilish keng tarqalgan."
    },
    {
        "nom": "Shaftoli",
        "emoji": "🍑",
        "vitaminlar": "A, C, kaliy, tola",
        "foyda": "Shaftoli A va C vitaminlariga boy bo'lib, teri va ko'z salomatligiga yordam beradi. Uning tolasi hazmga foydali hisoblanadi. Suvli tarkibi organizmni namlashga hissa qo'shadi.",
        "istehmol": "Shaftolini yuvib, yangi holida yoki salatga qo'shib iste'mol qilish mumkin."
    },
    {
        "nom": "Limon",
        "emoji": "🍋",
        "vitaminlar": "C, folat, kaliy",
        "foyda": "Limon C vitaminiga boy bo'lib, immunitetga yordam beradi. U ovqatga nordon ta'm berib, ishtahani yaxshilashga foydali hisoblanadi. Antioksidantlar manbai sifatida tanilgan.",
        "istehmol": "Limonni suvga yoki taomga oz miqdorda qo'shib iste'mol qilish tavsiya etiladi."
    },
    {
        "nom": "Banan",
        "emoji": "🍌",
        "vitaminlar": "B6, C, kaliy, magniy",
        "foyda": "Banan kaliyga boy bo'lib, mushaklar ishlashiga yordam beradi. U tez energiya beruvchi meva hisoblanadi. Tarkibida B6 vitamini bo'lgani uchun foydali.",
        "istehmol": "Bananni nonushtada yoki mashqdan keyin energiya uchun iste'mol qilish mumkin."
    },
    {
        "nom": "Qulupnay",
        "emoji": "🍓",
        "vitaminlar": "C, K, folat, marganets",
        "foyda": "Qulupnay C vitaminiga juda boy bo'lib, immunitetga yordam beradi. Uning antioksidantlari hujayralarni himoya qilishga foydali hisoblanadi. Kam kaloriyali meva hisoblanadi.",
        "istehmol": "Qulupnayni yuvib, yangi holida yoki yogurt bilan iste'mol qilish mumkin."
    },
]

SABZAVOTLAR = [
    {
        "nom": "Sabzi",
        "emoji": "🥕",
        "vitaminlar": "A, K, kaliy, tola",
        "foyda": "Sabzi A vitaminiga boy bo'lib, ko'z salomatligiga yordam beradi. Uning tolasi hazm tizimi uchun foydali hisoblanadi. Tarkibida antioksidantlar ham bor.",
        "istehmol": "Sabzini yangi holida yoki taomlarga qo'shib iste'mol qilish foydali."
    },
    {
        "nom": "Pomidor",
        "emoji": "🍅",
        "vitaminlar": "C, K, kaliy, likopen",
        "foyda": "Pomidor likopenga boy bo'lib, hujayralarni himoya qilishga yordam beradi. U C vitamini manbai sifatida foydali hisoblanadi. Salatlarda ko'p ishlatiladigan sabzavot.",
        "istehmol": "Pomidorni yangi holida salatga qo'shib yoki pishirilgan taomlarda iste'mol qilish mumkin."
    },
    {
        "nom": "Bodring",
        "emoji": "🥒",
        "vitaminlar": "K, C, kaliy, suv",
        "foyda": "Bodring suvga boy bo'lib, organizmni namlashga yordam beradi. U kam kaloriyali sabzavot sifatida foydali hisoblanadi. Issiq kunlarda tetiklik beradi.",
        "istehmol": "Bodringni yuvib, yangi holida salatga qo'shib iste'mol qilish tavsiya etiladi."
    },
    {
        "nom": "Karam",
        "emoji": "🥬",
        "vitaminlar": "C, K, folat, tola",
        "foyda": "Karam C va K vitaminlariga boy bo'lib, immunitetga yordam beradi. Uning tolasi hazm tizimi uchun foydali hisoblanadi. Tarkibida antioksidantlar mavjud.",
        "istehmol": "Karamni salat, sho'rva yoki pishirilgan holda iste'mol qilish mumkin."
    },
    {
        "nom": "Brokkoli",
        "emoji": "🥦",
        "vitaminlar": "C, K, folat, tola",
        "foyda": "Brokkoli vitamin va tolaga boy bo'lib, organizmga yordam beradi. Uning antioksidantlari hujayralarni himoya qilishga foydali hisoblanadi. Turli taomlarga qo'shish mumkin.",
        "istehmol": "Brokkolini bug'da pishirib yoki qaynatib iste'mol qilish foydali."
    },
    {
        "nom": "Ismaloq",
        "emoji": "🥬",
        "vitaminlar": "A, C, K, temir, folat",
        "foyda": "Ismaloq temir va folatga boy bo'lib, qon tarkibiga yordam beradi. U A va K vitaminlari manbai sifatida foydali hisoblanadi. Ko'kat sifatida yengil hazm bo'ladi.",
        "istehmol": "Ismaloqni yangi holida salatga yoki pishirilgan taomga qo'shish mumkin."
    },
    {
        "nom": "Qovoq",
        "emoji": "🎃",
        "vitaminlar": "A, C, kaliy, tola",
        "foyda": "Qovoq A vitaminiga boy bo'lib, ko'z va teri salomatligiga yordam beradi. Uning tolasi hazm tizimi uchun foydali hisoblanadi. Pishirilganda yumshoq bo'ladi.",
        "istehmol": "Qovoqni pishirib, sho'rvaga yoki yormaga qo'shib iste'mol qilish mumkin."
    },
    {
        "nom": "Baqlajon",
        "emoji": "🍆",
        "vitaminlar": "K, C, kaliy, tola",
        "foyda": "Baqlajon tolaga boy bo'lib, hazm tizimiga yordam beradi. U tarkibida antioksidantlar saqlaydi va foydali hisoblanadi. Turli usulda pishirilishi mumkin.",
        "istehmol": "Baqlajonni pishirib yoki qovurib, yog'ni kam ishlatib iste'mol qilish tavsiya etiladi."
    },
    {
        "nom": "Piyoz",
        "emoji": "🧅",
        "vitaminlar": "C, B6, kaliy, antioksidantlar",
        "foyda": "Piyoz tarkibida antioksidantlar bor, ular organizmni himoya qilishga yordam beradi. U taomga xushbo'y ta'm beruvchi sabzavot hisoblanadi. C vitamini manbai sifatida foydali.",
        "istehmol": "Piyozni ko'p taomlarga qo'shib, pishirilgan yoki yangi holida iste'mol qilish mumkin."
    },
    {
        "nom": "Sarimsoq",
        "emoji": "🧄",
        "vitaminlar": "C, B6, marganets, antioksidantlar",
        "foyda": "Sarimsoq tabiiy antioksidantlarga boy bo'lib, organizmni himoya qilishga yordam beradi. U taomlarga kuchli ta'm beradi. Kichik miqdorda foydali hisoblanadi.",
        "istehmol": "Sarimsoqni oz miqdorda, yangi holida taomga qo'shib iste'mol qilish tavsiya etiladi."
    },
    {
        "nom": "Turp",
        "emoji": "🥬",
        "vitaminlar": "C, folat, kaliy, tola",
        "foyda": "Turp C vitaminiga boy bo'lib, immunitetga yordam beradi. Uning tolasi hazm uchun foydali hisoblanadi. Tarkibida suv bo'lgani uchun tetiklashtiradi.",
        "istehmol": "Turpni yuvib, yangi holida salatga qo'shib iste'mol qilish mumkin."
    },
    {
        "nom": "Lavlagi",
        "emoji": "🟣",
        "vitaminlar": "C, folat, kaliy, tola",
        "foyda": "Lavlagi folat va tolaga boy bo'lib, organizmga yordam beradi. U tabiiy shakar va vitaminlar manbai sifatida foydali hisoblanadi. Qon hosil bo'lishiga yordam beruvchi sabzavot hisoblanadi.",
        "istehmol": "Lavlagini qaynatib yoki salatga qo'shib iste'mol qilish mumkin."
    },
    {
        "nom": "Kartoshka",
        "emoji": "🥔",
        "vitaminlar": "C, B6, kaliy, tola",
        "foyda": "Kartoshka kaliy va C vitaminiga ega bo'lib, energiya beradi. U to'ydiruvchi sabzavot sifatida foydali hisoblanadi. B6 vitamini manbai hisoblanadi.",
        "istehmol": "Kartoshkani qaynatib yoki pishirib, yog'ni kam ishlatib iste'mol qilish tavsiya etiladi."
    },
    {
        "nom": "Sholg'om",
        "emoji": "🥕",
        "vitaminlar": "C, K, folat, kaliy",
        "foyda": "Sholg'om C vitaminiga boy bo'lib, immunitetga yordam beradi. Uning tolasi hazm tizimi uchun foydali hisoblanadi. Tarkibida vitamin va minerallar mavjud.",
        "istehmol": "Sholg'omni yangi holida yoki pishirilgan taomlarga qo'shib iste'mol qilish mumkin."
    },
    {
        "nom": "Ko'katlar",
        "emoji": "🌿",
        "vitaminlar": "A, C, K, folat, temir",
        "foyda": "Ko'katlar vitamin va minerallarga boy bo'lib, organizmga yordam beradi. Ular taomga xushbo'y ta'm beruvchi qo'shimcha hisoblanadi. Yengil hazm bo'lgani uchun foydali.",
        "istehmol": "Ko'katlarni yuvib, taom va salatlarga yangi holida qo'shib iste'mol qilish tavsiya etiladi."
    },
]
