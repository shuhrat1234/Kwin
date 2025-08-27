const TranslationManager = {
    currentLang: 'uz', // Default to Uzbek
    langMap: {
        'en': 'EN',
        'uz': 'UZ',
        'ru': 'RU',
        'ger': 'DE'
    },

    init: function () {
        this.currentLang = this.getCurrentLanguage();
        this.updateLanguageDisplay();
        this.bindEvents();
        this.applyClientTranslations(this.currentLang);
    },

    getCurrentLanguage: function () {
        return localStorage.getItem('selectedLanguage') || 'uz';
    },

    setLanguage: function (lang) {
        if (!this.isLanguageSupported(lang)) {
            console.warn('Unsupported language:', lang);
            return;
        }
        this.currentLang = lang;
        localStorage.setItem('selectedLanguage', lang);
        this.updateLanguageDisplay();
        this.changeLanguage(lang);
    },

    updateLanguageDisplay: function () {
        const currentLangElement = document.getElementById('current-language');
        if (currentLangElement) {
            currentLangElement.textContent = this.langMap[this.currentLang];
        }
    },

    bindEvents: function () {
        const self = this;
        document.querySelectorAll('a[data-lang]').forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                const lang = this.getAttribute('data-lang');
                self.setLanguage(lang);
            });
        });
        window.setLanguage = lang => self.setLanguage(lang);
    },

    changeLanguage: function (lang) {
        this.applyClientTranslations(lang);
        const csrfToken = this.getCSRFToken();
        if (!csrfToken) {
            console.warn('CSRF token missing');
            return;
        }

        const url = this.buildLanguageUrl(lang);
        $.ajax({
            url: url,
            type: "POST",
            data: { language: lang, csrfmiddlewaretoken: csrfToken },
            success: () => {
                setTimeout(() => window.location.reload(), 100);
            },
            error: xhr => {
                console.error('Language change failed:', xhr.responseText);
            }
        });
    },

    applyClientTranslations: function (lang) {
        this.currentLang = lang;
        window.applyTranslations();
    },

    getCSRFToken: function () {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
            document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    },

    buildLanguageUrl: function (lang) {
        return window.languageChangeUrl ? `${window.languageChangeUrl}${lang}/` : `/set-language/${lang}/`;
    },

    getAvailableLanguages: function () {
        return Object.keys(this.langMap);
    },

    isLanguageSupported: function (lang) {
        return this.langMap.hasOwnProperty(lang);
    }
};

