(() => {
  'use strict';

  const RESULT_SCHEMA = 'stegverse.external-counterpart-return-consumption/v1';

  function fail(code) {
    const error = new Error(code);
    error.code = code;
    throw error;
  }

  async function consume(input) {
    const adapter = window.StegVerseMirAccountingReturn;
    if (!adapter || typeof adapter.submit !== 'function') {
      fail('EXTERNAL_RETURN_INTR_ADAPTER_UNAVAILABLE');
    }

    const admitted = await adapter.submit(input);
    if (!admitted || admitted.state !== 'SDK_EVALUATOR_INGRESS_ADMITTED') {
      fail('EXTERNAL_RETURN_NOT_ADMITTED');
    }
    const receipt = admitted.stegverse_return_exit_receipt;
    if (!receipt || receipt.transition_class !== 'STEGVERSE_RETURN_EXIT') {
      fail('EXTERNAL_RETURN_EXIT_TRANSITION_MISSING');
    }
    if (admitted.roundtrip_boundary_receipts_complete !== true) {
      fail('EXTERNAL_RETURN_BOUNDARY_RECEIPTS_INCOMPLETE');
    }

    let nodeReceipt = null;
    const node = window.StegVerseNodeContinuity;
    if (node && typeof node.appendCapabilityReceipt === 'function') {
      nodeReceipt = await node.appendCapabilityReceipt({
        transition: 'EXTERNAL_COUNTERPART_RETURN_ADMITTED',
        capability: 'external-counterpart-return',
        step: 'stegverse-return-exit',
        resulting_state: 'SDK_EVALUATOR_INGRESS_ADMITTED',
        evidence_ref: receipt.receipt_sha256 || null
      });
    }

    return {
      schema: RESULT_SCHEMA,
      state: 'EXTERNAL_COUNTERPART_RETURN_CONSUMED',
      response_to: admitted.response_to,
      manifest_hash: admitted.manifest_hash,
      materialization_id: admitted.materialization_id,
      stegverse_return_exit_receipt: receipt,
      sdk_evaluator_ingress_state: admitted.state,
      node_transition_receipt: nodeReceipt,
      authority_effect: 'NONE'
    };
  }

  window.StegVerseExternalCounterpartReturnConsumer = Object.freeze({
    RESULT_SCHEMA,
    consume
  });
})();
