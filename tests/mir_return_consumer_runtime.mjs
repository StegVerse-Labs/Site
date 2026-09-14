import fs from 'node:fs';

const root = globalThis;
root.window = root;
root.isSecureContext = true;
root.window.isSecureContext = true;
Object.defineProperty(root, 'navigator', {
  configurable: true,
  value: {
    serviceWorker: {
      register: async () => ({ scope: '/' }),
      ready: Promise.resolve({ active: true })
    }
  }
});

function canonical(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
}
async function sha256Bytes(bytes) {
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return 'sha256:' + Buffer.from(digest).toString('hex');
}
async function sha256Value(value) {
  return sha256Bytes(new TextEncoder().encode(canonical(value)));
}
async function sha256Utf8(text) {
  return sha256Bytes(new TextEncoder().encode(text));
}

let currentOutbox = null;
root.StegVerseGeneratedInTr = {
  PROFILES: { 'evaluator-read-review': {} },
  canonical,
  async buildIntent(profile, requestBytes, operation, operationId) {
    return {
      packet_id: 'INTR-RETURN-RUNTIME-001',
      payload_hash: await sha256Value(Array.from(requestBytes)),
      profile,
      operation,
      operation_id: operationId
    };
  },
  async buildMaterializationRequest(profile, intent, payloadRef, carrierBinding) {
    return {
      schema: 'stegverse.universal-intr-materialization-request/v1',
      profile,
      intent,
      payload_ref: payloadRef,
      carrier_binding: carrierBinding
    };
  }
};
root.StegVerseHBInTrCarrier = {
  async buildBinding(packetId, payloadHash) {
    return { packet_id: packetId, payload_hash: payloadHash, authority_effect: 'NONE' };
  }
};
const nodeTransitions = [];
root.StegVerseNodeContinuity = {
  async queueIntrMaterializationRequest(request) {
    currentOutbox = {
      materialization_id: 'INTR-MAT-111111111111111111111111',
      request_hash: 'sha256:' + '2'.repeat(64),
      transport_intent_hash: 'sha256:' + '3'.repeat(64),
      payload_hash: request.intent.payload_hash,
      node_id: 'SV-NODE-111111111111111111111111',
      interlock_id: 'SV-IL-111111111111111111111111',
      outbox_entry_hash: 'sha256:' + '4'.repeat(64)
    };
    return currentOutbox;
  },
  async appendCapabilityReceipt(input) {
    nodeTransitions.push(input);
    return {
      schema: 'stegos.node_capability_receipt.v1',
      transition: input.transition,
      capability: input.capability,
      step: input.step,
      resulting_state: input.resulting_state,
      evidence_ref: input.evidence_ref,
      authority_effect: 'NONE'
    };
  }
};

root.fetch = async (url, options = {}) => {
  if (url === '/intr/profile') {
    return {
      ok: true,
      status: 200,
      async json() {
        return {
          schema: 'stegverse.universal-intr-profiled-ingress/v1',
          protocol: 'InTr',
          profiles: ['SDK:EvaluatorReviewIngress'],
          materialization_path: '/intr/materialization',
          credential_authority: 'TV/TVC',
          execution_authority: 'NONE'
        };
      }
    };
  }
  if (url === '/intr/materialization' && options.method === 'POST') {
    if (!currentOutbox) throw new Error('runtime outbox must exist before materialization');
    return {
      ok: true,
      status: 202,
      async json() {
        return {
          state: 'INGRESS_ADMITTED',
          materialization_id: currentOutbox.materialization_id,
          request_hash: currentOutbox.request_hash,
          transport_intent_hash: currentOutbox.transport_intent_hash,
          payload_hash: currentOutbox.payload_hash,
          node_id: currentOutbox.node_id,
          interlock_id: currentOutbox.interlock_id,
          outbox_entry_hash: currentOutbox.outbox_entry_hash,
          transport_origin: 'STEGOS_NODE_OUTBOX',
          credential_authority: 'TV/TVC',
          github_token_runtime_authority: 'NONE',
          authority_effect: 'NONE_ADMISSION_ONLY'
        };
      }
    };
  }
  throw new Error(`unexpected runtime fetch ${url}`);
};

