(() => {
  'use strict';

  const PROJECTION_URL = 'data/ecosystem-continuity/current.json';
  const PROJECTION_SCHEMA = 'stegverse.site-ecosystem-continuity-projection.v1';
  const PROJECTION_AUTHORITY = 'NONE_READ_ONLY_PROJECTION';
  const CONTINUITY_STATES = new Set([
    'CONTINUOUS', 'CONTINUOUS_WITH_DEGRADATION', 'AT_RISK', 'INTERRUPTED', 'INDETERMINATE'
  ]);
  const OBSERVATION_STATES = new Set([
    'PASS', 'FAIL', 'DEGRADED', 'UNKNOWN', 'NOT_OBSERVED', 'STALE', 'UNREACHABLE', 'PROBE_REQUIRED'
  ]);
  const SAFE_FINDING_KEYS = new Set([
    'finding_id', 'component_id', 'predicate_id', 'observation_state', 'severity',
    'continuity_critical', 'evidence_age_seconds', 'authority_owner', 'remediation_state'
  ]);

  const byId = (id) => document.getElementById(id);

  function unavailable(reason) {
    const badge = byId('continuity-badge');
    badge.textContent = 'UNAVAILABLE';
    badge.dataset.state = 'UNAVAILABLE';
    byId('projection-state').textContent = 'No authentic retained projection is currently available.';
    byId('evaluation-id').textContent = 'Not observed';
    byId('evaluated-at').textContent = 'Not observed';
    byId('projected-at').textContent = 'Not supplied by projection v1';
    byId('completeness').textContent = 'Not observed';
    byId('authority-effect').textContent = 'NONE_READ_ONLY_PROJECTION';
    byId('findings').hidden = true;
    byId('findings').replaceChildren();
    byId('continuity-notice').textContent = `Fail-closed: ${reason}. Absence of a retained projection is not evidence of continuity or interruption.`;
  }

  function validFinding(row) {
    if (!row || typeof row !== 'object' || Array.isArray(row)) return false;
    if (!OBSERVATION_STATES.has(row.observation_state)) return false;
    return Object.keys(row).every((key) => SAFE_FINDING_KEYS.has(key));
  }

  function validate(value) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) return 'PROJECTION_NOT_OBJECT';
    if (value.schema !== PROJECTION_SCHEMA) return 'INVALID_PROJECTION_SCHEMA';
    if (value.authority_effect !== PROJECTION_AUTHORITY) return 'INVALID_PROJECTION_AUTHORITY';
    if (value.source_available !== true) return 'SOURCE_NOT_AVAILABLE';
    if (!CONTINUITY_STATES.has(value.continuity_state)) return 'INVALID_CONTINUITY_STATE';
    if (typeof value.source_evaluation_id !== 'string' || !value.source_evaluation_id.startsWith('ece_')) return 'INVALID_EVALUATION_ID';
    if (typeof value.evaluated_at !== 'string' || Number.isNaN(Date.parse(value.evaluated_at))) return 'INVALID_EVALUATED_AT';
    if (!value.completeness || typeof value.completeness !== 'object') return 'INVALID_COMPLETENESS';
    const { registered_predicates, observed_predicates, evaluation_errors } = value.completeness;
    if (![registered_predicates, observed_predicates, evaluation_errors].every(Number.isInteger)) return 'INVALID_COMPLETENESS_COUNTS';
    if (registered_predicates < 0 || observed_predicates < 0 || observed_predicates > registered_predicates || evaluation_errors < 0) return 'INVALID_COMPLETENESS_RANGE';
    if (!Array.isArray(value.findings) || !value.findings.every(validFinding)) return 'UNSAFE_OR_INVALID_FINDINGS';
    if (value.projection_error !== null) return 'PROJECTION_ERROR_PRESENT';
    return null;
  }

  function renderFinding(row) {
    const card = document.createElement('article');
    card.className = 'finding';
    const heading = document.createElement('h2');
    heading.textContent = `${row.component_id || 'Unknown component'} · ${row.predicate_id || 'Unknown predicate'}`;
    const state = document.createElement('p');
    state.textContent = `Observation: ${row.observation_state} · Severity: ${row.severity || 'UNKNOWN'}`;
    const remediation = document.createElement('p');
    remediation.textContent = `Remediation: ${row.remediation_state || 'UNASSIGNED'} · Authority owner: ${row.authority_owner || 'Unspecified'}`;
    const age = document.createElement('p');
    age.textContent = Number.isFinite(row.evidence_age_seconds) ? `Evidence age: ${row.evidence_age_seconds}s` : 'Evidence age: not supplied';
    card.append(heading, state, remediation, age);
    return card;
  }

  function render(value) {
    const badge = byId('continuity-badge');
    badge.textContent = value.continuity_state;
    badge.dataset.state = value.continuity_state;
    byId('projection-state').textContent = 'Authentic Site-safe retained projection loaded.';
    byId('evaluation-id').textContent = value.source_evaluation_id;
    byId('evaluated-at').textContent = value.evaluated_at;
    byId('projected-at').textContent = 'Not supplied by projection v1';
    byId('completeness').textContent = `${value.completeness.observed_predicates} / ${value.completeness.registered_predicates} observed; ${value.completeness.evaluation_errors} evaluation error(s)`;
    byId('authority-effect').textContent = value.authority_effect;
    byId('continuity-notice').textContent = 'This is a read-only projection of retained ECE output. It grants no execution, repair, custody, transition, credential, or recovery authority.';
    const findings = byId('findings');
    findings.replaceChildren(...value.findings.filter((row) => row.observation_state !== 'PASS').map(renderFinding));
    findings.hidden = findings.childElementCount === 0;
  }

  async function load() {
    unavailable('PROJECTION_NOT_LOADED');
    try {
      const response = await fetch(PROJECTION_URL, { cache: 'no-store', credentials: 'same-origin' });
      if (!response.ok) return unavailable(`PROJECTION_HTTP_${response.status}`);
      const value = await response.json();
      const error = validate(value);
      if (error) return unavailable(error);
      render(value);
    } catch (error) {
      unavailable(error instanceof SyntaxError ? 'PROJECTION_INVALID_JSON' : 'PROJECTION_FETCH_FAILED');
    }
  }

  document.addEventListener('DOMContentLoaded', load, { once: true });
})();
