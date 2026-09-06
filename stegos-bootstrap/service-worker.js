"use strict";

importScripts("./stegverse-reference-model.js", "./tvc-sovereign-local-model-route.js", "./external-resident-task.js", "./workercoordinator-portable-checkout.js", "./tvc-sv001-portable-lease.js", "./workercoordinator-portable-adapter.js", "./master-records-sv001-custody.js");

var CACHE_NAME = "stegos-web-bootstrap-v12";
var SHELL = [
  "./",
  "./index.html",
  "./persistent-card-ux.js",
  "./help/admitted-inference.html",
  "./help/authority-boundary.html",
  "./help/canonical-inference-evidence.html",
  "./help/continuity.html",
  "./help/ecosystem-chat.html",
  "./help/interaction-coordinator.html",
  "./help/master-records-sv001.html",
  "./help/node.html",
  "./help/offline-shell.html",
  "./help/runtime-capability.html",
  "./help/sv001-bounded-autonomy.html",
  "./stegos-bootstrap.js",
  "./admitted-inference.js",
  "./device-local-autostart.js",
  "./external-resident-task.js",
  "./workercoordinator-portable-checkout.js",
  "./workercoordinator-portable-adapter.js",
  "./master-records-sv001-custody.js",
  "./master-records-sv001-custody-package.json",
  "./workercoordinator-portable-sv001.json",
  "./workercoordinator-portable-authority-contract.json",
  "./tvc-sv001-portable-lease.js",
  "./tvc-sv001-portable-lease-package.json",
  "./tvc-sv001-portable-tv-request.json",
  "./tvc-sv001-portable-lease-policy.json",
  "./tvc-sv001-portable-lease-state.schema.json",
  "./stegverse-reference-model.js",
  "./tvc-sovereign-local-model-route.js",
  "./manifest.webmanifest"
];
var LOCAL_PATH = "/stegos-bootstrap/local-model";
var LOCAL_ENDPOINT = "https://stegverse.org" + LOCAL_PATH;
var DB_NAME = "stegos-web-bootstrap-v1";
var DB_VERSION = 1;
var META_STORE = "meta";
var RECEIPT_STORE = "receipts";
var GENERATION_KEY = "device-task-control-generation";
var TASK_KEY_PREFIX = "device-task-control:";
var TASK_SCOPE = "DEVICE_LOCAL_INFERENCE_ONLY";
var RESIDENT_TASK_PATH = "/stegos-bootstrap/resident-task";
var EXTERNAL_TASK_KEY_PREFIX = "external-resident-task:";
var PORTABLE_WC_PATH = "/stegos-bootstrap/portable-workercoordinator/sv001";
var MASTER_RECORDS_SV001_PATH = "/stegos-bootstrap/master-records/sv001";
var PORTABLE_WC_STATE_KEY = "workercoordinator-portable-authority:state";
var PORTABLE_WC_PACKAGE_URL = new URL("./workercoordinator-portable-sv001.json", self.location.href).toString();
var PORTABLE_TVC_STATE_KEY = "tvc-sv001-portable-lease-authority:state";
var PORTABLE_TVC_PACKAGE_URL = new URL("./tvc-sv001-portable-lease-package.json", self.location.href).toString();
var MR_SV001_INTR_SCHEMA = "stegverse.master-records.sv001-custody-intr-admission/v1";
var MR_SV001_TRANSITION = "SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION";
var MR_SV001_TASK = "MR-STEGVERSE001-BOUNDED-AUTONOMY-001";
var MR_SV001_CANONICAL_SOURCE_SHA = "sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35";

function jsonResponse(status, payload) {
  return new Response(JSON.stringify(payload), {
    status: status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
      "X-StegVerse-Execution": "SERVICE_WORKER_LOCAL_INTERCEPT",
      "X-StegVerse-Task-Control": "DEVICE_LOCAL_FENCED"
    }
  });
}

