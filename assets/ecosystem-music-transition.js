(() => {
  'use strict';

  const runtime = window.StegMusicRuntime;
  if (!runtime || typeof runtime.selectGeneratedTrack !== 'function') return;

  const originalSelect = runtime.selectGeneratedTrack.bind(runtime);
  const $ = id => document.getElementById(id);
  let pending = null;
  let timer = null;

  const emit = (type, human, governed) => window.dispatchEvent(new CustomEvent('stegmusic:emit', {
    detail: {type, human, governed}
  }));

  function isPlaying() {
    const button = $('playPause');
    return Boolean(button && button.textContent.trim().toLowerCase() === 'pause');
  }

  function boundedDelayMs() {
    const progress = Number(($('progress') && $('progress').value) || 0);
    const phaseSize = 25;
    const remainder = progress % phaseSize;
    const percentToBoundary = remainder === 0 ? phaseSize : phaseSize - remainder;
    return Math.max(250, Math.min(2200, Math.round(percentToBoundary / phaseSize * 1800)));
  }

  function executePending() {
    if (!pending) return;
    const request = pending;
    pending = null;
    timer = null;
    originalSelect(request.index, {
      ...request.selection,
      reason: request.selection.reason || 'bounded_transition',
      details: {
        ...(request.selection.details || {}),
        transition_scheduler: {
          strategy: 'phase_boundary_bounded_delay',
          delay_ms: request.delayMs,
          audio_context_reused: true,
          authority: 'none'
        }
      }
    });
    emit('stegdj_transition_executed', 'StegDJ executed the queued bounded transition.', {
      rights_status: 'stegdj_generated_local_prototype',
      source_class: 'browser_local_transition_scheduler',
      captured_records: [{target_track_index: request.index, delay_ms: request.delayMs}],
      derived_records: [{strategy: 'phase_boundary_bounded_delay', audio_context_reused: true, authority: 'none'}],
      contribution_eligibility: 'candidate',
      royalty_state: 'not_realized',
      policy_refs: ['stegdj-transition-smoothing-v1', 'governed-service-envelope-v0']
    });
  }

  function schedule(index, selection = {}) {
    if (!isPlaying() || selection.reason === 'explicit_user_selection' || selection.reason === 'transition_replay') {
      return originalSelect(index, selection);
    }

    const delayMs = boundedDelayMs();
    pending = {index, selection, delayMs};
    window.clearTimeout(timer);
    timer = window.setTimeout(executePending, delayMs);

    emit('stegdj_transition_scheduled', 'StegDJ queued the next generated track at a bounded phase boundary.', {
      rights_status: 'stegdj_generated_local_prototype',
      source_class: 'browser_local_transition_scheduler',
      captured_records: [{target_track_index: index, current_progress: Number(($('progress') && $('progress').value) || 0)}],
      derived_records: [{strategy: 'phase_boundary_bounded_delay', delay_ms: delayMs, maximum_delay_ms: 2200, authority: 'none'}],
      contribution_eligibility: 'candidate',
      royalty_state: 'not_realized',
      policy_refs: ['stegdj-transition-smoothing-v1', 'governed-service-envelope-v0']
    });

    const recommendation = $('adaptiveRecommendation');
    if (recommendation) recommendation.textContent += ` Transition queued for a bounded phrase boundary (${delayMs} ms).`;
    return {scheduled: true, delay_ms: delayMs};
  }

  window.StegMusicRuntime.selectGeneratedTrack = schedule;
  window.StegMusicTransitionScheduler = Object.freeze({
    strategy: 'phase_boundary_bounded_delay',
    maximum_delay_ms: 2200,
    audio_context_reused: true,
    authority: 'none'
  });
})();
