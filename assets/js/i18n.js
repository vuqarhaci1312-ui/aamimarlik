(function () {
    "use strict";

    var STORAGE_KEY = "aa_lang";
    var BRAND = "AA MEMARLIQ";
    var LOCALES = ["az", "tr", "en", "ru"];

    var AZ_TO_TR_PATH = {
        "/": "/",
        "/haqqimizda": "/hakkimizda",
        "/xidmetlerimiz": "/hizmetlerimiz",
        "/interyer-eksteryer": "/ic-dis-mekan",
        "/memarliq-layiheleri": "/mimarlik-projeleri",
        "/sergi-stendleri": "/fuar-standlari",
        "/layihe-idareetmesi": "/proje-yonetimi",
        "/faq": "/sss",
        "/elaqe": "/iletisim",
        "/premium-showroom": "/premium-showroom",
        "/ferdi-yasayis-evi": "/ozel-konut",
        "/muasir-ofis": "/modern-ofis",
        "/sergi-stendi-layihe": "/fuar-standi-projesi"
    };

    var AZ_TO_EN_PATH = {
        "/": "/",
        "/haqqimizda": "/about-us",
        "/xidmetlerimiz": "/services",
        "/interyer-eksteryer": "/interior-exterior",
        "/memarliq-layiheleri": "/architecture-projects",
        "/sergi-stendleri": "/exhibition-stands",
        "/layihe-idareetmesi": "/project-management",
        "/faq": "/faq",
        "/elaqe": "/contact",
        "/premium-showroom": "/premium-showroom",
        "/ferdi-yasayis-evi": "/private-residence",
        "/muasir-ofis": "/modern-office",
        "/sergi-stendi-layihe": "/exhibition-stand-project"
    };

    var AZ_TO_RU_PATH = {
        "/": "/",
        "/haqqimizda": "/o-nas",
        "/xidmetlerimiz": "/uslugi",
        "/interyer-eksteryer": "/interer-eksterer",
        "/memarliq-layiheleri": "/arhitekturnye-proekty",
        "/sergi-stendleri": "/vystavochnye-stendy",
        "/layihe-idareetmesi": "/upravlenie-proektami",
        "/faq": "/voprosy-otvety",
        "/elaqe": "/kontakty",
        "/premium-showroom": "/premium-showroom",
        "/ferdi-yasayis-evi": "/chastnyy-dom",
        "/muasir-ofis": "/sovremennyy-ofis",
        "/sergi-stendi-layihe": "/proekt-vystavochnogo-stenda"
    };

    var LOCALE_PATH = {
        tr: AZ_TO_TR_PATH,
        en: AZ_TO_EN_PATH,
        ru: AZ_TO_RU_PATH
    };

    var AZ_TO_TR_HASH = { "#layiheler": "#projeler" };
    var AZ_TO_EN_HASH = { "#layiheler": "#projects" };
    var AZ_TO_RU_HASH = { "#layiheler": "#proekty" };

    var LOCALE_HASH = {
        tr: AZ_TO_TR_HASH,
        en: AZ_TO_EN_HASH,
        ru: AZ_TO_RU_HASH
    };

    var PATH_TO_AZ = { "/": "/" };
    var HASH_TO_AZ = { "": "", "#layiheler": "#layiheler" };

    Object.keys(AZ_TO_TR_PATH).forEach(function (az) {
        PATH_TO_AZ[AZ_TO_TR_PATH[az]] = az;
    });
    Object.keys(AZ_TO_EN_PATH).forEach(function (az) {
        PATH_TO_AZ[AZ_TO_EN_PATH[az]] = az;
    });
    Object.keys(AZ_TO_RU_PATH).forEach(function (az) {
        PATH_TO_AZ[AZ_TO_RU_PATH[az]] = az;
    });
    Object.keys(AZ_TO_TR_HASH).forEach(function (az) {
        HASH_TO_AZ[AZ_TO_TR_HASH[az]] = az;
    });
    Object.keys(AZ_TO_EN_HASH).forEach(function (az) {
        HASH_TO_AZ[AZ_TO_EN_HASH[az]] = az;
    });
    Object.keys(AZ_TO_RU_HASH).forEach(function (az) {
        HASH_TO_AZ[AZ_TO_RU_HASH[az]] = az;
    });

    var PAGE_KEY_BY_PATH = {
        "/": "index",
        "/ana-sehife": "index",
        "/haqqimizda": "about",
        "/hakkimizda": "about",
        "/about-us": "about",
        "/xidmetlerimiz": "services",
        "/hizmetlerimiz": "services",
        "/services": "services",
        "/interyer-eksteryer": "svc_interyer",
        "/ic-dis-mekan": "svc_interyer",
        "/interior-exterior": "svc_interyer",
        "/memarliq-layiheleri": "svc_memarliq",
        "/mimarlik-projeleri": "svc_memarliq",
        "/architecture-projects": "svc_memarliq",
        "/sergi-stendleri": "svc_sergi",
        "/fuar-standlari": "svc_sergi",
        "/exhibition-stands": "svc_sergi",
        "/layihe-idareetmesi": "svc_pm",
        "/proje-yonetimi": "svc_pm",
        "/project-management": "svc_pm",
        "/faq": "faq",
        "/sss": "faq",
        "/elaqe": "contact",
        "/iletisim": "contact",
        "/contact": "contact",
        "/premium-showroom": "port_showroom",
        "/ferdi-yasayis-evi": "port_home",
        "/ozel-konut": "port_home",
        "/private-residence": "port_home",
        "/muasir-ofis": "port_ofis",
        "/modern-ofis": "port_ofis",
        "/modern-office": "port_ofis",
        "/sergi-stendi-layihe": "port_sergi",
        "/fuar-standi-projesi": "port_sergi",
        "/exhibition-stand-project": "port_sergi",
        "/o-nas": "about",
        "/uslugi": "services",
        "/interer-eksterer": "svc_interyer",
        "/arhitekturnye-proekty": "svc_memarliq",
        "/vystavochnye-stendy": "svc_sergi",
        "/upravlenie-proektami": "svc_pm",
        "/voprosy-otvety": "faq",
        "/kontakty": "contact",
        "/chastnyy-dom": "port_home",
        "/sovremennyy-ofis": "port_ofis",
        "/proekt-vystavochnogo-stenda": "port_sergi"
    };

    var ANCHOR_BY_LANG = {
        az: "layiheler",
        tr: "projeler",
        en: "projects",
        ru: "proekty"
    };

    function getLang() {
        var lang = localStorage.getItem(STORAGE_KEY) || "az";
        return LOCALES.indexOf(lang) !== -1 ? lang : "az";
    }

    function normalizePath(path) {
        if (!path || path === "/") return "/";
        return path.replace(/\/$/, "") || "/";
    }

    function splitHref(href) {
        var hash = "";
        var path = href;
        var hashIndex = href.indexOf("#");
        if (hashIndex !== -1) {
            path = href.slice(0, hashIndex) || "/";
            hash = href.slice(hashIndex);
        }
        return { path: normalizePath(path), hash: hash };
    }

    function toAzHref(href) {
        var parts = splitHref(href);
        var azPath = PATH_TO_AZ[parts.path] || parts.path;
        var azHash = HASH_TO_AZ[parts.hash] || parts.hash;
        return azPath + azHash;
    }

    function localizeHref(href, lang) {
        if (!href || href.charAt(0) !== "/") return href;

        var parts = splitHref(toAzHref(href));

        if (lang === "az") {
            return parts.path + parts.hash;
        }

        var pathMap = LOCALE_PATH[lang];
        var hashMap = LOCALE_HASH[lang];
        if (!pathMap) return parts.path + parts.hash;
        var localizedPath = pathMap[parts.path] || parts.path;
        var localizedHash = hashMap[parts.hash] || parts.hash;
        return localizedPath + localizedHash;
    }

    function getPageKey() {
        var page = document.body.getAttribute("data-page");
        if (page) return page;
        var path = normalizePath(window.location.pathname);
        return PAGE_KEY_BY_PATH[path] || "index";
    }

    function syncUrlWithLang() {
        var lang = getLang();
        var current = normalizePath(window.location.pathname) + (window.location.hash || "");
        var expected = localizeHref(current, lang);
        if (expected !== current) {
            window.location.replace(expected + window.location.search);
        }
    }

    function applyAnchorId(lang) {
        var section =
            document.getElementById("layiheler") ||
            document.getElementById("projeler") ||
            document.getElementById("projects") ||
            document.getElementById("proekty");
        if (!section) return;
        section.id = ANCHOR_BY_LANG[lang] || "layiheler";
    }

    function applyLocalizedUrls(lang) {
        document.querySelectorAll("a[href]").forEach(function (a) {
            var href = a.getAttribute("href");
            if (!href || href.charAt(0) !== "/" || href.indexOf("//") === 0) return;

            if (!a.hasAttribute("data-aa-href-az")) {
                a.setAttribute("data-aa-href-az", toAzHref(href));
            }

            var azHref = a.getAttribute("data-aa-href-az");
            a.setAttribute("href", localizeHref(azHref, lang));
        });
    }

    function t(key, lang) {
        lang = lang || getLang();
        var dict = window.AA_I18N && window.AA_I18N[lang];
        if (!dict) return null;
        if (dict[key] !== undefined) return dict[key];
        var shared = window.AA_I18N.shared && window.AA_I18N.shared[lang];
        if (shared && shared[key] !== undefined) return shared[key];
        return null;
    }

    function formatHtmlValue(value) {
        return value.replace(/\r\n/g, "\n").replace(/\n\s*/g, "<br>");
    }

    function applyHtmlTranslation(el, value, lang) {
        var html = formatHtmlValue(value);

        if (/<a[\s>]/i.test(html)) {
            el.innerHTML = html;
            applyLocalizedUrls(lang);
            return;
        }

        var directLink = el.querySelector(":scope > a");

        if (directLink && el.children.length === 1 && el.children[0] === directLink) {
            var attrs = ' href="' + directLink.getAttribute("href") + '"';
            if (directLink.getAttribute("target")) {
                attrs += ' target="' + directLink.getAttribute("target") + '"';
            }
            if (directLink.getAttribute("rel")) {
                attrs += ' rel="' + directLink.getAttribute("rel") + '"';
            }
            el.innerHTML = "<a" + attrs + ">" + html + "</a>";
            return;
        }

        var extraLinks = [];
        el.querySelectorAll(":scope > a").forEach(function (a) {
            extraLinks.push(a.cloneNode(true));
        });
        el.innerHTML = html;
        extraLinks.forEach(function (a) {
            el.appendChild(document.createElement("br"));
            el.appendChild(a);
        });
    }

    function applyToElement(el, lang) {
        var key = el.getAttribute("data-i18n");
        if (!key) return;
        var value = t(key, lang);
        if (value === null) return;

        if (el.hasAttribute("data-i18n-html")) {
            applyHtmlTranslation(el, value, lang);
            return;
        }

        var link = el.querySelector(":scope > a");
        if (link && el.children.length === 1) {
            link.textContent = value;
            return;
        }

        if (el.querySelector("img, svg, i, cite")) {
            var updated = false;
            el.childNodes.forEach(function (node) {
                if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                    node.textContent = " " + value.trim();
                    updated = true;
                }
            });
            if (!updated) {
                el.appendChild(document.createTextNode(" " + value));
            }
            return;
        }

        el.textContent = value;
    }

    function applyPlaceholders(lang) {
        document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
            var value = t(el.getAttribute("data-i18n-placeholder"), lang);
            if (value !== null) el.setAttribute("placeholder", value);
        });
    }

    function applySelectOptions(lang) {
        document.querySelectorAll("option[data-i18n]").forEach(function (el) {
            applyToElement(el, lang);
        });
    }

    function applyDataText(lang) {
        document.querySelectorAll("[data-text]").forEach(function (el) {
            var inner = el.querySelector("[data-i18n]");
            if (!inner) return;
            var value = t(inner.getAttribute("data-i18n"), lang);
            if (value !== null) el.setAttribute("data-text", value);
        });
    }

    function applyAriaLabels(lang) {
        var label = t("shared.lang_label", lang);
        if (!label) return;
        document.querySelectorAll(".lang-switcher").forEach(function (el) {
            el.setAttribute("aria-label", label);
        });
    }

    function applyMeta(lang) {
        var page = getPageKey();
        var titleKey = page + ".title";
        var descKey = page + ".meta_description";
        var title = t(titleKey, lang);
        var desc = t(descKey, lang);
        if (title) document.title = title + " - " + BRAND;
        var meta = document.querySelector('meta[name="description"]');
        if (meta && desc) meta.setAttribute("content", BRAND + " - " + desc);
        document.documentElement.lang = lang;
    }

    function updateSwitcher(lang) {
        document.querySelectorAll(".lang-switcher__btn").forEach(function (btn) {
            btn.classList.toggle("is-active", btn.getAttribute("data-lang") === lang);
        });
    }

    function applyLanguage(lang) {
        if (!window.AA_I18N) return;

        updateSwitcher(lang);

        if (lang === "az") {
            document.documentElement.lang = "az";
            applyAnchorId("az");
            applyLocalizedUrls("az");
            return;
        }

        applyMeta(lang);
        applyAriaLabels(lang);
        document.querySelectorAll("[data-i18n]").forEach(function (el) {
            applyToElement(el, lang);
        });
        applyPlaceholders(lang);
        applySelectOptions(lang);
        applyDataText(lang);
        applyAnchorId(lang);
        applyLocalizedUrls(lang);
    }

    function setLanguage(lang) {
        if (LOCALES.indexOf(lang) === -1) return;
        if (lang === getLang()) return;
        localStorage.setItem(STORAGE_KEY, lang);
        var target = localizeHref(
            normalizePath(window.location.pathname) + (window.location.hash || ""),
            lang
        );
        window.location.href = target + window.location.search;
    }

    function bindSwitcher() {
        document.querySelectorAll(".lang-switcher__btn").forEach(function (btn) {
            btn.addEventListener("click", function () {
                setLanguage(btn.getAttribute("data-lang"));
            });
        });
    }

    syncUrlWithLang();
    bindSwitcher();
    applyLanguage(getLang());

    window.AA_setLanguage = setLanguage;
    window.AA_getLanguage = getLang;
})();