function bytesToHex(bytes) {
  var out = "";
  for (var i = 0; i < bytes.length; i += 1) { out += bytes[i].toString(16).padStart(2, "0"); }
  return out;
}
function randomHex(length) {
  var bytes = new Uint8Array(length);
  crypto.getRandomValues(bytes);
  return bytesToHex(bytes);
}
function canonicalize(value) {
  if (value === null || typeof value !== "object") { return JSON.stringify(value); }
  if (Array.isArray(value)) { return "[" + value.map(canonicalize).join(",") + "]"; }
  return "{" + Object.keys(value).sort().map(function (key) { return JSON.stringify(key) + ":" + canonicalize(value[key]); }).join(",") + "}";
}
function sha256Hex(value) {
  var text = typeof value === "string" ? value : canonicalize(value);
  return crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(function (digest) { return bytesToHex(new Uint8Array(digest)); });
}
function sha256Uri(value) { return sha256Hex(value).then(function (hash) { return "sha256:" + hash; }); }
function openDb() {
  return new Promise(function (resolve, reject) {
    var request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = function () {
      var db = request.result;
      if (!db.objectStoreNames.contains(META_STORE)) { db.createObjectStore(META_STORE, { keyPath: "key" }); }
      if (!db.objectStoreNames.contains(RECEIPT_STORE)) { db.createObjectStore(RECEIPT_STORE, { keyPath: "sequence" }); }
    };
    request.onsuccess = function () { resolve(request.result); };
    request.onerror = function () { reject(request.error || new Error("task-control IndexedDB open failed")); };
    request.onblocked = function () { reject(new Error("task-control IndexedDB open blocked")); };
  });
}
function transactionPromise(transaction) {
  return new Promise(function (resolve, reject) {
    transaction.oncomplete = function () { resolve(); };
    transaction.onerror = function () { reject(transaction.error || new Error("task-control transaction failed")); };
    transaction.onabort = function () { reject(transaction.error || new Error("task-control transaction aborted")); };
  });
}
function getReceipts(db) {
  return new Promise(function (resolve, reject) {
    var tx = db.transaction(RECEIPT_STORE, "readonly");
    var req = tx.objectStore(RECEIPT_STORE).getAll();
    req.onsuccess = function () { var rows = req.result || []; rows.sort(function (a, b) { return a.sequence - b.sequence; }); resolve(rows); };
    req.onerror = function () { reject(req.error || new Error("task-control journal read failed")); };
  });
}
function appendReceipt(body) {
  return openDb().then(function (db) {
    return getReceipts(db).then(function (existing) {
      var envelope = { schema: "stegos.web_bootstrap_journal_entry.v1", sequence: existing.length + 1, previous_entry_sha256: existing.length ? existing[existing.length - 1].entry_sha256 : null, receipt: body };
      return sha256Hex(body).then(function (receiptHash) { envelope.receipt_sha256 = receiptHash; return sha256Hex(envelope); }).then(function (entryHash) {
        envelope.entry_sha256 = entryHash;
        var tx = db.transaction(RECEIPT_STORE, "readwrite");
        tx.objectStore(RECEIPT_STORE).add(envelope);
        return transactionPromise(tx).then(function () { db.close(); return envelope; });
      });
    }).catch(function (error) { db.close(); throw error; });
  });
}
function replayJournal() {
  return openDb().then(function (db) {
    return getReceipts(db).then(function (entries) {
      var previous = null;
      var chain = Promise.resolve();
      entries.forEach(function (entry) {
        chain = chain.then(function () {
          if (entry.previous_entry_sha256 !== previous) { throw new Error("task-control journal previous hash mismatch"); }
          return sha256Hex(entry.receipt).then(function (receiptHash) {
            if (receiptHash !== entry.receipt_sha256) { throw new Error("task-control journal receipt hash mismatch"); }
            var copy = {};
            Object.keys(entry).forEach(function (key) { if (key !== "entry_sha256") { copy[key] = entry[key]; } });
            return sha256Hex(copy);
          }).then(function (entryHash) {
            if (entryHash !== entry.entry_sha256) { throw new Error("task-control journal entry hash mismatch"); }
            previous = entry.entry_sha256;
          });
        });
      });
      return chain.then(function () { db.close(); return { state: "PASS", entries: entries.length, tail_sha256: previous }; });
    }).catch(function (error) { db.close(); throw error; });
  });
}
function claimDeviceTask(body) {
  var nodeId = body && body.stegverse && body.stegverse.node_id;
  if (!nodeId) { return Promise.reject(new Error("FAIL_CLOSED: task-control requires established StegVerse node identity")); }
  return sha256Hex(body).then(function (requestHash) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(META_STORE, "readwrite");
        var store = tx.objectStore(META_STORE);
        var req = store.get(GENERATION_KEY);
        var claim = null;
        req.onerror = function () { reject(req.error || new Error("task-control generation read failed")); };
        req.onsuccess = function () {
          var current = req.result && Number.isInteger(req.result.value) ? req.result.value : 0;
          var generation = current + 1;
          var taskId = "STEGOS-LOCAL-INFERENCE-" + randomHex(12);
          claim = {
            schema: "stegos.device_task_claim.v1", task_id: taskId, task_scope: TASK_SCOPE, state: "ACTIVE",
            claim_id: "STEGOS-" + taskId + "-G" + generation, fencing_token: generation, generation: generation,
            node_id: nodeId, request_sha256: requestHash, executor: "StegOS/service-worker",
            execution_authority_scope: TASK_SCOPE, global_workercoordinator_authority: false, carrier_granted_authority: false,
            credential_authority: "TV/TVC", github_token_required: false, external_non_stegverse_machine_required: false,
            claimed_at: new Date().toISOString()
          };
          store.put({ key: GENERATION_KEY, value: generation });
          store.put({ key: TASK_KEY_PREFIX + taskId, value: claim });
        };
        tx.oncomplete = function () { db.close(); resolve(claim); };
        tx.onerror = function () { var error = tx.error || new Error("task-control atomic checkout failed"); db.close(); reject(error); };
        tx.onabort = function () { var error = tx.error || new Error("task-control atomic checkout aborted"); db.close(); reject(error); };
      });
    });
  });
}
function updateTask(claim, state, extra) {
  return openDb().then(function (db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readwrite");
      var store = tx.objectStore(META_STORE);
      var req = store.get(TASK_KEY_PREFIX + claim.task_id);
      var updated = null;
      req.onerror = function () { reject(req.error || new Error("task-control task read failed")); };
      req.onsuccess = function () {
        var current = req.result && req.result.value;
        if (!current || current.claim_id !== claim.claim_id || current.fencing_token !== claim.fencing_token) {
          tx.abort();
          reject(new Error("FAIL_CLOSED: stale or mismatched task fence"));
          return;
        }
        updated = Object.assign({}, current, extra || {}, { state: state, updated_at: new Date().toISOString() });
        store.put({ key: TASK_KEY_PREFIX + claim.task_id, value: updated });
      };
      tx.oncomplete = function () { db.close(); resolve(updated); };
      tx.onerror = function () { var error = tx.error || new Error("task-control task update failed"); db.close(); reject(error); };
      tx.onabort = function () { db.close(); };
    });
  });
}
function executeDeviceTask(body) {
  var claim;
  var claimEntry;
  var rawResult;
  return claimDeviceTask(body).then(function (value) {
    claim = value;
    return appendReceipt({
      schema: "stegos.web_task_claim_receipt.v1", task_id: claim.task_id, task_scope: claim.task_scope,
      claim_id: claim.claim_id, fencing_token: claim.fencing_token, generation: claim.generation, node_id: claim.node_id,
      request_sha256: claim.request_sha256, executor: claim.executor, global_workercoordinator_authority: false,
      carrier_granted_authority: false, credential_authority: "TV/TVC", github_token_required: false,
      external_non_stegverse_machine_required: false, authority_effect: "DEVICE_LOCAL_TASK_EXECUTION_ONLY",
      created_at: new Date().toISOString()
    });
  }).then(function (entry) {
    claimEntry = entry;
    return self.StegVerseReferenceBrowserModel.chatCompletion(body);
  }).then(function (result) {
    rawResult = result;
    rawResult.model_id = rawResult.model;
    return sha256Hex(rawResult);
  }).then(function (resultHash) {
    return appendReceipt({
      schema: "stegos.web_task_terminal_receipt.v1", task_id: claim.task_id, task_scope: claim.task_scope,
      claim_id: claim.claim_id, fencing_token: claim.fencing_token, state: "COMPLETED",
      request_sha256: claim.request_sha256, model_result_sha256: resultHash, claim_entry_sha256: claimEntry.entry_sha256,
      credential_authority: "TV/TVC", model_output_authority: "NONE", authority_effect: "DEVICE_LOCAL_TASK_EXECUTION_ONLY",
      completed_at: new Date().toISOString()
    });
  }).then(function (terminalEntry) {
    return updateTask(claim, "COMPLETED", { terminal_entry_sha256: terminalEntry.entry_sha256, completed_at: new Date().toISOString() }).then(function () {
      return replayJournal().then(function (report) {
        if (report.state !== "PASS") { throw new Error("FAIL_CLOSED: task journal replay did not pass"); }
        return appendReceipt({
          schema: "stegos.web_task_reconstruction_receipt.v1", task_id: claim.task_id, claim_id: claim.claim_id,
          fencing_token: claim.fencing_token, state: "PASS", terminal_entry_sha256: terminalEntry.entry_sha256,
          replayed_entries: report.entries, replay_tail_sha256: report.tail_sha256, same_execution: true,
          authority_effect: "NONE", reconstructed_at: new Date().toISOString()
        }).then(function (reconstructionEntry) {
          return replayJournal().then(function (finalReport) {
            if (finalReport.state !== "PASS") { throw new Error("FAIL_CLOSED: post-reconstruction journal replay did not pass"); }
            return updateTask(claim, "COMPLETED", {
              reconstruction_state: "PASS", reconstruction_entry_sha256: reconstructionEntry.entry_sha256,
              final_replay_tail_sha256: finalReport.tail_sha256
            }).then(function () {
              rawResult.stegverse_task_control = {
                schema: "stegos.device_task_execution_proof.v1", task_id: claim.task_id, task_scope: claim.task_scope,
                claim_id: claim.claim_id, fencing_token: claim.fencing_token, generation: claim.generation, state: "COMPLETED",
                claim_entry_sha256: claimEntry.entry_sha256, terminal_entry_sha256: terminalEntry.entry_sha256,
                reconstruction_entry_sha256: reconstructionEntry.entry_sha256, reconstruction_state: "PASS",
                final_replay_tail_sha256: finalReport.tail_sha256, same_execution: true,
                global_workercoordinator_authority: false, carrier_granted_authority: false,
                credential_authority: "TV/TVC", external_non_stegverse_machine_required: false,
                authority_effect: "DEVICE_LOCAL_TASK_EXECUTION_ONLY"
              };
              return rawResult;
            });
          });
        });
      });
    });
  }).catch(function (error) {
    if (!claim) { throw error; }
    return updateTask(claim, "FAIL_CLOSED", { failure: String(error && error.message ? error.message : error), failed_at: new Date().toISOString() }).then(function () {
      return appendReceipt({ schema: "stegos.web_task_failure_receipt.v1", task_id: claim.task_id, claim_id: claim.claim_id,
        fencing_token: claim.fencing_token, state: "FAIL_CLOSED", reason: String(error && error.message ? error.message : error),
        authority_effect: "NONE", failed_at: new Date().toISOString() });
    }).then(function () { throw error; });
  });
}

