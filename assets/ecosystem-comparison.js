(() => {
  'use strict';

  const statusRoot = document.getElementById('comparisonStatus');
  const routeRoot = document.getElementById('routeComparison');
  const deltaRoot = document.getElementById('deltaComparison');
  const receiptRoot = document.getElementById('comparisonReceipt');
  const esc = (value) => String(value ?? '').replace(/[&<>'"]/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));

  function validateMetric(name, metric) {
    if (!metric || typeof metric !== 'object') throw new Error(`metric ${name} must be an object`);
    if (!['MEASURED','CONFIGURED','DERIVED','UNAVAILABLE'].includes(metric.evidence_class)) throw new Error(`invalid evidence class for ${name}`);
    if (metric.evidence_class === 'UNAVAILABLE' && metric.value !== null) throw new Error(`UNAVAILABLE metric ${name} must be null`);
    if (metric.evidence_class !== 'UNAVAILABLE' && (!Number.isFinite(Number(metric.value)) || !metric.unit)) throw new Error(`metric ${name} requires numeric value and unit`);
  }

  function validateReceipt(payload) {
    if (!payload.comparison_id || !payload.task_identity) throw new Error('comparison identity is required');
    if (!Array.isArray(payload.routes) || payload.routes.length !== 2) throw new Error('exactly two routes are required');
    const kinds = new Set(payload.routes.map((route) => route.route_kind));
    if (!kinds.has('STEGVERSE_GOVERNED') || !kinds.has('EXTERNAL_RECURSIVE')) throw new Error('governed and external recursive routes are required');
    for (const route of payload.routes) {
      if (!route.route_id || !route.label || !route.metrics) throw new Error('route identity, label, and metrics are required');
      Object.entries(route.metrics).forEach(([name, metric]) => validateMetric(name, metric));
    }
    Object.entries(payload.deltas || {}).forEach(([name, metric]) => validateMetric(name, metric));
    const invariants = payload.invariants || {};
    if (invariants.same_task_identity !== true || invariants.same_output_requirement !== true) throw new Error('like-for-like identity invariants failed');
    if (invariants.comparison_is_authority !== false || invariants.comparison_is_admissibility !== false) throw new Error('comparison may not claim authority or admissibility');
    if (payload.measurement_posture === 'CONFIGURED_FIXTURE' && invariants.configured_values_are_measured !== false) throw new Error('configured values may not be presented as measured');
  }

  function routeMaximums(routes) {
    const maxima = {};
    for (const route of routes) {
      for (const [name, metric] of Object.entries(route.metrics)) {
        if (metric.value === null) continue;
        maxima[name] = Math.max(maxima[name] || 0, Math.abs(Number(metric.value)));
      }
    }
    return maxima;
  }

  function renderRoutes(payload) {
    const maxima = routeMaximums(payload.routes);
    routeRoot.innerHTML = payload.routes.map((route) => {
      const metrics = Object.entries(route.metrics).map(([name, metric]) => {
        const value = metric.value === null ? 'Unavailable' : `${metric.value} ${metric.unit}`;
        const width = metric.value === null || !maxima[name] ? 0 : Math.max(2, Math.round(Math.abs(Number(metric.value)) / maxima[name] * 100));
        return `<div class="metric-row"><span>${esc(name)}<br><small>${esc(metric.evidence_class)}</small></span><div class="metric-track"><i class="metric-fill" style="--width:${width}%"></i></div><span class="metric-value">${esc(value)}</span></div>`;
      }).join('');
      const receipts = (route.receipt_refs || []).map((ref) => `<span>${esc(ref)}</span>`).join('<br>') || 'none';
      return `<article class="card route-card"><span class="route-kind">${esc(route.route_kind)}</span><h3>${esc(route.label)}</h3><p>${esc(route.output_summary)}</p><p class="muted">Admissibility posture: ${esc(route.admissibility_result)}</p>${metrics}<div class="receipt-list"><strong>Receipt refs</strong><br>${receipts}</div></article>`;
    }).join('');
  }

  function renderDeltas(payload) {
    deltaRoot.innerHTML = Object.entries(payload.deltas || {}).map(([name, metric]) => {
      const sign = Number(metric.value) > 0 ? '+' : '';
      return `<article class="card delta-card"><span class="muted">${esc(name)}</span><strong>${sign}${esc(metric.value)} ${esc(metric.unit)}</strong><span class="muted">${esc(metric.evidence_class)} · ${esc(metric.formula || 'external_recursive - stegverse_governed')}</span></article>`;
    }).join('');
  }

  function renderReceipt(payload) {
    const refs = payload.routes.flatMap((route) => route.receipt_refs || []);
    receiptRoot.innerHTML = `<p><strong>Comparison:</strong> ${esc(payload.comparison_id)}<br><strong>Task identity:</strong> ${esc(payload.task_identity)}<br><strong>Measurement posture:</strong> ${esc(payload.measurement_posture)}</p><p class="receipt-list">${refs.map((ref) => esc(ref)).join('<br>')}</p><p class="muted">The Site renders the supplied comparison receipt. It does not recalculate standing, grant execution authority, or relabel configured values as measured.</p>`;
  }

  async function main() {
    const response = await fetch('data/llm-route-comparison-fixture.json', {cache: 'no-store'});
    if (!response.ok) throw new Error(`comparison fixture returned ${response.status}`);
    const payload = await response.json();
    validateReceipt(payload);
    renderRoutes(payload);
    renderDeltas(payload);
    renderReceipt(payload);
    statusRoot.textContent = `${payload.comparison_id} · ${payload.measurement_posture} · like-for-like identity preserved`;
  }

  main().catch((error) => {
    statusRoot.textContent = `COMPARISON_LOAD_FAILED: ${error.message}`;
    routeRoot.innerHTML = '<div class="boundary">The comparison failed closed. No deltas were displayed.</div>';
    deltaRoot.innerHTML = '';
    receiptRoot.innerHTML = '<p class="muted">No comparison receipt rendered.</p>';
  });
})();
