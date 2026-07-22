(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const now = () => new Date().toISOString();
  const download = (name, payload) => {
    const blob = new Blob([JSON.stringify(payload, null, 2)], {type:'application/json'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = name;
    link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  };
  const latest = key => { try { return JSON.parse(localStorage.getItem(key) || 'null'); } catch { return null; } };

  function install() {
    const decision = $('decision');
    if (!decision || $('validationFeedback')) return;
    const panel = document.createElement('section');
    panel.id = 'validationFeedback';
    panel.className = 'transition-card';
    panel.innerHTML = `
      <h3>Record what was confusing</h3>
      <p class="muted">Optional. This creates a separate browser-local usability record. It does not change the candidate decision.</p>
      <div class="grid">
        <label class="field"><span>Could you complete the flow?</span><select id="feedbackCompletion"><option>YES</option><option>PARTLY</option><option>NO</option></select></label>
        <label class="field"><span>Was the next question clear?</span><select id="feedbackClarity"><option>YES</option><option>MOSTLY</option><option>NO</option></select></label>
        <label class="field wide"><span>What was confusing or missing?</span><textarea id="feedbackConfusion" placeholder="Example: I did not know which source authority to choose."></textarea></label>
        <label class="field wide"><span>What should be removed or simplified?</span><textarea id="feedbackSimplify" placeholder="Example: Hide warranty reserve until a quote exists."></textarea></label>
      </div>
      <div class="actions" style="margin-top:14px"><button class="sv-btn sv-btn-secondary" id="exportFeedback" type="button">Export test feedback</button></div>
      <p id="feedbackStatus" class="status" aria-live="polite"></p>`;
    decision.parentNode.insertBefore(panel, decision.nextSibling);
    $('exportFeedback').addEventListener('click', () => {
      const candidate = latest('gp10.workspace.records.v1.latest');
      const draft = latest('gp10.workspace.guided.draft.v1');
      const payload = {
        feedback_version:'1.0.0',
        created_at:now(),
        candidate_id:candidate?.candidate?.candidate_id || draft?.candidateId || null,
        completion:$('feedbackCompletion').value,
        next_question_clarity:$('feedbackClarity').value,
        confusing_or_missing:$('feedbackConfusion').value.trim() || null,
        remove_or_simplify:$('feedbackSimplify').value.trim() || null,
        active_path:{
          evidence_selected:draft?.hasEvidence || null,
          economics_selected:draft?.hasEconomics || null,
          threshold_selected:draft?.hasThresholdProfile || null,
          core_grade:draft?.coreGrade || null,
          stop_conditions_present:Boolean(String(draft?.stopConditions || '').trim())
        },
        latest_posture:candidate?.decision?.posture || null,
        custody_state:'BROWSER_LOCAL_UNCUSTODIED',
        execution_authority:false,
        warning:'Usability feedback only; not evidence, approval, or execution authority.'
      };
      download(`gp10-test-feedback-${new Date().toISOString().slice(0,10)}.json`, payload);
      $('feedbackStatus').textContent = 'Test feedback exported. It does not alter the candidate record.';
    });
  }

  install();
})();