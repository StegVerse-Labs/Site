(() => {
  'use strict';

  const FIXTURE_PATH = 'fixtures/ecosystem-chat/hps-visualization-status.example.json';

  function ensurePrimaryNavigation() {
    const nav = document.querySelector('nav.sv-nav');
    if (!nav) return;
    const links = [
      ['ecosystem-usage.html', 'Usage Ledger'],
      ['ecosystem-comparison.html', 'Route Comparison']
    ];
    for (const [href, label] of links) {
      if (nav.querySelector(`a[href="${href}"]`)) continue;
      const anchor = document.createElement('a');
      anchor.href = href;
      anchor.textContent = label;
      anchor.dataset.ecosystemNavigation = 'true';
      nav.appendChild(anchor);
    }
  }

  ensurePrimaryNavigation();

  const host = document.getElementById('hpsVisualization');
  if (!host) return;

  const text = (value, fallback = 'unavailable') => {
    if (value === null || value === undefined || value === '') return fallback;
    return String(value);
  };

  const percent = (value) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return 0;
    return Math.max(0, Math.min(100, Math.round(numeric * 100)));
  };

  const list = (value) => Array.isArray(value) && value.length ? value.join(', ') : 'none';

  function setFailClosed(message) {
    host.dataset.state = 'unavailable';
    host.innerHTML = `
      <div class="hps-head">
        <div><strong>HPS standing preview unavailable</strong><span>${message}</span></div>
        <span class="hps-badge">PREVIEW ONLY</span>
      </div>
      <p class="muted">No standing, authority, capability, replay, reconstruction, or receipt claim is inferred when the fixture cannot be validated.</p>`;
  }

  function validate(payload) {
    return payload &&
      payload.payload_type === 'hps_visualization_status' &&
      payload.preview_only === true &&
      payload.authority_granted === false &&
      payload.execution_enabled === false &&
      payload.receipt_issued_by_site === false &&
      payload.heartbeat && payload.standing && payload.capabilities && payload.continuity && payload.display;
  }

  function metric(label, value) {
    const safe = percent(value);
    return `<div class="hps-metric"><span>${label}</span><div class="hps-track"><i style="--hps-value:${safe}%"></i></div><b>${safe}%</b></div>`;
  }

  function render(payload) {
    if (!validate(payload)) {
      setFailClosed('Fixture did not satisfy the preview/no-authority contract.');
      return;
    }

    const heartbeat = payload.heartbeat;
    const standing = payload.standing;
    const capabilities = payload.capabilities;
    const continuity = payload.continuity;
    const bars = payload.display.bars || {};

    host.dataset.state = text(heartbeat.state, 'UNKNOWN').toLowerCase();
    host.innerHTML = `
      <div class="hps-head">
        <div>
          <strong>Heartbeat / standing preview</strong>
          <span>${text(payload.display.summary)}</span>
        </div>
        <span class="hps-badge">FIXTURE · PREVIEW ONLY · AUTHORITY NONE</span>
      </div>
      <div class="hps-grid">
        <div class="hps-cell"><small>Heartbeat</small><strong>${text(heartbeat.state)}</strong><span>phase=${text(heartbeat.phase)}</span></div>
        <div class="hps-cell"><small>Standing</small><strong>${text(standing.class)}</strong><span>score=${text(standing.score)}</span></div>
        <div class="hps-cell"><small>Replay</small><strong>${continuity.replay_available === true ? 'AVAILABLE' : 'UNAVAILABLE'}</strong><span>displayed posture only</span></div>
        <div class="hps-cell"><small>Reconstruction</small><strong>${continuity.reconstruction_available === true ? 'AVAILABLE' : 'UNAVAILABLE'}</strong><span>displayed posture only</span></div>
      </div>
      <div class="hps-capabilities">
        <div><small>Open window</small><span>${list(capabilities.open)}</span></div>
        <div><small>Closed window</small><span>${list(capabilities.closed)}</span></div>
        <div><small>Expired window</small><span>${list(capabilities.expired)}</span></div>
      </div>
      <div class="hps-metrics">
        ${metric('Standing', bars.standing)}
        ${metric('Continuity', bars.continuity)}
        ${metric('Capability availability', bars.capability_availability)}
      </div>
      <div class="hps-chain">chain_head=${text(continuity.chain_head)} · fixture_receipt=${text(heartbeat.receipt_id)} · site_receipt=not-issued · execution=disabled</div>`;
  }

  fetch(FIXTURE_PATH, { cache: 'no-store' })
    .then((response) => {
      if (!response.ok) throw new Error(`fixture HTTP ${response.status}`);
      return response.json();
    })
    .then(render)
    .catch(() => setFailClosed('Fixture could not be loaded; the visualization failed closed.'));

  for (const source of [
    'assets/ecosystem-chat-conversation.js',
    'assets/ecosystem-chat-transition-identity.js',
    'assets/ecosystem-chat-gateway-health.js',
    'assets/ecosystem-chat-traversal.js',
    'assets/ecosystem-chat-provider.js',
    'assets/ecosystem-chat-solver.js'
  ]) {
    const script = document.createElement('script');
    script.src = source;
    script.dataset.previewOnly = 'true';
    document.body.appendChild(script);
  }
})();
