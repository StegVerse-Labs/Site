"use strict";

(function () {
  var TARGET_URL = "/stegos-node/device-kv-intr-sync-target.json";
  var TARGET_SCHEMA = "stegos.site.device_kv_intr_sync_target.v1";
  var TRIGGER_SCHEMA = "stegos.node_intr_materialization_trigger.v1";
  var OUTBOX_SCHEMA = "stegos.node_intr_outbox_entry.v1";
  var INGRESS_RECEIPT_SCHEMA = "stegverse.device-kv-intr-materialization-ingress/v1";
  var DESTINATION = JSON.stringify({ boundary: "KV", subsystem: "KnowledgeVault:Interlock" });
  var OWNER = "StegVerse-Labs/continuity-vault-kit#79";
  var RECEIPT_DB = "stegos-node-device-kv-intr-sync-v1";
  var RECEIPT_STORE = "delivery_receipts";
  var NODE_DB = "stegos-node-v1";
  var NODE_DB_VERSION = 2;
  var META = "meta";
  var NETWORK_SYNC_KEY = "stegos-network-sync";

  function canonical(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]";
    return "{" + Object.keys(value).sort().map(function (key) { return JSON.stringify(key) + ":" + canonical(value[key]); }).join(",") + "}";
  }
  function bytesToHex(bytes) { return Array.from(bytes, function (v) { return v.toString(16).padStart(2, "0"); }).join(""); }
  function sha256Hex(value) {
    var text = typeof value === "string" ? value : canonical(value);
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(function (digest) { return bytesToHex(new Uint8Array(digest)); });
  }
  function sha256Uri(value) { return sha256Hex(value).then(function (digest) { return "sha256:" + digest; }); }

  function validateTarget(target) {
    if (!target || target.schema !== TARGET_SCHEMA) throw new Error("DEVICE_KV InTr sync target schema mismatch");
    if (target.transport_origin !== "STEGOS_NODE_OUTBOX") throw new Error("DEVICE_KV target origin mismatch");
    if (target.credential_authority !== "TV/TVC" || target.credential_requirement !== "NONE") throw new Error("DEVICE_KV target credential boundary mismatch");
    if (target.github_token_runtime_authority !== "NONE" || target.execution_authority !== "NONE" || target.authority_effect !== "NONE_DISCOVERY_ONLY") throw new Error("DEVICE_KV target authority invalid");
    if (target.state === "AWAITING_SOVEREIGN_INTR_INGRESS") {
      if (target.ingress_url !== null || target.runtime_ingress_observed !== false) throw new Error("Unavailable DEVICE_KV target may not expose runtime locator");
      return target;
    }
    if (target.state !== "CONFORMING_SOVEREIGN_INTR_INGRESS" || target.runtime_ingress_observed !== true) throw new Error("DEVICE_KV target state invalid");
    var parsed = new URL(String(target.ingress_url || ""), location.href);
    if (parsed.protocol !== "https:" || parsed.username || parsed.password || parsed.search || parsed.hash || !parsed.pathname.endsWith("/intr/materialization")) throw new Error("DEVICE_KV target must be exact credentialless HTTPS ingress");
    return Object.assign({}, target, { ingress_url: parsed.href });
  }

  function loadTarget() {
    return fetch(TARGET_URL, { method: "GET", cache: "no-store", credentials: "omit", headers: { Accept: "application/json" } })
      .then(function (response) { if (!response.ok) throw new Error("DEVICE_KV target unavailable: HTTP " + response.status); return response.json(); })
      .then(validateTarget);
  }

  function validateOutboxEntry(entry) {
    if (!entry || entry.schema !== OUTBOX_SCHEMA || entry.state !== "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY") throw new Error("DEVICE_KV outbox entry invalid");
    if (JSON.stringify(entry.destination) !== DESTINATION || entry.downstream_owner_ref !== OWNER) throw new Error("DEVICE_KV outbox destination/owner mismatch");
    if (!/^SV-NODE-[a-f0-9]{24}$/.test(String(entry.node_id || "")) || !/^SV-IL-[a-f0-9]{24}$/.test(String(entry.interlock_id || ""))) throw new Error("DEVICE_KV Node binding invalid");
    if (entry.network_delivery_observed !== false || entry.runtime_materialization_observed !== false || entry.receiver_receipt_observed !== false || entry.tvc_receipt_observed !== false) throw new Error("DEVICE_KV outbox promotes downstream evidence");
    if (entry.request_grants_execution_authority !== false || entry.claim_or_fence_minted !== false || entry.credential_authority !== "TV/TVC" || entry.github_token_runtime_authority !== "NONE" || entry.authority_effect !== "NONE_LOCAL_CONTINUITY_ONLY") throw new Error("DEVICE_KV outbox authority invalid");
    var request = entry.materialization_request;
    if (!request || request.materialization_id !== entry.materialization_id || request.request_hash !== entry.request_hash || JSON.stringify(request.destination) !== DESTINATION || request.downstream_owner_ref !== OWNER) throw new Error("DEVICE_KV request binding invalid");
    var body = Object.assign({}, entry), claimed = body.outbox_entry_hash; delete body.outbox_entry_hash;
    return sha256Uri(body).then(function (actual) { if (actual !== claimed) throw new Error("DEVICE_KV outbox hash mismatch"); return entry; });
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

  function validateIngressReceipt(receipt, entry, payloadSha256) {
    if (!receipt || receipt.schema !== INGRESS_RECEIPT_SCHEMA || receipt.state !== "INGRESS_ADMITTED") throw new Error("DEVICE_KV ingress receipt invalid");
    var expected = {
      materialization_id: entry.materialization_id,
      request_hash: entry.request_hash,
      transport_intent_hash: entry.transport_intent_hash,
      payload_hash: entry.payload_hash,
      transport_origin: "STEGOS_NODE_OUTBOX",
      transport_authorization_id: null,
      node_id: entry.node_id,
      interlock_id: entry.interlock_id,
      outbox_entry_hash: entry.outbox_entry_hash,
      transport_payload_sha256: payloadSha256,
      exact_request_validated: true,
      write_once_persisted: true,
      runtime_execution_attempted: false,
      consumer_dispatch_attempted: false,
      claim_or_fence_minted: false,
      g18_required: false,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      authority_effect: "NONE_INGRESS_ONLY"
    };
    Object.keys(expected).forEach(function (key) { if (canonical(receipt[key]) !== canonical(expected[key])) throw new Error("DEVICE_KV ingress binding mismatch: " + key); });
    var carrier = entry.materialization_request && entry.materialization_request.carrier_binding;
    if (carrier) {
      var carrierExpected = {
        carrier_binding_present: true,
        carrier_binding_validated: true,
        carrier_profile: carrier.carrier_profile,
        heartbeat_reference_epoch: carrier.heartbeat_reference.heartbeat_epoch,
        heartbeat_reference_id: carrier.heartbeat_reference.heartbeat_id,
        carrier_channel_id: carrier.channel.channel_id,
        carrier_binding_sha256: carrier.binding_sha256,
        carrier_binding_grants_authority: false
      };
      Object.keys(carrierExpected).forEach(function (key) {
        if (canonical(receipt[key]) !== canonical(carrierExpected[key])) throw new Error("DEVICE_KV carrier receipt binding mismatch: " + key);
      });
    } else {
      if (receipt.carrier_binding_present !== false || receipt.carrier_binding_validated !== false || receipt.carrier_binding_grants_authority !== false) {
        throw new Error("DEVICE_KV legacy carrier receipt boundary mismatch");
      }
    }
    return sha256Uri(receipt).then(function (digest) {
      return {
        schema: "stegos.node_intr_delivery_receipt.v1",
        materialization_id: entry.materialization_id,
        node_id: entry.node_id,
        interlock_id: entry.interlock_id,
        outbox_entry_hash: entry.outbox_entry_hash,
        ingress_receipt: receipt,
        ingress_receipt_sha256: digest,
        network_delivery_observed: true,
        runtime_materialization_observed: false,
        receiver_receipt_observed: false,
        tvc_receipt_observed: false,
        credential_authority: "TV/TVC",
        authority_effect: "NONE_OBSERVATION_ONLY"
      };
    });
  }

  function openReceiptDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(RECEIPT_DB, 1);
      request.onupgradeneeded = function () { var db = request.result; if (!db.objectStoreNames.contains(RECEIPT_STORE)) db.createObjectStore(RECEIPT_STORE, { keyPath: "materialization_id" }); };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("DEVICE_KV delivery receipt storage unavailable")); };
    });
  }
  function getDeliveryReceipt(id) {
    return openReceiptDb().then(function (db) { return new Promise(function (resolve, reject) {
      var tx = db.transaction(RECEIPT_STORE, "readonly"), req = tx.objectStore(RECEIPT_STORE).get(id);
      req.onsuccess = function () { resolve(req.result || null); }; req.onerror = function () { reject(req.error); }; tx.oncomplete = function () { db.close(); };
    }); });
  }
  function putDeliveryReceipt(receipt) {
    return openReceiptDb().then(function (db) { return new Promise(function (resolve, reject) {
      var tx = db.transaction(RECEIPT_STORE, "readwrite"), store = tx.objectStore(RECEIPT_STORE), req = store.get(receipt.materialization_id);
      req.onsuccess = function () { if (req.result && canonical(req.result) !== canonical(receipt)) { tx.abort(); reject(new Error("DEVICE_KV delivery receipt write-once collision")); return; } if (!req.result) store.add(receipt); };
      req.onerror = function () { reject(req.error); }; tx.oncomplete = function () { db.close(); resolve(receipt); }; tx.onabort = function () { db.close(); };
    }); });
  }
  function recordNetworkSync(delivery) {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(NODE_DB, NODE_DB_VERSION);
      request.onsuccess = function () {
        var db = request.result, tx = db.transaction(META, "readwrite");
        var value = {
          schema: "stegos.node_network_sync_observation.v1",
          observed_at: new Date().toISOString(),
          materialization_id: delivery.materialization_id,
          node_id: delivery.node_id,
          interlock_id: delivery.interlock_id,
          outbox_entry_hash: delivery.outbox_entry_hash,
          ingress_receipt_sha256: delivery.ingress_receipt_sha256,
          network_delivery_observed: true,
          runtime_materialization_observed: false,
          receiver_receipt_observed: false,
          tvc_receipt_observed: false,
          authority_effect: "NONE_OBSERVATION_ONLY"
        };
        tx.objectStore(META).put({ key: NETWORK_SYNC_KEY, value: value });
        tx.oncomplete = function () { db.close(); resolve(value); }; tx.onerror = function () { db.close(); reject(tx.error); };
      };
      request.onerror = function () { reject(request.error || new Error("StegOS Node metadata unavailable")); };
    });
  }

  function postTrigger(target, entry) {
    return buildTrigger(entry).then(function (trigger) {
      var text = canonical(trigger);
      return sha256Hex(text).then(function (payloadSha256) {
        return fetch(target.ingress_url, {
          method: "POST", mode: "cors", cache: "no-store", credentials: "omit",
          headers: { "Content-Type": "application/json", "X-StegVerse-Transport": "InTr", "X-StegVerse-Transport-Origin": "STEGOS_NODE_OUTBOX", "X-StegVerse-Payload-SHA256": payloadSha256 },
          body: text
        }).then(function (response) {
          if (response.status !== 202) throw new Error("DEVICE_KV ingress rejected trigger: HTTP " + response.status);
          return response.json();
        }).then(function (receipt) { return validateIngressReceipt(receipt, entry, payloadSha256); })
          .then(putDeliveryReceipt)
          .then(function (delivery) { return recordNetworkSync(delivery).then(function () { return delivery; }); });
      });
    });
  }

  function synchronizePending() {
    if (!globalThis.StegVerseNodeContinuity || typeof globalThis.StegVerseNodeContinuity.getIntrOutbox !== "function") return Promise.reject(new Error("StegVerse Node outbox API unavailable"));
    return Promise.all([loadTarget(), globalThis.StegVerseNodeContinuity.getIntrOutbox()]).then(function (values) {
      var target = values[0];
      var entries = values[1].filter(function (entry) {
        return entry && entry.state === "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY" && JSON.stringify(entry.destination) === DESTINATION && entry.downstream_owner_ref === OWNER;
      });
      if (target.state !== "CONFORMING_SOVEREIGN_INTR_INGRESS") return { state: "AWAITING_SOVEREIGN_INTR_INGRESS", pending: entries.length, delivered: 0, authority_effect: "NONE" };
      return entries.reduce(function (promise, entry) {
        return promise.then(function (result) {
          return getDeliveryReceipt(entry.materialization_id).then(function (existing) {
            if (existing) { result.delivered += 1; return result; }
            return postTrigger(target, entry).then(function () { result.delivered += 1; return result; });
          });
        });
      }, Promise.resolve({ state: "SYNC_ATTEMPT_COMPLETE", pending: entries.length, delivered: 0, authority_effect: "NONE" }));
    });
  }
  function attempt() {
    if (navigator.onLine === false) return Promise.resolve(null);
    return synchronizePending().catch(function () { return null; });
  }
  document.addEventListener("DOMContentLoaded", function () { setTimeout(attempt, 0); });
  window.addEventListener("online", attempt);
  globalThis.StegVerseDeviceKVInTrSync = Object.freeze({ validateTarget: validateTarget, validateOutboxEntry: validateOutboxEntry, buildTrigger: buildTrigger, validateIngressReceipt: validateIngressReceipt, synchronizePending: synchronizePending, attempt: attempt, authority_effect: "NONE" });
}());