function reserveExternalTask(binding) {
  return openDb().then(function (db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readwrite");
      var store = tx.objectStore(META_STORE);
      var key = EXTERNAL_TASK_KEY_PREFIX + binding.task_id + ":" + binding.claim_id;
      var req = store.get(key);
      req.onerror = function () { reject(req.error || new Error("external resident task binding read failed")); };
      req.onsuccess = function () {
        if (req.result) {
          tx.abort();
          reject(new Error("FAIL_CLOSED: external resident claim already consumed or reserved"));
          return;
        }
        store.put({ key: key, value: Object.assign({}, binding, { state: "ACTIVE", reserved_at: new Date().toISOString() }) });
      };
      tx.oncomplete = function () { db.close(); resolve(binding); };
      tx.onerror = function () { var error = tx.error || new Error("external resident task reserve failed"); db.close(); reject(error); };
      tx.onabort = function () { db.close(); };
    });
  });
}
function updateExternalTask(binding, state, extra) {
  return openDb().then(function (db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readwrite");
      var store = tx.objectStore(META_STORE);
      var key = EXTERNAL_TASK_KEY_PREFIX + binding.task_id + ":" + binding.claim_id;
      var req = store.get(key);
      var updated = null;
      req.onerror = function () { reject(req.error || new Error("external resident task state read failed")); };
      req.onsuccess = function () {
        var current = req.result && req.result.value;
        if (!current || current.claim_id !== binding.claim_id || current.fencing_token !== binding.fencing_token) {
          tx.abort();
          reject(new Error("FAIL_CLOSED: external resident task claim/fence mismatch"));
          return;
        }
        updated = Object.assign({}, current, extra || {}, { state: state, updated_at: new Date().toISOString() });
        store.put({ key: key, value: updated });
      };
      tx.oncomplete = function () { db.close(); resolve(updated); };
      tx.onerror = function () { var error = tx.error || new Error("external resident task state update failed"); db.close(); reject(error); };
      tx.onabort = function () { db.close(); };
    });
  });
}
function completeExternalTask(binding) { return updateExternalTask(binding, "COMPLETED", binding); }
function failExternalTask(binding) {
  return updateExternalTask(binding, "FAIL_CLOSED", { failure: binding.reason || "unknown", failed_at: new Date().toISOString() })
    .catch(function () { return null; });
}
function handleExternalResidentTask(request) {
  if (!self.StegOSExternalResidentTask || typeof self.StegOSExternalResidentTask.execute !== "function") {
    return Promise.resolve(jsonResponse(503, { state: "FAIL_CLOSED", reason: "external resident task adapter unavailable", authority_effect: "NONE" }));
  }
  return request.json().then(function (body) {
    return self.StegOSExternalResidentTask.execute(body, {
      sha256Hex: sha256Hex,
      appendReceipt: appendReceipt,
      replayJournal: replayJournal,
      reserveExternalTask: reserveExternalTask,
      completeExternalTask: completeExternalTask,
      failExternalTask: failExternalTask
    });
  }).then(function (result) {
    return jsonResponse(200, result);
  }).catch(function (error) {
    return jsonResponse(400, { state: "FAIL_CLOSED", reason: String(error && error.message ? error.message : error), authority_effect: "NONE" });
  });
}

