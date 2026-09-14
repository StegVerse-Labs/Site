(function (root) {
  "use strict";

  var TASK_ID = "STEG-BROWSER-RUNTIME-CONSUMPTION-001";
  var COSV_ID = "40000100100000";
  var REGISTRY_COMMIT = "f1a55fa4022e19b41f2a9f604978b08ece22f64c";
  var REGISTRY_GENERATION = 19;
  var SELECTED_SUBSTRATE = "ADMITTED-EPHEMERAL-STEGOS-NODE";
  var OWNER = "STEGVERSE-CANONICAL-WORK-COORDINATION-001";
  var NODE_DB = "stegos-node-v1";
  var NODE_DB_VERSION = 2;
  var NODE_META = "meta";
  var NODE_OUTBOX = "intr_outbox";
  var NODE_KEY = "registration";

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }
  function canonicalize(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(canonicalize).join(",") + "]"; }
    return "{" + Object.keys(value).sort().map(function (key) { return JSON.stringify(key) + ":" + canonicalize(value[key]); }).join(",") + "}";
  }
  function bytesToHex(bytes) { return Array.prototype.map.call(new Uint8Array(bytes), function (b) { return b.toString(16).padStart(2, "0"); }).join(""); }
  function sha256Uri(value) {
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonicalize(value))).then(function (digest) { return "sha256:" + bytesToHex(digest); });
  }
  function randomHex(length) {
    var bytes = new Uint8Array(length); crypto.getRandomValues(bytes); return bytesToHex(bytes);
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
      if (!registration || registration.state !== "REGISTERED" || !/^SV-NODE-[a-f0-9]{24}$/.test(String(registration.node_id || "")) || !/^SV-IL-[a-f0-9]{24}$/.test(String(registration.interlock_id || ""))) { fail("canonical registered StegVerse Node required"); }
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
  function waitForCanonicalProfile() {
    var deadline = Date.now() + 12000;
    function probe() {
      return fetch("/intr/profile", { credentials: "omit", cache: "no-store" }).then(function (response) {
        if (!response.ok) { throw new Error("root InTr profile HTTP " + response.status); }
        return response.json();
      }).then(function (profile) {
        if (profile && Array.isArray(profile.profiles) && profile.profiles.indexOf("CanonicalWork:Ingress") !== -1 && profile.runtime_surface === "CURRENT_USER_IPHONE_SERVICE_WORKER") { return profile; }
        if (Date.now() >= deadline) { fail("current root InTr worker has not converged to CanonicalWork:Ingress"); }
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
      return registration.update().catch(function () { return registration; }).then(function () { return waitForCanonicalProfile(); }).then(function (profile) {
        var active = registration.active || registration.waiting || registration.installing || navigator.serviceWorker.controller;
        if (!active) { fail("root Universal InTr service worker unavailable"); }
        return { registration: registration, active: active, profile: profile };
      });
    });
  }
  function buildTrigger(registration) {
    var binding = {
      schema: "stegverse.canonical-work-current-task-binding/v1",
      task_id: TASK_ID,
      cosv_id: COSV_ID,
      registry_commit: REGISTRY_COMMIT,
      registry_generation: REGISTRY_GENERATION,
      coordination_state: "ACTIVE",
      checkout_state: "CHECKED_OUT",
      selected_execution_substrate: SELECTED_SUBSTRATE,
      allowed_next_transition: "INGRESS_ADMITTED",
      worker_claim_authority: "WORKERCOORDINATOR",
      worker_claim_projection_only: true,
      worker_claim_ref: null,
      fence_ref: null,
      interlock_intr_required: true,
      task_registry_mints_execution_authority: false,
      external_device_required: false,
      second_user_operated_device_allowed: false
    };
    var materializationId = "CW-STBR-RUNTIME-" + randomHex(12);
    var transportIntent = { operation: "TASK_INGRESS", task_id: TASK_ID, cosv_id: COSV_ID, destination: "CanonicalWork:Ingress", substrate: SELECTED_SUBSTRATE };
    return Promise.all([sha256Uri(binding), sha256Uri(transportIntent)]).then(function (hashes) {
      var request = {
        schema: "stegverse.universal-intr-materialization-request/v1",
        state: "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
        materialization_id: materializationId,
        destination: { boundary: "STEGOS_ECOSYSTEM", subsystem: "CanonicalWork:Ingress" },
        downstream_owner_ref: OWNER,
        transport_intent_hash: hashes[1],
        payload_hash: hashes[0],
        canonical_work: binding,
        request_grants_execution_authority: false,
        transport_grants_execution_authority: false,
        claim_or_fence_minted: false,
        credential_authority: "TV/TVC",
        github_token_runtime_authority: "NONE",
        authority_effect: "NONE_REQUEST_ONLY"
      };
      return sha256Uri(request).then(function (requestHash) {
        request.request_hash = requestHash;
        var entry = {
          schema: "stegos.node_intr_outbox_entry.v1",
          state: "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY",
          materialization_id: materializationId,
          request_hash: requestHash,
          transport_intent_hash: request.transport_intent_hash,
          payload_hash: request.payload_hash,
          node_id: registration.node_id,
          interlock_id: registration.interlock_id,
          materialization_request: request,
          network_delivery_observed: false,
          runtime_materialization_observed: false,
          receiver_receipt_observed: false,
          tvc_receipt_observed: false,
          request_grants_execution_authority: false,
          claim_or_fence_minted: false,
          credential_authority: "TV/TVC",
          github_token_runtime_authority: "NONE",
          authority_effect: "NONE_LOCAL_CONTINUITY_ONLY"
        };
        return sha256Uri(entry).then(function (entryHash) {
          entry.outbox_entry_hash = entryHash;
          var trigger = {
            schema: "stegos.node_intr_materialization_trigger.v1",
            transport_origin: "STEGOS_NODE_OUTBOX",
            node_id: registration.node_id,
            interlock_id: registration.interlock_id,
            outbox_entry_hash: entryHash,
            node_outbox_entry: entry,
            request_grants_execution_authority: false,
            claim_or_fence_minted: false,
            authority_effect: "NONE_TRIGGER_ONLY"
          };
          return sha256Uri(trigger).then(function (triggerHash) { trigger.trigger_sha256 = triggerHash; return { entry: entry, trigger: trigger }; });
        });
      });
    });
  }
  function sendTrigger(active, trigger) {
    return new Promise(function (resolve, reject) {
      var channel = new MessageChannel();
      var timer = setTimeout(function () { reject(new Error("root Universal InTr Canonical Work admission timed out")); }, 8000);
      channel.port1.onmessage = function (event) {
        clearTimeout(timer);
        var data = event.data || {};
        if (!data.ok || !data.receipt) { reject(new Error("root Universal InTr denied Canonical Work: " + String(data.reason || "unknown"))); return; }
        resolve(data.receipt);
      };
      active.postMessage({ type: "STEGVERSE_INTR_LOCAL_TRIGGER", trigger: trigger }, [channel.port2]);
    });
  }
  function validateReceipt(receipt) {
    if (!receipt || receipt.schema !== "stegverse.canonical-work-intr-materialization-ingress/v1" || receipt.state !== "INGRESS_ADMITTED") { fail("canonical work ingress receipt invalid"); }
    if (receipt.task_id !== TASK_ID || receipt.cosv_id !== COSV_ID || receipt.registry_commit !== REGISTRY_COMMIT || receipt.registry_generation !== REGISTRY_GENERATION) { fail("canonical work ingress identity mismatch"); }
    if (receipt.runtime_surface !== "CURRENT_USER_IPHONE_SERVICE_WORKER" || receipt.current_device_ingress_observed !== true) { fail("current-iPhone ingress not observed"); }
    if (receipt.claim_or_fence_minted !== false || receipt.workercoordinator_claim_observed !== false || receipt.workercoordinator_fence_observed !== false) { fail("WorkerCoordinator authority fabricated by ingress"); }
    if (receipt.credential_authority !== "TV/TVC" || receipt.github_token_runtime_authority !== "NONE" || receipt.authority_effect !== "NONE_INGRESS_ONLY") { fail("canonical work ingress authority boundary invalid"); }
    return receipt;
  }
  function executeLocalBuildAnalysis(admission) {
    if (!root.StegOSAdmittedInference || typeof root.StegOSAdmittedInference.executeAdmittedInference !== "function") { return Promise.reject(new Error("StegVerse admitted local inference unavailable")); }
    var prompt = [
      "StegVerse self-build runtime analysis.",
      "Goal Task ID: " + TASK_ID + ".",
      "COSV: " + COSV_ID + ".",
      "Current-iPhone Universal InTr returned authentic INGRESS_ADMITTED for CanonicalWork:Ingress.",
      "WorkerCoordinator claim/fence is still pending and must not be fabricated.",
      "Select the next compliant action that advances StegVerse building StegVerse while preserving TV/TVC, Interlock/InTr, Master Records, and no-second-device invariants."
    ].join("\n");
    return root.StegOSAdmittedInference.executeAdmittedInference(prompt).then(function (result) {
      if (!result || !result.entry || !result.entry.entry_sha256) { fail("local build-analysis receipt missing"); }
      return {
        schema: "stegverse.self-build-start-evidence/v1",
        state: "CANONICAL_WORK_INGRESS_ADMITTED_LOCAL_BUILD_ANALYSIS_EXECUTED",
        task_id: TASK_ID,
        cosv_id: COSV_ID,
        canonical_work_ingress_receipt: admission,
        local_build_analysis: result.response,
        local_build_analysis_receipt_sha256: result.entry.entry_sha256,
        workercoordinator_claim_pending: true,
        workercoordinator_fence_pending: true,
        repository_mutation_claimed: false,
        self_build_completion_claimed: false,
        credential_authority: "TV/TVC",
        github_token_runtime_authority: "NONE",
        authority_effect: "NONE_EVIDENCE_ONLY"
      };
    });
  }
  function start() {
    if (!navigator.serviceWorker) { return Promise.reject(new Error("service worker unavailable")); }
    var node;
    return readRegisteredNode().then(function (value) { node = value; return rootIntrRegistration(); }).then(function (intr) {
      return buildTrigger(node).then(function (built) {
        return putOutboxOnce(built.entry).then(function () { return sendTrigger(intr.active, built.trigger); });
      });
    }).then(validateReceipt).then(function (admission) {
      return executeLocalBuildAnalysis(admission).catch(function (error) {
        return {
          schema: "stegverse.self-build-start-evidence/v1",
          state: "CANONICAL_WORK_INGRESS_ADMITTED_LOCAL_BUILD_ANALYSIS_PENDING",
          task_id: TASK_ID,
          cosv_id: COSV_ID,
          canonical_work_ingress_receipt: admission,
          local_build_analysis_error: String(error && error.message ? error.message : error),
          workercoordinator_claim_pending: true,
          workercoordinator_fence_pending: true,
          repository_mutation_claimed: false,
          self_build_completion_claimed: false,
          credential_authority: "TV/TVC",
          github_token_runtime_authority: "NONE",
          authority_effect: "NONE_EVIDENCE_ONLY"
        };
      });
    });
  }

  root.StegVerseCanonicalWorkRuntimeConsumption = { start: start, taskId: TASK_ID, cosvId: COSV_ID };
}(window));
