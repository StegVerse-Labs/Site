"use strict";

(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.StegVerseVisualRenderTransport = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  const REQUEST_SCHEMA = "stegverse.ecosystem_visual_render_request/v1";
  const RECEIPT_SCHEMA = "stegverse.ecosystem_visual_render_receipt/v1";
  const PROJECTION_SCHEMA = "stegverse.ecosystem_visual_projection/v1";
  const RENDERER_ROLE = "PROJECTION_ONLY";

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }
  function arr(value) { return Array.isArray(value) ? value : []; }
  function uniq(values) { return Array.from(new Set(arr(values).filter(Boolean).map(String))).sort(); }
  function exactArray(a, b) {
    return Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every((value, index) => value === b[index]);
  }

  function canonicalize(value) {
    if (value === null || typeof value !== "object") return value;
    if (Array.isArray(value)) return value.map(canonicalize);
    const out = {};
    Object.keys(value).sort().forEach((key) => { out[key] = canonicalize(value[key]); });
    return out;
  }

  function canonicalStringify(value) { return JSON.stringify(canonicalize(value)); }

  async function sha256Hex(value) {
    const text = typeof value === "string" ? value : canonicalStringify(value);
    if (typeof require === "function") {
      try {
        return require("node:crypto").createHash("sha256").update(text, "utf8").digest("hex");
      } catch (_) {}
    }
    if (typeof globalThis !== "undefined" && globalThis.crypto && globalThis.crypto.subtle) {
      const bytes = new TextEncoder().encode(text);
      const digest = await globalThis.crypto.subtle.digest("SHA-256", bytes);
      return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
    }
    fail("SHA-256 unavailable");
  }

  function assertProjection(projection) {
    if (!projection || projection.schema !== PROJECTION_SCHEMA) fail("unsupported projection schema");
    if (!projection.projection_id) fail("projection_id missing");
    if (!Array.isArray(projection.source_event_ids) || !projection.source_event_ids.length) fail("projection source_event_ids missing");
    if (!projection.provider || !Array.isArray(projection.provider.capabilities)) fail("projection provider capabilities missing");
    if (!projection.authority || projection.authority.renderer_role !== RENDERER_ROLE) fail("projection renderer role must be PROJECTION_ONLY");
    if (projection.authority.renderer_may_mutate_canonical_events !== false) fail("projection mutation authority prohibited");
    if (projection.authority.renderer_may_grant_admission !== false) fail("projection admission authority prohibited");
    if (projection.authority.renderer_may_invent_evidence !== false) fail("projection evidence authority prohibited");
  }

  function assertNoTransportSecrets(value) {
    const prohibited = ["endpoint", "credential", "credential_ref", "token", "authorization", "secret", "api_key", "apikey"];
    const visit = (node, path) => {
      if (!node || typeof node !== "object") return;
      Object.keys(node).forEach((key) => {
        if (prohibited.includes(String(key).toLowerCase())) fail("transport deployment field prohibited in canonical request: " + path.concat(key).join("."));
        visit(node[key], path.concat(key));
      });
    };
    visit(value, []);
  }

  async function buildRenderRequest(projection, options) {
    options = options || {};
    assertProjection(projection);
    assertNoTransportSecrets(options);

    const requested = uniq(options.requested_capabilities || projection.provider.capabilities);
    if (!requested.length) fail("at least one renderer capability required");
    const supported = new Set(projection.provider.capabilities.map(String));
    requested.forEach((capability) => { if (!supported.has(capability)) fail("unsupported requested capability " + capability); });

    const projectionSha = await sha256Hex(projection);
    const core = {
      schema: REQUEST_SCHEMA,
      projection: {
        schema: PROJECTION_SCHEMA,
        projection_id: String(projection.projection_id),
        sha256: projectionSha
      },
      source_event_ids: projection.source_event_ids.slice(),
      renderer: {
        provider_id: String(options.provider_id || projection.provider.id || "provider-neutral"),
        requested_capabilities: requested
      },
      interaction_policy: {
        selection_intents_only: true,
        refinement_intents_only: true,
        state_mutation_allowed: false
      },
      correlation_refs: uniq(options.correlation_refs || []),
      provenance: {
        canonical_projection_bound: true,
        generated_from_exact_projection: true
      },
      authority: {
        renderer_role: RENDERER_ROLE,
        renderer_may_mutate_canonical_events: false,
        renderer_may_grant_admission: false,
        renderer_may_invent_evidence: false,
        renderer_may_authorize_credentials: false,
        renderer_may_publish_state: false
      }
    };
    const requestIdSeed = await sha256Hex(core);
    const request = { ...core, request_id: String(options.request_id || ("render-request:" + requestIdSeed.slice(0, 24))) };
    validateRenderRequest(request, projection);
    return request;
  }

  async function hashRenderRequest(request) {
    validateRequestShape(request);
    return sha256Hex(request);
  }

  function validateRequestShape(request) {
    if (!request || request.schema !== REQUEST_SCHEMA) fail("unsupported render request schema");
    if (!request.request_id) fail("request_id missing");
    assertNoTransportSecrets(request);
    if (!request.projection || request.projection.schema !== PROJECTION_SCHEMA || !request.projection.projection_id || !/^[0-9a-f]{64}$/.test(String(request.projection.sha256 || ""))) fail("request projection binding invalid");
    if (!Array.isArray(request.source_event_ids) || !request.source_event_ids.length) fail("request source_event_ids missing");
    if (!request.renderer || !request.renderer.provider_id || !Array.isArray(request.renderer.requested_capabilities) || !request.renderer.requested_capabilities.length) fail("request renderer binding invalid");
    if (!request.interaction_policy || request.interaction_policy.selection_intents_only !== true || request.interaction_policy.refinement_intents_only !== true || request.interaction_policy.state_mutation_allowed !== false) fail("interaction policy must remain intent-only");
    if (!request.provenance || request.provenance.canonical_projection_bound !== true || request.provenance.generated_from_exact_projection !== true) fail("request provenance missing");
    if (!request.authority || request.authority.renderer_role !== RENDERER_ROLE) fail("request renderer role must be PROJECTION_ONLY");
    ["renderer_may_mutate_canonical_events", "renderer_may_grant_admission", "renderer_may_invent_evidence", "renderer_may_authorize_credentials", "renderer_may_publish_state"].forEach((key) => {
      if (request.authority[key] !== false) fail("request authority escalation prohibited: " + key);
    });
    return true;
  }

  async function validateRenderRequest(request, projection) {
    validateRequestShape(request);
    assertProjection(projection);
    if (request.projection.projection_id !== projection.projection_id) fail("projection_id mismatch");
    const projectionSha = await sha256Hex(projection);
    if (request.projection.sha256 !== projectionSha) fail("projection hash mismatch");
    if (!exactArray(request.source_event_ids, projection.source_event_ids)) fail("source event binding mismatch");
    const supported = new Set(projection.provider.capabilities.map(String));
    request.renderer.requested_capabilities.forEach((capability) => { if (!supported.has(String(capability))) fail("requested capability not supported by projection: " + capability); });
    return true;
  }

  async function validateRenderReceipt(receipt, request, projection) {
    validateRequestShape(request);
    await validateRenderRequest(request, projection);
    if (!receipt || receipt.schema !== RECEIPT_SCHEMA) fail("unsupported render receipt schema");
    if (!receipt.receipt_id) fail("receipt_id missing");
    if (receipt.request_id !== request.request_id) fail("receipt request_id mismatch");
    const expectedRequestSha = await hashRenderRequest(request);
    if (receipt.request_sha256 !== expectedRequestSha) fail("receipt request hash mismatch");
    if (!receipt.projection || receipt.projection.projection_id !== request.projection.projection_id || receipt.projection.sha256 !== request.projection.sha256) fail("receipt projection binding mismatch");
    if (!exactArray(receipt.source_event_ids, request.source_event_ids)) fail("receipt source event binding mismatch");
    if (!receipt.provider || !receipt.provider.provider_id) fail("receipt provider missing");
    if (!Array.isArray(receipt.provider.capabilities_used)) fail("receipt capabilities missing");
    const requested = new Set(request.renderer.requested_capabilities.map(String));
    receipt.provider.capabilities_used.forEach((capability) => { if (!requested.has(String(capability))) fail("receipt capability escalation: " + capability); });
    if (!["RENDERED", "REFUSED", "FAILED"].includes(receipt.status)) fail("unsupported receipt status");
    if (receipt.status === "RENDERED") {
      if (!receipt.artifact || typeof receipt.artifact !== "object" || !receipt.artifact.artifact_id) fail("RENDERED receipt requires artifact identity");
      if (!receipt.artifact.sha256 && !receipt.artifact.locator) fail("RENDERED receipt requires artifact hash or bounded locator");
      if (receipt.artifact.sha256 && !/^[0-9a-f]{64}$/.test(String(receipt.artifact.sha256))) fail("artifact sha256 invalid");
    }
    if (!Array.isArray(receipt.intents)) fail("receipt intents missing");
    receipt.intents.forEach((intent) => {
      if (!intent || !["SELECT", "REFINE"].includes(intent.kind)) fail("unsupported renderer intent");
      if (intent.state_change_authorized !== false) fail("renderer intent may not authorize state change");
      if (!intent.payload || typeof intent.payload !== "object" || Array.isArray(intent.payload)) fail("renderer intent payload invalid");
    });
    if (!receipt.provenance || receipt.provenance.request_bound !== true || receipt.provenance.projection_bound !== true || !Array.isArray(receipt.provenance.correlation_refs)) fail("receipt provenance missing");
    if (!receipt.authority || receipt.authority.renderer_role !== RENDERER_ROLE) fail("receipt renderer role must be PROJECTION_ONLY");
    ["canonical_event_mutation", "admission_granted", "evidence_invented", "credential_authorized", "publication_authorized", "custody_authority", "execution_authority"].forEach((key) => {
      if (receipt.authority[key] !== false) fail("receipt authority escalation prohibited: " + key);
    });
    return true;
  }

  return {
    REQUEST_SCHEMA,
    RECEIPT_SCHEMA,
    PROJECTION_SCHEMA,
    RENDERER_ROLE,
    canonicalStringify,
    sha256Hex,
    buildRenderRequest,
    hashRenderRequest,
    validateRenderRequest,
    validateRenderReceipt
  };
});
