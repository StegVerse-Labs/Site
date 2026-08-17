(function () {
  "use strict";

  var DB_NAME = "stegos-web-bootstrap-v1";
  var DB_VERSION = 1;
  var META_STORE = "meta";
  var RECEIPT_STORE = "receipts";
  var NODE_KEY = "node";
  var SERVICE_CHAT = "stegverse.ecosystem-chat";
  var AUTHORITY_PLANE = "STEGVERSE";
  var CREDENTIAL_AUTHORITY = "TV/TVC";

  function bytesToHex(bytes) {
    var out = "";
    for (var i = 0; i < bytes.length; i += 1) {
      out += bytes[i].toString(16).padStart(2, "0");
    }
    return out;
  }

  function canonicalize(value) {
    if (value === null || typeof value !== "object") {
      return JSON.stringify(value);
    }
    if (Array.isArray(value)) {
      return "[" + value.map(canonicalize).join(",") + "]";
    }
    var keys = Object.keys(value).sort();
    return "{" + keys.map(function (key) {
      return JSON.stringify(key) + ":" + canonicalize(value[key]);
    }).join(",") + "}";
  }

  function sha256Hex(value) {
    var text = typeof value === "string" ? value : canonicalize(value);
    var data = new TextEncoder().encode(text);
    return crypto.subtle.digest("SHA-256", data).then(function (digest) {
      return bytesToHex(new Uint8Array(digest));
    });
  }

  function randomHex(length) {
    var bytes = new Uint8Array(length);
    crypto.getRandomValues(bytes);
    return bytesToHex(bytes);
  }

  function openDb() {
    return new Promise(function (resolve, reject) {
      if (!window.indexedDB) {
        reject(new Error("IndexedDB unavailable"));
        return;
      }
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(META_STORE)) {
          db.createObjectStore(META_STORE, { keyPath: "key" });
        }
        if (!db.objectStoreNames.contains(RECEIPT_STORE)) {
          db.createObjectStore(RECEIPT_STORE, { keyPath: "sequence" });
        }
      };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("IndexedDB open failed")); };
      request.onblocked = function () { reject(new Error("IndexedDB open blocked")); };
    });
  }

  function transactionPromise(transaction) {
    return new Promise(function (resolve, reject) {
      transaction.oncomplete = function () { resolve(); };
      transaction.onerror = function () { reject(transaction.error || new Error("IndexedDB transaction failed")); };
      transaction.onabort = function () { reject(transaction.error || new Error("IndexedDB transaction aborted")); };
    });
  }

  function getMeta(db, key) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readonly");
      var req = tx.objectStore(META_STORE).get(key);
      req.onsuccess = function () { resolve(req.result ? req.result.value : null); };
      req.onerror = function () { reject(req.error || new Error("metadata read failed")); };
    });
  }

  function putMeta(db, key, value) {
    var tx = db.transaction(META_STORE, "readwrite");
    tx.objectStore(META_STORE).put({ key: key, value: value });
    return transactionPromise(tx);
  }

  function getReceipts(db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(RECEIPT_STORE, "readonly");
      var req = tx.objectStore(RECEIPT_STORE).getAll();
      req.onsuccess = function () {
        var rows = req.result || [];
        rows.sort(function (a, b) { return a.sequence - b.sequence; });
        resolve(rows);
      };
      req.onerror = function () { reject(req.error || new Error("receipt read failed")); };
    });
  }

  function appendReceipt(db, body) {
    return getReceipts(db).then(function (existing) {
      var sequence = existing.length + 1;
      var previous = existing.length ? existing[existing.length - 1].entry_sha256 : null;
      var envelope = {
        schema: "stegos.web_bootstrap_journal_entry.v1",
        sequence: sequence,
        previous_entry_sha256: previous,
        receipt: body
      };
      return sha256Hex(body).then(function (receiptHash) {
        envelope.receipt_sha256 = receiptHash;
        return sha256Hex(envelope);
      }).then(function (entryHash) {
        envelope.entry_sha256 = entryHash;
        var tx = db.transaction(RECEIPT_STORE, "readwrite");
        tx.objectStore(RECEIPT_STORE).add(envelope);
        return transactionPromise(tx).then(function () { return envelope; });
      });
    });
  }

  function runtimeCapabilities() {
    return {
      secure_context: window.isSecureContext === true,
      indexeddb: !!window.indexedDB,
      webcrypto: !!(window.crypto && window.crypto.subtle && window.crypto.getRandomValues),
      service_worker: "serviceWorker" in navigator,
      host_platform: "ios-safari-compatible-web",
      requires_external_non_stegverse_machine: false,
      activation_authority_plane: AUTHORITY_PLANE,
      credential_authority: CREDENTIAL_AUTHORITY,
      github_token_required: false,
      hosted_runtime_required_for_service_activation: false
    };
  }

  function requireLocalRuntime() {
    var caps = runtimeCapabilities();
    if (!caps.secure_context) { throw new Error("FAIL_CLOSED: secure HTTPS context required"); }
    if (!caps.indexeddb) { throw new Error("FAIL_CLOSED: IndexedDB required for local continuity"); }
    if (!caps.webcrypto) { throw new Error("FAIL_CLOSED: WebCrypto required for receipt hashing"); }
    return caps;
  }

  function probeOperationalReadiness() {
    var caps;
    try {
      caps = requireLocalRuntime();
    } catch (error) {
      return Promise.resolve({ state: "BLOCKED", reason: String(error.message || error), capabilities: runtimeCapabilities() });
    }
    return openDb().then(function (db) {
      return sha256Hex("stegos-operational-readiness-v1").then(function (digest) {
        return getMeta(db, NODE_KEY).then(function () {
          db.close();
          return {
            state: "READY",
            indexeddb_operational: true,
            webcrypto_operational: typeof digest === "string" && digest.length === 64,
            capabilities: caps,
            authority_effect: "NONE"
          };
        });
      });
    }).catch(function (error) {
      return {
        state: "BLOCKED",
        indexeddb_operational: false,
        webcrypto_operational: false,
        reason: String(error && error.message ? error.message : error),
        capabilities: caps,
        authority_effect: "NONE"
      };
    });
  }

  function readExistingNode() {
    return openDb().then(function (db) {
      return getMeta(db, NODE_KEY).then(function (node) {
        db.close();
        return node;
      });
    });
  }

  function establishNode() {
    var caps = requireLocalRuntime();
    return openDb().then(function (db) {
      return getMeta(db, NODE_KEY).then(function (existing) {
        if (existing) {
          return { db: db, node: existing, reused: true };
        }
        var createdAt = new Date().toISOString();
        var nonce = randomHex(32);
        return sha256Hex("stegverse-node-v1|" + location.origin + "|" + nonce).then(function (digest) {
          var node = {
            schema: "stegos.web_node.v1",
            node_id: "stegnode-web-" + digest.slice(0, 32),
            created_at: createdAt,
            host_origin: location.origin,
            host_user_agent_family: "ios-safari-compatible-web",
            activation_authority_plane: AUTHORITY_PLANE,
            credential_authority: CREDENTIAL_AUTHORITY,
            requires_external_non_stegverse_machine: false,
            github_token_runtime_authority: "NONE",
            hosted_ci_activation_authority: "NONE",
            upstream_authority_conferred: false
          };
          return putMeta(db, NODE_KEY, node).then(function () {
            return appendReceipt(db, {
              schema: "stegos.web_node_establishment_receipt.v1",
              node_id: node.node_id,
              created_at: createdAt,
              capability_snapshot: caps,
              activation_authority_plane: AUTHORITY_PLANE,
              credential_authority: CREDENTIAL_AUTHORITY,
              external_non_stegverse_machine_used_for_activation: false,
              upstream_authority_conferred: false
            });
          }).then(function () {
            return { db: db, node: node, reused: false };
          });
        });
      });
    });
  }

  function activateEcosystemChat() {
    return establishNode().then(function (state) {
      var node = state.node;
      var db = state.db;
      var serviceState = {
        service_id: SERVICE_CHAT,
        state: "ACTIVATED",
        activated_at: new Date().toISOString(),
        node_id: node.node_id,
        required_prerequisites: {
          local_node_runtime_ready: true,
          local_receipt_journal_ready: true
        },
        optional_capabilities: {
          tvc_route_interface_ready: false,
          sovereign_inference_route_ready: false
        },
        routed_actions_state: "FAIL_CLOSED_UNTIL_STEGVERSE_ROUTE_EVIDENCE",
        inference_actions_state: "FAIL_CLOSED_UNTIL_STEGVERSE_MODEL_EVIDENCE",
        activation_authority_plane: AUTHORITY_PLANE,
        credential_authority: CREDENTIAL_AUTHORITY,
        requires_external_non_stegverse_machine: false,
        external_non_stegverse_machine_used_for_activation: false,
        github_token_runtime_authority: "NONE",
        hosted_ci_activation_authority: "NONE",
        upstream_authority_conferred: false
      };
      return putMeta(db, "service:" + SERVICE_CHAT, serviceState).then(function () {
        return appendReceipt(db, {
          schema: "stegos.web_service_activation_receipt.v1",
          service: serviceState
        });
      }).then(function (entry) {
        return { node: node, service: serviceState, entry: entry };
      });
    });
  }

  function replayJournal() {
    return openDb().then(function (db) {
      return getReceipts(db).then(function (rows) {
        var chain = Promise.resolve(null);
        rows.forEach(function (row, index) {
          chain = chain.then(function (previous) {
            if (row.sequence !== index + 1) { throw new Error("FAIL_CLOSED: receipt sequence gap"); }
            if (row.previous_entry_sha256 !== previous) { throw new Error("FAIL_CLOSED: previous-entry hash mismatch"); }
            return sha256Hex(row.receipt).then(function (receiptHash) {
              if (receiptHash !== row.receipt_sha256) { throw new Error("FAIL_CLOSED: receipt hash mismatch"); }
              var check = {
                schema: row.schema,
                sequence: row.sequence,
                previous_entry_sha256: row.previous_entry_sha256,
                receipt: row.receipt,
                receipt_sha256: row.receipt_sha256
              };
              return sha256Hex(check);
            }).then(function (entryHash) {
              if (entryHash !== row.entry_sha256) { throw new Error("FAIL_CLOSED: journal entry hash mismatch"); }
              return row.entry_sha256;
            });
          });
        });
        return chain.then(function (tail) {
          return {
            schema: "stegos.web_journal_replay_report.v1",
            state: "PASS",
            entries: rows.length,
            tail_sha256: tail,
            external_non_stegverse_machine_required: false,
            authority_effect: "NONE"
          };
        });
      });
    });
  }

  function exportEvidence() {
    return Promise.all([establishNode(), replayJournal()]).then(function (parts) {
      var state = parts[0];
      var replay = parts[1];
      return getReceipts(state.db).then(function (rows) {
        return {
          schema: "stegos.web_bootstrap_evidence_bundle.v1",
          node: state.node,
          journal_replay: replay,
          receipts: rows,
          credential_authority: CREDENTIAL_AUTHORITY,
          activation_authority_plane: AUTHORITY_PLANE,
          non_tv_tvc_secret_or_token_used: false,
          external_non_stegverse_machine_used_for_activation: false
        };
      });
    });
  }

  function registerOfflineShell() {
    if (!("serviceWorker" in navigator) || !window.isSecureContext) {
      return Promise.resolve({ state: "UNAVAILABLE", authority_effect: "NONE" });
    }
    return navigator.serviceWorker.register("./service-worker.js", { scope: "./" }).then(function (registration) {
      return { state: "REGISTERED", scope: registration.scope, authority_effect: "NONE" };
    }).catch(function (error) {
      return { state: "FAILED_NONAUTHORIZING", reason: String(error), authority_effect: "NONE" };
    });
  }

  window.StegOSWebBootstrap = {
    runtimeCapabilities: runtimeCapabilities,
    probeOperationalReadiness: probeOperationalReadiness,
    readExistingNode: readExistingNode,
    establishNode: establishNode,
    activateEcosystemChat: activateEcosystemChat,
    replayJournal: replayJournal,
    exportEvidence: exportEvidence,
    registerOfflineShell: registerOfflineShell
  };
}());
