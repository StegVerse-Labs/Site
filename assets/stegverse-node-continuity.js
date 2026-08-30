(function (root) {
  "use strict";

  var DB_NAME = "stegos-node-v1";
  var DB_VERSION = 2;
  var META = "meta";
  var RECEIPTS = "receipts";
  var INTR_OUTBOX = "intr_outbox";
  var REGISTRATION_KEY = "registration";
  var TRIAL_KEY = "ecosystem-chat-unregistered-llm-usage";
  var MAX_UNREGISTERED_LLM = 10;

  function bytesToHex(bytes) {
    return Array.from(bytes, function (b) { return b.toString(16).padStart(2, "0"); }).join("");
  }

  function canonical(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]";
    return "{" + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ":" + canonical(value[key]);
    }).join(",") + "}";
  }

  function sha256(value) {
    var text = typeof value === "string" ? value : canonical(value);
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(function (digest) {
      return bytesToHex(new Uint8Array(digest));
    });
  }

  function openDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(META)) db.createObjectStore(META, { keyPath: "key" });
        if (!db.objectStoreNames.contains(RECEIPTS)) db.createObjectStore(RECEIPTS, { keyPath: "receipt_number" });
        if (!db.objectStoreNames.contains(INTR_OUTBOX)) db.createObjectStore(INTR_OUTBOX, { keyPath: "materialization_id" });
      };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("StegVerse Node storage unavailable")); };
    });
  }

  function readStore(store, key) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(store, "readonly");
        var req = key === undefined ? tx.objectStore(store).getAll() : tx.objectStore(store).get(key);
        req.onsuccess = function () { resolve(req.result || null); };
        req.onerror = function () { reject(req.error); };
        tx.oncomplete = function () { db.close(); };
      });
    });
  }

  function writeMeta(key, value) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(META, "readwrite");
        tx.objectStore(META).put({ key: key, value: value });
        tx.oncomplete = function () { db.close(); resolve(value); };
        tx.onerror = function () { reject(tx.error); };
      });
    });
  }

  function getRegistration() {
    return readStore(META, REGISTRATION_KEY).then(function (row) { return row ? row.value : null; });
  }

  function getReceipts() {
    return readStore(RECEIPTS).then(function (rows) {
      rows = Array.isArray(rows) ? rows : [];
      rows.sort(function (a, b) { return a.receipt_number - b.receipt_number; });
      return rows;
    });
  }

  function validateGenesis(receipt) {
    if (!receipt || receipt.schema !== "stegos.node_handoff_receipt.v1") throw new Error("Invalid Node Receipt #1 schema");
    if (receipt.receipt_number !== 1 || receipt.transition !== "NODE_REGISTERED") throw new Error("Invalid Node Receipt #1");
    if (receipt.continuity_parent !== "GENESIS" || receipt.authority_effect !== "NONE" || receipt.credential_authority !== "TV/TVC") {
      throw new Error("Invalid Node Receipt #1 authority boundary");
    }
    var body = Object.assign({}, receipt);
    var claimed = body.receipt_sha256;
    delete body.receipt_sha256;
    return sha256(body).then(function (actual) {
      if (actual !== claimed) throw new Error("Node Receipt #1 digest mismatch");
      return receipt;
    });
  }

  function deriveIdentity(deviceBindingSha256, label, prefix) {
    return sha256(label + ":" + deviceBindingSha256).then(function (digest) {
      return prefix + digest.slice(0, 24);
    });
  }

  function createGenesis(deviceBindingSha256) {
    return Promise.all([
      deriveIdentity(deviceBindingSha256, "stegos-node", "SV-NODE-"),
      deriveIdentity(deviceBindingSha256, "stegos-interlock", "SV-IL-")
    ]).then(function (ids) {
      var body = {
        schema: "stegos.node_handoff_receipt.v1",
        receipt_number: 1,
        transition: "NODE_REGISTERED",
        prior_state: "UNREGISTERED",
        resulting_state: "REGISTERED",
        continuity_parent: "GENESIS",
        node_id: ids[0],
        interlock_id: ids[1],
        device_binding_sha256: deviceBindingSha256,
        authority_effect: "NONE",
        heartbeat_authority: "StegVerse-Labs/.github",
        credential_authority: "TV/TVC"
      };
      return sha256(body).then(function (digest) {
        return Object.assign({}, body, { receipt_sha256: digest });
      });
    });
  }

  function registerDevice() {
    return status().then(function (current) {
      if (current.registered) return current.registration;
      var random = new Uint8Array(32);
      crypto.getRandomValues(random);
      return sha256(bytesToHex(random)).then(function (commitment) {
        random.fill(0);
        return createGenesis(commitment);
      }).then(function (receipt) {
        return validateGenesis(receipt).then(function () {
          var registration = {
            schema: "stegos.node_registration_projection.v1",
            state: "REGISTERED",
            node_id: receipt.node_id,
            interlock_id: receipt.interlock_id,
            device_binding_sha256: receipt.device_binding_sha256,
            receipt_number: 1,
            receipt_sha256: receipt.receipt_sha256,
            knowledge_vault_materialization_enabled: true,
            hardware_attestation_claimed: false,
            credential_authority: "TV/TVC",
            authority_effect: "NONE"
          };
          return openDb().then(function (db) {
            return new Promise(function (resolve, reject) {
              var tx = db.transaction([RECEIPTS, META], "readwrite");
              tx.objectStore(RECEIPTS).add(receipt);
              tx.objectStore(META).put({ key: REGISTRATION_KEY, value: registration });
              tx.oncomplete = function () { db.close(); resolve(registration); };
              tx.onerror = function () { reject(tx.error || new Error("Device registration failed")); };
              tx.onabort = function () { db.close(); };
            });
          });
        });
      });
    });
  }

  function status() {
    return Promise.all([getRegistration(), getReceipts()]).then(function (values) {
      var registration = values[0];
      var receipts = values[1];
      if (!registration) return { registered: false, state: "UNREGISTERED", registration: null, receipts: receipts };
      if (!receipts.length) throw new Error("FAIL_CLOSED: registration exists without Receipt #1");
      return validateGenesis(receipts[0]).then(function () {
        if (registration.node_id !== receipts[0].node_id || registration.receipt_sha256 !== receipts[0].receipt_sha256) {
          throw new Error("FAIL_CLOSED: registration and Receipt #1 do not match");
        }
        return { registered: true, state: "REGISTERED", registration: registration, receipts: receipts };
      });
    });
  }

  function appendReceipt(input) {
    return status().then(function (current) {
      if (!current.registered) throw new Error("REGISTER_DEVICE_REQUIRED");
      var receipts = current.receipts;
      var head = receipts[receipts.length - 1];
      var body = {
        schema: "stegos.node_capability_receipt.v1",
        receipt_number: head.receipt_number + 1,
        transition: String(input.transition || "").toUpperCase(),
        capability: String(input.capability || ""),
        step: input.step == null ? null : String(input.step),
        resulting_state: String(input.resulting_state || "OBSERVED"),
        continuity_parent: head.receipt_sha256,
        node_id: current.registration.node_id,
        interlock_id: current.registration.interlock_id,
        evidence_ref: input.evidence_ref ? String(input.evidence_ref) : null,
        contains_personal_information: false,
        contains_credentials: false,
        authority_effect: "NONE",
        credential_authority: "TV/TVC",
        observed_at: new Date().toISOString()
      };
      if (!body.transition || !body.capability) throw new Error("transition and capability are required");
      return sha256(body).then(function (digest) {
        var receipt = Object.assign({}, body, { receipt_sha256: digest });
        return openDb().then(function (db) {
          return new Promise(function (resolve, reject) {
            var tx = db.transaction(RECEIPTS, "readwrite");
            var store = tx.objectStore(RECEIPTS);
            var get = store.get(receipt.receipt_number);
            get.onsuccess = function () {
              if (get.result) {
                tx.abort();
                reject(new Error("FAIL_CLOSED: Node receipt head changed; retry"));
                return;
              }
              store.add(receipt);
            };
            tx.oncomplete = function () { db.close(); resolve(receipt); };
            tx.onerror = function () { reject(tx.error || new Error("Node receipt append failed")); };
            tx.onabort = function () { db.close(); };
          });
        });
      });
    });
  }

  function appendCapabilityReceipt(input) {
    if (navigator.locks && navigator.locks.request) {
      return navigator.locks.request("stegverse-node-receipt-chain", function () { return appendReceipt(input); });
    }
    return appendReceipt(input);
  }

  function capabilityProgress(capability) {
    return status().then(function (current) {
      var steps = {};
      current.receipts.forEach(function (receipt) {
        if (receipt.schema === "stegos.node_capability_receipt.v1" && receipt.capability === capability && receipt.step) {
          steps[receipt.step] = receipt;
        }
      });
      return { registered: current.registered, registration: current.registration, steps: steps, receipts: current.receipts };
    });
  }

  function recordStep(capability, step, state, evidenceRef) {
    return capabilityProgress(capability).then(function (progress) {
      var prior = progress.steps[String(step)];
      if (prior && prior.resulting_state === state) return prior;
      return appendCapabilityReceipt({
        transition: capability.toUpperCase().replace(/[^A-Z0-9]+/g, "_") + "_STEP_" + step + "_" + state,
        capability: capability,
        step: step,
        resulting_state: state,
        evidence_ref: evidenceRef || null
      });
    });
  }

  function validateMaterializationRequest(request) {
    if (!request || request.schema !== "stegverse.universal-intr-materialization-request/v1") throw new Error("Invalid InTr materialization request schema");
    if (request.state !== "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION") throw new Error("Invalid InTr materialization request state");
    if (request.transport_schema !== "stegverse.universal-intr-transport/v1" || request.transport_protocol !== "InTr") throw new Error("Invalid InTr transport binding");
    if (request.event_triggered !== true || request.always_on_receiver_required !== false || request.second_user_device_required !== false) throw new Error("Invalid InTr availability semantics");
    if (request.receiver_unavailable_disposition !== "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION") throw new Error("Invalid InTr unavailable disposition");
    if (request.request_grants_execution_authority !== false || request.claim_or_fence_minted !== false || request.transport_grants_execution_authority !== false) throw new Error("InTr materialization request cannot grant authority");
    if (request.credential_authority !== "TV/TVC" || request.github_token_runtime_authority !== "NONE" || request.authority_effect !== "NONE_REQUEST_ONLY") throw new Error("Invalid InTr materialization request authority boundary");
    if (!/^INTR-MAT-[a-f0-9]{24}$/.test(String(request.materialization_id || ""))) throw new Error("Invalid InTr materialization id");
    if (!/^sha256:[a-f0-9]{64}$/.test(String(request.request_hash || ""))) throw new Error("Invalid InTr materialization request hash");
    var body = Object.assign({}, request);
    var claimed = body.request_hash;
    delete body.request_hash;
    return sha256(body).then(function (actual) {
      if ("sha256:" + actual !== claimed) throw new Error("InTr materialization request hash mismatch");
      return request;
    });
  }

  function queueIntrMaterializationRequest(request) {
    return Promise.all([status(), validateMaterializationRequest(request)]).then(function (values) {
      var node = values[0];
      if (!node.registered) throw new Error("REGISTER_DEVICE_REQUIRED");
      var reg = node.registration;
      var body = {
        schema: "stegos.node_intr_outbox_entry.v1",
        state: "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY",
        node_id: reg.node_id,
        interlock_id: reg.interlock_id,
        materialization_id: request.materialization_id,
        request_hash: request.request_hash,
        transport_intent_hash: request.transport_intent_hash,
        payload_hash: request.payload_hash,
        destination: request.destination,
        downstream_owner_ref: request.downstream_owner_ref,
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
      return sha256(body).then(function (digest) {
        var entry = Object.assign({}, body, { outbox_entry_hash: "sha256:" + digest });
        return openDb().then(function (db) {
          return new Promise(function (resolve, reject) {
            var tx = db.transaction(INTR_OUTBOX, "readwrite");
            var store = tx.objectStore(INTR_OUTBOX);
            var get = store.get(entry.materialization_id);
            get.onsuccess = function () {
              if (get.result && canonical(get.result) !== canonical(entry)) {
                tx.abort();
                reject(new Error("FAIL_CLOSED: InTr outbox write-once collision"));
                return;
              }
              if (!get.result) store.add(entry);
            };
            get.onerror = function () { reject(get.error || new Error("InTr outbox read failed")); };
            tx.oncomplete = function () { db.close(); resolve(entry); };
            tx.onerror = function () { db.close(); reject(tx.error || new Error("InTr outbox write failed")); };
            tx.onabort = function () { db.close(); };
          });
        });
      });
    });
  }

  function getIntrOutbox() {
    return readStore(INTR_OUTBOX).then(function (rows) { return Array.isArray(rows) ? rows : []; });
  }

  function trialStatus() {
    return status().then(function (node) {
      if (node.registered) {
        return { node_registered: true, limit_applies: false, used: 0, remaining: null, limit: MAX_UNREGISTERED_LLM };
      }
      return readStore(META, TRIAL_KEY).then(function (row) {
        var value = row && row.value ? row.value : { schema: "stegverse.unregistered_llm_usage.v1", used: 0 };
        var used = Math.max(0, Math.min(MAX_UNREGISTERED_LLM, Number(value.used) || 0));
        return { node_registered: false, limit_applies: true, used: used, remaining: MAX_UNREGISTERED_LLM - used, limit: MAX_UNREGISTERED_LLM };
      });
    });
  }

  function beforeLlmRequest() {
    return trialStatus().then(function (trial) {
      if (trial.limit_applies && trial.remaining <= 0) {
        var error = new Error("UNREGISTERED_LLM_LIMIT_REACHED");
        error.code = "UNREGISTERED_LLM_LIMIT_REACHED";
        error.trial = trial;
        throw error;
      }
      return trial;
    });
  }

  function recordLlmExecution() {
    return trialStatus().then(function (trial) {
      if (!trial.limit_applies) return trial;
      var used = Math.min(MAX_UNREGISTERED_LLM, trial.used + 1);
      return writeMeta(TRIAL_KEY, {
        schema: "stegverse.unregistered_llm_usage.v1",
        used: used,
        max: MAX_UNREGISTERED_LLM,
        model_execution_count_only: true,
        authority_effect: "NONE"
      }).then(function () {
        return { node_registered: false, limit_applies: true, used: used, remaining: MAX_UNREGISTERED_LLM - used, limit: MAX_UNREGISTERED_LLM };
      });
    });
  }

  root.StegVerseNodeContinuity = {
    contract_version: "1.0.0",
    status: status,
    registerDevice: registerDevice,
    capabilityProgress: capabilityProgress,
    recordStep: recordStep,
    appendCapabilityReceipt: appendCapabilityReceipt,
    trialStatus: trialStatus,
    beforeLlmRequest: beforeLlmRequest,
    recordLlmExecution: recordLlmExecution,
    queueIntrMaterializationRequest: queueIntrMaterializationRequest,
    getIntrOutbox: getIntrOutbox,
    maxUnregisteredLlmQuestions: MAX_UNREGISTERED_LLM,
    authority_effect: "NONE",
    credential_authority: "TV/TVC"
  };
}(typeof globalThis !== "undefined" ? globalThis : window));
