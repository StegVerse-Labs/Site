"use strict";

/* Bounded StegBrowser Master Records custody admission over the existing root Universal InTr worker.
 * This does not modify or impersonate the SV001 custody profile. It adds no service worker,
 * transport, dispatcher, scheduler, runtime plane, WorkerCoordinator authority, credential path,
 * or device dependency. Admission is not custody completion.
 */
(function () {
  var DEST = JSON.stringify({ boundary: "MASTER_RECORDS", subsystem: "StegBrowser:RuntimeReadinessCustody" });
  var DOWNSTREAM_OWNER = "master-records/orchestration";
  var GOVERNANCE_SCHEMA = "stegverse.master-records.stegbrowser-readiness-custody-transition-request/v1";
  var INGRESS_SCHEMA = "stegverse.master-records.stegbrowser-readiness-custody-intr-admission/v1";
  var TRANSITION_ID = "STEGBROWSER_RUNTIME_READINESS_MASTER_RECORDS_CUSTODY";
  var TASK_ID = "STEG-BROWSER-RUNTIME-CONNECTION-INGRESS-001";
  var COSV_ID = "40000100100000";
  var NONCE = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z";
  var SOURCE_SCHEMA = "stegbrowser-runtime-readiness/v1";
  var baseProfile = profile;
  var baseAdmitValidatedTrigger = admitValidatedTrigger;

  function shaUriLike(value) {
    return /^sha256:[0-9a-f]{64}$/.test(String(value || ""));
  }

  function validateGovernance(entry, req) {
    var g = req && req.governance_request;
    require(req && req.schema === MATERIALIZATION_SCHEMA, "stegbrowser_mr_materialization_schema_invalid");
    require(req.state === "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION", "stegbrowser_mr_materialization_state_invalid");
    require(JSON.stringify(req.destination) === DEST, "stegbrowser_mr_destination_invalid");
    require(req.downstream_owner_ref === DOWNSTREAM_OWNER, "stegbrowser_mr_owner_invalid");
    require(req.request_grants_execution_authority === false && req.transport_grants_execution_authority === false && req.claim_or_fence_minted === false, "stegbrowser_mr_transport_authority_forbidden");
    require(req.credential_authority === "TV/TVC" && req.github_token_runtime_authority === "NONE" && req.authority_effect === "NONE_REQUEST_ONLY", "stegbrowser_mr_transport_boundary_invalid");
    require(g && g.schema === GOVERNANCE_SCHEMA, "stegbrowser_mr_governance_schema_invalid");
    require(g.transition_id === TRANSITION_ID && g.canonical_task === TASK_ID && g.cosv_task_vector === COSV_ID, "stegbrowser_mr_governance_identity_invalid");
    require(g.authority_class === "MACHINE_GOVERNED" && g.human_approval_required === false && g.current_governance_required === true && g.prior_receipt_authorizes_transition === false, "stegbrowser_mr_governance_authority_invalid");
    require(g.source_evidence_schema === SOURCE_SCHEMA && g.invocation_request_nonce === NONCE, "stegbrowser_mr_source_identity_invalid");
    require(shaUriLike(g.runtime_readiness_receipt_sha256) && shaUriLike(g.readiness_node_receipt_sha256) && shaUriLike(g.registration_receipt_sha256) && shaUriLike(g.exported_bundle_sha256), "stegbrowser_mr_source_hash_invalid");
    require(g.source_receipt_sha256 === g.readiness_node_receipt_sha256, "stegbrowser_mr_source_receipt_binding_invalid");
    require(g.node_id === entry.node_id && g.interlock_id === entry.interlock_id, "stegbrowser_mr_node_interlock_binding_invalid");
    require(typeof g.lease_id === "string" && g.lease_id && typeof g.runtime_id === "string" && g.runtime_id, "stegbrowser_mr_runtime_identity_invalid");
    require(req.payload_hash === g.exported_bundle_sha256, "stegbrowser_mr_payload_hash_invalid");
    require(req.payload_ref === "opaque://stegbrowser-runtime-readiness-custody/" + g.readiness_node_receipt_sha256.slice(7), "stegbrowser_mr_payload_ref_invalid");
    require(g.credential_authority === "TV/TVC" && g.authority_effect === "NONE_REQUEST_ONLY", "stegbrowser_mr_governance_credential_invalid");
    return g;
  }

  function ingressReceipt(entry, req, actual) {
    var g = validateGovernance(entry, req);
    return {
      schema: INGRESS_SCHEMA,
      state: "INGRESS_ADMITTED",
      governance_decision: "ALLOW",
      transition_id: g.transition_id,
      canonical_task: g.canonical_task,
      cosv_task_vector: g.cosv_task_vector,
      source_evidence_schema: g.source_evidence_schema,
      source_receipt_sha256: g.source_receipt_sha256,
      runtime_readiness_receipt_sha256: g.runtime_readiness_receipt_sha256,
      readiness_node_receipt_sha256: g.readiness_node_receipt_sha256,
      invocation_request_nonce: g.invocation_request_nonce,
      node_id: g.node_id,
      interlock_id: g.interlock_id,
      registration_receipt_sha256: g.registration_receipt_sha256,
      lease_id: g.lease_id,
      runtime_id: g.runtime_id,
      exported_bundle_sha256: g.exported_bundle_sha256,
      materialization_id: req.materialization_id,
      request_hash: req.request_hash,
      transport_intent_hash: req.transport_intent_hash,
      payload_hash: req.payload_hash,
      payload_ref: req.payload_ref,
      transport_origin: "STEGOS_NODE_OUTBOX",
      outbox_entry_hash: entry.outbox_entry_hash,
      transport_payload_sha256: actual,
      exact_request_validated: true,
      write_once_persisted: true,
      current_governance_decision_observed: true,
      human_approval_checkpoint_inserted: false,
      prior_receipt_authorizes_transition: false,
      site_custody_authority: false,
      site_execution_authority: false,
      master_records_custody_observed: false,
      master_records_reconstruction_observed: false,
      runtime_execution_attempted: false,
      workercoordinator_claim_observed: false,
      workercoordinator_fence_observed: false,
      claim_or_fence_minted: false,
      request_grants_execution_authority: false,
      transport_grants_execution_authority: false,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      authority_effect: "NONE_INGRESS_ONLY",
      admitted_at: new Date().toISOString()
    };
  }

  profile = function () {
    var current = baseProfile();
    var profiles = Array.isArray(current.profiles) ? current.profiles.slice() : [];
    if (profiles.indexOf("MasterRecords:StegBrowserRuntimeReadinessCustody") === -1) {
      profiles.push("MasterRecords:StegBrowserRuntimeReadinessCustody");
    }
    current.profiles = profiles;
    current.stegbrowser_master_records_custody = {
      destination: { boundary: "MASTER_RECORDS", subsystem: "StegBrowser:RuntimeReadinessCustody" },
      transition_id: TRANSITION_ID,
      canonical_task: TASK_ID,
      cosv_task_vector: COSV_ID,
      source_evidence_schema: SOURCE_SCHEMA,
      invocation_request_nonce: NONCE,
      downstream_owner_ref: DOWNSTREAM_OWNER,
      admission_is_custody_completion: false,
      authority_effect: "NONE_DISCOVERY_EVIDENCE_ONLY"
    };
    return current;
  };

  admitValidatedTrigger = function (entry, req, actual) {
    var destination = JSON.stringify(req && req.destination);
    if (destination !== DEST || !req || req.downstream_owner_ref !== DOWNSTREAM_OWNER) {
      return baseAdmitValidatedTrigger(entry, req, actual);
    }
    validateGovernance(entry, req);
    return putOnce(REQUESTS, req.materialization_id, {
      materialization_id: req.materialization_id,
      request_hash: req.request_hash,
      entry_hash: entry.outbox_entry_hash,
      request: req,
      profile: "MasterRecords:StegBrowserRuntimeReadinessCustody",
      admitted_at: new Date().toISOString()
    }).then(function () { return ingressReceipt(entry, req, actual); });
  };
}());
