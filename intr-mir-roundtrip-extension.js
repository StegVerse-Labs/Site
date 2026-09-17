"use strict";

/* MIR round-trip admission on the existing root-scoped Universal InTr service worker.
 * This adds no second service worker/runtime and grants no execution, credential,
 * routing, or transition authority. It only admits the exact registered-Node outbox
 * request and returns a current ingress receipt.
 */
(function () {
  var INGRESS_SCHEMA = "stegverse.mir-roundtrip-intr-materialization-ingress/v1";
  var DEST = JSON.stringify({ boundary: "STEGOS_ECOSYSTEM", subsystem: "MIR:MirrorRoundTrip" });
  var DOWNSTREAM_OWNER = "MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001";
  var GOAL_ID = "MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001";
  var ROOT_GOAL_ID = "MIR-STEGVERSE-SEPARATION-OF-POWERS-EVIDENCE-CONTRACT-001";
  var COSV_ID = "50000000100000";
  var baseProfile = profile;
  var baseAdmitValidatedTrigger = admitValidatedTrigger;

  function validateMir(req, entry) {
    require(req && req.schema === MATERIALIZATION_SCHEMA, "mir_materialization_schema_invalid");
    require(req.state === "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION", "mir_materialization_state_invalid");
    require(JSON.stringify(req.destination) === DEST, "mir_destination_invalid");
    require(req.downstream_owner_ref === DOWNSTREAM_OWNER, "mir_owner_invalid");
    require(req.goal_task_id === GOAL_ID && req.root_goal_task_id === ROOT_GOAL_ID && req.cosv_task_vector === COSV_ID, "mir_goal_identity_invalid");
    require(req.destination_profile === "MIR" && req.mir_destination === "STEGVERSE_OWNED_MIR_MIRROR", "mir_profile_invalid");
    require(req.request_grants_execution_authority === false && req.transport_grants_execution_authority === false && req.claim_or_fence_minted === false, "mir_authority_forbidden");
    require(req.credential_authority === "TV/TVC" && req.github_token_runtime_authority === "NONE", "mir_credential_boundary_invalid");
    require(req.event_triggered === true && req.always_on_receiver_required === false && req.second_user_device_required === false, "mir_event_availability_invalid");
    require(req.receiver_unavailable_disposition === "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION", "mir_unavailable_disposition_invalid");
    require(req.authority_effect === "NONE_REQUEST_ONLY", "mir_authority_effect_invalid");
    require(entry && entry.node_id && entry.interlock_id, "mir_node_binding_missing");
    return true;
  }

  function ingressReceipt(entry, req, actual) {
    validateMir(req, entry);
    return {
      schema: INGRESS_SCHEMA,
      state: "INGRESS_ADMITTED",
      goal_task_id: GOAL_ID,
      root_goal_task_id: ROOT_GOAL_ID,
      cosv_task_vector: COSV_ID,
      destination_profile: "MIR",
      mir_destination: "STEGVERSE_OWNED_MIR_MIRROR",
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
      claim_or_fence_minted: false,
      request_grants_execution_authority: false,
      transport_grants_execution_authority: false,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      interlock_intr_transition_authority_preserved: true,
      second_user_operated_device_required: false,
      authority_effect: "NONE_INGRESS_ONLY",
      admitted_at: new Date().toISOString()
    };
  }

  profile = function () {
    var current = baseProfile();
    var profiles = Array.isArray(current.profiles) ? current.profiles.slice() : [];
    if (profiles.indexOf("MIR:MirrorRoundTrip") === -1) profiles.push("MIR:MirrorRoundTrip");
    current.profiles = profiles;
    current.mir_roundtrip = {
      goal_task_id: GOAL_ID,
      root_goal_task_id: ROOT_GOAL_ID,
      cosv_task_vector: COSV_ID,
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
    validateMir(req, entry);
    return putOnce(REQUESTS, req.materialization_id, {
      materialization_id: req.materialization_id,
      request_hash: req.request_hash,
      entry_hash: entry.outbox_entry_hash,
      request: req,
      profile: "MIR:MirrorRoundTrip",
      admitted_at: new Date().toISOString()
    }).then(function () { return ingressReceipt(entry, req, actual); });
  };
}());
