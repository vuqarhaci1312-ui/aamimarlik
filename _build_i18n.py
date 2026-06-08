#!/usr/bin/env python3
"""Build translations.js and patch HTML files for AA MEMARLIQ i18n (az/tr)."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRANSLATIONS_JS = ROOT / "assets" / "js" / "translations.js"

PAGE_MAP = {
    "index.html": "index",
    "about.html": "about",
    "service-11.html": "services",
    "service-details-interyer.html": "svc_interyer",
    "service-details-memarliq.html": "svc_memarliq",
    "service-details-sergi.html": "svc_sergi",
    "service-details-idareetme.html": "svc_pm",
    "faq.html": "faq",
    "contact.html": "contact",
    "portfolio-details-showroom.html": "port_showroom",
    "portfolio-details-ferdiyasayis.html": "port_home",
    "portfolio-details-ofis.html": "port_ofis",
    "portfolio-details-sergistendleri.html": "port_sergi",
}

LANG_SWITCHER = (
    '<div class="lang-switcher" role="group" aria-label="Dil">\n'
    '  <button type="button" class="lang-switcher__btn is-active" data-lang="az">AZ</button>\n'
    '  <button type="button" class="lang-switcher__btn" data-lang="tr">TR</button>\n'
    '</div>'
)

I18N_SCRIPTS = (
    '  <script src="assets/js/translations.js"></script>\n'
    '  <script src="assets/js/i18n.js"></script>\n'
)


def _build_translations():
    rows = [
        # --- Page titles & meta ---
        ("index.title", "Ana Səhifə", "Ana Sayfa"),
        ("index.meta_description", "Ekspo Stend və Memarlıq Şirkəti", "Expo Stand ve Mimarlık Şirketi"),
        ("about.title", "Haqqımızda", "Hakkımızda"),
        ("about.meta_description", "Sərgi Stendləri, İnteryer və Eksteryer Dizayn", "Fuar Standları, İç Mekân ve Dış Mekân Tasarımı"),
        ("contact.title", "Əlaqə", "İletişim"),
        ("contact.meta_description", "Memarlıq və İnteryer Dizayn", "Mimarlık ve İç Mekân Tasarımı"),
        ("faq.title", "FAQ", "SSS"),
        ("faq.meta_description", "Memarlıq və İnteryer Dizayn", "Mimarlık ve İç Mekân Tasarımı"),
        ("services.title", "Xidmətlərimiz", "Hizmetlerimiz"),
        ("services.meta_description", "Xidmətlərimiz: İnteryer, Memarlıq, Sərgi Stendləri və Layihə İdarəetməsi", "Hizmetlerimiz: İç Mekân, Mimarlık, Fuar Standları ve Proje Yönetimi"),
        ("svc_interyer.title", "İnteryer və Eksteryer", "İç Mekân ve Dış Mekân"),
        ("svc_interyer.meta_description", "İnteryer və Eksteryer xidməti", "İç Mekân ve Dış Mekân hizmeti"),
        ("svc_memarliq.title", "Memarlıq Layihələri", "Mimarlık Projeleri"),
        ("svc_memarliq.meta_description", "Memarlıq Layihələri xidməti", "Mimarlık Projeleri hizmeti"),
        ("svc_sergi.title", "Sərgi Stendləri", "Fuar Standları"),
        ("svc_sergi.meta_description", "Sərgi Stendləri xidməti", "Fuar Standları hizmeti"),
        ("svc_pm.title", "Layihə İdarəetməsi", "Proje Yönetimi"),
        ("svc_pm.meta_description", "Layihə İdarəetməsi xidməti", "Proje Yönetimi hizmeti"),
        ("port_showroom.title", "Premium Showroom", "Premium Showroom"),
        ("port_showroom.meta_description", "Premium Showroom Interyeri layihəsi", "Premium Showroom İç Mekân projesi"),
        ("port_home.title", "Fərdi Yaşayış Evi", "Özel Konut"),
        ("port_home.meta_description", "Fərdi Yaşayış Evi Interyeri layihəsi", "Özel Konut İç Mekân projesi"),
        ("port_ofis.title", "Müasir Ofis", "Modern Ofis"),
        ("port_ofis.meta_description", "Müasir Ofis Interyeri layihəsi", "Modern Ofis İç Mekân projesi"),
        ("port_sergi.title", "Sərgi Stendi Layihəsi", "Fuar Standı Projesi"),
        ("port_sergi.meta_description", "Sərgi Stendləri layihəsi", "Fuar Standları projesi"),
        # --- Shared nav / footer / sidebar ---
        ("shared.lang_label", "Dil", "Dil"),
        ("nav.home", "Ana Səhifə", "Ana Sayfa"),
        ("nav.about", "Haqqımızda", "Hakkımızda"),
        ("nav.services", "Xidmətlərimiz", "Hizmetlerimiz"),
        ("nav.services_short", "Xidmətlər", "Hizmetler"),
        ("nav.projects", "Layihələr", "Projeler"),
        ("nav.faq", "FAQ", "SSS"),
        ("nav.contact", "Əlaqə", "İletişim"),
        ("nav.svc_interyer", "İnteryer və Eksteryer", "İç Mekân ve Dış Mekân"),
        ("nav.svc_memarliq", "Memarlıq Layihələri", "Mimarlık Projeleri"),
        ("nav.svc_sergi", "Sərgi Stendləri", "Fuar Standları"),
        ("nav.svc_pm", "Layihə İdarəetməsi", "Proje Yönetimi"),
        ("btn.contact", "Əlaqə", "İletişim"),
        ("btn.contact_talk", "Bizimlə Danışın", "Bizimle Görüşün"),
        ("btn.contact_us", "Bizimlə Əlaqə Saxlayın", "Bizimle İletişime Geçin"),
        ("btn.send_now", "İndi göndər", "Şimdi Gönderin"),
        ("btn.more", "Ətraflı", "Detaylı"),
        ("btn.all_projects", "Bütün Layihələr", "Tüm Projeler"),
        ("btn.explore_services", "Xidmətləri araşdırın", "Hizmetleri Keşfedin"),
        ("btn.close", "Bağla", "Kapat"),
        ("sidebar.tagline", "Baku Expo Center ilə rəsmi müqaviləli olaraq fəaliyyət göstərən peşəkar ekspo stend və memarlıq şirkəti.", "Baku Expo Center ile resmi sözleşmeli olarak faaliyet gösteren profesyonel expo stand ve mimarlık şirketi."),
        ("sidebar.founded", "Yaranma: 2019", "Kuruluş: 2019"),
        ("sidebar.social", "Sosial Media", "Sosyal Medya"),
        ("sidebar.menu", "Menyu", "Menü"),
        ("sidebar.write_us", "Bizə yazın", "Bize Yazın"),
        ("sidebar.contact_title", "Bizimlə Əlaqə", "Bizimle İletişim"),
        ("footer.subscribe", "Abunə olun", "Abone Olun"),
        ("footer.subscribe_banner", "YENİLİKLƏRƏ ABUNƏ OLUN", "YENİLİKLERİ TAKİP EDİN"),
        ("footer.work_together", "Gəlin birlikdə işləyək", "Birlikte Çalışalım"),
        ("footer.quick_links", "Sürətli Keçidlər", "Hızlı Bağlantılar"),
        ("footer.social", "Sosial Şəbəkələr", "Sosyal Ağlar"),
        ("footer.office", "Ofis", "Ofis"),
        ("footer.terms", "İstifadə qaydaları", "Kullanım Koşulları"),
        ("footer.copyright", "© 2026. Bütün hüquqlar qorunur.", "© 2026. Tüm hakları saklıdır."),
        ("footer.copyright_short", "© AA MEMARLIQ.", "© AA MEMARLIQ."),
        ("footer.location_html", "Baku Expo Center,<br>Bakı, Azərbaycan", "Baku Expo Center,<br>Bakı, Azerbaycan"),
        ("footer.location_html2", "Baku Expo Center, <br>\n                                        Bakı, Azərbaycan", "Baku Expo Center, <br>\n                                        Bakı, Azerbaycan"),
        ("footer.location_line", "Baku Expo Center", "Baku Expo Center"),
        ("ph.name", "Ad", "Ad"),
        ("ph.name_req", "Ad*", "Ad*"),
        ("ph.name_your", "Adınız*", "Adınız*"),
        ("ph.email", "E-poçt*", "E-posta*"),
        ("ph.email_addr", "E-poçt ünvanınız", "E-posta adresiniz"),
        ("ph.email_addr2", "E-poçt ünvaniniz", "E-posta adresiniz"),
        ("ph.phone", "Telefon*", "Telefon*"),
        ("ph.company", "Şirkət", "Şirket"),
        ("ph.budget", "Büdcə*", "Bütçe*"),
        ("ph.service", "Tələb olunan xidmət*", "Talep Edilen Hizmet*"),
        ("ph.message", "Mesajınız*", "Mesajınız*"),
        ("ph.message_opt", "Mesajınız", "Mesajınız"),
        ("ph.email_star", "E-poçt*", "E-posta*"),
        ("select.budget_1", "5,000 - 10,000 AZN", "5.000 - 10.000 AZN"),
        ("select.budget_2", "10,000 - 15,000 AZN", "10.000 - 15.000 AZN"),
        ("select.budget_3", "15,000 - 20,000 AZN", "15.000 - 20.000 AZN"),
        ("select.budget_4", "20,000 - 25,000 AZN", "20.000 - 25.000 AZN"),
        ("select.budget_5", "25,000 AZN-dən yuxarı", "25.000 AZN ve üzeri"),
        ("info.client", "Müştəri:", "Müşteri:"),
        ("info.type", "Tip:", "Tür:"),
        ("info.year", "İl:", "Yıl:"),
        ("info.area", "Sahə:", "Alan:"),
        ("info.location", "Yer:", "Konum:"),
        ("info.status", "Status:", "Durum:"),
        ("info.details", "Məlumat", "Bilgi"),
        ("info.overview", "Ümumi baxış", "Genel Bakış"),
        ("info.scope", "İş həcmi", "İş Kapsamı"),
        ("info.completed", "Tamamlandı", "Tamamlandı"),
        ("info.baku", "Bakı, Azərbaycan", "Bakı, Azerbaycan"),
        ("info.baku_full", "Baku Expo Center, Bakı, Azərbaycan", "Baku Expo Center, Bakı, Azerbaycan"),
        ("val.individual", "Fərdi sifariş", "Bireysel sipariş"),
        ("val.commercial", "Kommersiya sifarişi", "Ticari sipariş"),
        ("val.corporate", "Korporativ sifariş", "Kurumsal sipariş"),
        ("val.interior_exterior", "İnteryer və eksteryer", "İç mekân ve dış mekân"),
        ("val.arch_project", "Memarlıq layihəsi", "Mimarlık projesi"),
        ("val.exhibition", "Sərgi stendi", "Fuar standı"),
        ("val.pm", "Layihə idarəetməsi", "Proje yönetimi"),
        ("val.residential", "Yaşayış və kommersiya", "Konut ve ticari"),
        ("val.commercial_space", "Kommersiya məkanı", "Ticari mekân"),
        ("val.exhibition_area", "Sərgi stendi", "Fuar standı"),
        ("val.corporate_office", "Korporativ ofis", "Kurumsal ofis"),
        ("val.showroom_interior", "Showroom interyeri", "Showroom iç mekânı"),
        ("val.showroom_space", "Showroom məkanı", "Showroom mekânı"),
        ("val.home_interior", "Yasayis evi interyeri", "Konut iç mekânı"),
        ("val.home_space", "Fərdi yasayış evi", "Özel konut"),
        ("val.office_interior", "Ofis interyeri", "Ofis iç mekânı"),
        ("val.office_space", "Ofis məkanı", "Ofis mekânı"),
    ]
    rows.extend(_page_translation_rows())
    return {k: {"az": az, "tr": tr} for k, az, tr in rows}


def _page_translation_rows():
    return [
        # --- index.html ---
        ("index.hero.location", "Bakı, Azərbaycan.", "Bakı, Azerbaycan."),
        ("index.hero.desc", "Müştəri məmnuniyyətinə əsaslanaraq müasir sərgi stendləri, landşaftlar, eksteryer və interyerlər dizayn edirik.", "Müşteri memnuniyetini esas alarak modern fuar standları, peyzajlar, dış mekân ve iç mekânlar tasarlıyoruz."),
        ("index.hero.subtitle", "Məkanların Həyata İlham Verdiyi Yer", "Mekânların Hayata İlham Verdiği Yer"),
        ("index.hero.interior", "İnteryer", "İç Mekân"),
        ("index.hero.exterior_html", "Və <br> Eksteryer <br> Dizayn firması", "Ve <br> Dış Mekân <br> Tasarım firması"),
        ("index.about.subtitle", "ŞİRKƏTİMİZ", "ŞİRKETİMİZ"),
        ("index.about.title_html", "AA MEMARLIQ hər <br> layihəni <span>özünəməxsus sənət <br> əsərinə çevirir.</span>", "AA MEMARLIQ her <br> projeyi <span>eşsiz bir sanat <br> eserine dönüştürür.</span>"),
        ("index.about.desc", "AA MEMARLIQ Ekspo Stend Şirkəti 2019-cu ildən bəri Azərbaycanda fəaliyyət göstərir. Firmamız hər daim müştəri məmnuniyyətinə əsaslanaraq çalışır. Əhəmiyyətli sahələrimizdən biri də dekorasiya və dizayn işlərinin yerinə yetirilməsidir. Şirkətimiz Baku Expo Center ilə rəsmi müqaviləli olaraq xidmət göstərir və sərgi sektorunda 100-dən çox layihəyə öz imzasını atmışdır. Siz dəyərli müştərilərimizi ən yaxşı şəkildə tanıtmaq və bizə olan etibarınızı doğrultmaq üçün bütün komandamızla hər zaman xidmətinizdəyik.", "AA MEMARLIQ Expo Stand Şirketi 2019 yılından bu yana Azerbaycan'da faaliyet göstermektedir. Firmamız her zaman müşteri memnuniyetini esas alarak çalışmaktadır. Önemli alanlarımızdan biri de dekorasyon ve tasarım işlerinin gerçekleştirilmesidir. Şirketimiz Baku Expo Center ile resmi sözleşmeli olarak hizmet vermekte ve fuar sektöründe 100'den fazla projeye imzasını atmıştır. Siz değerli müşterilerimizi en iyi şekilde tanıtmak ve bize duyduğunuz güveni doğrulamak için tüm ekibimizle her zaman hizmetinizdeyiz."),
        ("index.about.item1_title", "Müştəri Məmnuniyyəti.", "Müşteri Memnuniyeti."),
        ("index.about.item1_desc", "Şirkətimiz hər daim müştəri məmnuniyyətinə əsaslanaraq çalışır və bizə olan güveninizi doğruldur.", "Şirketimiz her zaman müşteri memnuniyetini esas alarak çalışır ve bize duyduğunuz güveni doğrular."),
        ("index.about.item2_title", "Rəsmi Tərəfdaşlıq.", "Resmi Ortaklık."),
        ("index.about.item2_desc", "Baku Expo Center ilə rəsmi müqavilə əsasında sərgi stendlərinin qurulması xidmətini göstəririk.", "Baku Expo Center ile resmi sözleşme kapsamında fuar standlarının kurulumu hizmetini sunuyoruz."),
        ("index.about.item3_title", "100-dən Çox Layihə.", "100'den Fazla Proje."),
        ("index.about.item3_desc", "Sərgi stendləri və dekorasiya işləri sahəsində 100-dən çox layihəyə öz imzamızı atmışıq.", "Fuar standları ve dekorasyon işleri alanında 100'den fazla projeye imzamızı atmış bulunmaktayız."),
        ("index.svc1_link_html", "İnteryer.\n                        Dizayn.\n                        İncəsənət.", "İç Mekân.\n                        Tasarım.\n                        Sanat."),
        ("index.svc1_desc", "Məkanın funksionallığını və estetikasını artıraraq sizin üçün rahat daxili məkanlar dizayn edirik.", "Mekânın işlevselliğini ve estetiğini artırarak sizin için konforlu iç mekânlar tasarlıyoruz."),
        ("index.svc1_title_html", "İnteryer <span>Dizaynı</span>", "İç Mekân <span>Tasarımı</span>"),
        ("index.svc2_link_html", "Ekspo.\n                        Stend.\n                        Təqdimat.", "Expo.\n                        Stand.\n                        Sunum."),
        ("index.svc2_desc", "Baku Expo Center-də brendinizin ən gözəl şəkildə təqdim edilməsi üçün sərgi stendləri qururuq.", "Baku Expo Center'de markanızın en güzel şekilde sunulması için fuar standları kuruyoruz."),
        ("index.svc2_title_html", "Stend <span>Dizaynı</span>", "Stand <span>Tasarımı</span>"),
        ("index.svc3_link_html", "Eksteryer.\n                        Memarlıq.\n                        Estetika.", "Dış Mekân.\n                        Mimarlık.\n                        Estetik."),
        ("index.svc3_desc", "Binaların müasir və gözəl çöl görünüşünün memarlıq standartlarına uyğun dizayn edilməsi.", "Binaların modern ve estetik dış görünümünün mimarlık standartlarına uygun tasarlanması."),
        ("index.svc3_title_html", "Eksteryer <span>Dizaynı</span>", "Dış Mekân <span>Tasarımı</span>"),
        ("index.svc4_link_html", "Landşaft.\n                        Peysaj.\n                        Yaşıllıq.", "Peyzaj.\n                        Doğa.\n                        Yeşillik."),
        ("index.svc4_desc", "Həyətyanı sahələriniz və parklarınız üçün təbiətlə vəhdət təşkil edən peysaj dizaynı.", "Bahçe alanlarınız ve parklarınız için doğayla uyum içinde peyzaj tasarımı."),
        ("index.svc4_title_html", "Landşaft <span>Dizaynı</span>", "Peyzaj <span>Tasarımı</span>"),
        ("index.projects.title", "SON LAYİHƏLƏRİMİZ", "SON PROJELERİMİZ"),
        ("index.projects.p1_title_html", "Müasir Sərgi Stendi <br> Layihəsi", "Modern Fuar Standı <br> Projesi"),
        ("index.projects.p1_cat", "EKSPO STENDİ", "EXPO STANDI"),
        ("index.projects.p2_title_html", "Fərdi Yaşayış Evi <br> İnteryeri", "Özel Konut <br> İç Mekânı"),
        ("index.projects.p2_cat", "DAXİLİ MƏKAN", "İÇ MEKÂN"),
        ("index.projects.p3_title_html", "Müasir Eksteryer <br> Və Landşaft Dizaynı", "Modern Dış Mekân <br> ve Peyzaj Tasarımı"),
        ("index.projects.p3_cat", "ÇÖL MƏKAN VƏ PEYSAJ", "DIŞ MEKÂN VE PEYZAJ"),
        ("index.exp.subtitle", "TƏCRÜBƏMİZ", "DENEYİMİMİZ"),
        ("index.exp.title_html", "Sərgi stendləri və dizayn <br><span>sahəsində zəngin təcrübə</span>", "Fuar standları ve tasarım <br><span>alanında zengin deneyim</span>"),
        ("index.exp.desc", "Komandamızla birlikdə hər bir məkana funksionallıq, estetika və yüksək keyfiyyət qatırıq.", "Ekibimizle birlikte her mekâna işlevsellik, estetik ve yüksek kalite katıyoruz."),
        ("index.exp.stat1", "Uğurlu layihələr", "Başarılı projeler"),
        ("index.exp.stat2", "İllik təcrübə", "Yıllık deneyim"),
        ("index.exp.stat3", "Rəsmi tərəfdaş", "Resmi ortak"),
        ("index.exp.stat4", "Komanda üzvü", "Ekip üyesi"),
        ("index.cta.subtitle", "BİZİMLƏ ƏLAQƏ", "BİZİMLE İLETİŞİM"),
        ("index.cta.title_html", "2019-CU İLDƏN BƏRİ HƏR MƏQSƏDƏ UYĞUN <br>MƏKANLARIN QURULMASI", "2019'DAN BU YANA HER AMACA UYGUN <br>MEKÂNLARIN OLUŞTURULMASI"),
        ("index.proj6.title", "İnsanların məkanlarla, təbiətlə və texnologiya ilə əlaqəsini yenidən formalaşdıran fərqli layihələrə diqqət yetiririk.", "İnsanların mekânlarla, doğayla ve teknolojiyle bağlantısını yeniden şekillendiren farklı projelere odaklanıyoruz."),
        ("index.proj6.desc", "AA MEMARLIQ olaraq dizayn etdiyimiz hər bir məkanı özünəməxsus estetika, funksionallıq və müasirlik ilə zənginləşdiririk.", "AA MEMARLIQ olarak tasarladığımız her mekânı eşsiz estetik, işlevsellik ve modernlik ile zenginleştiriyoruz."),
        ("index.proj6.featured", "ÖNƏ ÇIXAN LAYİHƏ", "ÖNE ÇIKAN PROJE"),
        ("index.proj6.interior", "İNTERYER DİZAYNI", "İÇ MEKÂN TASARIMI"),
        ("index.proj6.arch", "MEMARLIQ", "MİMARLIK"),
        ("index.proj6.exhibition", "SƏRGİ STENDİ", "FUAR STANDI"),
        ("index.proj6.price_label", "Başlanğıc qiymət", "Başlangıç fiyatı"),
        ("index.proj6.p1_title", "Təbiətlə Vəhdət Stendi", "Doğayla Uyum Standı"),
        ("index.proj6.p2_title", "Müasir Lüks Ofis Məkanı", "Modern Lüks Ofis Mekânı"),
        ("index.proj6.p3_title", "Zərif Villa Layihəsi", "Zarif Villa Projesi"),
        ("index.proj6.p4_title", "Baku Expo Sərgi Stendi", "Baku Expo Fuar Standı"),
        ("index.proj6.d1", "1 Stend", "1 Stand"),
        ("index.proj6.d2", "1 Sahə", "1 Alan"),
        ("index.proj6.d3", "150 m²", "150 m²"),
        ("index.proj6.d4", "5 Otaq", "5 Oda"),
        ("index.proj6.d5", "2 Sanitar q.", "2 Banyo"),
        ("index.proj6.d6", "320 m²", "320 m²"),
        ("index.proj6.d7", "8 Otaq", "8 Oda"),
        ("index.proj6.d8", "4 Hamam", "4 Banyo"),
        ("index.proj6.d9", "450 m²", "450 m²"),
        ("index.proj6.d10", "1 Zona", "1 Bölge"),
        ("index.proj6.d11", "120 m²", "120 m²"),
        # --- about.html ---
        ("about.breadcrumb_sub_html", "2019-cu ildən bəri <br> Azərbaycanda sərgi və dizayn xidməti", "2019'dan bu yana <br> Azerbaycan'da fuar ve tasarım hizmeti"),
        ("about.breadcrumb_title", "Şirkətimiz", "Şirketimiz"),
        ("about.intro", "AA MEMARLIQ sərgi stendləri, interyer, eksteryer və landşaft dizaynı sahəsində ən yaxşı həlləri təklif edir. Peşəkar komandamız layihələrinizin dizaynından tutmuş qurulmasına qədər olan bütün mərhələləri yüksək səviyyədə həyata keçirir.", "AA MEMARLIQ fuar standları, iç mekân, dış mekân ve peyzaj tasarımı alanında en iyi çözümleri sunmaktadır. Profesyonel ekibimiz projelerinizin tasarımından kurulumuna kadar tüm aşamaları yüksek düzeyde gerçekleştirmektedir."),
        ("about.quote", "2019-cu ildən bəri sərgi sektorunda 100-dən çox layihəyə imza atmışıq. Müştəri məmnuniyyətini əsas tutaraq, layihələrinizi ən peşəkar şəkildə həyata keçirməyə davam edirik.", "2019'dan bu yana fuar sektöründe 100'den fazla projeye imza attık. Müşteri memnuniyetini esas alarak projelerinizi en profesyonel şekilde hayata geçirmeye devam ediyoruz."),
        ("about.tagline", "Ekspo və Memarlıq", "Expo ve Mimarlık"),
        ("about.side_title", "AA MEMARLIQ müasir dizayn fəlsəfəsinə və funksionallığa önəm verən, hər bir layihənin özünəməxsusluğunu əks etdirən fərdi sərgi stendləri və memarlıq layihələri hazırlayır.", "AA MEMARLIQ modern tasarım felsefesine ve işlevselliğe önem veren, her projenin özgünlüğünü yansıtan özel fuar standları ve mimarlık projeleri hazırlamaktadır."),
        ("about.exp1", "Uğurlu layihələr", "Başarılı projeler"),
        ("about.exp2", "İllik təcrübə", "Yıllık deneyim"),
        ("about.exp3", "Partnyorlar", "Ortaklar"),
        ("about.feature", "Memarlığa və stend dizaynına yeni nəfəs gətirərək, müştərilərimiz üçün ən müasir həlləri yaradırıq.", "Mimarlığa ve stand tasarımına yeni bir soluk getirerek müşterilerimiz için en modern çözümleri yaratıyoruz."),
        ("about.awards_sub", "MÜKAFATLARIMIZ", "ÖDÜLLERİMİZ"),
        ("about.awards_title_html", "Müxtəlif sahələrdə <br> Memarlıq və Dizayn mükafatları", "Çeşitli alanlarda <br> Mimarlık ve Tasarım ödülleri"),
        ("about.award1_html", "Uğurlu Stend Dizaynı Mükafatı <span>2023</span>", "Başarılı Stand Tasarımı Ödülü <span>2023</span>"),
        ("about.award2_html", "Qızıl Stend Mükafatı <span>2020</span>", "Altın Stand Ödülü <span>2020</span>"),
        ("about.award3_html", "Eksteryer və Landşaft Master Mükafatı <span>2019</span>", "Dış Mekân ve Peyzaj Ustalık Ödülü <span>2019</span>"),
        ("about.award4_html", "İlin Ən Yaxşı Sərgi Tərəfdaşı <span>2021</span>", "Yılın En İyi Fuar Ortağı <span>2021</span>"),
        ("about.awards_desc", "2019-cu ildən bəri müasir sərgi stendləri və memarlıq sahəsində ixtisaslaşaraq müştərilərimizə peşəkar və çoxşaxəli xidmətlər təqdim edirik.", "2019'dan bu yana modern fuar standları ve mimarlık alanında uzmanlaşarak müşterilerimize profesyonel ve çok yönlü hizmetler sunuyoruz."),
        # --- contact.html ---
        ("contact.page_sub", "Bizimlə əlaqə", "Bizimle iletişim"),
        ("contact.page_title_html", "Bizə yazın və <br>\n                                    layihənizi dərhal <br> başladaq.", "Bize yazın ve <br>\n                                    projenizi hemen <br> başlatalım."),
        ("contact.reach_title", "Əlaqə saxlayın", "İletişime geçin"),
        ("contact.reach_text_html", "Sizinlə işləməkdən və birlikdə möhtəşəm bir layihə ərsəyə gətirməkdən məmnun olarıq. <br>", "Sizinle çalışmaktan ve birlikte muhteşem bir proje ortaya koymaktan memnuniyet duyarız. <br>"),
        ("contact.follow", "İzləyin", "Takip Edin"),
        ("contact.dept_title", "Departamentlərimiz:", "Departmanlarımız:"),
        ("contact.dept1", "Baş Ofis (Ekspo Mərkəzi)", "Merkez Ofis (Expo Merkezi)"),
        ("contact.dept2", "Dizayn Departamenti", "Tasarım Departmanı"),
        ("contact.dept3", "İstehsalat və Quraşdırma", "Üretim ve Kurulum"),
        # --- faq.html ---
        ("faq.page_sub_html", "Ağlınızdakı sualların <br>\n                                    cavablarını tapın", "Aklınızdaki soruların <br>\n                                    cevaplarını bulun"),
        ("faq.page_title_html", "Tez-Tez Verilən <br>\n                                    Suallar", "Sıkça Sorulan <br>\n                                    Sorular"),
        ("faq.sidebar_sub", "FAQ", "SSS"),
        ("faq.sidebar_title", "Sualların cavabı yoxdur? Xüsusi cavablar əldə edin", "Sorularınızın cevabı yok mu? Özel cevaplar alın"),
        ("faq.q1", "Memarlar hansı xidmətləri göstərirlər?", "Mimarlar hangi hizmetleri sunmaktadır?"),
        ("faq.a1", "AA MEMARLIQ olaraq biz sərgi stendlərinin dizaynı və quraşdırılması, yaşayış və kommersiya obyektlərinin interyer və eksteryer dizaynı, habelə landşaft dizaynı və layihələrin idarəedilməsi xidmətlərini təqdim edirik.", "AA MEMARLIQ olarak fuar standlarının tasarımı ve kurulumu, konut ve ticari yapıların iç mekân ve dış mekân tasarımı ile peyzaj tasarımı ve proje yönetimi hizmetlerini sunmaktayız."),
        ("faq.q2", "Layihəmin hansı mərhələsində memarla əlaqə saxlamalıyamsa?", "Projemin hangi aşamasında mimarla iletişime geçmeliyim?"),
        ("faq.a2", "Layihənin ən erkən mərhələsində memarla işləməyə başlamaq tövsiyə olunur. Bu, ilkin konsepsiyanın düzgün qurulmasına, büdcə planlaşdırılmasına və gələcəkdə yarana biləcək problemlərin qarşısının alınmasına kömək edir.", "Projenin en erken aşamasında mimarla çalışmaya başlamanız önerilir. Bu, ilk konseptin doğru oluşturulmasına, bütçe planlamasına ve gelecekte ortaya çıkabilecek sorunların önlenmesine yardımcı olur."),
        ("faq.q3", "İnteryer dizaynerlərinizin iş nümunələri və tövsiyə məktubları varmı?", "İç mekân tasarımcılarınızın iş örnekleri ve tavsiye mektupları var mı?"),
        ("faq.a3", "Bəli, bizim zəngin portfoliomuz mövcuddur. Baku Expo Center və digər məkanlarda həyata keçirdiyimiz 100-dən çox layihənin dizayn və quraşdırılma nümunələrini ofisimizdə və ya vebsaytımızın layihələr bölməsində nəzərdən keçirə bilərsiniz.", "Evet, zengin portföyümüz mevcuttur. Baku Expo Center ve diğer mekânlarda gerçekleştirdiğimiz 100'den fazla projenin tasarım ve kurulum örneklerini ofisimizde veya web sitemizin projeler bölümünde inceleyebilirsiniz."),
        ("faq.q4", "Layihəm üçün düzgün memarı necə tapa bilərəm?", "Projem için doğru mimarı nasıl bulabilirim?"),
        ("faq.a4", "Düzgün memar seçmək üçün onun əvvəlki iş təcrübəsini, portfolio keyfiyyətini və sizin baxış bucağınızı nə dərəcədə anladığını yoxlamalısınız. AA MEMARLIQ olaraq biz hər layihəyə fərdi yanaşaraq mükəmməl nəticə zəmanəti veririk.", "Doğru mimarı seçmek için önceki iş deneyimini, portföy kalitesini ve bakış açınızı ne ölçüde anladığını kontrol etmelisiniz. AA MEMARLIQ olarak her projeye bireysel yaklaşarak mükemmel sonuç garantisi veriyoruz."),
        ("faq.q5", "Memarlıq planlarını hazırlamaq üçün ən yaxşı vaxt hansıdır?", "Mimarlık planlarını hazırlamak için en uygun zaman nedir?"),
        ("faq.a5", "Tikinti və ya quraşdırma işlərinə başlamazdan ən azı bir neçə ay öncə planların hazırlanması idealdır. Bu, bütün detalların dəqiqləşdirilməsinə, material seçiminə və rəsmi icazələrin/təsdiqlərin alınmasına kifayət qədər vaxt yaradır.", "İnşaat veya kurulum işlerine başlamadan en az birkaç ay önce planların hazırlanması idealdir. Bu, tüm detayların netleştirilmesine, malzeme seçimine ve resmi izinlerin/onayların alınmasına yeterli zaman sağlar."),
        ("faq.q6", "Çizimlərin və dizaynın tamamlanması nə qədər vaxt aparır?", "Çizimlerin ve tasarımın tamamlanması ne kadar zaman alır?"),
        ("faq.a6", "Layihənin mürəkkəbliyindən və miqyasından asılı olaraq dizayn mərhələsi adətən 2 həftədən 1 aya qədər çəkir. Sərgi stendlərinin dizaynı isə daha sürətli şəkildə — bir neçə gün ərzində hazırlana bilər.", "Projenin karmaşıklığına ve ölçeğine bağlı olarak tasarım aşaması genellikle 2 haftadan 1 aya kadar sürer. Fuar standlarının tasarımı ise daha hızlı bir şekilde — birkaç gün içinde hazırlanabilir."),
        ("faq.q7", "Kommersiya yoxsa yaşayış sahələrinin dizayn və memarlığını edirsiniz?", "Ticari mi yoksa konut alanlarının tasarım ve mimarlığını mı yapıyorsunuz?"),
        ("faq.a7", "Biz hər iki sahədə xidmət göstəririk. Həm fərdi villaların, mənzillərin interyer dizaynını, həm də sərgi stendləri, ofislər, restoranlar və digər kommersiya obyektlərinin dizayn və quraşdırılmasını həyata keçiririk.", "Her iki alanda da hizmet vermekteyiz. Hem bireysel villaların, dairelerin iç mekân tasarımını hem de fuar standları, ofisler, restoranlar ve diğer ticari yapıların tasarım ve kurulumunu gerçekleştiriyoruz."),
        ("faq.q8", "Qiymətləriniz necə təyin olunur? Bütün layihələr yüksək büdcəlidirmi?", "Fiyatlarınız nasıl belirlenmektedir? Tüm projeler yüksek bütçeli midir?"),
        ("faq.a8", "Layihələrimizin qiyməti sahənin ölçüsünə, istifadə olunacaq materialların növünə və dizaynın mürəkkəbliyinə görə fərdi olaraq hesablanır. Hər bir müştərinin büdcəsinə uyğun optimallaşdırılmış və keyfiyyətli həllər təklif edirik.", "Projelerimizin fiyatı alanın büyüklüğüne, kullanılacak malzemelerin türüne ve tasarımın karmaşıklığına göre bireysel olarak hesaplanır. Her müşterinin bütçesine uygun optimize edilmiş ve kaliteli çözümler sunuyoruz."),
        ("faq.q9", "Memarlarla işləmək layihənin maya dəyərini əhəmiyyətli dərəcədə artırmırmı?", "Mimarlarla çalışmak projenin maliyetini önemli ölçüde artırır mı?"),
        ("faq.a9", "Əksinə, peşəkar memarla çalışmaq material itkisinin qarşısını alır, səhv tikinti/quraşdırma xərclərini aradan qaldırır və büdcənizdən maksimum səmərəli istifadə etməyə kömək etməklə sizə qənaət bəxş edir.", "Aksine, profesyonel bir mimarla çalışmak malzeme israfını önler, hatalı inşaat/kurulum masraflarını ortadan kaldırır ve bütçenizden maksimum verimli kullanım sağlayarak size tasarruf sağlar."),
        # --- service-11.html ---
        ("services.breadcrumb_sub_html", "Şirkətimiz tərəfindən təqdim olunan <br> peşəkar memarlıq və dizayn xidmətləri", "Şirketimiz tarafından sunulan <br> profesyonel mimarlık ve tasarım hizmetleri"),
        ("services.breadcrumb_title", "Xidmətlərimiz", "Hizmetlerimiz"),
        ("services.section_tag", "[ Xidmətlərimiz ]", "[ Hizmetlerimiz ]"),
        ("services.s1_title", "İnteryer və Eksteryer", "İç Mekân ve Dış Mekân"),
        ("services.s1_desc", "Müştərilərimizin istəklərinə uyğun fərdi dizayn edilmiş interyer və eksteryer layihələrimiz, layihənin yerindən, həcmindən və büdcəsindən asılı olmayaraq bütün tələblərə cavab verir.", "Müşterilerimizin isteklerine uygun özel tasarlanmış iç mekân ve dış mekân projelerimiz, projenin konumundan, hacminden ve bütçesinden bağımsız olarak tüm gereksinimleri karşılamaktadır."),
        ("services.s2_title", "Memarlıq Layihələri", "Mimarlık Projeleri"),
        ("services.s2_desc", "AA MEMARLIQ olaraq dizayn və memarlıq sahəsindəki zəngin təcrübəmizlə layihələrinizin həm estetik cəhətdən gözəl, həm də struktur cəhətdən davamlı olmasını təmin edirik.", "AA MEMARLIQ olarak tasarım ve mimarlık alanındaki zengin deneyimimizle projelerinizin hem estetik hem de yapısal açıdan dayanıklı olmasını sağlıyoruz."),
        ("services.s3_title", "Sərgi Stendləri", "Fuar Standları"),
        ("services.s3_desc", "Yerli və beynəlxalq səviyyəli müştərilərimiz üçün Baku Expo Center və digər məkanlarda sərgi stendlərinin dizaynı və peşəkar quraşdırılması xidmətini təklif edirik.", "Yerel ve uluslararası düzeydeki müşterilerimiz için Baku Expo Center ve diğer mekânlarda fuar standlarının tasarımı ve profesyonel kurulumu hizmetini sunuyoruz."),
        ("services.s4_title", "Layihə İdarəetməsi", "Proje Yönetimi"),
        ("services.s4_desc", "Layihəni ilk eskizdən açar təhvil verilməsinə qədər bütün mərhələlərdə peşəkar planlaşdırma, koordinasiya və keyfiyyət nəzarəti xidməti göstəririk.", "Projeyi ilk eskizden anahtar teslimine kadar tüm aşamalarda profesyonel planlama, koordinasyon ve kalite kontrolü hizmeti sunuyoruz."),
        # --- service detail pages (shared + specific) ---
        ("svc.interyer.page_title", "İnteryer və Eksteryer", "İç Mekân ve Dış Mekân"),
        ("svc.interyer.hero_html", "Müştərilərimizin ehtiyaclarına uyğun hazırlanmış interyer və eksteryer layihələri. <span>Funksionallıq, estetika və rahatlıq</span> prinsipləri əsasında hər bir məkan harmonik şəkildə dizayn edilib.", "Müşterilerimizin ihtiyaçlarına uygun hazırlanmış iç mekân ve dış mekân projeleri. <span>İşlevsellik, estetik ve konfor</span> ilkeleri doğrultusunda her mekân uyumlu bir şekilde tasarlanmıştır."),
        ("svc.interyer.ov1", "Yaşayış və kommersiya məkanları üçün daxili və xarici interyer həlləri hazırlayırıq. Hər layihədə işıqlandırma, material seçimi və funksional planlaşdırma müasir dizayn prinsiplərinə uyğun həyata keçirilir.", "Konut ve ticari mekânlar için iç ve dış mekân çözümleri hazırlıyoruz. Her projede aydınlatma, malzeme seçimi ve fonksiyonel planlama modern tasarım ilkelerine uygun gerçekleştirilmektedir."),
        ("svc.interyer.ov2", "Fərdi yaşayış evlərindən tutmuş kommersiya məkanlarına qədər bütün interyer layihələrində vahid estetik dil və yüksək keyfiyyət standartları qorunur.", "Özel konutlardan ticari mekânlara kadar tüm iç mekân projelerinde birleşik estetik dil ve yüksek kalite standartları korunmaktadır."),
        ("svc.interyer.w1", "İnteryer konsepsiyasının hazırlanması və 3D vizualizasiya", "İç mekân konseptinin hazırlanması ve 3D görselleştirme"),
        ("svc.interyer.w2", "Eksteryer görünüşün planlaşdırılması", "Dış mekân görünümünün planlanması"),
        ("svc.interyer.w3", "Mebel, işıqlandırma və dekor elementlərinin seçimi", "Mobilya, aydınlatma ve dekor elemanlarının seçimi"),
        ("svc.interyer.w4", "Funksional planlaşdırma və rahat məkan təşkili", "Fonksiyonel planlama ve konforlu mekân düzenlemesi"),
        ("svc.memarliq.page_title", "Memarlıq Layihələri", "Mimarlık Projeleri"),
        ("svc.memarliq.hero_html", "Kommersiya və nümayiş məkanları üçün hazırlanmış <span>memarlıq və interyer layihələri</span>. Estetik, funksional və müasir dizayn prinsipləri əsasında.", "Ticari ve sergi mekânları için hazırlanmış <span>mimarlık ve iç mekân projeleri</span>. Estetik, fonksiyonel ve modern tasarım ilkeleri doğrultusunda."),
        ("svc.memarliq.ov1", "AA MEMARLIQ olaraq dizayn və memarlıq sahəsindəki zəngin təcrübəmizlə layihələrinizin həm estetik cəhətdən gözəl, həm də struktur cəhətdən davamlı olmasını təmin edirik.", "AA MEMARLIQ olarak tasarım ve mimarlık alanındaki zengin deneyimimizle projelerinizin hem estetik hem de yapısal açıdan dayanıklı olmasını sağlıyoruz."),
        ("svc.memarliq.ov2", "Showroom və kommersiya məkanlarında vahid dizayn dili, peşəkar planlaşdırma və yüksək keyfiyyətli icra ilə fərqlənirik.", "Showroom ve ticari mekânlarda birleşik tasarım dili, profesyonel planlama ve yüksek kaliteli uygulama ile fark yaratıyoruz."),
        ("svc.memarliq.w1", "Memarlıq konsepsiyasının hazırlanması", "Mimarlık konseptinin hazırlanması"),
        ("svc.memarliq.w2", "Nümayiş və satış zonalarının planlaşdırılması", "Sergi ve satış alanlarının planlanması"),
        ("svc.memarliq.w3", "3D vizualizasiya və texniki eskizlər", "3D görselleştirme ve teknik eskizler"),
        ("svc.memarliq.w4", "Material və işıqlandırma həllərinin seçimi", "Malzeme ve aydınlatma çözümlerinin seçimi"),
        ("svc.sergi.page_title", "Sərgi Stendləri", "Fuar Standları"),
        ("svc.sergi.hero_html", "Baku Expo Center və digər sərgi məkanları üçün hazırlanmış <span>funksional, estetik və brendə uyğun</span> sərgi stendi layihələri.", "Baku Expo Center ve diğer fuar mekânları için hazırlanmış <span>fonksiyonel, estetik ve markaya uygun</span> fuar standı projeleri."),
        ("svc.sergi.ov1", "Yerli və beynəlxalq səviyyəli müştərilərimiz üçün Baku Expo Center və digər məkanlarda sərgi stendlərinin dizaynı və peşəkar quraşdırılması xidmətini təklif edirik.", "Yerel ve uluslararası düzeydeki müşterilerimiz için Baku Expo Center ve diğer mekânlarda fuar standlarının tasarımı ve profesyonel kurulumu hizmetini sunuyoruz."),
        ("svc.sergi.ov2", "Stend quruluşu, işıqlandırma, material seçimi və brendinq zonalarının planlaşdırılması müasir sərgi stendi dizayn prinsiplərinə uyğun həyata keçirilir.", "Stand kurulumu, aydınlatma, malzeme seçimi ve markalama alanlarının planlanması modern fuar standı tasarım ilkelerine uygun gerçekleştirilmektedir."),
        ("svc.sergi.w1", "Stend konsepsiyasının hazırlanması", "Stand konseptinin hazırlanması"),
        ("svc.sergi.w2", "Brendinq və nümayiş zonalarının dizaynı", "Markalama ve sergi alanlarının tasarımı"),
        ("svc.sergi.w3", "İstehsal, montaj və quraşdırma", "Üretim, montaj ve kurulum"),
        ("svc.sergi.w4", "Sərgi açılışına qədər tam hazırlıq", "Fuar açılışına kadar tam hazırlık"),
        ("svc.pm.page_title", "Layihə İdarəetməsi", "Proje Yönetimi"),
        ("svc.pm.hero_html", "Korporativ ofis layihələrində <span>planlaşdırma, koordinasiya və keyfiyyət nəzarəti</span> prinsiplərinə uyğun peşəkar layihə idarəetməsi.", "Kurumsal ofis projelerinde <span>planlama, koordinasyon ve kalite kontrolü</span> ilkelerine uygun profesyonel proje yönetimi."),
        ("svc.pm.ov1", "Layihəni ilk eskizdən açar təhvil verilməsinə qədər bütün mərhələlərdə peşəkar şəkildə idarə edirik. Korporativ ofis layihələrində vaxt, büdcə və keyfiyyət balansını qoruyuruq.", "Projeyi ilk eskizden anahtar teslimine kadar tüm aşamalarda profesyonel şekilde yönetiyoruz. Kurumsal ofis projelerinde zaman, bütçe ve kalite dengesini koruyoruz."),
        ("svc.pm.ov2", "Hər müştəriyə xüsusi layihə meneceri təyin olunur — bütün mərhələlər üzrə hesabatlar və yeniliklər müntəzəm təqdim edilir.", "Her müşteriye özel proje yöneticisi atanır — tüm aşamalara ilişkin raporlar ve güncellemeler düzenli olarak sunulur."),
        ("svc.pm.w1", "Layihə planlaşdırması və vaxt cədvəli", "Proje planlaması ve zaman çizelgesi"),
        ("svc.pm.w2", "Podratçı və təchizatçı koordinasiyası", "Taşeron ve tedarikçi koordinasyonu"),
        ("svc.pm.w3", "Keyfiyyət nəzarəti və hesabatlılıq", "Kalite kontrolü ve raporlama"),
        ("svc.pm.w4", "Vaxtında təhvil və son yoxlama", "Zamanında teslim ve son kontrol"),
        # --- portfolio pages ---
        ("port.showroom.page_title_html", "Premium Showroom <br>                                    Interyeri", "Premium Showroom <br>                                    İç Mekânı"),
        ("port.showroom.hero_html", "Müasir showroom mühitində <span>funksionallıq, rahatlıq və peşəkar görünüş</span> prinsiplərinə uyğun hazırlanmış interyer layihəsi.", "Modern showroom ortamında <span>işlevsellik, konfor ve profesyonel görünüm</span> ilkelerine uygun hazırlanmış iç mekân projesi."),
        ("port.showroom.ov1", "Bu layihədə Showroom məkanının iş prosesinə uyğun planlaşdırılması, işıqlandırma, material seçimi və iş zonalarının optimallaşdırılması müasir showroom dizayn prinsiplərinə uyğun həyata keçirilib.", "Bu projede showroom mekânının iş sürecine uygun planlanması, aydınlatma, malzeme seçimi ve çalışma alanlarının optimizasyonu modern showroom tasarım ilkelerine uygun gerçekleştirilmiştir."),
        ("port.showroom.ov2", "Qəbul, nümayiş və satış sahələrində vahid dizayn dili qorunub — həm estetik, həm də funksional showroom mühiti yaradılıb.", "Karşılama, sergi ve satış alanlarında birleşik tasarım dili korunmuş — hem estetik hem de fonksiyonel bir showroom ortamı yaratılmıştır."),
        ("port.showroom.w1", "Showroom interyer konsepsiyasinin hazirlanmasi", "Showroom iç mekân konseptinin hazırlanması"),
        ("port.showroom.w2", "Nümayiş zonalarının planlaşdırılması və 3D vizualizasiya", "Sergi alanlarının planlanması ve 3D görselleştirme"),
        ("port.showroom.w3", "Mebel, işıqlandırma və dekor elementlərinin seçimi", "Mobilya, aydınlatma ve dekor elemanlarının seçimi"),
        ("port.showroom.w4", "Peşəkar və rahat showroom mühitinin qurulması", "Profesyonel ve konforlu showroom ortamının oluşturulması"),
        ("port.home.page_title_html", "F?rdi Yasayis Evi <br>\n                                    Interyeri", "Özel Konut <br>\n                                    İç Mekânı"),
        ("port.home.page_title_fixed_html", "Fərdi Yaşayış Evi <br>\n                                    Interyeri", "Özel Konut <br>\n                                    İç Mekânı"),
        ("port.home.hero_html", "Müştərinin ehtiyaclarına uygun hazirlanmis fərdi yaşayış evi interyeri layihəsi. <span>Funksionallıq, estetika və rahatlıq</span> prinsipləri əsasında hər bir otaq harmonik şəkildə dizayn edilib.", "Müşterinin ihtiyaçlarına uygun hazırlanmış özel konut iç mekân projesi. <span>İşlevsellik, estetik ve konfor</span> ilkeleri doğrultusunda her oda uyumlu bir şekilde tasarlanmıştır."),
        ("port.home.ov1", "Bu layihədə yaşayış məkanının gündəlik istifadə rahatlığı, işıqlandırma, material seçimi və mebel yerləşdirməsi müasir interyer prinsiplərinə uyğun planlaşdırılıb.", "Bu projede yaşam alanının günlük kullanım konforu, aydınlatma, malzeme seçimi ve mobilya yerleşimi modern iç mekân ilkelerine uygun planlanmıştır."),
        ("port.home.ov2", "Hər bir otaq müştərinin həyat tərzinə uyğun fərdi yanaşma ilə dizayn edilib — qonaq otağından yataq otaqlarına qədər bütün məkanlarda vahid estetik dil qorunub.", "Her oda müşterinin yaşam tarzına uygun bireysel yaklaşımla tasarlanmıştır — oturma odasından yatak odalarına kadar tüm mekânlarda birleşik estetik dil korunmuştur."),
        ("port.home.w1", "İnteryer konsepsiyasının hazırlanması və 3D vizualizasiya", "İç mekân konseptinin hazırlanması ve 3D görselleştirme"),
        ("port.home.w2", "Mebel, işıqlandırma və dekor elementlərinin seçimi", "Mobilya, aydınlatma ve dekor elemanlarının seçimi"),
        ("port.home.w3", "Rəng palitrası və material harmoniyasının qurulması", "Renk paleti ve malzeme uyumunun oluşturulması"),
        ("port.home.w4", "Funksional planlaşdırma və rahat məkan təşkili", "Fonksiyonel planlama ve konforlu mekân düzenlemesi"),
        ("port.ofis.page_title_html", "Müasir Ofis <br>\n                                    Interyeri", "Modern Ofis <br>\n                                    İç Mekânı"),
        ("port.ofis.hero_html", "Müasir ofis mühitində <span>funksionallıq, rahatlıq və peşəkar görünüş</span> prinsiplərinə uyğun hazırlanmış interyer layihəsi.", "Modern ofis ortamında <span>işlevsellik, konfor ve profesyonel görünüm</span> ilkelerine uygun hazırlanmış iç mekân projesi."),
        ("port.ofis.ov1", "Bu layihədə ofis məkanının iş prosesinə uyğun planlaşdırılması, işıqlandırma, material seçimi və iş zonalarının optimallaşdırılması müasir ofis dizayn prinsiplərinə uyğun həyata keçirilib.", "Bu projede ofis mekânının iş sürecine uygun planlanması, aydınlatma, malzeme seçimi ve çalışma alanlarının optimizasyonu modern ofis tasarım ilkelerine uygun gerçekleştirilmiştir."),
        ("port.ofis.ov2", "Qəbul, iş otaqları və ümumi istifadə sahələrində vahid dizayn dili qorunub — həm estetik, həm də funksional ofis mühiti yaradılıb.", "Karşılama, çalışma odaları ve ortak kullanım alanlarında birleşik tasarım dili korunmuş — hem estetik hem de fonksiyonel bir ofis ortamı yaratılmıştır."),
        ("port.ofis.w1", "Ofis interyer konsepsiyasinin hazirlanmasi", "Ofis iç mekân konseptinin hazırlanması"),
        ("port.ofis.w2", "İş zonalarının planlaşdırılması və 3D vizualizasiya", "Çalışma alanlarının planlanması ve 3D görselleştirme"),
        ("port.ofis.w3", "Mebel, işıqlandırma və dekor elementlərinin seçimi", "Mobilya, aydınlatma ve dekor elemanlarının seçimi"),
        ("port.ofis.w4", "Peşəkar və rahat ofis mühitinin qurulması", "Profesyonel ve konforlu ofis ortamının oluşturulması"),
        ("port.sergi.page_title_html", "Sərgi <br>\n                                    Stendləri", "Fuar <br>\n                                    Standları"),
        ("port.sergi.hero_html", "Baku Expo Center və digər sərgi məkanları üçün hazırlanmış <span>funksional, estetik və brendə uyğun</span> sərgi stendi layihələri.", "Baku Expo Center ve diğer fuar mekânları için hazırlanmış <span>fonksiyonel, estetik ve markaya uygun</span> fuar standı projeleri."),
        ("port.sergi.ov1", "Bu layihədə stend quruluşu, işıqlandırma, material seçimi və brendinq zonalarının planlaşdırılması müasir sərgi stendi dizayn prinsiplərinə uyğun həyata keçirilib.", "Bu projede stand kurulumu, aydınlatma, malzeme seçimi ve markalama alanlarının planlanması modern fuar standı tasarım ilkelerine uygun gerçekleştirilmiştir."),
        ("port.sergi.ov2", "Quruluş, nümayiş və qarşılama sahələrində vahid dizayn dili qorunub — həm estetik, həm də funksional sərgi stendi mühiti yaradılıb.", "Kurulum, sergi ve karşılama alanlarında birleşik tasarım dili korunmuş — hem estetik hem de fonksiyonel bir fuar standı ortamı yaratılmıştır."),
        ("port.sergi.w1", "Sərgi stendi konsepsiyasinin hazirlanmasi", "Fuar standı konseptinin hazırlanması"),
        ("port.sergi.w2", "Stend zonalarının planlaşdırılması və 3D vizualizasiya", "Stand alanlarının planlanması ve 3D görselleştirme"),
        ("port.sergi.w3", "Mebel, işıqlandırma və dekor elementlərinin seçimi", "Mobilya, aydınlatma ve dekor elemanlarının seçimi"),
        ("port.sergi.w4", "Peşəkar və rahat sərgi stendi mühitinin qurulması", "Profesyonel ve konforlu fuar standı ortamının oluşturulması"),
    ]


TRANSLATIONS = _build_translations()


def _i(key, html=False, ph=False):
    """Build data-i18n attribute fragment."""
    if ph:
        return f'data-i18n-placeholder="{key}"'
    if html:
        return f'data-i18n="{key}" data-i18n-html'
    return f'data-i18n="{key}"'


def _build_injections():
    I = []  # (old, new)

    def add(old, key, html=False, ph=False):
        attr = _i(key, html=html, ph=ph)
        if ph:
            new = old.replace("placeholder=", f"{attr} placeholder=", 1)
        elif '="' in old.split(">", 1)[0]:
            new = old.replace('>', f' {attr}>', 1)
        else:
            new = old.replace("<", f"<", 1)
            idx = new.index(">")
            new = new[:idx] + f" {attr}" + new[idx:]
        I.append((old, new))

    # Shared navigation (data-i18n on anchor)
    nav = [
        ('<li><a href="/">Ana Səhifə</a></li>', '<li><a href="/" data-i18n="nav.home">Ana Səhifə</a></li>'),
        ('<li><a href="/haqqimizda">Haqqımızda</a></li>', '<li><a href="/haqqimizda" data-i18n="nav.about">Haqqımızda</a></li>'),
        ('<a href="/xidmetlerimiz">Xidmətlərimiz</a>', '<a href="/xidmetlerimiz" data-i18n="nav.services">Xidmətlərimiz</a>'),
        ('<li><a href="/interyer-eksteryer">İnteryer və Eksteryer</a></li>', '<li><a href="/interyer-eksteryer" data-i18n="nav.svc_interyer">İnteryer və Eksteryer</a></li>'),
        ('<li><a href="/memarliq-layiheleri">Memarlıq Layihələri</a></li>', '<li><a href="/memarliq-layiheleri" data-i18n="nav.svc_memarliq">Memarlıq Layihələri</a></li>'),
        ('<li><a href="/sergi-stendleri">Sərgi Stendləri</a></li>', '<li><a href="/sergi-stendleri" data-i18n="nav.svc_sergi">Sərgi Stendləri</a></li>'),
        ('<li><a href="/layihe-idareetmesi">Layihə İdarəetməsi</a></li>', '<li><a href="/layihe-idareetmesi" data-i18n="nav.svc_pm">Layihə İdarəetməsi</a></li>'),
        ('<li><a href="/faq">FAQ</a></li>', '<li><a href="/faq" data-i18n="nav.faq">FAQ</a></li>'),
        ('<li><a href="/elaqe">Əlaqə</a></li>', '<li><a href="/elaqe" data-i18n="nav.contact">Əlaqə</a></li>'),
        ('<li><a href="/#layiheler">Layihələr</a></li>', '<li><a href="/#layiheler" data-i18n="nav.projects">Layihələr</a></li>'),
    ]
    for old, new in nav:
        I.append((old, new))

    # Shared buttons / sidebar
    shared = [
        ('<span class="text-one">Əlaqə</span>', "btn.contact"),
        ('<span class="text-two">Əlaqə</span>', "btn.contact"),
        ('<span class="text-one">Bizimlə Danışın</span>', "btn.contact_talk"),
        ('<span class="text-two">Bizimlə Danışın</span>', "btn.contact_talk"),
        ('<h2 class="title">Bizimlə Əlaqə</h2>', "sidebar.contact_title"),
        ('<span class="text">Baku Expo Center</span>', "footer.location_line"),
        ('<span class="text">Baku Expo Center, Bakı, Azərbaycan</span>', "info.baku_full"),
        ('<span class="text">Əlaqə </span>', "btn.contact"),
        ('<span class="text">Bizimlə Danışın </span>', "btn.contact_talk"),
        ('<span class="text">İndi göndər </span>', "btn.send_now"),
        ('<span class="text">Ətraflı </span>', "btn.more"),
        ('<span class="text">Bütün Layihələr </span>', "btn.all_projects"),
        ('<span class="text">Xidmətləri araşdırın </span>', "btn.explore_services"),
        ('<h2 class="title">Abunə olun</h2>', "footer.subscribe"),
        ('<h2 class="title">Sürətli Keçidlər</h2>', "footer.quick_links"),
        ('<h2 class="title">Sosial Şəbəkələr</h2>', "footer.social"),
        ('<h2 class="title">Ofis</h2>', "footer.office"),
        ('<span>Haqqımızda</span>', "nav.about"),
        ('<span>Layihələr</span>', "nav.projects"),
        ('<span>Xidmətlər</span>', "nav.services_short"),
        ('<span>Əlaqə</span>', "nav.contact"),
        ('<span>Müştəri:</span>', "info.client"),
        ('<span>Tip:</span>', "info.type"),
        ('<span>İl:</span>', "info.year"),
        ('<span>Sahə:</span>', "info.area"),
        ('<span>Yer:</span>', "info.location"),
        ('<span>Status:</span>', "info.status"),
        ('<h4 class="sub-title">Məlumat</h4>', "info.details"),
        ('<h6 class="title">Ümumi baxış</h6>', "info.overview"),
        ('<li class="title">İş həcmi</li>', "info.scope"),
    ]
    for old, key in shared:
        add(old, key)

    # Placeholders
    phs = [
        ('placeholder="Ad"', "ph.name"),
        ('placeholder="Ad*"', "ph.name_req"),
        ('placeholder="Adınız*"', "ph.name_your"),
        ('placeholder="E-poçt*"', "ph.email"),
        ('placeholder="E-poçt ünvanınız"', "ph.email_addr"),
        ('placeholder="E-poçt ünvaniniz"', "ph.email_addr2"),
        ('placeholder="Telefon*"', "ph.phone"),
        ('placeholder="Şirkət"', "ph.company"),
        ('placeholder="Tələb olunan xidmət*"', "ph.service"),
        ('placeholder="Mesajınız*"', "ph.message"),
        ('placeholder="Mesajınız"', "ph.message_opt"),
    ]
    for old, key in phs:
        add(f'<input type="text" name="name" id="name" {old}>', key, ph=True)
        add(f'<input type="text" name="name" id="name2" {old}>', key, ph=True)
        add(f'<input type="email" name="email" id="email" {old}>', key, ph=True)
        add(f'<input type="text" name="email" id="email2" {old}>', key, ph=True)
        add(f'<input type="text" name="phone" id="phone" {old}>', key, ph=True)
        add(f'<input type="text" name="company" id="company" {old}>', key, ph=True)
        add(f'<input type="text" name="solution" id="solution"\n                                                    {old}>', key, ph=True)
        add(f'<input type="text" name="message" id="message" {old}>', key, ph=True)
        add(f'<textarea id="message" name="message" {old}>', key, ph=True)

    # Select budget
    I.append((
        '<option value="0" disabled selected>Büdcə*</option>',
        f'<option value="0" disabled selected {_i("ph.budget")}>Büdcə*</option>',
    ))
    for n in range(1, 6):
        az = TRANSLATIONS[f"select.budget_{n}"]["az"]
        I.append((
            f'<option value="{n}">{az}</option>',
            f'<option value="{n}" {_i(f"select.budget_{n}")}>{az}</option>',
        ))

    # index.html specific
    index_items = [
        ('<h6>Baku Expo Center ilə rəsmi müqaviləli olaraq fəaliyyət göstərən peşəkar ekspo stend və memarlıq şirkəti.</h6>', "sidebar.tagline"),
        ('<span class="date">Yaranma: 2019</span>', "sidebar.founded"),
        ('<h6 class="title">Sosial Media</h6>', "sidebar.social"),
        ('<h6 class="title">Menyu</h6>', "sidebar.menu"),
        ('<h6 class="title">Bizə yazın</h6>', "sidebar.write_us"),
        ('<button id="side-info-4-close" class="side-info-close">\n            Bağla<i class="fas fa-times"></i>\n          </button>',
         '<button id="side-info-4-close" class="side-info-close">\n            <span data-i18n="btn.close">Bağla</span><i class="fas fa-times"></i>\n          </button>'),
        ('<h6 class="sub-title">Bakı, Azərbaycan.</h6>', "index.hero.location"),
        ('<p class="desc">Müştəri məmnuniyyətinə əsaslanaraq müasir sərgi stendləri, landşaftlar, eksteryer və interyerlər dizayn edirik.</p>', "index.hero.desc"),
        ('<h6 class="sub-title">Məkanların Həyata İlham Verdiyi Yer</h6>', "index.hero.subtitle"),
        ('<h2 class="title">İnteryer</h2>', "index.hero.interior"),
        ('<h2 class="sub-title">ŞİRKƏTİMİZ</h2>', "index.about.subtitle"),
        ('<h2 class="title rr_title_anim">SON LAYİHƏLƏRİMİZ</h2>', "index.projects.title"),
        ('<h2 class="sub-title">TƏCRÜBƏMİZ</h2>', "index.exp.subtitle"),
        ('<h2 class="sub-title">BİZİMLƏ ƏLAQƏ</h2>', "index.cta.subtitle"),
        ('<h3 class="title">Gəlin birlikdə işləyək</h3>', "footer.work_together"),
        ('<h2 class="title">YENİLİKLƏRƏ ABUNƏ OLUN</h2>', "footer.subscribe_banner"),
        ('<h2 class="title">Sürətli Keçidlər</h2>', "footer.quick_links"),
        ('<li><a href="/elaqe">İstifadə qaydaları</a></li>', '<li><a href="/elaqe" data-i18n="footer.terms">İstifadə qaydaları</a></li>'),
        ('<li>EKSPO STENDİ</li>', "index.projects.p1_cat"),
        ('<li>DAXİLİ MƏKAN</li>', "index.projects.p2_cat"),
        ('<li>ÇÖL MƏKAN VƏ PEYSAJ</li>', "index.projects.p3_cat"),
        ('<h2 class="sub-title">ÖNƏ ÇIXAN LAYİHƏ</h2>', "index.proj6.featured"),
        ('<h2 class="sub-title">İNTERYER DİZAYNI</h2>', "index.proj6.interior"),
        ('<h2 class="sub-title">MEMARLIQ</h2>', "index.proj6.arch"),
        ('<h2 class="sub-title">SƏRGİ STENDİ</h2>', "index.proj6.exhibition"),
        ('<span>Başlanğıc qiymət</span>', "index.proj6.price_label"),
        ('<h3 class="title"><a href="/sergi-stendi-layihe">Təbiətlə Vəhdət Stendi</a></h3>', "index.proj6.p1_title"),
        ('<h3 class="title"><a href="/sergi-stendi-layihe">Müasir Lüks Ofis Məkanı</a></h3>', "index.proj6.p2_title"),
        ('<h3 class="title"><a href="/sergi-stendi-layihe">Zərif Villa Layihəsi</a></h3>', "index.proj6.p3_title"),
        ('<h3 class="title"><a href="/sergi-stendi-layihe">Baku Expo Sərgi Stendi</a></h3>', "index.proj6.p4_title"),
        ('<h3 class="sub-title">Uğurlu layihələr</h3>', "index.exp.stat1"),
        ('<h3 class="sub-title">İllik təcrübə</h3>', "index.exp.stat2"),
        ('<h3 class="sub-title">Rəsmi tərəfdaş</h3>', "index.exp.stat3"),
        ('<h3 class="sub-title">Komanda üzvü</h3>', "index.exp.stat4"),
        ('<h3 class="title">Müştəri Məmnuniyyəti.</h3>', "index.about.item1_title"),
        ('<h3 class="title">Rəsmi Tərəfdaşlıq.</h3>', "index.about.item2_title"),
        ('<h3 class="title">100-dən Çox Layihə.</h3>', "index.about.item3_title"),
    ]
    for item in index_items:
        if isinstance(item, tuple) and len(item) == 2 and (
            item[1].startswith("<") or "data-i18n=" in item[1]
        ):
            I.append(item)
        elif isinstance(item, tuple) and len(item) == 2:
            add(item[0], item[1])
        elif isinstance(item, tuple) and len(item) == 3:
            add(item[0], item[1], html=item[2])
        else:
            I.append(item)

    # HTML content injections (index)
    html_index = [
        ('<span class="sub-title">Və <br> Eksteryer <br> Dizayn firması</span>', "index.hero.exterior_html"),
        ('<h3 class="title rr_title_anim">AA MEMARLIQ hər <br> layihəni <span>özünəməxsus sənət <br> əsərinə çevirir.</span>\n                      </h3>', "index.about.title_html"),
        ('<p class="desc-text" style="margin-top: 25px; color: #7a7a7a; font-size: 16px; line-height: 1.8; font-weight: 400;">\n                        AA MEMARLIQ Ekspo Stend Şirkəti 2019-cu ildən bəri Azərbaycanda fəaliyyət göstərir. Firmamız hər daim müştəri məmnuniyyətinə əsaslanaraq çalışır. Əhəmiyyətli sahələrimizdən biri də dekorasiya və dizayn işlərinin yerinə yetirilməsidir. Şirkətimiz Baku Expo Center ilə rəsmi müqaviləli olaraq xidmət göstərir və sərgi sektorunda 100-dən çox layihəyə öz imzasını atmışdır. Siz dəyərli müştərilərimizi ən yaxşı şəkildə tanıtmaq və bizə olan etibarınızı doğrultmaq üçün bütün komandamızla hər zaman xidmətinizdəyik.\n                      </p>', "index.about.desc"),
        ('<h2 class="title rr_title_anim">Sərgi stendləri və dizayn <br><span>sahəsində zəngin təcrübə</span>\n                    </h2>', "index.exp.title_html"),
        ('<h2 class="title rr_title_anim">2019-CU İLDƏN BƏRİ HƏR MƏQSƏDƏ UYĞUN <br>MƏKANLARIN QURULMASI\n              </h2>', "index.cta.title_html"),
        ('<h2 class="title rr_title_anim">İnsanların məkanlarla, təbiətlə və texnologiya ilə əlaqəsini yenidən formalaşdıran fərqli layihələrə diqqət yetiririk.\n                </h2>', "index.proj6.title"),
        ('<h3 class="title"><a href="/sergi-stendi-layihe">Müasir Sərgi Stendi <br> Layihəsi</a></h3>', "index.projects.p1_title_html"),
        ('<h3 class="title"><a href="/sergi-stendi-layihe">Fərdi Yaşayış Evi <br> İnteryeri</a></h3>', "index.projects.p2_title_html"),
        ('<h3 class="title"><a href="/sergi-stendi-layihe">Müasir Eksteryer <br> Və Landşaft Dizaynı</a></h3>', "index.projects.p3_title_html"),
        ('<a href="https://maps.app.goo.gl/JKwVELppRvPnjZ8c6" target="_blank">Baku Expo Center,\n                      <br>\n                      Bakı, Azərbaycan</a>', "footer.location_html"),
        ('<p class="copyright__text"><a href="/"> AA MEMARLIQ </a>© 2026. Bütün hüquqlar qorunur.</p>', "footer.copyright"),
    ]
    for old, key in html_index:
        add(old, key, html=True)

    # Service cards index (with html)
    svc_cards = [
        ('<h3 class="title"><a href="/interyer-eksteryer">İnteryer.\n                        Dizayn.\n                        İncəsənət.</a></h3>', "index.svc1_link_html"),
        ('<h2 class="title">İnteryer <span>Dizaynı</span></h2>', "index.svc1_title_html"),
        ('<h3 class="title"><a href="/interyer-eksteryer">Ekspo.\n                        Stend.\n                        Təqdimat.</a></h3>', "index.svc2_link_html"),
        ('<h2 class="title">Stend <span>Dizaynı</span></h2>', "index.svc2_title_html"),
        ('<h3 class="title"><a href="/interyer-eksteryer">Eksteryer.\n                        Memarlıq.\n                        Estetika.</a></h3>', "index.svc3_link_html"),
        ('<h2 class="title">Eksteryer <span>Dizaynı</span></h2>', "index.svc3_title_html"),
        ('<h3 class="title"><a href="/interyer-eksteryer">Landşaft.\n                        Peysaj.\n                        Yaşıllıq.</a></h3>', "index.svc4_link_html"),
        ('<h2 class="title">Landşaft <span>Dizaynı</span></h2>', "index.svc4_title_html"),
    ]
    for old, key in svc_cards:
        add(old, key, html=True)

    index_descs = [
        ('<p class="desc">Məkanın funksionallığını və estetikasını artıraraq sizin üçün rahat daxili məkanlar dizayn edirik.</p>', "index.svc1_desc"),
        ('<p class="desc">Baku Expo Center-də brendinizin ən gözəl şəkildə təqdim edilməsi üçün sərgi stendləri qururuq.</p>', "index.svc2_desc"),
        ('<p class="desc">Binaların müasir və gözəl çöl görünüşünün memarlıq standartlarına uyğun dizayn edilməsi.</p>', "index.svc3_desc"),
        ('<p class="desc">Həyətyanı sahələriniz və parklarınız üçün təbiətlə vəhdət təşkil edən peysaj dizaynı.</p>', "index.svc4_desc"),
        ('<p class="desc">Şirkətimiz hər daim müştəri məmnuniyyətinə əsaslanaraq çalışır və bizə olan güveninizi doğruldur.</p>', "index.about.item1_desc"),
        ('<p class="desc">Baku Expo Center ilə rəsmi müqavilə əsasında sərgi stendlərinin qurulması xidmətini göstəririk.</p>', "index.about.item2_desc"),
        ('<p class="desc">Sərgi stendləri və dekorasiya işləri sahəsində 100-dən çox layihəyə öz imzamızı atmışıq.</p>', "index.about.item3_desc"),
        ('<p class="desc">Komandamızla birlikdə hər bir məkana funksionallıq, estetika və yüksək keyfiyyət qatırıq.</p>', "index.exp.desc"),
        ('<p class="project-6__dec">AA MEMARLIQ olaraq dizayn etdiyimiz hər bir məkanı özünəməxsus estetika, funksionallıq və müasirlik ilə zənginləşdiririk.</p>', "index.proj6.desc"),
    ]
    for old, key in index_descs:
        add(old, key)

    index_details = [
        ('<li><img src="assets/imgs/icon/icon-10.svg" alt="icon not found"> 1 Stend</li>', "index.proj6.d1"),
        ('<li><img src="assets/imgs/icon/icon-11.svg" alt="icon not found"> 1 Sahə</li>', "index.proj6.d2"),
        ('<li><img src="assets/imgs/icon/icon-12.svg" alt="icon not found"> 150 m²</li>', "index.proj6.d3"),
        ('<li><img src="assets/imgs/icon/icon-10.svg" alt="icon not found"> 5 Otaq</li>', "index.proj6.d4"),
        ('<li><img src="assets/imgs/icon/icon-11.svg" alt="icon not found"> 2 Sanitar q.</li>', "index.proj6.d5"),
        ('<li><img src="assets/imgs/icon/icon-12.svg" alt="icon not found"> 320 m²</li>', "index.proj6.d6"),
        ('<li><img src="assets/imgs/icon/icon-10.svg" alt="icon not found"> 8 Otaq</li>', "index.proj6.d7"),
        ('<li><img src="assets/imgs/icon/icon-11.svg" alt="icon not found"> 4 Hamam</li>', "index.proj6.d8"),
        ('<li><img src="assets/imgs/icon/icon-12.svg" alt="icon not found"> 450 m²</li>', "index.proj6.d9"),
        ('<li><img src="assets/imgs/icon/icon-11.svg" alt="icon not found"> 1 Zona</li>', "index.proj6.d10"),
        ('<li><img src="assets/imgs/icon/icon-12.svg" alt="icon not found"> 120 m²</li>', "index.proj6.d11"),
    ]
    for old, key in index_details:
        add(old, key)

    I.extend(_build_page_injections())
    return I


def _build_page_injections():
    I = []

    def add(old, key, html=False):
        attr = _i(key, html=html)
        if ">" in old:
            new = old.replace(">", f" {attr}>", 1)
        else:
            new = old
        I.append((old, new))

    # about.html
    about = [
        ('<h2 class="breadcrumb__sub-title">2019-cu ildən bəri <br> Azərbaycanda sərgi və dizayn xidməti</h2>', "about.breadcrumb_sub_html", True),
        ('<h3 class="breadcrumb__title">Şirkətimiz</h3>', "about.breadcrumb_title"),
        ('<h3 class="title">AA MEMARLIQ sərgi stendləri, interyer, eksteryer və landşaft dizaynı sahəsində ən yaxşı həlləri təklif edir. Peşəkar komandamız layihələrinizin dizaynından tutmuş qurulmasına qədər olan bütün mərhələləri yüksək səviyyədə həyata keçirir.</h3>', "about.intro"),
        ('<p class="desc">“ 2019-cu ildən bəri sərgi sektorunda 100-dən çox layihəyə imza atmışıq. Müştəri məmnuniyyətini əsas tutaraq, layihələrinizi ən peşəkar şəkildə həyata keçirməyə davam edirik.</p>', "about.quote"),
        ('<span>Ekspo və Memarlıq</span>', "about.tagline"),
        ('<h3 class="title">AA MEMARLIQ müasir dizayn fəlsəfəsinə və funksionallığa önəm verən, hər bir layihənin özünəməxsusluğunu əks etdirən fərdi sərgi stendləri və memarlıq layihələri hazırlayır.</h3>', "about.side_title"),
        ('<p>Uğurlu layihələr</p>', "about.exp1"),
        ('<p>İllik təcrübə</p>', "about.exp2"),
        ('<p>Partnyorlar</p>', "about.exp3"),
        ('<p class="dedication">Memarlığa və stend dizaynına yeni nəfəs gətirərək, müştərilərimiz üçün ən müasir həlləri yaradırıq.</p>', "about.feature"),
        ('<h2 class="sub-title">MÜKAFATLARIMIZ</h2>', "about.awards_sub"),
        ('<h3 class="title">Müxtəlif sahələrdə <br> Memarlıq və Dizayn mükafatları</h3>', "about.awards_title_html", True),
        ('<h3 class="title">Uğurlu Stend Dizaynı Mükafatı <span>2023</span></h3>', "about.award1_html", True),
        ('<h3 class="title">Qızıl Stend Mükafatı <span>2020</span></h3>', "about.award2_html", True),
        ('<h3 class="title">Eksteryer və Landşaft Master Mükafatı <span>2019</span></h3>', "about.award3_html", True),
        ('<h3 class="title">İlin Ən Yaxşı Sərgi Tərəfdaşı <span>2021</span></h3>', "about.award4_html", True),
        ('<p class="dedication">2019-cu ildən bəri müasir sərgi stendləri və memarlıq sahəsində ixtisaslaşaraq müştərilərimizə peşəkar və çoxşaxəli xidmətlər təqdim edirik.</p>', "about.awards_desc"),
    ]
    for item in about:
        add(*item)

    # contact.html
    contact = [
        ('<h2 class="page-sub-title">Bizimlə əlaqə</h2>', "contact.page_sub"),
        ('<h3 class="page-title"> Bizə yazın və <br>\n                                    layihənizi dərhal <br> başladaq.</h3>', "contact.page_title_html", True),
        ('<p class="title">Əlaqə saxlayın</p>', "contact.reach_title"),
        ('<p class="text">Sizinlə işləməkdən və birlikdə möhtəşəm bir layihə ərsəyə gətirməkdən məmnun olarıq. <br>', "contact.reach_text_html", True),
        ('<p class="title">İzləyin</p>', "contact.follow"),
        ('<h2 class="sub-title">Departamentlərimiz:</h2>', "contact.dept_title"),
        ('<h3 class="title">Baş Ofis (Ekspo Mərkəzi)</h3>', "contact.dept1"),
        ('<h3 class="title">Dizayn Departamenti</h3>', "contact.dept2"),
        ('<h3 class="title">İstehsalat və Quraşdırma</h3>', "contact.dept3"),
        ('<p>Baku Expo Center, <br>\n                                    Bakı, Azərbaycan</p>', "footer.location_html2", True),
    ]
    for item in contact:
        add(*item)

    # faq.html
    faq = [
        ('<h2 class="page-sub-title">Ağlınızdakı sualların <br>\n                                    cavablarını tapın</h2>', "faq.page_sub_html", True),
        ('<h3 class="page-title">Tez-Tez Verilən <br>\n                                    Suallar</h3>', "faq.page_title_html", True),
        ('<h2 class="sub-title">FAQ</h2>', "faq.sidebar_sub"),
        ('<h3 class="title">Sualların cavabı yoxdur? Xüsusi cavablar əldə edin</h3>', "faq.sidebar_title"),
    ]
    for item in faq:
        add(*item)
    for n in range(1, 10):
        az_q = TRANSLATIONS[f"faq.q{n}"]["az"]
        az_a = TRANSLATIONS[f"faq.a{n}"]["az"]
        I.append((
            f'                                                {az_q}\n                                            </button>',
            f'                                                <span data-i18n="faq.q{n}">{az_q}</span>\n                                            </button>',
        ))
        I.append((
            f'                                            <div class="accordion-body">\n                                                {az_a}\n                                            </div>',
            f'                                            <div class="accordion-body" data-i18n="faq.a{n}">\n                                                {az_a}\n                                            </div>',
        ))

    # services page
    services = [
        ('<h2 class="breadcrumb__sub-title">Şirkətimiz tərəfindən təqdim olunan <br> peşəkar memarlıq və dizayn xidmətləri</h2>', "services.breadcrumb_sub_html", True),
        ('<h2 class="breadcrumb__title">Xidmətlərimiz</h2>', "services.breadcrumb_title"),
        ('<h2 class="subtitle">[ Xidmətlərimiz ]</h2>', "services.section_tag"),
        ('<h3 class="our-service-9__title"><a href="/interyer-eksteryer">İnteryer və Eksteryer</a></h3>', "services.s1_title"),
        ('<h3 class="our-service-9__title"><a\n                                                    href="/memarliq-layiheleri">Memarlıq Layihələri</a></h3>', "services.s2_title"),
        ('<h3 class="our-service-9__title"><a\n                                                    href="/sergi-stendleri">Sərgi Stendləri</a></h3>', "services.s3_title"),
        ('<h3 class="our-service-9__title"><a\n                                                    href="/layihe-idareetmesi">Layihə İdarəetməsi</a></h3>', "services.s4_title"),
        ('<a href="/elaqe" class="underline">Bizimlə Əlaqə Saxlayın</a>', "btn.contact_us"),
        ('<p class="our-service-9__desc">\n                                                Müştərilərimizin istəklərinə uyğun fərdi dizayn edilmiş interyer və eksteryer layihələrimiz, layihənin yerindən, həcmindən və büdcəsindən asılı olmayaraq bütün tələblərə cavab verir.\n                                            </p>', "services.s1_desc"),
        ('<p class="our-service-9__desc">\n                                                AA MEMARLIQ olaraq dizayn və memarlıq sahəsindəki zəngin təcrübəmizlə layihələrinizin həm estetik cəhətdən gözəl, həm də struktur cəhətdən davamlı olmasını təmin edirik.\n                                            </p>', "services.s2_desc"),
        ('<p class="our-service-9__desc">\n                                                Yerli və beynəlxalq səviyyəli müştərilərimiz üçün Baku Expo Center və digər məkanlarda sərgi stendlərinin dizaynı və peşəkar quraşdırılması xidmətini təklif edirik.\n                                            </p>', "services.s3_desc"),
        ('<p class="our-service-9__desc">\n                                                Layihəni ilk eskizdən açar təhvil verilməsinə qədər bütün mərhələlərdə peşəkar planlaşdırma, koordinasiya və keyfiyyət nəzarəti xidməti göstəririk.\n                                            </p>', "services.s4_desc"),
    ]
    for item in services:
        add(*item)

    # Service detail + portfolio shared info values
    info_vals = [
        ('<h5 class="title">Fərdi sifariş</h5>', "val.individual"),
        ('<h5 class="title">Kommersiya sifarişi</h5>', "val.commercial"),
        ('<h5 class="title">Korporativ sifariş</h5>', "val.corporate"),
        ('<h6 class="title">İnteryer və eksteryer</h6>', "val.interior_exterior"),
        ('<h6 class="title">Memarlıq layihəsi</h6>', "val.arch_project"),
        ('<h6 class="title">Sərgi stendi</h6>', "val.exhibition"),
        ('<h6 class="title">Layihə idarəetməsi</h6>', "val.pm"),
        ('<h6 class="title">Yaşayış və kommersiya</h6>', "val.residential"),
        ('<h6 class="title">Kommersiya məkanı</h6>', "val.commercial_space"),
        ('<h6 class="title">Korporativ ofis</h6>', "val.corporate_office"),
        ('<h6 class="title">Showroom interyeri</h6>', "val.showroom_interior"),
        ('<h6 class="title">Showroom məkanı</h6>', "val.showroom_space"),
        ('<h6 class="title">Yasayis evi interyeri</h6>', "val.home_interior"),
        ('<h6 class="title">Fərdi yasayış evi</h6>', "val.home_space"),
        ('<h6 class="title">Ofis interyeri</h6>', "val.office_interior"),
        ('<h6 class="title">Ofis məkanı</h6>', "val.office_space"),
        ('<h6 class="title">Bakı, Azərbaycan</h6>', "info.baku"),
        ('<h6 class="title">Tamamlandı</h6>', "info.completed"),
    ]
    for old, key in info_vals:
        add(old, key)

    # Page-specific titles and content
    pages = [
        ('<h2 class="page-title">İnteryer və Eksteryer</h2>', "svc.interyer.page_title"),
        ('<h2 class="page-title">Memarlıq Layihələri</h2>', "svc.memarliq.page_title"),
        ('<h2 class="page-title">Sərgi Stendləri</h2>', "svc.sergi.page_title"),
        ('<h2 class="page-title">Layihə İdarəetməsi</h2>', "svc.pm.page_title"),
        ('<h2 class="page-title">Premium Showroom <br>                                    Interyeri</h2>', "port.showroom.page_title_html", True),
        ('<h2 class="page-title">F?rdi Yasayis Evi <br>\n                                    Interyeri</h2>', "port.home.page_title_html", True),
        ('<h2 class="page-title">Müasir Ofis <br>\n                                    Interyeri</h2>', "port.ofis.page_title_html", True),
        ('<h2 class="page-title">Sərgi <br>\n                                    Stendləri</h2>', "port.sergi.page_title_html", True),
    ]
    for item in pages:
        add(*item)

    html_pages = [
        ('<h3 class="title">Müştərilərimizin ehtiyaclarına uyğun hazırlanmış interyer və eksteryer layihələri. <span>Funksionallıq, estetika və rahatlıq</span> prinsipləri əsasında hər bir məkan harmonik şəkildə dizayn edilib.</h3>', "svc.interyer.hero_html"),
        ('<h3 class="title">Kommersiya və nümayiş məkanları üçün hazırlanmış <span>memarlıq və interyer layihələri</span>. Estetik, funksional və müasir dizayn prinsipləri əsasında.</h3>', "svc.memarliq.hero_html"),
        ('<h3 class="title">Baku Expo Center və digər sərgi məkanları üçün hazırlanmış <span>funksional, estetik və brendə uyğun</span> sərgi stendi layihələri.</h3>', "svc.sergi.hero_html"),
        ('<h3 class="title">Korporativ ofis layihələrində <span>planlaşdırma, koordinasiya və keyfiyyət nəzarəti</span> prinsiplərinə uyğun peşəkar layihə idarəetməsi.</h3>', "svc.pm.hero_html"),
        ('<h3 class="title">Müasir showroom mühitində <span>funksionallıq, rahatlıq və peşəkar görünüş</span> prinsiplərinə uyğun hazırlanmış interyer layihəsi.</h3>', "port.showroom.hero_html"),
        ('<h3 class="title">Müştərinin ehtiyaclarına uygun hazirlanmis fərdi yaşayış evi interyeri layihəsi. <span>Funksionallıq, estetika və rahatlıq</span> prinsipləri əsasında hər bir otaq harmonik şəkildə dizayn edilib.</h3>', "port.home.hero_html"),
        ('<h3 class="title">Müasir ofis mühitində <span>funksionallıq, rahatlıq və peşəkar görünüş</span> prinsiplərinə uyğun hazırlanmış interyer layihəsi.</h3>', "port.ofis.hero_html"),
    ]
    for old, key in html_pages:
        add(old, key, True)

    # Overview paragraphs - add by matching unique start
    text_blocks = [
        ("svc.interyer.ov1", "Yaşayış və kommersiya məkanları üçün daxili və xarici interyer həlləri hazırlayırıq."),
        ("svc.interyer.ov2", "Fərdi yaşayış evlərindən tutmuş kommersiya məkanlarına qədər bütün interyer layihələrində vahid estetik dil və yüksək keyfiyyət standartları qorunur."),
        ("svc.memarliq.ov1", "AA MEMARLIQ olaraq dizayn və memarlıq sahəsindəki zəngin təcrübəmizlə layihələrinizin həm estetik cəhətdən gözəl, həm də struktur cəhətdən davamlı olmasını təmin edirik."),
        ("svc.memarliq.ov2", "Showroom və kommersiya məkanlarında vahid dizayn dili, peşəkar planlaşdırma və yüksək keyfiyyətli icra ilə fərqlənirik."),
        ("svc.sergi.ov1", "Yerli və beynəlxalq səviyyəli müştərilərimiz üçün Baku Expo Center və digər məkanlarda sərgi stendlərinin dizaynı və peşəkar quraşdırılması xidmətini təklif edirik."),
        ("svc.sergi.ov2", "Stend quruluşu, işıqlandırma, material seçimi və brendinq zonalarının planlaşdırılması müasir sərgi stendi dizayn prinsiplərinə uyğun həyata keçirilir."),
        ("svc.pm.ov1", "Layihəni ilk eskizdən açar təhvil verilməsinə qədər bütün mərhələlərdə peşəkar şəkildə idarə edirik. Korporativ ofis layihələrində vaxt, büdcə və keyfiyyət balansını qoruyuruq."),
        ("svc.pm.ov2", "Hər müştəriyə xüsusi layihə meneceri təyin olunur — bütün mərhələlər üzrə hesabatlar və yeniliklər müntəzəm təqdim edilir."),
        ("port.showroom.ov1", "Bu layihədə Showroom məkanının iş prosesinə uyğun planlaşdırılması"),
        ("port.showroom.ov2", "Qəbul, nümayiş və satış sahələrində vahid dizayn dili qorunub"),
        ("port.home.ov1", "Bu layihədə yaşayış məkanının gündəlik istifadə rahatlığı"),
        ("port.home.ov2", "Hər bir otaq müştərinin həyat tərzinə uyğun fərdi yanaşma ilə dizayn edilib"),
        ("port.ofis.ov1", "Bu layihədə ofis məkanının iş prosesinə uyğun planlaşdırılması"),
        ("port.ofis.ov2", "Qəbul, iş otaqları və ümumi istifadə sahələrində vahid dizayn dili qorunub"),
        ("port.sergi.ov1", "Bu layihədə stend quruluşu, işıqlandırma, material seçimi"),
        ("port.sergi.ov2", "Quruluş, nümayiş və qarşılama sahələrində vahid dizayn dili qorunub"),
    ]
    for key, snippet in text_blocks:
        az = TRANSLATIONS[key]["az"]
        I.append((f'<p>{az}</p>', f'<p {_i(key)}>{az}</p>'))

    # Work scope list items
    for prefix in ("svc.interyer", "svc.memarliq", "svc.sergi", "svc.pm", "port.showroom", "port.home", "port.ofis", "port.sergi"):
        for n in range(1, 5):
            key = f"{prefix}.w{n}"
            az = TRANSLATIONS[key]["az"]
            I.append((f'<li>{az}</li>', f'<li {_i(key)}>{az}</li>'))

    # Footer location blocks
    I.append((
        '<p>Baku Expo Center, <br>\n                                        Bakı, Azərbaycan\n                                    </p>',
        f'<p {_i("footer.location_html2", html=True)}>Baku Expo Center, <br>\n                                        Bakı, Azərbaycan\n                                    </p>',
    ))

    return I


INJECTIONS = _build_injections()


def write_translations_js():
    az = {k: v["az"] for k, v in TRANSLATIONS.items()}
    tr = {k: v["tr"] for k, v in TRANSLATIONS.items()}
    content = "window.AA_I18N = " + json.dumps({"az": az, "tr": tr}, ensure_ascii=False, indent=2) + ";\n"
    TRANSLATIONS_JS.parent.mkdir(parents=True, exist_ok=True)
    TRANSLATIONS_JS.write_text(content, encoding="utf-8")


def patch_body_tag(html, page_key):
    if 'data-page="' in html:
        html = re.sub(r'data-page="[^"]*"', f'data-page="{page_key}"', html, count=1)
        return html
    if re.search(r"<body[^>]*class=", html):
        return re.sub(r"<body(\s+class=\"[^\"]*\")", rf'<body\1 data-page="{page_key}"', html, count=1)
    return re.sub(r"<body>", f'<body data-page="{page_key}">', html, count=1)


def inject_lang_switcher(html, filename):
    if 'class="lang-switcher"' in html:
        return html
    html = html.replace(
        '<div class="header__navicon">',
        LANG_SWITCHER + "\n                " + '<div class="header__navicon">',
        1,
    )
    if filename == "index.html" and 'side-info-4' in html:
        marker = (
            '<h6>Baku Expo Center ilə rəsmi müqaviləli olaraq fəaliyyət göstərən peşəkar ekspo stend və memarlıq şirkəti.</h6>'
        )
        if marker in html:
            html = html.replace(
                marker,
                marker + "\n            " + LANG_SWITCHER,
                1,
            )
        elif 'data-i18n="sidebar.tagline"' in html:
            html = html.replace(
                'data-i18n="sidebar.tagline">',
                'data-i18n="sidebar.tagline">' ,
            )
            html = html.replace(
                '</h6>\n            <span class="date"',
                '</h6>\n            ' + LANG_SWITCHER + '\n            <span class="date"',
                1,
            )
    return html


def inject_scripts(html):
    marker = '<script src="assets/vandor/common-js/common.js"></script>'
    if "assets/js/translations.js" in html:
        return html
    return html.replace(marker, I18N_SCRIPTS + "  " + marker, 1)


def apply_injections(html):
    for old, new in INJECTIONS:
        if old in html and new not in html:
            html = html.replace(old, new)
    return html


def patch_html_file(path, page_key):
    html = path.read_text(encoding="utf-8")
    html = re.sub(r'<html lang="[^"]*">', '<html lang="az">', html, count=1)
    html = patch_body_tag(html, page_key)
    html = inject_lang_switcher(html, path.name)
    html = apply_injections(html)
    html = inject_scripts(html)
    path.write_text(html, encoding="utf-8")


def main():
    write_translations_js()
    patched = []
    for filename, page_key in PAGE_MAP.items():
        fpath = ROOT / filename
        if fpath.exists():
            patch_html_file(fpath, page_key)
            patched.append(filename)
    print(f"Translation keys: {len(TRANSLATIONS)}")
    print(f"Injection rules: {len(INJECTIONS)}")
    print(f"Files patched: {len(patched)}")
    for f in patched:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
