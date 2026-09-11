const PURPOSE = "CURRENT_IPHONE_TESTFLIGHT_SIGNING";
const SHA256_RE = /^sha256:[0-9a-f]{64}$/;

function requireOpaqueCommitment(value, field) {
  if (typeof value !== "string" || !SHA256_RE.test(value)) {
    throw new Error(`kv_projection_${field}_missing_or_invalid`);
  }
  return value;
}

export function validateKvBoundEphemeralProjectionContext(context) {
  if (!context || typeof context !== "object") {
    throw new Error("kv_projection_context_required");
  }
  if (context.schema !== "stegos.kv-bound-ephemeral-projection-context/v1") {
    throw new Error("kv_projection_schema_mismatch");
  }
  if (context.purpose !== PURPOSE) {
    throw new Error("kv_projection_purpose_mismatch");
  }
  if (context.entry_state !== "ADMITTED") {
    throw new Error("kv_projection_entry_not_admitted");
  }
  if (context.browser_capability_state !== "OBSERVED_COMPATIBLE") {
    throw new Error("kv_projection_browser_capability_not_observed");
  }
  if (context.persistence_effect !== "NONE_EPHEMERAL_CONTEXT_ONLY") {
    throw new Error("kv_projection_persistence_effect_mismatch");
  }
  if (context.authority_effect !== "NONE_PROJECTION_GATE_ONLY") {
    throw new Error("kv_projection_authority_effect_mismatch");
  }
  return Object.freeze({
    schema: "stegos.kv-bound-ephemeral-projection-context/v1",
    purpose: PURPOSE,
    entry_state: "ADMITTED",
    kv_transition_commitment: requireOpaqueCommitment(context.kv_transition_commitment, "kv_transition_commitment"),
    admission_commitment: requireOpaqueCommitment(context.admission_commitment, "admission_commitment"),
    browser_capability_state: "OBSERVED_COMPATIBLE",
    browser_capability_commitment: requireOpaqueCommitment(context.browser_capability_commitment, "browser_capability_commitment"),
    persistence_effect: "NONE_EPHEMERAL_CONTEXT_ONLY",
    authority_effect: "NONE_PROJECTION_GATE_ONLY",
  });
}

export function consumeInjectedKvBoundEphemeralProjectionContext(globalObject = globalThis) {
  const slot = "__STEGVERSE_KV_PROJECTION_CONTEXT__";
  const candidate = globalObject[slot];
  try {
    return validateKvBoundEphemeralProjectionContext(candidate);
  } finally {
    try { delete globalObject[slot]; } catch (_) { globalObject[slot] = undefined; }
  }
}
