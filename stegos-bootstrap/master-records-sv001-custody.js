"use strict";

(function (root) {
  var SOURCE_SCHEMA = "stegverse.stegverse001.bounded-autonomy-cycle-receipt/v1";
  var TRANSITION = "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED";
  var AUTHORIZED_SOURCE = "EXTERNAL_WORKERCOORDINATOR_TVC_BOUND_ENVELOPE";

  function fail(message) { throw new Error("FAIL_CLOSED: " + message); }

  function canonicalize(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(canonicalize).join(",") + "]"; }
    return "{" + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ":" + canonicalize(value[key]);
    }).join(",") + "}";
  }

  function bytesToHex(bytes) {
    var out = "";
    for (var i = 0; i < bytes.length; i += 1) { out += bytes[i].toString(16).padStart(2, "0"); }
    return out;
  }

  function sha(value) {
    return root.crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonicalize(value))).then(function (digest) {
      return "sha256:" + bytesToHex(new Uint8Array(digest));
    });
  }

  function authorizedExecution(source) {
    return source && (source.authorized_execution === true || source.authorized_execution_source === AUTHORIZED_SOURCE);
  }

  function validateSource(source) {
    if (!source || source.schema !== SOURCE_SCHEMA) { fail("source receipt schema mismatch"); }
    if (source.state !== "COMPLETED" || source.transition_id !== TRANSITION) { fail("terminal transition mismatch"); }
    if (source.entity_id !== "StegVerse-001" || source.entity_alias !== "Beta_Orionis") { fail("entity identity mismatch"); }
    if (!authorizedExecution(source)) { fail("authorized execution evidence missing"); }
    if (source.denial_reachable_at_commit !== true) { fail("DENY reachability missing"); }
    if (source.self_accreditation !== false || source.sovereign_authority_claimed !== false) { fail("authority boundary mismatch"); }
    if (source.network_access_performed !== false || source.repository_writeback_performed !== false ||
        source.financial_binding_performed !== false || source.credential_created_or_used !== false) {
      fail("forbidden side effect observed");
    }
    if (typeof source.claim_id !== "string" || !source.claim_id) { fail("claim_id missing"); }
    if (!Number.isInteger(source.fencing_token) || source.fencing_token < 1) { fail("fencing_token invalid"); }
    if (typeof source.lease_sha256 !== "string" || source.lease_sha256.indexOf("sha256:") !== 0) { fail("lease hash missing"); }
    if (typeof source.receipt_hash !== "string" || !/^sha256:[a-f0-9]{64}$/.test(source.receipt_hash)) { fail("source receipt hash missing"); }
    var body = {};
    Object.keys(source).forEach(function (key) { if (key !== "receipt_hash") { body[key] = source[key]; } });
    return sha(body).then(function (digest) {
      if (digest !== source.receipt_hash) { fail("source receipt self-hash mismatch"); }
      return source;
    });
  }

  function custody(source) {
    return validateSource(source).then(function () {
      return Promise.all([sha(source.candidate_task), sha(source.plan), sha(source.observations)]).then(function (hashes) {
        var record = {
          schema: "stegverse.master-records.stegverse001-bounded-autonomy-custody/v1",
          record_id: "MR-" + source.receipt_hash.split(":", 2)[1].slice(0, 24),
          source_receipt_sha256: source.receipt_hash,
          lease_sha256: source.lease_sha256,
          candidate_task_sha256: hashes[0],
          plan_sha256: hashes[1],
          observations_sha256: hashes[2],
          claim_id: source.claim_id,
          fencing_token: source.fencing_token,
          entity_id: "StegVerse-001",
          authorized_execution: true,
          denial_reachable_at_commit: true,
          custody_authority: true,
          execution_authority: false,
          lease_issuance_authority: false,
          sovereign_authority: false,
          authority_effect: "CUSTODY_AND_RECONSTRUCTION_ONLY"
        };
        return sha(record).then(function (digest) { record.custody_hash = digest; return record; });
      });
    });
  }

  function reconstruct(source, record) {
    return validateSource(source).then(function () {
      return Promise.all([sha(source.candidate_task), sha(source.plan), sha(source.observations)]).then(function (hashes) {
        var checks = {
          source_receipt_hash: record.source_receipt_sha256 === source.receipt_hash,
          lease_hash: record.lease_sha256 === source.lease_sha256,
          candidate_hash: record.candidate_task_sha256 === hashes[0],
          plan_hash: record.plan_sha256 === hashes[1],
          observations_hash: record.observations_sha256 === hashes[2],
          claim_identity: record.claim_id === source.claim_id,
          fence_identity: record.fencing_token === source.fencing_token,
          authority_preserved: record.execution_authority === false && record.sovereign_authority === false
        };
        var pass = Object.keys(checks).every(function (key) { return checks[key] === true; });
        var out = {
          schema: "stegverse.master-records.stegverse001-bounded-autonomy-reconstruction/v1",
          state: pass ? "PASS" : "FAIL_CLOSED",
          entity_id: "StegVerse-001",
          source_receipt_sha256: source.receipt_hash,
          custody_hash: record.custody_hash,
          checks: checks,
          authorized_execution_reconstructed: authorizedExecution(source),
          denial_reachable_reconstructed: source.denial_reachable_at_commit,
          self_accreditation_reconstructed: source.self_accreditation,
          sovereign_authority_claimed_reconstructed: source.sovereign_authority_claimed,
          authority_effect: "NONE_RECONSTRUCTION_ONLY"
        };
        return sha(out).then(function (digest) { out.reconstruction_hash = digest; return out; });
      });
    });
  }

  function process(source) {
    return custody(source).then(function (record) {
      return reconstruct(source, record).then(function (reconstruction) {
        return {
          schema: "stegverse.master-records.portable-sv001-custody-result/v1",
          state: reconstruction.state,
          source_receipt_sha256: source.receipt_hash,
          custody: record,
          reconstruction: reconstruction,
          canonical_owner: "master-records/orchestration",
          execution_surface: "CURRENT_USER_IPHONE",
          network_access_performed: false,
          repository_writeback_performed: false,
          credential_required: false,
          external_non_stegverse_machine_required: false,
          authority_effect: "CUSTODY_AND_RECONSTRUCTION_ONLY"
        };
      });
    });
  }

  root.StegVerseMasterRecordsPortableSv001 = {
    process: process,
    custody: custody,
    reconstruct: reconstruct,
    validateSource: validateSource,
    authorizedExecution: authorizedExecution
  };
}(typeof self !== "undefined" ? self : globalThis));
