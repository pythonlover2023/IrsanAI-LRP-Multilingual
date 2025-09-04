/**
 * IrsanAI-LRP Internationalization Engine
 * Handles language detection, loading, and text translation
 */

class I18nEngine {
    constructor() {
        this.currentLanguage = 'de';
        this.fallbackLanguage = 'de';
        this.translations = {};
        this.supportedLanguages = ['de', 'en', 'es', 'fr', 'it', 'zh-cn'];
        this.languageNames = {
            'de': 'Deutsch',
            'en': 'English',
            'es': 'Español',
            'fr': 'Français',
            'it': 'Italiano',
            'zh-cn': '中文'
        };
        this.observers = [];
        this.loadingPromises = {};
        
        this.init();
    }

    /**
     * Initialize the i18n engine
     */
    async init() {
        // Detect browser language
        const detectedLanguage = this.detectBrowserLanguage();
        
        // Check for stored language preference
        const storedLanguage = localStorage.getItem('irsanai-language');
        
        // Determine initial language
        const initialLanguage = storedLanguage || detectedLanguage || this.fallbackLanguage;
        
        // Load and set initial language
        await this.setLanguage(initialLanguage);
        
        // Initialize language selector
        this.initLanguageSelector();
    }

    /**
     * Detect browser language
     */
    detectBrowserLanguage() {
        const browserLang = navigator.language || navigator.userLanguage;
        const langCode = browserLang.toLowerCase();
        
        // Check for exact match
        if (this.supportedLanguages.includes(langCode)) {
            return langCode;
        }
        
        // Check for language family match (e.g., 'en-US' -> 'en')
        const langFamily = langCode.split('-')[0];
        if (this.supportedLanguages.includes(langFamily)) {
            return langFamily;
        }
        
        // Check for Chinese variants
        if (langCode.startsWith('zh')) {
            return 'zh-cn';
        }
        
        return null;
    }

    /**
     * Load language file
     */
    async loadLanguage(language) {
        if (this.translations[language]) {
            return this.translations[language];
        }

        // Prevent multiple simultaneous loads of the same language
        if (this.loadingPromises[language]) {
            return this.loadingPromises[language];
        }

        this.loadingPromises[language] = this.fetchLanguageFile(language);
        
        try {
            const translations = await this.loadingPromises[language];
            this.translations[language] = translations;
            delete this.loadingPromises[language];
            return translations;
        } catch (error) {
            delete this.loadingPromises[language];
            console.error(`Failed to load language ${language}:`, error);
            
            // Fallback to default language if not already trying it
            if (language !== this.fallbackLanguage) {
                return this.loadLanguage(this.fallbackLanguage);
            }
            
            throw error;
        }
    }

