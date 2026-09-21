"use strict";

(function (root) {
  var ROUTE_PATH = "/stegos-bootstrap/portable-workercoordinator/hil-custody-v1";
  var PROTOCOL = "HIL_BROWSER_CUSTODY_V1";
  var TASK_ID = "SHWP-HIL-SOVEREIGN-RECEIVER-001";
  var REQUEST_ID = "RESIDENT-EXEC-HIL-SOVEREIGN-RECEIVER-002";
  var LEASE_ID = "HIL-BROWSER-ESRL-7bafde4a280e847758da157e";
  var BROWSER_CONTEXT_ID = "ctx_d151139d2db1eeecb6512f5844058246";
  var NODE_ID = "stegnode-web-f24e3bfb7f5343cb37323187a88e51f3";
  var CLAIM_ID = "SHWP-SHWP-HIL-SOVEREIGN-RECEIVER-001-G25";
  var FENCING_TOKEN = 25;
  var PRIMARY_SHA256 = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462";
  var PROMPT_SHA256 = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c";
  var STAGING_DB = "stegverse-hil-v3";
  var STAGING_STORE = "response_files";
  var CUSTODY_DB = "stegos-hil-browser-custody-v1";
  var NODE_DB = "stegos-node-v1";
  var NODE_OUTBOX = "intr_outbox";
  var CUSTODY_OBJECTS = "objects";
  var CUSTODY_RECEIPTS = "receipts";
  var CANONICAL_RECEIVER_PATH = "/api/hil/submissions";

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }
  function jsonResponse(status, value) {
    return new Response(JSON.stringify(value, null, 2) + "\n", {
      status: status,
      headers: { "Content-Type": "application/json", "Cache-Control": "no-store" }
    });
  }
  function requireIntr() {
    var intr = root.StegVerseGeneratedInTr;
    if (!intr || typeof intr.buildIntent !== "function" || typeof intr.buildReceipt !== "function" ||
        typeof intr.validateComplete !== "function" || typeof intr.sha256Bytes !== "function" ||
        typeof intr.sha256Value !== "function" || typeof intr.canonical !== "function") {
      fail("canonical generated InTr connector unavailable");
    }
    if (!intr.PROFILES["hil-submission"] || !intr.PROFILES["hil-ingress-custody"] || !intr.PROFILES["hil-tvc-lifecycle"]) {
      fail("canonical downstream HIL profiles unavailable");
    }
    return intr;
  }
  function validateLease(lease) {
    if (!lease || lease.schema !== "stegverse.hil-browser-esrl-lease-open/v1" ||
        lease.state !== "LEASE_OPEN" || lease.lease_state !== "LEASE_OPEN") {
      fail("accepted ESRL LEASE_OPEN artifact required");
    }
    if (lease.task_id !== TASK_ID || lease.resident_request_id !== REQUEST_ID ||
        lease.lease_id !== LEASE_ID || lease.claim_id !== CLAIM_ID || lease.fencing_token !== FENCING_TOKEN) {
      fail("accepted ESRL lineage mismatch");
    }
    if (lease.second_claim_minted !== false || lease.credential_authority !== "TV/TVC" ||
        lease.github_token_runtime_authority !== "NONE") {
      fail("ESRL authority boundary drift");
    }
    if (lease.custody_observed !== false || lease.post_restart_exact_byte_proof_observed !== false ||
        lease.tvc_lifecycle_receipt_observed !== false || lease.broader_hil_lifecycle_complete !== false) {
      fail("ESRL predecessor must remain non-custodial");
    }
    return lease;
  }
  function openExistingDb(name) {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(name);
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error(name + " open failed")); };
      request.onblocked = function () { reject(new Error(name + " open blocked")); };
      request.onupgradeneeded = function () {
        request.transaction.abort();
        reject(new Error(name + " does not exist"));
      };
    });
  }
  function base64ToBytes(value) {
    var binary = atob(String(value || ""));
    var bytes = new Uint8Array(binary.length);
    for (var i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
    return bytes;
  }
  function readNodeContinuity(objectKey) {
    return openExistingDb(NODE_DB).then(function (db) {
      return new Promise(function (resolve, reject) {
        if (!db.objectStoreNames.contains(NODE_OUTBOX)) {
          db.close(); reject(new Error("StegOS Node HIL continuity outbox missing")); return;
        }
        var tx = db.transaction(NODE_OUTBOX, "readonly");
        var req = tx.objectStore(NODE_OUTBOX).getAll();
        req.onsuccess = function () {
          var rows = req.result || [];
          db.close();
          var expectedPayloadRef = "indexeddb://" + STAGING_DB + "/" + STAGING_STORE + "/" + encodeURIComponent(objectKey);
          var row = rows.find(function (entry) {
            var continuity = entry && entry.exact_payload_continuity;
            var request = entry && entry.materialization_request;
            return continuity && continuity.schema === "stegos.node_hil_payload_continuity/v1" &&
              continuity.custody_established === false &&
              continuity.authority_effect === "NONE_LOCAL_CONTINUITY_ONLY" &&
              request && request.payload_ref === expectedPayloadRef;
          }) || null;
          if (!row) { resolve(null); return; }
          var continuity = row.exact_payload_continuity;
          var bytes = base64ToBytes(continuity.response_bytes_base64);
          resolve({
            bytes: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
            response_sha256: continuity.response_sha256,
            provenance_manifest: continuity.provenance_manifest,
            intr_transport_intent: continuity.intr_transport_intent,
            intr_materialization_request: continuity.intr_materialization_request,
            continuity_source: "STEGOS_NODE_INTR_OUTBOX",
            custody_established: false
          });
        };
        req.onerror = function () { var error = req.error || new Error("StegOS Node HIL continuity read failed"); db.close(); reject(error); };
      });
    });
  }
  function readStaged(objectKey) {
    return openExistingDb(STAGING_DB).then(function (db) {
      return new Promise(function (resolve, reject) {
        if (!db.objectStoreNames.contains(STAGING_STORE)) {
          db.close(); reject(new Error("staged HIL response store missing")); return;
        }
        var tx = db.transaction(STAGING_STORE, "readonly");
        var req = tx.objectStore(STAGING_STORE).get(objectKey);
        req.onsuccess = function () {
          var value = req.result || null;
          db.close();
          if (value) { resolve(value); return; }
          readNodeContinuity(objectKey).then(resolve, reject);
        };
        req.onerror = function () {
          db.close();
          readNodeContinuity(objectKey).then(resolve, reject);
        };
      });
    }).catch(function () {
      return readNodeContinuity(objectKey);
    });
  }
  function openCustodyDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(CUSTODY_DB, 1);
      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(CUSTODY_OBJECTS)) { db.createObjectStore(CUSTODY_OBJECTS, { keyPath: "object_key" }); }
        if (!db.objectStoreNames.contains(CUSTODY_RECEIPTS)) { db.createObjectStore(CUSTODY_RECEIPTS, { keyPath: "object_key" }); }
      };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("custody IndexedDB open failed")); };
      request.onblocked = function () { reject(new Error("custody IndexedDB open blocked")); };
    });
  }
  function idbGet(db, storeName, key) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(storeName, "readonly");
      var req = tx.objectStore(storeName).get(key);
      req.onsuccess = function () { resolve(req.result || null); };
      req.onerror = function () { reject(req.error || new Error(storeName + " read failed")); };
    });
  }
  function idbAdd(db, storeName, value) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(storeName, "readwrite");
      var req = tx.objectStore(storeName).add(value);
      req.onerror = function () { reject(req.error || new Error(storeName + " add failed")); };
      tx.oncomplete = function () { resolve(); };
      tx.onerror = function () { reject(tx.error || new Error(storeName + " transaction failed")); };
      tx.onabort = function () { reject(tx.error || new Error(storeName + " transaction aborted")); };
    });
  }
  function bytesFromStaged(staged) {
    if (!staged || !staged.bytes) { fail("exact staged HIL bytes unavailable"); }
    if (staged.bytes instanceof ArrayBuffer) { return new Uint8Array(staged.bytes); }
    if (ArrayBuffer.isView(staged.bytes)) {
      return new Uint8Array(staged.bytes.buffer, staged.bytes.byteOffset, staged.bytes.byteLength);
    }
    fail("staged HIL bytes type invalid");
  }
  function payloadBinding(staged, intr) {
    return intr.sha256Value(staged.provenance_manifest).then(function (provenanceSha) {
      return {
        schema: "stegverse.hil.intr_payload_binding/v1",
        protocol: "HIL-PROTOCOL-v1.1",
        response_sha256: "sha256:" + staged.response_sha256,
        provenance_sha256: provenanceSha,
        primary_sha256: "sha256:" + PRIMARY_SHA256,
        prompt_sha256: "sha256:" + PROMPT_SHA256
      };
    });
  }
  function verifyStaged(objectKey, staged, intr) {
    var bytes = bytesFromStaged(staged);
    if (!/^[a-f0-9]{64}$/.test(String(staged.response_sha256 || ""))) { fail("staged response SHA-256 missing"); }
    if (!staged.provenance_manifest || !staged.intr_transport_intent || !staged.intr_materialization_request) {
      fail("complete staged HIL packet required");
    }
    if (staged.provenance_manifest.schema_version !== "HIL-RESPONSE-PROVENANCE-v1.1" ||
        staged.provenance_manifest.primary_sha256 !== PRIMARY_SHA256 ||
        staged.provenance_manifest.prompt_sha256 !== PROMPT_SHA256 ||
        staged.provenance_manifest.response_sha256 !== staged.response_sha256) {
      fail("staged provenance binding mismatch");
    }
    return intr.sha256Bytes(bytes).then(function (digest) {
      if (digest !== "sha256:" + staged.response_sha256) { fail("staged exact-byte SHA-256 mismatch"); }
      return payloadBinding(staged, intr);
    }).then(function (binding) {
      var bindingBytes = new TextEncoder().encode(intr.canonical(binding));
      var ingress = staged.intr_transport_intent;
      return intr.buildIntent("hil-submission", bindingBytes, "SUBMIT", ingress.operation_id, null).then(function (expectedIngress) {
        if (intr.canonical(expectedIngress) !== intr.canonical(ingress)) { fail("staged canonical ingress intent mismatch"); }
        var materialization = staged.intr_materialization_request;
        var expectedRef = "indexeddb://" + STAGING_DB + "/" + STAGING_STORE + "/" + encodeURIComponent(objectKey);
        if (materialization.payload_ref !== expectedRef) { fail("staged materialization payload reference mismatch"); }
        return intr.buildMaterializationRequest(
          "hil-submission", ingress, expectedRef, materialization.carrier_binding || null, null
        ).then(function (expectedMaterialization) {
          if (intr.canonical(expectedMaterialization) !== intr.canonical(materialization)) {
            fail("staged materialization request hash/binding mismatch");
          }
          return { bytes: bytes, binding: binding, bindingBytes: bindingBytes, ingress: ingress };
        });
      });
    });
  }
  function validateCanonicalReceiverReceipt(receipt, verified, intr) {
    if (!receipt || receipt.schema_version !== "HIL-RECEIVER-RECEIPT-v2") { fail("canonical machine receiver receipt required"); }
    if (!/^[a-f0-9]{64}$/.test(String(receipt.receipt_sha256 || ""))) { fail("canonical receiver receipt hash missing"); }
    if (receipt.submitted_file_sha256 !== verified.bytes_sha256_hex ||
        receipt.primary_sha256 !== PRIMARY_SHA256 ||
        receipt.prompt_sha256 !== PROMPT_SHA256) {
      fail("canonical receiver exact-byte/primary/prompt binding mismatch");
    }
    if (receipt.custody_state !== "EXACT_BYTES_PERSISTED" || receipt.registry_state !== "RECORDED") {
      fail("canonical receiver custody/readback incomplete");
    }
    if (receipt.next_required_transition !== "HIL_CUSTODY_TVC_INTERLOCK_ADMISSION" ||
        !/^sha256:[a-f0-9]{64}$/.test(String(receipt.intr_tvc_queue_hash || ""))) {
      fail("canonical receiver TVC successor binding incomplete");
    }
    var chain = receipt.intr_receipt_chain;
    if (!chain || chain.schema !== "stegverse.hil.intr_receipt_chain/v2" ||
        chain.next_required_transition !== "HIL_CUSTODY_TVC_INTERLOCK_ADMISSION") {
      fail("canonical receiver InTr chain incomplete");
    }
    if (intr.canonical(chain.ingress_transport_intent) !== intr.canonical(verified.ingress)) {
      fail("canonical receiver ingress intent diverged from staged exact packet");
    }
    var chainBody = Object.assign({}, chain);
    var claimedChainHash = chainBody.chain_hash;
    delete chainBody.chain_hash;
    return intr.sha256Value(chainBody).then(function (actualChainHash) {
      if (actualChainHash !== claimedChainHash) { fail("canonical receiver InTr chain hash mismatch"); }
      var body = Object.assign({}, receipt);
      var claimedReceiptHash = body.receipt_sha256;
      delete body.receipt_sha256;
      return intr.sha256Value(body).then(function (actualReceiptHash) {
        if (actualReceiptHash.slice(7) !== claimedReceiptHash) { fail("canonical receiver receipt self-hash mismatch"); }
        return receipt;
      });
    });
  }
  function submitToCanonicalReceiver(staged, verified, intr) {
    var form = new FormData();
    var exactBytes = verified.bytes.buffer.slice(verified.bytes.byteOffset, verified.bytes.byteOffset + verified.bytes.byteLength);
    form.append("response_pdf", new Blob([exactBytes], { type: "application/pdf" }), "hil-response.pdf");
    form.append("provenance_manifest", new Blob([intr.canonical(staged.provenance_manifest)], { type: "application/json" }), "provenance.json");
    form.append("intr_transport_intent", new Blob([intr.canonical(staged.intr_transport_intent)], { type: "application/json" }), "intr-transport.json");
    form.append("participant_identifier", "not_provided");
    form.append("publication_consent", "not_provided");
    form.append("primary_sha256", PRIMARY_SHA256);
    form.append("prompt_sha256", PROMPT_SHA256);
    form.append("model_response_declared_unedited", "false");
    form.append("participant_consent_authority_acknowledged", "false");
    return fetch(CANONICAL_RECEIVER_PATH, {
      method: "POST",
      cache: "no-store",
      credentials: "omit",
      body: form
    }).then(function (response) {
      return response.json().catch(function () { return {}; }).then(function (value) {
        if (!response.ok) { fail("canonical machine receiver rejected custody: " + String(value.detail || value.reason || response.status)); }
        return validateCanonicalReceiverReceipt(value, verified, intr);
      });
    });
  }
  function mirrorCanonicalReceiverReceipt(objectKey, lease, staged, verified, receipt, intr, observedAt) {
    var db;
    return openCustodyDb().then(function (opened) {
      db = opened;
      return idbGet(db, CUSTODY_RECEIPTS, objectKey);
    }).then(function (existingReceipt) {
      if (existingReceipt) {
        if (existingReceipt.lease_id !== lease.lease_id ||
            intr.canonical(existingReceipt.receipt) !== intr.canonical(receipt)) {
          fail("write-once canonical receiver receipt mirror collision");
        }
        db.close();
        return receipt;
      }
      return idbGet(db, CUSTODY_OBJECTS, objectKey).then(function (existingObject) {
        if (existingObject) { return existingObject; }
        var objectRecord = {
          object_key: objectKey,
          schema: "stegverse.hil.browser-custody-object/v1",
          state: "PERSISTED_PENDING_READBACK",
          lease_id: lease.lease_id,
          task_id: TASK_ID,
          claim_id: CLAIM_ID,
          fencing_token: FENCING_TOKEN,
          response_sha256: verified.bytes_sha256_hex,
          bytes: verified.bytes.buffer.slice(verified.bytes.byteOffset, verified.bytes.byteOffset + verified.bytes.byteLength),
          provenance_manifest: staged.provenance_manifest,
          persisted_at: observedAt
        };
        return idbAdd(db, CUSTODY_OBJECTS, objectRecord).then(function () {
          return idbGet(db, CUSTODY_OBJECTS, objectKey);
        });
      }).then(function (restored) {
        if (!restored || !restored.bytes ||
            restored.object_key !== objectKey ||
            restored.lease_id !== lease.lease_id ||
            restored.task_id !== TASK_ID ||
            restored.claim_id !== CLAIM_ID ||
            restored.fencing_token !== FENCING_TOKEN ||
            restored.response_sha256 !== verified.bytes_sha256_hex) {
          fail("local custody continuity mirror lineage mismatch");
        }
        return intr.sha256Bytes(new Uint8Array(restored.bytes)).then(function (hash) {
          if (hash !== "sha256:" + verified.bytes_sha256_hex) { fail("local custody continuity mirror exact-byte hash mismatch"); }
          if (intr.canonical(restored.provenance_manifest) !== intr.canonical(staged.provenance_manifest)) {
            fail("local custody continuity mirror provenance mismatch");
          }
          var envelope = {
            object_key: objectKey,
            lease_id: lease.lease_id,
            receiver_receipt_source: "MACHINE_OWNED_CANONICAL_RECEIVER",
            receipt: receipt
          };
          return idbAdd(db, CUSTODY_RECEIPTS, envelope).then(function () {
            return idbGet(db, CUSTODY_RECEIPTS, objectKey);
          }).then(function (restoredReceipt) {
            if (!restoredReceipt ||
                restoredReceipt.receiver_receipt_source !== "MACHINE_OWNED_CANONICAL_RECEIVER" ||
                intr.canonical(restoredReceipt.receipt) !== intr.canonical(receipt)) {
              fail("canonical receiver receipt mirror readback mismatch");
            }
            db.close();
            return receipt;
          });
        });
      });
    }).catch(function (error) {
      if (db) { try { db.close(); } catch (_) {} }
      throw error;
    });
  }
  function materialize(body) {
    if (!body || body.hil_custody_protocol !== PROTOCOL) {
      return Promise.reject(new Error("FAIL_CLOSED: exact HIL browser custody protocol required"));
    }
    var lease = validateLease(body.esrl_lease);
    var objectKey = String(body.response_object_key || "");
    if (!/^response:HIL-UPLOAD-[a-f0-9]{32}$/.test(objectKey)) {
      return Promise.reject(new Error("FAIL_CLOSED: exact staged HIL object key required"));
    }
    var intr = requireIntr();
    var observedAt = new Date().toISOString();
    var stagedValue;
    var verified;
    return readStaged(objectKey).then(function (staged) {
      stagedValue = staged;
      return verifyStaged(objectKey, staged, intr).then(function (value) {
        value.bytes_sha256_hex = staged.response_sha256;
        value.provenance_manifest = staged.provenance_manifest;
        verified = value;
        return submitToCanonicalReceiver(staged, verified, intr);
      });
    }).then(function (receipt) {
      return mirrorCanonicalReceiverReceipt(objectKey, lease, stagedValue, verified, receipt, intr, observedAt);
    });
  }
  function handle(request) {
    return request.json().then(materialize).then(function (value) {
      return jsonResponse(201, value);
    }).catch(function (error) {
      return jsonResponse(400, {
        schema: "stegverse.hil.browser-custody-failure/v1",
        state: "FAIL_CLOSED",
        task_id: TASK_ID,
        reason: String(error && error.message ? error.message : error),
        custody_state: "NOT_ESTABLISHED",
        tvc_admission_completed: false,
        post_restart_exact_byte_proof_observed: false,
        credential_authority: "TV/TVC",
        github_token_runtime_authority: "NONE",
        authority_effect: "NONE"
      });
    });
  }

  root.addEventListener("fetch", function (event) {
    var url = new URL(event.request.url);
    if (url.origin === root.location.origin && url.pathname === ROUTE_PATH && event.request.method === "POST") {
      event.respondWith(handle(event.request));
    }
  });

  root.StegOSHILBrowserCustody = {
    protocolVersion: PROTOCOL,
    routePath: ROUTE_PATH,
    materialize: materialize,
    handle: handle
  };
}(self));