const manifest = {
  schema: 'stegverse.sdk.complete-manifest/v1',
  goal_task_id: 'MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001',
  cosv_id: '50000000100000',
  processing: { capability: 'mir_history_accounting', route_id: 'mir-run2' },
  state_transitions: [{ seq: 1, state: 'STEGVERSE_GOVERNANCE_COMPLETE', receipt: 'sv-r1' }]
};
const manifestHash = await sha256Value(manifest);
const correlation = 'mir-node-mirror-runtime-return-001';
const externalReceipt = {
  schema: 'stegverse.external-framework-boundary-receipt/v1',
  transition_class: 'EXTERNAL_FRAMEWORK_INGRESS',
  external_system_profile: 'MIR',
  counterpart: 'MIR NODE MIRROR',
  response_to: correlation,
  correlation_id: correlation,
  manifest_sha256: manifestHash,
  state_effect: 'EXTERNAL_COUNTERPART_RECEIVED',
  authority_namespace_effect: 'NONE',
  next_required_transition_class: 'STEGVERSE_RETURN_EXIT'
};
const returnArtifact = {
  schema: 'stegverse.external-counterpart-mirror.return/v1',
  response_mode: 'SOURCE_NATIVE_RESULT',
  manifest_continuation: {
    outbound_manifest: manifest,
    outbound_manifest_sha256: manifestHash,
    continuation_receipts: [externalReceipt],
    required_next_receipt: 'STEGVERSE_RETURN_EXIT'
  },
  source_native_result: {
    record_role: 'IMMUTABLE_STATE_TRANSITION_RECORD',
    accounting: { event_count: 2 }
  }
};

const retainedPayload = JSON.stringify({
  schema: 'stegverse.mir-profile-runtime.response/v1',
  state: 'MIR_PROFILE_MIRROR_EXECUTED',
  runtime_id: 'MIR-NODE-MIRROR-RUN2-ROUNDTRIP-001',
  correlation_id: correlation,
  counterpart: 'MIR NODE MIRROR',
  goal_task_id: 'MIR-STEGVERSE-HISTORICAL-ACCOUNTING-RUN-002',
  revision: 1,
  mirror_return: returnArtifact
});
const retainedPacket = {
  schema: 'stegverse.canonical-runtime-exact-return-packet/v1',
  profile_id: 'MIR',
  correlation_id: correlation,
  packet_sha256: await sha256Utf8(retainedPayload),
  packet_utf8: retainedPayload
};

const adapterSource = fs.readFileSync(new URL('../assets/mir-accounting-return-v1.js', import.meta.url), 'utf8');
const consumerSource = fs.readFileSync(new URL('../assets/external-counterpart-return-consumer.js', import.meta.url), 'utf8');
(0, eval)(adapterSource);
(0, eval)(consumerSource);

const prepared = await window.StegVerseExternalCounterpartReturnConsumer.retainedPacketToConsumerInput(retainedPacket);
if (prepared.manifest_hash !== manifestHash) throw new Error('retained packet manifest hash mismatch');
if (prepared.response_to !== correlation) throw new Error('retained packet correlation mismatch');
if (prepared.retained_packet_sha256 !== retainedPacket.packet_sha256) throw new Error('retained packet hash not carried forward');
if (prepared.artifact_bytes.length === 0) throw new Error('retained artifact bytes missing');

let rejectedSynthesizedFixture = false;
try {
  await window.StegVerseExternalCounterpartReturnConsumer.consumeRetainedPacket({
    schema: 'stegverse.external-counterpart-mirror.return/v1',
    profile_id: 'MIR',
    correlation_id: correlation,
    packet_sha256: retainedPacket.packet_sha256,
    packet_utf8: retainedPayload
  });
} catch (error) {
  rejectedSynthesizedFixture = error.code === 'RETAINED_MIR_PACKET_SCHEMA_INVALID';
}
if (!rejectedSynthesizedFixture) throw new Error('synthetic fixture without retained packet wrapper was not rejected');

