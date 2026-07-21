(() => {
  'use strict';

  const GATEWAY_PATH = '/api/universal-translator';
  const MAX_INPUT_CHARS = 12000;
  const supportedLanguages = [
    ['auto', 'Detect automatically'], ['en', 'English'], ['es', 'Español'],
    ['zh-Hans', '中文（简体）'], ['zh-Hant', '中文（繁體）'], ['ar', 'العربية'],
    ['hi', 'हिन्दी'], ['pt', 'Português'], ['fr', 'Français'], ['de', 'Deutsch'],
    ['ja', '日本語'], ['ko', '한국어'], ['it', 'Italiano'], ['nl', 'Nederlands'],
    ['pl', 'Polski'], ['ru', 'Русский'], ['tr', 'Türkçe'], ['uk', 'Українська'],
    ['vi', 'Tiếng Việt'], ['id', 'Bahasa Indonesia'], ['th', 'ไทย'], ['he', 'עברית'],
    ['fa', 'فارسی'], ['ur', 'اردو'], ['bn', 'বাংলা'], ['sw', 'Kiswahili']
  ];

  const els = {
    source: document.getElementById('translatorSourceLanguage'),
    target: document.getElementById('translatorTargetLanguage'),
    input: document.getElementById('translatorInput'),
    output: document.getElementById('translatorOutput'),
    form: document.getElementById('translatorForm'),
    status: document.getElementById('translatorStatus'),
    receipt: document.getElementById('translatorReceipt'),
    swap: document.getElementById('translatorSwap'),
    copy: document.getElementById('translatorCopy'),
    clear: document.getElementById('translatorClear')
  };

  if (!els.form) return;

  populateLanguageSelects();
  restorePreferences();

  els.form.addEventListener('submit', translate);
  els.swap.addEventListener('click', swapLanguages);
  els.copy.addEventListener('click', copyOutput);
  els.clear.addEventListener('click', clearTranslator);
  els.source.addEventListener('change', savePreferences);
  els.target.addEventListener('change', savePreferences);

  function populateLanguageSelects() {
    supportedLanguages.forEach(([value, label]) => {
      const sourceOption = new Option(label, value);
      els.source.add(sourceOption);
      if (value !== 'auto') els.target.add(new Option(label, value));
    });
  }

  function restorePreferences() {
    const source = localStorage.getItem('stegverse.translator.source') || 'auto';
    const target = localStorage.getItem('stegverse.translator.target') || preferredTargetLanguage();
    els.source.value = source;
    els.target.value = supportedLanguages.some(([value]) => value === target) && target !== 'auto' ? target : 'es';
  }

  function savePreferences() {
    localStorage.setItem('stegverse.translator.source', els.source.value);
    localStorage.setItem('stegverse.translator.target', els.target.value);
  }

  function preferredTargetLanguage() {
    const language = (navigator.language || 'es').toLowerCase();
    if (language.startsWith('zh-tw') || language.startsWith('zh-hk') || language.startsWith('zh-mo')) return 'zh-Hant';
    if (language.startsWith('zh')) return 'zh-Hans';
    const base = language.split('-')[0];
    return supportedLanguages.some(([value]) => value === base) ? base : 'es';
  }

  async function translate(event) {
    event.preventDefault();
    const text = els.input.value.trim();
    if (!text) return setStatus('Enter text to translate.', 'error');
    if (text.length > MAX_INPUT_CHARS) return setStatus(`Input exceeds ${MAX_INPUT_CHARS.toLocaleString()} characters.`, 'error');

    setBusy(true);
    setStatus('Detecting language and selecting a governed translation path…');
    els.output.value = '';
    els.receipt.textContent = 'translation_state=pending';

    try {
      const sourceLanguage = els.source.value === 'auto' ? await detectLanguage(text) : els.source.value;
      const targetLanguage = els.target.value;
      if (!sourceLanguage) throw new Error('Source language could not be determined. Select it manually.');
      if (normalizeLanguage(sourceLanguage) === normalizeLanguage(targetLanguage)) {
        els.output.value = text;
        writeReceipt({ sourceLanguage, targetLanguage, engine: 'identity', governed: true, remote: false });
        return setStatus('Source and target languages match. Original text preserved.', 'ok');
      }

      const localResult = await translateLocally(text, sourceLanguage, targetLanguage);
      if (localResult) {
        els.output.value = localResult;
        writeReceipt({ sourceLanguage, targetLanguage, engine: 'browser-native', governed: true, remote: false });
        return setStatus('Translated locally on this device.', 'ok');
      }

      const gatewayResult = await translateThroughGateway(text, sourceLanguage, targetLanguage);
      els.output.value = gatewayResult.translation;
      writeReceipt({
        sourceLanguage: gatewayResult.detected_source_language || sourceLanguage,
        targetLanguage,
        engine: gatewayResult.provider || 'governed-gateway',
        governed: gatewayResult.governed !== false,
        remote: true,
        receiptId: gatewayResult.receipt_id
      });
      setStatus('Translated through the governed gateway.', 'ok');
    } catch (error) {
      els.output.value = '';
      els.receipt.textContent = `translation_state=failed · original_preserved=true · authority=none · reason=${safeToken(error.message)}`;
      setStatus(error.message || 'Translation failed. Original text was preserved.', 'error');
    } finally {
      setBusy(false);
    }
  }

  async function detectLanguage(text) {
    try {
      if ('LanguageDetector' in window && typeof window.LanguageDetector.create === 'function') {
        const detector = await window.LanguageDetector.create();
        const results = await detector.detect(text);
        if (results && results[0] && results[0].detectedLanguage) return canonicalLanguage(results[0].detectedLanguage);
      }
      if (window.ai && window.ai.languageDetector && typeof window.ai.languageDetector.create === 'function') {
        const detector = await window.ai.languageDetector.create();
        const results = await detector.detect(text);
        if (results && results[0] && results[0].detectedLanguage) return canonicalLanguage(results[0].detectedLanguage);
      }
    } catch (_) {
      // Detection failure falls through to the governed gateway.
    }
    return 'auto';
  }

  async function translateLocally(text, sourceLanguage, targetLanguage) {
    if (sourceLanguage === 'auto') return null;
    try {
      if ('Translator' in window && typeof window.Translator.create === 'function') {
        const availability = typeof window.Translator.availability === 'function'
          ? await window.Translator.availability({ sourceLanguage, targetLanguage }) : 'available';
        if (!['available', 'readily', 'after-download'].includes(availability)) return null;
        const translator = await window.Translator.create({ sourceLanguage, targetLanguage });
        return await translator.translate(text);
      }
      if (window.ai && window.ai.translator && typeof window.ai.translator.create === 'function') {
        const translator = await window.ai.translator.create({ sourceLanguage, targetLanguage });
        return await translator.translate(text);
      }
    } catch (_) {
      return null;
    }
    return null;
  }

  async function translateThroughGateway(text, sourceLanguage, targetLanguage) {
    const response = await fetch(GATEWAY_PATH, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        source_language: sourceLanguage,
        target_language: targetLanguage,
        preserve_formatting: true,
        preserve_named_entities: true,
        authority_required: false,
        execution_authority: false,
        receipt_requested: true,
        client: 'StegVerse-Labs/Site',
        surface: 'universal-translator.html'
      })
    });
    if (!response.ok) throw new Error(`Governed translation gateway unavailable (${response.status}).`);
    const payload = await response.json();
    if (!payload || typeof payload.translation !== 'string' || !payload.translation.trim()) {
      throw new Error('Governed gateway returned no translation.');
    }
    return payload;
  }

  function swapLanguages() {
    const source = els.source.value;
    const target = els.target.value;
    els.source.value = target;
    els.target.value = source === 'auto' ? preferredTargetLanguage() : source;
    if (els.output.value) {
      const oldInput = els.input.value;
      els.input.value = els.output.value;
      els.output.value = oldInput;
    }
    savePreferences();
  }

  async function copyOutput() {
    if (!els.output.value) return;
    await navigator.clipboard.writeText(els.output.value);
    setStatus('Translation copied.', 'ok');
  }

  function clearTranslator() {
    els.input.value = '';
    els.output.value = '';
    els.receipt.textContent = 'translation_state=idle · authority=none · original_preserved=true';
    setStatus('Ready.');
    els.input.focus();
  }

  function writeReceipt({ sourceLanguage, targetLanguage, engine, governed, remote, receiptId }) {
    const fields = [
      'translation_state=complete',
      `source_language=${safeToken(sourceLanguage)}`,
      `target_language=${safeToken(targetLanguage)}`,
      `engine=${safeToken(engine)}`,
      `governed=${Boolean(governed)}`,
      `remote=${Boolean(remote)}`,
      'execution_authority=false',
      'original_preserved=true'
    ];
    if (receiptId) fields.push(`receipt_id=${safeToken(receiptId)}`);
    els.receipt.textContent = fields.join(' · ');
  }

  function setBusy(busy) {
    els.form.querySelector('button[type="submit"]').disabled = busy;
    els.source.disabled = busy;
    els.target.disabled = busy;
  }

  function setStatus(message, state = '') {
    els.status.textContent = message;
    els.status.dataset.state = state;
  }

  function canonicalLanguage(language) {
    const lower = String(language || '').toLowerCase();
    if (lower === 'zh' || lower.startsWith('zh-cn') || lower.startsWith('zh-sg')) return 'zh-Hans';
    if (lower.startsWith('zh-tw') || lower.startsWith('zh-hk') || lower.startsWith('zh-mo')) return 'zh-Hant';
    return language;
  }

  function normalizeLanguage(language) {
    return canonicalLanguage(language).toLowerCase().split('-')[0];
  }

  function safeToken(value) {
    return String(value || 'unknown').replace(/[^a-zA-Z0-9._:-]/g, '_').slice(0, 120);
  }
})();
