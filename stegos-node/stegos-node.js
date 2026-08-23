"use strict";

(function () {
  var DB_NAME = "stegos-node-v1";
  var DB_VERSION = 1;
  var META = "meta";
  var RECEIPTS = "receipts";
  var REGISTRATION_KEY = "registration";
  var PERSONAL_KV_SYNC_KEY = "personal-kv-sync";
  var NETWORK_SYNC_KEY = "stegos-network-sync";

  function bytesToHex(bytes) {
    var out = "";
    for (var i = 0; i < bytes.length; i += 1) out += bytes[i].toString(16).padStart(2, "0");
    return out;
  }

  function canonicalize(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
    return "{" + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ":" + canonicalize(value[key]);
    }).join(",") + "}";
  }

  function sha256Hex(value) {
    var text = typeof value === "string" ? value : canonicalize(value);
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
      request.onerror = function () { reject(request.error || new Error("StegOS Node storage unavailable")); };
    });
  }

  function txDone(tx) {
    return new Promise(function (resolve, reject) {
      tx.oncomplete = function () { resolve(); };
      tx.onerror = function () { reject(tx.error || new Error("StegOS Node storage transaction failed")); };
      tx.onabort = function () { reject(tx.error || new Error("StegOS Node storage transaction aborted")); };
    });
  }

  function getMeta(key) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(META, "readonly");
        var req = tx.objectStore(META).get(key);
        req.onsuccess = function () { resolve(req.result ? req.result.value : null); };
        req.onerror = function () { reject(req.error); };
        tx.oncomplete = function () { db.close(); };
      });
    });
  }

  function putMeta(key, value) {
    return openDb().then(function (db) {
      var tx = db.transaction(META, "readwrite");
      tx.objectStore(META).put({ key: key, value: value });
      return txDone(tx).then(function () { db.close(); return value; });
    });
  }

  function getReceipts() {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(RECEIPTS, "readonly");
        var req = tx.objectStore(RECEIPTS).getAll();
        req.onsuccess = function () {
          var rows = req.result || [];
          rows.sort(function (a, b) { return a.receipt_number - b.receipt_number; });
          resolve(rows);
        };
        req.onerror = function () { reject(req.error); };
        tx.oncomplete = function () { db.close(); };
      });
    });
  }

  function putReceipt(receipt) {
    return openDb().then(function (db) {
      var tx = db.transaction(RECEIPTS, "readwrite");
      tx.objectStore(RECEIPTS).put(receipt);
      return txDone(tx).then(function () { db.close(); return receipt; });
    });
  }

  function validateGenesis(receipt) {
    if (!receipt || receipt.schema !== "stegos.node_handoff_receipt.v1") throw new Error("Invalid Receipt #1 schema");
    if (receipt.receipt_number !== 1 || receipt.transition !== "NODE_REGISTERED") throw new Error("Invalid Receipt #1 transition");
    if (receipt.prior_state !== "UNREGISTERED" || receipt.resulting_state !== "REGISTERED") throw new Error("Invalid Receipt #1 states");
    if (receipt.continuity_parent !== "GENESIS") throw new Error("Invalid Receipt #1 continuity parent");
    if (receipt.authority_effect !== "NONE") throw new Error("Receipt #1 cannot grant external authority");
    if (receipt.credential_authority !== "TV/TVC") throw new Error("Credential authority mismatch");
    var body = Object.assign({}, receipt);
    var claimed = body.receipt_sha256;
    delete body.receipt_sha256;
    return sha256Hex(body).then(function (actual) {
      if (actual !== claimed) throw new Error("Receipt #1 digest mismatch");
      return receipt;
    });
  }

  function deriveIdentity(deviceBindingSha256, label, prefix) {
    return sha256Hex(label + ":" + deviceBindingSha256).then(function (digest) {
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
      return sha256Hex(body).then(function (digest) {
        return Object.assign({}, body, { receipt_sha256: digest });
      });
    });
  }

  function registerDevice() {
    return Promise.all([getMeta(REGISTRATION_KEY), getReceipts()]).then(function (values) {
      var existing = values[0];
      var receipts = values[1];
      if (existing && receipts.length) {
        return validateGenesis(receipts[0]).then(function () { return existing; });
      }
      var random = new Uint8Array(32);
      crypto.getRandomValues(random);
      return sha256Hex(bytesToHex(random)).then(function (commitment) {
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
          return putReceipt(receipt).then(function () { return putMeta(REGISTRATION_KEY, registration); });
        });
      });
    });
  }

  function sectionFor(receipt) {
    var transition = String(receipt.transition || receipt.event || "").toUpperCase();
    if (transition.indexOf("REGISTER") >= 0) return "Device Registration";
    if (transition.indexOf("KV") >= 0 || transition.indexOf("VAULT") >= 0) return "KnowledgeVault";
    if (transition.indexOf("HEARTBEAT") >= 0 || transition.indexOf("SYNC") >= 0) return "HeartBeat";
    if (transition.indexOf("MODULE") >= 0) return "Modules";
    if (transition.indexOf("INSTALL") >= 0) return "Installation";
    if (transition.indexOf("EXTERNAL") >= 0 || transition.indexOf("CONNECT") >= 0) return "External Connections";
    if (transition.indexOf("STATE") >= 0) return "Device State";
    return "Other";
  }

  function historyProjection() {
    return Promise.all([
      getMeta(REGISTRATION_KEY),
      getMeta(PERSONAL_KV_SYNC_KEY),
      getMeta(NETWORK_SYNC_KEY),
      getReceipts()
    ]).then(function (values) {
      var registration = values[0];
      var receipts = values[3];
      var sections = {};
      receipts.forEach(function (receipt) {
        var section = sectionFor(receipt);
        if (!sections[section]) sections[section] = [];
        sections[section].push(receipt);
      });
      return {
        schema: "stegos.offline_device_history_projection.v1",
        offline_capable: true,
        current_network_required: false,
        registration: registration,
        local_receipt_head: receipts.length ? {
          receipt_number: receipts[receipts.length - 1].receipt_number,
          receipt_sha256: receipts[receipts.length - 1].receipt_sha256
        } : null,
        last_personal_kv_sync: values[1],
        last_stegos_network_sync: values[2],
        sections: sections,
        canonical_chain_receipt_count: receipts.length,
        section_views_are_filtered_projections: true,
        competing_logs_allowed: false,
        wall_clock_is_causal_order: false,
        credential_authority: "TV/TVC",
        authority_effect: "NONE"
      };
    });
  }

  function syncText(sync) {
    if (!sync) return "Not yet observed";
    var head = sync.receipt_number ? "Receipt #" + sync.receipt_number : "Observed";
    return sync.observed_at ? head + " · " + sync.observed_at : head;
  }

  function render() {
    return historyProjection().then(function (projection) {
      var registerButton = document.getElementById("register-device");
      var state = document.getElementById("node-state");
      var nodeId = document.getElementById("node-id");
      var receiptHead = document.getElementById("local-receipt-head");
      var personal = document.getElementById("personal-kv-sync");
      var network = document.getElementById("network-sync");
      var kv = document.getElementById("knowledge-vault-state");
      var history = document.getElementById("history");

      if (projection.registration) {
        state.textContent = "REGISTERED";
        nodeId.textContent = projection.registration.node_id;
        registerButton.disabled = true;
        registerButton.textContent = "Device Registered";
        kv.textContent = "Available";
      } else {
        state.textContent = "UNREGISTERED";
        nodeId.textContent = "Not registered";
        kv.textContent = "Locked until Receipt #1";
      }
      receiptHead.textContent = projection.local_receipt_head ? "Receipt #" + projection.local_receipt_head.receipt_number : "None";
      personal.textContent = syncText(projection.last_personal_kv_sync);
      network.textContent = syncText(projection.last_stegos_network_sync);
      history.innerHTML = "";

      Object.keys(projection.sections).forEach(function (sectionName) {
        var section = document.createElement("section");
        section.className = "history-section";
        var heading = document.createElement("h3");
        heading.textContent = sectionName;
        var links = document.createElement("p");
        links.className = "section-links";
        links.innerHTML = '<a href="#about-' + sectionName.toLowerCase().replace(/[^a-z0-9]+/g, "-") + '">What is this?</a> · <button type="button" class="link-button">View receipts</button>';
        var list = document.createElement("ol");
        list.hidden = true;
        projection.sections[sectionName].forEach(function (receipt) {
          var item = document.createElement("li");
          item.textContent = "Receipt #" + receipt.receipt_number + " — " + (receipt.transition || receipt.event || "Transition");
          list.appendChild(item);
        });
        links.querySelector("button").addEventListener("click", function () { list.hidden = !list.hidden; });
        section.appendChild(heading);
        section.appendChild(links);
        section.appendChild(list);
        history.appendChild(section);
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var button = document.getElementById("register-device");
    button.addEventListener("click", function () {
      button.disabled = true;
      button.textContent = "Registering…";
      registerDevice().then(render).catch(function (error) {
        button.disabled = false;
        button.textContent = "Register Device";
        document.getElementById("node-error").textContent = "FAIL_CLOSED: " + error.message;
      });
    });
    render();
    if ("serviceWorker" in navigator) navigator.serviceWorker.register("./service-worker.js");
  });

  window.StegOSNodeProjection = {
    registerDevice: registerDevice,
    historyProjection: historyProjection,
    validateGenesis: validateGenesis
  };
}());