const Translations = {
    en: {
        // Existing translations
        password: 'Password',
        site_title: 'KWIN Commerce',
        home: 'Home',
        products: 'Products',
        contact: 'Contact',
        home_slogan_highlight: 'Your Reliable Partner',
        home_slogan: 'in the world of auto products. High-quality auto components from leading manufacturers since 2005.',
        shop_now: 'Shop Now',
        learn_more: 'Learn More',
        about: 'About',
        about_us: 'Us',
        about_description: 'Your reliable partner in the world of auto products. High-quality auto components from leading manufacturers since 2005.',
        about_content: 'Since 2005, KWIN Commerce has been successfully developing the Uzbekistan auto components market, offering our clients only proven products from leading global manufacturers. Over the years, we have established ourselves as a reliable supplier and partner, earning the trust of thousands of clients and numerous companies across various regions of the country. KWIN Commerce is the official distributor of brands such as Heyner (Germany), Alca (Germany), Utal (Poland), ARS (Russia), and Delta (Russia). We take pride in representing products, that combine innovation, durability, and high quality, meeting international standards.',
        our: 'Our',
        categories: 'Categories',
        contact_title: 'Get in Touch',
        contact_description: 'Our mission is to provide you with quality auto products that make vehicle use safer and more comfortable. Contact us to learn more or get assistance!',
        email: 'Email',
        phone: 'Phone',
        name: 'Name',
        name_placeholder: 'Your Name',
        phone_validation_message: 'Please enter a valid phone number (+998 (XX) XXX-XX-XX)',
        message: 'Message',
        message_placeholder: 'Your Message',
        send_message: 'Send Message',
        contact_success: 'Message sent successfully!',
        contact_error: 'Failed to send message',
        login: 'Login',
        register: 'Register',
        lang_en: 'English',
        lang_uz: 'Uzbek',
        lang_ru: 'Russian',
        lang_ger: 'German',
        footer_title: 'KWIN Commerce',
        footer_slogan: 'Your reliable partner in the world of auto products.',
        footer_copyright: 'KWIN. All rights reserved.',
        // Product template translations
        auto_parts: 'Auto Parts',
        products_found: 'Products found:',
        filters: 'Filters',
        brands: 'Brands',
        select_brand: 'Select brand',
        models: 'Models',
        select_model: 'Select model',
        years: 'Years',
        select_year: 'Select year',
        series: 'Series',
        select_series: 'Select series',
        filter: 'Filter',
        reset_filters: 'Reset filters',
        remove_from_cart: 'Remove from cart',
        add_to_cart: 'Add to cart',
        buy_now: 'Buy now',
        no_products_found: 'No products found',
        try_changing_filters: 'Try changing search parameters or filters',
        order_checkout: 'Checkout',
        full_name: 'Full name *',
        phone_number: 'Phone number *',
        phone_placeholder: '+998 (XX) XXX-XX-XX',
        additional_info: 'Additional information',
        additional_info_placeholder: 'Delivery address, order notes...',
        cancel: 'Cancel',
        confirm_order: 'Confirm order',
        sending: 'Sending...',
        order_success: 'Order successfully placed!',
        order_error: 'An error occurred while placing the order',
        order_submit_error: 'An error occurred while submitting the order'
    },
    uz: {
        // Existing translations
        password: 'Parol',
        site_title: 'KWIN Tijorat',
        home: 'Bosh sahifa',
        products: 'Mahsulotlar',
        contact: 'Aloqa',
        home_slogan_highlight: 'Ishonchli Hamkoringiz',
        home_slogan: 'avto mahsulotlar dunyosida. 2005 yildan beri yetakchi ishlab chiqaruvchilardan yuqori sifatli avto komponentlar.',
        shop_now: 'Hozir xarid qilish',
        learn_more: 'Ko‘proq bilib oling',
        about: 'Biz haqimizda',
        about_us: 'Biz',
        about_description: 'Avto mahsulotlar dunyosidagi ishonchli hamkoringiz. 2005 yildan beri yetakchi ishlab chiqaruvchilardan yuqori sifatli avto komponentlar.',
        about_content: '2005 yildan boshlab, KWIN Tijorat O‘zbekiston avto komponentlar bozorini muvaffaqiyatli rivojlantirmoqda, mijozlarimizga faqat sinovdan o‘tgan, dunyoning yetakchi ishlab chiqaruvchilaridan mahsulotlar taklif qilmoqda. Yillar davomida biz ishonchli yetkazib beruvchi va hamkor sifatida o‘zimizni ko‘rsatdik, mamlakatning turli hududlaridagi minglab mijozlar va ko‘plab kompaniyalar ishonchini qozondik. KWIN Tijorat Heyner (Germaniya), Alca (Germaniya), Utal (Polsha), ARS (Rossiya) va Delta (Rossiya) brendlarining rasmiy distribyutori hisoblanadi. Biz innovatsiya, chidamlilik va xalqaro standartlarga mos keluvchi yuqori sifatni birlashtirgan mahsulotlarni taqdim etishdan faxrlanamiz.',
        our: 'Bizning',
        categories: 'Kategoriyalar',
        contact_title: 'Qayta aloqa uchun',
        contact_description: 'Bizning vazifamiz — avtomobillarni xavfsizroq va qulayroq qiladigan sifatli avto mahsulotlar bilan ta’minlash. Ko‘proq ma’lumot olish yoki yordam olish uchun biz bilan bog‘laning!',
        email: 'Email',
        phone: 'Telefon',
        name: 'Ism',
        name_placeholder: 'Sizning ismingiz',
        phone_validation_message: 'Iltimos, to‘g‘ri telefon raqamini kiriting (+998 (XX) XXX-XX-XX)',
        message: 'Xabar',
        message_placeholder: 'Sizning xabaringiz',
        send_message: 'Xabar yuborish',
        contact_success: 'Xabar muvaffaqiyatli yuborildi!',
        contact_error: 'Xabarni yuborib bo‘lmadi',
        login: 'Kirish',
        register: "Ro'yxatdan o'tish",
        lang_en: 'Inglizcha',
        lang_uz: 'O‘zbekcha',
        lang_ru: 'Ruscha',
        lang_ger: 'Nemisch',
        footer_title: 'KWIN Tijorat',
        footer_slogan: 'Avto mahsulotlar dunyosidagi ishonchli hamkoringiz.',
        footer_copyright: 'KWIN. Barcha huquqlar himoyalangan.',
        // Product template translations
        auto_parts: 'Avto ehtiyot qismlari',
        products_found: 'Topilgan mahsulotlar:',
        filters: 'Filtrlar',
        brands: 'Brendlar',
        select_brand: 'Brendni tanlang',
        models: 'Modellar',
        select_model: 'Modelni tanlang',
        years: 'Yillar',
        select_year: 'Yilni tanlang',
        series: 'Seriyalar',
        select_series: 'Seriyani tanlang',
        filter: 'Filtrlash',
        reset_filters: 'Filtrlarni tiklash',
        remove_from_cart: 'Savatdan olib tashlash',
        add_to_cart: "Savatga qo'shish",
        buy_now: 'Hozir sotib olish',
        no_products_found: 'Mahsulotlar topilmadi',
        try_changing_filters: "Qidiruv parametrlari yoki filtrlarni o'zgartirib ko'ring",
        order_checkout: 'Buyurtma rasmiylashtirish',
        full_name: "To'liq ism *",
        phone_number: 'Telefon raqami *',
        phone_placeholder: '+998 (XX) XXX-XX-XX',
        additional_info: "Qo'shimcha ma'lumot",
        additional_info_placeholder: "Yetkazib berish manzili, buyurtma eslatmalari...",
        cancel: 'Bekor qilish',
        confirm_order: 'Buyurtmani tasdiqlash',
        sending: 'Yuborilmoqda...',
        order_success: 'Buyurtma muvaffaqiyatli joylashtirildi!',
        order_error: 'Buyurtma berishda xatolik yuz berdi',
        order_submit_error: 'Buyurtmani yuborishda xatolik yuz berdi'
    },
    ru: {
        // Existing translations
        password: 'Пароль',
        site_title: 'KWIN Коммерция',
        home: 'Главная',
        products: 'Продукты',
        contact: 'Контакты',
        home_slogan_highlight: 'Ваш Надежный Партнер',
        home_slogan: 'в мире авто товаров. Качественные автокомплектующие от ведущих производителей с 2005 года.',
        shop_now: 'Купить сейчас',
        learn_more: 'Узнать больше',
        about: 'О нас',
        about_us: 'Нас',
        about_description: 'Ваш надежный партнер в мире авто товаров. Качественные автокомплектующие от ведущих производителей с 2005 года.',
        about_content: 'С 2005 года компания KWIN Коммерция успешно развивает рынок автокомплектующих Узбекистана, предлагая своим клиентам только проверенную продукцию ведущих мировых производителей. За годы работы мы зарекомендовали себя как надежный поставщик и партнер, заслужив доверие тысяч клиентов и множества компаний в разных регионах страны. KWIN Коммерция — официальный дистрибьютор брендов Heyner (Германия), Alca (Германия), Utal (Польша), ARS (Россия) и Delta (Россия). Мы гордимся тем, что представляем продукцию, которая сочетает в себе инновации, долговечность и высокое качество, соответствующее международным стандартам.',
        our: 'Наши',
        categories: 'Категории',
        contact_title: 'Связаться с нами',
        contact_description: 'Наша миссия — обеспечить вас качественными автотоварами, которые делают использование автомобилей безопаснее и комфортнее. Свяжитесь с нами, чтобы узнать больше или получить помощь!',
        email: 'Электронная почта',
        phone: 'Телефон',
        name: 'Имя',
        name_placeholder: 'Ваше имя',
        phone_validation_message: 'Пожалуйста, введите действительный номер телефона (+998 (XX) XXX-XX-XX)',
        message: 'Сообщение',
        message_placeholder: 'Ваше сообщение',
        send_message: 'Отправить сообщение',
        contact_success: 'Сообщение успешно отправлено!',
        contact_error: 'Не удалось отправить сообщение',
        login: 'Войти',
        register: 'Регистрация',
        lang_en: 'Английский',
        lang_uz: 'Узбекский',
        lang_ru: 'Русский',
        lang_ger: 'Немецкий',
        footer_title: 'KWIN Коммерция',
        footer_slogan: 'Ваш надежный партнер в мире авто товаров.',
        footer_copyright: 'KWIN. Все права защищены.',
        // Product template translations
        auto_parts: 'Автокомплектующие',
        products_found: 'Найдено товаров:',
        filters: 'Фильтры',
        brands: 'Бренды',
        select_brand: 'Выберите бренд',
        models: 'Модели',
        select_model: 'Выберите модель',
        years: 'Годы',
        select_year: 'Выберите год',
        series: 'Серии',
        select_series: 'Выберите серию',
        filter: 'Отфильтровать',
        reset_filters: 'Сбросить фильтры',
        remove_from_cart: 'Удалить из корзины',
        add_to_cart: 'Добавить в корзину',
        buy_now: 'Купить сейчас',
        no_products_found: 'Товары не найдены',
        try_changing_filters: 'Попробуйте изменить параметры поиска или фильтры',
        order_checkout: 'Оформление заказа',
        full_name: 'Полное имя *',
        phone_number: 'Номер телефона *',
        phone_placeholder: '+998 (XX) XXX-XX-XX',
        additional_info: 'Дополнительная информация',
        additional_info_placeholder: 'Адрес доставки, пожелания к заказу...',
        cancel: 'Отмена',
        confirm_order: 'Подтвердить заказ',
        sending: 'Отправка...',
        order_success: 'Заказ успешно оформлен!',
        order_error: 'Произошла ошибка при оформлении заказа',
        order_submit_error: 'Произошла ошибка при отправке заказа'
    },
    ger: {
        // Existing translations
        password: 'Passwort',
        site_title: 'KWIN Handel',
        home: 'Startseite',
        products: 'Produkte',
        contact: 'Kontakt',
        home_slogan_highlight: 'Ihr Zuverlässiger Partner',
        home_slogan: 'in der Welt der Autoprodukte. Hochwertige Autokomponenten von führenden Herstellern seit 2005.',
        shop_now: 'Jetzt einkaufen',
        learn_more: 'Mehr erfahren',
        about: 'Über uns',
        about_us: 'Uns',
        about_description: 'Ihr zuverlässiger Partner in der Welt der Autoprodukte. Hochwertige Autokomponenten von führenden Herstellern seit 2005.',
        about_content: 'Seit 2005 entwickelt KWIN Handel erfolgreich den usbekischen Markt für Autokomponenten und bietet unseren Kunden nur bewährte Produkte von führenden globalen Herstellern an. Im Laufe der Jahre haben wir uns als zuverlässiger Lieferant und Partner etabliert und das Vertrauen von Tausenden von Kunden und zahlreichen Unternehmen in verschiedenen Regionen des Landes gewonnen. KWIN Handel ist der offizielle Distributor von Marken wie Heyner (Deutschland), Alca (Deutschland), Utal (Polen), ARS (Russland) und Delta (Russland). Wir sind stolz darauf, Produkte zu vertreten, die Innovation, Langlebigkeit und hohe Qualität vereinen und internationalen Standards entsprechen.',
        our: 'Unsere',
        categories: 'Kategorien',
        contact_title: 'Kontaktieren Sie uns',
        contact_description: 'Unsere Mission ist es, Ihnen qualitativ hochwertige Autoprodukte zu liefern, die die Nutzung von Fahrzeugen sicherer und komfortabler machen. Kontaktieren Sie uns, um mehr zu erfahren oder Unterstützung zu erhalten!',
        email: 'E-Mail',
        phone: 'Telefon',
        name: 'Name',
        name_placeholder: 'Ihr Name',
        phone_validation_message: 'Bitte geben Sie eine gültige Telefonnummer ein (+998 (XX) XXX-XX-XX)',
        message: 'Nachricht',
        message_placeholder: 'Ihre Nachricht',
        send_message: 'Nachricht senden',
        contact_success: 'Nachricht erfolgreich gesendet!',
        contact_error: 'Nachricht konnte nicht gesendet werden',
        login: 'Anmelden',
        register: 'Registrieren',
        lang_en: 'Englisch',
        lang_uz: 'Usbekisch',
        lang_ru: 'Russisch',
        lang_ger: 'Deutsch',
        footer_title: 'KWIN Handel',
        footer_slogan: 'Ihr zuverlässiger Partner in der Welt der Autoprodukte.',
        footer_copyright: 'KWIN. Alle Rechte vorbehalten.',
        // Product template translations
        auto_parts: 'Autoteile',
        products_found: 'Gefundene Produkte:',
        filters: 'Filter',
        brands: 'Marken',
        select_brand: 'Marke auswählen',
        models: 'Modelle',
        select_model: 'Modell auswählen',
        years: 'Jahre',
        select_year: 'Jahr auswählen',
        series: 'Serien',
        select_series: 'Serie auswählen',
        filter: 'Filtern',
        reset_filters: 'Filter zurücksetzen',
        remove_from_cart: 'Aus dem Warenkorb entfernen',
        add_to_cart: 'In den Warenkorb',
        buy_now: 'Jetzt kaufen',
        no_products_found: 'Keine Produkte gefunden',
        try_changing_filters: 'Versuchen Sie, die Suchparameter oder Filter zu ändern',
        order_checkout: 'Bestellung abschließen',
        full_name: 'Vollständiger Name *',
        phone_number: 'Telefonnummer *',
        phone_placeholder: '+998 (XX) XXX-XX-XX',
        additional_info: 'Zusätzliche Informationen',
        additional_info_placeholder: 'Lieferadresse, Anmerkungen zur Bestellung...',
        cancel: 'Abbrechen',
        confirm_order: 'Bestellung bestätigen',
        sending: 'Senden...',
        order_success: 'Bestellung erfolgreich aufgegeben!',
        order_error: 'Fehler beim Aufgeben der Bestellung',
        order_submit_error: 'Fehler beim Senden der Bestellung'
    }
};

