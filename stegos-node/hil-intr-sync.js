"use strict";

(function () {
  var TARGET_URL = "./hil-intr-sync-target.json";
  var NODE_DB = "stegos-node-v1";
  var NODE_DB_VERSION = 2;
  var META = "meta";
  var NETWORK_SYNC_KEY = "stegos-network-sync";
  var LOCAL_INGRESS_KEY = "stegos-hil-local-intr-admission";
  var RECEIPT_DB = "stegos-node-hil-intr-sync-v1";
  var RECEIPT_STORE = "delivery_receipts";
  var TARGET_SCHEMA = "stegos.site.hil_intr_sync_target.v1";
  var TRIGGER_SCHEMA = "stegos.node_intr_materialization_trigger.v1";
  var OUTBOX_SCHEMA = "stegos.node_intr_outbox_entry.v1";
  var INGRESS_RECEIPT_SCHEMA = "stegverse.hil-intr-materialization-ingress/v1";

  function canonical(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]";
    return "{" + Object.keys(value).sort().map(function (key) { return JSON.stringify(key) + ":" + canonical(value[key]); }).join(",") + "}";
  }

  function bytesToHex(bytes) {
    return Array.from(bytes, function (value) { return value.toString(16).padStart(2, "0"); }).join("");
  }

  function sha256Hex(value) {
    var bytes = typeof value === "string" ? new TextEncoder().encode(value) : new TextEncoder().encode(canonical(value));
    return crypto.subtle.digest("SHA-256", bytes).then(function (digest) { return bytesToHex(new Uint8Array(digest)); });
  }

  function sha256Uri(value) { return sha256Hex(value).then(function (digest) { return "sha256:" + digest; }); }
  function isSha256Uri(value) { return /^sha256:[a-f0-9]{64}$/.test(String(value || "")); }

  function validateTarget(target) {
    if (!target || target.schema !== TARGET_SCHEMA) throw new Error("HIL InTr sync target schema mismatch");
    if (target.transport_origin !== "STEGOS_NODE_OUTBOX") throw new Error("HIL InTr sync target origin mismatch");
    if (target.credential_authority !== "TV/TVC" || target.credential_requirement !== "NONE") throw new Error("HIL InTr sync target credential boundary mismatch");
    if (target.github_token_runtime_authority !== "NONE" || target.execution_authority !== "NONE") throw new Error("HIL InTr sync target execution authority invalid");
    if (target.authority_effect !== "NONE_DISCOVERY_ONLY") throw new Error("HIL InTr sync target authority effect invalid");
    if (target.state === "AWAITING_SOVEREIGN_INTR_INGRESS") {
      if (target.ingress_url !== null || target.runtime_ingress_observed !== false) throw new Error("unavailable HIL InTr target may not expose runtime locator");
      return target;
    }
    if (target.state !== "CONFORMING_SOVEREIGN_INTR_INGRESS" || target.runtime_ingress_observed !== true) throw new Error("HIL InTr sync target state invalid");
    var parsed = new URL(String(target.ingress_url || ""), location.href);
    if (parsed.protocol !== "https:" || parsed.username || parsed.password || parsed.search || parsed.hash || !parsed.pathname.endsWith("/intr/materialization")) {
      throw new Error("HIL InTr sync target must be exact credentialless HTTPS ingress");
    }
    if (parsed.origin === "null") throw new Error("HIL InTr sync target origin invalid");
    return Object.assign({}, target, { ingress_url: parsed.href });
  }

  function validateLocalProfile(profile) {
    if (!profile || profile.schema !== "stegverse.universal-intr-profiled-ingress/v1") throw new Error("device-local HIL InTr profile schema mismatch");
    if (profile.state !== "ACTIVE_SOVEREIGN_INTR_INGRESS" || profile.protocol !== "InTr") throw new Error("device-local HIL InTr profile inactive");
    if (profile.profile_path !== "/intr/profile" || profile.materialization_path !== "/intr/materialization") throw new Error("device-local HIL InTr route mismatch");
    if (profile.runtime_surface !== "CURRENT_USER_IPHONE_SERVICE_WORKER" || profile.runtime_owner !== "REGISTERED_STEGVERSE_NODE") throw new Error("device-local HIL InTr runtime identity mismatch");
    if (profile.event_triggered !== true || profile.always_on_application_receiver_required !== false || profile.second_user_device_required !== false) throw new Error("device-local HIL InTr availability semantics mismatch");
    if (!Array.isArray(profile.supported_transport_origins) || profile.supported_transport_origins.indexOf("STEGOS_NODE_OUTBOX") === -1) throw new Error("device-local HIL Node outbox origin unavailable");
    if (!Array.isArray(profile.profiles) || profile.profiles.indexOf("HIL:Ingress") === -1) throw new Error("device-local HIL profile unavailable");
    if (profile.tls_enabled !== true || profile.credential_authority !== "TV/TVC" || profile.github_token_runtime_authority !== "NONE" || profile.execution_authority !== "NONE" || profile.authority_effect !== "NONE_DISCOVERY_EVIDENCE_ONLY") throw new Error("device-local HIL authority/TLS boundary mismatch");
    return profile;
  }

  function waitForLocalController(registration) {
    var pending = registration.installing || registration.waiting;
    if (navigator.serviceWorker.controller && !pending) return Promise.resolve(registration);
    return new Promise(function (resolve) {
      var settled = false, timer = null;
      function finish() { if (settled) return; settled = true; if (timer !== null) clearTimeout(timer); navigator.serviceWorker.removeEventListener("controllerchange", finish); resolve(registration); }
      navigator.serviceWorker.addEventListener("controllerchange", finish);
      timer = setTimeout(finish, 1800);
    });
  }

  function refreshLocalServiceWorker(registration) {
    if (!registration || typeof registration.update !== "function") return Promise.resolve(registration);
    return registration.update().catch(function () { return registration; }).then(function () { return waitForLocalController(registration); });
  }

  function loadDeviceLocalTarget() {
    if (!("serviceWorker" in navigator) || !window.isSecureContext) return Promise.reject(new Error("device-local HIL InTr service worker unavailable"));
    return navigator.serviceWorker.register("/intr-service-worker.js", { scope: "/" })
      .then(function (registration) { return navigator.serviceWorker.ready.then(function () { return refreshLocalServiceWorker(registration); }); })
      .then(function () { return fetch("/intr/profile", { method: "GET", cache: "no-store", credentials: "omit", headers: { Accept: "application/json" } }); })
      .then(function (response) { if (!response.ok) throw new Error("device-local HIL InTr profile unavailable: HTTP " + response.status); return response.json(); })
      .then(validateLocalProfile)
      .then(function (profile) {
        return validateTarget({
          schema: TARGET_SCHEMA,
          state: "CONFORMING_SOVEREIGN_INTR_INGRESS",
          ingress_url: location.origin + "/intr/materialization",
          transport_origin: "STEGOS_NODE_OUTBOX",
          runtime_ingress_observed: true,
          runtime_surface: profile.runtime_surface,
          runtime_profile_observed: true,
          device_local: true,
          configuration_authority: "authenticated device-local /intr/profile observation",
          credential_authority: "TV/TVC",
          credential_requirement: "NONE",
          github_token_runtime_authority: "NONE",
          execution_authority: "NONE",
          authority_effect: "NONE_DISCOVERY_ONLY"
        });
      });
  }

  function loadRemoteTarget() {
    return fetch(TARGET_URL, { method: "GET", cache: "no-store", credentials: "omit", headers: { Accept: "application/json" } })
      .then(function (response) { if (!response.ok) throw new Error("HIL InTr target unavailable: HTTP " + response.status); return response.json(); })
      .then(validateTarget);
  }

  function loadTarget() {
    return loadDeviceLocalTarget().catch(loadRemoteTarget);
  }

  function validateOutboxEntry(entry) {
    if (!entry || entry.schema !== OUTBOX_SCHEMA || entry.state !== "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY") throw new Error("HIL InTr outbox entry state invalid");
    if (!/^SV-NODE-[a-f0-9]{24}$/.test(String(entry.node_id || "")) || !/^SV-IL-[a-f0-9]{24}$/.test(String(entry.interlock_id || ""))) throw new Error("HIL InTr outbox Node binding invalid");
    if (entry.network_delivery_observed !== false || entry.runtime_materialization_observed !== false || entry.receiver_receipt_observed !== false || entry.tvc_receipt_observed !== false) throw new Error("HIL InTr outbox entry already promotes downstream evidence");
    if (entry.request_grants_execution_authority !== false || entry.claim_or_fence_minted !== false || entry.credential_authority !== "TV/TVC" || entry.github_token_runtime_authority !== "NONE" || entry.authority_effect !== "NONE_LOCAL_CONTINUITY_ONLY") throw new Error("HIL InTr outbox authority boundary invalid");
    if (!entry.materialization_request || entry.materialization_request.materialization_id !== entry.materialization_id || entry.materialization_request.request_hash !== entry.request_hash) throw new Error("HIL InTr outbox request binding invalid");
    var body = Object.assign({}, entry); var claimed = body.outbox_entry_hash; delete body.outbox_entry_hash;
    return sha256Uri(body).then(function (actual) { if (claimed !== actual) throw new Error("HIL InTr outbox entry hash mismatch"); return entry; });
  }

  function buildTrigger(entry) {
    return validateOutboxEntry(entry).then(function () {
      var body = {
        schema: TRIGGER_SCHEMA,
        transport_origin: "STEGOS_NODE_OUTBOX",
        node_id: entry.node_id,
        interlock_id: entry.interlock_id,
        outbox_entry_hash: entry.outbox_entry_hash,
        node_outbox_entry: entry,
        request_grants_execution_authority: false,
        claim_or_fence_minted: false,
        authority_effect: "NONE_TRIGGER_ONLY"
      };
      return sha256Uri(body).then(function (digest) { return Object.assign({}, body, { trigger_sha256: digest }); });
    });
  }

  function validateIngressReceipt(receipt, entry, triggerBodySha256, localIngress) {
    if (!receipt || receipt.schema !== INGRESS_RECEIPT_SCHEMA || receipt.state !== "INGRESS_ADMITTED") throw new Error("HIL InTr ingress receipt invalid");
    var exact = {
      materialization_id: entry.materialization_id,
      request_hash: entry.request_hash,
      transport_intent_hash: entry.transport_intent_hash,
      payload_hash: entry.payload_hash,
      transport_origin: "STEGOS_NODE_OUTBOX",
      transport_authorization_id: null,
      node_id: entry.node_id,
      interlock_id: entry.interlock_id,
      outbox_entry_hash: entry.outbox_entry_hash,
      transport_payload_sha256: triggerBodySha256,
      exact_request_validated: true,
      write_once_persisted: true,
      runtime_execution_attempted: false,
      receiver_readiness_claimed: false,
      hil_custody_claimed: false,
      claim_or_fence_minted: false,
      g18_required: false,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      authority_effect: "NONE_INGRESS_ONLY"
    };
    Object.keys(exact).forEach(function (key) { if (canonical(receipt[key]) !== canonical(exact[key])) throw new Error("HIL InTr ingress receipt binding mismatch: " + key); });
    return sha256Uri(receipt).then(function (receiptDigest) {
      return { schema: "stegos.node_intr_delivery_receipt.v1", materialization_id: entry.materialization_id, node_id: entry.node_id, interlock_id: entry.interlock_id,
        outbox_entry_hash: entry.outbox_entry_hash, ingress_receipt: receipt, ingress_receipt_sha256: receiptDigest,
        local_ingress_observed: localIngress === true, network_delivery_observed: localIngress !== true,
        runtime_materialization_observed: false, receiver_receipt_observed: false, tvc_receipt_observed: false, credential_authority: "TV/TVC", authority_effect: "NONE_OBSERVATION_ONLY" };
    });
  }

  function openReceiptDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(RECEIPT_DB, 1);
      request.onupgradeneeded = function () { var db = request.result; if (!db.objectStoreNames.contains(RECEIPT_STORE)) db.createObjectStore(RECEIPT_STORE, { keyPath: "materialization_id" }); };
      request.onsuccess = function () { resolve(request.result); }; request.onerror = function () { reject(request.error || new Error("HIL InTr delivery receipt storage unavailable")); };
    });
  }

  function getDeliveryReceipt(materializationId) {
    return openReceiptDb().then(function (db) { return new Promise(function (resolve, reject) { var tx = db.transaction(RECEIPT_STORE, "readonly"); var req = tx.objectStore(RECEIPT_STORE).get(materializationId); req.onsuccess = function () { resolve(req.result || null); }; req.onerror = function () { reject(req.error); }; tx.oncomplete = function () { db.close(); }; }); });
  }

  function putDeliveryReceipt(receipt) {
    return openReceiptDb().then(function (db) { return new Promise(function (resolve, reject) { var tx = db.transaction(RECEIPT_STORE, "readwrite"); var store = tx.objectStore(RECEIPT_STORE); var req = store.get(receipt.materialization_id); req.onsuccess = function () { if (req.result && canonical(req.result) !== canonical(receipt)) { tx.abort(); reject(new Error("HIL InTr delivery receipt write-once collision")); return; } if (!req.result) store.add(receipt); }; req.onerror = function () { reject(req.error); }; tx.oncomplete = function () { db.close(); resolve(receipt); }; tx.onabort = function () { db.close(); }; }); });
  }

  function recordNetworkSync(delivery) {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(NODE_DB, NODE_DB_VERSION);
      request.onsuccess = function () { var db = request.result; var tx = db.transaction(META, "readwrite"); var value = { schema: "stegos.node_network_sync_observation.v1", observed_at: new Date().toISOString(), materialization_id: delivery.materialization_id,
        node_id: delivery.node_id, interlock_id: delivery.interlock_id, outbox_entry_hash: delivery.outbox_entry_hash, ingress_receipt_sha256: delivery.ingress_receipt_sha256,
        network_delivery_observed: true, runtime_materialization_observed: false, receiver_receipt_observed: false, tvc_receipt_observed: false, authority_effect: "NONE_OBSERVATION_ONLY" };
        tx.objectStore(META).put({ key: NETWORK_SYNC_KEY, value: value }); tx.oncomplete = function () { db.close(); resolve(value); }; tx.onerror = function () { db.close(); reject(tx.error); }; };
      request.onerror = function () { reject(request.error || new Error("StegOS Node metadata unavailable")); };
    });
  }

  function recordLocalIngress(delivery) {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(NODE_DB, NODE_DB_VERSION);
      request.onsuccess = function () {
        var db = request.result; var tx = db.transaction(META, "readwrite");
        var value = { schema: "stegos.node_hil_local_intr_admission.v1", observed_at: new Date().toISOString(),
          materialization_id: delivery.materialization_id, node_id: delivery.node_id, interlock_id: delivery.interlock_id,
          outbox_entry_hash: delivery.outbox_entry_hash, ingress_receipt_sha256: delivery.ingress_receipt_sha256,
          local_ingress_observed: true, network_delivery_observed: false, runtime_materialization_observed: false,
          receiver_receipt_observed: false, tvc_receipt_observed: false, authority_effect: "NONE_OBSERVATION_ONLY" };
        tx.objectStore(META).put({ key: LOCAL_INGRESS_KEY, value: value });
        tx.oncomplete = function () { db.close(); resolve(value); }; tx.onerror = function () { db.close(); reject(tx.error); };
      };
      request.onerror = function () { reject(request.error || new Error("StegOS Node metadata unavailable")); };
    });
  }

  function postTrigger(target, entry) {
    return buildTrigger(entry).then(function (trigger) {
      var text = canonical(trigger);
      return sha256Hex(text).then(function (payloadSha256) {
        return fetch(target.ingress_url, { method: "POST", mode: "cors", cache: "no-store", credentials: "omit",
          headers: { "Content-Type": "application/json", "X-StegVerse-Transport": "InTr", "X-StegVerse-Transport-Origin": "STEGOS_NODE_OUTBOX", "X-StegVerse-Payload-SHA256": payloadSha256 }, body: text })
          .then(function (response) { if (response.status !== 202) throw new Error("HIL InTr ingress rejected trigger: HTTP " + response.status); return response.json(); })
          .then(function (receipt) { return validateIngressReceipt(receipt, entry, payloadSha256, target.device_local === true); })
          .then(putDeliveryReceipt).then(function (delivery) {
            var recorder = delivery.local_ingress_observed === true ? recordLocalIngress : recordNetworkSync;
            return recorder(delivery).then(function () { return delivery; });
          });
      });
    });
  }

  function synchronizePending() {
    if (!globalThis.StegOSNodeProjection || typeof globalThis.StegOSNodeProjection.getIntrOutbox !== "function") return Promise.reject(new Error("StegOS Node outbox API unavailable"));
    return Promise.all([loadTarget(), globalThis.StegOSNodeProjection.getIntrOutbox()]).then(function (values) {
      var target = values[0]; var entries = values[1].filter(function (entry) { return entry && entry.state === "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY"; });
      if (target.state !== "CONFORMING_SOVEREIGN_INTR_INGRESS") return { state: "AWAITING_SOVEREIGN_INTR_INGRESS", pending: entries.length, delivered: 0, authority_effect: "NONE" };
      return entries.reduce(function (promise, entry) {
        return promise.then(function (result) { return getDeliveryReceipt(entry.materialization_id).then(function (existing) { if (existing) { result.delivered += 1; return result; } return postTrigger(target, entry).then(function () { result.delivered += 1; return result; }); }); });
      }, Promise.resolve({ state: "SYNC_ATTEMPT_COMPLETE", pending: entries.length, delivered: 0, device_local: target.device_local === true, authority_effect: "NONE" }));
    });
  }

  function updateStatus(result) {
    var node = document.getElementById("hil-intr-outbox"); if (!node || !result) return;
    if (result.state === "AWAITING_SOVEREIGN_INTR_INGRESS") node.textContent = result.pending ? result.pending + " pending locally · sovereign ingress unavailable" : "None pending";
    else node.textContent = result.pending ? result.delivered + "/" + result.pending + " ingress admitted" + (result.device_local ? " locally" : "") : "None pending";
  }

  function attempt() { if (navigator.onLine === false) return Promise.resolve(null); return synchronizePending().then(function (result) { updateStatus(result); return result; }).catch(function (error) { var node = document.getElementById("node-error"); if (node) node.textContent = "FAIL_CLOSED: " + error.message; return null; }); }
  document.addEventListener("DOMContentLoaded", function () { setTimeout(attempt, 0); });
  window.addEventListener("online", attempt);

  globalThis.StegOSHILInTrSync = Object.freeze({ validateTarget: validateTarget, validateOutboxEntry: validateOutboxEntry, buildTrigger: buildTrigger, validateIngressReceipt: validateIngressReceipt, synchronizePending: synchronizePending, authority_effect: "NONE" });
}());
