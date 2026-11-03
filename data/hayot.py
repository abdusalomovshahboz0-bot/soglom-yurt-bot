"""«Sog'lom Yurt Education» boti uchun sog'lom turmush tarzi ma'lumotlari.

Bu modul faqat matnli ma'lumotlarni saqlaydi: kundalik foydali odatlar,
shaxsiy gigiyena bo'yicha ta'lim materiallari, ertalabki mashqlar,
uyda bajariladigan mashqlar va qisqa kundalik maslahatlar.

Barcha ma'lumotlar umumiy sog'lom turmush tarzi tavsiyalaridan iborat bo'lib,
faqat keng tarqalgan va xavfsiz maslahatlarni o'z ichiga oladi.
Bu yerda hech qanday tashxis, dori nomi yoki davolash usuli berilmaydi.
Har qanday mashq paytida og'riq yoki bosh aylanishi sezilsa, mashqni to'xtatish
va zarur bo'lganda shifokorga murojaat qilish tavsiya etiladi.
"""

KUNLIK_ODATLAR = [
    {
        "nom": "Ertalab bir stakan suv",
        "emoji": "💧",
        "matn": "Tunda tana suv yo'qotadi, shuning uchun ertalab bir stakan iliq suv ichish foydali. "
        "Bu hazm tizimini yumshatadi va kunni tetik boshlashga yordam beradi. "
        "Suvni kichik qultumlar bilan, shoshilmasdan iching.",
    },
    {
        "nom": "Ertalabki mashq",
        "emoji": "🤸",
        "matn": "Kunni qisqa yengil mashq bilan boshlash tanani uyg'otadi. "
        "Beshta daqiqalik qizish mashqlari ham yetarli natija beradi. "
        "Harakatlarni sekin va o'zingizga qulay tezlikda bajaring.",
    },
    {
        "nom": "Sog'lom nonushta",
        "emoji": "🥣",
        "matn": "Nonushta kunga energiya beradigan asosiy taomdir. "
        "Bo'tqa, sut mahsuloti, tuxum yoki meva kabi to'ydiruvchi taomlarni tanlang. "
        "Nonushtani o'tkazib yubormaslik kun bo'yi tetik yurishga yordam beradi.",
    },
    {
        "nom": "Kun bo'yi suv ichish",
        "emoji": "🚰",
        "matn": "Kuniga taxminan 6-8 stakan suv ichish tanaga foyda keltiradi. "
        "Suv ichishni eslatish uchun yoningizda shisha saqlang. "
        "Issiq havoda va harakat paytida suvga bo'lgan ehtiyoj ortadi.",
    },
    {
        "nom": "Kunlik sayr",
        "emoji": "🚶",
        "matn": "Har kuni kamida 30 daqiqa piyoda yurish yurak va kayfiyat uchun foydali. "
        "Sayrni ertalab yoki kechqurun, toza havoda qilish yaxshi. "
        "Yo'lni bosqichma-bosqich uzaytirib boring.",
    },
    {
        "nom": "Yetarli uyqu",
        "emoji": "😴",
        "matn": "Kuniga 7-8 soat uxlash tana va xotirani tiklaydi. "
        "Yotish va uyg'onish vaqtini iloji boricha bir xil saqlang. "
        "Yotishdan oldin xonani qorong'i va sokin qilishga harakat qiling.",
    },
    {
        "nom": "Ekran vaqtini cheklash",
        "emoji": "📱",
        "matn": "Telefon va kompyuter oldida uzoq o'tirish ko'z va tanani charchatadi. "
        "Har soatda o'rnidan turib, bir necha daqiqa yurib oling. "
        "Yotishdan oldin ekran vaqtini kamaytirish uyquni yaxshilaydi.",
    },
    {
        "nom": "Toza havoda nafas olish",
        "emoji": "🌳",
        "matn": "Kuniga bir necha daqiqa toza havoda bo'lish kayfiyatni ko'taradi. "
        "Deraza yonida yoki hovlida chuqur nafas olish foydali. "
        "Bunday qisqa tanaffuslar stressni kamaytirishga yordam beradi.",
    },
    {
        "nom": "Sog'lom gazak",
        "emoji": "🍎",
        "matn": "Shirinlik va chips o'rniga meva, yong'oq yoki sabzavot tanlang. "
        "Sog'lom gazak ochlikni yengillashtiradi va foydali moddalar beradi. "
        "Gazakni kichik porsiyalarda iste'mol qilish yaxshi.",
    },
    {
        "nom": "Kechki ovqatni yengil qilish",
        "emoji": "🥗",
        "matn": "Kechki ovqatni yotishdan 2-3 soat oldin yeyish tavsiya etiladi. "
        "Kechqurun og'ir taomlardan ko'ra yengil taomlar tanlanadi. "
        "Bu hazmni osonlashtiradi va uyquni yaxshilaydi.",
    },
    {
        "nom": "Dam olish va nafas mashqi",
        "emoji": "🧘",
        "matn": "Kun davomida bir necha daqiqa tinch o'tirish foydali. "
        "Chuqur nafas olib, sekin chiqarish xotirjamlikni beradi. "
        "Bunday qisqa tanaffus ish unumdorligini ham oshiradi.",
    },
    {
        "nom": "Kun tartibini rejalashtirish",
        "emoji": "📝",
        "matn": "Kun uchun qisqa reja tuzish tartibsizlikni kamaytiradi. "
        "Muhim ishlarni birinchi navbatda belgilang. "
        "Reja tuzish vaqtni boshqarishga va xotirjam bo'lishga yordam beradi.",
    },
]

