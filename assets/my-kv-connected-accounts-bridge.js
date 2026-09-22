/*
 * StegVerseKVAccountObservationBridge
 *
 * my-kv-connected-accounts.html consumes this global; nothing defined it, so
 * the Connected Accounts page always took its fail-closed branch. This is
 * remaining-work item 1 of
 * StegVerse-Labs/.github/docs/SKAP_AUTHENTIC_ACCOUNT_METADATA_POPULATION_MIRROR_HANDOFF.md.
 *
 * Two methods, matching the contract asserted in assets/my-kv-connected-accounts.js:
 *
 *   listObservedAccounts(request)          -> {accounts: [...]}
 *   populateSelectedAccountMetadata(req)   -> {accepted: true, ...}
 *
 * Observations are never invented here. They are read from the owner's own
 * device-local KnowledgeVault over the existing `device-kv` profile, exactly
 * as assets/my-kv-personal-profile-write-bridge.js reads the personal profile.
 * Population dispatches the canonical `kv-skap-account-metadata` profile
 * (StegOS specs/universal-intr-connector-profiles.v1.json) and refuses to
 * report success without an exact TVC SKAP receipt.
 *
 * This bridge mints no authority. It does not create SKAP account state; it
 * carries an owner-selected, non-secret transfer to the boundary that does,
 * and fails closed everywhere the runtime is absent.
 */
