(() => {
  const recordsEl = document.getElementById('records');
  const summaryEl = document.getElementById('summary');
  const statusEl = document.getElementById('status');
  const executorEl = document.getElementById('executor-status');
  const searchEl = document.getElementById('search');
  const stateEl = document.getElementById('state');
  const originEl = document.getElementById('origin');
  let records = [];
  let importStatus = null;
  let executorStatus = null;

  const esc = (value) => String(value ?? '—').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

  function metric(label, value) {
    return `<div class="metric"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`;
  }

  function renderSummary(items) {
    const completed = items.filter((item) => item.lifecycle_state === 'COMPLETED').length;
    const pendingCustody = items.filter((item) => item.master_record_status !== 'RECORDED').length;
    const pendingReconstruction = items.filter((item) => !['PASS','PARTIAL','FAIL'].includes(item.reconstruction_status)).length;
    summaryEl.innerHTML = [
      metric('Visible transitions', items.length),
      metric('Completed', completed),
      metric('Custody pending', pendingCustody),
      metric('Reconstruction pending', pendingReconstruction),
      metric('Native executor', executorStatus?.activation?.state || 'UNAVAILABLE'),
    ].join('');
  }

  function renderExecutor() {
    if (!executorStatus) {
      executorEl.innerHTML = '<p>Executor projection unavailable.</p>';
      return;
    }
    const source = executorStatus.from_executor || {};
    const target = executorStatus.to_executor || {};
    const activation = executorStatus.activation || {};
    executorEl.innerHTML = `<article class="card">
      <div class="row">
        <div><span class="eyebrow">Receipted orchestration projection</span><h2>Native StegVerse AI executor</h2></div>
        <span class="tag ${activation.state === 'ACTIVE' ? 'complete' : 'pending'}">${esc(activation.state)}</span>
      </div>
      <dl>
        <dt>Native executor</dt><dd>${esc(target.executor_id)}</dd>
        <dt>Native status</dt><dd>${esc(target.status)}</dd>
        <dt>Bootstrap executor</dt><dd>${esc(source.executor_id)}</dd>
        <dt>Bootstrap status</dt><dd>${esc(source.status)}</dd>
        <dt>Activation receipt</dt><dd>${esc(activation.activation_receipt_id)}</dd>
        <dt>Transition</dt><dd>${esc(executorStatus.transition_id)}</dd>
        <dt>Run</dt><dd>${esc(executorStatus.run_id)}</dd>
      </dl>
      <p class="lede">Activation indicates eligibility to receive governed work. It does not grant per-transition execution, publication, admissibility, receipt-signing, or Master-Records authority.</p>
    </article>`;
  }

  function card(item) {
    const relationships = item.relationships || {};
    const stateClass = item.lifecycle_state === 'COMPLETED' ? 'complete' : 'pending';
    return `<article class="card">
      <div class="row">
        <div><span class="eyebrow">${esc(item.origin_class)}</span><h2>${esc(item.transition_id)}</h2></div>
        <div><span class="tag ${stateClass}">${esc(item.lifecycle_state)}</span></div>
      </div>
      <dl>
        <dt>Repository</dt><dd>${esc(item.repository_ref)}</dd>
        <dt>Task</dt><dd>${esc(item.task_ref)}</dd>
        <dt>Actor</dt><dd>${esc(item.actor_ref)}</dd>
        <dt>Run</dt><dd>${esc(item.run_id)}</dd>
        <dt>Handoff</dt><dd>${esc(relationships.handoff_ref)}</dd>
        <dt>Event</dt><dd>${esc(relationships.event_id)}</dd>
        <dt>Admissibility</dt><dd>${esc(item.admissibility_result)}</dd>
        <dt>Commit validity</dt><dd>${esc(item.commit_time_validity)}</dd>
        <dt>Verification</dt><dd>${esc(item.verification_ref)}</dd>
        <dt>Final receipt</dt><dd>${esc(item.final_receipt_id)}</dd>
        <dt>Master-Records</dt><dd>${esc(item.master_record_status)}</dd>
        <dt>Reconstruction</dt><dd>${esc(item.reconstruction_status)}</dd>
        <dt>Next task</dt><dd>${esc(relationships.next_task_ref)}</dd>
      </dl>
    </article>`;
  }

  function render() {
    const query = searchEl.value.trim().toLowerCase();
    const state = stateEl.value;
    const origin = originEl.value;
    const visible = records.filter((item) => {
      const haystack = JSON.stringify(item).toLowerCase();
      return (!query || haystack.includes(query)) && (!state || item.lifecycle_state === state) && (!origin || item.origin_class === origin);
    });
    renderSummary(visible);
    renderExecutor();
    recordsEl.innerHTML = visible.map(card).join('') || '<p>No transitions match the current filters.</p>';
    const provenance = importStatus
      ? `${importStatus.state}; source=${importStatus.source}; hash_verified=${importStatus.hash_verified}; executor_state_imported=${importStatus.executor_state_imported}; live_feed=${importStatus.live_orchestration_feed}`
      : 'import status unavailable';
    statusEl.textContent = `${visible.length} of ${records.length} transition records shown. Projection provenance: ${provenance}.`;
  }

  function fill(select, values) {
    [...new Set(values)].sort().forEach((value) => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = value;
      select.appendChild(option);
    });
  }

  Promise.all([
    fetch('data/governed-transition-index.json', {cache: 'no-store'}),
    fetch('data/governed-transition-index-import-status.json', {cache: 'no-store'}),
    fetch('data/governed-executor-status.json', {cache: 'no-store'}),
  ])
    .then(async ([indexResponse, statusResponse, executorResponse]) => {
      if (!indexResponse.ok) throw new Error(`index HTTP ${indexResponse.status}`);
      if (!statusResponse.ok) throw new Error(`import status HTTP ${statusResponse.status}`);
      if (!executorResponse.ok) throw new Error(`executor status HTTP ${executorResponse.status}`);
      return [await indexResponse.json(), await statusResponse.json(), await executorResponse.json()];
    })
    .then(([data, status, executor]) => {
      if (data.projection_type !== 'governed_transition_index' || !Array.isArray(data.records)) {
        throw new Error('projection contract mismatch');
      }
      if (status.status_type !== 'governed_transition_index_import_status') {
        throw new Error('import status contract mismatch');
      }
      if (executor.projection_type !== 'governed_executor_status') {
        throw new Error('executor projection contract mismatch');
      }
      records = data.records.filter((item) => item.site_visibility !== 'HIDDEN');
      importStatus = status;
      executorStatus = executor;
      fill(stateEl, records.map((item) => item.lifecycle_state));
      fill(originEl, records.map((item) => item.origin_class));
      render();
    })
    .catch((error) => {
      statusEl.innerHTML = `<span class="error">Transition projection unavailable: ${esc(error.message)}</span>`;
    });

  [searchEl, stateEl, originEl].forEach((element) => element.addEventListener('input', render));
})();