function readPortableWorkerCoordinatorState() {
  return openDb().then(function (db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readonly");
      var req = tx.objectStore(META_STORE).get(PORTABLE_WC_STATE_KEY);
      req.onsuccess = function () { var value = req.result ? req.result.value : null; db.close(); resolve(value); };
      req.onerror = function () { var error = req.error || new Error("portable WorkerCoordinator state read failed"); db.close(); reject(error); };
    });
  });
}
function atomicCompareAndSwapPortableWorkerCoordinatorState(expected, nextState) {
  return openDb().then(function (db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readwrite");
      var store = tx.objectStore(META_STORE);
      var req = store.get(PORTABLE_WC_STATE_KEY);
      var matched = false;
      req.onerror = function () { reject(req.error || new Error("portable WorkerCoordinator state CAS read failed")); };
      req.onsuccess = function () {
        var current = req.result ? req.result.value : null;
        if (current === null) {
          matched = !!expected
            && expected.schema === "stegverse.workercoordinator-portable-state/v1"
            && expected.portable_authority_epoch === "WC-PORTABLE-IPHONE-20260902"
            && expected.canonical_authority_owner === "StegVerse-Labs/.github WorkerCoordinator"
            && expected.predecessor_registry_git_blob_sha === "d860e4c09aaeffaf896a3a95b440334984547dce"
            && expected.generation === 22
            && expected.parallel_workercoordinator_claim_issuance_allowed === false;
        } else {
          matched = canonicalize(current) === canonicalize(expected);
        }
        if (!matched) { return; }
        store.put({ key: PORTABLE_WC_STATE_KEY, value: nextState });
      };
      tx.oncomplete = function () { db.close(); resolve(matched); };
      tx.onerror = function () { var error = tx.error || new Error("portable WorkerCoordinator state CAS failed"); db.close(); reject(error); };
      tx.onabort = function () { var error = tx.error || new Error("portable WorkerCoordinator state CAS aborted"); db.close(); reject(error); };
    });
  });
}
function portableWorkerCoordinatorStateStore() {
  return {
    read: readPortableWorkerCoordinatorState,
    atomicCompareAndSwap: atomicCompareAndSwapPortableWorkerCoordinatorState
  };
}
function loadPortableWorkerCoordinatorPackage() {
  return caches.match(PORTABLE_WC_PACKAGE_URL).then(function (response) {
    if (!response) { throw new Error("FAIL_CLOSED: canonical portable WorkerCoordinator package not installed in service-worker cache"); }
    return response.json();
  });
}

