(function () {
  "use strict";

  var SCHEMA = "stegos.web_command.v1";
  var DB_NAME = "stegos-web-bootstrap-v1";
  var DB_VERSION = 1;
  var RECEIPT_STORE = "receipts";
  var MAX_BYTES = 32768;
  var MAX_DEPTH = 12;
  var ALLOWED = {
    "node.status": true,
    "node.establish": true,
    "chat.activate": true,
    "journal.replay": true,
    "journal.export": true,
    "evidence.admit": true,
    "evidence.status": true,
    "inference.request": true
  };
  var PROTECTED = {
    token: true,
    access_token: true,
    github_token: true,
    gh_token: true,
    authorization: true,
    provider_credential: true,
    provider_credentials: true,
    secret: true,
    private_key: true
  };

  function canonicalize(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(canonicalize).join(",") + "]"; }
    return "{" + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ":" + canonicalize(value[key]);
    }).join(",") + "}";
  }

  function bytesToHex(bytes) {
    var out = "";
    for (var i = 0; i < bytes.length; i += 1) { out += bytes[i].toString(16).padStart(2, "0"); }
    return out;
  }

  function sha256Hex(value) {
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonicalize(value))).then(function (digest) {
      return bytesToHex(new Uint8Array(digest));
    });
  }

  function depthOf(value, depth) {
    depth = depth || 0;
    if (depth > MAX_DEPTH) { throw new Error("FAIL_CLOSED: command envelope nesting exceeds limit"); }
    if (value && typeof value === "object") {
      Object.keys(value).forEach(function (key) { depthOf(value[key], depth + 1); });
    }
  }

  function rejectProtected(value, path) {
    path = path || "command";
    if (!value || typeof value !== "object") { return; }
    Object.keys(value).forEach(function (key) {
      var lowered = String(key).toLowerCase();
      if (PROTECTED[lowered]) {
        throw new Error("FAIL_CLOSED: protected credential material is not admissible at " + path + "." + key);
      }
      rejectProtected(value[key], path + "." + key);
    });
  }

  function normalize(input) {
    var envelope = typeof input === "string" ? JSON.parse(input) : input;
    if (!envelope || typeof envelope !== "object" || Array.isArray(envelope)) {
      throw new Error("FAIL_CLOSED: command envelope object required");
    }
    if (envelope.schema !== SCHEMA) { throw new Error("FAIL_CLOSED: command schema mismatch"); }
    if (!ALLOWED[envelope.command]) { throw new Error("FAIL_CLOSED_UNKNOWN_COMMAND"); }
    if (envelope.authority_effect !== undefined && envelope.authority_effect !== "NONE") {
      throw new Error("FAIL_CLOSED: command transport cannot confer authority");
    }
    depthOf(envelope, 0);
    rejectProtected(envelope);
    if (new TextEncoder().encode(canonicalize(envelope)).length > MAX_BYTES) {
      throw new Error("FAIL_CLOSED: command envelope exceeds size limit");
    }
    return envelope;
  }

  function openDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("IndexedDB open failed")); };
      request.onblocked = function () { reject(new Error("IndexedDB open blocked")); };
    });
  }

  function allReceipts(db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(RECEIPT_STORE, "readonly");
      var req = tx.objectStore(RECEIPT_STORE).getAll();
      req.onsuccess = function () { resolve((req.result || []).sort(function (a, b) { return a.sequence - b.sequence; })); };
      req.onerror = function () { reject(req.error || new Error("receipt read failed")); };
    });
  }

  function appendCommandReceipt(receipt) {
    return openDb().then(function (db) {
      return allReceipts(db).then(function (rows) {
        var entry = {
          schema: "stegos.web_bootstrap_journal_entry.v1",
          sequence: rows.length + 1,
          previous_entry_sha256: rows.length ? rows[rows.length - 1].entry_sha256 : null,
          receipt: receipt
        };
        return sha256Hex(receipt).then(function (receiptHash) {
          entry.receipt_sha256 = receiptHash;
          return sha256Hex(entry);
        }).then(function (entryHash) {
          entry.entry_sha256 = entryHash;
          return new Promise(function (resolve, reject) {
            var tx = db.transaction(RECEIPT_STORE, "readwrite");
            tx.objectStore(RECEIPT_STORE).add(entry);
            tx.oncomplete = function () { db.close(); resolve(entry); };
            tx.onerror = function () { reject(tx.error || new Error("command receipt write failed")); };
            tx.onabort = function () { reject(tx.error || new Error("command receipt write aborted")); };
          });
        });
      });
    });
  }

  function dispatch(envelope) {
    var bootstrap = window.StegOSWebBootstrap;
    var inference = window.StegOSAdmittedInference;
    var payload = envelope.payload || {};
    switch (envelope.command) {
      case "node.status":
        return bootstrap.readExistingNode().then(function (node) { return { state: node ? "ESTABLISHED" : "NOT_ESTABLISHED", node: node }; });
      case "node.establish":
        return bootstrap.establishNode().then(function (result) { return { state: "ESTABLISHED", node: result.node }; });
      case "chat.activate":
        return bootstrap.activateEcosystemChat().then(function (result) { return { state: result.service.state, service: result.service, node: result.node }; });
      case "journal.replay":
        return bootstrap.replayJournal();
      case "journal.export":
        return bootstrap.exportEvidence();
      case "evidence.admit":
        if (!payload.bundle) { return Promise.reject(new Error("FAIL_CLOSED: evidence.admit requires payload.bundle")); }
        return inference.importCanonicalInferenceEvidence(payload.bundle);
      case "evidence.status":
        return inference.readAdmittedInferenceEvidence().then(function (evidence) { return { state: evidence ? evidence.state : "NOT_ADMITTED", evidence: evidence }; });
      case "inference.request":
        if (typeof payload.prompt !== "string" || !payload.prompt.trim()) {
          return Promise.reject(new Error("FAIL_CLOSED: inference.request requires payload.prompt"));
        }
        return inference.executeAdmittedInference(payload.prompt, payload.execution_binding || null);
      default:
        return Promise.reject(new Error("FAIL_CLOSED_UNKNOWN_COMMAND"));
    }
  }

  function submit(input) {
    var envelope;
    try { envelope = normalize(input); } catch (error) { return Promise.reject(error); }
    return Promise.all([window.StegOSWebBootstrap.readExistingNode(), sha256Hex(envelope)]).then(function (parts) {
      var beforeNode = parts[0];
      var inputHash = parts[1];
      return dispatch(envelope).then(function (result) {
        var resultNode = result && result.node && result.node.node_id ? result.node : beforeNode;
        var receipt = {
          schema: "stegos.web_command_receipt.v1",
          node_id: resultNode && resultNode.node_id ? resultNode.node_id : null,
          command: envelope.command,
          canonical_input_sha256: inputHash,
          result_state: result && result.state ? result.state : "PASS",
          observed_at: new Date().toISOString(),
          credential_authority: "TV/TVC",
          non_tv_tvc_secret_or_token_used: false,
          transport_authority: "NONE",
          execution_authority_conferred: false,
          model_output_authority: "NONE",
          authority_effect: "NONE"
        };
        return appendCommandReceipt(receipt).then(function (entry) {
          return { envelope: envelope, result: result, receipt: receipt, entry: entry };
        });
      });
    });
  }

  window.StegOSCommandIngress = {
    schema: SCHEMA,
    maxBytes: MAX_BYTES,
    maxDepth: MAX_DEPTH,
    allowedCommands: Object.keys(ALLOWED),
    normalize: normalize,
    submit: submit
  };
}());
