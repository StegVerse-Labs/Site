(() => {
  'use strict';

  const PROFILE_ID = 'evaluator-read-review';
  const OPERATION = 'READ_REVIEW';
  const REQUEST_SCHEMA = 'stegverse.evaluator_review.interlock_request.v1';
  const RESPONSE_CLASS = 'MIR_HISTORICAL_ACCOUNTING';
  const PROFILE_NAME = 'SDK:EvaluatorReviewIngress';
  const MATERIALIZATION_PATH = '/intr/materialization';
  const PROFILE_PATH = '/intr/profile';

  function fail(code) {
    const error = new Error(code);
    error.code = code;
    throw error;
  }

  function canonical(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
  }

  function bytesToHex(bytes) {
    return Array.from(new Uint8Array(bytes), (b) => b.toString(16).padStart(2, '0')).join('');
  }

  async function sha256Bytes(bytes) {
    return `sha256:${bytesToHex(await crypto.subtle.digest('SHA-256', bytes))}`;
  }

  async function sha256Value(value) {
    return sha256Bytes(new TextEncoder().encode(canonical(value)));
  }

  function isSha256Uri(value) {
    return /^sha256:[a-f0-9]{64}$/.test(String(value || ''));
  }

  function normalizeManifestHash(value) {
    const text = String(value || '').trim().toLowerCase();
    const hex = text.startsWith('sha256:') ? text.slice(7) : text;
    if (!/^[a-f0-9]{64}$/.test(hex)) fail('MIR_RETURN_MANIFEST_HASH_INVALID');
    return hex;
  }

  function normalizeArtifactBytes(value) {
    if (value instanceof Uint8Array) return value;
    if (value instanceof ArrayBuffer) return new Uint8Array(value);
    if (typeof value === 'string') return new TextEncoder().encode(value);
    fail('MIR_RETURN_ARTIFACT_BYTES_REQUIRED');
  }

  function bytesToBase64(bytes) {
    let out = '';
    const chunk = 0x8000;
    for (let i = 0; i < bytes.length; i += chunk) {
      out += String.fromCharCode.apply(null, bytes.subarray(i, Math.min(i + chunk, bytes.length)));
    }
    return btoa(out);
  }

  function validateBinding(input) {
    if (!input || typeof input !== 'object') fail('MIR_RETURN_BINDING_REQUIRED');
    const testId = String(input.test_id || '').trim();
    const responseTo = String(input.response_to || '').trim();
    const responseClass = String(input.response_class || '').trim();
    const revision = Number(input.revision);
    if (!testId) fail('MIR_RETURN_TEST_ID_REQUIRED');
    if (!responseTo) fail('MIR_RETURN_RESPONSE_TO_REQUIRED');
    if (responseClass !== RESPONSE_CLASS) fail('MIR_RETURN_RESPONSE_CLASS_INVALID');
    if (!Number.isInteger(revision) || revision < 1) fail('MIR_RETURN_REVISION_INVALID');
    return {
      test_id: testId,
      revision,
      manifest_hash: normalizeManifestHash(input.manifest_hash),
      response_to: responseTo,
      response_class: responseClass,
      counterparty_ref: String(input.counterparty_ref || 'MIR').trim() || 'MIR'
    };
  }

  async function buildEvaluatorRequest(input) {
    const binding = validateBinding(input);
    const artifactBytes = normalizeArtifactBytes(input.artifact_bytes);
    const artifactSha256 = await sha256Bytes(artifactBytes);
    if (input.artifact_sha256 != null && String(input.artifact_sha256).toLowerCase() !== artifactSha256) {
      fail('MIR_RETURN_ARTIFACT_HASH_MISMATCH');
    }
    const payload = {
      testId: binding.test_id,
      revision: binding.revision,
      manifestHash: binding.manifest_hash,
      sourceSystem: 'MIR',
      responseTo: binding.response_to,
      responseClass: binding.response_class,
      counterpartyRef: binding.counterparty_ref,
      artifactSha256,
      artifactMediaType: String(input.artifact_media_type || 'application/json'),
      artifactEncoding: 'base64',
      artifactBase64: bytesToBase64(artifactBytes),
      sourceNativeSemanticsPreserved: true,
      authorityTransfer: false
    };
    return {
      request: {
        schema_version: REQUEST_SCHEMA,
        request_class: 'EVALUATOR_REVIEW',
        transport: 'InTr',
        operation: OPERATION,
        authority_ref: `mir://historical-accounting/${encodeURIComponent(binding.response_to)}`,
        authority_transfer: false,
        bindings: {
          test_id: binding.test_id,
          revision: binding.revision,
          manifest_hash: binding.manifest_hash
        },
        payload
      },
      artifact_bytes: artifactBytes,
      artifact_sha256: artifactSha256,
      binding
    };
  }

  async function probeProfile() {
    if (!('serviceWorker' in navigator) || !window.isSecureContext) fail('MIR_RETURN_INTR_RUNTIME_UNAVAILABLE');
    await navigator.serviceWorker.register('/intr-service-worker.js', { scope: '/' });
    await navigator.serviceWorker.ready;
    const response = await fetch(PROFILE_PATH, {
      method: 'GET', cache: 'no-store', credentials: 'omit', headers: { Accept: 'application/json' }
    });
    if (!response.ok) fail(`MIR_RETURN_PROFILE_HTTP_${response.status}`);
    const profile = await response.json();
    if (profile.schema !== 'stegverse.universal-intr-profiled-ingress/v1' || profile.protocol !== 'InTr') {
      fail('MIR_RETURN_PROFILE_SCHEMA_INVALID');
    }
    if (!Array.isArray(profile.profiles) || !profile.profiles.includes(PROFILE_NAME)) {
      fail('BLOCKED_PROFILE_UNAVAILABLE');
    }
    if (profile.materialization_path !== MATERIALIZATION_PATH || profile.credential_authority !== 'TV/TVC' || profile.execution_authority !== 'NONE') {
      fail('MIR_RETURN_PROFILE_BOUNDARY_INVALID');
    }
    return profile;
  }

  async function buildTransport(prepared) {
    const intr = window.StegVerseGeneratedInTr;
    const carrier = window.StegVerseHBInTrCarrier;
    if (!intr || typeof intr.buildIntent !== 'function' || typeof intr.buildMaterializationRequest !== 'function') {
      fail('MIR_RETURN_CANONICAL_INTR_CONNECTOR_UNAVAILABLE');
    }
    if (!intr.PROFILES || !intr.PROFILES[PROFILE_ID]) fail('MIR_RETURN_EVALUATOR_PROFILE_UNAVAILABLE');
    if (!carrier || typeof carrier.buildBinding !== 'function') fail('MIR_RETURN_HB_CARRIER_UNAVAILABLE');
    const requestBytes = new TextEncoder().encode(intr.canonical(prepared.request));
    const operationId = `MIR-RETURN:${prepared.binding.test_id}:v${prepared.binding.revision}:${prepared.artifact_sha256.slice(7, 31)}`;
    const intent = await intr.buildIntent(PROFILE_ID, requestBytes, OPERATION, operationId);
    const carrierBinding = await carrier.buildBinding(intent.packet_id, intent.payload_hash);
    const payloadRef = `data:application/vnd.stegverse.evaluator-review+json;base64,${bytesToBase64(requestBytes)}`;
    const materializationRequest = await intr.buildMaterializationRequest(
      PROFILE_ID, intent, payloadRef, carrierBinding
    );
    return { requestBytes, operationId, intent, carrierBinding, materializationRequest };
  }

  async function buildTrigger(outboxEntry) {
    const body = {
      schema: 'stegos.node_intr_materialization_trigger.v1',
      transport_origin: 'STEGOS_NODE_OUTBOX',
      node_id: outboxEntry.node_id,
      interlock_id: outboxEntry.interlock_id,
      outbox_entry_hash: outboxEntry.outbox_entry_hash,
      node_outbox_entry: outboxEntry,
      request_grants_execution_authority: false,
      claim_or_fence_minted: false,
      authority_effect: 'NONE_TRIGGER_ONLY'
    };
    return Object.assign({}, body, { trigger_sha256: await sha256Value(body) });
  }

  async function validateIngressReceipt(receipt, outboxEntry, triggerSha256) {
    if (!receipt || receipt.state !== 'INGRESS_ADMITTED') fail('MIR_RETURN_INGRESS_RECEIPT_INVALID');
    const expected = {
      materialization_id: outboxEntry.materialization_id,
      request_hash: outboxEntry.request_hash,
      transport_intent_hash: outboxEntry.transport_intent_hash,
      payload_hash: outboxEntry.payload_hash,
      node_id: outboxEntry.node_id,
      interlock_id: outboxEntry.interlock_id,
      outbox_entry_hash: outboxEntry.outbox_entry_hash,
      transport_origin: 'STEGOS_NODE_OUTBOX',
      credential_authority: 'TV/TVC',
      github_token_runtime_authority: 'NONE'
    };
    for (const [key, value] of Object.entries(expected)) {
      if (canonical(receipt[key]) !== canonical(value)) fail(`MIR_RETURN_INGRESS_RECEIPT_BINDING_MISMATCH:${key}`);
    }
    if (receipt.transport_payload_sha256 && receipt.transport_payload_sha256 !== triggerSha256) {
      fail('MIR_RETURN_INGRESS_TRIGGER_HASH_MISMATCH');
    }
    if (receipt.authority_effect && !String(receipt.authority_effect).startsWith('NONE')) {
      fail('MIR_RETURN_INGRESS_AUTHORITY_INVALID');
    }
    return receipt;
  }

  async function submit(input) {
    const prepared = await buildEvaluatorRequest(input);
    await probeProfile();
    const transport = await buildTransport(prepared);
    const node = window.StegVerseNodeContinuity;
    if (!node || typeof node.queueIntrMaterializationRequest !== 'function') fail('MIR_RETURN_REGISTERED_NODE_QUEUE_UNAVAILABLE');
    const outboxEntry = await node.queueIntrMaterializationRequest(transport.materializationRequest);
    const trigger = await buildTrigger(outboxEntry);
    const triggerSha256 = await sha256Value(trigger);
    const response = await fetch(MATERIALIZATION_PATH, {
      method: 'POST',
      cache: 'no-store',
      credentials: 'omit',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(trigger)
    });
    if (response.status !== 202) fail(`MIR_RETURN_INGRESS_HTTP_${response.status}`);
    const receipt = await response.json();
    await validateIngressReceipt(receipt, outboxEntry, triggerSha256);
    return {
      schema: 'stegverse.mir.accounting-return-intr-result/v1',
      state: 'SDK_EVALUATOR_INGRESS_ADMITTED',
      test_id: prepared.binding.test_id,
      revision: prepared.binding.revision,
      manifest_hash: prepared.binding.manifest_hash,
      response_to: prepared.binding.response_to,
      response_class: prepared.binding.response_class,
      artifact_sha256: prepared.artifact_sha256,
      materialization_id: outboxEntry.materialization_id,
      outbox_entry_hash: outboxEntry.outbox_entry_hash,
      ingress_receipt: receipt,
      sdk_delta_evaluation_observed: false,
      mir_historical_accounting_claimed_by_transport: false,
      governance_authority_effect: 'NONE',
      transport_authority_effect: 'NONE'
    };
  }

  window.StegVerseMirAccountingReturn = Object.freeze({
    PROFILE_ID,
    PROFILE_NAME,
    RESPONSE_CLASS,
    buildEvaluatorRequest,
    probeProfile,
    buildTransport,
    submit
  });
})();