function readPortableTvcLeaseState() {
  return openDb().then(function (db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readonly");
      var req = tx.objectStore(META_STORE).get(PORTABLE_TVC_STATE_KEY);
      req.onsuccess = function () { var value = req.result ? req.result.value : null; db.close(); resolve(value); };
      req.onerror = function () { var error = req.error || new Error("portable TVC lease state read failed"); db.close(); reject(error); };
    });
  });
}
function atomicCompareAndSwapPortableTvcLeaseState(expected, nextState) {
  return openDb().then(function (db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readwrite");
      var store = tx.objectStore(META_STORE);
      var req = store.get(PORTABLE_TVC_STATE_KEY);
      var matched = false;
      req.onerror = function () { reject(req.error || new Error("portable TVC lease state CAS read failed")); };
      req.onsuccess = function () {
        var current = req.result ? req.result.value : null;
        if (current === null) {
          if (!self.StegVerseTVCPortableSv001Lease || typeof self.StegVerseTVCPortableSv001Lease.initialState !== "function") {
            return;
          }
          matched = canonicalize(expected) === canonicalize(self.StegVerseTVCPortableSv001Lease.initialState());
        } else {
          matched = canonicalize(current) === canonicalize(expected);
        }
        if (!matched) { return; }
        store.put({ key: PORTABLE_TVC_STATE_KEY, value: nextState });
      };
      tx.oncomplete = function () { db.close(); resolve(matched); };
      tx.onerror = function () { var error = tx.error || new Error("portable TVC lease state CAS failed"); db.close(); reject(error); };
      tx.onabort = function () { var error = tx.error || new Error("portable TVC lease state CAS aborted"); db.close(); reject(error); };
    });
  });
}
function portableTvcLeaseStateStore() {
  return {
    read: readPortableTvcLeaseState,
    atomicCompareAndSwap: atomicCompareAndSwapPortableTvcLeaseState
  };
}
function loadPortableTvcLeasePackage() {
  return caches.match(PORTABLE_TVC_PACKAGE_URL).then(function (response) {
    if (!response) { throw new Error("FAIL_CLOSED: exact portable TVC lease package not installed in service-worker cache"); }
    return response.json();
  });
}
function issuePortableTvcLease(workerCoordinatorReceipt) {
  if (!self.StegVerseTVCPortableSv001Lease || typeof self.StegVerseTVCPortableSv001Lease.issue !== "function") {
    return Promise.reject(new Error("FAIL_CLOSED: exact TVC portable lease issuer unavailable"));
  }
  return loadPortableTvcLeasePackage().then(function (pkg) {
    return self.StegVerseTVCPortableSv001Lease.issue(pkg, workerCoordinatorReceipt, portableTvcLeaseStateStore(), {});
  });
}
function consumePortableTvcLease(leaseId, executionReceiptHash) {
  if (!self.StegVerseTVCPortableSv001Lease || typeof self.StegVerseTVCPortableSv001Lease.markConsumed !== "function") {
    return Promise.reject(new Error("FAIL_CLOSED: exact TVC portable lease consumer unavailable"));
  }
  return self.StegVerseTVCPortableSv001Lease.markConsumed(leaseId, executionReceiptHash, portableTvcLeaseStateStore());
}

