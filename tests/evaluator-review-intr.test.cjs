const assert = require('node:assert/strict');
const api = require('../assets/evaluator-review.js');

(function(){
  const request = api.buildInterlockRequest('approve', {
    testId: 'cross-framework-current-basis-001',
    revision: 4,
    manifestHash: 'a'.repeat(64),
    attestation: 'TEST_SPECIFICATION_ONLY'
  });

  assert.equal(request.schema_version, api.INTERLOCK_REQUEST_SCHEMA);
  assert.equal(request.request_class, 'EVALUATOR_REVIEW');
  assert.equal(request.operation, 'APPROVE');
  assert.equal(request.transport, 'InTr');
  assert.equal(request.authority_transfer, false);
  assert.deepEqual(request.bindings, {
    test_id: 'cross-framework-current-basis-001',
    revision: 4,
    manifest_hash: 'a'.repeat(64)
  });

  const receipt = {
    schema_version: api.INTR_RECEIPT_SCHEMA,
    boundary_verification: 'VERIFIED',
    transition_state: 'RECEIVED',
    authority_transfer: false,
    secret_plaintext_present: false,
    payload_hash: 'b'.repeat(64),
    receipt_hash: 'c'.repeat(64),
    from_role: 'SITE',
    to_role: 'INTERLOCK'
  };
  assert.equal(api.validateIntrReceipt(receipt, request).ok, true);

  const response = {
    schema_version: api.INTERLOCK_RESPONSE_SCHEMA,
    operation: 'APPROVE',
    decision: 'ALLOW_BOUNDED_CONTEXT',
    authority_effect: 'NONE',
    authority_transfer: false,
    bindings: {
      test_id: 'cross-framework-current-basis-001',
      revision: 4,
      manifest_hash: 'a'.repeat(64)
    },
    intr_receipt: receipt,
    review: { review_schema:'stegverse.evaluator-review.v1' }
  };
  assert.equal(api.validateInterlockResponse(request, response).ok, true);

  const wrongHash = structuredClone(response);
  wrongHash.bindings.manifest_hash = 'd'.repeat(64);
  assert.equal(api.validateInterlockResponse(request, wrongHash).ok, false);

  const authorityTransfer = structuredClone(response);
  authorityTransfer.intr_receipt.authority_transfer = true;
  assert.equal(api.validateInterlockResponse(request, authorityTransfer).ok, false);

  const unverified = structuredClone(response);
  unverified.intr_receipt.boundary_verification = 'UNVERIFIED';
  assert.equal(api.validateInterlockResponse(request, unverified).ok, false);

  assert.throws(
    () => api.buildInterlockRequest('unsupported-operation', {}),
    /Unsupported evaluator review Interlock operation/
  );

  console.log('EVALUATOR_REVIEW_INTR_BINDING_PASS');
})();
