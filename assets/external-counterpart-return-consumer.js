(() => {
  'use strict';

  const RESULT_SCHEMA = 'stegverse.external-counterpart-return-consumption/v1';
  const RETAINED_PACKET_SCHEMA = 'stegverse.canonical-runtime-exact-return-packet/v1';
  const RETAINED_PACKET_PROFILE = 'MIR';
  const SDK_PROCESSING_HANDOFF_SCHEMA = 'stegverse.site.sdk-processing-handoff/v1';

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

  async function sha256Utf8(text) {
    return sha256Bytes(new TextEncoder().encode(text));
  }

  async function sha256Value(value) {
    return sha256Bytes(new TextEncoder().encode(canonical(value)));
  }

  function normalizeHash(value, code) {
    const text = String(value || '').trim().toLowerCase();
    const hex = text.startsWith('sha256:') ? text.slice(7) : text;
    if (!/^[a-f0-9]{64}$/.test(hex)) fail(code);
    return `sha256:${hex}`;
  }

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function firstExternalIngress(continuation) {
    if (!continuation || !Array.isArray(continuation.continuation_receipts)) {
      fail('RETAINED_MIR_PACKET_EXTERNAL_RECEIPTS_REQUIRED');
    }
    const receipt = continuation.continuation_receipts.find(
      (item) => item && item.transition_class === 'EXTERNAL_FRAMEWORK_INGRESS'
    );
    if (!receipt) fail('RETAINED_MIR_PACKET_EXTERNAL_INGRESS_RECEIPT_REQUIRED');
    return receipt;
  }

  async function retainedPacketToConsumerInput(packet, overrides = {}) {
    if (!packet || typeof packet !== 'object') fail('RETAINED_MIR_PACKET_REQUIRED');
    if (packet.schema !== RETAINED_PACKET_SCHEMA) fail('RETAINED_MIR_PACKET_SCHEMA_INVALID');
    if (packet.profile_id !== RETAINED_PACKET_PROFILE) fail('RETAINED_MIR_PACKET_PROFILE_INVALID');

    const packetUtf8 = packet.packet_utf8;
    if (typeof packetUtf8 !== 'string' || packetUtf8.length === 0) {
      fail('RETAINED_MIR_PACKET_UTF8_REQUIRED');
    }

    const expectedPacketHash = normalizeHash(packet.packet_sha256, 'RETAINED_MIR_PACKET_HASH_INVALID');
    const actualPacketHash = await sha256Utf8(packetUtf8);
    if (actualPacketHash !== expectedPacketHash) fail('RETAINED_MIR_PACKET_HASH_MISMATCH');

    let decoded;
    try {
      decoded = JSON.parse(packetUtf8);
    } catch (error) {
      fail('RETAINED_MIR_PACKET_JSON_INVALID');
    }
    if (!decoded || typeof decoded !== 'object') fail('RETAINED_MIR_PACKET_BODY_INVALID');

    const mirrorReturn = decoded.mirror_return;
    if (!mirrorReturn || typeof mirrorReturn !== 'object' || Array.isArray(mirrorReturn)) {
      fail('RETAINED_MIR_PACKET_MIRROR_RETURN_REQUIRED');
    }

    const continuation = mirrorReturn.manifest_continuation;
    if (!continuation || typeof continuation !== 'object') {
      fail('RETAINED_MIR_PACKET_MANIFEST_CONTINUATION_REQUIRED');
    }
    if (!continuation.outbound_manifest || typeof continuation.outbound_manifest !== 'object') {
      fail('RETAINED_MIR_PACKET_OUTBOUND_MANIFEST_REQUIRED');
    }

    const manifest = clone(continuation.outbound_manifest);
    const manifestHash = normalizeHash(
      continuation.outbound_manifest_sha256,
      'RETAINED_MIR_PACKET_MANIFEST_HASH_INVALID'
    );
    const computedManifestHash = await sha256Value(manifest);
    if (computedManifestHash !== manifestHash) fail('RETAINED_MIR_PACKET_MANIFEST_HASH_MISMATCH');

    const ingress = firstExternalIngress(continuation);
    if (normalizeHash(ingress.manifest_sha256, 'RETAINED_MIR_PACKET_INGRESS_MANIFEST_HASH_INVALID') !== manifestHash) {
      fail('RETAINED_MIR_PACKET_INGRESS_MANIFEST_MISMATCH');
    }

    const packetCorrelation = String(packet.correlation_id || '').trim();
    const ingressCorrelation = String(ingress.correlation_id || ingress.response_to || '').trim();
    const bodyCorrelation = String(decoded.correlation_id || decoded.response_to || '').trim();
    const selectedCorrelation = String(overrides.response_to || packetCorrelation || ingressCorrelation || bodyCorrelation).trim();
    if (!selectedCorrelation) fail('RETAINED_MIR_PACKET_CORRELATION_REQUIRED');
    for (const candidate of [packetCorrelation, ingressCorrelation, bodyCorrelation].filter(Boolean)) {
      if (candidate !== selectedCorrelation) fail('RETAINED_MIR_PACKET_CORRELATION_MISMATCH');
    }

    if (continuation.required_next_receipt !== 'STEGVERSE_RETURN_EXIT') {
      fail('RETAINED_MIR_PACKET_RETURN_EXIT_REQUIREMENT_MISSING');
    }

    const artifactText = canonical(mirrorReturn);
    const artifactBytes = new TextEncoder().encode(artifactText);
    const artifactHash = await sha256Bytes(artifactBytes);

    return {
      test_id: String(overrides.test_id || decoded.goal_task_id || manifest.goal_task_id || '').trim(),
      revision: Number(overrides.revision || decoded.revision || 1),
      manifest,
      manifest_hash: manifestHash,
      manifest_continuation: clone(continuation),
      response_to: selectedCorrelation,
      response_class: String(overrides.response_class || 'MIR_HISTORICAL_ACCOUNTING'),
      response_mode: String(mirrorReturn.response_mode || overrides.response_mode || 'SOURCE_NATIVE_RESULT'),
      counterparty_ref: String(overrides.counterparty_ref || decoded.counterpart || ingress.counterpart || 'MIR_NODE_MIRROR'),
      counterpart_mode: String(overrides.counterpart_mode || 'STEGOS_EXTERNAL_COUNTERPART_MIRROR'),
      external_system_profile: RETAINED_PACKET_PROFILE,
      artifact_media_type: String(
        overrides.artifact_media_type || 'application/vnd.stegverse.external-counterpart-return+json'
      ),
      artifact_bytes: artifactBytes,
      artifact_sha256: artifactHash,
      retained_packet_sha256: expectedPacketHash,
      retained_packet_schema: RETAINED_PACKET_SCHEMA
    };
  }

  async function buildSdkProcessingHandoff(input, admitted, receipt, nodeReceipt) {
    if (!admitted.manifest || typeof admitted.manifest !== 'object') {
      fail('SDK_PROCESSING_HANDOFF_MANIFEST_REQUIRED');
    }
    if (!admitted.manifest_continuation || typeof admitted.manifest_continuation !== 'object') {
      fail('SDK_PROCESSING_HANDOFF_CONTINUATION_REQUIRED');
    }
    const manifestHash = normalizeHash(admitted.manifest_hash, 'SDK_PROCESSING_HANDOFF_MANIFEST_HASH_INVALID');
    if (manifestHash !== normalizeHash(input.manifest_hash, 'SDK_PROCESSING_HANDOFF_INPUT_MANIFEST_HASH_INVALID')) {
      fail('SDK_PROCESSING_HANDOFF_MANIFEST_HASH_MISMATCH');
    }
    const responseTo = String(admitted.response_to || '').trim();
    if (!responseTo || responseTo !== String(input.response_to || '').trim()) {
      fail('SDK_PROCESSING_HANDOFF_CORRELATION_MISMATCH');
    }
    const body = {
      schema: SDK_PROCESSING_HANDOFF_SCHEMA,
      state: 'READY_FOR_MANIFEST_SELECTED_SDK_PROCESSING',
      manifest: clone(admitted.manifest),
      manifest_hash: manifestHash,
      manifest_continuation: clone(admitted.manifest_continuation),
      response_to: responseTo,
      retained_packet_sha256: input.retained_packet_sha256 || null,
      retained_packet_schema: input.retained_packet_schema || null,
      stegverse_return_exit_receipt: clone(receipt),
      sdk_evaluator_ingress_state: admitted.state,
      node_transition_receipt: nodeReceipt ? clone(nodeReceipt) : null,
      next_required_transition: 'EXECUTE_MANIFEST_SELECTED_SDK_PROCESSING_AFTER_EVALUATOR_INGRESS',
      authority_effect: 'NONE'
    };
    return Object.assign({}, body, { handoff_sha256: await sha256Value(body) });
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
    const sdkProcessingHandoff = await buildSdkProcessingHandoff(input, admitted, receipt, nodeReceipt);

    return {
      schema: RESULT_SCHEMA,
      state: 'EXTERNAL_COUNTERPART_RETURN_CONSUMED',
      response_to: admitted.response_to,
      manifest_hash: admitted.manifest_hash,
      materialization_id: admitted.materialization_id,
      stegverse_return_exit_receipt: receipt,
      sdk_evaluator_ingress_state: admitted.state,
      node_transition_receipt: nodeReceipt,
      sdk_processing_handoff: sdkProcessingHandoff,
      retained_packet_sha256: input.retained_packet_sha256 || null,
      authority_effect: 'NONE'
    };
  }

  async function consumeRetainedPacket(packet, overrides = {}) {
    const input = await retainedPacketToConsumerInput(packet, overrides);
    const result = await consume(input);
    if (result.response_to !== input.response_to) fail('RETAINED_MIR_PACKET_CONSUMER_CORRELATION_MISMATCH');
    if (normalizeHash(result.manifest_hash, 'RETAINED_MIR_PACKET_CONSUMER_MANIFEST_HASH_INVALID') !== input.manifest_hash) {
      fail('RETAINED_MIR_PACKET_CONSUMER_MANIFEST_MISMATCH');
    }
    if (!result.sdk_processing_handoff || result.sdk_processing_handoff.state !== 'READY_FOR_MANIFEST_SELECTED_SDK_PROCESSING') {
      fail('RETAINED_MIR_PACKET_SDK_PROCESSING_HANDOFF_MISSING');
    }
    return Object.assign({}, result, {
      retained_packet_schema: RETAINED_PACKET_SCHEMA,
      retained_packet_sha256: input.retained_packet_sha256,
      retained_packet_consumed: true
    });
  }

  window.StegVerseExternalCounterpartReturnConsumer = Object.freeze({
    RESULT_SCHEMA,
    RETAINED_PACKET_SCHEMA,
    SDK_PROCESSING_HANDOFF_SCHEMA,
    retainedPacketToConsumerInput,
    buildSdkProcessingHandoff,
    consume,
    consumeRetainedPacket
  });
})();
