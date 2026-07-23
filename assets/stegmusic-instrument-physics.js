(() => {
  'use strict';

  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, Number(value) || 0));

  const CLASS_DEFAULTS = Object.freeze({
    tensioned_linear: { fatigue: 0, wear: 0, defect: 0, load: 0, environment: 0 },
    air_path: { leakage: 0, condensation: 0, obstruction: 0, load: 0, environment: 0 },
    reed: { fatigue: 0, moisture: 0, edgeDamage: 0, load: 0, environment: 0 },
    lip_reed_interface: { fatigue: 0, instability: 0, load: 0, environment: 0 },
    membrane: { fatigue: 0, denting: 0, tear: 0, tensionVariance: 0, load: 0, environment: 0 },
    idiophone: { fatigue: 0, crack: 0, deformation: 0, load: 0, environment: 0 },
    resonator: { fatigue: 0, crack: 0, couplingLoss: 0, load: 0, environment: 0 },
    electroacoustic: { drift: 0, noise: 0, thermal: 0, intermittence: 0, load: 0, environment: 0 },
    excitation_tool: { wear: 0, damage: 0, misalignment: 0, load: 0, environment: 0 },
    maintenance_and_test_tool: { wear: 0, damage: 0, miscalibration: 0, uncertainty: 0, load: 0, environment: 0 }
  });

  function createComponent(input = {}) {
    const componentClass = input.componentClass || 'excitation_tool';
    if (!CLASS_DEFAULTS[componentClass]) throw new Error(`Unsupported component class: ${componentClass}`);
    return {
      schemaVersion: '1.0.0',
      componentId: input.componentId || `component-${Date.now()}-${Math.random().toString(16).slice(2)}`,
      componentClass,
      identity: { ...(input.identity || {}) },
      construction: { ...(input.construction || {}) },
      geometry: { ...(input.geometry || {}) },
      materialState: { ...(input.materialState || {}) },
      mechanicalState: { ...CLASS_DEFAULTS[componentClass], ...(input.mechanicalState || {}) },
      acousticState: { ...(input.acousticState || {}) },
      attachmentAndCoupling: { ...(input.attachmentAndCoupling || {}) },
      environment: { temperatureC: 20, humidity: 0.5, moisture: 0, ...(input.environment || {}) },
      usageAndExcitation: { cycles: 0, force: 0, velocity: 0, rate: 0, ...(input.usageAndExcitation || {}) },
      conditionAndDamage: { ...(input.conditionAndDamage || {}) },
      controlSurfaceState: { ...(input.controlSurfaceState || {}) },
      failure: { failed: false, failureType: null, hazard: 0, occurredAt: null, ...(input.failure || {}) },
      repair: { state: 'NONE', method: null, residualInstability: 0, ...(input.repair || {}) },
      recalibration: { required: false, completed: false, uncertainty: 0, ...(input.recalibration || {}) },
      reentry: { allowed: true, stability: 1, confidence: 1, ...(input.reentry || {}) },
      authority: 'none'
    };
  }

  function environmentalLoad(component) {
    const e = component.environment || {};
    const temperature = Math.abs((Number(e.temperatureC) || 20) - 20) / 60;
    const humidity = Math.abs((Number(e.humidity) || 0.5) - 0.5) * 1.5;
    const moisture = Number(e.moisture) || 0;
    return clamp(temperature + humidity + moisture);
  }

  function excitationLoad(component) {
    const x = component.usageAndExcitation || {};
    return clamp((Number(x.force) || 0) * 0.4 + (Number(x.velocity) || 0) * 0.25 + (Number(x.rate) || 0) * 0.2 + Math.log10(1 + (Number(x.cycles) || 0)) / 20);
  }

  function classDamage(component) {
    const s = component.mechanicalState || {};
    const values = Object.entries(s)
      .filter(([key]) => !['load', 'environment'].includes(key))
      .map(([, value]) => clamp(value));
    const conditionValues = Object.values(component.conditionAndDamage || {}).map(clamp);
    const all = values.concat(conditionValues);
    return all.length ? clamp(all.reduce((sum, value) => sum + value, 0) / all.length) : 0;
  }

  function failureHazard(component) {
    if (component.failure && component.failure.failed) return 1;
    const baseline = clamp(component.materialState && component.materialState.baselineLimitUsage);
    const fatigue = classDamage(component);
    const excitation = excitationLoad(component);
    const environment = environmentalLoad(component);
    const coupling = clamp(component.attachmentAndCoupling && component.attachmentAndCoupling.instability);
    return clamp(baseline * 0.1 + fatigue * 0.35 + excitation * 0.3 + environment * 0.15 + coupling * 0.1);
  }

  function advance(component, gesture = {}) {
    component.usageAndExcitation = { ...component.usageAndExcitation, ...gesture };
    component.usageAndExcitation.cycles = (Number(component.usageAndExcitation.cycles) || 0) + 1;
    const load = excitationLoad(component);
    const env = environmentalLoad(component);
    component.mechanicalState.load = load;
    component.mechanicalState.environment = env;
    ['fatigue', 'wear', 'drift', 'thermal', 'instability'].forEach((key) => {
      if (Object.prototype.hasOwnProperty.call(component.mechanicalState, key)) {
        component.mechanicalState[key] = clamp((Number(component.mechanicalState[key]) || 0) + load * 0.002 + env * 0.0005);
      }
    });
    component.failure.hazard = failureHazard(component);
    return component;
  }

  function sampleFailure(component, random = Math.random) {
    const hazard = failureHazard(component);
    component.failure.hazard = hazard;
    if (!component.failure.failed && random() < hazard * 0.02) {
      component.failure.failed = true;
      component.failure.failureType = `${component.componentClass}_failure`;
      component.failure.occurredAt = new Date().toISOString();
      component.reentry.allowed = false;
      component.reentry.stability = 0;
      component.reentry.confidence = 0;
    }
    return component.failure;
  }

  function repair(component, method = 'replacement', residualInstability = 0.15) {
    component.repair = { state: 'COMPLETED', method, residualInstability: clamp(residualInstability) };
    component.failure = { failed: false, failureType: null, hazard: clamp(residualInstability * 0.4), occurredAt: null };
    component.recalibration = { required: true, completed: false, uncertainty: clamp(residualInstability) };
    component.reentry = { allowed: true, stability: clamp(1 - residualInstability), confidence: clamp(1 - residualInstability * 1.5) };
    return component;
  }

  function recalibrate(component, uncertainty = 0.05) {
    component.recalibration = { required: false, completed: true, uncertainty: clamp(uncertainty) };
    component.reentry.stability = clamp(component.reentry.stability + 0.2);
    component.reentry.confidence = clamp(component.reentry.confidence + 0.2);
    return component;
  }

  window.StegMusicInstrumentPhysics = Object.freeze({
    componentClasses: Object.keys(CLASS_DEFAULTS),
    createComponent,
    environmentalLoad,
    excitationLoad,
    failureHazard,
    advance,
    sampleFailure,
    repair,
    recalibrate
  });
})();