function handlePortableWorkerCoordinatorSv001(request) {
  if (!self.StegOSPortableWorkerCoordinatorAdapter || typeof self.StegOSPortableWorkerCoordinatorAdapter.executeSv001 !== "function") {
    return Promise.resolve(jsonResponse(503, { state: "FAIL_CLOSED", reason: "portable WorkerCoordinator adapter unavailable", authority_effect: "NONE" }));
  }
  return request.json().then(function (body) {
    return self.StegOSPortableWorkerCoordinatorAdapter.executeSv001(body, {
      loadPackage: loadPortableWorkerCoordinatorPackage,
      portableStateStore: portableWorkerCoordinatorStateStore,
      appendReceipt: appendReceipt,
      issueTvcLease: issuePortableTvcLease,
      consumeTvcLease: consumePortableTvcLease,
      executeExternalResidentTask: function (envelope) {
        if (!self.StegOSExternalResidentTask || typeof self.StegOSExternalResidentTask.execute !== "function") {
          throw new Error("FAIL_CLOSED: subordinate external resident task adapter unavailable");
        }
        return self.StegOSExternalResidentTask.execute(envelope, {
          sha256Hex: sha256Hex,
          appendReceipt: appendReceipt,
          replayJournal: replayJournal,
          reserveExternalTask: reserveExternalTask,
          completeExternalTask: completeExternalTask,
          failExternalTask: failExternalTask
        });
      }
    });
  }).then(function (proof) {
    return jsonResponse(200, proof);
  }).catch(function (error) {
    return jsonResponse(400, { state: "FAIL_CLOSED", reason: String(error && error.message ? error.message : error), authority_effect: "NONE" });
  });
}

function findMasterRecordsSv001Custody(sourceHash) {
  return openDb().then(function (db) {
    return getReceipts(db).then(function (entries) {
      db.close();
      var admissionEntry = null;
      var custodyEntry = null;
      var reconstructionEntry = null;
      entries.forEach(function (entry) {
        var receipt = entry && entry.receipt;
        if (!receipt || receipt.source_receipt_sha256 !== sourceHash) { return; }
        if (receipt.schema === MR_SV001_INTR_SCHEMA && receipt.state === "INGRESS_ADMITTED") { admissionEntry = entry; }
        if (receipt.schema === "stegverse.master-records.stegverse001-bounded-autonomy-custody/v1") { custodyEntry = entry; }
        if (receipt.schema === "stegverse.master-records.stegverse001-bounded-autonomy-reconstruction/v1") { reconstructionEntry = entry; }
      });
      return { admission_entry: admissionEntry, custody_entry: custodyEntry, reconstruction_entry: reconstructionEntry };
    }).catch(function (error) { db.close(); throw error; });
  });
}

function validateMasterRecordsSv001IntrAdmission(receipt, sourceHash) {
  if (!receipt || receipt.schema !== MR_SV001_INTR_SCHEMA || receipt.state !== "INGRESS_ADMITTED" || receipt.governance_decision !== "ALLOW") {
    return Promise.reject(new Error("FAIL_CLOSED: contemporaneous InTr admission required before Master Records custody"));
  }
  if (receipt.transition_id !== MR_SV001_TRANSITION || receipt.canonical_task !== MR_SV001_TASK || receipt.authority_class !== "MACHINE_GOVERNED") {
    return Promise.reject(new Error("FAIL_CLOSED: Master Records custody InTr transition binding invalid"));
  }
  if (receipt.source_receipt_sha256 !== sourceHash || sourceHash !== MR_SV001_CANONICAL_SOURCE_SHA) {
    return Promise.reject(new Error("FAIL_CLOSED: Master Records custody InTr source binding invalid"));
  }
  if (receipt.current_governance_decision_observed !== true || receipt.human_approval_checkpoint_inserted !== false || receipt.prior_receipt_authorizes_transition !== false) {
    return Promise.reject(new Error("FAIL_CLOSED: Master Records custody governance semantics invalid"));
  }
  if (!/^SV-NODE-[a-f0-9]{24}$/.test(String(receipt.node_id || "")) || !/^SV-IL-[a-f0-9]{24}$/.test(String(receipt.interlock_id || ""))) {
    return Promise.reject(new Error("FAIL_CLOSED: Master Records custody registered Node/Interlock binding invalid"));
  }
  if (receipt.carrier_binding_present !== true || receipt.carrier_binding_validated !== true || receipt.carrier_binding_grants_authority !== false || !receipt.heartbeat_reference_id) {
    return Promise.reject(new Error("FAIL_CLOSED: Master Records custody HB-derived carrier binding invalid"));
  }
  if (receipt.site_custody_authority !== false || receipt.site_execution_authority !== false || receipt.credential_authority !== "TV/TVC" || receipt.authority_effect !== "NONE_INGRESS_ONLY") {
    return Promise.reject(new Error("FAIL_CLOSED: Master Records custody authority boundary invalid"));
  }
  var body = Object.assign({}, receipt);
  var claimed = body.receipt_sha256;
  delete body.receipt_sha256;
  return sha256Uri(body).then(function (actual) {
    if (actual !== claimed) { throw new Error("FAIL_CLOSED: Master Records custody InTr admission receipt hash mismatch"); }
    return receipt;
  });
}

