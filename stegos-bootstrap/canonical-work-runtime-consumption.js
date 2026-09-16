(function (root) {
  "use strict";

  var GOAL_ID = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001";
  var PARENT_TASK_ID = "STEG-BROWSER-RUNTIME-MATERIALIZATION-REMEDIATION-001";
  var COSV_ID = "40000100100000";
  var NONCE = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z";
  var MANIFEST_SHA256 = "fcde63451bf612df8f3b2b62fa6766670dc880f2fcb66605680a2af6f2096f74";
  var DESTINATION = "StegBrowser:ManifestInvocation";
  var DOWNSTREAM_OWNER = "StegVerse-Labs/.github#1952";
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
  function sha256HexText(value) {
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(String(value))).then(function (digest) { return bytesToHex(digest); });
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
    var transportIntent = {
      operation_id: "STEGBROWSER:" + GOAL_ID + ":" + NONCE,
      payload_hash: null,
      source: { boundary: "DEVICE_SYSTEM", subsystem: "StegBrowser:ManifestRequest" },
      destination: { boundary: "STEGOS_ECOSYSTEM", subsystem: DESTINATION }
    };
    return Promise.all([sha256Uri(binding), sha256HexText(NONCE)]).then(function (values) {
      var bindingHash = values[0], nonceHash = values[1];
      var materializationId = "STBR-MAT-" + nonceHash.slice(0, 24);
      transportIntent.payload_hash = bindingHash;
      return sha256Uri(transportIntent).then(function (intentHash) {
        var request = {
          schema: "stegverse.universal-intr-materialization-request/v1",
          state: "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
          materialization_id: materializationId,
          destination: { boundary: "STEGOS_ECOSYSTEM", subsystem: DESTINATION },
          downstream_owner_ref: DOWNSTREAM_OWNER,
          transport_intent_hash: intentHash,
          payload_hash: bindingHash,
          payload_ref: "opaque://stegbrowser-manifest-invocation/" + bindingHash.replace(/^sha256:/, ""),
          request_grants_execution_authority: false,
          transport_grants_execution_authority: false,
          claim_or_fence_minted: false,
          credential_authority: "TV/TVC",
          github_token_runtime_authority: "NONE",
          authority_effect: "NONE_REQUEST_ONLY"
        };
        return sha256Uri(request).then(function (requestHash) {
          request.request_hash = requestHash;
          var entryBody = {
            schema: "stegos.node_intr_outbox_entry.v1",
            state: "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY",
            materialization_id: materializationId,
            request_hash: requestHash,
            transport_intent_hash: intentHash,
            payload_hash: bindingHash,
            binding_hash: bindingHash,
            node_id: registration.node_id,
            interlock_id: registration.interlock_id,
            destination: request.destination,
            downstream_owner_ref: DOWNSTREAM_OWNER,
            stegbrowser_invocation: binding,
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
          return sha256Uri(entryBody).then(function (entryHash) {
            var entry = Object.assign({}, entryBody, { outbox_entry_hash: entryHash });
            var triggerBody = {
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
            return sha256Uri(triggerBody).then(function (triggerHash) { return { entry: entry, trigger: Object.assign({}, triggerBody, { trigger_sha256: triggerHash }) }; });
          });
        });
      });
    });
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

  root.StegVerseCanonicalWorkRuntimeConsumption = { start: start, taskId: GOAL_ID, cosvId: COSV_ID, nonce: NONCE, destination: DESTINATION };
}(window));
