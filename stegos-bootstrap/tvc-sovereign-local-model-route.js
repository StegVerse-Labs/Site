(function (root) {
  "use strict";
  var SCHEMA_VERSION = "stegverse.tvc.sovereign-local-model-route-receipt.v1";
  var PROOF_SCHEMA = "stegverse.sovereign-local-model-proof/v1";
  var VERIFIED = { VERIFIED_REFERENCE_MODEL_RUNTIME: true, VERIFIED_LOCAL_LLM_RUNTIME: true };
  var DEVICE_ENDPOINT = "https://stegverse.org/stegos-bootstrap/local-model";
  var DEVICE_SCOPE = "https://stegverse.org/stegos-bootstrap/";

  function cmp(a, b) { return a < b ? -1 : a > b ? 1 : 0; }
  function stableJson(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(stableJson).join(",") + "]"; }
    return "{" + Object.keys(value).sort(cmp).map(function (key) { return JSON.stringify(key) + ":" + stableJson(value[key]); }).join(",") + "}";
  }
  function hex(bytes) { return Array.prototype.map.call(bytes, function (b) { return b.toString(16).padStart(2, "0"); }).join(""); }
  function sha256(value) {
    var text = typeof value === "string" ? value : stableJson(value);
    return root.crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(function (digest) { return hex(new Uint8Array(digest)); });
  }
  function privateEndpoint(url) {
    try {
      var parsed = new URL(url);
      if (parsed.protocol !== "http:" && parsed.protocol !== "https:") { return false; }
      var host = parsed.hostname.toLowerCase();
      if (host === "localhost" || host === "localhost.localdomain" || host === "127.0.0.1" || host === "::1") { return true; }
      if (/\.stegverse(\.local)?$/.test(host)) { return true; }
      var parts = host.split(".").map(Number);
      if (parts.length === 4 && parts.every(function (x) { return Number.isInteger(x) && x >= 0 && x <= 255; })) {
        return parts[0] === 10 || parts[0] === 127 || (parts[0] === 169 && parts[1] === 254) || (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) || (parts[0] === 192 && parts[1] === 168);
      }
      return false;
    } catch (_error) { return false; }
  }
  function deviceEndpoint(url, proof) {
    var p = proof && proof.predicates || {};
    return Boolean(
      proof && proof.schema === PROOF_SCHEMA &&
      String(url || "").replace(/\/$/, "") === DEVICE_ENDPOINT &&
      proof.endpoint === DEVICE_ENDPOINT &&
      proof.endpoint_transport === "SERVICE_WORKER_LOCAL_INTERCEPT" &&
      proof.service_worker_scope === DEVICE_SCOPE &&
      p.browser_service_worker_runtime_observed === true &&
      p.device_local_intercepted_endpoint === true &&
      p.network_egress_required === false &&
      p.real_inference_response_observed === true &&
      proof.github_token_required === false &&
      proof.third_party_execution_platform_required === false &&
      proof.authority_effect === "NONE"
    );
  }
  function normalize(proof) {
    proof = proof || {};
    if (proof.schema === PROOF_SCHEMA) {
      var p = proof.predicates || {};
      var selected = ((proof.selection || {}).selected || {});
      return {
        proof_complete: VERIFIED[String(proof.state || "")] === true,
        proof_state: String(proof.state || ""),
        runtime: String(selected.engine || proof.runtime || ""),
        model_id: String(proof.model_id || selected.model_ref || ""),
        real_inference: (p.real_model_process_observed === true || p.browser_service_worker_runtime_observed === true) && p.real_inference_response_observed === true,
        external_provider: p.third_party_inference_required !== false,
        authority_attached: p.model_output_grants_authority !== false || proof.authority_effect !== "NONE",
        canonical_proof: true
      };
    }
    var inference = proof.inference || {};
    return {
      proof_complete: String(proof.state || "") === "COMPLETE",
      proof_state: String(proof.state || ""),
      runtime: String(proof.runtime || ((proof.runtime_identity || {}).runtime || "")),
      model_id: String(inference.model_id || proof.model_id || ""),
      real_inference: proof.real_local_inference_observed === true || proof.real_inference_response_observed === true,
      external_provider: proof.external_provider_used === true,
      authority_attached: proof.authority_attached === true || inference.authority_attached === true,
      canonical_proof: false
    };
  }
  function evaluate(proof, endpoint) {
    endpoint = String(endpoint || "").replace(/\/$/, "");
    var claims = normalize(proof);
    var failures = [];
    if (!claims.proof_complete) { failures.push("runtime_proof_not_complete"); }
    if (!claims.runtime) { failures.push("runtime_identity_missing"); }
    if (!claims.model_id) { failures.push("model_id_missing"); }
    if (!claims.real_inference) { failures.push("real_inference_not_observed"); }
    if (claims.external_provider) { failures.push("external_provider_used"); }
    if (claims.authority_attached) { failures.push("model_authority_attached"); }
    var isDevice = deviceEndpoint(endpoint, proof);
    if (!privateEndpoint(endpoint) && !isDevice) { failures.push("endpoint_not_private_sovereign"); }
    return sha256(proof).then(function (proofHash) {
      var receipt = {
        schema_version: SCHEMA_VERSION,
        state: failures.length ? "DENY" : "ROUTE_ADMITTED",
        route_authority: "StegVerse-Labs/TVC",
        runtime: claims.runtime || "unresolved",
        model_id: claims.model_id || "unresolved",
        endpoint: endpoint,
        endpoint_transport: isDevice ? "SERVICE_WORKER_LOCAL_INTERCEPT" : "PRIVATE_HTTP",
        runtime_proof_schema: String(proof.schema || "legacy"),
        runtime_proof_state: claims.proof_state,
        canonical_micro_node_proof_consumed: claims.canonical_proof,
        runtime_proof_hash: proofHash,
        credential_requirement: "NONE",
        github_token_required: false,
        third_party_execution_platform_required: false,
        execution_authority: false,
        authority_effect: "NONE",
        reason: failures.length ? failures.join(",") : "verified sovereign local runtime may be routed without credentials"
      };
      return sha256(receipt).then(function (receiptHash) { receipt.receipt_hash = receiptHash; return receipt; });
    });
  }
  var api = { SCHEMA_VERSION: SCHEMA_VERSION, DEVICE_ENDPOINT: DEVICE_ENDPOINT, DEVICE_SCOPE: DEVICE_SCOPE, stableJson: stableJson, sha256: sha256, evaluate: evaluate };
  root.StegVerseTVCPortableRoute = api;
  if (typeof module !== "undefined" && module.exports) { module.exports = api; }
}(typeof self !== "undefined" ? self : globalThis));
