(() => {
  'use strict';

  const STORAGE_KEY = 'gp10.workspace.records.v1';
  const $ = (id) => document.getElementById(id);
  const fields = [
    'candidateId','unitNumber','donorLineage','coreGrade','retrofitTier','validationState',
    'evidenceRefs','unresolvedConditions','stopConditions','currency','totalCost','quotePrice',
    'contingencyAmount','warrantyReserve','contributionCost','turnaroundDays','stopLossAmount',
    'thresholdId','minGrossMargin','minContributionMargin','maxContingency','minWarrantyReserve',
    'maxTurnaround','maxStopLoss'
  ];

  const lines = (value) => String(value || '').split(/\r?\n/).map(v => v.trim()).filter(Boolean);
  const numberOrNull = (value) => value === '' || value == null ? null : Number(value);
  const finite = (value) => typeof value === 'number' && Number.isFinite(value);
  const percent = (numerator, denominator) => finite(numerator) && finite(denominator) && denominator > 0
    ? Number(((numerator / denominator) * 100).toFixed(2)) : null;

  function collect() {
    const totalCost = numberOrNull($('totalCost').value);
    const quotePrice = numberOrNull($('quotePrice').value);
    const contingencyAmount = numberOrNull($('contingencyAmount').value);
    const warrantyReserve = numberOrNull($('warrantyReserve').value);
    const contributionCost = numberOrNull($('contributionCost').value);
    const turnaroundDays = numberOrNull($('turnaroundDays').value);
    const stopLossAmount = numberOrNull($('stopLossAmount').value);

    const metrics = {
      modeled_total_cost: totalCost,
      modeled_quote_price: quotePrice,
      gross_margin_percent: finite(totalCost) && finite(quotePrice) && quotePrice > 0 ? Number((((quotePrice - totalCost) / quotePrice) * 100).toFixed(2)) : null,
      contribution_margin_percent: finite(contributionCost) && finite(quotePrice) && quotePrice > 0 ? Number((((quotePrice - contributionCost) / quotePrice) * 100).toFixed(2)) : null,
      contingency_percent: percent(contingencyAmount, totalCost),
      warranty_reserve_percent: percent(warrantyReserve, quotePrice),
      turnaround_days: turnaroundDays,
      stop_loss_amount: stopLossAmount
    };

    const thresholdId = $('thresholdId').value.trim();
    const threshold = thresholdId ? {
      profile_id: thresholdId,
      local_entry_only: true,
      approval_verified: false,
      thresholds: {
        minimum_gross_margin_percent: numberOrNull($('minGrossMargin').value),
        minimum_contribution_margin_percent: numberOrNull($('minContributionMargin').value),
        maximum_contingency_percent: numberOrNull($('maxContingency').value),
        minimum_warranty_reserve_percent: numberOrNull($('minWarrantyReserve').value),
        maximum_turnaround_days: numberOrNull($('maxTurnaround').value),
        maximum_stop_loss_amount: numberOrNull($('maxStopLoss').value)
      },
      execution_authority: false
    } : null;

    return {
      record_version: '1.0.0',
      record_id: `LOCAL-${crypto.randomUUID ? crypto.randomUUID() : Date.now()}`,
      created_at: new Date().toISOString(),
      source_surface: 'gp10-workspace.html',
      custody_state: 'BROWSER_LOCAL_UNCUSTODIED',
      candidate: {
        candidate_id: $('candidateId').value.trim(),
        unit_number: $('unitNumber').value.trim() || null,
        donor_lineage: $('donorLineage').value,
        core_grade: $('coreGrade').value,
        retrofit_tier: $('retrofitTier').value,
        evidence_refs: lines($('evidenceRefs').value),
        unresolved_conditions: lines($('unresolvedConditions').value),
        stop_conditions: lines($('stopConditions').value)
      },
      economics: {
        model_id: `LOCAL-ECON-${$('candidateId').value.trim() || 'UNASSIGNED'}`,
        validation_state: $('validationState').value,
        currency: $('currency').value.trim().toUpperCase() || 'USD',
        metrics
      },
      threshold_profile: threshold,
      decision: null,
      execution_authority: false,
      warnings: [
        'Browser-local record; not repository custody.',
        'No condition, fitment, safety, compliance, pricing, profit, approval, or execution claim is established.'
      ]
    };
  }

  function evaluate(record) {
    const c = record.candidate;
    const e = record.economics;
    const m = e.metrics;
    const reasons = [];
    const required_actions = [];
    let posture = 'PROCEED';

    if (c.stop_conditions.length || c.core_grade === 'C') {
      posture = 'REJECT';
      reasons.push('Grade C or a stop-work condition excludes ordinary commercial acceptance.');
      required_actions.push('Resolve through qualified review or retain as donor, custom, or research scope.');
    } else if (c.core_grade === 'UNASSESSED') {
      posture = 'DISCOVERY_ONLY';
      reasons.push('No evidence-backed core grade is available.');
      required_actions.push('Complete governed inspection and core grading.');
    } else if (e.validation_state === 'ASSUMPTION_ONLY') {
      posture = 'DISCOVERY_ONLY';
      reasons.push('Assumption-only economics cannot support commercial commitment.');
      required_actions.push('Capture current supplier, labor, transport, warranty, schedule, and customer evidence.');
    } else if (c.core_grade === 'B') {
      posture = 'COST_PLUS';
      reasons.push('Grade B uncertainty requires bounded discovery, allowances, or cost-plus protection.');
      required_actions.push('Define capped discovery, exclusions, allowances, and change-order authority.');
    } else if (c.unresolved_conditions.length || e.validation_state === 'PARTIALLY_SOURCED') {
      posture = 'RE_SCOPE';
      reasons.push(c.unresolved_conditions.length ? 'Unresolved conditions remain outside the bounded standard build.' : 'The economics model remains only partially sourced.');
      required_actions.push('Price, remove, evidence, or explicitly allocate each unresolved assumption or condition.');
    }

    const t = record.threshold_profile;
    const violations = [];
    if (t && posture === 'PROCEED') {
      const requiredMetricMap = [
        ['gross_margin_percent','minimum_gross_margin_percent','min'],
        ['contribution_margin_percent','minimum_contribution_margin_percent','min'],
        ['contingency_percent','maximum_contingency_percent','max'],
        ['warranty_reserve_percent','minimum_warranty_reserve_percent','min'],
        ['turnaround_days','maximum_turnaround_days','max'],
        ['stop_loss_amount','maximum_stop_loss_amount','stoploss']
      ];
      for (const [metricName, thresholdName, direction] of requiredMetricMap) {
        const metric = m[metricName];
        const limit = t.thresholds[thresholdName];
        if (!finite(metric) || !finite(limit)) {
          violations.push(`${metricName}: missing metric or threshold`);
          continue;
        }
        if (direction === 'min' && metric < limit) violations.push(`${metricName}: ${metric} below ${limit}`);
        if (direction === 'max' && metric > limit) violations.push(`${metricName}: ${metric} above ${limit}`);
        if (direction === 'stoploss' && metric > limit) violations.push(`${metricName}: ${metric} exceeds stop-loss ${limit}`);
      }
      if (violations.some(v => v.includes('stop-loss'))) posture = 'REJECT';
      else if (violations.length) posture = 'RE_SCOPE';
      if (violations.length) {
        reasons.push('Local threshold evaluation identified one or more violations.');
        required_actions.push('Use only a repository-validated APPROVED profile and resolve every violation before named review.');
      }
    }

    if (posture === 'PROCEED') {
      reasons.push('Candidate may advance to named governed approval based on entered posture data.');
      required_actions.push('Export, commit through governed intake, verify evidence, and obtain named approval before any execution.');
    }

    record.decision = {
      posture,
      reasons,
      required_actions,
      threshold_violations: violations,
      threshold_profile_verified: false,
      execution_authority: false,
      computed_at: new Date().toISOString()
    };
    return record;
  }

  function save(record) {
    const records = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    records.unshift(record);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(records.slice(0, 50)));
    localStorage.setItem(`${STORAGE_KEY}.latest`, JSON.stringify(record));
  }

  function render(record) {
    const posture = record?.decision?.posture || 'DISCOVERY_ONLY';
    const decision = $('decision');
    decision.dataset.posture = posture;
    decision.querySelector('strong').textContent = posture;
    $('decisionReason').textContent = record?.decision?.reasons?.join(' ') || 'Complete intake to compute a posture.';
    $('recordPreview').textContent = record ? JSON.stringify(record, null, 2) : 'No saved record.';
  }

  function latest() {
    try { return JSON.parse(localStorage.getItem(`${STORAGE_KEY}.latest`) || 'null'); }
    catch { return null; }
  }

  function exportRecord(record) {
    if (!record) return setStatus('No saved record to export.');
    const blob = new Blob([JSON.stringify(record, null, 2)], {type:'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${record.candidate.candidate_id || 'gp10-candidate'}-${record.created_at.slice(0,10)}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    setStatus('JSON export created. Export is not custody or approval.');
  }

  function setStatus(message) { $('status').textContent = message; }

  $('gp10Form').addEventListener('submit', (event) => {
    event.preventDefault();
    const record = evaluate(collect());
    if (!record.candidate.candidate_id) return setStatus('Candidate ID is required.');
    save(record);
    render(record);
    setStatus(`Saved locally: ${record.decision.posture}. No execution authority granted.`);
  });

  $('exportJson').addEventListener('click', () => exportRecord(latest()));
  $('copyJson').addEventListener('click', async () => {
    const record = latest();
    if (!record) return setStatus('No saved record to copy.');
    try {
      await navigator.clipboard.writeText(JSON.stringify(record, null, 2));
      setStatus('JSON copied. Clipboard content is not custody or approval.');
    } catch {
      setStatus('Clipboard access failed; use Export JSON.');
    }
  });
  $('newRecord').addEventListener('click', () => {
    $('gp10Form').reset();
    $('currency').value = 'USD';
    render(null);
    setStatus('New unsaved record.');
  });

  for (const id of fields) {
    $(id).addEventListener('change', () => setStatus('Unsaved changes.'));
  }
  render(latest());
})();