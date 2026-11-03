"""Sog'lom ovqatlanish bo'yicha ma'lumotlar to'plami.

Bu modul Telegram ta'lim boti uchun sog'lom va muvozanatli ovqatlanish
haqidagi umumiy ma'lumotlarni saqlaydi. Barcha matnlar umumiy ovqatlanish
bilimlariga asoslangan bo'lib, foydali hisoblanadi degan xulosalar beradi.
Modulda uchta ro'yxat mavjud: ovqatlanish tamoyillari, taxminiy ratsion
namunalari va tabiiy (kam qayta ishlangan) mahsulotlar tavsiyalari.
"""

TAMOYILLAR = [
    {
        "sarlavha": "Muvozanatli ratsion",
        "matn": "Muvozanatli ratsion - bu organizm uchun zarur bo'lgan barcha ozuqa moddalarini to'g'ri nisbatda olish demakdir. Har bir taomda oqsil, murakkab uglevod va foydali yog'lar bo'lishi maqsadga muvofiqdir. Bir xil mahsulotlarga qarab qolmaslik, balki turli xil taomlarni almashtirib iste'mol qilish foydali hisoblanadi. Shu tarzda organizm zarur vitamin va minerallarni to'liqroq oladi.",
    },
    {
        "sarlavha": "Tarelka qoidasi",
        "matn": "Tarelka qoidasi ovqatni ko'z bilan to'g'ri taqsimlashga yordam beradi. Tarelkaning yarmini sabzavot va ko'katlar, chorak qismini murakkab uglevodlar, qolgan choragini oqsil manbalari egallashi tavsiya etiladi. Bu oddiy usul porsiya hajmini nazorat qilishga ko'maklashadi. Bunday taqsimot ko'pchilik uchun foydali hisoblanadi.",
    },
    {
        "sarlavha": "Nonushta ahamiyati",
        "matn": "Nonushta kun davomida energiya va diqqatni saqlashga yordam beradi. Ertalabki taomni o'tkazib yuborish ko'pchilikda keyinroq ortiqcha ochlik va shoshilinch gazaklarga olib kelishi mumkin. To'liq nonushta don mahsulotlari, oqsil va mevalardan iborat bo'lsa foydali hisoblanadi. Shuning uchun nonushtaga vaqt ajratish tavsiya etiladi.",
    },
    {
        "sarlavha": "Kunlik meva va sabzavot miqdori",
        "matn": "Meva va sabzavotlar tolaga, vitaminlarga va antioksidantlarga boy hisoblanadi. Kuniga kamida besh porsiya meva va sabzavot iste'mol qilish ko'pchilik mutaxassislar tomonidan tavsiya etiladi. Ularni har bir asosiy taomga qo'shish yoki gazak sifatida ishlatish qulay usuldir. Rangi va turi bo'yicha xilma-xil tanlash yanada foydali hisoblanadi.",
    },
    {
        "sarlavha": "Tola (fibra)",
        "matn": "Tola hazm tizimining ishlashiga yordam beradi va uzoq vaqt to'q tutishga ko'maklashadi. U butun don mahsulotlari, dukkaklilar, sabzavot va mevalarda ko'p uchraydi. Ratsionga yetarli tola qo'shish ovqat hazmini yaxshilashga yordam beradi. Buning uchun oq non o'rniga butun donli mahsulotlarni tanlash maqsadga muvofiqdir.",
    },
    {
        "sarlavha": "Sog'lom yog'lar",
        "matn": "Yog'lar organizm uchun muhim bo'lib, ular energiya manbai hisoblanadi. To'yinmagan yog'lar zaytun moyi, yong'oq va baliqda ko'p uchraydi. Bunday yog'lar yurak-qon tomir tizimi uchun foydali hisoblanadi. Qovurilgan mahsulotlar va qattiq yog'larni kamaytirib, sog'lom manbalarni tanlash tavsiya etiladi.",
    },
    {
        "sarlavha": "Shakar va shirinliklarni cheklash",
        "matn": "Qo'shilgan shakar miqdorini kamaytirish ko'pchilik uchun foydali hisoblanadi. Shirin ichimliklar va shirinliklar ko'p miqdorda bo'sh kaloriya beradi. Ularni meva yoki tabiiy shirinliklar bilan almashtirish yaxshi yechim bo'ladi. Shakarni me'yorida iste'mol qilish sog'liq uchun tavsiya etiladi.",
    },
    {
        "sarlavha": "Tuzni kamaytirish",
        "matn": "Ortiqcha tuz iste'moli ko'pchilik uchun maqbul emas. Tayyor mahsulotlar, konservalar va gazaklar ko'p tuz saqlaydi. Taom tayyorlashda tuzni asta-sekin kamaytirib, ziravorlar va ko'katlar bilan ta'mni yaxshilash mumkin. Tuzni me'yorida iste'mol qilish foydali hisoblanadi.",
    },
    {
        "sarlavha": "Qayta ishlangan mahsulotlar",
        "matn": "Qayta ishlangan mahsulotlar ko'pincha ko'p tuz, shakar va qo'shimchalarni saqlaydi. Kolbasa, tayyor gazak va yarim tayyor mahsulotlarni kamaytirish tavsiya etiladi. Ularning o'rniga tabiiy va kam ishlangan mahsulotlarni tanlash foydali hisoblanadi. Uy sharoitida tayyorlangan taomlar odatda yanada sog'lom bo'ladi.",
    },
    {
        "sarlavha": "Porsiya nazorati",
        "matn": "Porsiya hajmini nazorat qilish to'yib ovqatlanish va vaznni boshqarishga yordam beradi. Kichikroq idishlardan foydalanish ko'pchilik uchun foydali hisoblanadi. Ovqatni sekin iste'mol qilish to'qlik belgisini o'z vaqtida sezishga ko'maklashadi. Shoshilmasdan, miqdorga e'tibor berib ovqatlanish tavsiya etiladi.",
    },
]

