(() => {
  'use strict';

  const CONFIG_PATH = 'data/ecosystem-chat-gateway.json';
  const EXAMPLE_PATH = 'data/external-chat-example.json';
  const idEl = document.getElementById('framework-id');
  const nameEl = document.getElementById('framework-name');
  const submissionEl = document.getElementById('submission');
  const statusEl = document.getElementById('status');
  const resultEl = document.getElementById('result');
  const summaryEl = document.getElementById('summary');
  const linksEl = document.getElementById('wiki-links');
  const outputEl = document.getElementById('output');

  const esc = (value) => String(value ?? '—').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

  function metric(label, value) {
    return `<div class="metric"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`;
  }

  async function loadExample() {
    const response = await fetch(EXAMPLE_PATH, { cache: 'no-store' });
    if (!response.ok) throw new Error(`example HTTP ${response.status}`);
    const payload = await response.json();
    idEl.value = payload.framework_id || '';
    nameEl.value = payload.framework_name || '';
    submissionEl.value = JSON.stringify(payload, null, 2);
    statusEl.textContent = 'Example loaded. Review it before submitting.';
  }

  async function endpoint() {
    const response = await fetch(CONFIG_PATH, { cache: 'no-store' });
    if (!response.ok) throw new Error(`gateway config HTTP ${response.status}`);
    const config = await response.json();
    if (config.enabled !== true || !config.endpoint) throw new Error('governed gateway disabled');
    return config.endpoint.replace(/\/api\/ecosystem-chat$/, '/api/external-framework-compatibility');
  }

  function render(data) {
    resultEl.hidden = false;
    const coverage = data.field_coverage || {};
    summaryEl.innerHTML = [
      metric('Result', data.result),
      metric('Field coverage', `${coverage.present ?? 0}/${coverage.required ?? 0}`),
      metric('Known wiki report', data.known_framework_report === true ? 'YES' : 'NO'),
      metric('Receipt', data.receipt_id || 'none'),
    ].join('');
    const links = [];
    if (data.admissibility_wiki_page) links.push(`<a href="${esc(data.admissibility_wiki_page)}" target="_blank" rel="noopener">Open framework page</a>`);
    if (data.admissibility_wiki_report) links.push(`<a href="${esc(data.admissibility_wiki_report)}" target="_blank" rel="noopener">Open compatibility report</a>`);
    linksEl.innerHTML = links.join(' · ') || 'No existing wiki report matched this framework ID. The result remains provisional intake.';
    outputEl.textContent = JSON.stringify(data, null, 2);
    statusEl.innerHTML = `<span class="good">Compatibility test complete.</span> Evidence only; no certification, execution, or standing was created.`;
  }

  async function submit() {
    statusEl.textContent = 'Running bounded compatibility test…';
    resultEl.hidden = true;
    let payload;
    try {
      payload = JSON.parse(submissionEl.value);
    } catch (error) {
      statusEl.innerHTML = `<span class="error">Invalid JSON: ${esc(error.message)}</span>`;
      return;
    }
    payload.framework_id = idEl.value.trim() || payload.framework_id;
    payload.framework_name = nameEl.value.trim() || payload.framework_name;
    try {
      const url = await endpoint();
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), 20000);
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          signal: controller.signal,
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail?.reason || `HTTP ${response.status}`);
        if (data.compatibility_evidence_only !== true || data.boundary?.compatibility_result_is_authority !== false) {
          throw new Error('compatibility authority boundary mismatch');
        }
        if (data.submission_retained !== false || data.wiki_record_created !== false) {
          throw new Error('submission retention/publication boundary mismatch');
        }
        render(data);
      } finally {
        window.clearTimeout(timeout);
      }
    } catch (error) {
      statusEl.innerHTML = `<span class="error">Compatibility service unavailable: ${esc(error.message)}</span> No result or receipt was claimed.`;
    }
  }

  document.getElementById('load-example').addEventListener('click', () => loadExample().catch((error) => {
    statusEl.innerHTML = `<span class="error">Could not load example: ${esc(error.message)}</span>`;
  }));
  document.getElementById('submit').addEventListener('click', submit);
  loadExample().catch(() => {});
})();
