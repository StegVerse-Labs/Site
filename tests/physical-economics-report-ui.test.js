'use strict';

const assert = require('assert');
const report = require('../js/physical-economics-report.js');

function fixture(overrides = {}) {
  const rendererVersion = 'physical-economics-report-renderer.v0.1';
  const base = {
    state: 'GENERATED_NOT_PUBLICLY_ACTIVATED',
    report_document: {
      report_id: 'PE-REPORT-TEST-001',
      generated_as_of_time: '2026-08-26T15:07:00Z',
      question: 'What changed?',
      claim_classes: ['PRICE_CHANGE'],
      scope: { subject: 'Food', economic_domain: 'Food at home', geography: 'United States', population_scope: 'Households' },
      boundary: {
        completeness_state: 'COMPLETE_WITHIN_BOUNDARY',
        statement: 'Common required-attribute comparable/complete window: 2026-01-01 through 2026-07-31.',
        earliest_common_comparable_date: '2026-01-01',
        latest_common_complete_date: '2026-07-31'
      },
      coverage_matrix: [
        {
          attribute_id: 'nominal_price',
          required: true,
          earliest_admissible_date: '2026-01-01',
          latest_observed_date: '2026-07-31',
          latest_complete_date: '2026-07-31',
          current_period_state: 'COMPLETE',
          methodology_regime_id: 'TEST-V1',
          comparability: 'COMPARABLE',
          provenance_posture: 'DIRECT_AUTHORITATIVE',
          missingness_posture: 'OBSERVED'
        }
      ],
      uncertainty_surface: [
        { attribute_id: 'nominal_price', uncertainty_posture: null, aggregate_propagation_state: null }
      ],
      findings: [
        {
          finding_id: 'F-1',
          finding_class: 'OBSERVED',
          statement: 'Observed price evidence is available within the bounded window.',
          claim_class: 'PRICE_CHANGE',
          evidence_posture: 'DIRECT',
          source_receipt_ids: ['SRC-1'],
          uncertainty_note: null,
          boundary_note: 'Do not extend beyond the common complete window.'
        }
      ],
      opaque_elements: [],
      prospective_evidence_gates: [],
      receipts: {
        report_request_hash: 'sha256:req',
        evidence_snapshot_hash: 'sha256:snapshot',
        boundary_manifest_hash: 'sha256:boundary',
        pertinence_matrix_version: '0.1',
        contract_version: 'physical-economics-report-generation.v0.1',
        source_receipt_ids: ['SRC-1']
      },
      renderer_version: rendererVersion,
      prior_report_delta: null
    },
    verification_receipt: {
      verification_receipt_id: 'PE-VR-TEST-001',
      report_id: 'PE-REPORT-TEST-001',
      report_request_hash: 'sha256:req',
      evidence_snapshot_id: 'PE-SNAPSHOT-TEST-001',
      evidence_snapshot_hash: 'sha256:snapshot',
      boundary_manifest_id: 'PE-BM-TEST-001',
      boundary_manifest_hash: 'sha256:boundary',
      pertinence_matrix_version: '0.1',
      contract_version: 'physical-economics-report-generation.v0.1',
      renderer_version: rendererVersion,
      report_content_hash: 'sha256:report',
      source_receipt_ids: ['SRC-1'],
      verification_state: 'VERIFIABLE',
      verification_notes: []
    }
  };
  return Object.assign(base, overrides);
}

function requestInput() {
  return {
    question: 'How has household food purchasing power changed?',
    subject: 'Household food purchasing power',
    economic_domain: 'Food at home',
    geography: 'United States',
    population_scope: 'Households',
    essential_or_discretionary_class: 'ESSENTIAL',
    claim_classes: ['PHYSICAL_PURCHASING_POWER', 'ESSENTIAL_AFFORDABILITY'],
    vintage_policy: 'CURRENT_VINTAGE',
    allow_optional_context_attributes: true,
    include_state_vector: true,
    include_data_coverage_matrix: true,
    include_prospective_evidence_gates: true,
    include_source_receipts: true,
    include_uncertainty_surface: true
  };
}

