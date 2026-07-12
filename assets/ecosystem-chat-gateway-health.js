(() => {
  'use strict';

  const CONFIG_PATH = 'data/ecosystem-chat-gateway.json';

  function insertPanel() {
    const panel = document.createElement('section');
    panel.className = 'simple-card';
    panel.id = 'gateway-health';
    panel.setAttribute('aria-live', 'polite');
    panel.innerHTML = '<h2 class="sv-h2">Governed gateway status</h2><p class="muted">Checking the bounded request-response service…</p>';
    const consoleHeading = document.getElementById('console');
    if (consoleHeading?.parentNode) consoleHeading.parentNode.insertBefore(panel, consoleHeading);
    else document.querySelector('.sv-wrap')?.appendChild(panel);
    return panel;
  }

  function render(panel, state, summary, detail) {
    panel.dataset.state = state;
    const label = state === 'healthy' ? 'LIVE · BOUNDED' : state === 'fallback' ? 'LOCAL FALLBACK' : 'UNAVAILABLE';
    panel.innerHTML = `
      <div class="hps-head">
        <div><strong>Governed gateway ${state}</strong><span>${summary}</span></div>
        <span class="hps-badge">${label}</span>
      </div>
      <p class="muted">${detail}</p>`;
  }

  async function check() {
    const panel = insertPanel();
    try {
      const configResponse = await fetch(CONFIG_PATH, { cache: 'no-store' });
      if (!configResponse.ok) throw new Error(`config HTTP ${configResponse.status}`);
      const config = await configResponse.json();
      if (config.enabled !== true || !config.health_endpoint) {
        render(panel, 'fallback', 'Gateway disabled by configuration.', 'Requests remain available through deterministic local classification. No gateway, provider, or final response receipt is claimed.');
        return;
      }
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), Math.min(Number(config.timeout_ms || 20000), 10000));
      try {
        const healthResponse = await fetch(config.health_endpoint, { cache: 'no-store', signal: controller.signal });
        if (!healthResponse.ok) throw new Error(`health HTTP ${healthResponse.status}`);
        const health = await healthResponse.json();
        if (health.status !== 'ok' || health.service !== 'stegverse-ecosystem-chat-gateway') throw new Error('health contract mismatch');
        if (health.provider_output_is_authority !== false || health.provider_failure_falls_back !== true) throw new Error('provider boundary mismatch');
        const storage = health.sqlite_transition_store === true
          ? (health.storage_durable_across_restarts === true ? 'persistent SQLite storage' : 'SQLite on ephemeral host storage')
          : 'transition persistence unavailable';
        const custody = health.master_records_submission_enabled === true
          ? 'Master-Records submission enabled'
          : 'Master-Records submission pending configuration';
        const provider = health.governed_provider_enabled === true
          ? 'provider enabled under quota and cost policy'
          : 'provider disabled; deterministic fallback active';
        render(
          panel,
          'healthy',
          `Native executor ${health.native_executor_status || 'UNKNOWN'}; ${provider}.`,
          `${storage}; ${custody}. Provider output is never authority, provider credentials are not exposed to Site, and provider failure falls back without repository mutation or custody overclaim.`
        );
      } finally {
        window.clearTimeout(timeout);
      }
    } catch (error) {
      render(panel, 'unavailable', 'The remote gateway could not be verified.', `Local classification remains active. Reason: ${String(error)}`);
    }
  }

  window.addEventListener('DOMContentLoaded', check);
})();