GIGIYENA = [
    {
        "sarlavha": "Qo'l yuvish tartibi",
        "matn": "Qo'lni har kuni bir necha marta sovun bilan yuvish eng oddiy himoya usullaridan biridir. "
        "Ovqatdan oldin, hojatxonadan keyin, ko'chadan kelgach va hayvonlar bilan muloqotdan so'ng qo'lni yuvish kerak. "
        "Qo'lni ho'llab, sovun bilan 20-30 soniya davomida kaft, barmoq orasi va tirnoq ostini ishqalang. "
        "So'ng toza suvda chayib, qo'lni toza sochiq bilan quriting.",
    },
    {
        "sarlavha": "Tish tozalash",
        "matn": "Tishlarni kuniga ikki marta, ertalab va yotishdan oldin tozalash tavsiya etiladi. "
        "Yumshoq cho'tka bilan tish yuzasini aylanma harakatlarda, har bir tishni alohida tozalang. "
        "Tozalash taxminan ikki daqiqa davom etishi kerak. "
        "Tish cho'tkasini 2-3 oyda bir marta almashtirish foydali.",
    },
    {
        "sarlavha": "Cho'milish",
        "matn": "Tana tozaligi uchun har kuni iliq suvda yuvinish tavsiya etiladi. "
        "Issiq kunlarda yoki harakatdan keyin cho'milish terini tozalab, o'zini yengil his qilishga yordam beradi. "
        "Sovun yoki gel bilan tanani yumshoq harakatlarda yuvib, keyin toza suvda chaying. "
        "Cho'milgandan so'ng tanani quritib, toza kiyim kiying.",
    },
    {
        "sarlavha": "Tirnoq parvarishi",
        "matn": "Tirnoqlarni toza va qisqa holatda saqlash qo'l gigiyenasining muhim qismidir. "
        "Tirnoq ostida chang va mayda zarralar to'planadi, shuning uchun ularni muntazam tozalab turing. "
        "Tirnoqlarni tekis qirqib, o'tkir qirralarni tekislash tavsiya etiladi. "
        "Qirqish asboblarini faqat o'zingizga ishlatish yaxshi.",
    },
    {
        "sarlavha": "Kiyim va poyabzal tozaligi",
        "matn": "Kiyimni muntazam almashtirib, toza saqlash tana salomatligi uchun foydalidir. "
        "Ichki kiyim va paypoqni har kuni almashtirish tavsiya etiladi. "
        "Poyabzalni kunda shamollatib, vaqti-vaqti bilan tozalab turing. "
        "Nam yoki iflos poyabzalda uzoq yurish oyoq uchun noqulaydir.",
    },
    {
        "sarlavha": "Soch parvarishi",
        "matn": "Sochni haftada bir necha marta yuvish va muntazam tarash tavsiya etiladi. "
        "Bosh terisiga mos yumshoq shampuan tanlang va sochni kuchli ishqalamang. "
        "Soch nam holatda ekan, uni ehtiyotkorlik bilan tarang. "
        "Toza soch bosh terisini sog'lom saqlashga yordam beradi.",
    },
    {
        "sarlavha": "Oshxona gigiyenasi",
        "matn": "Ovqat tayyorlashdan oldin qo'lni yuvish va ish yuzasini toza saqlash zarur. "
        "Kesish taxtasi va pichoqlarni xom go'sht, sabzavot va nondan keyin yuvib turing. "
        "Idishlarni issiq suv va tozalash vositasi bilan yuvib, yaxshilab chaying. "
        "Oshxonadagi sochiq va lattani tez-tez almashtiring.",
    },
    {
        "sarlavha": "Mahsulotlarni yuvish",
        "matn": "Sabzavot va mevalarni iste'moldan oldin toza suvda yaxshilab yuvish tavsiya etiladi. "
        "Ularning sirtida chang va tuproq qolishi mumkin, shuning uchun yaxshilab chaying. "
        "Ko'katlarni ham bir necha marta suvda yuvib turing. "
        "Yuvilgan mahsulotlarni toza idishda saqlang.",
    },
    {
        "sarlavha": "Shaxsiy buyumlar",
        "matn": "Tish cho'tkasi, sochiq, taroq va shaxsiy idishlar faqat o'zingizga tegishli bo'lishi kerak. "
        "Bunday buyumlarni boshqalar bilan bo'lishmaslik himoya qiladi. "
        "Sochiq va taroqni tez-tez yuvib, quruq joyda saqlang. "
        "Har bir oila a'zosining o'z buyumlari bo'lsa yaxshi.",
    },
    {
        "sarlavha": "Jamoat joylarida gigiyena",
        "matn": "Jamoat joylarida tutqich, eshik va lift tugmalariga tegib, keyin qo'lni yuvishni unutmang. "
        "Yo'talganda yoki aksirganda og'iz va burunni tirsak ichi yoki salfetka bilan yoping. "
        "Kasal paytida uyda qolish va boshqalardan masofa saqlash foydali. "
        "Qo'l yuvish imkoni bo'lmasa, bu ishni imkon topishingiz bilan bajaring.",
    },
    {
        "sarlavha": "Uy tozaligi va shamollatish",
        "matn": "Xonani kuniga kamida ikki marta 5-10 daqiqa shamollatish havoni yangilaydi. "
        "Uy yuzalarini nam latta bilan muntazam artib, changni tozalab turing. "
        "Idish-tovoq va chiqindilarni vaqtida tozalash muhim. "
        "Toza va havodor uy kayfiyatni ham yaxshilaydi.",
    },
    {
        "sarlavha": "Oziq-ovqat saqlash qoidalari",
        "matn": "Ovqatni salqin joyda va yopiq idishda saqlash tavsiya etiladi. "
        "Tayyor ovqatni xom mahsulotlardan alohida saqlang. "
        "Buzilgan yoki hidi o'zgargan ovqatni iste'mol qilmang. "
        "Pishirilgan taomni uzoq vaqt xona haroratida qoldirmaslik kerak.",
    },
]

