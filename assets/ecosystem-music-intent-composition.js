(() => {
  'use strict';

  const $ = id => document.getElementById(id);
  const clamp = value => Math.max(0, Math.min(100, Math.round(value)));
  const PROFILES = Object.freeze({
    fine_tune: {
      label: 'BALANCED LAB',
      phases: {
        INTRO: {energy:-8, brightness:-6, bass:4, exploration:-4},
        BUILD: {energy:4, brightness:0, bass:2, exploration:0},
        LIFT: {energy:12, brightness:8, bass:-2, exploration:6},
        RESOLVE: {energy:-10, brightness:-8, bass:4, exploration:-8}
      }
    },
    stay_alert: {
      label: 'ALERTNESS ARC',
      phases: {
        INTRO: {energy:4, brightness:4, bass:-2, exploration:0},
        BUILD: {energy:12, brightness:8, bass:-4, exploration:4},
        LIFT: {energy:20, brightness:14, bass:-6, exploration:8},
        RESOLVE: {energy:8, brightness:6, bass:-2, exploration:-2}
      }
    },
    focus: {
      label: 'FOCUS PLATEAU',
      phases: {
        INTRO: {energy:-6, brightness:-10, bass:6, exploration:-12},
        BUILD: {energy:0, brightness:-8, bass:8, exploration:-14},
        LIFT: {energy:4, brightness:-4, bass:6, exploration:-10},
        RESOLVE: {energy:-8, brightness:-12, bass:8, exploration:-16}
      }
    },
    settle: {
      label: 'DESCENDING SETTLE',
      phases: {
        INTRO: {energy:-8, brightness:-12, bass:8, exploration:-10},
        BUILD: {energy:-12, brightness:-14, bass:10, exploration:-14},
        LIFT: {energy:-16, brightness:-16, bass:12, exploration:-18},
        RESOLVE: {energy:-22, brightness:-20, bass:14, exploration:-22}
      }
    },
    explore: {
      label: 'BOUNDARY EXPLORATION',
      phases: {
        INTRO: {energy:-2, brightness:2, bass:0, exploration:10},
        BUILD: {energy:6, brightness:8, bass:-2, exploration:18},
        LIFT: {energy:12, brightness:14, bass:-4, exploration:26},
        RESOLVE: {energy:-4, brightness:0, bass:2, exploration:12}
      }
    }
  });

  let base = null;
  let lastApplied = null;

  function controls() {
    return {
      energy: Number($('energy')?.value || 0),
      brightness: Number($('brightness')?.value || 0),
      bass: Number($('bass')?.value || 0),
      exploration: Number($('exploration')?.value || 0)
    };
  }

  function captureBase() { base = controls(); }

  function currentPhase() {
    const text = $('compositionPhase')?.textContent || 'COMPOSITION · INTRO';
    return text.split('·').pop().trim().toUpperCase();
  }

  function emit(intent, phase, applied) {
    window.dispatchEvent(new CustomEvent('stegmusic:emit', {
      detail: {
        type: 'composition_intent_profile_applied',
        human: `Applied ${PROFILES[intent].label} structure for ${phase}.`,
        governed: {
          rights_status: 'stegdj_generated_local_prototype',
          source_class: 'browser_local_composition_controller',
          captured_records: [{session_intent:intent, composition_phase:phase, base_controls:base}],
          derived_records: [{structure_profile:PROFILES[intent].label, applied_controls:applied, phase_specific:true}],
          contribution_eligibility: 'candidate',
          royalty_state: 'not_realized',
          policy_refs: ['stegdj-intent-composition-v1','governed-service-envelope-v0'],
          authority: 'none'
        }
      }
    }));
  }

  function apply(reason='phase_change') {
    const intent = $('sessionIntent')?.value || 'fine_tune';
    const profile = PROFILES[intent] || PROFILES.fine_tune;
    const phase = currentPhase();
    const offsets = profile.phases[phase] || profile.phases.INTRO;
    if (!base) captureBase();
    const applied = {};
    for (const key of ['energy','brightness','bass','exploration']) {
      const element = $(key);
      if (!element) continue;
      applied[key] = clamp(base[key] + offsets[key]);
      element.value = String(applied[key]);
    }
    const marker = `${intent}:${phase}:${JSON.stringify(applied)}`;
    const label = $('intentCompositionStatus');
    if (label) label.textContent = `INTENT FORM · ${profile.label} · ${phase}`;
    if (marker !== lastApplied) {
      lastApplied = marker;
      emit(intent, phase, applied);
    }
  }

  function installStatus() {
    if ($('intentCompositionStatus')) return;
    const phase = $('compositionPhase');
    if (!phase) return;
    const status = document.createElement('span');
    status.id = 'intentCompositionStatus';
    status.className = 'license';
    status.setAttribute('role','status');
    status.setAttribute('aria-live','polite');
    status.textContent = 'INTENT FORM · WAITING';
    phase.insertAdjacentElement('afterend', status);
  }

  function bind() {
    installStatus();
    captureBase();
    $('sessionIntent')?.addEventListener('change', () => { captureBase(); apply('intent_change'); });
    ['energy','brightness','bass','exploration'].forEach(id => $(id)?.addEventListener('change', captureBase));
    const phase = $('compositionPhase');
    if (phase) new MutationObserver(() => apply('phase_change')).observe(phase, {childList:true, characterData:true, subtree:true});
    apply('initial');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bind); else bind();
  window.StegMusicIntentComposition = Object.freeze({profiles:PROFILES, apply, authority:'none', model_scope:'active_profile'});
})();