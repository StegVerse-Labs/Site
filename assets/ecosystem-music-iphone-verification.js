(() => {
  'use strict';

  const $ = id => document.getElementById(id);
  const KEY = 'stegmusic.iphone-verification.v1';
  const steps = [
    ['audible', 'Hear generated audio'],
    ['adaptive', 'Confirm Adaptive Next'],
    ['local', 'Play an authorized local file'],
    ['dimmed', 'Confirm dimmed-screen continuity'],
    ['locked', 'Confirm locked-screen continuity'],
    ['resumed', 'Confirm playback after returning']
  ];
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (_) { return {}; } };
  const state = load();
  const save = () => localStorage.setItem(KEY, JSON.stringify(state));
  const emit = (type, human, captured, derived = {}) => window.dispatchEvent(new CustomEvent('stegmusic:emit', { detail: { type, human, governed: { rights_status: 'not_applicable', source_class: 'target_device_verification', captured_records: [captured], derived_records: [derived], contribution_eligibility: 'not_evaluated', royalty_state: 'not_realized', fixture: false } } }));

  function completedCount() { return steps.filter(([id]) => state[id]?.confirmed).length; }
  function nextStep() { return steps.find(([id]) => !state[id]?.confirmed); }
  function mark(id, source = 'direct_human_confirmation') {
    state[id] = { confirmed: true, confirmed_at: new Date().toISOString(), source, user_agent: navigator.userAgent };
    save();
    render();
    emit('iphone_guided_verification_step_completed', `Completed iPhone verification step: ${id}.`, { step: id, ...state[id] }, { direct_human_observation: source === 'direct_human_confirmation', authority: 'none' });
  }
  function exportReceipt() {
    const events = (() => { try { return JSON.parse(localStorage.getItem('stegmusic.events.v1') || '[]'); } catch (_) { return []; } })();
    const payload = {
      schema: 'stegmusic-iphone-verification-receipt-v1',
      exported_at: new Date().toISOString(),
      page: location.href,
      user_agent: navigator.userAgent,
      verification: state,
      completed_steps: completedCount(),
      total_steps: steps.length,
      all_steps_complete: completedCount() === steps.length,
      claims: {
        human_audibility_verified: Boolean(state.audible?.confirmed),
        adaptive_next_verified: Boolean(state.adaptive?.confirmed),
        local_file_playback_verified: Boolean(state.local?.confirmed),
        screen_dim_continuity_verified: Boolean(state.dimmed?.confirmed),
        screen_lock_continuity_verified: Boolean(state.locked?.confirmed),
        return_resume_verified: Boolean(state.resumed?.confirmed),
        authority_effect: 'NONE'
      },
      governed_events: events
    };
    const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = `stegmusic-iphone-verification-${Date.now()}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    emit('iphone_guided_verification_receipt_exported', 'Exported the iPhone playback verification receipt.', { completed_steps: payload.completed_steps, total_steps: payload.total_steps }, { all_steps_complete: payload.all_steps_complete, authority: 'none' });
  }
  function render() {
    const host = $('iphonePlaybackVerification');
    if (!host) return;
    let panel = $('iphoneGuidedVerification');
    if (!panel) {
      panel = document.createElement('div');
      panel.id = 'iphoneGuidedVerification';
      panel.style.marginTop = '12px';
      host.appendChild(panel);
    }
    const next = nextStep();
    panel.innerHTML = `<strong>GUIDED TEST · ${completedCount()}/${steps.length} COMPLETE</strong><div class="status ${next ? 'pending' : 'active'}" id="iphoneGuidedNext">${next ? `NEXT · ${next[1]}` : 'TARGET DEVICE VERIFICATION · COMPLETE'}</div><div class="event-list">${steps.map(([id,label]) => `<div class="event"><strong>${state[id]?.confirmed ? '✓' : '○'} ${label}</strong>${state[id]?.confirmed ? `<br>${state[id].confirmed_at}` : ''}</div>`).join('')}</div><div class="player-actions"><button class="sv-btn sv-btn-primary" id="exportIphoneVerification" type="button">Export verification receipt</button><button class="sv-btn sv-btn-secondary" id="resetIphoneVerification" type="button">Reset guided test</button></div>`;
    $('exportIphoneVerification')?.addEventListener('click', exportReceipt);
    $('resetIphoneVerification')?.addEventListener('click', () => { steps.forEach(([id]) => delete state[id]); save(); render(); emit('iphone_guided_verification_reset', 'Reset the guided iPhone verification checklist.', { reset_at: new Date().toISOString() }, { authority: 'none' }); });
  }

  function bind() {
    const host = $('iphonePlaybackVerification');
    if (!host) return setTimeout(bind, 100);
    host.querySelectorAll('[data-confirm]').forEach(button => button.addEventListener('click', () => mark(button.dataset.confirm), true));
    $('localAudioPlayer')?.addEventListener('play', () => mark('local', 'direct_player_event'));
    render();
  }

  bind();
  window.StegMusicIphoneVerification = Object.freeze({ mark, exportReceipt, getState: () => ({ ...state }) });
})();