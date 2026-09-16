"use strict";

/* Rebinds the existing root-scoped Universal InTr worker from retired Canonical Work
 * lineage to the active StegBrowser manifest invocation. This does not create a
 * second service worker, listener, scheduler, materializer, WorkerCoordinator,
 * credential path, device path, or execution authority.
 */
(function () {
  var INGRESS_SCHEMA = "stegverse.stegbrowser-intr-materialization-ingress/v1";
  var BINDING_SCHEMA = "stegverse.stegbrowser-universal-intr-invocation-binding/v1";
  var DEST = JSON.stringify({ boundary: "STEGOS_ECOSYSTEM", subsystem: "StegBrowser:ManifestInvocation" });
  var DOWNSTREAM_OWNER = "StegVerse-Labs/.github#1952";
  var GOAL_ID = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001";
  var PARENT_TASK_ID = "STEG-BROWSER-RUNTIME-MATERIALIZATION-REMEDIATION-001";
  var COSV_ID = "40000100100000";
  var NONCE = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z";
  var MANIFEST_SHA256 = "fcde63451bf612df8f3b2b62fa6766670dc880f2fcb66605680a2af6f2096f74";
  var baseProfile = profile;
  var baseAdmitValidatedTrigger = admitValidatedTrigger;

  function invocationBinding(req, entry) {
    var binding = entry && entry.stegbrowser_invocation;
    require(req && req.schema === MATERIALIZATION_SCHEMA, "stegbrowser_materialization_schema_invalid");
    require(req.state === "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION", "stegbrowser_materialization_state_invalid");
    require(JSON.stringify(req.destination) === DEST, "stegbrowser_destination_invalid");
    require(req.downstream_owner_ref === DOWNSTREAM_OWNER, "stegbrowser_owner_invalid");
    require(req.request_grants_execution_authority === false && req.transport_grants_execution_authority === false && req.claim_or_fence_minted === false, "stegbrowser_authority_forbidden");
    require(req.credential_authority === "TV/TVC" && req.github_token_runtime_authority === "NONE", "stegbrowser_credential_boundary_invalid");
    require(req.authority_effect === "NONE_REQUEST_ONLY", "stegbrowser_authority_effect_invalid");
    require(binding && binding.schema === BINDING_SCHEMA, "stegbrowser_binding_schema_invalid");
    require(binding.state === "BOUND_FOR_UNIVERSAL_INTR_MATERIALIZATION", "stegbrowser_binding_state_invalid");
    require(binding.goal_task_id === GOAL_ID && binding.parent_task_id === PARENT_TASK_ID && binding.cosv_task_vector === COSV_ID, "stegbrowser_goal_identity_invalid");
    require(binding.invocation_request_nonce === NONCE, "stegbrowser_nonce_invalid");
    require(binding.manifest_sha256 === MANIFEST_SHA256, "stegbrowser_manifest_invalid");
    require(binding.node_id === entry.node_id && binding.interlock_id === entry.interlock_id, "stegbrowser_node_interlock_binding_invalid");
    require(binding.registration_receipt_sha256 && binding.request_mutated === false, "stegbrowser_registration_or_request_invariant_invalid");
    require(binding.resident_request_sweep_required === false && binding.control_plane_source_package_required === false, "stegbrowser_non_gating_source_invariant_invalid");
    require(binding.credential_authority === "TV/TVC" && binding.github_runtime_authority === "NONE" && binding.authority_effect === "NONE_BINDING_ONLY", "stegbrowser_binding_authority_invalid");
    require(req.payload_hash === entry.binding_hash, "stegbrowser_payload_hash_invalid");
    require(req.payload_ref === "opaque://stegbrowser-manifest-invocation/" + String(entry.binding_hash || "").replace(/^sha256:/, ""), "stegbrowser_payload_ref_invalid");
    return binding;
  }

  function ingressReceipt(entry, req, actual) {
    var binding = invocationBinding(req, entry);
    return {
      schema: INGRESS_SCHEMA,
      state: "INGRESS_ADMITTED",
      goal_task_id: GOAL_ID,
      parent_task_id: PARENT_TASK_ID,
      cosv_task_vector: COSV_ID,
      invocation_request_nonce: NONCE,
      manifest_sha256: MANIFEST_SHA256,
      materialization_id: req.materialization_id,
      request_hash: req.request_hash,
      transport_intent_hash: req.transport_intent_hash,
      payload_hash: req.payload_hash,
      payload_ref: req.payload_ref,
      transport_origin: "STEGOS_NODE_OUTBOX",
      node_id: entry.node_id,
      interlock_id: entry.interlock_id,
      registration_receipt_sha256: binding.registration_receipt_sha256,
      outbox_entry_hash: entry.outbox_entry_hash,
      transport_payload_sha256: actual,
      exact_request_validated: true,
      write_once_persisted: true,
      current_device_ingress_observed: true,
      runtime_surface: "CURRENT_USER_IPHONE_SERVICE_WORKER",
      runtime_owner: "REGISTERED_STEGVERSE_NODE",
      runtime_execution_attempted: false,
      workercoordinator_claim_observed: false,
      workercoordinator_fence_observed: false,
      claim_or_fence_minted: false,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      request_grants_execution_authority: false,
      transport_grants_execution_authority: false,
      heartbeat_grants_execution_authority: false,
      interlock_intr_transition_authority_preserved: true,
      external_device_required: false,
      second_user_operated_device_allowed: false,
      authority_effect: "NONE_INGRESS_ONLY",
      admitted_at: new Date().toISOString()
    };
  }

  profile = function () {
    var current = baseProfile();
    var profiles = Array.isArray(current.profiles) ? current.profiles.slice() : [];
    var retired = profiles.indexOf("CanonicalWork:Ingress");
    if (retired !== -1) { profiles.splice(retired, 1); }
    if (profiles.indexOf("StegBrowser:ManifestInvocation") === -1) { profiles.push("StegBrowser:ManifestInvocation"); }
    current.profiles = profiles;
    delete current.canonical_work;
    current.stegbrowser_manifest_invocation = {
      goal_task_id: GOAL_ID,
      parent_task_id: PARENT_TASK_ID,
      cosv_task_vector: COSV_ID,
      invocation_request_nonce: NONCE,
      manifest_sha256: MANIFEST_SHA256,
      downstream_owner_ref: DOWNSTREAM_OWNER,
      runtime_surface: "CURRENT_USER_IPHONE_SERVICE_WORKER",
      authority_effect: "NONE_DISCOVERY_EVIDENCE_ONLY"
    };
    return current;
  };

  admitValidatedTrigger = function (entry, req, actual) {
    var destination = JSON.stringify(req && req.destination);
    if (destination !== DEST || !req || req.downstream_owner_ref !== DOWNSTREAM_OWNER) {
      return baseAdmitValidatedTrigger(entry, req, actual);
    }
    invocationBinding(req, entry);
    return putOnce(REQUESTS, req.materialization_id, {
      materialization_id: req.materialization_id,
      request_hash: req.request_hash,
      entry_hash: entry.outbox_entry_hash,
      request: req,
      profile: "StegBrowser:ManifestInvocation",
      admitted_at: new Date().toISOString()
    }).then(function () { return ingressReceipt(entry, req, actual); });
  };
}());
