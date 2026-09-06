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
  var REGISTERED_NODE_DB = "stegos-node-v1";
  var REGISTERED_NODE_DB_VERSION = 2;
  var REGISTERED_NODE_META = "meta";
  var REGISTERED_NODE_OUTBOX = "intr_outbox";
  var REGISTERED_NODE_KEY = "registration";
  var MR_SV001_SOURCE_SHA = "sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35";
  var MR_SV001_TRANSITION = "SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION";
  var MR_SV001_TASK = "MR-STEGVERSE001-BOUNDED-AUTONOMY-001";
  var MR_SV001_OWNER = "master-records/orchestration#73";
  var HB_ANCHOR_EPOCH = 32;
  var HB_ANCHOR_UNIX_MS = 1787511600000;
  var HB_PERIOD_MS = 10;
  var HB_CHANNEL_COUNT = 16;

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
  function sha256Uri(value) { return sha256Hex(value).then(function (h) { return "sha256:" + h; }); }

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

  function executePortableSv001() {
    requireLocalRuntime();
    return readExistingNode().then(function (node) {
      if (!node || !node.node_id) {
        throw new Error("FAIL_CLOSED: established StegVerse node required before SV001 execution");
      }
      return registerOfflineShell().then(function (registration) {
        if (!registration || registration.state !== "REGISTERED") {
          throw new Error("FAIL_CLOSED: StegOS service worker registration required");
        }
        return navigator.serviceWorker.ready;
      }).then(function () {
        var endpoint = new URL("./portable-workercoordinator/sv001", window.location.href).toString();
        return fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "same-origin",
          cache: "no-store",
          body: JSON.stringify({
            execution_surface: "CURRENT_USER_IPHONE",
            node_id: node.node_id,
            request_tvc_lease: true,
            credential_authority: "TV/TVC",
            github_token_runtime_authority: "NONE",
            heartbeat_granted_authority: false
          })
        });
      }).then(function (response) {
        return response.json().then(function (payload) {
          if (!response.ok || !payload || payload.state !== "COMPLETED") {
            var reason = payload && payload.reason ? payload.reason : "portable SV001 execution failed";
            throw new Error("FAIL_CLOSED: " + reason);
          }
          return payload;
        });
      });
    });
  }

  function openRegisteredNodeDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(REGISTERED_NODE_DB, REGISTERED_NODE_DB_VERSION);
      request.onupgradeneeded = function () { request.transaction.abort(); };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("registered StegVerse Node database unavailable")); };
    });
  }
  function readRegisteredNode() {
    return openRegisteredNodeDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        if (!db.objectStoreNames.contains(REGISTERED_NODE_META) || !db.objectStoreNames.contains(REGISTERED_NODE_OUTBOX)) { db.close(); reject(new Error("registered StegVerse Node stores unavailable")); return; }
        var tx = db.transaction(REGISTERED_NODE_META, "readonly");
        var req = tx.objectStore(REGISTERED_NODE_META).get(REGISTERED_NODE_KEY);
        req.onsuccess = function () { var value = req.result ? req.result.value : null; db.close(); resolve(value); };
        req.onerror = function () { var error = req.error || new Error("registered StegVerse Node read failed"); db.close(); reject(error); };
      });
    }).then(function (registration) {
      if (!registration || registration.state !== "REGISTERED" || !/^SV-NODE-[a-f0-9]{24}$/.test(String(registration.node_id || "")) || !/^SV-IL-[a-f0-9]{24}$/.test(String(registration.interlock_id || ""))) {
        throw new Error("FAIL_CLOSED: canonical registered StegVerse Node required for Master Records governance");
      }
      return registration;
    });
  }
  function putRegisteredOutboxOnce(entry) {
    return openRegisteredNodeDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(REGISTERED_NODE_OUTBOX, "readwrite");
        var store = tx.objectStore(REGISTERED_NODE_OUTBOX);
        var req = store.get(entry.materialization_id);
        req.onsuccess = function () {
          if (req.result && canonicalize(req.result) !== canonicalize(entry)) { tx.abort(); reject(new Error("FAIL_CLOSED: Node outbox write-once collision")); return; }
          if (!req.result) { store.add(entry); }
        };
        req.onerror = function () { reject(req.error || new Error("registered Node outbox read failed")); };
        tx.oncomplete = function () { db.close(); resolve(entry); };
        tx.onerror = function () { var error = tx.error || new Error("registered Node outbox write failed"); db.close(); reject(error); };
      });
    });
  }
  function encodeHeartbeatId(epoch) { return "HB-" + epoch.toString(36).toUpperCase().padStart(8, "0"); }
  function deriveHeartbeatReference() {
    var sampled = Date.now(), elapsed = sampled - HB_ANCHOR_UNIX_MS, quanta = Math.floor(elapsed / HB_PERIOD_MS), offset = elapsed % HB_PERIOD_MS, epoch = HB_ANCHOR_EPOCH + quanta;
    return { heartbeat_epoch: epoch, heartbeat_id: encodeHeartbeatId(epoch), sampled_unix_ms: sampled, phase_offset_ms: offset, reference_frequency_hz: 100, progression_dependency: "OSCILLATOR_ONLY" };
  }
  function deriveCarrierChannel(payloadHash) {
    var slot = parseInt(String(payloadHash).charAt(22), 16);
    if (!Number.isInteger(slot)) { slot = 0; }
    return { channel_id: "HB:H1:P" + slot, channel_family: "H1_PHASE_SLOTS", frequency_ratio: 1.0, phase_slot: slot, phase_slot_count: HB_CHANNEL_COUNT, phase_radians: Number((2 * Math.PI * slot / HB_CHANNEL_COUNT).toFixed(12)), amplitude_ratio: 1.0, derivation: "PAYLOAD_SHA256_FIRST64_MOD_16" };
  }
  function buildCarrierBinding(packetId, payloadHash) {
    var body = { schema: "stegverse.intr.hb-derived-carrier-binding/v1", carrier_profile: "stegverse.intr.hb-derived-carrier-profile/v1", fundamental_mode: "HB", packet_id: packetId, payload_hash: payloadHash, heartbeat_reference: deriveHeartbeatReference(), channel: deriveCarrierChannel(payloadHash), carrier_grants_admission_authority: false, carrier_grants_execution_authority: false, carrier_grants_credential_authority: false, carrier_grants_routing_authority: false, carrier_grants_transition_authority: false, carrier_grants_receiving_authority: false, credential_authority: "TV/TVC", authority_effect: "NONE_CARRIER_ONLY" };
    return sha256Uri(body).then(function (hash) { return Object.assign({}, body, { binding_sha256: hash }); });
  }
  function buildMasterRecordsSv001Trigger(cycleReceipt, registration) {
    var sourceHash = String(cycleReceipt.receipt_hash || "");
    if (sourceHash !== MR_SV001_SOURCE_SHA) { return Promise.reject(new Error("FAIL_CLOSED: exact canonical G23 SV001 source receipt required")); }
    var materializationId = "MR-SV001-CUSTODY-" + randomHex(12);
    var governance = { schema: "stegverse.master-records.sv001-custody-transition-request/v1", transition_id: MR_SV001_TRANSITION, canonical_task: MR_SV001_TASK, authority_class: "MACHINE_GOVERNED", human_approval_required: false, current_governance_required: true, prior_receipt_authorizes_transition: false, source_receipt_sha256: sourceHash, credential_authority: "TV/TVC", authority_effect: "NONE_REQUEST_ONLY" };
    return Promise.all([sha256Uri(governance), buildCarrierBinding("INTR-" + materializationId, sourceHash)]).then(function (parts) {
      var request = { schema: "stegverse.universal-intr-materialization-request/v1", state: "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION", materialization_id: materializationId, destination: { boundary: "MASTER_RECORDS", subsystem: "SV001:Custody" }, downstream_owner_ref: MR_SV001_OWNER, transport_intent_hash: parts[0], payload_hash: sourceHash, governance_request: governance, carrier_binding: parts[1], request_grants_execution_authority: false, transport_grants_execution_authority: false, claim_or_fence_minted: false, credential_authority: "TV/TVC", github_token_runtime_authority: "NONE", authority_effect: "NONE_REQUEST_ONLY" };
      return sha256Uri(request).then(function (requestHash) {
        request.request_hash = requestHash;
        var entry = { schema: "stegos.node_intr_outbox_entry.v1", state: "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY", materialization_id: materializationId, request_hash: requestHash, transport_intent_hash: request.transport_intent_hash, payload_hash: sourceHash, node_id: registration.node_id, interlock_id: registration.interlock_id, materialization_request: request, network_delivery_observed: false, runtime_materialization_observed: false, receiver_receipt_observed: false, tvc_receipt_observed: false, request_grants_execution_authority: false, claim_or_fence_minted: false, credential_authority: "TV/TVC", github_token_runtime_authority: "NONE", authority_effect: "NONE_LOCAL_CONTINUITY_ONLY" };
        return sha256Uri(entry).then(function (entryHash) {
          entry.outbox_entry_hash = entryHash;
          var trigger = { schema: "stegos.node_intr_materialization_trigger.v1", transport_origin: "STEGOS_NODE_OUTBOX", node_id: registration.node_id, interlock_id: registration.interlock_id, outbox_entry_hash: entryHash, node_outbox_entry: entry, request_grants_execution_authority: false, claim_or_fence_minted: false, authority_effect: "NONE_TRIGGER_ONLY" };
          return sha256Uri(trigger).then(function (triggerHash) { trigger.trigger_sha256 = triggerHash; return { entry: entry, trigger: trigger }; });
        });
      });
    });
  }
  function rootIntrRegistration() {
    return navigator.serviceWorker.register("/intr-service-worker.js", { scope: "/" }).then(function (registration) {
      return registration.update().catch(function () { return registration; }).then(function () {
        var active = registration.active || registration.waiting || registration.installing;
        if (!active) { throw new Error("FAIL_CLOSED: root Universal InTr service worker unavailable"); }
        return { registration: registration, active: active };
      });
    });
  }
  function sendRootIntrTrigger(active, trigger) {
    return new Promise(function (resolve, reject) {
      var channel = new MessageChannel();
      var timer = setTimeout(function () { reject(new Error("FAIL_CLOSED: root Universal InTr admission timed out")); }, 5000);
      channel.port1.onmessage = function (event) {
        clearTimeout(timer);
        var data = event.data || {};
        if (!data.ok || !data.receipt) { reject(new Error("FAIL_CLOSED: root Universal InTr denied custody: " + String(data.reason || "unknown"))); return; }
        resolve(data.receipt);
      };
      active.postMessage({ type: "STEGVERSE_INTR_LOCAL_TRIGGER", trigger: trigger }, [channel.port2]);
    });
  }
  function admitMasterRecordsSv001Custody(cycleReceipt) {
    return Promise.all([readRegisteredNode(), rootIntrRegistration()]).then(function (parts) {
      var registration = parts[0], root = parts[1];
      return buildMasterRecordsSv001Trigger(cycleReceipt, registration).then(function (built) {
        return putRegisteredOutboxOnce(built.entry).then(function () { return sendRootIntrTrigger(root.active, built.trigger); });
      });
    }).then(function (receipt) {
      if (!receipt || receipt.schema !== "stegverse.master-records.sv001-custody-intr-admission/v1" || receipt.state !== "INGRESS_ADMITTED" || receipt.governance_decision !== "ALLOW" || receipt.transition_id !== MR_SV001_TRANSITION || receipt.source_receipt_sha256 !== MR_SV001_SOURCE_SHA || receipt.current_governance_decision_observed !== true || receipt.human_approval_checkpoint_inserted !== false || receipt.prior_receipt_authorizes_transition !== false || receipt.site_custody_authority !== false || receipt.authority_effect !== "NONE_INGRESS_ONLY") {
        throw new Error("FAIL_CLOSED: root Universal InTr custody admission binding invalid");
      }
      var body = Object.assign({}, receipt), claimed = body.receipt_sha256; delete body.receipt_sha256;
      return sha256Uri(body).then(function (actual) { if (actual !== claimed) { throw new Error("FAIL_CLOSED: root Universal InTr custody admission receipt hash mismatch"); } return receipt; });
    });
  }

  function executeMasterRecordsSv001Custody(cycleReceipt) {
    requireLocalRuntime();
    if (!cycleReceipt || typeof cycleReceipt !== "object") {
      return Promise.reject(new Error("FAIL_CLOSED: exact completed SV001 cycle receipt required"));
    }
    if (cycleReceipt.transition_id !== "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED") {
      return Promise.reject(new Error("FAIL_CLOSED: completed SV001 cycle receipt required; do not rerun SV001"));
    }
    if (cycleReceipt.receipt_hash !== MR_SV001_SOURCE_SHA) {
      return Promise.reject(new Error("FAIL_CLOSED: canonical G23 SV001 cycle receipt required"));
    }
    return readExistingNode().then(function (node) {
      if (!node || !node.node_id) {
        throw new Error("FAIL_CLOSED: established StegVerse node required before Master Records custody");
      }
      return admitMasterRecordsSv001Custody(cycleReceipt).then(function (intrAdmission) {
        return registerOfflineShell().then(function (registration) {
          if (!registration || registration.state !== "REGISTERED") {
            throw new Error("FAIL_CLOSED: StegOS service worker registration required");
          }
          return navigator.serviceWorker.ready;
        }).then(function () {
          var endpoint = new URL("./master-records/sv001", window.location.href).toString();
          return fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "same-origin",
            cache: "no-store",
            body: JSON.stringify({ cycle_receipt: cycleReceipt, intr_admission_receipt: intrAdmission })
          });
        });
      });
    }).then(function (response) {
      return response.json().then(function (payload) {
        if (!response.ok || !payload || payload.state !== "PASS" || payload.reconstruction_state !== "PASS") {
          var reason = payload && payload.reason ? payload.reason : "Master Records SV001 custody failed";
          throw new Error("FAIL_CLOSED: " + reason);
        }
        return payload;
      });
    });
  }

  window.StegOSWebBootstrap = {
    runtimeCapabilities: runtimeCapabilities,
    probeOperationalReadiness: probeOperationalReadiness,
    readExistingNode: readExistingNode,
    establishNode: establishNode,
    activateEcosystemChat: activateEcosystemChat,
    executePortableSv001: executePortableSv001,
    executeMasterRecordsSv001Custody: executeMasterRecordsSv001Custody,
    replayJournal: replayJournal,
    exportEvidence: exportEvidence,
    registerOfflineShell: registerOfflineShell
  };
}());