    /**
     * Fetch language file from server
     */
    async fetchLanguageFile(language) {
        const response = await fetch(`locales/${language}.json`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return response.json();
    }

    /**
     * Set current language
     */
    async setLanguage(language) {
        if (!this.supportedLanguages.includes(language)) {
            console.warn(`Unsupported language: ${language}. Falling back to ${this.fallbackLanguage}`);
            language = this.fallbackLanguage;
        }

        try {
            await this.loadLanguage(language);
            this.currentLanguage = language;
            
            // Store language preference
            localStorage.setItem('irsanai-language', language);
            
            // Update document language
            document.documentElement.lang = language;
            
            // Update page title
            document.title = this.t('ui.title');
            
            // Notify observers
            this.notifyObservers();
            
            // Update language selector
            this.updateLanguageSelector();
            
        } catch (error) {
            console.error(`Failed to set language to ${language}:`, error);
            
            // If we failed to load the requested language and it's not the fallback,
            // try the fallback language
            if (language !== this.fallbackLanguage) {
                await this.setLanguage(this.fallbackLanguage);
            }
        }
    }

    /**
     * Get translated text
     */
    t(key, params = {}) {
        const translation = this.getNestedValue(this.translations[this.currentLanguage], key);
        
        if (translation === undefined) {
            // Try fallback language
            const fallbackTranslation = this.getNestedValue(this.translations[this.fallbackLanguage], key);
            
            if (fallbackTranslation === undefined) {
                console.warn(`Translation missing for key: ${key}`);
                return key; // Return the key as fallback
            }
            
            return this.interpolate(fallbackTranslation, params);
        }
        
        return this.interpolate(translation, params);
    }

    /**
     * Get nested object value by dot notation
     */
    getNestedValue(obj, path) {
        if (!obj) return undefined;
        
        return path.split('.').reduce((current, key) => {
            return current && current[key] !== undefined ? current[key] : undefined;
        }, obj);
    }

    /**
     * Interpolate parameters into translation string
     */
    interpolate(text, params) {
        if (typeof text !== 'string') {
            return text;
        }
        
        return text.replace(/\{(\w+)\}/g, (match, key) => {
            return params[key] !== undefined ? params[key] : match;
        });
    }

    /**
     * Get current language metadata
     */
    getCurrentLanguageMeta() {
        const translations = this.translations[this.currentLanguage];
        return translations ? translations.meta : null;
    }

    /**
     * Subscribe to language changes
     */
    subscribe(callback) {
        this.observers.push(callback);
        
        // Return unsubscribe function
        return () => {
            const index = this.observers.indexOf(callback);
            if (index > -1) {
                this.observers.splice(index, 1);
            }
        };
    }

    /**
     * Notify all observers of language change
     */
    notifyObservers() {
        this.observers.forEach(callback => {
            try {
                callback(this.currentLanguage);
            } catch (error) {
                console.error('Error in i18n observer:', error);
            }
        });
    }

    /**
     * Initialize language selector UI
     */
    initLanguageSelector() {
        const selector = document.getElementById('languageSelector');
        if (!selector) return;

        // Create language selector HTML
        selector.innerHTML = `
            <div class="language-selector">
                <button class="language-toggle" id="languageToggle">
                    <img src="assets/flags/${this.currentLanguage}.svg" alt="${this.languageNames[this.currentLanguage]}" class="flag-icon">
                    <span class="language-name">${this.languageNames[this.currentLanguage]}</span>
                    <span class="dropdown-arrow">▼</span>
                </button>
                <div class="language-dropdown" id="languageDropdown">
                    ${this.supportedLanguages.map(lang => `
                        <a href="#" class="language-option" data-lang="${lang}">
                            <img src="assets/flags/${lang}.svg" alt="${this.languageNames[lang]}" class="flag-icon">
                            <span>${this.languageNames[lang]}</span>
                        </a>
                    `).join('')}
                </div>
            </div>
        `;

        // Add event listeners
        const toggle = document.getElementById('languageToggle');
        const dropdown = document.getElementById('languageDropdown');
        
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            dropdown.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!selector.contains(e.target)) {
                dropdown.classList.remove('show');
            }
        });

        // Handle language selection
        dropdown.addEventListener('click', (e) => {
            e.preventDefault();
            const option = e.target.closest('.language-option');
            if (option) {
                const selectedLang = option.dataset.lang;
                this.setLanguage(selectedLang);
                dropdown.classList.remove('show');
            }
        });
    }

    /**
     * Update language selector display
     */
    updateLanguageSelector() {
        const toggle = document.getElementById('languageToggle');
        if (toggle) {
            const flagIcon = toggle.querySelector('.flag-icon');
            const languageName = toggle.querySelector('.language-name');
            
            if (flagIcon) {
                flagIcon.src = `assets/flags/${this.currentLanguage}.svg`;
                flagIcon.alt = this.languageNames[this.currentLanguage];
            }
            
            if (languageName) {
                languageName.textContent = this.languageNames[this.currentLanguage];
            }
        }
    }

    /**
     * Update all translatable elements in the DOM
     */
    updateDOM() {
        // Update elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' && element.type === 'text') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });

        // Update elements with data-i18n-html attribute (for HTML content)
        document.querySelectorAll('[data-i18n-html]').forEach(element => {
            const key = element.getAttribute('data-i18n-html');
            const translation = this.t(key);
            element.innerHTML = translation;
        });

        // Update title
        const titleElement = document.querySelector('h1');
        if (titleElement) {
            titleElement.textContent = this.t('ui.title');
        }
    }

    /**
     * Format number according to current locale
     */
    formatNumber(number, options = {}) {
        const locale = this.getLocaleCode();
        return new Intl.NumberFormat(locale, options).format(number);
    }

    /**
     * Format date according to current locale
     */
    formatDate(date, options = {}) {
        const locale = this.getLocaleCode();
        return new Intl.DateTimeFormat(locale, options).format(date);
    }

    /**
     * Get locale code for Intl APIs
     */
    getLocaleCode() {
        const localeMap = {
            'de': 'de-DE',
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'it': 'it-IT',
            'zh-cn': 'zh-CN'
        };
        
        return localeMap[this.currentLanguage] || 'en-US';
    }

    /**
     * Get text direction for current language
     */
    getTextDirection() {
        const meta = this.getCurrentLanguageMeta();
        return meta ? meta.direction : 'ltr';
    }

    /**
     * Check if current language is RTL
     */
    isRTL() {
        return this.getTextDirection() === 'rtl';
    }
}

// Create global instance
window.i18n = new I18nEngine();

