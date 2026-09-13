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
async function sha256Value(value) {
  const bytes = new TextEncoder().encode(canonical(value));
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return 'sha256:' + Buffer.from(digest).toString('hex');
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
const artifactBytes = new TextEncoder().encode(canonical(returnArtifact));
const artifactHash = 'sha256:' + Buffer.from(await crypto.subtle.digest('SHA-256', artifactBytes)).toString('hex');

const adapterSource = fs.readFileSync(new URL('../assets/mir-accounting-return-v1.js', import.meta.url), 'utf8');
const consumerSource = fs.readFileSync(new URL('../assets/external-counterpart-return-consumer.js', import.meta.url), 'utf8');
(0, eval)(adapterSource);
(0, eval)(consumerSource);

const result = await window.StegVerseExternalCounterpartReturnConsumer.consume({
  test_id: 'MIR-STEGVERSE-HISTORICAL-ACCOUNTING-RUN-002',
  revision: 1,
  manifest,
  manifest_hash: manifestHash,
  manifest_continuation: returnArtifact.manifest_continuation,
  response_to: correlation,
  response_class: 'MIR_HISTORICAL_ACCOUNTING',
  response_mode: 'SOURCE_NATIVE_RESULT',
  counterparty_ref: 'MIR_NODE_MIRROR',
  counterpart_mode: 'STEGOS_EXTERNAL_COUNTERPART_MIRROR',
  external_system_profile: 'MIR',
  artifact_media_type: 'application/vnd.stegverse.external-counterpart-return+json',
  artifact_bytes: artifactBytes,
  artifact_sha256: artifactHash
});

if (result.state !== 'EXTERNAL_COUNTERPART_RETURN_CONSUMED') throw new Error('consumer state transition missing');
if (result.sdk_evaluator_ingress_state !== 'SDK_EVALUATOR_INGRESS_ADMITTED') throw new Error('SDK evaluator ingress transition missing');
if (result.stegverse_return_exit_receipt.transition_class !== 'STEGVERSE_RETURN_EXIT') throw new Error('STEGVERSE_RETURN_EXIT missing');
if (result.stegverse_return_exit_receipt.response_to !== correlation) throw new Error('return correlation mismatch');
if (result.stegverse_return_exit_receipt.manifest_sha256 !== manifestHash) throw new Error('return manifest mismatch');
if (nodeTransitions.length !== 1 || nodeTransitions[0].transition !== 'EXTERNAL_COUNTERPART_RETURN_ADMITTED') throw new Error('node transition not retained');

console.log(JSON.stringify({
  state: result.state,
  sdk_state: result.sdk_evaluator_ingress_state,
  transition_class: result.stegverse_return_exit_receipt.transition_class,
  response_to: result.response_to,
  manifest_hash: result.manifest_hash,
  materialization_id: result.materialization_id,
  node_transition: nodeTransitions[0].transition
}));
