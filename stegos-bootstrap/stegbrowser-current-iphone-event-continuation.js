"use strict";

(function (root) {
  var GOAL_ID = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001";
  var COSV_ID = "40000100100000";
  var NONCE = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z";
  var DESTINATION = "StegBrowser:ManifestInvocation";
  var NODE_DB = "stegos-node-v1";
  var NODE_DB_VERSION = 2;
  var NODE_OUTBOX = "intr_outbox";
  var RUNTIME_BINDING_URL = "/data/stegbrowser-manifest-runtime-binding.v1.json";

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }

  function openNodeDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(NODE_DB, NODE_DB_VERSION);
      request.onupgradeneeded = function () { request.transaction.abort(); };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("registered StegVerse Node database unavailable")); };
    });
  }

  function readOutboxEntry(materializationId) {
    return openNodeDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        if (!db.objectStoreNames.contains(NODE_OUTBOX)) { db.close(); reject(new Error("registered Node outbox unavailable")); return; }
        var tx = db.transaction(NODE_OUTBOX, "readonly");
        var req = tx.objectStore(NODE_OUTBOX).get(materializationId);
        req.onsuccess = function () { var value = req.result || null; db.close(); resolve(value); };
        req.onerror = function () { var error = req.error || new Error("registered Node outbox read failed"); db.close(); reject(error); };
      });
    }).then(function (entry) {
      if (!entry || entry.materialization_id !== materializationId) { fail("same-invocation Node outbox entry unavailable"); }
      if (!entry.stegbrowser_invocation || entry.stegbrowser_invocation.invocation_request_nonce !== NONCE) { fail("immutable invocation binding unavailable in Node outbox"); }
      return entry;
    });
  }

  function loadRuntimeBinding() {
    return fetch(RUNTIME_BINDING_URL, { credentials: "omit", cache: "no-store" }).then(function (response) {
      if (!response.ok) { fail("StegBrowser runtime binding HTTP " + response.status); }
      return response.json();
    }).then(function (binding) {
      if (!binding || binding.schema !== "stegverse.stegbrowser-universal-intr-invocation-binding/v1") { fail("StegBrowser runtime binding schema invalid"); }
      if (binding.goal_task_id !== GOAL_ID || binding.cosv_task_vector !== COSV_ID) { fail("StegBrowser runtime binding Goal/COSV mismatch"); }
      if (binding.destination && binding.destination !== DESTINATION) { fail("StegBrowser runtime binding destination mismatch"); }
      if (binding.route_owner !== "STEGVERSE" || binding.outbound_interlock_intr_endpoint !== "STEGVERSE_OWNED_INTR_EGRESS_ENDPOINT" || binding.far_end_receiver !== "STEGVERSE_OWNED_MIRROR_REFLECTOR") { fail("StegBrowser owned route binding mismatch"); }
      if (binding.authority_effect !== "NONE_ROUTE_BINDING_ONLY") { fail("StegBrowser runtime binding authority widened"); }
      return binding;
    });
  }

  function validateIngress(base) {
    var ingress = base && base.ingress_receipt;
    if (!base || base.state !== "INGRESS_ADMITTED" || !ingress) { fail("authentic A1/A2 ingress evidence required before EVENT_EPHEMERAL continuation"); }
    if (base.goal_task_id !== GOAL_ID || base.cosv_task_vector !== COSV_ID || base.invocation_request_nonce !== NONCE) { fail("A1/A2 Goal/COSV/nonce mismatch"); }
    if (ingress.state !== "INGRESS_ADMITTED" || ingress.goal_task_id !== GOAL_ID || ingress.cosv_task_vector !== COSV_ID || ingress.invocation_request_nonce !== NONCE) { fail("ingress receipt correlation mismatch"); }
    if (ingress.runtime_surface !== "CURRENT_USER_IPHONE_SERVICE_WORKER" || ingress.current_device_ingress_observed !== true) { fail("current-iPhone ingress required"); }
    if (ingress.claim_or_fence_minted !== false || ingress.workercoordinator_claim_observed !== false || ingress.workercoordinator_fence_observed !== false) { fail("ingress cannot mint WorkerCoordinator authority"); }
    return ingress;
  }

  function validateRuntime(state, ingress, binding) {
    var receipt = state && state.receipt;
    if (!state || state.state !== "RUNTIME_READY_FOR_WORKERCOORDINATOR" || !receipt) { fail("EVENT_EPHEMERAL runtime readiness not observed"); }
    if (state.goal_task_id !== GOAL_ID || state.cosv_task_vector !== COSV_ID || state.runtime_class !== "EVENT_EPHEMERAL") { fail("EVENT_EPHEMERAL runtime identity mismatch"); }
    if (state.node_id !== ingress.node_id || state.interlock_id !== ingress.interlock_id) { fail("Node/Interlock runtime correlation mismatch"); }
    if (receipt.materialization_id !== ingress.materialization_id || receipt.request_hash !== ingress.request_hash) { fail("materialization/request runtime correlation mismatch"); }
    if (receipt.registration_receipt_sha256 !== ingress.registration_receipt_sha256) { fail("registration receipt runtime correlation mismatch"); }
    if (receipt.manifest_sha256 !== binding.manifest_sha256) { fail("manifest runtime correlation mismatch"); }
    if (receipt.claim_or_fence_minted !== false || receipt.github_runtime_authority !== "NONE" || receipt.credential_authority !== "TV/TVC" || receipt.authority_effect !== "NONE_RUNTIME_MATERIALIZATION_ONLY") { fail("EVENT_EPHEMERAL authority boundary invalid"); }
    return state;
  }

  function install() {
    var api = root.StegVerseCanonicalWorkRuntimeConsumption;
    var runtime = root.StegVerseStegBrowserManifestRuntime;
    if (!api || typeof api.start !== "function") { fail("canonical current-iPhone invocation API unavailable"); }
    if (!runtime || typeof runtime.materialize !== "function") { fail("StegBrowser EVENT_EPHEMERAL materializer unavailable"); }
    if (api.__eventEphemeralContinuationInstalled === true) { return; }
    var baseStart = api.start;
    api.start = function () {
      var baseEvidence;
      var ingress;
      var entry;
      var binding;
      return baseStart().then(function (value) {
        baseEvidence = value;
        ingress = validateIngress(value);
        return readOutboxEntry(ingress.materialization_id);
      }).then(function (value) {
        entry = value;
        return loadRuntimeBinding();
      }).then(function (value) {
        binding = value;
        if (binding.manifest_sha256 !== "sha256:" + String(ingress.manifest_sha256 || "").replace(/^sha256:/, "")) { fail("ingress/runtime manifest digest mismatch"); }
        return runtime.materialize({
          entry: entry,
          binding: binding,
          node: {
            node_id: ingress.node_id,
            interlock_id: ingress.interlock_id,
            registration_receipt_sha256: ingress.registration_receipt_sha256
          }
        });
      }).then(function (runtimeState) {
        runtimeState = validateRuntime(runtimeState, ingress, binding);
        return {
          schema: "stegverse.stegbrowser-current-device-a1-a2-2-evidence/v1",
          state: "EVENT_EPHEMERAL_RUNTIME_MATERIALIZED",
          goal_task_id: GOAL_ID,
          parent_goal_task_id: "STEG-BROWSER-CURRENT-IPHONE-A1-A4-EXECUTION-001",
          cosv_task_vector: COSV_ID,
          invocation_request_nonce: NONCE,
          manifest_sha256: ingress.manifest_sha256,
          node_id: ingress.node_id,
          interlock_id: ingress.interlock_id,
          registration_receipt_sha256: ingress.registration_receipt_sha256,
          materialization_id: ingress.materialization_id,
          request_hash: ingress.request_hash,
          ingress_receipt: ingress,
          event_ephemeral_runtime: runtimeState,
          event_ephemeral_runtime_observed: true,
          execution_time_runtime_identity_bound: true,
          workercoordinator_claim_pending: true,
          workercoordinator_fence_pending: true,
          a4_ingress_pending: true,
          a1_a4_complete: false,
          round_trip_1_started: false,
          request_mutated: false,
          second_request_emitted: false,
          github_runtime_authority: "NONE",
          credential_authority: "TV/TVC",
          authority_effect: "NONE_EVIDENCE_ONLY",
          prior_a1_a2_evidence: baseEvidence
        };
      });
    };
    api.__eventEphemeralContinuationInstalled = true;
  }

  install();
}(window));