function masterRecordsSv001Proof(result, admissionEntry, custodyEntry, reconstructionEntry, replay, alreadyCustodied) {
  return {
    schema: "stegos.master-records.portable-sv001-custody-proof/v1",
    state: "PASS",
    already_custodied: alreadyCustodied === true,
    execution_surface: "CURRENT_USER_IPHONE",
    source_receipt_sha256: result.source_receipt_sha256,
    intr_governance_admission_observed: !!admissionEntry,
    intr_admission_receipt_sha256: admissionEntry ? admissionEntry.receipt.receipt_sha256 : null,
    intr_admission_journal_entry_sha256: admissionEntry ? admissionEntry.entry_sha256 : null,
    custody_hash: result.custody.custody_hash,
    reconstruction_hash: result.reconstruction.reconstruction_hash,
    reconstruction_state: result.reconstruction.state,
    custody_journal_entry_sha256: custodyEntry.entry_sha256,
    reconstruction_journal_entry_sha256: reconstructionEntry.entry_sha256,
    final_replay_tail_sha256: replay.tail_sha256,
    canonical_owner: "master-records/orchestration",
    site_custody_authority: false,
    site_execution_authority: false,
    credential_authority: "TV/TVC",
    github_token_runtime_authority: "NONE",
    heartbeat_granted_authority: false,
    human_approval_checkpoint_inserted: false,
    prior_receipt_authorizes_transition: false,
    external_non_stegverse_machine_required: false,
    authority_effect: "SITE_MATERIALIZATION_AND_LOCAL_PERSISTENCE_CARRIER_ONLY"
  };
}

function handleMasterRecordsSv001Custody(request) {
  if (!self.StegVerseMasterRecordsPortableSv001 || typeof self.StegVerseMasterRecordsPortableSv001.process !== "function") {
    return Promise.resolve(jsonResponse(503, { state: "FAIL_CLOSED", reason: "canonical Master Records portable custody module unavailable", authority_effect: "NONE" }));
  }
  var source;
  var sourceHash;
  var suppliedAdmission;
  var result;
  var admissionEntry;
  var custodyEntry;
  var reconstructionEntry;
  return request.json().then(function (body) {
    source = body && body.cycle_receipt ? body.cycle_receipt : body;
    suppliedAdmission = body && body.intr_admission_receipt ? body.intr_admission_receipt : null;
    sourceHash = source && source.receipt_hash ? String(source.receipt_hash) : "";
    if (sourceHash !== MR_SV001_CANONICAL_SOURCE_SHA || !source || source.transition_id !== "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED") {
      throw new Error("FAIL_CLOSED: exact canonical G23 completed SV001 cycle receipt required");
    }
    return findMasterRecordsSv001Custody(sourceHash);
  }).then(function (existing) {
    if (existing.custody_entry && existing.reconstruction_entry) {
      admissionEntry = existing.admission_entry;
      custodyEntry = existing.custody_entry;
      reconstructionEntry = existing.reconstruction_entry;
      return self.StegVerseMasterRecordsPortableSv001.process(source).then(function (processed) {
        result = processed;
        if (!result || result.state !== "PASS" || result.reconstruction.state !== "PASS") { throw new Error("FAIL_CLOSED: canonical Master Records reconstruction did not PASS"); }
        return replayJournal();
      }).then(function (replay) {
        if (!replay || replay.state !== "PASS") { throw new Error("FAIL_CLOSED: journal replay did not PASS"); }
        return masterRecordsSv001Proof(result, admissionEntry, custodyEntry, reconstructionEntry, replay, true);
      });
    }
    if (existing.custody_entry || existing.reconstruction_entry) {
      throw new Error("FAIL_CLOSED: partial Master Records custody state requires explicit recovery");
    }
    return validateMasterRecordsSv001IntrAdmission(suppliedAdmission, sourceHash).then(function (admission) {
      return appendReceipt(admission);
    }).then(function (entry) {
      admissionEntry = entry;
      return self.StegVerseMasterRecordsPortableSv001.process(source);
    }).then(function (processed) {
      result = processed;
      if (!result || result.state !== "PASS" || result.reconstruction.state !== "PASS") { throw new Error("FAIL_CLOSED: canonical Master Records reconstruction did not PASS"); }
      return appendReceipt(result.custody);
    }).then(function (entry) {
      custodyEntry = entry;
      return appendReceipt(result.reconstruction);
    }).then(function (entry) {
      reconstructionEntry = entry;
      return replayJournal();
    }).then(function (replay) {
      if (!replay || replay.state !== "PASS") { throw new Error("FAIL_CLOSED: post-custody journal replay did not PASS"); }
      return masterRecordsSv001Proof(result, admissionEntry, custodyEntry, reconstructionEntry, replay, false);
    });
  }).then(function (proof) {
    return jsonResponse(200, proof);
  }).catch(function (error) {
    return jsonResponse(400, {
      state: "FAIL_CLOSED",
      reason: String(error && error.message ? error.message : error),
      source_receipt_sha256: sourceHash || null,
      intr_governance_admission_observed: false,
      site_custody_authority: false,
      site_execution_authority: false,
      human_approval_checkpoint_inserted: false,
      prior_receipt_authorizes_transition: false,
      authority_effect: "NONE"
    });
  });
}

