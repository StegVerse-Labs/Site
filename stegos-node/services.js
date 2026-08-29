"use strict";

(function () {
  var DB_NAME = "stegos-node-v1";
  var DB_VERSION = 1;
  var META = "meta";
  var RECEIPTS = "receipts";

  function canonicalize(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
    return "{" + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ":" + canonicalize(value[key]);
    }).join(",") + "}";
  }

  function bytesToHex(bytes) {
    var out = "";
    for (var i = 0; i < bytes.length; i += 1) out += bytes[i].toString(16).padStart(2, "0");
    return out;
  }

  function sha256Hex(value) {
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonicalize(value))).then(function (digest) {
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
      request.onerror = function () { reject(request.error || new Error("StegOS Node storage unavailable")); };
    });
  }

  function getLocalEvidence() {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction([META, RECEIPTS], "readonly");
        var registration = tx.objectStore(META).get("registration");
        var receipt = tx.objectStore(RECEIPTS).get(1);
        tx.oncomplete = function () {
          db.close();
          resolve({
            registration: registration.result ? registration.result.value : null,
            receipt: receipt.result || null
          });
        };
        tx.onerror = function () { reject(tx.error || new Error("Receipt #1 read failed")); };
      });
    });
  }

  function validateReceipt1(evidence) {
    var registration = evidence.registration;
    var receipt = evidence.receipt;
    if (!registration || registration.schema !== "stegos.node_registration_projection.v1" ||
        registration.state !== "REGISTERED" || registration.receipt_number !== 1 ||
        registration.authority_effect !== "NONE" || registration.credential_authority !== "TV/TVC") {
      return Promise.resolve(false);
    }
    if (!receipt || receipt.schema !== "stegos.node_handoff_receipt.v1" ||
        receipt.receipt_number !== 1 || receipt.transition !== "NODE_REGISTERED" ||
        receipt.prior_state !== "UNREGISTERED" || receipt.resulting_state !== "REGISTERED" ||
        receipt.continuity_parent !== "GENESIS" || receipt.authority_effect !== "NONE" ||
        receipt.credential_authority !== "TV/TVC") {
      return Promise.resolve(false);
    }
    var body = Object.assign({}, receipt);
    var claimed = body.receipt_sha256;
    delete body.receipt_sha256;
    return sha256Hex(body).then(function (actual) {
      return actual === claimed &&
        registration.receipt_sha256 === claimed &&
        registration.node_id === receipt.node_id &&
        registration.interlock_id === receipt.interlock_id;
    });
  }

  function loadSnapshot() {
    return fetch("./kv-readiness-snapshot.json", { cache: "no-store" }).then(function (response) {
      if (!response.ok) throw new Error("Canonical KV readiness snapshot unavailable");
      return response.json();
    }).then(function (snapshot) {
      if (!snapshot || snapshot.schema !== "stegverse.kv.activation-readiness-snapshot/v1" ||
          snapshot.authority_effect !== "NONE" || snapshot.activation_performed !== false ||
          typeof snapshot.production_interlock_runtime_activated !== "boolean" ||
          !Array.isArray(snapshot.entries) || snapshot.entry_count !== snapshot.entries.length) {
        throw new Error("Canonical KV readiness snapshot invalid");
      }
      return snapshot;
    });
  }

  function card(entry, state) {
    var article = document.createElement("article");
    article.className = "service";
    article.dataset.state = state.service_state;
    article.setAttribute("aria-label", entry.entry_id + ": " + state.service_state);
    var heading = document.createElement("h2");
    heading.textContent = entry.entry_id;
    var badge = document.createElement("span");
    badge.className = "badge";
    badge.textContent = state.service_state;
    var reason = document.createElement("p");
    reason.textContent = state.reason;
    var action = document.createElement("p");
    action.className = "meta";
    action.textContent = state.required_action ? "Required action: " + state.required_action : "Required action: none";
    var verdict = document.createElement("p");
    verdict.className = "meta";
    verdict.textContent = "Governed readiness: " + entry.governed_action_readiness;
    article.appendChild(heading);
    article.appendChild(badge);
    article.appendChild(reason);
    article.appendChild(action);
    article.appendChild(verdict);
    return article;
  }

  function render(snapshot, registrationVerified) {
    var services = snapshot.entries.filter(function (entry) { return entry.entry_type === "SERVICE"; });
    var target = document.getElementById("services");
    target.textContent = "";
    services.forEach(function (entry) {
      var state = window.StegVerseServiceState.classify(entry, {
        registration_verified: registrationVerified,
        production_interlock_runtime_activated: snapshot.production_interlock_runtime_activated
      });
      target.appendChild(card(entry, state));
    });
    document.getElementById("projection-state").textContent =
      registrationVerified ? "Established Node · Receipt #1 verified" : "REVIEW · Register Device";
    document.getElementById("projection-detail").textContent =
      "KV facts: " + (snapshot.facts_observed_at || "unknown") +
      " · services: " + services.length +
      " · runtime activation claimed: false · authority effect: NONE";
  }

  function failClosed(error) {
    document.getElementById("projection-state").textContent = "UNAVAILABLE · FAIL_CLOSED";
    document.getElementById("projection-state").className = "fail";
    document.getElementById("projection-detail").textContent = error.message;
    document.getElementById("services").textContent = "";
  }

  document.addEventListener("DOMContentLoaded", function () {
    Promise.all([getLocalEvidence(), loadSnapshot()]).then(function (values) {
      return validateReceipt1(values[0]).then(function (verified) {
        render(values[1], verified);
      });
    }).catch(failClosed);
  });
}());
