(() => {
  'use strict';

  const PROFILE_URL = 'assets/stegmusic-style-characteristics.json';
  let registryPromise;
  let activeProfile = null;

  const normalize = value => String(value || '').trim().toLowerCase();
  const emit = (type, human, captured = {}, derived = {}) => window.dispatchEvent(new CustomEvent('stegmusic:emit', {
    detail: {
      type,
      human,
      governed: {
        rights_status: 'not_applicable',
        source_class: 'style_characteristic_resolution',
        captured_records: [captured],
        derived_records: [derived],
        contribution_eligibility: 'not_evaluated',
        royalty_state: 'not_realized',
        fixture: false,
        policy_refs: ['stegmusic-style-characteristics-v1']
      }
    }
  }));

  async function loadRegistry() {
    if (!registryPromise) {
      registryPromise = fetch(PROFILE_URL, { cache: 'no-cache' }).then(response => {
        if (!response.ok) throw new Error(`Style registry unavailable (${response.status}).`);
        return response.json();
      });
    }
    return registryPromise;
  }

  function scoreEdmBassDrop(text) {
    const terms = {
      edm: 4, electronic: 2, dance: 2, bass: 3, 'bass drop': 5, drop: 3,
      energetic: 3, energy: 2, 'high energy': 5, festival: 2, mainstage: 2,
      dubstep: 3, 'bass house': 3, 'drum and bass': 3, dnb: 3, trap: 2
    };
    return Object.entries(terms).reduce((score, [term, weight]) => score + (text.includes(term) ? weight : 0), 0);
  }

  async function resolve(input) {
    const registry = await loadRegistry();
    const text = normalize(input);
    const candidates = [];
    const edm = registry.profiles?.edm_high_energy_bass_drop;
    if (edm) candidates.push({ id: 'edm_high_energy_bass_drop', score: scoreEdmBassDrop(text), profile: edm });
    candidates.sort((a, b) => b.score - a.score);
    const winner = candidates[0];
    if (!winner || winner.score < 4) {
      emit('stegmusic_style_profile_unresolved', 'No governed style profile met the resolution threshold.', {
        input: String(input || ''), registry_id: registry.registry_id,
        candidate_scores: candidates.map(candidate => ({ id: candidate.id, score: candidate.score }))
      }, { result: 'UNRESOLVED', authority: 'none', user_clarification_required: true });
      return null;
    }
    const result = Object.freeze({
      profile_id: winner.id,
      display_name: winner.profile.display_name,
      genre_family: winner.profile.genre_family,
      characteristics: winner.profile.characteristics,
      required_events: winner.profile.required_events,
      preferred_sound_design: winner.profile.preferred_sound_design,
      avoid: winner.profile.avoid,
      resolver_defaults: winner.profile.resolver_defaults,
      score: winner.score,
      registry_id: registry.registry_id,
      registry_schema_version: registry.schema_version
    });
    emit('stegmusic_style_profile_resolved', `Resolved “${String(input || '')}” to ${result.display_name}.`, {
      input: String(input || ''), profile_id: result.profile_id, score: result.score,
      registry_id: result.registry_id, characteristics: result.characteristics,
      required_events: result.required_events
    }, {
      result: 'RESOLVED', genre_label_is_not_render_authority: true,
      explicit_characteristics_control_rendering: true, user_override_allowed: true,
      human_audibility_confirmed: false
    });
    return result;
  }

  function setControl(id, value) {
    const control = document.getElementById(id);
    if (!control || !Number.isFinite(Number(value))) return;
    control.value = String(Math.max(Number(control.min || 0), Math.min(Number(control.max || 100), Number(value))));
    control.dispatchEvent(new Event('input', { bubbles: true }));
    control.dispatchEvent(new Event('change', { bubbles: true }));
  }

  function applyProfile(profile) {
    if (!profile) return null;
    const c = profile.characteristics;
    setControl('energy', c.energy);
    setControl('bass', c.bass_weight);
    setControl('brightness', c.brightness);
    setControl('exploration', Math.round((c.harmonic_complexity + c.melodic_activity) / 2));
    activeProfile = profile;
    const recommendation = document.getElementById('adaptiveRecommendation');
    if (recommendation) recommendation.textContent = `${profile.display_name} · energy ${c.energy} · bass ${c.bass_weight} · drop prominence ${c.drop_prominence} · ${c.tempo_bpm.preferred} BPM target`;
    emit('stegmusic_style_profile_applied', `Applied ${profile.display_name} to StegMusic controls.`, {
      profile_id: profile.profile_id,
      applied_controls: {
        energy: c.energy,
        bass: c.bass_weight,
        brightness: c.brightness,
        exploration: Math.round((c.harmonic_complexity + c.melodic_activity) / 2)
      },
      tempo_preferred_bpm: c.tempo_bpm.preferred,
      drop_prominence: c.drop_prominence,
      required_events: profile.required_events
    }, {
      render_contract: 'explicit_characteristics',
      user_override_allowed: true,
      source_bytes_uploaded: false,
      human_audibility_confirmed: false
    });
    return profile;
  }

  async function resolveCurrentPreference({ apply = true } = {}) {
    const freeText = document.getElementById('feedbackText')?.value || '';
    const searchText = document.getElementById('musicSearch')?.value || '';
    const profile = await resolve([searchText, freeText].filter(Boolean).join(' '));
    return apply ? applyProfile(profile) : profile;
  }

  function bind() {
    ['searchButton', 'applyFeedback'].forEach(id => {
      document.getElementById(id)?.addEventListener('click', () => {
        window.setTimeout(() => resolveCurrentPreference().catch(error => emit(
          'stegmusic_style_profile_error',
          `Style profile resolution failed: ${error.message}`,
          { error: error.message },
          { authority: 'none' }
        )), 0);
      });
    });
  }

  window.StegMusicStyleResolver = Object.freeze({
    registryUrl: PROFILE_URL,
    loadRegistry,
    resolve,
    applyProfile,
    resolveCurrentPreference,
    getActiveProfile: () => activeProfile
  });
  bind();
})();
