(function (root) {
  "use strict";

  var DB_NAME = "stegos-node-v1";
  var DB_VERSION = 1;
  var META = "meta";
  var RECEIPTS = "receipts";
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
    capabilityProgress: capabilityProgress,
    recordStep: recordStep,
    appendCapabilityReceipt: appendCapabilityReceipt,
    trialStatus: trialStatus,
    beforeLlmRequest: beforeLlmRequest,
    recordLlmExecution: recordLlmExecution,
    maxUnregisteredLlmQuestions: MAX_UNREGISTERED_LLM,
    authority_effect: "NONE",
    credential_authority: "TV/TVC"
  };
}(typeof globalThis !== "undefined" ? globalThis : window));
