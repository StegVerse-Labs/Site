"use strict";

(function (root) {
  var TARGET_URL = "/stegos-node/stegbrowser-intr-sync-target.json";
  var TARGET_SCHEMA = "stegos.site.stegbrowser_intr_sync_target.v1";
  var REQUEST_SCHEMA = "stegverse.universal-intr-materialization-request/v1";
  var TRANSPORT_SCHEMA = "stegverse.universal-intr-transport/v1";
  var TRIGGER_SCHEMA = "stegos.node_intr_materialization_trigger.v1";
  var OUTBOX_SCHEMA = "stegos.node_intr_outbox_entry.v1";
  var RECEIPT_SCHEMA = "stegverse.stegbrowser-intr-materialization-ingress/v1";
  var DESTINATION = { boundary: "STEGOS_ECOSYSTEM", subsystem: "StegBrowser:ManifestInvocation" };
  var DOWNSTREAM_OWNER = "StegVerse-Labs/.github#1952";
  var OPERATION_PREFIX = "STEGBROWSER:STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001:";

  function canonical(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]";
    return "{" + Object.keys(value).sort().map(function (key) { return JSON.stringify(key) + ":" + canonical(value[key]); }).join(",") + "}";
  }
  function bytesToHex(bytes) { return Array.from(bytes, function (value) { return value.toString(16).padStart(2, "0"); }).join(""); }
  function sha256Hex(value) {
    var text = typeof value === "string" ? value : canonical(value);
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(function (digest) { return bytesToHex(new Uint8Array(digest)); });
  }
  function sha256Uri(value) { return sha256Hex(value).then(function (digest) { return "sha256:" + digest; }); }
  function require(ok, message) { if (!ok) throw new Error(message); }

  function buildCanonicalEntry(registration, binding) {
    require(registration && binding, "StegBrowser canonical InTr registration/binding required");
    require(/^SV-NODE-[a-f0-9]{24}$/.test(String(registration.node_id || "")), "StegBrowser canonical Node id invalid");
    require(/^SV-IL-[a-f0-9]{24}$/.test(String(registration.interlock_id || "")), "StegBrowser canonical Interlock id invalid");
    require(binding.node_id === registration.node_id && binding.interlock_id === registration.interlock_id, "StegBrowser canonical binding Node/Interlock mismatch");
    var operationId = OPERATION_PREFIX + binding.invocation_request_nonce;
    return sha256Uri(binding).then(function (payloadHash) {
      var basis = {
        operation_id: operationId,
        payload_hash: payloadHash,
        source_boundary: "DEVICE_SYSTEM",
        source_subsystem: "StegBrowser:ManifestRequest",
        destination_boundary: "STEGOS_ECOSYSTEM",
        destination_subsystem: "StegBrowser:ManifestInvocation",
        boundary_path: ["DEVICE_SYSTEM", "STEGOS_ECOSYSTEM"]
      };
      return sha256Hex(basis).then(function (packetBasisHash) {
        var packetId = "INTR-" + packetBasisHash.slice(0, 24);
        var intent = {
          schema: TRANSPORT_SCHEMA,
          protocol: "InTr",
          operation_id: operationId,
          packet_id: packetId,
          payload_hash: payloadHash,
          prior_transport_receipt_hash: null,
          source: { boundary: "DEVICE_SYSTEM", subsystem: "StegBrowser:ManifestRequest" },
          destination: DESTINATION,
          boundary_path: ["DEVICE_SYSTEM", "STEGOS_ECOSYSTEM"],
          interlock_required: true,
          transport_semantics: {
            event_triggered: true,
            always_on_receiver_required: false,
            second_user_device_required: false,
            receiver_unavailable_disposition: "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
            exact_packet_transport_retry_allowed: true,
            blind_consequence_retry_allowed: false
          },
          authority: {
            authority_transfer: false,
            transport_grants_execution_authority: false,
            credential_authority: "TV/TVC"
          },
          receipt_chain: {
            required: true,
            receipt_schema: "stegverse.intr.hop_receipt/v1",
            payload_plaintext_in_receipts: false,
            prior_hash_required_after_first_hop: true
          }
        };
        return sha256Uri(intent).then(function (intentHash) {
          var identityBasis = {
            transport_intent_hash: intentHash,
            operation_id: operationId,
            packet_id: packetId,
            payload_hash: payloadHash,
            destination: DESTINATION
          };
          return sha256Hex(identityBasis).then(function (materializationBasisHash) {
            var materializationId = "INTR-MAT-" + materializationBasisHash.slice(0, 24);
            var requestBody = {
              schema: REQUEST_SCHEMA,
              materialization_id: materializationId,
              state: "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
              transport_schema: TRANSPORT_SCHEMA,
              transport_protocol: "InTr",
              transport_intent_hash: intentHash,
              operation_id: operationId,
              packet_id: packetId,
              payload_hash: payloadHash,
              payload_ref: "opaque://stegbrowser-manifest-invocation/" + payloadHash.slice(7),
              destination: DESTINATION,
              boundary_path: ["DEVICE_SYSTEM", "STEGOS_ECOSYSTEM"],
              downstream_owner_ref: DOWNSTREAM_OWNER,
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
            return sha256Uri(requestBody).then(function (requestHash) {
              var request = Object.assign({}, requestBody, { request_hash: requestHash });
              var entryBody = {
                schema: OUTBOX_SCHEMA,
                state: "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY",
                materialization_id: materializationId,
                request_hash: requestHash,
                transport_intent_hash: intentHash,
                payload_hash: payloadHash,
                binding_hash: payloadHash,
                node_id: registration.node_id,
                interlock_id: registration.interlock_id,
                destination: DESTINATION,
                downstream_owner_ref: DOWNSTREAM_OWNER,
                stegbrowser_invocation: binding,
                materialization_request: request,
                network_delivery_observed: false,
                runtime_materialization_observed: false,
                receiver_receipt_observed: false,
                tvc_receipt_observed: false,
                request_grants_execution_authority: false,
                claim_or_fence_minted: false,
                credential_authority: "TV/TVC",
                github_token_runtime_authority: "NONE",
                authority_effect: "NONE_LOCAL_CONTINUITY_ONLY"
              };
              return sha256Uri(entryBody).then(function (entryHash) {
                var entry = Object.assign({}, entryBody, { outbox_entry_hash: entryHash });
                var triggerBody = {
                  schema: TRIGGER_SCHEMA,
                  transport_origin: "STEGOS_NODE_OUTBOX",
                  node_id: registration.node_id,
                  interlock_id: registration.interlock_id,
                  outbox_entry_hash: entryHash,
                  node_outbox_entry: entry,
                  request_grants_execution_authority: false,
                  claim_or_fence_minted: false,
                  authority_effect: "NONE_TRIGGER_ONLY"
                };
                return sha256Uri(triggerBody).then(function (triggerHash) {
                  return { intent: intent, request: request, entry: entry, trigger: Object.assign({}, triggerBody, { trigger_sha256: triggerHash }) };
                });
              });
            });
          });
        });
      });
    });
  }

  function validateTarget(target) {
    require(target && target.schema === TARGET_SCHEMA, "StegBrowser InTr sync target schema mismatch");
    require(target.transport_origin === "STEGOS_NODE_OUTBOX", "StegBrowser InTr sync target origin mismatch");
    require(target.credential_authority === "TV/TVC" && target.credential_requirement === "NONE", "StegBrowser InTr sync target credential boundary mismatch");
    require(target.github_token_runtime_authority === "NONE" && target.execution_authority === "NONE" && target.authority_effect === "NONE_DISCOVERY_ONLY", "StegBrowser InTr sync target authority mismatch");
    if (target.state === "AWAITING_SOVEREIGN_INTR_INGRESS") {
      require(target.ingress_url === null && target.runtime_ingress_observed === false, "Unavailable StegBrowser target may not expose runtime locator");
      return target;
    }
    require(target.state === "CONFORMING_SOVEREIGN_INTR_INGRESS" && target.runtime_ingress_observed === true, "StegBrowser InTr sync target state invalid");
    var parsed = new URL(String(target.ingress_url || ""), location.href);
    require(parsed.protocol === "https:" && !parsed.username && !parsed.password && !parsed.search && !parsed.hash && parsed.pathname.endsWith("/intr/materialization"), "StegBrowser InTr target must be exact credentialless HTTPS ingress");
    require(parsed.origin !== location.origin, "StegBrowser sovereign target must not resolve to the device-local service-worker origin");
    return Object.assign({}, target, { ingress_url: parsed.href });
  }

  function loadTarget() {
    return fetch(TARGET_URL, { method: "GET", cache: "no-store", credentials: "omit", headers: { Accept: "application/json" } })
      .then(function (response) { if (!response.ok) throw new Error("StegBrowser InTr target unavailable: HTTP " + response.status); return response.json(); })
      .then(validateTarget);
  }

  function validateEntry(entry) {
    require(entry && entry.schema === OUTBOX_SCHEMA && entry.state === "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY", "StegBrowser InTr outbox entry invalid");
    require(canonical(entry.destination) === canonical(DESTINATION) && entry.downstream_owner_ref === DOWNSTREAM_OWNER, "StegBrowser InTr outbox destination/owner mismatch");
    require(entry.materialization_request && entry.materialization_request.request_hash === entry.request_hash && entry.materialization_request.materialization_id === entry.materialization_id, "StegBrowser InTr outbox request binding invalid");
    require(entry.request_grants_execution_authority === false && entry.claim_or_fence_minted === false && entry.credential_authority === "TV/TVC" && entry.github_token_runtime_authority === "NONE", "StegBrowser InTr outbox authority invalid");
    var body = Object.assign({}, entry), claimed = body.outbox_entry_hash; delete body.outbox_entry_hash;
    return sha256Uri(body).then(function (actual) { require(actual === claimed, "StegBrowser InTr outbox hash mismatch"); return entry; });
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

  function validateIngressReceipt(receipt, entry, payloadSha256) {
    require(receipt && receipt.schema === RECEIPT_SCHEMA && receipt.state === "INGRESS_ADMITTED", "StegBrowser sovereign ingress receipt invalid");
    var request = entry.materialization_request;
    var expected = {
      materialization_id: entry.materialization_id,
      request_hash: entry.request_hash,
      transport_intent_hash: entry.transport_intent_hash,
      payload_hash: entry.payload_hash,
      operation_id: request.operation_id,
      packet_id: request.packet_id,
      transport_origin: "STEGOS_NODE_OUTBOX",
      transport_authorization_id: null,
      node_id: entry.node_id,
      interlock_id: entry.interlock_id,
      outbox_entry_hash: entry.outbox_entry_hash,
      transport_payload_sha256: payloadSha256,
      exact_request_validated: true,
      write_once_persisted: true,
      runtime_execution_attempted: false,
      claim_or_fence_minted: false,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      authority_effect: "NONE_INGRESS_ONLY"
    };
    Object.keys(expected).forEach(function (key) { require(canonical(receipt[key]) === canonical(expected[key]), "StegBrowser sovereign ingress receipt binding mismatch: " + key); });
    return receipt;
  }

  function postEntry(entry) {
    return Promise.all([loadTarget(), buildTrigger(entry)]).then(function (values) {
      var target = values[0], trigger = values[1];
      if (target.state !== "CONFORMING_SOVEREIGN_INTR_INGRESS") {
        return { state: "AWAITING_SOVEREIGN_INTR_INGRESS", materialization_id: entry.materialization_id, request_hash: entry.request_hash, authority_effect: "NONE" };
      }
      var text = canonical(trigger);
      return sha256Hex(text).then(function (payloadSha256) {
        return fetch(target.ingress_url, {
          method: "POST", mode: "cors", cache: "no-store", credentials: "omit",
          headers: { "Content-Type": "application/json", "X-StegVerse-Transport": "InTr", "X-StegVerse-Transport-Origin": "STEGOS_NODE_OUTBOX", "X-StegVerse-Payload-SHA256": payloadSha256 },
          body: text
        }).then(function (response) {
          if (response.status !== 202) throw new Error("StegBrowser sovereign ingress rejected trigger: HTTP " + response.status);
          return response.json();
        }).then(function (receipt) { return validateIngressReceipt(receipt, entry, payloadSha256); });
      });
    });
  }

  root.StegVerseStegBrowserInTrSync = Object.freeze({
    buildCanonicalEntry: buildCanonicalEntry,
    validateTarget: validateTarget,
    validateEntry: validateEntry,
    buildTrigger: buildTrigger,
    validateIngressReceipt: validateIngressReceipt,
    postEntry: postEntry,
    authority_effect: "NONE"
  });
}(globalThis));
