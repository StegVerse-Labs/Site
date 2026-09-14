"use strict";

(function (root) {
  var PROFILE_ID = "ERL_ACTIVE_RESEARCH_INTR_SAME_DEVICE_V1";
  var PARENT_TASK_ID = "SS-ERL-ACTIVE-RESEARCH-INTR-RUNTIME-BINDING-001";
  var COMPONENT_TASK_ID = "SS-ERL-SAME-DEVICE-PORTABLE-EXECUTION-001";
  var COSV = "40000100100000";
  var DEVICE_KV_TASK_ID = "SHWP-DEVICE-KV-INTR-OBSERVATION-001";
  var DEVICE_KV_WORKER_ID = "device-kv-intr-observation-worker";
  var PACKAGE_URL = new URL("./workercoordinator-portable-device-kv.json", root.location.href).toString();
  var FULL_PATH = ["EXTERNAL_SYSTEM", "STEGOS_ECOSYSTEM", "DEVICE_SYSTEM", "KV"];
  var TERMINAL_PATH = ["DEVICE_SYSTEM", "KV"];
  var GROUP_ID = "ERL-RC-CYBER-SABOTAGE-LINEAGE-2026";
  var SOURCE_ID = "ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET";
  var SOURCE_URL = "https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-176a";
  var KV_DB = "stegverse-device-local-intr-v1";
  var KV_DB_VERSION = 1;
  var KV_STORE = "kv_files";
  var KV_KEY = "02_Research/ERL/ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET.envelope.json";
  var PROVIDER_PROOF = Object.freeze({
    provider_file: "google-drive:file:1KKBS1drUFVh-czLpmg5koRgDs4YMf-gG",
    size_bytes: 1015,
    sha256: "94470c58db24e544c3edfcd390cca395375a348879ec3c53451ba517ff917763"
  });

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }
  function sameArray(a, b) { return Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every(function (v, i) { return v === b[i]; }); }
  function canonical(value) { return root.StegVerseGeneratedInTr.canonical(value); }
  function sha(value) { return root.StegVerseGeneratedInTr.sha256Value(value); }
  function shaBytes(bytes) { return root.StegVerseGeneratedInTr.sha256Bytes(bytes); }
  function now() { return new Date().toISOString(); }

  function validateInput(envelope) {
    if (!envelope || envelope.schema !== "stegverse.external-resident-task-envelope/v1") { fail("resident task envelope schema mismatch"); }
    if (envelope.profile_id !== PROFILE_ID) { fail("ERL profile mismatch"); }
    if (envelope.task_id !== PARENT_TASK_ID || envelope.component_task_id !== COMPONENT_TASK_ID || envelope.cosv_task_vector !== COSV) { fail("ERL task/COSV identity mismatch"); }
    if (envelope.credential_authority !== "TV/TVC" || envelope.github_token_runtime_authority !== "NONE" || envelope.heartbeat_granted_authority !== false) { fail("ERL authority boundary drift"); }
    if (envelope.provider_operation_reexecution_authorized !== false || envelope.external_non_stegverse_machine_required !== false) { fail("ERL provider/machine boundary drift"); }
    if (Object.prototype.hasOwnProperty.call(envelope, "claim_id") || Object.prototype.hasOwnProperty.call(envelope, "fencing_token")) { fail("caller-supplied claim/fence prohibited"); }
    if (Object.prototype.hasOwnProperty.call(envelope, "device_id") || Object.prototype.hasOwnProperty.call(envelope, "node_id") || Object.prototype.hasOwnProperty.call(envelope, "execution_surface")) { fail("device identity/presence predicates prohibited"); }
  }

  function buildBinding() {
    var intr = root.StegVerseGeneratedInTr;
    if (!intr || typeof intr.buildReceipt !== "function" || typeof intr.validateComplete !== "function") { return Promise.reject(new Error("FAIL_CLOSED: canonical generated InTr connector unavailable")); }
    var acquisition = {
      schema: "stegverse.erl.active-research-acquisition-envelope/v1",
      group_id: GROUP_ID,
      source_id: SOURCE_ID,
      source_url: SOURCE_URL,
      required_storage_lane: "02_Research/ERL",
      finding_authorized: false,
      publication_authorized: false
    };
    return sha(acquisition).then(function (payloadHash) {
      return sha({ group_id: GROUP_ID, source_id: SOURCE_ID, payload_hash: payloadHash }).then(function (operationDigest) {
        var operationId = "ERL-ACTIVE-RESEARCH-" + operationDigest.slice(7, 31);
        var basis = {
          operation_id: operationId,
          payload_hash: payloadHash,
          source_boundary: "EXTERNAL_SYSTEM",
          source_subsystem: "ERL:ActiveResearchExternalSource",
          destination_boundary: "KV",
          destination_subsystem: "KnowledgeVault:ERL",
          boundary_path: FULL_PATH
        };
        return sha(basis).then(function (packetDigest) {
          var intent = {
            schema: "stegverse.universal-intr-transport/v1",
            protocol: "InTr",
            operation_id: operationId,
            packet_id: "INTR-" + packetDigest.slice(7, 31),
            payload_hash: payloadHash,
            prior_transport_receipt_hash: null,
            source: { boundary: "EXTERNAL_SYSTEM", subsystem: "ERL:ActiveResearchExternalSource" },
            destination: { boundary: "KV", subsystem: "KnowledgeVault:ERL" },
            boundary_path: FULL_PATH.slice(),
            interlock_required: true,
            transport_semantics: {
              event_triggered: true,
              always_on_receiver_required: false,
              second_user_device_required: false,
              receiver_unavailable_disposition: "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
              exact_packet_transport_retry_allowed: true,
              blind_consequence_retry_allowed: false
            },
            authority: { authority_transfer: false, transport_grants_execution_authority: false, credential_authority: "TV/TVC" },
            receipt_chain: { required: true, receipt_schema: "stegverse.intr.hop_receipt/v1", payload_plaintext_in_receipts: false, prior_hash_required_after_first_hop: true }
          };
          var payloadRef = "device-kv:" + KV_KEY;
          return sha(intent).then(function (intentHash) {
            var identity = { transport_intent_hash: intentHash, operation_id: operationId, packet_id: intent.packet_id, payload_hash: payloadHash, destination: intent.destination };
            return sha(identity).then(function (identityDigest) {
              var requestBody = {
                schema: "stegverse.universal-intr-materialization-request/v1",
                materialization_id: "INTR-MAT-" + identityDigest.slice(7, 31),
                state: "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
                transport_schema: "stegverse.universal-intr-transport/v1",
                transport_protocol: "InTr",
                transport_intent_hash: intentHash,
                operation_id: operationId,
                packet_id: intent.packet_id,
                payload_hash: payloadHash,
                payload_ref: payloadRef,
                destination: intent.destination,
                boundary_path: FULL_PATH.slice(),
                downstream_owner_ref: "StegVerse-Labs/Executive_Rhetoric_Ledger:active-research-kv-consumer",
                event_triggered: true,
                always_on_receiver_required: false,
                second_user_device_required: false,
                receiver_unavailable_disposition: "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
                exact_packet_transport_retry_allowed: true,
                blind_consequence_retry_allowed: false,
                interlock_required: true,
                request_grants_execution_authority: false,
                claim_or_fence_minted: false,
                transport_grants_execution_authority: false,
                credential_authority: "TV/TVC",
                github_token_runtime_authority: "NONE",
                authority_transfer: false,
                authority_effect: "NONE_REQUEST_ONLY"
              };
              return sha(requestBody).then(function (requestHash) {
                var request = Object.assign({}, requestBody, { request_hash: requestHash });
                var bindingBody = {
                  schema: "stegverse.erl.active-research-intr-binding/v1",
                  group_id: GROUP_ID,
                  source_id: SOURCE_ID,
                  acquisition_envelope: acquisition,
                  acquisition_envelope_sha256: payloadHash,
                  transport_intent: intent,
                  materialization_request: request,
                  expected_runtime_receipt_schema: "stegverse.intr.hop_receipt/v1",
                  expected_runtime_receipt_count: 3,
                  expected_boundary_path: FULL_PATH.slice(),
                  runtime_receipts_present: false,
                  transport_execution_claimed: false,
                  finding_authorized: false,
                  publication_authorized: false,
                  authority_effect: "NONE_REQUEST_ONLY"
                };
                return sha(bindingBody).then(function (bindingHash) { return Object.assign({}, bindingBody, { binding_hash: bindingHash }); });
              });
            });
          });
        });
      });
    });
  }

  function validateBinding(binding) {
    var intent = binding.transport_intent, request = binding.materialization_request;
    if (!binding || binding.schema !== "stegverse.erl.active-research-intr-binding/v1") { fail("ERL binding invalid"); }
    if (!intent || intent.schema !== "stegverse.universal-intr-transport/v1" || intent.protocol !== "InTr" || !sameArray(intent.boundary_path, FULL_PATH)) { fail("ERL full-path intent invalid"); }
    if (!request || !sameArray(request.boundary_path, FULL_PATH) || request.operation_id !== intent.operation_id || request.packet_id !== intent.packet_id || request.payload_hash !== intent.payload_hash) { fail("ERL materialization binding invalid"); }
    if (binding.runtime_receipts_present !== false || binding.transport_execution_claimed !== false) { fail("source binding promoted runtime evidence"); }
    return binding;
  }

  function admitUpstream(binding) {
    validateBinding(binding);
    var intr = root.StegVerseGeneratedInTr, intent = binding.transport_intent;
    return intr.buildReceipt(intent, 1, "ERL-ACTIVE-" + intent.packet_id + "-1", "resident://universal-intr-profiled-ingress", now(), null, "FORWARDED").then(function (hop1) {
      return intr.buildReceipt(intent, 2, "ERL-ACTIVE-" + intent.packet_id + "-2", "resident://device-system-materialization", now(), hop1.receipt_hash, "FORWARDED").then(function (hop2) {
        var body = {
          schema: "stegverse.universal-intr-materialization-request/v1",
          materialization_id: binding.materialization_request.materialization_id,
          state: "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
          transport_schema: "stegverse.universal-intr-transport/v1",
          transport_protocol: "InTr",
          transport_intent_hash: binding.materialization_request.transport_intent_hash,
          operation_id: intent.operation_id,
          packet_id: intent.packet_id,
          payload_hash: intent.payload_hash,
          payload_ref: binding.materialization_request.payload_ref,
          destination: { boundary: "KV", subsystem: "KnowledgeVault:Interlock" },
          boundary_path: TERMINAL_PATH.slice(),
          downstream_owner_ref: "StegVerse-Labs/continuity-vault-kit#79",
          prior_transport_receipt_hash: hop2.receipt_hash,
          erl_full_path: FULL_PATH.slice(),
          erl_upstream_receipt_hashes: [hop1.receipt_hash, hop2.receipt_hash],
          erl_transport_intent: intent,
          event_triggered: true,
          always_on_receiver_required: false,
          second_user_device_required: false,
          receiver_unavailable_disposition: "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
          exact_packet_transport_retry_allowed: true,
          blind_consequence_retry_allowed: false,
          interlock_required: true,
          request_grants_execution_authority: false,
          claim_or_fence_minted: false,
          transport_grants_execution_authority: false,
          credential_authority: "TV/TVC",
          github_token_runtime_authority: "NONE",
          authority_transfer: false,
          authority_effect: "NONE_REQUEST_ONLY"
        };
        return sha(body).then(function (requestHash) {
          return { hop_receipts: [hop1, hop2], terminal_request: Object.assign({}, body, { request_hash: requestHash }) };
        });
      });
    });
  }

  function loadPackage() {
    return caches.match(PACKAGE_URL).then(function (response) {
      if (!response) { fail("DEVICE_KV portable WorkerCoordinator package not installed"); }
      return response.json();
    });
  }

  function validatePackage(pkg) {
    if (!pkg || pkg.schema !== "stegverse.workercoordinator-portable-checkout-package/v1" || !pkg.task || pkg.task.task_id !== DEVICE_KV_TASK_ID || !pkg.worker || pkg.worker.worker_id !== DEVICE_KV_WORKER_ID) { fail("DEVICE_KV package identity mismatch"); }
    if (pkg.task.state !== "HANDOFF_READY" || pkg.credential_authority !== "TV/TVC" || pkg.github_token_runtime_authority !== "NONE" || pkg.heartbeat_grants_execution_authority !== false) { fail("DEVICE_KV package authority drift"); }
    if (pkg.external_non_stegverse_machine_required !== false || pkg.parallel_workercoordinator_claim_issuance_allowed !== false) { fail("DEVICE_KV package machine/parallel issuance drift"); }
    return pkg;
  }

  function verifyCheckout(receipt) {
    if (!receipt || receipt.schema !== "stegverse.workercoordinator-portable-checkout-receipt/v1" || receipt.task_id !== DEVICE_KV_TASK_ID || receipt.worker_id !== DEVICE_KV_WORKER_ID) { fail("DEVICE_KV checkout identity mismatch"); }
    if (!receipt.claim_id || !Number.isInteger(receipt.fencing_token) || receipt.fencing_token <= 24 || receipt.credential_authority !== "TV/TVC" || receipt.github_token_runtime_authority !== "NONE" || receipt.heartbeat_granted_authority !== false) { fail("DEVICE_KV checkout authority/fence invalid"); }
    return receipt;
  }

  function resolveCheckout(pkg) {
    if (!root.StegVersePortableWorkerCoordinator || !root.StegOSEcosystemChatServiceWorkerBridge) { return Promise.reject(new Error("FAIL_CLOSED: canonical portable WorkerCoordinator unavailable")); }
    var store = root.StegOSEcosystemChatServiceWorkerBridge.portableStateStoreForPackage(pkg);
    return store.read().then(function (state) {
      var ids = state && Array.isArray(state.checked_out_task_ids) ? state.checked_out_task_ids : [];
      if (ids.indexOf(DEVICE_KV_TASK_ID) === -1) {
        return root.StegVersePortableWorkerCoordinator.checkout(pkg, store).then(function (checkout) { return verifyCheckout(checkout.receipt); });
      }
      if (state.last_task_id !== DEVICE_KV_TASK_ID || !state.last_checkout_receipt) { fail("DEVICE_KV already checked out but retained receipt is not recoverable as current tail"); }
      return verifyCheckout(state.last_checkout_receipt);
    });
  }

  function openKv() {
    return new Promise(function (resolve, reject) {
      var req = indexedDB.open(KV_DB, KV_DB_VERSION);
      req.onupgradeneeded = function () { var db = req.result; if (!db.objectStoreNames.contains(KV_STORE)) { db.createObjectStore(KV_STORE, { keyPath: "key" }); } };
      req.onsuccess = function () { resolve(req.result); };
      req.onerror = function () { reject(req.error || new Error("DEVICE_KV store unavailable")); };
    });
  }

  function persistAndReadback(binding, terminal, checkout) {
    var raw = new TextEncoder().encode(canonical(binding.acquisition_envelope));
    return shaBytes(raw).then(function (payloadHash) {
      if (payloadHash !== binding.acquisition_envelope_sha256 || payloadHash !== terminal.payload_hash) { fail("terminal exact payload hash mismatch"); }
      return openKv().then(function (db) {
        return new Promise(function (resolve, reject) {
          var tx = db.transaction(KV_STORE, "readwrite"), store = tx.objectStore(KV_STORE), get = store.get(KV_KEY), existing = null;
          get.onerror = function () { reject(get.error || new Error("DEVICE_KV read failed")); };
          get.onsuccess = function () {
            existing = get.result || null;
            if (existing) {
              if (existing.sha256 !== payloadHash || existing.content !== canonical(binding.acquisition_envelope)) { tx.abort(); reject(new Error("FAIL_CLOSED: DEVICE_KV write-once collision")); }
              return;
            }
            store.add({
              key: KV_KEY,
              directory_id: "erl-active-research",
              canonical_path: "02_Research/ERL",
              name: SOURCE_ID + ".envelope.json",
              media_type: "application/json",
              size_bytes: raw.byteLength,
              sha256: payloadHash,
              content: canonical(binding.acquisition_envelope),
              materialization_id: terminal.materialization_id,
              operation_id: terminal.operation_id,
              packet_id: terminal.packet_id,
              workercoordinator_claim_id: checkout.claim_id,
              workercoordinator_fencing_token: checkout.fencing_token,
              credential_material_present: false,
              provider_operation_authorized: false,
              authority_effect: "NONE"
            });
          };
          tx.oncomplete = function () {
            var readTx = db.transaction(KV_STORE, "readonly"), read = readTx.objectStore(KV_STORE).get(KV_KEY);
            read.onerror = function () { db.close(); reject(read.error || new Error("DEVICE_KV exact readback failed")); };
            read.onsuccess = function () { var row = read.result; db.close(); if (!row || row.sha256 !== payloadHash || row.content !== canonical(binding.acquisition_envelope)) { reject(new Error("FAIL_CLOSED: DEVICE_KV exact readback mismatch")); return; } resolve({ row: row, sha256: payloadHash, exact_readback_verified: true }); };
          };
          tx.onerror = function () { db.close(); reject(tx.error || new Error("DEVICE_KV write failed")); };
          tx.onabort = function () { db.close(); };
        });
      });
    });
  }

  function executeErL(envelope, api) {
    validateInput(envelope);
    var binding, upstream, checkout;
    return buildBinding().then(function (value) {
      binding = validateBinding(value);
      return admitUpstream(binding);
    }).then(function (value) {
      upstream = value;
      return loadPackage().then(validatePackage).then(resolveCheckout);
    }).then(function (value) {
      checkout = value;
      return persistAndReadback(binding, upstream.terminal_request, checkout);
    }).then(function (kv) {
      return root.StegVerseGeneratedInTr.buildReceipt(binding.transport_intent, 3, "ERL-ACTIVE-" + binding.transport_intent.packet_id + "-3", "workercoordinator://" + checkout.claim_id, now(), upstream.hop_receipts[1].receipt_hash, "RECEIVED").then(function (hop3) {
        return root.StegVerseGeneratedInTr.validateComplete(binding.transport_intent, upstream.hop_receipts.concat([hop3])).then(function (complete) {
          return api.appendReceipt({
            schema: "stegverse.erl.same-device-portable-execution-receipt/v1",
            state: "ERL_TERMINAL_DEVICE_KV_OBSERVED",
            parent_task_id: PARENT_TASK_ID,
            component_task_id: COMPONENT_TASK_ID,
            cosv_task_vector: COSV,
            operation_id: binding.transport_intent.operation_id,
            packet_id: binding.transport_intent.packet_id,
            payload_hash: binding.transport_intent.payload_hash,
            materialization_id: upstream.terminal_request.materialization_id,
            hop_receipts: upstream.hop_receipts.concat([hop3]),
            terminal_receipt_hash: hop3.receipt_hash,
            complete_three_hop_chain_verified: complete.state === "TRANSPORT_COMPLETE",
            kv_key: KV_KEY,
            kv_payload_readback_sha256: kv.sha256,
            exact_payload_bytes_transported: true,
            durable_payload_readback_verified: kv.exact_readback_verified === true,
            workercoordinator_claim_id: checkout.claim_id,
            workercoordinator_fencing_token: checkout.fencing_token,
            provider_proof_binding: PROVIDER_PROOF,
            provider_operation_attempted: false,
            provider_operation_reexecution_authorized: false,
            master_records_custody_observed: false,
            master_records_reconstruction_observed: false,
            credential_authority: "TV/TVC",
            github_token_runtime_authority: "NONE",
            heartbeat_granted_authority: false,
            device_confirmation_performed: false,
            device_discovery_performed: false,
            device_presence_probe_performed: false,
            second_machine_required: false,
            authority_effect: "NONE_TRANSPORT_OBSERVATION_ONLY",
            observed_at: now()
          });
        });
      });
    }).then(function (entry) {
      return api.replayJournal().then(function (report) {
        if (!report || report.state !== "PASS") { fail("post-ERL journal replay failed"); }
        return {
          schema: "stegverse.erl.same-device-portable-execution-result/v1",
          state: "ERL_TERMINAL_DEVICE_KV_OBSERVED",
          parent_task_id: PARENT_TASK_ID,
          component_task_id: COMPONENT_TASK_ID,
          cosv_task_vector: COSV,
          evidence_entry_sha256: entry.entry_sha256,
          journal_replay_state: report.state,
          journal_replay_tail_sha256: report.tail_sha256,
          master_records_custody_observed: false,
          master_records_reconstruction_observed: false,
          provider_operation_attempted: false,
          device_confirmation_performed: false,
          device_discovery_performed: false,
          device_presence_probe_performed: false,
          authority_effect: "NONE_COMPONENT_EVIDENCE_ONLY"
        };
      });
    });
  }

  if (!root.StegOSExternalResidentTask || typeof root.StegOSExternalResidentTask.execute !== "function") { fail("existing resident-task dispatcher unavailable"); }
  var priorExecute = root.StegOSExternalResidentTask.execute;
  root.StegOSExternalResidentTask.execute = function (envelope, api) {
    if (envelope && envelope.profile_id === PROFILE_ID) { return executeErL(envelope, api); }
    return priorExecute(envelope, api);
  };
  root.StegOSExternalResidentTask.erlProfileId = PROFILE_ID;
  root.StegOSERLActiveResearchPortableExecution = { profileId: PROFILE_ID, execute: executeErL, buildBinding: buildBinding };
}(self));
