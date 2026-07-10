(() => {
  'use strict';

  const FIXTURE = 'fixtures/ecosystem-chat/solver-response.example.json';
  let host = document.getElementById('solverResponsePreview');

  if (!host) {
    const consoleHeading = document.getElementById('console');
    if (!consoleHeading) return;
    const section = document.createElement('section');
    section.className = 'simple-card';
    section.id = 'solver-preview';
    section.innerHTML = '<h2 class="sv-h2">Governed math-solver preview</h2><div class="trust-note">Static proof-step fixture only. No live solver runs, no authority is granted, and no receipt is issued.</div><div id="solverResponsePreview" aria-live="polite"><p class="muted">Loading governed solver fixture…</p></div>';
    consoleHeading.parentNode.insertBefore(section, consoleHeading);
    host = document.getElementById('solverResponsePreview');
  }

  const style = document.createElement('style');
  style.textContent = '.solver-head{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;flex-wrap:wrap}.solver-head strong,.solver-head span{display:block}.solver-head span{color:var(--muted);font-size:12px;margin-top:4px}.solver-badge{font:10px var(--mono);letter-spacing:.06em;color:#bce9c5!important;border:1px solid #245c34;border-radius:999px;padding:7px 9px}.solver-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:14px 0}.solver-grid>div,.solver-step{border:1px solid var(--border);border-radius:var(--radius);padding:12px}.solver-grid small,.solver-step small{display:block;color:var(--muted);text-transform:uppercase;font:10px var(--mono);margin-bottom:5px}.solver-grid strong,.solver-grid span{display:block}.solver-grid span{color:var(--muted);font-size:11px;margin-top:4px}.solver-steps{display:grid;gap:8px;margin:12px 0}.solver-step strong,.solver-step span{display:block}.solver-step span{color:var(--muted);font-size:11px;margin-top:4px}.solver-meters{display:grid;gap:8px}.solver-meter{display:grid;grid-template-columns:140px 1fr 42px;gap:10px;align-items:center;font:11px var(--mono);color:var(--muted)}.solver-track{height:8px;border-radius:999px;background:#0a111c;border:1px solid var(--border2);overflow:hidden}.solver-track i{display:block;height:100%;width:var(--solver-value,0%);background:linear-gradient(90deg,rgba(77,184,255,.22),rgba(102,255,153,.72))}.solver-line{margin-top:12px;padding-top:10px;border-top:1px solid var(--border);font:10px var(--mono);color:var(--muted);overflow-wrap:anywhere}@media(max-width:600px){.solver-meter{grid-template-columns:105px 1fr 38px}}';
  document.head.appendChild(style);

  const safe = (value, fallback = 'unavailable') => value === null || value === undefined || value === '' ? fallback : String(value);
  const pct = (value) => Math.max(0, Math.min(100, Math.round(Number(value || 0) * 100)));

  function failClosed(message) {
    host.dataset.state = 'unavailable';
    host.innerHTML = `<div class="solver-head"><strong>Solver preview unavailable</strong><span>PREVIEW ONLY</span></div><p class="muted">${message} No result, verification, unit, authority, execution, or receipt claim is inferred.</p>`;
  }

  function valid(data) {
    return data && data.payload_type === 'solver_response_preview' && data.preview_only === true && data.live_solver_execution === false && data.authority_granted === false && data.execution_enabled === false && data.receipt_issued_by_site === false && data.request && data.result && Array.isArray(data.proof_steps) && data.verification && data.limits && data.display;
  }

  function meter(label, value) {
    const amount = pct(value);
    return `<div class="solver-meter"><span>${label}</span><div class="solver-track"><i style="--solver-value:${amount}%"></i></div><b>${amount}%</b></div>`;
  }

  function render(data) {
    if (!valid(data)) return failClosed('Fixture contract validation failed.');
    if (data.limits.steps_used > data.limits.max_steps) return failClosed('Fixture exceeded declared resource limits.');
    if (data.verification.passed !== true) return failClosed('Fixture verification did not pass.');

    host.dataset.state = 'preview';
    const steps = data.proof_steps.map((step) => `<div class="solver-step"><small>Step ${safe(step.index)}</small><strong>${safe(step.statement)}</strong><span>${safe(step.operation)} → ${safe(step.result)}</span></div>`).join('');
    host.innerHTML = `
      <div class="solver-head"><div><strong>Solver result posture</strong><span>${safe(data.display.summary)}</span></div><span class="solver-badge">FIXTURE · VERIFIED LOCALLY</span></div>
      <div class="solver-grid">
        <div><small>Expression</small><strong>${safe(data.request.expression)}</strong><span>${safe(data.request.operation_class)}</span></div>
        <div><small>Answer</small><strong>${safe(data.result.answer)}</strong><span>${safe(data.result.answer_type)}</span></div>
        <div><small>Units</small><strong>${safe(data.result.units, 'none')}</strong><span>explicit unit posture</span></div>
        <div><small>Verification</small><strong>${data.verification.passed ? 'PASS' : 'FAIL'}</strong><span>${safe(data.verification.method)}</span></div>
        <div><small>Independent engine</small><strong>${data.verification.independent_engine ? 'YES' : 'NO'}</strong><span>fixture verification only</span></div>
        <div><small>Resource limit</small><strong>${safe(data.limits.steps_used)} / ${safe(data.limits.max_steps)} steps</strong><span>allowlisted=${safe(data.limits.operation_allowlisted)}</span></div>
      </div>
      <div class="solver-steps">${steps}</div>
      <div class="solver-meters">
        ${meter('Step completion', data.display.bands.step_completion)}
        ${meter('Verification', data.display.bands.verification)}
        ${meter('Resource use', data.display.bands.resource_use)}
      </div>
      <div class="solver-line">substitution=${safe(data.verification.substitution)} · left=${safe(data.verification.left_value)} · right=${safe(data.verification.right_value)} · live_solver_execution=false · authority=none · receipt=not-issued · confidence=${safe(data.display.confidence_posture)}</div>`;
  }

  fetch(FIXTURE, { cache: 'no-store' })
    .then((response) => {
      if (!response.ok) throw new Error(`fixture HTTP ${response.status}`);
      return response.json();
    })
    .then(render)
    .catch(() => failClosed('Fixture could not be loaded.'));
})();