function translateText(key, lang = null) {
    const currentLang = lang || TranslationManager.currentLang;
    return Translations[currentLang]?.[key] || Translations['en']?.[key] || key;
}

function applyTranslations() {
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        const translatedText = translateText(key);

        if (element.tagName.toLowerCase() === 'input') {
            if (['text', 'tel', 'password'].includes(element.type)) {
                element.placeholder = translatedText;
            } else if (['submit', 'button'].includes(element.type)) {
                element.value = translatedText;
            }
        } else if (element.tagName.toLowerCase() === 'button' && !element.type) {
            element.textContent = translatedText;
        } else {
            element.textContent = translatedText;
        }
    });
    document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
        const key = element.getAttribute('data-translate-placeholder');
        const translatedText = translateText(key);
        element.setAttribute('placeholder', translatedText);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    TranslationManager.init();
    setTimeout(applyTranslations, 100);
});

$(document).ready(() => {
    if (!window.TranslationManager.currentLang) {
        TranslationManager.init();
    }
    setTimeout(applyTranslations, 200);
});

window.TranslationManager = TranslationManager;
window.translateText = translateText;
window.applyTranslations = applyTranslations;

window.debugTranslations = () => {
    console.log('=== Translation Debug Info ===');
    console.log('Current language:', TranslationManager.currentLang);
    console.log('Available languages:', TranslationManager.getAvailableLanguages());
    console.log('Elements with data-translate:', document.querySelectorAll('[data-translate]').length);
    console.log('CSRF token available:', !!TranslationManager.getCSRFToken());
};