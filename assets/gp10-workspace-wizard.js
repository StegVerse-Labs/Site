(() => {
  'use strict';
  const steps = [...document.querySelectorAll('[data-gp10-step]')];
  const progress = document.getElementById('gp10Progress');
  const status = document.getElementById('status');
  const DRAFT_KEY = 'gp10.workspace.guided.draft.v1';
  let current = 0;

  const $ = (id) => document.getElementById(id);
  const fieldIds = [
    'candidateId','unitNumber','donorLineage','coreGrade','retrofitTier','validationState',
    'unresolvedConditions','stopConditions','evidenceRefs','currency','totalCost','quotePrice',
    'contingencyAmount','warrantyReserve','contributionCost','turnaroundDays','stopLossAmount',
    'thresholdId','minGrossMargin','minContributionMargin','maxContingency','minWarrantyReserve',
    'maxTurnaround','maxStopLoss'
  ];

  function choiceBlock(id, question, yesText, noText) {
    const wrapper = document.createElement('div');
    wrapper.className = 'field wide';
    wrapper.innerHTML = `<span>${question}</span><select id="${id}"><option value="NO">${noText}</option><option value="YES">${yesText}</option></select>`;
    return wrapper;
  }

  function installGate(stepIndex, gateId, question, yesText, noText) {
    const step = steps[stepIndex];
    const grid = step?.querySelector('.grid');
    if (!step || !grid || $(gateId)) return;
    grid.parentNode.insertBefore(choiceBlock(gateId, question, yesText, noText), grid);
    grid.dataset.conditionalFields = gateId;
    const toggle = () => {
      const enabled = $(gateId).value === 'YES';
      grid.hidden = !enabled;
      step.querySelectorAll('.actions').forEach((actions, index) => {
        if (stepIndex === 2 && index === 0) actions.hidden = !enabled;
      });
      if (!enabled && stepIndex === 4) clearThresholds();
    };
    $(gateId).addEventListener('change', () => { toggle(); saveDraft(); });
    toggle();
  }

  function clearThresholds() {
    ['thresholdId','minGrossMargin','minContributionMargin','maxContingency','minWarrantyReserve','maxTurnaround','maxStopLoss'].forEach(id => { if ($(id)) $(id).value = ''; });
  }

  function hardStop() {
    return $('coreGrade')?.value === 'C' || String($('stopConditions')?.value || '').trim().length > 0;
  }

  function nextIndex(index) {
    if (index === 2 && hardStop()) return 5;
    return Math.min(index + 1, steps.length - 1);
  }

  function previousIndex(index) {
    if (index === 5 && hardStop()) return 2;
    return Math.max(index - 1, 0);
  }

  function activePath() {
    return hardStop() ? [0, 1, 2, 5] : [0, 1, 2, 3, 4, 5];
  }

  function renderSummary() {
    const decision = $('decision');
    if (!decision) return;
    let summary = $('guidedSummary');
    if (!summary) {
      summary = document.createElement('div');
      summary.id = 'guidedSummary';
      summary.className = 'transition-card';
      decision.parentNode.insertBefore(summary, decision);
    }
    const evidenceChoice = $('hasEvidence')?.value === 'YES' ? 'Evidence import selected' : 'No file import selected';
    const economicsChoice = hardStop() ? 'Commercial-detail steps skipped because a hard stop is present' : ($('hasEconomics')?.value === 'YES' ? 'Project numbers entered or available' : 'Project numbers not yet available');
    const thresholdChoice = hardStop() ? 'Threshold profile not applied to a hard-stop path' : ($('hasThresholdProfile')?.value === 'YES' ? 'Local threshold profile entered' : 'No threshold profile entered');
    summary.innerHTML = `<strong>Review path</strong><p>${escapeHtml($('candidateId')?.value || 'Unassigned candidate')} · ${escapeHtml($('unitNumber')?.value || 'Unknown unit')} · ${escapeHtml($('coreGrade')?.value || 'UNASSESSED')}</p><p class="muted">${escapeHtml(evidenceChoice)}<br>${escapeHtml(economicsChoice)}<br>${escapeHtml(thresholdChoice)}</p>`;
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[char]));
  }

  function show(index) {
    current = Math.max(0, Math.min(index, steps.length - 1));
    steps.forEach((step, i) => {
      step.hidden = i !== current;
      step.setAttribute('aria-hidden', i === current ? 'false' : 'true');
    });
    const path = activePath();
    const position = Math.max(0, path.indexOf(current));
    if (progress) progress.textContent = `Step ${position + 1} of ${path.length} · ${steps[current].dataset.stepName}`;
    if (current === 5) renderSummary();
    saveDraft();
    window.scrollTo({top: 0, behavior: 'smooth'});
  }

  function requiredComplete(step) {
    const missing = [...step.querySelectorAll('[required]')].find(field => !String(field.value || '').trim());
    if (!missing) return true;
    missing.focus();
    if (status) status.textContent = 'Complete the required field before continuing.';
    return false;
  }

  function saveDraft() {
    const values = {current};
    fieldIds.concat(['hasEvidence','hasEconomics','hasThresholdProfile']).forEach(id => {
      const field = $(id);
      if (field) values[id] = field.value;
    });
    localStorage.setItem(DRAFT_KEY, JSON.stringify(values));
  }

  function restoreDraft() {
    let draft = null;
    try { draft = JSON.parse(localStorage.getItem(DRAFT_KEY) || 'null'); } catch { draft = null; }
    if (!draft) return;
    Object.entries(draft).forEach(([id, value]) => {
      const field = $(id);
      if (field && typeof value === 'string') field.value = value;
    });
    ['hasEvidence','hasEconomics','hasThresholdProfile'].forEach(id => $(id)?.dispatchEvent(new Event('change')));
    current = Number.isInteger(draft.current) ? draft.current : 0;
  }

  installGate(2, 'hasEvidence', 'Do you have an authorized record to import now?', 'Yes — show import fields', 'No — continue without a file');
  installGate(3, 'hasEconomics', 'Do you have project numbers available now?', 'Yes — show project-number fields', 'No — keep the numbers missing');
  installGate(4, 'hasThresholdProfile', 'Does a real approved threshold profile already exist?', 'Yes — show threshold fields', 'No — skip these fields');

  document.addEventListener('click', event => {
    const next = event.target.closest('[data-next-step]');
    const back = event.target.closest('[data-prev-step]');
    if (next) {
      event.preventDefault();
      if (requiredComplete(steps[current])) show(nextIndex(current));
    }
    if (back) {
      event.preventDefault();
      show(previousIndex(current));
    }
  });

  document.addEventListener('change', saveDraft);
  document.addEventListener('input', saveDraft);
  $('newRecord')?.addEventListener('click', () => {
    localStorage.removeItem(DRAFT_KEY);
    setTimeout(() => show(0), 0);
  });

  restoreDraft();
  show(current);
})();