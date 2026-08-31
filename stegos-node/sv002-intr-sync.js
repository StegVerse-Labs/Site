"use strict";

(function () {
  var TARGET_URL = "/stegos-node/sv002-intr-sync-target.json";
  var TARGET_SCHEMA = "stegos.site.sv002_intr_sync_target.v1";
  var TRIGGER_SCHEMA = "stegos.node_intr_materialization_trigger.v1";
  var OUTBOX_SCHEMA = "stegos.node_intr_outbox_entry.v1";
  var INGRESS_RECEIPT_SCHEMA = "stegverse.sv002-intr-materialization-ingress/v1";
  var DESTINATION = JSON.stringify({ boundary: "STEGOS_ECOSYSTEM", subsystem: "SV002:PublicObservation" });

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
    if (!target || target.schema !== TARGET_SCHEMA) throw new Error("SV002 InTr sync target schema mismatch");
    if (target.transport_origin !== "STEGOS_NODE_OUTBOX") throw new Error("SV002 InTr sync target origin mismatch");
    if (target.credential_authority !== "TV/TVC" || target.credential_requirement !== "NONE") throw new Error("SV002 InTr target credential boundary mismatch");
    if (target.github_token_runtime_authority !== "NONE" || target.execution_authority !== "NONE" || target.authority_effect !== "NONE_DISCOVERY_ONLY") throw new Error("SV002 InTr target authority invalid");
    if (target.state === "AWAITING_SOVEREIGN_INTR_INGRESS") {
      if (target.ingress_url !== null || target.runtime_ingress_observed !== false) throw new Error("Unavailable SV002 target may not expose runtime locator");
      return target;
    }
    if (target.state !== "CONFORMING_SOVEREIGN_INTR_INGRESS" || target.runtime_ingress_observed !== true) throw new Error("SV002 InTr target state invalid");
    var parsed = new URL(String(target.ingress_url || ""), location.href);
    if (parsed.protocol !== "https:" || parsed.username || parsed.password || parsed.search || parsed.hash || !parsed.pathname.endsWith("/intr/materialization")) throw new Error("SV002 InTr target must be exact credentialless HTTPS ingress");
    return Object.assign({}, target, { ingress_url: parsed.href });
  }

  function loadTarget() {
    return fetch(TARGET_URL, { method: "GET", cache: "no-store", credentials: "omit", headers: { Accept: "application/json" } })
      .then(function (response) { if (!response.ok) throw new Error("SV002 InTr target unavailable: HTTP " + response.status); return response.json(); })
      .then(validateTarget);
  }

  function validateOutboxEntry(entry) {
    if (!entry || entry.schema !== OUTBOX_SCHEMA || entry.state !== "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY") throw new Error("SV002 InTr outbox entry invalid");
    if (JSON.stringify(entry.destination) !== DESTINATION || entry.downstream_owner_ref !== "StegVerse-Labs/.github#493") throw new Error("SV002 InTr outbox destination/owner mismatch");
    if (entry.request_grants_execution_authority !== false || entry.claim_or_fence_minted !== false || entry.credential_authority !== "TV/TVC" || entry.github_token_runtime_authority !== "NONE") throw new Error("SV002 InTr outbox authority invalid");
    if (!entry.materialization_request || entry.materialization_request.materialization_id !== entry.materialization_id || entry.materialization_request.request_hash !== entry.request_hash) throw new Error("SV002 InTr outbox request binding invalid");
    var body = Object.assign({}, entry), claimed = body.outbox_entry_hash; delete body.outbox_entry_hash;
    return sha256Uri(body).then(function (actual) { if (actual !== claimed) throw new Error("SV002 InTr outbox hash mismatch"); return entry; });
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
    if (!receipt || receipt.schema !== INGRESS_RECEIPT_SCHEMA || receipt.state !== "INGRESS_ADMITTED") throw new Error("SV002 InTr ingress receipt invalid");
    var expected = {
      materialization_id: entry.materialization_id,
      request_hash: entry.request_hash,
      transport_intent_hash: entry.transport_intent_hash,
      payload_hash: entry.payload_hash,
      transport_origin: "STEGOS_NODE_OUTBOX",
      node_id: entry.node_id,
      interlock_id: entry.interlock_id,
      outbox_entry_hash: entry.outbox_entry_hash,
      transport_payload_sha256: payloadSha256,
      exact_request_validated: true,
      write_once_persisted: true,
      runtime_execution_attempted: false,
      receiver_readiness_claimed: false,
      round_trip_claimed: false,
      claim_or_fence_minted: false,
      g18_required: false,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      authority_effect: "NONE_INGRESS_ONLY"
    };
    Object.keys(expected).forEach(function (key) {
      if (canonical(receipt[key]) !== canonical(expected[key])) throw new Error("SV002 InTr ingress binding mismatch: " + key);
    });
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
        if (canonical(receipt[key]) !== canonical(carrierExpected[key])) throw new Error("SV002 HB carrier receipt mismatch: " + key);
      });
    } else {
      if (receipt.carrier_binding_present !== false || receipt.carrier_binding_validated !== false || receipt.carrier_binding_grants_authority !== false) {
        throw new Error("SV002 legacy carrier receipt boundary mismatch");
      }
    }
    return receipt;
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
          if (response.status !== 202) throw new Error("SV002 InTr ingress rejected trigger: HTTP " + response.status);
          return response.json();
        }).then(function (receipt) { return validateIngressReceipt(receipt, entry, payloadSha256); });
      });
    });
  }

  function synchronizePending() {
    if (!globalThis.StegVerseNodeContinuity || typeof globalThis.StegVerseNodeContinuity.getIntrOutbox !== "function") return Promise.reject(new Error("StegVerse Node outbox API unavailable"));
    return Promise.all([loadTarget(), globalThis.StegVerseNodeContinuity.getIntrOutbox()]).then(function (values) {
      var target = values[0];
      var entries = values[1].filter(function (entry) {
        return entry && entry.state === "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY" &&
          JSON.stringify(entry.destination) === DESTINATION &&
          entry.downstream_owner_ref === "StegVerse-Labs/.github#493";
      });
      if (target.state !== "CONFORMING_SOVEREIGN_INTR_INGRESS") return { state: "AWAITING_SOVEREIGN_INTR_INGRESS", pending: entries.length, delivered: 0, authority_effect: "NONE" };
      return entries.reduce(function (promise, entry) {
        return promise.then(function (result) {
          return postTrigger(target, entry).then(function () { result.delivered += 1; return result; });
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
  globalThis.StegVerseSV002InTrSync = Object.freeze({
    validateTarget: validateTarget,
    validateOutboxEntry: validateOutboxEntry,
    buildTrigger: buildTrigger,
    validateIngressReceipt: validateIngressReceipt,
    synchronizePending: synchronizePending,
    attempt: attempt,
    authority_effect: "NONE"
  });
}());
