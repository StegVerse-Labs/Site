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
  var CUSTODY_OBJECTS = "objects";
  var CUSTODY_RECEIPTS = "receipts";

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
        lease.lease_id !== LEASE_ID || lease.browser_context_id !== BROWSER_CONTEXT_ID ||
        lease.node_id !== NODE_ID || lease.claim_id !== CLAIM_ID || lease.fencing_token !== FENCING_TOKEN) {
      fail("accepted ESRL lineage mismatch");
    }
    if (lease.execution_surface !== "CURRENT_USER_IPHONE" || lease.requires_other_machine !== false ||
        lease.second_claim_minted !== false || lease.credential_authority !== "TV/TVC" ||
        lease.github_token_runtime_authority !== "NONE") {
      fail("ESRL execution/authority boundary drift");
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
  function readStaged(objectKey) {
    return openExistingDb(STAGING_DB).then(function (db) {
      return new Promise(function (resolve, reject) {
        if (!db.objectStoreNames.contains(STAGING_STORE)) {
          db.close(); reject(new Error("staged HIL response store missing")); return;
        }
        var tx = db.transaction(STAGING_STORE, "readonly");
        var req = tx.objectStore(STAGING_STORE).get(objectKey);
        req.onsuccess = function () { var value = req.result || null; db.close(); resolve(value); };
        req.onerror = function () { var error = req.error || new Error("staged HIL packet read failed"); db.close(); reject(error); };
      });
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
  function buildChain(verified, intr, observedAt) {
    var ingressReceipt;
    var custodyIntent;
    var custodyReceipt;
    return intr.buildReceipt(
      verified.ingress, 1, "HIL-INTR-INGRESS-" + observedAt.replace(/[^0-9]/g, "").slice(0, 17),
      "stegverse://StegOS/HIL/Ingress/" + BROWSER_CONTEXT_ID, observedAt, null, "RECEIVED"
    ).then(function (receipt) {
      ingressReceipt = receipt;
      return intr.validateComplete(verified.ingress, [receipt]);
    }).then(function () {
      return intr.buildIntent(
        "hil-ingress-custody", verified.bindingBytes, "ACCEPT_CUSTODY",
        verified.ingress.operation_id + ":HIL_CUSTODY", ingressReceipt.receipt_hash
      );
    }).then(function (intent) {
      custodyIntent = intent;
      return intr.buildReceipt(
        intent, 1, "HIL-INTR-CUSTODY-" + observedAt.replace(/[^0-9]/g, "").slice(0, 17),
        "stegverse://StegOS/HIL/Custody/" + BROWSER_CONTEXT_ID, observedAt,
        ingressReceipt.receipt_hash, "RECEIVED"
      );
    }).then(function (receipt) {
      custodyReceipt = receipt;
      return intr.validateComplete(custodyIntent, [receipt]);
    }).then(function () {
      return intr.buildIntent(
        "hil-tvc-lifecycle", verified.bindingBytes, "ADMIT_LIFECYCLE",
        verified.ingress.operation_id + ":TVC_HIL_LIFECYCLE", custodyReceipt.receipt_hash
      );
    }).then(function (nextIntent) {
      var chainBody = {
        schema: "stegverse.hil.intr_receipt_chain/v2",
        payload_hash: verified.ingress.payload_hash,
        ingress_transport_intent: verified.ingress,
        device_stegos_ingress_receipt: ingressReceipt,
        hil_custody_transport_intent: custodyIntent,
        hil_custody_interlock_receipt: custodyReceipt,
        next_interlock_intent: nextIntent,
        next_required_transition: "HIL_CUSTODY_TVC_INTERLOCK_ADMISSION",
        authority_transfer: false
      };
      return intr.sha256Value(chainBody).then(function (chainHash) {
        return Object.assign({}, chainBody, { chain_hash: chainHash });
      });
    });
  }
  function persistAndVerify(objectKey, lease, verified, chain, intr, observedAt) {
    var db;
    return openCustodyDb().then(function (opened) {
      db = opened;
      return idbGet(db, CUSTODY_RECEIPTS, objectKey);
    }).then(function (existingReceipt) {
      if (existingReceipt) {
        if (existingReceipt.lease_id !== lease.lease_id ||
            existingReceipt.receipt.submitted_file_sha256 !== verified.bytes_sha256_hex) {
          fail("write-once custody receipt collision");
        }
        db.close();
        return { existing: true, receipt: existingReceipt.receipt };
      }
      return idbGet(db, CUSTODY_OBJECTS, objectKey).then(function (existingObject) {
        if (existingObject) { fail("partial custody object exists without qualifying receipt"); }
        return idbAdd(db, CUSTODY_OBJECTS, {
          object_key: objectKey,
          schema: "stegverse.hil.browser-custody-object/v1",
          state: "PERSISTED_PENDING_READBACK",
          lease_id: lease.lease_id,
          task_id: TASK_ID,
          claim_id: CLAIM_ID,
          fencing_token: FENCING_TOKEN,
          response_sha256: verified.bytes_sha256_hex,
          bytes: verified.bytes.buffer.slice(verified.bytes.byteOffset, verified.bytes.byteOffset + verified.bytes.byteLength),
          provenance_manifest: verified.provenance_manifest,
          intr_receipt_chain: chain,
          persisted_at: observedAt
        });
      }).then(function () {
        return idbGet(db, CUSTODY_OBJECTS, objectKey);
      }).then(function (restored) {
        if (!restored || !restored.bytes) { fail("custody exact-byte readback missing"); }
        return intr.sha256Bytes(new Uint8Array(restored.bytes)).then(function (hash) {
          if (hash !== "sha256:" + verified.bytes_sha256_hex) { fail("custody exact-byte readback hash mismatch"); }
          if (intr.canonical(restored.provenance_manifest) !== intr.canonical(verified.provenance_manifest) ||
              intr.canonical(restored.intr_receipt_chain) !== intr.canonical(chain)) {
            fail("custody metadata readback mismatch");
          }
          return intr.sha256Value({
            schema: "stegverse.hil.tvc_interlock_queue/v1",
            state: "READY_FOR_INTERLOCK_ADMISSION",
            payload_hash: verified.ingress.payload_hash,
            prior_receipt_hash: chain.hil_custody_interlock_receipt.receipt_hash,
            transport_intent: chain.next_interlock_intent,
            authority_transfer: false,
            tvc_admission_completed: false,
            blind_consequence_retry_allowed: false
          });
        });
      }).then(function (queueHash) {
        return intr.sha256Value({
          task_id: TASK_ID,
          lease_id: lease.lease_id,
          object_key: objectKey,
          response_sha256: verified.bytes_sha256_hex
        }).then(function (identityHash) {
          var receiptCore = {
            schema_version: "HIL-RECEIVER-RECEIPT-v2",
            receipt_id: "HIL-BROWSER-RECEIPT-" + identityHash.slice(7, 23).toUpperCase(),
            submission_id: "HIL-BROWSER-SUBMISSION-" + identityHash.slice(7, 23).toUpperCase(),
            received_at: observedAt,
            submitted_file_sha256: verified.bytes_sha256_hex,
            primary_sha256: PRIMARY_SHA256,
            prompt_sha256: PROMPT_SHA256,
            chain_validation_state: "PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED",
            custody_state: "EXACT_BYTES_PERSISTED",
            custody_backend: "same-device-indexeddb-v1",
            registry_state: "RECORDED",
            review_state: "PENDING",
            publication_state: "NOT_AUTHORIZED",
            task_id: TASK_ID,
            resident_request_id: REQUEST_ID,
            lease_id: lease.lease_id,
            browser_context_id: BROWSER_CONTEXT_ID,
            node_id: NODE_ID,
            claim_id: CLAIM_ID,
            fencing_token: FENCING_TOKEN,
            execution_surface: "CURRENT_USER_IPHONE",
            intr_receipt_chain: chain,
            intr_tvc_queue_hash: queueHash,
            next_required_transition: "HIL_CUSTODY_TVC_INTERLOCK_ADMISSION",
            tvc_admission_completed: false,
            post_restart_exact_byte_proof_observed: false,
            broader_hil_lifecycle_complete: false,
            credential_authority: "TV/TVC",
            github_token_runtime_authority: "NONE",
            requires_other_machine: false,
            second_claim_minted: false,
            authority: {
              execution: false,
              lifecycle_admission: false,
              review: false,
              publication: false,
              master_record_append: false
            }
          };
          return intr.sha256Value(receiptCore).then(function (receiptHash) {
            var receipt = Object.assign({}, receiptCore, { receipt_sha256: receiptHash });
            var envelope = { object_key: objectKey, lease_id: lease.lease_id, receipt: receipt };
            return idbAdd(db, CUSTODY_RECEIPTS, envelope).then(function () {
              return idbGet(db, CUSTODY_RECEIPTS, objectKey);
            }).then(function (restoredReceipt) {
              if (!restoredReceipt || intr.canonical(restoredReceipt.receipt) !== intr.canonical(receipt)) {
                fail("custody registry receipt readback mismatch");
              }
              db.close();
              return { existing: false, receipt: receipt };
            });
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
    var verified;
    return readStaged(objectKey).then(function (staged) {
      return verifyStaged(objectKey, staged, intr).then(function (value) {
        value.bytes_sha256_hex = staged.response_sha256;
        value.provenance_manifest = staged.provenance_manifest;
        verified = value;
        return buildChain(value, intr, observedAt);
      });
    }).then(function (chain) {
      return persistAndVerify(objectKey, lease, verified, chain, intr, observedAt);
    }).then(function (result) {
      return result.receipt;
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
