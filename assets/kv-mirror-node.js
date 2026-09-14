(() => {
  'use strict';

  const NODE_SCHEMA = 'stegverse.kv-mirror-node.entry-point/v1';
  const RECEIPT_SCHEMA = 'stegverse.kv-mirror-node.receipt/v1';
  const DEFAULT_NODE_ID = 'KV-MIRROR-NODE-ENTRYPOINT-0001';
  const DEFAULT_PROFILE_ID = 'KV_ENTRY_POINT';

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

  async function sha256Utf8(text) {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return `sha256:${bytesToHex(digest)}`;
  }

  async function sha256Value(value) {
    return sha256Utf8(canonical(value));
  }

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function normalizeHash(value, code) {
    const text = String(value || '').trim().toLowerCase();
    const hex = text.startsWith('sha256:') ? text.slice(7) : text;
    if (!/^[a-f0-9]{64}$/.test(hex)) fail(code);
    return `sha256:${hex}`;
  }

  function nonEmpty(value, code) {
    const text = String(value || '').trim();
    if (!text) fail(code);
    return text;
  }

  function normalizeBoolean(value, code) {
    if (typeof value !== 'boolean') fail(code);
    return value;
  }

  function validateProvider(provider) {
    if (!provider || typeof provider !== 'object' || Array.isArray(provider)) {
      fail('KV_MIRROR_PROVIDER_REQUIRED');
    }
    const out = {
      provider_id: nonEmpty(provider.provider_id, 'KV_MIRROR_PROVIDER_ID_REQUIRED'),
      provider_class: nonEmpty(provider.provider_class, 'KV_MIRROR_PROVIDER_CLASS_REQUIRED'),
      adapter_profile: nonEmpty(provider.adapter_profile, 'KV_MIRROR_PROVIDER_ADAPTER_PROFILE_REQUIRED'),
      owner_authorized: normalizeBoolean(provider.owner_authorized, 'KV_MIRROR_PROVIDER_OWNER_AUTHORIZED_REQUIRED'),
      write_capable: normalizeBoolean(provider.write_capable, 'KV_MIRROR_PROVIDER_WRITE_CAPABLE_REQUIRED'),
      read_capable: normalizeBoolean(provider.read_capable, 'KV_MIRROR_PROVIDER_READ_CAPABLE_REQUIRED')
    };
    if (out.owner_authorized !== true) fail('KV_MIRROR_PROVIDER_OWNER_AUTHORIZATION_REQUIRED');
    if (out.write_capable !== true || out.read_capable !== true) fail('KV_MIRROR_PROVIDER_READ_WRITE_REQUIRED');
    return out;
  }

  function validateNamespaces(namespaces) {
    if (!namespaces || typeof namespaces !== 'object' || Array.isArray(namespaces)) {
      fail('KV_MIRROR_NAMESPACES_REQUIRED');
    }
    const required = ['principal', 'device', 'node', 'request', 'receipt', 'continuity', 'reconstruction'];
    const out = {};
    for (const key of required) out[key] = nonEmpty(namespaces[key], `KV_MIRROR_NAMESPACE_${key.toUpperCase()}_REQUIRED`);
    return out;
  }

  function validatePolicy(policy) {
    if (!policy || typeof policy !== 'object' || Array.isArray(policy)) fail('KV_MIRROR_POLICY_REQUIRED');
    const out = {
      credential_authority: nonEmpty(policy.credential_authority, 'KV_MIRROR_CREDENTIAL_AUTHORITY_REQUIRED'),
      execution_authority: nonEmpty(policy.execution_authority, 'KV_MIRROR_EXECUTION_AUTHORITY_REQUIRED'),
      github_runtime_authority: nonEmpty(policy.github_runtime_authority, 'KV_MIRROR_GITHUB_RUNTIME_AUTHORITY_REQUIRED'),
      authority_effect: nonEmpty(policy.authority_effect, 'KV_MIRROR_AUTHORITY_EFFECT_REQUIRED'),
      kv_entry_point_required: normalizeBoolean(policy.kv_entry_point_required, 'KV_MIRROR_REQUIRED_FLAG_REQUIRED'),
      kv_entry_point_preferred: normalizeBoolean(policy.kv_entry_point_preferred, 'KV_MIRROR_PREFERRED_FLAG_REQUIRED'),
      event_triggered: normalizeBoolean(policy.event_triggered, 'KV_MIRROR_EVENT_TRIGGERED_REQUIRED'),
      persistent_receiver: normalizeBoolean(policy.persistent_receiver, 'KV_MIRROR_PERSISTENT_RECEIVER_REQUIRED'),
      always_on_application_receiver_required: normalizeBoolean(
        policy.always_on_application_receiver_required,
        'KV_MIRROR_ALWAYS_ON_RECEIVER_REQUIRED'
      ),
      second_user_device_required: normalizeBoolean(
        policy.second_user_device_required,
        'KV_MIRROR_SECOND_DEVICE_REQUIRED'
      )
    };
    if (out.credential_authority !== 'TV/TVC') fail('KV_MIRROR_TV_TVC_REQUIRED');
    if (out.execution_authority !== 'NONE') fail('KV_MIRROR_EXECUTION_AUTHORITY_MUST_BE_NONE');
    if (out.github_runtime_authority !== 'NONE') fail('KV_MIRROR_GITHUB_AUTHORITY_MUST_BE_NONE');
    if (out.authority_effect !== 'NONE_CUSTODY_PROFILE_ONLY') fail('KV_MIRROR_AUTHORITY_EFFECT_INVALID');
    if (out.kv_entry_point_required !== false) fail('KV_MIRROR_MUST_NOT_REQUIRE_KV_FOR_TRANSPORT');
    if (out.kv_entry_point_preferred !== true) fail('KV_MIRROR_MUST_PREFER_KV_CUSTODY');
    if (out.event_triggered !== true) fail('KV_MIRROR_EVENT_TRIGGERED_REQUIRED_TRUE');
    if (out.persistent_receiver !== false) fail('KV_MIRROR_PERSISTENT_RECEIVER_FORBIDDEN');
    if (out.always_on_application_receiver_required !== false) fail('KV_MIRROR_ALWAYS_ON_FORBIDDEN');
    if (out.second_user_device_required !== false) fail('KV_MIRROR_SECOND_DEVICE_FORBIDDEN');
    return out;
  }

  function validateBindings(bindings) {
    if (!bindings || typeof bindings !== 'object' || Array.isArray(bindings)) fail('KV_MIRROR_BINDINGS_REQUIRED');
    return {
      accepted_intr_profiles: Array.isArray(bindings.accepted_intr_profiles)
        ? bindings.accepted_intr_profiles.map((item) => nonEmpty(item, 'KV_MIRROR_INTR_PROFILE_REQUIRED'))
        : fail('KV_MIRROR_INTR_PROFILES_REQUIRED'),
      request_manifest_hash_required: normalizeBoolean(
        bindings.request_manifest_hash_required,
        'KV_MIRROR_REQUEST_MANIFEST_HASH_FLAG_REQUIRED'
      ),
      receipt_hash_chain_required: normalizeBoolean(
        bindings.receipt_hash_chain_required,
        'KV_MIRROR_RECEIPT_HASH_CHAIN_FLAG_REQUIRED'
      ),
      exact_request_binding_required: normalizeBoolean(
        bindings.exact_request_binding_required,
        'KV_MIRROR_EXACT_REQUEST_BINDING_FLAG_REQUIRED'
      ),
      write_once_receipt_bundle_required: normalizeBoolean(
        bindings.write_once_receipt_bundle_required,
        'KV_MIRROR_WRITE_ONCE_BUNDLE_FLAG_REQUIRED'
      ),
      reconstruction_readback_required_for_completion: normalizeBoolean(
        bindings.reconstruction_readback_required_for_completion,
        'KV_MIRROR_RECONSTRUCTION_READBACK_FLAG_REQUIRED'
      )
    };
  }

  function buildCandidate(overrides = {}) {
    return {
      schema: NODE_SCHEMA,
      node_id: overrides.node_id || DEFAULT_NODE_ID,
      profile_id: overrides.profile_id || DEFAULT_PROFILE_ID,
      node_kind: 'KV_MIRROR_Node',
      counterpart_pattern: 'MIR NODE MIRROR',
      provenance: 'DETERMINISTIC_MIRROR_ONLY',
      principal_ref: overrides.principal_ref || 'principal:owner-local-kv-entrypoint-mirror',
      device_ref: overrides.device_ref || 'device:owner-current-device',
      provider: validateProvider(overrides.provider || {
        provider_id: 'provider:owner-cloud-slot-001',
        provider_class: 'OWNER_CONTROLLED_PERSONAL_CLOUD',
        adapter_profile: 'intr-kv-entrypoint-adapter-v1',
        owner_authorized: true,
        write_capable: true,
        read_capable: true
      }),
      namespaces: validateNamespaces(overrides.namespaces || {
        principal: '/kv/principal/current',
        device: '/kv/devices/current',
        node: '/kv/nodes/kv-mirror-node',
        request: '/kv/intr/requests',
        receipt: '/kv/intr/receipts',
        continuity: '/kv/continuity',
        reconstruction: '/kv/reconstruction'
      }),
      policy: validatePolicy(overrides.policy || {
        credential_authority: 'TV/TVC',
        execution_authority: 'NONE',
        github_runtime_authority: 'NONE',
        authority_effect: 'NONE_CUSTODY_PROFILE_ONLY',
        kv_entry_point_required: false,
        kv_entry_point_preferred: true,
        event_triggered: true,
        persistent_receiver: false,
        always_on_application_receiver_required: false,
        second_user_device_required: false
      }),
      bindings: validateBindings(overrides.bindings || {
        accepted_intr_profiles: ['evaluator-read-review', 'SDK:EvaluatorReviewIngress'],
        request_manifest_hash_required: true,
        receipt_hash_chain_required: true,
        exact_request_binding_required: true,
        write_once_receipt_bundle_required: true,
        reconstruction_readback_required_for_completion: true
      }),
      live_kv_runtime_claimed: false,
      live_provider_write_claimed: false,
      authority_effect: 'NONE'
    };
  }

  async function buildNode(overrides = {}) {
    const node = buildCandidate(overrides);
    return Object.freeze(Object.assign({}, node, { node_sha256: await sha256Value(node) }));
  }

  async function validateNode(node) {
    if (!node || typeof node !== 'object' || Array.isArray(node)) fail('KV_MIRROR_NODE_REQUIRED');
    if (node.schema !== NODE_SCHEMA) fail('KV_MIRROR_NODE_SCHEMA_INVALID');
    nonEmpty(node.node_id, 'KV_MIRROR_NODE_ID_REQUIRED');
    if (node.node_kind !== 'KV_MIRROR_Node') fail('KV_MIRROR_NODE_KIND_INVALID');
    if (node.provenance !== 'DETERMINISTIC_MIRROR_ONLY') fail('KV_MIRROR_PROVENANCE_INVALID');
    nonEmpty(node.principal_ref, 'KV_MIRROR_PRINCIPAL_REF_REQUIRED');
    nonEmpty(node.device_ref, 'KV_MIRROR_DEVICE_REF_REQUIRED');
    validateProvider(node.provider);
    validateNamespaces(node.namespaces);
    validatePolicy(node.policy);
    const bindings = validateBindings(node.bindings);
    if (!bindings.accepted_intr_profiles.includes('evaluator-read-review')) fail('KV_MIRROR_EVALUATOR_PROFILE_REQUIRED');
    for (const [key, value] of Object.entries(bindings)) {
      if (key !== 'accepted_intr_profiles' && value !== true) fail(`KV_MIRROR_BINDING_${key.toUpperCase()}_MUST_BE_TRUE`);
    }
    if (node.live_kv_runtime_claimed !== false) fail('KV_MIRROR_LIVE_RUNTIME_CLAIM_FORBIDDEN');
    if (node.live_provider_write_claimed !== false) fail('KV_MIRROR_LIVE_WRITE_CLAIM_FORBIDDEN');
    if (node.authority_effect !== 'NONE') fail('KV_MIRROR_NODE_AUTHORITY_EFFECT_FORBIDDEN');
    const body = clone(node);
    const suppliedHash = body.node_sha256 ? normalizeHash(body.node_sha256, 'KV_MIRROR_NODE_HASH_INVALID') : null;
    delete body.node_sha256;
    const computedHash = await sha256Value(body);
    if (suppliedHash && suppliedHash !== computedHash) fail('KV_MIRROR_NODE_HASH_MISMATCH');
    return Object.freeze({ schema: RECEIPT_SCHEMA, state: 'KV_MIRROR_NODE_VALIDATED', node_id: node.node_id, node_sha256: computedHash, authority_effect: 'NONE' });
  }

  async function bindIntrRequest(node, request) {
    const receipt = await validateNode(node);
    if (!request || typeof request !== 'object' || Array.isArray(request)) fail('KV_MIRROR_INTR_REQUEST_REQUIRED');
    const profile = nonEmpty(request.profile || request.intr_profile, 'KV_MIRROR_INTR_REQUEST_PROFILE_REQUIRED');
    if (!node.bindings.accepted_intr_profiles.includes(profile)) fail('KV_MIRROR_INTR_PROFILE_NOT_ACCEPTED');
    const manifestHash = normalizeHash(request.manifest_sha256 || request.manifest_hash, 'KV_MIRROR_INTR_REQUEST_MANIFEST_HASH_REQUIRED');
    const requestHash = normalizeHash(request.request_sha256 || request.request_hash, 'KV_MIRROR_INTR_REQUEST_HASH_REQUIRED');
    const priorReceiptHash = normalizeHash(request.prior_receipt_hash, 'KV_MIRROR_INTR_PRIOR_RECEIPT_HASH_REQUIRED');
    const body = {
      schema: 'stegverse.kv-mirror-node.intr-request-binding/v1',
      state: 'KV_MIRROR_INTR_REQUEST_BOUND_FOR_VALIDATION',
      node_id: receipt.node_id,
      node_sha256: receipt.node_sha256,
      profile,
      manifest_sha256: manifestHash,
      request_sha256: requestHash,
      prior_receipt_hash: priorReceiptHash,
      custody_namespace: node.namespaces.request,
      receipt_namespace: node.namespaces.receipt,
      authority_effect: 'NONE'
    };
    return Object.freeze(Object.assign({}, body, { binding_sha256: await sha256Value(body) }));
  }

  const api = Object.freeze({
    NODE_SCHEMA,
    RECEIPT_SCHEMA,
    buildNode,
    validateNode,
    bindIntrRequest
  });

  if (typeof window !== 'undefined') window.StegVerseKVMirrorNode = api;
  if (typeof globalThis !== 'undefined') globalThis.StegVerseKVMirrorNode = api;
})();