async function main() {
  assert.strictEqual(report.PERTINENCE_MATRIX_VERSION, '0.1');
  assert(report.CLAIM_CLASSES.includes('PHYSICAL_PURCHASING_POWER'));

  const request = report.buildRequest(requestInput(), {
    now: '2026-08-26T15:07:00Z',
    randomSource: () => 0.5
  });
  assert.strictEqual(request.pertinence_policy.mode, 'DETERMINISTIC_CLAIM_CLASS_MAPPING');
  assert.strictEqual(request.pertinence_policy.required_attribute_sets_version, '0.1');
  assert.deepStrictEqual(request.pertinence_policy.excluded_attributes, []);
  assert.strictEqual(request.scope.essential_or_discretionary_class, 'ESSENTIAL');
  assert.strictEqual(request.requested_as_of_time, '2026-08-26T15:07:00.000Z');

  assert.throws(
    () => report.buildRequest({ ...requestInput(), claim_classes: [] }),
    (error) => error.code === 'INVALID_REQUEST'
  );
  assert.throws(
    () => report.buildRequest({ ...requestInput(), requested_start_date: '2026-08-01', requested_end_date: '2026-07-01' }),
    (error) => error.code === 'INVALID_REQUEST'
  );

  const valid = fixture();
  const validated = report.validateBackendResponse(valid);
  assert.strictEqual(validated.verification_receipt.verification_state, 'VERIFIABLE');

  const html = report.renderReportToHtml(valid);
  const boundaryIndex = html.indexOf('id="report-boundary"');
  const findingsIndex = html.indexOf('id="report-findings"');
  assert(boundaryIndex >= 0, 'boundary section missing');
  assert(findingsIndex > boundaryIndex, 'findings rendered before boundary');
  assert(html.includes('Portable verification'));
  assert(html.includes('VERIFIABLE'));
  assert(html.includes('OBSERVED'));

  const noFindings = fixture();
  noFindings.report_document.findings = [];
  const emptyHtml = report.renderReportToHtml(noFindings);
  assert(emptyHtml.includes('The UI will not invent any.'));

  const unverified = fixture();
  unverified.verification_receipt.verification_state = 'FAIL_CLOSED_HASH_MISMATCH';
  assert.throws(
    () => report.validateBackendResponse(unverified),
    (error) => error.code === 'UNVERIFIED_REPORT'
  );

  const badState = fixture();
  badState.state = 'PUBLICLY_ACTIVATED';
  assert.throws(
    () => report.validateBackendResponse(badState),
    (error) => error.code === 'BACKEND_STATE_NOT_ADMISSIBLE'
  );

  await assert.rejects(
    () => report.submitReportRequest(request, { endpoint: '', fetchImpl: async () => ({ ok: true }) }),
    (error) => error.code === 'BACKEND_NOT_CONFIGURED'
  );

  let capturedRequest = null;
  const transportResult = await report.submitReportRequest(request, {
    endpoint: 'https://example.invalid/physical-economics/report',
    fetchImpl: async (url, options) => {
      capturedRequest = { url, options };
      return { ok: true, status: 200, json: async () => fixture() };
    }
  });
  assert.strictEqual(capturedRequest.options.credentials, 'omit');
  assert.strictEqual(capturedRequest.options.cache, 'no-store');
  assert.strictEqual(capturedRequest.options.redirect, 'error');
  assert.strictEqual(JSON.parse(capturedRequest.options.body).pertinence_policy.required_attribute_sets_version, '0.1');
  assert.strictEqual(transportResult.verification_receipt.verification_state, 'VERIFIABLE');

  const escaped = report.escapeHtml('<script>alert("x")</script>');
  assert(!escaped.includes('<script>'));
  assert(escaped.includes('&lt;script&gt;'));

  console.log('PHYSICAL_ECONOMICS_REPORT_UI_REQUEST_CONTRACT=PASS');
  console.log('PHYSICAL_ECONOMICS_REPORT_UI_FAIL_CLOSED_BACKEND=PASS');
  console.log('PHYSICAL_ECONOMICS_REPORT_UI_BOUNDARY_BEFORE_FINDINGS=PASS');
  console.log('PHYSICAL_ECONOMICS_REPORT_UI_PORTABLE_VERIFICATION=PASS');
  console.log('PHYSICAL_ECONOMICS_REPORT_UI_NO_INVENTED_FINDINGS=PASS');
  console.log('PHYSICAL_ECONOMICS_REPORT_UI_HTML_ESCAPING=PASS');
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
