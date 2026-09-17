"use strict";

(function () {
  var TRIGGER_SCHEMA = "stegos.node_intr_materialization_trigger.v1";
  var OUTBOX_SCHEMA = "stegos.node_intr_outbox_entry.v1";
  var INGRESS_SCHEMA = "stegverse.mir-roundtrip-intr-materialization-ingress/v1";
  var DEST = JSON.stringify({ boundary: "STEGOS_ECOSYSTEM", subsystem: "MIR:MirrorRoundTrip" });
  var DOWNSTREAM_OWNER = "MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001";

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

  function validateEntry(entry) {
    if (!entry || entry.schema !== OUTBOX_SCHEMA || entry.state !== "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY") throw new Error("MIR InTr outbox entry invalid");
    if (JSON.stringify(entry.destination) !== DEST || entry.downstream_owner_ref !== DOWNSTREAM_OWNER) throw new Error("MIR InTr outbox destination/owner mismatch");
    if (entry.request_grants_execution_authority !== false || entry.claim_or_fence_minted !== false || entry.credential_authority !== "TV/TVC" || entry.github_token_runtime_authority !== "NONE") throw new Error("MIR InTr outbox authority invalid");
    var body = Object.assign({}, entry), claimed = body.outbox_entry_hash; delete body.outbox_entry_hash;
    return sha256Uri(body).then(function (actual) { if (actual !== claimed) throw new Error("MIR InTr outbox hash mismatch"); return entry; });
  }

  function buildTrigger(entry) {
    return validateEntry(entry).then(function () {
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

  function validateReceipt(receipt, entry, payloadSha256) {
    if (!receipt || receipt.schema !== INGRESS_SCHEMA || receipt.state !== "INGRESS_ADMITTED") throw new Error("MIR InTr ingress receipt invalid");
    var req = entry.materialization_request || {};
    var expected = {
      goal_task_id: "MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001",
      root_goal_task_id: "MIR-STEGVERSE-SEPARATION-OF-POWERS-EVIDENCE-CONTRACT-001",
      cosv_task_vector: "50000000100000",
      destination_profile: "MIR",
      mir_destination: "STEGVERSE_OWNED_MIR_MIRROR",
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
      current_device_ingress_observed: true,
      runtime_surface: "CURRENT_USER_IPHONE_SERVICE_WORKER",
      runtime_owner: "REGISTERED_STEGVERSE_NODE",
      runtime_execution_attempted: false,
      claim_or_fence_minted: false,
      request_grants_execution_authority: false,
      transport_grants_execution_authority: false,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      interlock_intr_transition_authority_preserved: true,
      second_user_operated_device_required: false,
      authority_effect: "NONE_INGRESS_ONLY"
    };
    Object.keys(expected).forEach(function (key) {
      if (canonical(receipt[key]) !== canonical(expected[key])) throw new Error("MIR InTr ingress binding mismatch: " + key);
    });
    if (req.destination_profile !== "MIR") throw new Error("MIR request profile mismatch");
    return receipt;
  }

  function postEntry(entry) {
    return buildTrigger(entry).then(function (trigger) {
      var text = canonical(trigger);
      return sha256Hex(text).then(function (payloadSha256) {
        return fetch("/intr/materialization", {
          method: "POST", cache: "no-store", credentials: "omit",
          headers: { "Content-Type": "application/json", "X-StegVerse-Transport": "InTr", "X-StegVerse-Transport-Origin": "STEGOS_NODE_OUTBOX", "X-StegVerse-Payload-SHA256": payloadSha256 },
          body: text
        }).then(function (response) {
          if (response.status !== 202) throw new Error("MIR InTr ingress rejected trigger: HTTP " + response.status);
          return response.json();
        }).then(function (receipt) { return validateReceipt(receipt, entry, payloadSha256); });
      });
    });
  }

  function synchronizeMaterialization(materializationId) {
    if (!globalThis.StegVerseNodeContinuity || typeof globalThis.StegVerseNodeContinuity.getIntrOutbox !== "function") return Promise.reject(new Error("StegVerse Node outbox API unavailable"));
    return globalThis.StegVerseNodeContinuity.getIntrOutbox().then(function (rows) {
      var entry = (rows || []).filter(function (row) { return row && row.materialization_id === materializationId; })[0];
      if (!entry) throw new Error("MIR InTr queued materialization not found");
      return postEntry(entry);
    });
  }

  globalThis.StegVerseMirRoundTripInTrSync = Object.freeze({
    validateEntry: validateEntry,
    buildTrigger: buildTrigger,
    validateReceipt: validateReceipt,
    synchronizeMaterialization: synchronizeMaterialization,
    authority_effect: "NONE_TRANSPORT_ONLY"
  });
}());