function canonicalEvidence() {
  return self.StegVerseReferenceBrowserModel.runtimeProof(LOCAL_ENDPOINT).then(function (proof) {
    return self.StegVerseTVCPortableRoute.evaluate(proof, LOCAL_ENDPOINT).then(function (route) {
      if (route.state !== "ROUTE_ADMITTED") { throw new Error("TVC device-local route denied: " + route.reason); }
      return {
        schema: "stegos.web_canonical_inference_evidence.v1",
        model: { canonical_owner: "StegVerse-002/micro-node-runtime", model_id: "stegverse-reference-lm-v1", credential_authority: "TV/TVC",
          github_token_required: false, third_party_inference_required: false, model_output_authority: "NONE", proof_valid: proof.state === "VERIFIED_REFERENCE_MODEL_RUNTIME",
          endpoint_scope: "stegverse-local", endpoint: LOCAL_ENDPOINT, proof_sha256: route.runtime_proof_hash, proof: proof },
        route: { canonical_owner: "StegVerse-Labs/TVC", task_id: "TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002", credential_authority: "TV/TVC",
          model_output_authority: "NONE", endpoint_scope: "stegverse-local", receipt: route },
        source_provenance: { model_runtime_commit: "ce142a56bf4ac14c2fb075c78bcc413a02bc0f5e", tvc_route_commit: "cf673ced2b0f13d0c2ef4fa581e477a660771a75" },
        external_non_stegverse_machine_required: false, network_egress_required: false, authority_effect: "NONE"
      };
    });
  });
}
function handleLocalModel(request, url) {
  var suffix = url.pathname.slice(LOCAL_PATH.length) || "/";
  if (request.method === "GET" && (suffix === "/" || suffix === "/health")) {
    return self.StegVerseReferenceBrowserModel.modelHash().then(function (hash) {
      return jsonResponse(200, { state: "READY", model: "stegverse-reference-lm-v1", model_hash: hash, runtime: "browser-service-worker",
        device_local_intercepted_endpoint: true, task_control: "DEVICE_LOCAL_FENCED", network_egress_required: false,
        third_party_inference_required: false, authority_effect: "NONE" });
    });
  }
  if (request.method === "GET" && suffix === "/v1/models") {
    return jsonResponse(200, { object: "list", data: [{ id: "stegverse-reference-lm-v1", object: "model", owned_by: "StegVerse" }] });
  }
  if (request.method === "GET" && suffix === "/canonical-evidence") {
    return canonicalEvidence().then(function (bundle) { return jsonResponse(200, bundle); }).catch(function (error) {
      return jsonResponse(503, { state: "FAIL_CLOSED", reason: String(error && error.message ? error.message : error), authority_effect: "NONE" });
    });
  }
  if (request.method === "POST" && suffix === "/v1/chat/completions") {
    return request.json().then(function (body) { return executeDeviceTask(body); }).then(function (result) { return jsonResponse(200, result); }).catch(function (error) {
      return jsonResponse(400, { error: String(error && error.message ? error.message : error), authority_effect: "NONE" });
    });
  }
  return Promise.resolve(jsonResponse(404, { error: "not_found", authority_effect: "NONE" }));
}
self.addEventListener("install", function (event) {
  event.waitUntil(caches.open(CACHE_NAME).then(function (cache) { return cache.addAll(SHELL); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (key) { return key !== CACHE_NAME; }).map(function (key) { return caches.delete(key); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (event) {
  var url = new URL(event.request.url);
  if (url.origin === self.location.origin && url.pathname === MASTER_RECORDS_SV001_PATH && event.request.method === "POST") {
    event.respondWith(handleMasterRecordsSv001Custody(event.request));
    return;
  }
  if (url.origin === self.location.origin && url.pathname === PORTABLE_WC_PATH && event.request.method === "POST") {
    event.respondWith(handlePortableWorkerCoordinatorSv001(event.request));
    return;
  }
  if (url.origin === self.location.origin && url.pathname === RESIDENT_TASK_PATH && event.request.method === "POST") {
    event.respondWith(handleExternalResidentTask(event.request));
    return;
  }
  if (url.origin === self.location.origin && (url.pathname === LOCAL_PATH || url.pathname.indexOf(LOCAL_PATH + "/") === 0)) {
    event.respondWith(handleLocalModel(event.request, url));
    return;
  }
  if (event.request.method !== "GET") { return; }
  event.respondWith(caches.match(event.request).then(function (cached) {
    if (cached) { return cached; }
    return fetch(event.request).then(function (response) {
      if (!response || response.status !== 200 || response.type === "opaque") { return response; }
      var copy = response.clone();
      caches.open(CACHE_NAME).then(function (cache) { cache.put(event.request, copy); });
      return response;
    });
  }));
});