(function (root) {
  "use strict";
  if (!root || root.StegVerseKVAccountObservationBridge) return;

  var OBSERVATION_RECORD_CLASS = "CONNECTED_ACCOUNT_OBSERVATIONS";
  var OBSERVATION_DEST = "_System/Connections/Connected_Accounts.json";
  var TRANSFER_SCHEMA = "stegverse.kv-skap.account-metadata-transfer/v1";
  var ENVELOPE_SCHEMA = "stegverse.intr.boundary-transfer/v1";
  var PROFILE = "kv-skap-account-metadata";
  var OPERATION = "SKAP_ACCOUNT_METADATA_ADMIT";
  var SKAP_RECEIPT_SCHEMA = "stegverse.skap.account-metadata-admission-receipt/v1";

  function requireValue(ok, msg) { if (!ok) throw new Error("FAIL_CLOSED: " + msg); }

  function intr() {
    var api = root.StegVerseGeneratedInTr;
    requireValue(api && typeof api.buildIntent === "function" &&
      typeof api.buildMaterializationRequest === "function",
      "generated InTr connector unavailable");
    requireValue(api.PROFILES && api.PROFILES[PROFILE],
      "generated connector does not carry the " + PROFILE + " profile");
    return api;
  }

  function canon(value) { return intr().canonical(value); }

  function randomId(prefix) {
    var b = new Uint8Array(16);
    crypto.getRandomValues(b);
    return prefix + Array.from(b, function (x) { return x.toString(16).padStart(2, "0"); }).join("");
  }

  function utf8(text) { return new TextEncoder().encode(text); }

  function sha256Value(value) { return intr().sha256Value(value); }

  /* ---- node binding -------------------------------------------------- */

  function registeredNode() {
    var node = root.StegVerseNodeContinuity;
    requireValue(node && typeof node.status === "function" &&
      typeof node.queueIntrMaterializationRequest === "function",
      "registered Node continuity unavailable");
    return node.status().then(function (s) {
      requireValue(s && s.registered === true && s.registration && s.registration.node_id,
        "Register this device before managing Connected Accounts");
      return { node: node, registration: s.registration };
    });
  }

  /* ---- observation read ---------------------------------------------- */

  function buildObservationRequest(nodeId) {
    return {
      schema_version: "kv.interlock.request.v1",
      operation: "REQUEST",
      request_id: randomId("SITE-CONNECTED-ACCOUNTS-"),
      requester: { module: "Site", component: "MyKVConnectedAccounts" },
      purpose: "Read the owner's bounded connected-account observations from this KnowledgeVault.",
      record_class: OBSERVATION_RECORD_CLASS,
      requested_scope: ["connected_account_observations"],
      minimum_necessary_justification:
        "Load only bounded non-secret provider-account observations needed to let the owner choose which accounts to admit. Credentials and raw provider identifiers are prohibited.",
      authority_ref: "stegos-node://" + nodeId,
      disclosure_mode: "BOUNDED_CONTEXT"
    };
  }

  function listObservedAccounts(request) {
    try { return listObservedAccountsInner(request); }
    catch (err) { return Promise.reject(err); }
  }

  function listObservedAccountsInner(request) {
    var accounts = root.StegVerseMyKVConnectedAccounts;
    requireValue(accounts && typeof accounts.assertBounded === "function",
      "connected-accounts contract unavailable");
    requireValue(request && request.include_secrets === false &&
      request.include_raw_provider_ids === false,
      "bounded observation request required");

    var sync = root.StegVerseDeviceKVInTrSync;
    requireValue(sync && typeof sync.loadTarget === "function",
      "DEVICE_KV sync unavailable");

    return registeredNode().then(function (bound) {
      var q = buildObservationRequest(bound.registration.node_id);
      return dispatchDeviceKV(bound, q).then(function (response) {
        var observed = response && response.context && response.context.connected_account_observations;
        requireValue(observed && Array.isArray(observed.accounts),
          "bounded connected-account observations were not returned");
        // Re-assert boundedness on whatever KV returned before it reaches the UI.
        accounts.assertBounded(observed, "connected_account_observations");
        return { accounts: observed.accounts };
      });
    });
  }

  /* ---- device-kv dispatch (observation read) -------------------------- */

  function dispatchDeviceKV(bound, q) {
    var api = intr();
    var hb = root.StegVerseHBInTrCarrier;
    var sync = root.StegVerseDeviceKVInTrSync;
    requireValue(hb && typeof hb.buildBinding === "function", "HB/InTr carrier unavailable");
    var payload = utf8(canon(q));
    return api.buildIntent("device-kv", payload, q.operation, q.request_id)
      .then(function (intent) {
        return hb.buildBinding(intent.packet_id, intent.payload_hash).then(function (binding) {
          return api.buildMaterializationRequest(
            "device-kv", intent, "inline://materialization_request.kv_request", binding, { kv_request: q });
        });
      })
      .then(function (m) {
        return bound.node.queueIntrMaterializationRequest(m)
          .then(function () { return sync.synchronizeMaterialization(m.materialization_id); })
          .then(function (result) {
            requireValue(result && result.response, "connected-account observation result unavailable");
            assertNonAuthorizing(result.response, "observation");
            return result.response;
          });
      });
  }

  /* ---- governance assertions ------------------------------------------ */

  function assertNonAuthorizing(doc, label) {
    requireValue(doc.credential_authority === "TV/TVC",
      label + " credential authority invalid");
    requireValue(doc.github_token_runtime_authority === "NONE",
      label + " GitHub runtime authority invalid");
    requireValue(doc.credential_material_present === false,
      label + " credential material boundary invalid");
    requireValue(doc.authority_effect === "NONE" ||
      String(doc.authority_effect || "").indexOf("NONE") === 0,
      label + " authority effect invalid");
  }

  /* ---- population ------------------------------------------------------ */

  function buildTransferPacket(account, ownerSelectionRef) {
    // Mirrors continuity-vault-kit runtime/kv_skap_account_transfer.build_transfer_packet.
    // Field names and the non-secret assertions are the producer's contract, not ours.
    var payload = {
      owner_selection_ref: ownerSelectionRef,
      provider_org_ref: account.provider_org_ref,
      account_class: account.account_class,
      account_status: account.status,
      source_evidence_ref: account.account_ref
    };
    return sha256Value(payload).then(function (payloadHash) {
      return {
        schema: TRANSFER_SCHEMA,
        direction: "KNOWLEDGEVAULT_TO_SKAP_VAULT",
        source_boundary: "KnowledgeVault",
        destination_boundary: "SKAP_Vault",
        owner_selection_ref: payload.owner_selection_ref,
        provider_org_ref: payload.provider_org_ref,
        account_class: payload.account_class,
        account_status: payload.account_status,
        source_evidence_ref: payload.source_evidence_ref,
        payload_sha256: payloadHash,
        contains_secret_material: false,
        raw_provider_account_identifier_present: false,
        requested_transition: OPERATION
      };
    });
  }

  function buildBoundaryEnvelope(packet, kvRequest) {
    return Promise.all([sha256Value(packet), sha256Value(kvRequest)])
      .then(function (hashes) {
        return {
          schema: ENVELOPE_SCHEMA,
          source_boundary: "KnowledgeVault",
          destination_boundary: "SKAP_Vault",
          transfer_packet_sha256: hashes[0],
          request_sha256: hashes[1],
          payload_sha256: packet.payload_sha256,
          canonical_state_changed: false,
          credential_material_transferred: false,
          authority_effect: "NONE_BOUNDARY_TRANSFER_ONLY"
        };
      });
  }

  function buildInterlockRequest(nodeId) {
    return {
      schema_version: "kv.interlock.request.v1",
      operation: "COMMIT_CANDIDATE",
      request_id: randomId("SITE-SKAP-ACCOUNT-METADATA-"),
      requester: { module: "Site", component: "MyKVConnectedAccounts" },
      purpose: "Owner-selected admission of bounded non-secret account metadata into the SKAP Vault.",
      record_class: OBSERVATION_RECORD_CLASS,
      requested_scope: ["skap_account_metadata_admit"],
      minimum_necessary_justification:
        "Transfer only the owner-selected bounded account metadata. No credential material, no raw provider account identifiers.",
      authority_ref: "stegos-node://" + nodeId,
      disclosure_mode: "BOUNDED_CONTEXT",
      candidate_writeback: {
        candidate_type: "SKAP_ACCOUNT_METADATA_ADMIT",
        payload_ref: "inline://materialization_request.account_metadata_transfer",
        requested_destination: OBSERVATION_DEST
      }
    };
  }

  function populateOne(bound, account, ownerSelectionRef) {
    var api = intr();
    var hb = root.StegVerseHBInTrCarrier;
    requireValue(hb && typeof hb.buildBinding === "function", "HB/InTr carrier unavailable");
    var nodeId = bound.registration.node_id;
    var kvRequest = buildInterlockRequest(nodeId);

    return buildTransferPacket(account, ownerSelectionRef).then(function (packet) {
      return buildBoundaryEnvelope(packet, kvRequest).then(function (envelope) {
        var payload = utf8(canon(packet));
        return api.buildIntent(PROFILE, payload, OPERATION, kvRequest.request_id)
          .then(function (intent) {
            return hb.buildBinding(intent.packet_id, intent.payload_hash).then(function (binding) {
              return api.buildMaterializationRequest(
                PROFILE, intent,
                "inline://materialization_request.account_metadata_transfer",
                binding,
                {
                  account_metadata_transfer: packet,
                  kv_interlock_request: kvRequest,
                  intr_boundary_envelope: envelope
                });
            });
          })
          .then(function (m) {
            return bound.node.queueIntrMaterializationRequest(m).then(function (entry) {
              return requireSkapReceipt(entry, m, packet);
            });
          });
      });
    });
  }

  function requireSkapReceipt(entry, materialization, packet) {
    // A queued outbox entry is not an admission. Only an exact TVC SKAP
    // receipt, bound to this materialization and this packet hash, may be
    // reported as accepted.
    requireValue(entry && entry.tvc_receipt_observed === true,
      "no TVC SKAP receipt observed for this account metadata transfer");
    var receipt = entry.tvc_receipt;
    requireValue(receipt && receipt.schema === SKAP_RECEIPT_SCHEMA,
      "SKAP account metadata receipt schema invalid");
    requireValue(receipt.materialization_id === materialization.materialization_id &&
      receipt.request_hash === materialization.request_hash,
      "SKAP receipt materialization binding invalid");
    requireValue(receipt.payload_sha256 === packet.payload_sha256,
      "SKAP receipt payload binding invalid");
    requireValue(receipt.synthetic_material_only === false,
      "synthetic material cannot satisfy account metadata admission");
    assertNonAuthorizing(receipt, "SKAP receipt");
    requireValue(typeof receipt.skap_account_ref === "string" && receipt.skap_account_ref,
      "SKAP receipt account reference missing");
    return {
      skap_account_ref: receipt.skap_account_ref,
      provider_org_ref: packet.provider_org_ref,
      account_class: packet.account_class,
      status: packet.account_status
    };
  }

  function populateSelectedAccountMetadata(request) {
    try { return populateSelectedAccountMetadataInner(request); }
    catch (err) { return Promise.reject(err); }
  }

  function populateSelectedAccountMetadataInner(request) {
    requireValue(request && request.schema ===
      "stegverse.site.my-kv.connected-account-population-request/v1",
      "population request schema invalid");
    requireValue(request.destination === "SKAP_NONSECRET_ACCOUNT_METADATA",
      "population destination invalid");
    requireValue(request.synthetic_input_allowed === false &&
      request.raw_provider_identifiers_present === false &&
      request.credential_material_present === false,
      "population request boundary assertions invalid");
    requireValue(Array.isArray(request.accounts) && request.accounts.length,
      "at least one selected account required");

    var ownerSelectionRef = randomId("owner-selection:");
    return registeredNode().then(function (bound) {
      return request.accounts.reduce(function (chain, account) {
        return chain.then(function (admitted) {
          return populateOne(bound, account, ownerSelectionRef).then(function (row) {
            return admitted.concat([row]);
          });
        });
      }, Promise.resolve([])).then(function (admitted) {
        // Deliberately carries no field whose name would trip the caller's
        // own bounded-result scan in assets/my-kv-connected-accounts.js.
        return {
          accepted: true,
          schema: "stegverse.site.my-kv.connected-account-population-result/v1",
          owner_selection_ref: ownerSelectionRef,
          admitted: admitted,
          authority_effect: "NONE_POPULATION_RESULT_ONLY"
        };
      });
    });
  }

  root.StegVerseKVAccountObservationBridge = Object.freeze({
    listObservedAccounts: listObservedAccounts,
    populateSelectedAccountMetadata: populateSelectedAccountMetadata,
    authority_effect: "NONE",
    credential_authority: "TV/TVC"
  });
}(typeof globalThis !== "undefined" ? globalThis : this));