RATSION = [
    {
        "sarlavha": "Kunlik ovqatlanish tartibi",
        "matn": "Kunlik ovqatlanishni uch asosiy taom va bir-ikki gazakka bo'lish tavsiya etiladi. Har bir taomni taxminan bir xil vaqt oralig'ida iste'mol qilish organizmga qulay hisoblanadi. Doimiy tartib ochlikni nazorat qilishga yordam beradi. Shunday qilib, kun davomida energiya barqaror saqlanadi.",
    },
    {
        "sarlavha": "Nonushta misoli",
        "matn": "Nonushtaga butun donli bo'tqa yoki jo'xori parhezi mos keladi. Unga tuxum, qatiq yoki kam yog'li sut mahsuloti qo'shish oqsilni oshiradi. Bir-ikki porsiya meva yoki yong'oq taomni yanada to'yimli qiladi. Bunday nonushta kunga yaxshi boshlanish hisoblanadi.",
    },
    {
        "sarlavha": "Tushlik misoli",
        "matn": "Tushlikning asosini don, dukkakli yoki grechka kabi murakkab uglevodlar tashkil qilishi mumkin. Unga tovuq yoki baliq kabi oqsil manbasi qo'shish foydali hisoblanadi. Sabzavotli salat yoki bug'langan sabzavot taomni to'ldiradi. Shu tarkib tushlikni muvozanatli qiladi.",
    },
    {
        "sarlavha": "Kechki ovqat misoli",
        "matn": "Kechki ovqatni yengilroq qilish ko'pchilik uchun qulay hisoblanadi. Sabzavotli taom, ozgina oqsil va kam miqdorda uglevod mos keladi. Kechqurun og'ir va yog'li taomlardan saqlanish tavsiya etiladi. Ovqatni yotishdan bir necha soat oldin iste'mol qilish maqsadga muvofiqdir.",
    },
    {
        "sarlavha": "Sog'lom gazaklar",
        "matn": "Gazak sifatida meva, sabzavot, yong'oq yoki qatiq tanlash foydali hisoblanadi. Shirin va tuzli tayyor gazaklar o'rniga tabiiy mahsulotlar afzal ko'riladi. Gazakni asosiy taomlar orasida, ochlik kuchaymasidan oldin iste'mol qilish tavsiya etiladi. Bu ortiqcha ovqatlanishning oldini olishga yordam beradi.",
    },
    {
        "sarlavha": "Ichimliklar tanlovi",
        "matn": "Eng yaxshi ichimlik - bu oddiy toza suv hisoblanadi. Shirin gazlangan ichimliklar va shakarli sharbatlar o'rniga suv yoki shakarsiz choy tanlash yaxshi bo'ladi. Kun davomida yetarli suv ichish foydali hisoblanadi. Toza suv organizmning normal ishlashiga yordam beradi.",
    },
    {
        "sarlavha": "Oziq-ovqat xarid qilish",
        "matn": "Xarid qilishdan oldin oddiy ro'yxat tuzish rejali va foydali hisoblanadi. Ro'yxat ortiqcha va tasodifiy mahsulot sotib olishni kamaytiradi. Asosan tabiiy mahsulotlar, sabzavot va don mahsulotlariga ustuvorlik berish tavsiya etiladi. Mahsulot tarkibini o'qib, tarkibida shakar va tuz kam bo'lganini tanlash maqsadga muvofiqdir.",
    },
    {
        "sarlavha": "Taom tayyorlash usullari",
        "matn": "Bug'lash, pishirish va qaynatish taomni tayyorlashning foydali usullari hisoblanadi. Ko'p yog'da qovurishdan iloji boricha saqlanish tavsiya etiladi. Sabzavotlarni qisqa vaqt pishirish ularning foydali xususiyatlarini saqlashga yordam beradi. Shu usullar taomni yengil va sog'lom qiladi.",
    },
    {
        "sarlavha": "Mavsumiy mahsulotlar",
        "matn": "Mavsumiy sabzavot va mevalar odatda yangi va ta'mli bo'ladi. Ular ko'pincha arzon va foydali hisoblanadi. Mavsumga mos mahsulotlardan foydalanish ratsionni xilma-xil qilishga yordam beradi. Shu tarzda taomlar tabiiy va to'yimli bo'ladi.",
    },
    {
        "sarlavha": "To'yib ovqatlanish va vazn nazorati",
        "matn": "To'yib ovqatlanish ochlikni nazorat qilish va vaznni boshqarishga yordam beradi. Sekin iste'mol qilish va porsiyaga e'tibor berish foydali hisoblanadi. Muntazam jismoniy harakat bilan birga sog'lom ovqatlanish yaxshi natija beradi. Ovqatlanishda muvozanatni saqlash uzoq muddatda yordam beradi.",
    },
]

