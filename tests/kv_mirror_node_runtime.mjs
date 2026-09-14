import fs from 'node:fs';

const root = globalThis;
root.window = root;
root.isSecureContext = true;
root.window.isSecureContext = true;

const source = fs.readFileSync(new URL('../assets/kv-mirror-node.js', import.meta.url), 'utf8');
(0, eval)(source);

const node = await window.StegVerseKVMirrorNode.buildNode();
const validation = await window.StegVerseKVMirrorNode.validateNode(node);

if (node.node_kind !== 'KV_MIRROR_Node') throw new Error('KV mirror node kind missing');
if (node.counterpart_pattern !== 'MIR NODE MIRROR') throw new Error('MIR mirror pattern not declared');
if (node.policy.kv_entry_point_required !== false) throw new Error('KV entry point became a transport prerequisite');
if (node.policy.kv_entry_point_preferred !== true) throw new Error('KV entry point not marked preferred');
if (node.policy.event_triggered !== true) throw new Error('event-triggered invariant missing');
if (node.policy.persistent_receiver !== false) throw new Error('persistent receiver regression');
if (node.policy.always_on_application_receiver_required !== false) throw new Error('always-on receiver regression');
if (node.policy.credential_authority !== 'TV/TVC') throw new Error('TV/TVC boundary missing');
if (node.policy.github_runtime_authority !== 'NONE') throw new Error('GitHub runtime authority regression');
if (node.live_kv_runtime_claimed !== false) throw new Error('live KV runtime falsely claimed');
if (node.live_provider_write_claimed !== false) throw new Error('provider write falsely claimed');
if (validation.state !== 'KV_MIRROR_NODE_VALIDATED') throw new Error('KV mirror validation failed');

const request = {
  profile: 'evaluator-read-review',
  manifest_sha256: 'sha256:' + 'a'.repeat(64),
  request_sha256: 'sha256:' + 'b'.repeat(64),
  prior_receipt_hash: 'sha256:' + 'c'.repeat(64)
};
const binding = await window.StegVerseKVMirrorNode.bindIntrRequest(node, request);
if (binding.state !== 'KV_MIRROR_INTR_REQUEST_BOUND_FOR_VALIDATION') throw new Error('request binding state missing');
if (binding.profile !== 'evaluator-read-review') throw new Error('request profile mismatch');
if (binding.manifest_sha256 !== request.manifest_sha256) throw new Error('manifest hash not retained');
if (binding.request_sha256 !== request.request_sha256) throw new Error('request hash not retained');
if (binding.prior_receipt_hash !== request.prior_receipt_hash) throw new Error('prior receipt hash not retained');
if (!/^sha256:[a-f0-9]{64}$/.test(binding.binding_sha256)) throw new Error('binding hash missing');

let rejectedRequiredKv = false;
try {
  const badNode = await window.StegVerseKVMirrorNode.buildNode({
    policy: { ...node.policy, kv_entry_point_required: true }
  });
  await window.StegVerseKVMirrorNode.validateNode(badNode);
} catch (error) {
  rejectedRequiredKv = error.code === 'KV_MIRROR_MUST_NOT_REQUIRE_KV_FOR_TRANSPORT';
}
if (!rejectedRequiredKv) throw new Error('KV transport prerequisite regression was not rejected');

let rejectedLiveRuntimeClaim = false;
try {
  await window.StegVerseKVMirrorNode.validateNode({ ...node, live_kv_runtime_claimed: true });
} catch (error) {
  rejectedLiveRuntimeClaim = error.code === 'KV_MIRROR_LIVE_RUNTIME_CLAIM_FORBIDDEN';
}
if (!rejectedLiveRuntimeClaim) throw new Error('live KV runtime claim was not rejected');

let rejectedUnacceptedProfile = false;
try {
  await window.StegVerseKVMirrorNode.bindIntrRequest(node, { ...request, profile: 'unknown-profile' });
} catch (error) {
  rejectedUnacceptedProfile = error.code === 'KV_MIRROR_INTR_PROFILE_NOT_ACCEPTED';
}
if (!rejectedUnacceptedProfile) throw new Error('unaccepted InTr profile was not rejected');

console.log(JSON.stringify({
  state: validation.state,
  node_kind: node.node_kind,
  node_sha256: validation.node_sha256,
  kv_entry_point_required: node.policy.kv_entry_point_required,
  kv_entry_point_preferred: node.policy.kv_entry_point_preferred,
  event_triggered: node.policy.event_triggered,
  persistent_receiver: node.policy.persistent_receiver,
  always_on_application_receiver_required: node.policy.always_on_application_receiver_required,
  credential_authority: node.policy.credential_authority,
  github_runtime_authority: node.policy.github_runtime_authority,
  binding_state: binding.state,
  binding_sha256: binding.binding_sha256
}));
