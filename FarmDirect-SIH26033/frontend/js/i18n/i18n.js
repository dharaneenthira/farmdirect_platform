/**
 * FarmDirect i18n Engine
 * Handles dynamic language selection, localStorage persistence, and DOM updates.
 */
class I18nEngine {
  constructor() {
    this.STORAGE_KEY = 'farmdirect_lang';
    this.DEFAULT_LANG = 'en';
    this.currentLang = localStorage.getItem(this.STORAGE_KEY) || this.DEFAULT_LANG;
    this.translations = typeof translations !== 'undefined' ? translations : {};
  }

  /**
   * Initialize i18n engine on page load
   */
  init() {
    this.setLanguage(this.currentLang);
    this.bindEvents();
  }

  /**
   * Set active language, update storage, and re-render DOM
   * @param {string} lang - 'en' | 'ta'
   */
  setLanguage(lang) {
    if (!this.translations[lang]) {
      console.warn(`Language '${lang}' not found in translations. Falling back to '${this.DEFAULT_LANG}'.`);
      lang = this.DEFAULT_LANG;
    }

    this.currentLang = lang;
    localStorage.setItem(this.STORAGE_KEY, lang);
    document.documentElement.lang = lang;

    this.updateDOM();

    // Sync select dropdown if present
    const langSelect = document.getElementById('languageSelect');
    if (langSelect && langSelect.value !== lang) {
      langSelect.value = lang;
    }

    // Dispatch custom event for dynamically rendered components
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
  }

  /**
   * Translate a given key
   * @param {string} key 
   * @returns {string} Translated string or key if missing
   */
  t(key) {
    const langDict = this.translations[this.currentLang] || this.translations[this.DEFAULT_LANG];
    return langDict[key] || (this.translations[this.DEFAULT_LANG] ? this.translations[this.DEFAULT_LANG][key] : key) || key;
  }

  /**
   * Scans DOM for data-i18n attributes and updates text content / attributes
   */
  updateDOM() {
    // Update elements with text content keys
    document.querySelectorAll('[data-i18n]').forEach((element) => {
      const key = element.getAttribute('data-i18n');
      const translation = this.t(key);
      if (translation) {
        element.textContent = translation;
      }
    });

    // Update input placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
      const key = element.getAttribute('data-i18n-placeholder');
      const translation = this.t(key);
      if (translation) {
        element.setAttribute('placeholder', translation);
      }
    });
  }

  /**
   * Bind event listeners for UI language controls
   */
  bindEvents() {
    const langSelect = document.getElementById('languageSelect');
    if (langSelect) {
      langSelect.addEventListener('change', (e) => {
        this.setLanguage(e.target.value);
      });
    }
  }
}

// Global Singleton Instance
const i18n = new I18nEngine();
document.addEventListener('DOMContentLoaded', () => i18n.init());
