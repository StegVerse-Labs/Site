(() => {
  'use strict';

  const FIXTURE = 'fixtures/ecosystem-chat/provider-status.example.json';
  let host = document.getElementById('providerStatusPreview');

  if (!host) {
    const consoleHeading = document.getElementById('console');
    if (!consoleHeading) return;
    const section = document.createElement('section');
    section.className = 'simple-card';
    section.id = 'provider-preview';
    section.innerHTML = '<h2 class="sv-h2">Provider, quota, cost, latency, and usage</h2><div class="trust-note">Fixture-bound display contract only. No model is invoked, no current price is fetched, no billing occurs, and no authority or receipt is issued.</div><div id="providerStatusPreview" aria-live="polite"><p class="muted">Loading bounded provider posture…</p></div>';
    consoleHeading.parentNode.insertBefore(section, consoleHeading);
    host = document.getElementById('providerStatusPreview');
  }

  const style = document.createElement('style');
  style.textContent = '.provider-head{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;flex-wrap:wrap}.provider-head strong,.provider-head span{display:block}.provider-head span{color:var(--muted);font-size:12px;margin-top:4px}.provider-badge{font:10px var(--mono);letter-spacing:.06em;color:#bce9c5!important;border:1px solid #245c34;border-radius:999px;padding:7px 9px}.provider-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:14px 0}.provider-grid>div{border:1px solid var(--border);border-radius:var(--radius);padding:12px}.provider-grid small{display:block;color:var(--muted);text-transform:uppercase;font:10px var(--mono);margin-bottom:5px}.provider-grid strong,.provider-grid span{display:block}.provider-grid span{color:var(--muted);font-size:11px;margin-top:4px}.provider-meters{display:grid;gap:8px}.provider-meter{display:grid;grid-template-columns:140px 1fr 42px;gap:10px;align-items:center;font:11px var(--mono);color:var(--muted)}.provider-track{height:8px;border-radius:999px;background:#0a111c;border:1px solid var(--border2);overflow:hidden}.provider-track i{display:block;height:100%;width:var(--provider-value,0%);background:linear-gradient(90deg,rgba(77,184,255,.22),rgba(102,255,153,.72))}.provider-line{margin-top:12px;padding-top:10px;border-top:1px solid var(--border);font:10px var(--mono);color:var(--muted);overflow-wrap:anywhere}@media(max-width:600px){.provider-meter{grid-template-columns:105px 1fr 38px}}';
  document.head.appendChild(style);

  const safe = (value, fallback = 'unavailable') => value === null || value === undefined || value === '' ? fallback : String(value);
  const pct = (value) => Math.max(0, Math.min(100, Math.round(Number(value || 0) * 100)));

  function failClosed(message) {
    host.dataset.state = 'unavailable';
    host.innerHTML = `<div class="provider-head"><strong>Provider preview unavailable</strong><span>PREVIEW ONLY</span></div><p class="muted">${message} No provider invocation, pricing, authority, execution, or receipt claim is inferred.</p>`;
  }

  function valid(data) {
    return data && data.payload_type === 'provider_status_preview' && data.preview_only === true && data.live_invocation === false && data.authority_granted === false && data.execution_enabled === false && data.receipt_issued_by_site === false && data.pricing_current === false && data.provider && data.quota && data.usage && data.cost && data.latency && data.display;
  }

  function meter(label, value) {
    const amount = pct(value);
    return `<div class="provider-meter"><span>${label}</span><div class="provider-track"><i style="--provider-value:${amount}%"></i></div><b>${amount}%</b></div>`;
  }

  function render(data) {
    if (!valid(data)) return failClosed('Fixture contract validation failed.');
    host.dataset.state = 'preview';
    host.innerHTML = `
      <div class="provider-head"><div><strong>Provider / usage posture</strong><span>${safe(data.display.summary)}</span></div><span class="provider-badge">FIXTURE · NOT INVOKED</span></div>
      <div class="provider-grid">
        <div><small>Provider status</small><strong>${safe(data.provider.status)}</strong><span>${safe(data.provider.route)}</span></div>
        <div><small>Fallback</small><strong>${safe(data.provider.fallback)}</strong><span>local boundary retained</span></div>
        <div><small>Daily quota</small><strong>${safe(data.quota.remaining)} / ${safe(data.quota.limit)}</strong><span>fixture counter only</span></div>
        <div><small>Trial quota</small><strong>${safe(data.quota.trial_total_limit - data.quota.trial_total_used)} / ${safe(data.quota.trial_total_limit)}</strong><span>fixture counter only</span></div>
        <div><small>Estimated cost</small><strong>${safe(data.cost.currency)} ${Number(data.cost.estimated).toFixed(4)}</strong><span>not current pricing</span></div>
        <div><small>Latency</small><strong>${safe(data.latency.total_ms)} ms</strong><span>classification only</span></div>
      </div>
      <div class="provider-meters">
        ${meter('Quota remaining', data.display.bands.quota_remaining)}
        ${meter('Trial remaining', data.display.bands.trial_remaining)}
        ${meter('Provider activity', data.display.bands.provider_activity)}
      </div>
      <div class="provider-line">requests=${safe(data.usage.requests)} · input_units=${safe(data.usage.input_units)} · output_units=${safe(data.usage.output_units)} · billable_units=${safe(data.usage.billable_units)} · provider_ms=${safe(data.latency.provider_ms)} · billed=${safe(data.cost.billed)} · live_invocation=false · authority=none · receipt=not-issued</div>`;
  }

  fetch(FIXTURE, { cache: 'no-store' })
    .then((response) => {
      if (!response.ok) throw new Error(`fixture HTTP ${response.status}`);
      return response.json();
    })
    .then(render)
    .catch(() => failClosed('Fixture could not be loaded.'));
})();