ERTALABKI_MASHQ = [
    {
        "nom": "Uyg'onish va yengil qizish",
        "davomiylik": "5 daqiqa",
        "qadamlar": [
            "Joyida asta-sekin yuring.",
            "Qo'llarni yuqoriga cho'zing.",
            "Yelkalarni oldinga va orqaga aylantiring.",
            "Boshni sekin chapga va o'ngga buring.",
            "Chuqur nafas olib, sekin chiqaring.",
        ],
        "foyda": "Bu mashqlar tanani uyg'otadi va kunni tetik boshlashga yordam beradi. "
        "Harakatlar sekin bajarilganda bo'g'inlar ham yumshaydi.",
    },
    {
        "nom": "Bo'yin va yelka",
        "davomiylik": "4 daqiqa",
        "qadamlar": [
            "Bo'yinni sekin oldinga egib, keyin tik tuting.",
            "Bo'yinni chapga va o'ngga sekin buring.",
            "Yelkalarni yuqoriga ko'tarib, tushiring.",
            "Yelkalarni aylana harakatda aylantiring.",
            "Qo'llarni yon tomonga yozing.",
        ],
        "foyda": "Bo'yin va yelka mashqlari uzoq o'tirishdan keyingi taranglikni kamaytiradi. "
        "Ularni sog'lom harakat bilan boshlash kun bo'yi qulaylik beradi.",
    },
    {
        "nom": "Qo'l va bilak",
        "davomiylik": "4 daqiqa",
        "qadamlar": [
            "Qo'llarni oldinga uzatib, barmoqlarni ochib-yoping.",
            "Kaftlarni tashqariga va ichkariga buring.",
            "Bilaklarni aylana harakatda aylantiring.",
            "Qo'llarni yelka balandligida ko'taring.",
            "Tirsaklarni sekin bukib-yozing.",
        ],
        "foyda": "Qo'l va bilak mashqlari kundalik ishda band bo'lgan mushaklarni bo'shashtiradi. "
        "Ularni yumshoq bajarsangiz, qo'llar yengil bo'ladi.",
    },
    {
        "nom": "Bel va yon tomonlar",
        "davomiylik": "5 daqiqa",
        "qadamlar": [
            "Qo'llarni belga qo'ying.",
            "Gavdani sekin chapga va o'ngga eging.",
            "Gavdani oldinga egib, keyin tik turing.",
            "Torsni sekin chapga va o'ngga buring.",
            "Barcha harakatlarni silliq bajaring.",
        ],
        "foyda": "Bel mashqlari gavdaning egiluvchanligini yaxshilaydi. "
        "Silliq harakatlar tanani kunga tayyorlaydi.",
    },
    {
        "nom": "Oyoq va to'piq",
        "davomiylik": "4 daqiqa",
        "qadamlar": [
            "To'piqlarni aylana harakatda aylantiring.",
            "Oyoq uchida ko'tarilib, tushing.",
            "Tizzalarni sekin bukib-yozing.",
            "Har bir oyoqni navbat bilan ko'taring.",
            "Joyida yengil harakat qiling.",
        ],
        "foyda": "Oyoq mashqlari yurishga tayyorgarlik ko'radi va qadamni yengillashtiradi. "
        "To'piq harakatlari ertalab qattiqlikni kamaytiradi.",
    },
    {
        "nom": "Joyida yurish va yugurish",
        "davomiylik": "6 daqiqa",
        "qadamlar": [
            "Joyida 2 daqiqa tinch yuring.",
            "Tezlikni asta-sekin oshiring.",
            "Qo'llarni harakatga moslashtiring.",
            "2 daqiqa joyida yengil yuguring.",
            "Yana 2 daqiqa yurib, nafasni tiklang.",
        ],
        "foyda": "Bu qism yurak va nafas tizimini o'rtacha yuklaydi. "
        "Kunlik energiya darajasini oshirishga yordam beradi.",
    },
    {
        "nom": "Cho'zilish bilan yakun",
        "davomiylik": "5 daqiqa",
        "qadamlar": [
            "Qo'llarni yuqoriga cho'zib ushlab turing.",
            "Yon tomonlarga sekin egilib cho'ziling.",
            "Oyoqni oldinga cho'zib, gavdani egang.",
            "Orqani sekin aylantirib, bo'shashtiring.",
            "Har bir holatda 10-15 soniya turing.",
        ],
        "foyda": "Cho'zilish mushaklarni bo'shashtiradi va harakat oralig'ini kengaytiradi. "
        "Mashqni yumshoq yakunlash tanaga qulaylik beradi.",
    },
    {
        "nom": "Nafas tiklash",
        "davomiylik": "3 daqiqa",
        "qadamlar": [
            "Tik turib yoki o'tirib, tinchlaning.",
            "Burun orqali chuqur nafas oling.",
            "Og'iz orqali sekin chiqaring.",
            "Buni o'n marta takrorlang.",
            "Yelkalar bo'sh turishiga e'tibor bering.",
        ],
        "foyda": "Nafas mashqi yurak urishini tinchlantiradi va diqqatni jamlaydi. "
        "Kunni xotirjam boshlashga yordam beradi.",
    },
]

