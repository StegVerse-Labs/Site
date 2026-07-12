(() => {
  'use strict';

  const CONFIG_PATH = 'data/ecosystem-chat-gateway.json';
  const LAST_RESULT_KEY = 'stegverse_ecosystem_chat_last_gateway_result';
  const host = document.getElementById('live-custody-status');
  if (!host) return;

  const esc = (value) => String(value ?? '—').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

  function requestedTransitionId() {
    const query = new URLSearchParams(window.location.search).get('transition_id');
    if (query) return query;
    try {
      const last = JSON.parse(window.sessionStorage.getItem(LAST_RESULT_KEY) || '{}');
      return last.transition_id || null;
    } catch (_) {
      return null;
    }
  }

  function renderEmpty(message) {
    host.innerHTML = `<article class="card"><span class="eyebrow">Live custody lookup</span><h2>No live transition selected</h2><p class="lede">${esc(message)}</p></article>`;
  }

  function renderStatus(data) {
    const custody = data.custody_submission || {};
    const recorded = data.master_record_status === 'RECORDED';
    host.innerHTML = `<article class="card">
      <div class="row">
        <div><span class="eyebrow">Live gateway lifecycle lookup</span><h2>${esc(data.transition_id)}</h2></div>
        <span class="tag ${recorded ? 'complete' : 'pending'}">${esc(data.master_record_status)}</span>
      </div>
      <dl>
        <dt>Run</dt><dd>${esc(data.run_id)}</dd>
        <dt>Lifecycle</dt><dd>${esc(data.lifecycle_state)}</dd>
        <dt>Admissibility</dt><dd>${esc(data.admissibility_result)}</dd>
        <dt>Commit validity</dt><dd>${esc(data.commit_time_validity)}</dd>
        <dt>Final receipt</dt><dd>${esc(data.final_receipt_id)}</dd>
        <dt>Custody queue</dt><dd>${esc(custody.state || 'NOT_QUEUED')}</dd>
        <dt>Custody receipt</dt><dd>${esc(custody.custody_receipt_id)}</dd>
        <dt>Master-Records</dt><dd>${esc(data.master_record_status)}</dd>
        <dt>Master record ref</dt><dd>${esc(data.master_record_ref)}</dd>
        <dt>Reconstruction</dt><dd>${esc(data.reconstruction_status)}</dd>
        <dt>Local persistence</dt><dd>${data.durable_local_persistence === true ? 'SQLITE_PERSISTED' : 'UNVERIFIED'}</dd>
      </dl>
      <p class="lede">This is a live status projection from the gateway. Site does not issue the final receipt, custody receipt, Master-Records admission, or reconstruction result.</p>
    </article>`;
  }

  async function load() {
    const transitionId = requestedTransitionId();
    if (!transitionId) {
      renderEmpty('Open this page after an Ecosystem Chat request, or add ?transition_id=… to inspect a specific transition.');
      return;
    }
    try {
      const configResponse = await fetch(CONFIG_PATH, {cache: 'no-store'});
      if (!configResponse.ok) throw new Error(`config HTTP ${configResponse.status}`);
      const config = await configResponse.json();
      if (config.enabled !== true || !config.endpoint) throw new Error('gateway disabled');
      const base = new URL(config.endpoint);
      const statusUrl = `${base.origin}/api/transitions/${encodeURIComponent(transitionId)}`;
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), Math.min(Number(config.timeout_ms || 20000), 10000));
      try {
        const response = await fetch(statusUrl, {cache: 'no-store', signal: controller.signal});
        if (!response.ok) throw new Error(`transition HTTP ${response.status}`);
        const data = await response.json();
        if (data.transition_id !== transitionId) throw new Error('transition identity mismatch');
        if (data.master_record_status === 'RECORDED' && (!data.master_record_ref || data.reconstruction_status !== 'PASS')) {
          throw new Error('RECORDED custody contract mismatch');
        }
        renderStatus(data);
      } finally {
        window.clearTimeout(timeout);
      }
    } catch (error) {
      renderEmpty(`Live custody status unavailable. The checked-in projection remains visible below. Reason: ${String(error)}`);
    }
  }

  window.addEventListener('DOMContentLoaded', load);
})();