TABIIY_MAHSULOTLAR = [
    {
        "nom": "Jo'xori",
        "emoji": "🌾",
        "foyda": "Jo'xori tolaga boy bo'lib, uzoq vaqt to'q tutishga yordam beradi. U murakkab uglevodlar manbai sifatida foydali hisoblanadi.",
        "istehmol": "Nonushtaga jo'xori parhezini tayyorlab, ustiga meva qo'shib iste'mol qilish tavsiya etiladi.",
    },
    {
        "nom": "Suli",
        "emoji": "🥣",
        "foyda": "Suli tolaga va foydali uglevodlarga boy hisoblanadi. U hazm tizimining normal ishlashiga yordam beradi.",
        "istehmol": "Suli bo'tqasini suv yoki kam yog'li sut bilan tayyorlab, nonushtaga iste'mol qilish mumkin.",
    },
    {
        "nom": "Grechka",
        "emoji": "🌾",
        "foyda": "Grechka oqsil, tola va minerallarga boy don hisoblanadi. U uzoq vaqt to'q tutishga yordam beradi.",
        "istehmol": "Grechkani yon taom sifatida sabzavot bilan birga iste'mol qilish maqsadga muvofiqdir.",
    },
    {
        "nom": "Loviya",
        "emoji": "🫘",
        "foyda": "Loviya o'simlik oqsili va tolaga boy hisoblanadi. U to'yimli va foydali mahsulotlardan biri sanaladi.",
        "istehmol": "Loviyani sho'rva yoki sabzavotli taomlarga qo'shib iste'mol qilish tavsiya etiladi.",
    },
    {
        "nom": "No'xat",
        "emoji": "🫛",
        "foyda": "No'xat oqsil va tolaga boy dukkakli mahsulot hisoblanadi. U to'yimli va foydali hisoblanadi.",
        "istehmol": "No'xatni salat yoki sabzavotli taomlarga qo'shib iste'mol qilish mumkin.",
    },
    {
        "nom": "Yasmiq",
        "emoji": "🫘",
        "foyda": "Yasmiq o'simlik oqsili va tolaga boy hisoblanadi. U to'yimli taomlar tayyorlash uchun foydali mahsulot sanaladi.",
        "istehmol": "Yasmiqdan sho'rva yoki bo'tqa tayyorlab, sabzavot bilan iste'mol qilish tavsiya etiladi.",
    },
    {
        "nom": "Yong'oqlar",
        "emoji": "🥜",
        "foyda": "Yong'oqlar foydali yog'lar, oqsil va minerallarga boy hisoblanadi. Ular kichik miqdorda to'yimli gazak bo'ladi.",
        "istehmol": "Yong'oqlarni me'yorida, kuniga bir hovuch atrofida iste'mol qilish tavsiya etiladi.",
    },
    {
        "nom": "Bodom",
        "emoji": "🌰",
        "foyda": "Bodom foydali yog'lar, oqsil va tolaga boy hisoblanadi. U to'yimli gazak sifatida foydali sanaladi.",
        "istehmol": "Bodomni me'yorida, kichik miqdorda gazak sifatida iste'mol qilish maqsadga muvofiqdir.",
    },
    {
        "nom": "Yong'oq mag'zi",
        "emoji": "🌰",
        "foyda": "Yong'oq mag'zi foydali yog'lar va oqsilga boy hisoblanadi. U organizm uchun foydali mahsulot sanaladi.",
        "istehmol": "Yong'oq mag'zini me'yorida salat yoki nonushtaga qo'shib iste'mol qilish tavsiya etiladi.",
    },
    {
        "nom": "Kunjut",
        "emoji": "🌱",
        "foyda": "Kunjut foydali yog'lar va minerallarga boy hisoblanadi. U oz miqdorda ham to'yimli hisoblanadi.",
        "istehmol": "Kunjutni non yoki salatlarga seping yoki me'yorida iste'mol qilish mumkin.",
    },
    {
        "nom": "Zaytun moyi",
        "emoji": "🫒",
        "foyda": "Zaytun moyi to'yinmagan yog'larga boy foydali mahsulot hisoblanadi. U salatlar uchun mos keladi.",
        "istehmol": "Zaytun moyini salatlarga oz miqdorda qo'shib iste'mol qilish tavsiya etiladi.",
    },
    {
        "nom": "Asal",
        "emoji": "🍯",
        "foyda": "Asal tabiiy shirin mahsulot bo'lib, oz miqdorda iste'mol qilinganda foydali hisoblanadi. U choy bilan birga ishlatilishi mumkin.",
        "istehmol": "Asalni me'yorida iste'mol qilish tavsiya etiladi, chunki u shakar manbai hisoblanadi.",
    },
    {
        "nom": "Qatiq",
        "emoji": "🥛",
        "foyda": "Qatiq oqsil va foydali bakteriyalarga boy sut mahsuloti hisoblanadi. U hazm tizimiga yordam beradi.",
        "istehmol": "Qatiqni gazak sifatida yoki taomlarga qo'shib iste'mol qilish mumkin.",
    },
    {
        "nom": "Tvorog",
        "emoji": "🧀",
        "foyda": "Tvorog oqsil va kaltsiyga boy sut mahsuloti hisoblanadi. U to'yimli va foydali sanaladi.",
        "istehmol": "Tvorogni nonushtaga meva bilan birga iste'mol qilish tavsiya etiladi.",
    },
    {
        "nom": "Tuxum",
        "emoji": "🥚",
        "foyda": "Tuxum oqsil va muhim vitaminlarga boy hisoblanadi. U to'yimli mahsulot sifatida foydali sanaladi.",
        "istehmol": "Tuxumni qaynatib yoki pishirib, nonushtaga iste'mol qilish mumkin.",
    },
    {
        "nom": "Baliq",
        "emoji": "🐟",
        "foyda": "Baliq oqsil va foydali yog'larga boy hisoblanadi. U yurak-qon tomir tizimi uchun foydali sanaladi.",
        "istehmol": "Baliqni haftada bir necha marta bug'lash yoki pishirish usulida iste'mol qilish tavsiya etiladi.",
    },
    {
        "nom": "Tovuq go'shti",
        "emoji": "🍗",
        "foyda": "Tovuq go'shti oqsilga boy va nisbatan yengil mahsulot hisoblanadi. U to'yimli taomlar uchun foydali sanaladi.",
        "istehmol": "Tovuq go'shtini terisini olib tashlab, pishirish yoki bug'lash usulida iste'mol qilish mumkin.",
    },
    {
        "nom": "Karam",
        "emoji": "🥬",
        "foyda": "Karam tolaga, vitamin va minerallarga boy sabzavot hisoblanadi. U kam kaloriya bilan to'ydiradi.",
        "istehmol": "Karamni salat yoki pishirilgan taomlarga qo'shib iste'mol qilish tavsiya etiladi.",
    },
    {
        "nom": "Kungaboqar urug'i",
        "emoji": "🌻",
        "foyda": "Kungaboqar urug'i foydali yog'lar va oqsilga boy hisoblanadi. U to'yimli gazak sifatida foydali sanaladi.",
        "istehmol": "Kungaboqar urug'ini me'yorida, tuzsiz holda iste'mol qilish maqsadga muvofiqdir.",
    },
    {
        "nom": "Quritilgan mevalar",
        "emoji": "🍇",
        "foyda": "Quritilgan mevalar tolaga va minerallarga boy hisoblanadi. Ular oz miqdorda to'yimli gazak bo'ladi.",
        "istehmol": "Quritilgan mevalarni me'yorida iste'mol qilish tavsiya etiladi, chunki ularda tabiiy shakar ko'p.",
    },
]