UY_MASHQLARI = [
    {
        "nom": "Umumiy badan tarbiya",
        "daraja": "Oson",
        "davomiylik": "15 daqiqa",
        "mashqlar": [
            "Joyida yurish - 2 daqiqa",
            "Yelka aylantirish - 10 marta",
            "Oldinga egilish - 10 marta",
            "Chuqur cho'kish - 8 marta",
            "Oyoq uchida ko'tarilish - 12 marta",
            "Yon tomonga egilish - 10 marta",
        ],
        "foyda": "Bu mashqlar butun tanani bir tekis harakatga keltiradi. "
        "Boshlovchilar uchun mos va uyda bajarish oson.",
        "ehtiyot": "Mashq paytida og'riq yoki bosh aylanishi sezilsa, darhol to'xtang va zarur bo'lsa shifokorga murojaat qiling.",
    },
    {
        "nom": "Qorin mushaklari",
        "daraja": "O'rta",
        "davomiylik": "12 daqiqa",
        "mashqlar": [
            "Yotib oyoq ko'tarish - 10 marta",
            "Qisqa qorin harakati - 8 marta",
            "Plank holati - 20 soniya",
            "Yon plank - har tomonga 15 soniya",
            "Tizza bukib qorin harakati - 10 marta",
            "Qo'llarni cho'zib ko'tarilish - 8 marta",
        ],
        "foyda": "Qorin mushaklari mashqi gavdani tik tutishga yordam beradi. "
        "Bel atrofidagi mushaklarni mustahkamlaydi.",
        "ehtiyot": "Bel sohasida og'riq sezsangiz, mashqni to'xtating va kerak bo'lsa shifokor bilan maslahatlashing.",
    },
    {
        "nom": "Oyoq va dumba",
        "daraja": "O'rta",
        "davomiylik": "15 daqiqa",
        "mashqlar": [
            "Chuqur cho'kish - 12 marta",
            "Oldinga qadam qo'yish - har oyoqqa 8 marta",
            "Dumba ko'tarish - 12 marta",
            "Oyoqni yon tomonga ko'tarish - har oyoqqa 10 marta",
            "Tizza bukish - 12 marta",
            "Oyoq uchida turish - 15 marta",
        ],
        "foyda": "Bu mashqlar oyoq va dumba mushaklarini kuchaytiradi. "
        "Yurish va zinapoyaga chiqish osonlashadi.",
        "ehtiyot": "Tizzada noqulaylik yoki og'riq paydo bo'lsa, mashqni to'xtatib, kerak bo'lsa shifokorga murojaat qiling.",
    },
    {
        "nom": "Qo'l va yelka",
        "daraja": "O'rta",
        "davomiylik": "12 daqiqa",
        "mashqlar": [
            "Devorga tayanib surilish - 8 marta",
            "Qo'lni yon tomonga ko'tarish - 12 marta",
            "Tirsakni bukib-yozish - 12 marta",
            "Yelka aylantirish - 10 marta",
            "Qo'llarni yuqoriga ko'tarish - 10 marta",
            "Kaftlarni birlashtirib bosish - 10 soniya",
        ],
        "foyda": "Qo'l va yelka mashqlari kuchni oshiradi va holatni yaxshilaydi. "
        "Kundalik ko'tarish ishlarini yengillashtiradi.",
        "ehtiyot": "Yelka yoki tirsakda og'riq sezilsa, mashqni to'xtating va zarur bo'lganda shifokorga murojaat qiling.",
    },
    {
        "nom": "Orqa va turish qaddi",
        "daraja": "Oson",
        "davomiylik": "10 daqiqa",
        "mashqlar": [
            "Yotib orqani ko'tarish - 10 marta",
            "To'rt oyoqlab egilish - 8 marta",
            "Qo'llarni yuqoriga cho'zish - 10 marta",
            "Yelkani orqaga tortish - 10 marta",
            "Cho'zilish holatida turish - 10 soniya",
            "Bo'yinni muloyim cho'zish - 6 marta",
        ],
        "foyda": "Bu mashqlar orqa mushaklarini mustahkamlab, tik turishga yordam beradi. "
        "Uzoq o'tirishdan keyingi taranglikni kamaytiradi.",
        "ehtiyot": "Orqada kuchli og'riq yoki uvishish paydo bo'lsa, mashqni to'xtatib, shifokorga murojaat qiling.",
    },
    {
        "nom": "Kardio (joyida)",
        "daraja": "O'rta",
        "davomiylik": "15 daqiqa",
        "mashqlar": [
            "Joyida yurish - 3 daqiqa",
            "Yengil yugurish - 3 daqiqa",
            "Joyida sakrash - 30 marta",
            "Tizza ko'tarib yurish - 20 marta",
            "Yon qadamlar - 20 marta",
            "Nafas tiklash uchun sekin yurish - 2 daqiqa",
        ],
        "foyda": "Kardio mashqlari yurak va nafas tizimini chiniqtiradi. "
        "Kayfiyatni ko'tarishga ham yordam beradi.",
        "ehtiyot": "Nafas qisishi, bosh aylanishi yoki ko'krakda noqulaylik sezilsa, darhol to'xtang va kerak bo'lsa shifokorga murojaat qiling.",
    },
    {
        "nom": "Cho'zilish (stretching)",
        "daraja": "Oson",
        "davomiylik": "10 daqiqa",
        "mashqlar": [
            "Qo'llarni yuqoriga cho'zish - 20 soniya",
            "Yon tomonga egilish - har tomonga 20 soniya",
            "Oyoqni cho'zib gavdani egish - 20 soniya",
            "Tizza bukib cho'zilish - 20 soniya",
            "Yelkani aylantirish - 10 marta",
            "Bo'yinni muloyim egish - 15 soniya",
        ],
        "foyda": "Cho'zilish mushaklarni bo'shashtiradi va harakatchanlikni yaxshilaydi. "
        "Har qanday mashqdan keyin bajarish foydali.",
        "ehtiyot": "Cho'zilish paytida keskin og'riq sezilsa, harakatni to'xtating va zarur bo'lsa shifokorga murojaat qiling.",
    },
    {
        "nom": "Nafas mashqlari",
        "daraja": "Oson",
        "davomiylik": "8 daqiqa",
        "mashqlar": [
            "Chuqur nafas olish - 10 marta",
            "Burun orqali nafas - 10 marta",
            "Qorin bilan nafas olish - 10 marta",
            "Sekin chiqarish - 10 marta",
            "Tanaffus bilan nafas - 8 marta",
            "Tinch holatda dam olish - 2 daqiqa",
        ],
        "foyda": "Nafas mashqlari xotirjamlik beradi va stressni kamaytiradi. "
        "Istalgan paytda, hatto ish stolida ham bajarish mumkin.",
        "ehtiyot": "Nafas olishda noqulaylik yoki bosh aylanishi sezilsa, to'xtang va kerak bo'lsa shifokorga murojaat qiling.",
    },
    {
        "nom": "Yengil pilates uslubi",
        "daraja": "O'rta",
        "davomiylik": "15 daqiqa",
        "mashqlar": [
            "Yotib tinchlanish - 1 daqiqa",
            "Gavdani ko'tarish - 10 marta",
            "Oyoqlarni almashtirib ko'tarish - 12 marta",
            "Qo'llarni cho'zib ushlash - 20 soniya",
            "Plank holati - 20 soniya",
            "Yon tomonga burilish - 10 marta",
        ],
        "foyda": "Yengil pilates gavdani nazorat qilishni o'rgatadi. "
        "Mushaklarni kuchaytirib, harakatni yumshoq qiladi.",
        "ehtiyot": "Mashq paytida og'riq yoki bosh aylanishi sezilsa, darhol to'xtang va zarur bo'lsa shifokorga murojaat qiling.",
    },
    {
        "nom": "Bola bilan birga mashq",
        "daraja": "Oson",
        "davomiylik": "12 daqiqa",
        "mashqlar": [
            "Joyida birga yurish - 2 daqiqa",
            "Qo'llarni yuqoriga ko'tarish - 10 marta",
            "Koptok uzatish - 15 marta",
            "Birga cho'zilish - 10 marta",
            "Joyida yengil harakat - 20 marta",
            "Sekin yurib nafas tiklash - 2 daqiqa",
        ],
        "foyda": "Bolalar bilan birga mashq qilish harakatni o'yin ko'rinishida o'tkazadi. "
        "Bu oilada sog'lom odatni shakllantirishga yordam beradi.",
        "ehtiyot": "Mashq paytida og'riq, bosh aylanishi yoki nafas qisishi sezilsa, to'xtang va kerak bo'lsa shifokorga murojaat qiling.",
    },
]

