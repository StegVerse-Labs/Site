(() => {
  'use strict';

  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, Number(value) || 0));
  const STANDARD_VERSION = 'stegmusic-string-component-v1';

  const DEFAULTS = Object.freeze({
    component_id: 'string-unknown', instrument_id: 'instrument-unknown', position: 1, course_id: null,
    role: 'primary_sounding_string', material_family: 'steel', material_detail: 'unspecified', core_type: 'solid',
    winding_type: 'none', winding_material: null, coating: 'none', manufacturing_method: 'unknown',
    speaking_length_mm: 650, total_length_mm: 700, diameter_mm: 0.3, linear_density_kg_m: 0.00055,
    cross_section_shape: 'round', nominal_tension_n: 70, current_tension_n: 70, breaking_load_n: 320,
    elastic_modulus_pa: 2.0e11, plastic_deformation_ratio: 0, creep_ratio: 0, target_frequency_hz: 196,
    current_frequency_hz: 196, pitch_drift_cents: 0, tuning_stability: 1, temperament_reference: 'twelve_tone_equal',
    anchor_a_type: 'fixed', anchor_b_type: 'tuning_mechanism', break_angle_degrees: 8, bearing_points: [],
    termination_condition: 'stable', temperature_c: 21, relative_humidity: 45, contamination: 0,
    corrosion_level: 0, moisture_exposure: 0, age_hours: 0, cycles_estimate: 0, attack_rate_hz: 0,
    average_excitation_force_n: 0, peak_excitation_force_n: 0, bend_distance_mm: 0, bow_pressure_n: 0,
    pick_contact: null, strike_contact: null, wear_ratio: 0, fatigue_ratio: 0, notch_severity: 0,
    fray_ratio: 0, flattening_ratio: 0, prior_repairs: [], damage_sites: [], inharmonicity: 0,
    damping_ratio: 0.01, attack_profile: 'instrument_adapter_required', decay_profile: 'instrument_adapter_required',
    noise_components: [], sympathetic_coupling: [], repairability: 'replaceable', repair_method_candidates: ['replace'],
    replacement_required: false, temporary_fix_allowed: false, retension_profile: 'gradual', reentry_stability: 0.8
  });

  function createStringComponent(input = {}) {
    return {...DEFAULTS, ...input, standard_version: STANDARD_VERSION};
  }

  function stressRatio(state) {
    return clamp(state.current_tension_n / Math.max(1, state.breaking_load_n), 0, 2);
  }

  function environmentalLoad(state) {
    const heat = clamp(Math.abs(state.temperature_c - 21) / 55);
    const humidity = clamp(Math.abs(state.relative_humidity - 45) / 70);
    return clamp((heat * 0.35) + (humidity * 0.2) + (clamp(state.corrosion_level) * 0.3) + (clamp(state.moisture_exposure) * 0.15));
  }

  function excitationLoad(state) {
    const force = clamp(state.peak_excitation_force_n / Math.max(1, state.current_tension_n * 0.25));
    const rate = clamp(state.attack_rate_hz / 18);
    const bend = clamp(state.bend_distance_mm / 12);
    const bow = clamp(state.bow_pressure_n / 8);
    return clamp((force * 0.4) + (rate * 0.2) + (bend * 0.2) + (bow * 0.2));
  }

  function conditionLoad(state) {
    return clamp(
      clamp(state.wear_ratio) * 0.2 + clamp(state.fatigue_ratio) * 0.3 + clamp(state.notch_severity) * 0.25 +
      clamp(state.fray_ratio) * 0.15 + clamp(state.flattening_ratio) * 0.1
    );
  }

  function calculateFailureHazard(state) {
    const hazard = clamp(
      Math.pow(stressRatio(state), 3) * 0.42 +
      excitationLoad(state) * 0.24 +
      conditionLoad(state) * 0.26 +
      environmentalLoad(state) * 0.08
    );
    return Number(hazard.toFixed(6));
  }

  function advanceStringState(state, observation = {}) {
    const next = {...state, ...observation};
    const cycles = Number(observation.cycles_added || 0);
    const elapsedHours = Number(observation.hours_added || 0);
    next.cycles_estimate = Number(state.cycles_estimate || 0) + cycles;
    next.age_hours = Number(state.age_hours || 0) + elapsedHours;
    next.fatigue_ratio = clamp(Number(state.fatigue_ratio || 0) + cycles / 2500000 + excitationLoad(next) * 0.00008);
    next.wear_ratio = clamp(Number(state.wear_ratio || 0) + cycles / 5000000 + clamp(next.contamination) * 0.00001);
    next.tuning_stability = clamp(1 - next.fatigue_ratio * 0.35 - environmentalLoad(next) * 0.2);
    next.hazard_score = calculateFailureHazard(next);
    return next;
  }

  function sampleFailure(state, randomValue = Math.random()) {
    const hazard = calculateFailureHazard(state);
    const occurred = Number(randomValue) < hazard;
    if (!occurred) return {occurred: false, hazard_score: hazard, standard_version: STANDARD_VERSION};
    const location = state.damage_sites?.length ? state.damage_sites[0] : 'stochastic_high_stress_site';
    return {
      occurred: true,
      hazard_score: hazard,
      failure_mode: state.fray_ratio > state.notch_severity ? 'progressive_fray_separation' : 'high_stress_rupture',
      failure_location: location,
      transient_components: ['pitch_instability', 'rupture_impulse', 'loose_segment_motion', 'sympathetic_response'],
      exact_bar_locked: false,
      standard_version: STANDARD_VERSION,
      authority: 'none'
    };
  }

  function registerInstrumentAdapter(name, adapter) {
    if (!name || typeof adapter !== 'object') throw new TypeError('instrument adapter requires a name and object');
    adapters.set(String(name), Object.freeze({...adapter}));
  }

  const adapters = new Map();
  window.StegMusicStringPhysics = Object.freeze({
    STANDARD_VERSION, DEFAULTS, createStringComponent, stressRatio, environmentalLoad, excitationLoad,
    conditionLoad, calculateFailureHazard, advanceStringState, sampleFailure, registerInstrumentAdapter,
    getInstrumentAdapter: name => adapters.get(String(name)) || null,
    canonical_scope: 'all_tensioned_musical_strings_and_string_like_linear_elements',
    authority: 'none'
  });
})();