let rejectedDigestMismatch = false;
try {
  await window.StegVerseExternalCounterpartReturnConsumer.consumeRetainedPacket({
    ...retainedPacket,
    packet_sha256: 'sha256:' + '0'.repeat(64)
  });
} catch (error) {
  rejectedDigestMismatch = error.code === 'RETAINED_MIR_PACKET_HASH_MISMATCH';
}
if (!rejectedDigestMismatch) throw new Error('retained packet digest mismatch was not rejected');

const result = await window.StegVerseExternalCounterpartReturnConsumer.consumeRetainedPacket(retainedPacket);
const handoff = result.sdk_processing_handoff;

if (result.state !== 'EXTERNAL_COUNTERPART_RETURN_CONSUMED') throw new Error('consumer state transition missing');
if (result.sdk_evaluator_ingress_state !== 'SDK_EVALUATOR_INGRESS_ADMITTED') throw new Error('SDK evaluator ingress transition missing');
if (result.stegverse_return_exit_receipt.transition_class !== 'STEGVERSE_RETURN_EXIT') throw new Error('STEGVERSE_RETURN_EXIT missing');
if (result.stegverse_return_exit_receipt.response_to !== correlation) throw new Error('return correlation mismatch');
if (result.stegverse_return_exit_receipt.manifest_sha256 !== manifestHash) throw new Error('return manifest mismatch');
if (result.retained_packet_consumed !== true) throw new Error('retained packet consumption not reported');
if (result.retained_packet_sha256 !== retainedPacket.packet_sha256) throw new Error('retained packet hash not retained in result');
if (nodeTransitions.length !== 1 || nodeTransitions[0].transition !== 'EXTERNAL_COUNTERPART_RETURN_ADMITTED') throw new Error('node transition not retained');
if (!handoff || handoff.schema !== 'stegverse.site.sdk-processing-handoff/v1') throw new Error('SDK processing handoff missing');
if (handoff.state !== 'READY_FOR_MANIFEST_SELECTED_SDK_PROCESSING') throw new Error('SDK processing handoff state missing');
if (handoff.response_to !== correlation) throw new Error('SDK processing handoff correlation mismatch');
if (handoff.manifest_hash !== manifestHash) throw new Error('SDK processing handoff manifest hash mismatch');
if (canonical(handoff.manifest) !== canonical(manifest)) throw new Error('SDK processing handoff manifest object mismatch');
if (handoff.retained_packet_sha256 !== retainedPacket.packet_sha256) throw new Error('SDK processing handoff retained packet hash mismatch');
if (handoff.sdk_evaluator_ingress_state !== 'SDK_EVALUATOR_INGRESS_ADMITTED') throw new Error('SDK processing handoff ingress state mismatch');
if (handoff.stegverse_return_exit_receipt.transition_class !== 'STEGVERSE_RETURN_EXIT') throw new Error('SDK processing handoff return exit missing');
if (handoff.node_transition_receipt.transition !== 'EXTERNAL_COUNTERPART_RETURN_ADMITTED') throw new Error('SDK processing handoff node receipt missing');
if (handoff.next_required_transition !== 'EXECUTE_MANIFEST_SELECTED_SDK_PROCESSING_AFTER_EVALUATOR_INGRESS') {
  throw new Error('SDK processing handoff next transition mismatch');
}
if (!/^sha256:[a-f0-9]{64}$/.test(handoff.handoff_sha256)) throw new Error('SDK processing handoff hash missing');

console.log(JSON.stringify({
  state: result.state,
  sdk_state: result.sdk_evaluator_ingress_state,
  transition_class: result.stegverse_return_exit_receipt.transition_class,
  response_to: result.response_to,
  manifest_hash: result.manifest_hash,
  materialization_id: result.materialization_id,
  node_transition: nodeTransitions[0].transition,
  retained_packet_sha256: result.retained_packet_sha256,
  retained_packet_consumed: result.retained_packet_consumed,
  sdk_processing_handoff_state: handoff.state,
  sdk_processing_handoff_sha256: handoff.handoff_sha256
}));