KUNLIK_MASLAHATLAR = [
    "Ertalab bir stakan suv ichish tanani uyg'otadi va kunni tetik boshlashga yordam beradi.",
    "Har kuni kamida 30 daqiqa piyoda yurish yurak uchun foydali odatdir.",
    "Nonushtani tashlab ketmang, chunki u kunga energiya beradi.",
    "Ovqatni sekin chaynab yeyish hazmni osonlashtiradi va to'yish hissini beradi.",
    "Kuniga 7-8 soat uxlash tanani tiklaydi va kayfiyatni yaxshilaydi.",
    "Yotishdan bir soat oldin telefon va kompyuterni qo'yib, ko'zni dam oldiring.",
    "Toza havoda qisqa sayr qilish stressni kamaytiradi.",
    "Sabzavot va mevani har kuni iste'mol qilish tanani quvvatlaydi.",
    "Shirin gazlangan ichimlik o'rniga oddiy suv yoki kompot ichish yaxshi.",
    "Ovqatga tuz qo'shishni kamaytirsangiz, yurak uchun foydali bo'ladi.",
    "Kunduzi bir necha daqiqa ko'zni yumib dam olish ko'zni tetik qiladi.",
    "Zinapoyadan ko'tarilish liftdan yaxshiroq, chunki bu tabiiy mashqdir.",
    "Har soatda o'rningizdan turib, bir necha qadam yurib oling.",
    "Uy ishlarini bajarish ham jismoniy harakat hisoblanadi.",
    "Tishlarni kuniga ikki marta tozalashni odat qiling.",
    "Ovqatdan oldin qo'l yuvish oddiy va kuchli himoyadir.",
    "Xonani kuniga ikki marta shamollatib, havoni yangilang.",
    "Yangi kun uchun qisqa reja tuzish tartibsizlikni kamaytiradi.",
    "Kechki ovqatni yotishdan 2-3 soat oldin yeyishni odat qiling.",
    "Har kuni rahmat aytish va iliq so'z kayfiyatni ko'taradi.",
    "Kulish va xursand bo'lish stressga qarshi eng yaxshi vositadir.",
    "Yengil cho'zilish mashqlari tanani sergak qiladi.",
    "Chekishni tashlash sog'liq uchun eng muhim qadamlardan biridir.",
    "Spirtli ichimliklardan voz kechish tanani asraydi.",
    "Har kuni bir necha daqiqa quyosh nurida bo'lish organizmga foydali.",
    "Qo'llarni sovun bilan yuvish salomatlikni asrashning oson usulidir.",
    "Ovqatni yopiq idishda saqlash uning sifatini yaxshilaydi.",
    "Buzilgan yoki hidi o'zgargan ovqatni iste'mol qilishdan saqlaning.",
    "Toza suv ichish hazm tizimi uchun foydalidir.",
    "Kunlik suv miqdorini eslatuvchi idish yonida saqlang.",
    "Har kuni bir oz harakat qilish uzoq umr sari qo'yilgan qadamdir.",
    "Ko'p o'tirish bel uchun zararli, shuning uchun tez-tez qimirlang.",
    "Mashqdan oldin qizish harakatlarini bajarishni unutmang.",
    "Mashqdan keyin cho'zilish mushaklarni bo'shashtiradi.",
    "Yengil musiqa bilan mashq qilish kayfiyatni oshiradi.",
    "Do'stlar bilan birga yurish mashqni qiziqarli qiladi.",
    "Uyqudan oldin iliq dush olish tinchlantiradi.",
    "Kunduzi xona yorug'ligi yetarli bo'lsa, ishlash osonlashadi.",
    "Ovqatni kichik luqmalar bilan va shoshilmasdan yeyish tavsiya etiladi.",
    "Har hafta bir yangi sabzavotni sinab ko'ring.",
    "Kechqurun shirinlikdan voz kechish uyquni yaxshilaydi.",
    "Nonushtaga tuxum, sut yoki bo'tqa kabi to'ydiruvchi taom tanlang.",
    "Yong'oq va meva kabi sog'lom gazaklarni uyda saqlang.",
    "Kun davomida qisqa jismoniy tanaffus qilishni unutmang.",
    "Poyabzalni almashtirib kiyish oyoq uchun foydalidir.",
    "Toza paypoq va kiyim tanani tetik tutadi.",
    "Iliq yashil choy ichish yoqimli va foydali odatdir.",
    "Shovqinli joydan uzoqda bir necha daqiqa dam oling.",
    "Har hafta mashq rejasini tuzib, unga rioya qiling.",
    "Tabiatda sayr qilish kayfiyatni yaxshilaydi.",
    "Guruhda mashq qilish sizni harakatga undaydi.",
    "Har kuni bitta kichik maqsad qo'yish o'zgarishga yordam beradi.",
    "Nafas mashqlari xotirjamlik beradi va diqqatni jamlaydi.",
    "Yetarli dam olish ish unumdorligini oshiradi.",
    "Har kuni kulgi va xushfe'llikni saqlash foydali.",
    "Uyda tozalikni saqlash sog'lom muhit yaratadi.",
    "Yoningizda chiroyli idishda suv olib yurish ichishga undaydi.",
    "Har oyda o'z sog'liq odatlaringizni ko'rib chiqing.",
    "Yangi odatni asta-sekin joriy qilish osonroq kechadi.",
    "Sog'lom hayot har kuni qilingan kichik qadamlardan iborat.",
]
