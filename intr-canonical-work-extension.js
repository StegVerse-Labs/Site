"use strict";

/* Extends the existing root-scoped Universal InTr worker with one exact Canonical Work profile.
 * This file does not create a second service worker, router, scheduler, WorkerCoordinator,
 * credential path, or execution authority. It wraps the already-loaded base worker.
 */
(function () {
  var CANONICAL_WORK_INGRESS_SCHEMA = "stegverse.canonical-work-intr-materialization-ingress/v1";
  var CANONICAL_WORK_BINDING_SCHEMA = "stegverse.canonical-work-current-task-binding/v1";
  var CANONICAL_WORK_DEST = JSON.stringify({ boundary: "STEGOS_ECOSYSTEM", subsystem: "CanonicalWork:Ingress" });
  var CANONICAL_WORK_OWNER = "STEGVERSE-CANONICAL-WORK-COORDINATION-001";
  var TASK_ID = "STEG-BROWSER-RUNTIME-CONSUMPTION-001";
  var COSV_ID = "40000100100000";
  var REGISTRY_COMMIT = "f1a55fa4022e19b41f2a9f604978b08ece22f64c";
  var REGISTRY_GENERATION = 19;
  var SELECTED_SUBSTRATE = "ADMITTED-EPHEMERAL-STEGOS-NODE";
  var baseProfile = profile;
  var baseAdmitValidatedTrigger = admitValidatedTrigger;

  function canonicalWorkRequest(req, entry) {
    var binding = req && req.canonical_work;
    require(req && req.schema === MATERIALIZATION_SCHEMA, "canonical_work_materialization_schema_invalid");
    require(req.state === "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION", "canonical_work_materialization_state_invalid");
    require(JSON.stringify(req.destination) === CANONICAL_WORK_DEST, "canonical_work_destination_invalid");
    require(req.downstream_owner_ref === CANONICAL_WORK_OWNER, "canonical_work_owner_invalid");
    require(req.request_grants_execution_authority === false && req.transport_grants_execution_authority === false && req.claim_or_fence_minted === false, "canonical_work_authority_forbidden");
    require(req.credential_authority === "TV/TVC" && req.github_token_runtime_authority === "NONE", "canonical_work_credential_boundary_invalid");
    require(req.authority_effect === "NONE_REQUEST_ONLY", "canonical_work_authority_effect_invalid");
    require(binding && binding.schema === CANONICAL_WORK_BINDING_SCHEMA, "canonical_work_binding_schema_invalid");
    require(binding.task_id === TASK_ID && binding.cosv_id === COSV_ID, "canonical_work_task_identity_invalid");
    require(binding.registry_commit === REGISTRY_COMMIT && binding.registry_generation === REGISTRY_GENERATION, "canonical_work_registry_binding_invalid");
    require(binding.coordination_state === "ACTIVE" && binding.checkout_state === "CHECKED_OUT", "canonical_work_coordination_state_invalid");
    require(binding.selected_execution_substrate === SELECTED_SUBSTRATE, "canonical_work_substrate_invalid");
    require(binding.allowed_next_transition === "INGRESS_ADMITTED", "canonical_work_transition_invalid");
    require(binding.worker_claim_authority === "WORKERCOORDINATOR" && binding.worker_claim_projection_only === true, "canonical_work_worker_authority_invalid");
    require(binding.worker_claim_ref === null && binding.fence_ref === null, "canonical_work_preexisting_claim_forbidden");
    require(binding.interlock_intr_required === true && binding.task_registry_mints_execution_authority === false, "canonical_work_authority_model_invalid");
    require(binding.external_device_required === false && binding.second_user_operated_device_allowed === false, "canonical_work_device_boundary_invalid");
    require(entry && entry.node_id && entry.interlock_id, "canonical_work_registered_node_binding_missing");
    return binding;
  }

  function canonicalWorkReceipt(entry, req, actual) {
    var binding = canonicalWorkRequest(req, entry);
    return {
      schema: CANONICAL_WORK_INGRESS_SCHEMA,
      state: "INGRESS_ADMITTED",
      task_id: TASK_ID,
      cosv_id: COSV_ID,
      registry_commit: REGISTRY_COMMIT,
      registry_generation: REGISTRY_GENERATION,
      coordination_state_before: binding.coordination_state,
      checkout_state: binding.checkout_state,
      selected_execution_substrate: SELECTED_SUBSTRATE,
      materialization_id: req.materialization_id,
      request_hash: req.request_hash,
      transport_intent_hash: req.transport_intent_hash,
      payload_hash: req.payload_hash,
      transport_origin: "STEGOS_NODE_OUTBOX",
      node_id: entry.node_id,
      interlock_id: entry.interlock_id,
      outbox_entry_hash: entry.outbox_entry_hash,
      transport_payload_sha256: actual,
      exact_request_validated: true,
      write_once_persisted: true,
      current_device_ingress_observed: true,
      runtime_surface: "CURRENT_USER_IPHONE_SERVICE_WORKER",
      runtime_owner: "REGISTERED_STEGVERSE_NODE",
      runtime_execution_attempted: false,
      canonical_work_consumption_observed: false,
      workercoordinator_claim_observed: false,
      workercoordinator_fence_observed: false,
      claim_or_fence_minted: false,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      request_grants_execution_authority: false,
      transport_grants_execution_authority: false,
      heartbeat_grants_execution_authority: false,
      task_registry_mints_execution_authority: false,
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
    if (profiles.indexOf("CanonicalWork:Ingress") === -1) { profiles.push("CanonicalWork:Ingress"); }
    current.profiles = profiles;
    current.canonical_work = {
      task_id: TASK_ID,
      cosv_id: COSV_ID,
      registry_commit: REGISTRY_COMMIT,
      registry_generation: REGISTRY_GENERATION,
      selected_execution_substrate: SELECTED_SUBSTRATE,
      authority_effect: "NONE_DISCOVERY_EVIDENCE_ONLY"
    };
    return current;
  };

  admitValidatedTrigger = function (entry, req, actual) {
    var destination = JSON.stringify(req && req.destination);
    if (destination !== CANONICAL_WORK_DEST || !req || req.downstream_owner_ref !== CANONICAL_WORK_OWNER) {
      return baseAdmitValidatedTrigger(entry, req, actual);
    }
    canonicalWorkRequest(req, entry);
    return putOnce(REQUESTS, req.materialization_id, {
      materialization_id: req.materialization_id,
      request_hash: req.request_hash,
      entry_hash: entry.outbox_entry_hash,
      request: req,
      profile: "CanonicalWork:Ingress",
      admitted_at: new Date().toISOString()
    }).then(function () { return canonicalWorkReceipt(entry, req, actual); });
  };
}());
