(function () {
  "use strict";

  var DB_NAME = "stegos-web-bootstrap-v1";
  var DB_VERSION = 1;
  var META_STORE = "meta";
  var RECEIPT_STORE = "receipts";
  var NODE_KEY = "node";
  var EVIDENCE_KEY = "canonical-inference-evidence";
  var SERVICE_CHAT = "stegverse.ecosystem-chat";
  var LOCAL_MODEL_SOURCE = "StegVerse-002/micro-node-runtime";
  var LOCAL_MODEL_ID = "stegverse-reference-lm-v1";
  var TVC_SOURCE = "StegVerse-Labs/TVC";
  var TVC_TASK = "TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002";
  var TVC_ROUTE_SCHEMA = "stegverse.tvc.sovereign-local-model-route-receipt.v1";
  var CREDENTIAL_AUTHORITY = "TV/TVC";

  function bytesToHex(bytes) {
    var out = "";
    for (var i = 0; i < bytes.length; i += 1) {
      out += bytes[i].toString(16).padStart(2, "0");
    }
    return out;
  }

  function canonicalize(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(canonicalize).join(",") + "]"; }
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
      var envelope = {
        schema: "stegos.web_bootstrap_journal_entry.v1",
        sequence: existing.length + 1,
        previous_entry_sha256: existing.length ? existing[existing.length - 1].entry_sha256 : null,
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

  function rejectProtectedMaterial(value, path) {
    path = path || "evidence";
    if (value === null || typeof value !== "object") { return; }
    var prohibited = [
      "token", "access_token", "github_token", "gh_token", "authorization",
      "provider_credential", "provider_credentials", "secret", "private_key"
    ];
    Object.keys(value).forEach(function (key) {
      var lowered = String(key).toLowerCase();
      if (prohibited.indexOf(lowered) !== -1) {
        throw new Error("FAIL_CLOSED: protected credential material is not admissible at " + path + "." + key);
      }
      rejectProtectedMaterial(value[key], path + "." + key);
    });
  }

  function permittedScope(scope) {
    return scope === "loopback" || scope === "private" || scope === "stegverse-local";
  }

  function normalizeTvcRoute(route) {
    if (!route || typeof route !== "object") { throw new Error("FAIL_CLOSED: TVC route evidence required"); }
    if (route.receipt && typeof route.receipt === "object") {
      var raw = route.receipt;
      if (route.canonical_owner !== TVC_SOURCE) { throw new Error("FAIL_CLOSED: TVC canonical owner mismatch"); }
      if (route.task_id !== TVC_TASK) { throw new Error("FAIL_CLOSED: TVC task mismatch"); }
      if (route.credential_authority !== CREDENTIAL_AUTHORITY) { throw new Error("FAIL_CLOSED: TVC credential authority mismatch"); }
      if (route.model_output_authority !== "NONE") { throw new Error("FAIL_CLOSED: TVC route cannot grant model-output authority"); }
      if (!permittedScope(route.endpoint_scope)) { throw new Error("FAIL_CLOSED: TVC route endpoint scope is not StegVerse-local/private/loopback"); }
      if (raw.schema_version !== TVC_ROUTE_SCHEMA) { throw new Error("FAIL_CLOSED: raw TVC route receipt schema mismatch"); }
      if (raw.state !== "ROUTE_ADMITTED") { throw new Error("FAIL_CLOSED_UNTIL_STEGVERSE_ROUTE_EVIDENCE"); }
      if (raw.route_authority !== TVC_SOURCE) { throw new Error("FAIL_CLOSED: TVC route authority mismatch"); }
      if (raw.model_id !== LOCAL_MODEL_ID) { throw new Error("FAIL_CLOSED: TVC route model identity mismatch"); }
      if (raw.credential_requirement !== "NONE") { throw new Error("FAIL_CLOSED: admitted local-model route must require no credential"); }
      if (raw.github_token_required !== false) { throw new Error("FAIL_CLOSED: TVC route requires GitHub token"); }
      if (raw.third_party_execution_platform_required !== false) { throw new Error("FAIL_CLOSED: TVC route requires third-party execution platform"); }
      if (raw.execution_authority !== false) { throw new Error("FAIL_CLOSED: TVC route cannot grant execution authority"); }
      if (raw.authority_effect !== "NONE") { throw new Error("FAIL_CLOSED: TVC route receipt has nonzero authority effect"); }
      if (!/^https?:\/\//.test(raw.endpoint || "")) { throw new Error("FAIL_CLOSED: TVC route endpoint invalid"); }
      if (!/^[0-9a-f]{64}$/.test(raw.runtime_proof_hash || "")) { throw new Error("FAIL_CLOSED: TVC runtime proof digest invalid"); }
      if (!/^[0-9a-f]{64}$/.test(raw.receipt_hash || "")) { throw new Error("FAIL_CLOSED: canonical TVC route receipt hash required"); }
      return {
        canonical_owner: route.canonical_owner,
        task_id: route.task_id,
        route_authority: raw.route_authority,
        credential_authority: route.credential_authority,
        credential_requirement: raw.credential_requirement,
        github_token_required: raw.github_token_required,
        execution_authority: raw.execution_authority,
        model_output_authority: route.model_output_authority,
        route_state: raw.state,
        endpoint: raw.endpoint,
        endpoint_scope: route.endpoint_scope,
        runtime_proof_hash: raw.runtime_proof_hash,
        route_receipt_sha256: raw.receipt_hash,
        source_schema: raw.schema_version
      };
    }

    if (route.canonical_owner !== TVC_SOURCE) { throw new Error("FAIL_CLOSED: TVC canonical owner mismatch"); }
    if (route.task_id !== TVC_TASK) { throw new Error("FAIL_CLOSED: TVC task mismatch"); }
    if (route.route_authority !== TVC_SOURCE) { throw new Error("FAIL_CLOSED: TVC route authority mismatch"); }
    if (route.credential_authority !== CREDENTIAL_AUTHORITY) { throw new Error("FAIL_CLOSED: TVC credential authority mismatch"); }
    if (route.credential_requirement !== "NONE") { throw new Error("FAIL_CLOSED: admitted local-model route must require no credential"); }
    if (route.github_token_required !== false) { throw new Error("FAIL_CLOSED: TVC route requires GitHub token"); }
    if (route.execution_authority !== false) { throw new Error("FAIL_CLOSED: TVC route cannot grant execution authority"); }
    if (route.model_output_authority !== "NONE") { throw new Error("FAIL_CLOSED: TVC route cannot grant model-output authority"); }
    if (route.route_state !== "ROUTE_ADMITTED") { throw new Error("FAIL_CLOSED_UNTIL_STEGVERSE_ROUTE_EVIDENCE"); }
    if (!permittedScope(route.endpoint_scope)) { throw new Error("FAIL_CLOSED: TVC route endpoint scope is not StegVerse-local/private/loopback"); }
    if (!/^[0-9a-f]{64}$/.test(route.route_receipt_sha256 || "")) { throw new Error("FAIL_CLOSED: TVC route receipt digest invalid"); }
    return route;
  }

  function validateCanonicalEvidence(bundle) {
    if (!bundle || typeof bundle !== "object") { throw new Error("FAIL_CLOSED: canonical evidence bundle required"); }
    rejectProtectedMaterial(bundle);
    if (bundle.schema !== "stegos.web_canonical_inference_evidence.v1") {
      throw new Error("FAIL_CLOSED: canonical inference evidence schema mismatch");
    }
    var model = bundle.model;
    if (!model || !bundle.route) { throw new Error("FAIL_CLOSED: model proof and TVC route are both required"); }
    if (model.canonical_owner !== LOCAL_MODEL_SOURCE) { throw new Error("FAIL_CLOSED: model canonical owner mismatch"); }
    if (model.model_id !== LOCAL_MODEL_ID) { throw new Error("FAIL_CLOSED: model identity mismatch"); }
    if (model.credential_authority !== CREDENTIAL_AUTHORITY) { throw new Error("FAIL_CLOSED: model credential authority mismatch"); }
    if (model.github_token_required !== false) { throw new Error("FAIL_CLOSED: model proof requires GitHub token"); }
    if (model.third_party_inference_required !== false) { throw new Error("FAIL_CLOSED: third-party inference is not admissible"); }
    if (model.model_output_authority !== "NONE") { throw new Error("FAIL_CLOSED: model output cannot carry authority"); }
    if (model.proof_valid !== true) { throw new Error("FAIL_CLOSED_UNTIL_STEGVERSE_MODEL_EVIDENCE"); }
    if (!permittedScope(model.endpoint_scope)) { throw new Error("FAIL_CLOSED: model endpoint scope is not StegVerse-local/private/loopback"); }
    if (!/^https?:\/\//.test(model.endpoint || "")) { throw new Error("FAIL_CLOSED: model endpoint must be an explicit HTTP(S) endpoint"); }
    if (!/^[0-9a-f]{64}$/.test(model.proof_sha256 || "")) { throw new Error("FAIL_CLOSED: model proof digest invalid"); }
    var route = normalizeTvcRoute(bundle.route);
    if (route.endpoint !== model.endpoint) { throw new Error("FAIL_CLOSED: TVC route endpoint does not exactly match model proof endpoint"); }
    if (route.endpoint_scope !== model.endpoint_scope) { throw new Error("FAIL_CLOSED: route/model endpoint scope mismatch"); }
    if (route.runtime_proof_hash !== model.proof_sha256) { throw new Error("FAIL_CLOSED: route does not bind exact model runtime proof"); }
    return {
      schema: bundle.schema,
      state: "ADMITTED",
      model_owner: LOCAL_MODEL_SOURCE,
      model_id: LOCAL_MODEL_ID,
      model_proof_sha256: model.proof_sha256,
      route_owner: TVC_SOURCE,
      route_task_id: TVC_TASK,
      route_receipt_sha256: route.route_receipt_sha256,
      endpoint: route.endpoint,
      endpoint_scope: route.endpoint_scope,
      credential_authority: CREDENTIAL_AUTHORITY,
      credential_requirement: "NONE",
      github_token_required: false,
      third_party_inference_required: false,
      execution_authority: false,
      model_output_authority: "NONE",
      external_non_stegverse_machine_required: false,
      upstream_authority_conferred: false,
      authority_effect: "NONE"
    };
  }

  function importCanonicalInferenceEvidence(bundle) {
    var admitted = validateCanonicalEvidence(bundle);
    return openDb().then(function (db) {
      return getMeta(db, NODE_KEY).then(function (node) {
        if (!node || !node.node_id) { throw new Error("FAIL_CLOSED: establish StegVerse node before admitting inference evidence"); }
        return sha256Hex(bundle).then(function (bundleHash) {
          admitted.source_bundle_sha256 = bundleHash;
          admitted.admitted_at = new Date().toISOString();
          admitted.node_id = node.node_id;
          return putMeta(db, EVIDENCE_KEY, admitted).then(function () {
            return appendReceipt(db, {
              schema: "stegos.web_inference_evidence_admission_receipt.v1",
              node_id: node.node_id,
              evidence: admitted,
              credential_material_retained: false,
              model_output_authority: "NONE",
              authority_effect: "NONE"
            });
          }).then(function (entry) {
            db.close();
            return { evidence: admitted, entry: entry };
          });
        });
      });
    });
  }

  function readAdmittedInferenceEvidence() {
    return openDb().then(function (db) {
      return getMeta(db, EVIDENCE_KEY).then(function (value) { db.close(); return value; });
    });
  }

  function executeAdmittedInference(prompt) {
    if (typeof prompt !== "string" || !prompt.trim()) { return Promise.reject(new Error("FAIL_CLOSED: nonempty inference prompt required")); }
    return openDb().then(function (db) {
      return Promise.all([getMeta(db, NODE_KEY), getMeta(db, EVIDENCE_KEY)]).then(function (parts) {
        var node = parts[0];
        var evidence = parts[1];
        if (!node || !node.node_id) { throw new Error("FAIL_CLOSED: StegVerse node is not established"); }
        if (!evidence || evidence.state !== "ADMITTED") { throw new Error("FAIL_CLOSED: canonical inference evidence is not admitted"); }
        var request = {
          schema: "stegos.web_admitted_inference_request.v1",
          node_id: node.node_id,
          service_id: SERVICE_CHAT,
          model_id: LOCAL_MODEL_ID,
          prompt: prompt,
          created_at: new Date().toISOString(),
          model_output_authority: "NONE",
          authority_effect: "NONE"
        };
        return sha256Hex(request).then(function (requestHash) {
          return fetch(evidence.endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "omit",
            cache: "no-store",
            body: JSON.stringify(request)
          }).then(function (response) {
            if (!response.ok) { throw new Error("FAIL_CLOSED: admitted inference endpoint returned HTTP " + response.status); }
            return response.json();
          }).then(function (result) {
            rejectProtectedMaterial(result, "inference_result");
            var usage = result.usage_proof || result.usage;
            if (!usage || usage.measured !== true || usage.model_used !== true) {
              throw new Error("FAIL_CLOSED: model usage proof missing");
            }
            if (result.model_id && result.model_id !== LOCAL_MODEL_ID) { throw new Error("FAIL_CLOSED: inference response model identity mismatch"); }
            return sha256Hex(result).then(function (responseHash) {
              var receipt = {
                schema: "stegos.web_admitted_inference_receipt.v1",
                node_id: node.node_id,
                service_id: SERVICE_CHAT,
                model_owner: LOCAL_MODEL_SOURCE,
                model_id: LOCAL_MODEL_ID,
                model_proof_sha256: evidence.model_proof_sha256,
                route_owner: TVC_SOURCE,
                route_task_id: TVC_TASK,
                route_receipt_sha256: evidence.route_receipt_sha256,
                endpoint_scope: evidence.endpoint_scope.toUpperCase().replace("-", "_"),
                request_sha256: requestHash,
                response_sha256: responseHash,
                usage_proof: usage,
                credential_authority: CREDENTIAL_AUTHORITY,
                credential_requirement: "NONE",
                github_token_required: false,
                external_non_stegverse_machine_used: false,
                model_output_authority: "NONE",
                authority_effect: "NONE",
                created_at: new Date().toISOString()
              };
              return appendReceipt(db, receipt).then(function (entry) {
                db.close();
                return { request: request, response: result, receipt: receipt, entry: entry };
              });
            });
          });
        });
      });
    });
  }

  window.StegOSAdmittedInference = {
    normalizeTvcRoute: normalizeTvcRoute,
    validateCanonicalEvidence: validateCanonicalEvidence,
    importCanonicalInferenceEvidence: importCanonicalInferenceEvidence,
    readAdmittedInferenceEvidence: readAdmittedInferenceEvidence,
    executeAdmittedInference: executeAdmittedInference
  };
}());
