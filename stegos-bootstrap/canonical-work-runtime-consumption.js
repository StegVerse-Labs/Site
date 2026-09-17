(function (root) {
  "use strict";

  var GOAL_ID = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001";
  var PARENT_TASK_ID = "STEG-BROWSER-RUNTIME-MATERIALIZATION-REMEDIATION-001";
  var COSV_ID = "40000100100000";
  var NONCE = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z";
  var MANIFEST_SHA256 = "fcde63451bf612df8f3b2b62fa6766670dc880f2fcb66605680a2af6f2096f74";
  var DESTINATION = "StegBrowser:ManifestInvocation";
  var NODE_DB = "stegos-node-v1";
  var NODE_DB_VERSION = 2;
  var NODE_META = "meta";
  var NODE_OUTBOX = "intr_outbox";
  var NODE_KEY = "registration";
  var ROUTE_BINDING_URL = "/data/stegbrowser-manifest-runtime-binding.v1.json";

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }
  function canonicalize(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(canonicalize).join(",") + "]"; }
    return "{" + Object.keys(value).sort().map(function (key) { return JSON.stringify(key) + ":" + canonicalize(value[key]); }).join(",") + "}";
  }
  function openRegisteredNodeDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(NODE_DB, NODE_DB_VERSION);
      request.onupgradeneeded = function () { request.transaction.abort(); };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("registered StegVerse Node database unavailable")); };
    });
  }
  function readRegisteredNode() {
    return openRegisteredNodeDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        if (!db.objectStoreNames.contains(NODE_META) || !db.objectStoreNames.contains(NODE_OUTBOX)) { db.close(); reject(new Error("registered StegVerse Node stores unavailable")); return; }
        var tx = db.transaction(NODE_META, "readonly"), req = tx.objectStore(NODE_META).get(NODE_KEY);
        req.onsuccess = function () { var value = req.result ? req.result.value : null; db.close(); resolve(value); };
        req.onerror = function () { var error = req.error || new Error("registered StegVerse Node read failed"); db.close(); reject(error); };
      });
    }).then(function (registration) {
      if (!registration || registration.state !== "REGISTERED" || !/^SV-NODE-[a-f0-9]{24}$/.test(String(registration.node_id || "")) || !/^SV-IL-[a-f0-9]{24}$/.test(String(registration.interlock_id || "")) || !/^sha256:[0-9a-f]{64}$/.test(String(registration.receipt_sha256 || ""))) { fail("canonical registered StegVerse Node Receipt #1 required"); }
      return registration;
    });
  }
  function putOutboxOnce(entry) {
    return openRegisteredNodeDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(NODE_OUTBOX, "readwrite"), store = tx.objectStore(NODE_OUTBOX), req = store.get(entry.materialization_id);
        req.onsuccess = function () {
          if (req.result && canonicalize(req.result) !== canonicalize(entry)) { tx.abort(); reject(new Error("registered Node outbox write-once collision")); return; }
          if (!req.result) { store.add(entry); }
        };
        req.onerror = function () { reject(req.error || new Error("registered Node outbox read failed")); };
        tx.oncomplete = function () { db.close(); resolve(entry); };
        tx.onerror = function () { var error = tx.error || new Error("registered Node outbox write failed"); db.close(); reject(error); };
      });
    });
  }
  function readOutboxEntry(materializationId) {
    return openRegisteredNodeDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(NODE_OUTBOX, "readonly"), req = tx.objectStore(NODE_OUTBOX).get(materializationId);
        req.onsuccess = function () { var value = req.result || null; db.close(); if (!value) { reject(new Error("same-invocation Node outbox entry unavailable")); return; } resolve(value); };
        req.onerror = function () { var error = req.error || new Error("same-invocation Node outbox read failed"); db.close(); reject(error); };
      });
    });
  }
  function loadRuntimeRouteBinding() {
    return fetch(ROUTE_BINDING_URL, { credentials: "omit", cache: "no-store" }).then(function (response) {
      if (!response.ok) { throw new Error("StegBrowser runtime route binding HTTP " + response.status); }
      return response.json();
    }).then(function (binding) {
      if (!binding || binding.schema !== "stegverse.stegbrowser-universal-intr-invocation-binding/v1" || binding.goal_task_id !== GOAL_ID || binding.cosv_task_vector !== COSV_ID || binding.manifest_task_id !== PARENT_TASK_ID) { fail("StegBrowser runtime route binding mismatch"); }
      if (binding.manifest_sha256 !== "sha256:" + MANIFEST_SHA256 || binding.authority_effect !== "NONE_ROUTE_BINDING_ONLY") { fail("StegBrowser runtime route authority binding mismatch"); }
      return binding;
    });
  }
  function waitForManifestProfile() {
    var deadline = Date.now() + 12000;
    function probe() {
      return fetch("/intr/profile", { credentials: "omit", cache: "no-store" }).then(function (response) {
        if (!response.ok) { throw new Error("root InTr profile HTTP " + response.status); }
        return response.json();
      }).then(function (profile) {
        if (profile && Array.isArray(profile.profiles) && profile.profiles.indexOf(DESTINATION) !== -1 && profile.runtime_surface === "CURRENT_USER_IPHONE_SERVICE_WORKER") { return profile; }
        if (Date.now() >= deadline) { fail("current root InTr worker has not converged to " + DESTINATION); }
        return new Promise(function (resolve) { setTimeout(resolve, 300); }).then(probe);
      }).catch(function (error) {
        if (Date.now() >= deadline) { throw error; }
        return new Promise(function (resolve) { setTimeout(resolve, 300); }).then(probe);
      });
    }
    return probe();
  }
  function rootIntrRegistration() {
    return navigator.serviceWorker.register("/intr-service-worker.js", { scope: "/" }).then(function (registration) {
      return registration.update().catch(function () { return registration; }).then(function () { return waitForManifestProfile(); }).then(function (profile) {
        var active = registration.active || registration.waiting || registration.installing || navigator.serviceWorker.controller;
        if (!active) { fail("root Universal InTr service worker unavailable"); }
        return { registration: registration, active: active, profile: profile };
      });
    });
  }
  function buildTrigger(registration) {
    if (!root.StegVerseStegBrowserInTrSync || typeof root.StegVerseStegBrowserInTrSync.buildCanonicalEntry !== "function") { fail("canonical StegBrowser Universal InTr builder unavailable"); }
    var binding = {
      schema: "stegverse.stegbrowser-universal-intr-invocation-binding/v1",
      state: "BOUND_FOR_UNIVERSAL_INTR_MATERIALIZATION",
      goal_task_id: GOAL_ID,
      parent_task_id: PARENT_TASK_ID,
      cosv_task_vector: COSV_ID,
      invocation_request_nonce: NONCE,
      manifest_ref: "StegVerse-Labs/.github/control/transport-manifests/STEG-BROWSER-RUNTIME-MATERIALIZATION-REMEDIATION-001.json",
      manifest_sha256: MANIFEST_SHA256,
      node_genesis_receipt_ref: "indexeddb://stegos-node-v1/meta/registration",
      node_id: registration.node_id,
      interlock_id: registration.interlock_id,
      registration_receipt_sha256: registration.receipt_sha256,
      stegos_source_root: "StegVerse-Labs/Site#SV002_VALIDATED_BROWSER_BASELINE",
      request_mutated: false,
      resident_request_sweep_required: false,
      control_plane_source_package_required: false,
      credential_authority: "TV/TVC",
      github_runtime_authority: "NONE",
      authority_effect: "NONE_BINDING_ONLY"
    };
    return root.StegVerseStegBrowserInTrSync.buildCanonicalEntry(registration, binding);
  }
  function sendTrigger(active, trigger) {
    return new Promise(function (resolve, reject) {
      var channel = new MessageChannel();
      var timer = setTimeout(function () { reject(new Error("root Universal InTr StegBrowser admission timed out")); }, 8000);
      channel.port1.onmessage = function (event) {
        clearTimeout(timer);
        var data = event.data || {};
        if (!data.ok || !data.receipt) { reject(new Error("root Universal InTr denied StegBrowser manifest invocation: " + String(data.reason || "unknown"))); return; }
        resolve(data.receipt);
      };
      active.postMessage({ type: "STEGVERSE_INTR_LOCAL_TRIGGER", trigger: trigger }, [channel.port2]);
    });
  }
  function validateReceipt(receipt) {
    if (!receipt || receipt.schema !== "stegverse.stegbrowser-intr-materialization-ingress/v1" || receipt.state !== "INGRESS_ADMITTED") { fail("StegBrowser ingress receipt invalid"); }
    if (receipt.goal_task_id !== GOAL_ID || receipt.parent_task_id !== PARENT_TASK_ID || receipt.cosv_task_vector !== COSV_ID || receipt.invocation_request_nonce !== NONCE || receipt.manifest_sha256 !== MANIFEST_SHA256) { fail("StegBrowser ingress invocation correlation mismatch"); }
    if (receipt.runtime_surface !== "CURRENT_USER_IPHONE_SERVICE_WORKER" || receipt.current_device_ingress_observed !== true) { fail("current-iPhone StegBrowser ingress not observed"); }
    if (receipt.claim_or_fence_minted !== false || receipt.workercoordinator_claim_observed !== false || receipt.workercoordinator_fence_observed !== false) { fail("WorkerCoordinator authority fabricated by ingress"); }
    if (receipt.credential_authority !== "TV/TVC" || receipt.github_token_runtime_authority !== "NONE" || receipt.authority_effect !== "NONE_INGRESS_ONLY") { fail("StegBrowser ingress authority boundary invalid"); }
    return receipt;
  }
  function start() {
    if (!navigator.serviceWorker) { return Promise.reject(new Error("service worker unavailable")); }
    var node;
    return readRegisteredNode().then(function (value) { node = value; return rootIntrRegistration(); }).then(function (intr) {
      return buildTrigger(node).then(function (built) {
        return putOutboxOnce(built.entry).then(function () { return sendTrigger(intr.active, built.trigger); });
      });
    }).then(validateReceipt).then(function (admission) {
      return {
        schema: "stegverse.stegbrowser-current-device-a1-a2-evidence/v1",
        state: "INGRESS_ADMITTED",
        goal_task_id: GOAL_ID,
        parent_task_id: PARENT_TASK_ID,
        cosv_task_vector: COSV_ID,
        invocation_request_nonce: NONCE,
        manifest_sha256: MANIFEST_SHA256,
        ingress_receipt: admission,
        workercoordinator_claim_pending: true,
        workercoordinator_fence_pending: true,
        event_ephemeral_runtime_pending: true,
        a4_ingress_pending: true,
        round_trip_1_started: false,
        repository_mutation_claimed: false,
        completion_claimed: false,
        credential_authority: "TV/TVC",
        github_token_runtime_authority: "NONE",
        authority_effect: "NONE_EVIDENCE_ONLY"
      };
    });
  }
  function continueIntoExistingEventRuntime(admissionEvidence) {
    var admission = admissionEvidence && admissionEvidence.ingress_receipt;
    var retainedEntry = null;
    if (!admission || admission.state !== "INGRESS_ADMITTED") { fail("authentic StegBrowser ingress required before event runtime materialization"); }
    if (!root.StegVerseStegBrowserManifestRuntime || typeof root.StegVerseStegBrowserManifestRuntime.materialize !== "function") { fail("existing StegBrowser EVENT_EPHEMERAL materializer unavailable"); }
    return Promise.all([readOutboxEntry(admission.materialization_id), loadRuntimeRouteBinding()]).then(function (values) {
      var entry = values[0], routeBinding = values[1];
      retainedEntry = entry;
      return root.StegVerseStegBrowserManifestRuntime.materialize({
        entry: entry,
        binding: routeBinding,
        node: {
          node_id: admission.node_id,
          interlock_id: admission.interlock_id,
          registration_receipt_sha256: admission.registration_receipt_sha256
        }
      });
    }).then(function (runtimeState) {
      if (!runtimeState || runtimeState.state !== "RUNTIME_READY_FOR_WORKERCOORDINATOR" || runtimeState.runtime_class !== "EVENT_EPHEMERAL") { fail("StegBrowser EVENT_EPHEMERAL runtime readiness invalid"); }
      var evidence = {
        schema: "stegverse.stegbrowser-current-device-a1-a2-event-runtime-evidence/v1",
        state: "RUNTIME_READY_FOR_WORKERCOORDINATOR",
        goal_task_id: GOAL_ID,
        parent_task_id: PARENT_TASK_ID,
        cosv_task_vector: COSV_ID,
        invocation_request_nonce: NONCE,
        manifest_sha256: MANIFEST_SHA256,
        ingress_receipt: admission,
        event_ephemeral_runtime: runtimeState,
        registered_node_bound_to_invocation: true,
        interlock_bound_to_node_and_manifest: true,
        intr_materialization_admitted: true,
        invocation_scoped_lease_established: true,
        event_ephemeral_runtime_materialized: true,
        execution_time_runtime_identity_bound: true,
        workercoordinator_claim_pending: true,
        workercoordinator_fence_pending: true,
        a4_ingress_pending: true,
        round_trip_1_started: false,
        repository_mutation_claimed: false,
        completion_claimed: false,
        credential_authority: "TV/TVC",
        github_token_runtime_authority: "NONE",
        authority_effect: "NONE_EVIDENCE_ONLY"
      };
      if (!root.StegVerseStegBrowserInTrSync || typeof root.StegVerseStegBrowserInTrSync.postEntry !== "function") { return evidence; }
      return root.StegVerseStegBrowserInTrSync.postEntry(retainedEntry).then(function (delivery) {
        evidence.sovereign_ingress_delivery = delivery;
        evidence.sovereign_ingress_retained = delivery && delivery.schema === "stegverse.stegbrowser-intr-materialization-ingress/v1" && delivery.state === "INGRESS_ADMITTED";
        return evidence;
      }).catch(function (error) {
        evidence.sovereign_ingress_delivery = { state: "SOVEREIGN_INGRESS_DELIVERY_FAIL_CLOSED", reason: String(error && error.message ? error.message : error), authority_effect: "NONE" };
        evidence.sovereign_ingress_retained = false;
        return evidence;
      });
    });
  }
  function startThroughExistingEventRuntime() {
    return start().then(continueIntoExistingEventRuntime);
  }

  root.StegVerseCanonicalWorkRuntimeConsumption = { start: startThroughExistingEventRuntime, startIngressOnly: start, taskId: GOAL_ID, cosvId: COSV_ID, nonce: NONCE, destination: DESTINATION };
}(window));
