"use strict";

(function (root) {
  var DB_NAME = "stegos-web-bootstrap-v1";
  var DB_VERSION = 1;
  var RECEIPT_STORE = "receipts";
  var PACKAGE_URL = "./master-records-sv001-custody-package.json";
  var CANONICAL_SOURCE_SHA = "sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35";
  var MAX_HYDRATION_ATTEMPTS = 80;
  var HYDRATION_RETRY_MS = 100;
  var runPromise = null;

  function fail(message) { throw new Error("FAIL_CLOSED: " + message); }
  function byId(id) { return document.getElementById(id); }

  function openDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("automatic Master Records recovery IndexedDB open failed")); };
      request.onblocked = function () { reject(new Error("automatic Master Records recovery IndexedDB open blocked")); };
    });
  }

  function getReceipts(db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(RECEIPT_STORE, "readonly");
      var request = tx.objectStore(RECEIPT_STORE).getAll();
      request.onsuccess = function () {
        var rows = request.result || [];
        rows.sort(function (a, b) { return a.sequence - b.sequence; });
        resolve(rows);
      };
      request.onerror = function () { reject(request.error || new Error("automatic Master Records recovery journal read failed")); };
    });
  }

  function readJournal() {
    return openDb().then(function (db) {
      return getReceipts(db).then(function (rows) { db.close(); return rows; }).catch(function (error) { db.close(); throw error; });
    });
  }

  function loadPackage() {
    return fetch(PACKAGE_URL, { cache: "no-store", credentials: "same-origin" }).then(function (response) {
      if (!response.ok) { fail("canonical Master Records recovery package unavailable"); }
      return response.json();
    }).then(function (pkg) {
      var recovery = pkg && pkg.canonical_journal_recovery;
      if (!pkg || pkg.schema !== "stegverse.master-records.portable-sv001-custody-package/v1" || pkg.canonical_owner !== "master-records/orchestration") {
        fail("canonical Master Records package identity mismatch");
      }
      if (pkg.execution_surface !== "CURRENT_USER_IPHONE" || pkg.execution_authority !== false || pkg.lease_issuance_authority !== false || pkg.credential_authority !== false) {
        fail("Master Records package authority boundary mismatch");
      }
      if (!recovery || recovery.target_source_receipt_sha256 !== CANONICAL_SOURCE_SHA ||
          recovery.target_claim_id !== "SHWP-SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001-G23" || recovery.target_fencing_token !== 23 ||
          recovery.execution_surface !== "CURRENT_USER_IPHONE" || recovery.exact_unique_hash_match_required !== true || recovery.journal_integrity_required !== true ||
          recovery.same_execution_reconstruction_required !== true || recovery.tvc_single_cycle_consumption_required !== true ||
          recovery.source_or_ci_is_authentic_recovery !== false || recovery.authority_effect !== "NONE_RECOVERY_ONLY") {
        fail("canonical Master Records recovery policy mismatch");
      }
      return pkg;
    });
  }

  function dispatchPersistenceSignals() {
    ["mr-sv001-receipt", "mr-sv001-output"].forEach(function (id) {
      var node = byId(id);
      if (node) { node.dispatchEvent(new Event("input", { bubbles: true })); }
    });
  }

  function extractCycleReceipt(proof) {
    if (!proof || typeof proof !== "object") { return null; }
    if (proof.transition_id === "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED") { return proof; }
    if (proof.subordinate_execution_proof && proof.subordinate_execution_proof.cycle_receipt) {
      return proof.subordinate_execution_proof.cycle_receipt;
    }
    if (proof.cycle_receipt) { return proof.cycle_receipt; }
    return null;
  }

  function exactCanonicalCycleReceipt(proof) {
    var receipt = extractCycleReceipt(proof);
    if (!receipt || receipt.transition_id !== "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED" || receipt.receipt_hash !== CANONICAL_SOURCE_SHA) {
      return null;
    }
    return receipt;
  }

  function publishSourceReceipt(receipt, label) {
    var input = byId("mr-sv001-receipt");
    var state = byId("mr-sv001-state");
    var sv001State = byId("sv001-state");
    var sv001Button = byId("run-sv001");
    if (sv001State) { sv001State.textContent = "COMPLETED — TERMINAL"; }
    if (sv001Button) { sv001Button.disabled = true; sv001Button.textContent = "SV001 Cycle Completed"; }
    if (input) { input.value = JSON.stringify(receipt, null, 2); }
    if (state && !/^PASS/.test(state.textContent || "")) { state.textContent = label; }
    dispatchPersistenceSignals();
  }

  function publishRecovered(recovery) {
    var output = byId("mr-sv001-output");
    publishSourceReceipt(recovery.source_receipt, "RECOVERED_HASH_VERIFIED_PENDING_MACHINE_GOVERNANCE");
    if (output) {
      output.textContent = JSON.stringify({
        schema: recovery.schema,
        state: recovery.state,
        source_receipt_sha256: recovery.source_receipt_sha256,
        matched_completed_at: recovery.matched_completed_at,
        unique_match_count: recovery.unique_match_count,
        journal_integrity_verified: recovery.journal_integrity_verified,
        same_execution_reconstruction_verified: recovery.same_execution_reconstruction_verified,
        tvc_single_cycle_consumption_verified: recovery.tvc_single_cycle_consumption_verified,
        custody_executed: false,
        custody_waits_for: "CONTEMPORANEOUS_INTERLOCK_INTR_GOVERNANCE_FOR_SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION",
        human_approval_required: false,
        human_interaction_queue_blocks_transition: false,
        authority_effect: "NONE_RECOVERY_ONLY"
      }, null, 2);
    }
    dispatchPersistenceSignals();
    document.dispatchEvent(new CustomEvent("stegverse:sv001-master-records-recovery-ready", { detail: recovery }));
    return recovery;
  }

  function publishRecoveryFailClosed(error) {
    var state = byId("mr-sv001-state");
    var output = byId("mr-sv001-output");
    if (state && !/^PASS/.test(state.textContent || "")) { state.textContent = "AWAITING_EXACT_COMPLETED_PROOF"; }
    if (output && !(output.textContent || "").trim()) {
      output.textContent = "Automatic canonical G23 recovery did not complete: " + String(error && error.message ? error.message : error) +
        "\nManual exact-proof import remains a fail-closed fallback. SV001 must not be rerun.";
    }
    dispatchPersistenceSignals();
    return null;
  }

  function publishCustodyFailClosed(error, sourceMode) {
    var state = byId("mr-sv001-state");
    var output = byId("mr-sv001-output");
    if (state && !/^PASS/.test(state.textContent || "")) { state.textContent = "FAIL_CLOSED_MACHINE_GOVERNED_CUSTODY"; }
    if (output) {
      output.textContent = JSON.stringify({
        schema: "stegos.master-records.sv001-auto-continuation-failure/v1",
        state: "FAIL_CLOSED",
        source_mode: sourceMode,
        source_receipt_sha256: CANONICAL_SOURCE_SHA,
        reason: String(error && error.message ? error.message : error),
        current_governance_required: true,
        human_approval_required: false,
        prior_receipt_authorizes_transition: false,
        sv001_rerun_allowed: false,
        authority_effect: "NONE"
      }, null, 2);
    }
    dispatchPersistenceSignals();
    return null;
  }

  function findExactRetainedProof() {
    if (!root.StegOSPersistentCardUX || typeof root.StegOSPersistentCardUX.findStoredSv001Proof !== "function") { return Promise.resolve(null); }
    return root.StegOSPersistentCardUX.findStoredSv001Proof().then(function (proof) {
      return exactCanonicalCycleReceipt(proof);
    }).catch(function () { return null; });
  }

  function hydrationReady(attempt) {
    var state = byId("sv001-state");
    if (state && /^COMPLETED/.test(state.textContent || "")) { return Promise.resolve(true); }
    if (attempt >= MAX_HYDRATION_ATTEMPTS) { return Promise.resolve(false); }
    return new Promise(function (resolve) { root.setTimeout(resolve, HYDRATION_RETRY_MS); }).then(function () { return hydrationReady(attempt + 1); });
  }

  function custodyAlreadyComplete() {
    var state = byId("mr-sv001-state");
    return !!(state && /^PASS/.test(state.textContent || ""));
  }

  function recoverCanonicalSource() {
    if (!root.StegVerseMasterRecordsSv001CanonicalJournalRecovery || typeof root.StegVerseMasterRecordsSv001CanonicalJournalRecovery.recover !== "function") {
      return Promise.reject(new Error("FAIL_CLOSED: exact canonical Master Records recovery module unavailable"));
    }
    return Promise.all([readJournal(), loadPackage()]).then(function (parts) {
      return root.StegVerseMasterRecordsSv001CanonicalJournalRecovery.recover(parts[0], parts[1].canonical_journal_recovery.target_source_receipt_sha256);
    }).then(function (recovery) {
      if (!recovery || recovery.state !== "RECOVERED_HASH_VERIFIED" || recovery.unique_match_count !== 1 ||
          recovery.source_receipt_sha256 !== CANONICAL_SOURCE_SHA || recovery.authority_effect !== "NONE_RECOVERY_ONLY") {
        fail("canonical retained-journal recovery did not produce one verified source object");
      }
      if (!exactCanonicalCycleReceipt(recovery.source_receipt)) { fail("recovered source object does not bind canonical G23"); }
      publishRecovered(recovery);
      return { receipt: recovery.source_receipt, source_mode: "CANONICAL_RETAINED_JOURNAL_RECOVERY", recovery: recovery };
    });
  }

  function resolveCanonicalSource() {
    return findExactRetainedProof().then(function (receipt) {
      if (receipt) {
        publishSourceReceipt(receipt, "READY_FROM_SAME_DEVICE_CANONICAL_G23_PROOF");
        return { receipt: receipt, source_mode: "SAME_DEVICE_PERSISTED_CANONICAL_G23", recovery: null };
      }
      return recoverCanonicalSource();
    });
  }

  function executeMachineGovernedCustody(resolved) {
    var state = byId("mr-sv001-state");
    var output = byId("mr-sv001-output");
    if (!resolved || !resolved.receipt) { return Promise.resolve(null); }
    if (!root.StegOSWebBootstrap || typeof root.StegOSWebBootstrap.executeMasterRecordsSv001Custody !== "function") {
      return Promise.reject(new Error("FAIL_CLOSED: existing machine-governed Master Records custody API unavailable"));
    }
    if (state) { state.textContent = "EXECUTING_MACHINE_GOVERNED_CUSTODY"; }
    if (output) {
      output.textContent = JSON.stringify({
        schema: "stegos.master-records.sv001-auto-continuation/v1",
        state: "REQUESTING_CONTEMPORANEOUS_INTR_GOVERNANCE",
        source_mode: resolved.source_mode,
        source_receipt_sha256: CANONICAL_SOURCE_SHA,
        human_approval_required: false,
        prior_receipt_authorizes_transition: false,
        authority_effect: "NONE_CARRIER_ONLY"
      }, null, 2);
    }
    dispatchPersistenceSignals();
    return root.StegOSWebBootstrap.executeMasterRecordsSv001Custody(resolved.receipt).then(function (result) {
      if (!result || result.state !== "PASS" || result.reconstruction_state !== "PASS" || result.intr_governance_admission_observed !== true) {
        fail("machine-governed Master Records custody did not return admitted reconstruction PASS");
      }
      if (state) { state.textContent = result.already_custodied ? "PASS_ALREADY_CUSTODIED" : "PASS"; }
      if (output) {
        output.textContent = JSON.stringify({
          schema: "stegos.master-records.sv001-auto-continuation/v1",
          state: "PASS",
          source_mode: resolved.source_mode,
          source_receipt_sha256: CANONICAL_SOURCE_SHA,
          recovery: resolved.recovery ? {
            state: resolved.recovery.state,
            unique_match_count: resolved.recovery.unique_match_count,
            matched_completed_at: resolved.recovery.matched_completed_at,
            journal_integrity_verified: resolved.recovery.journal_integrity_verified
          } : null,
          custody: result,
          current_governance_observed: true,
          human_approval_required: false,
          prior_receipt_authorizes_transition: false,
          sv001_rerun_allowed: false,
          authority_effect: "NONE_SITE_CARRIER_ONLY"
        }, null, 2);
      }
      if (result.final_replay_tail_sha256 && byId("tail")) { byId("tail").textContent = result.final_replay_tail_sha256; }
      dispatchPersistenceSignals();
      document.dispatchEvent(new CustomEvent("stegverse:sv001-master-records-auto-continuation-pass", { detail: result }));
      return result;
    }).catch(function (error) {
      return publishCustodyFailClosed(error, resolved.source_mode);
    });
  }

  function recoverNow() {
    if (runPromise) { return runPromise; }
    if (custodyAlreadyComplete()) { return Promise.resolve(null); }
    runPromise = hydrationReady(0).then(function (terminal) {
      if (!terminal || custodyAlreadyComplete()) { return null; }
      return resolveCanonicalSource().then(executeMachineGovernedCustody).catch(publishRecoveryFailClosed);
    }).finally(function () { runPromise = null; });
    return runPromise;
  }

  root.StegOSMasterRecordsAutoRecovery = {
    run: recoverNow,
    extractCycleReceipt: extractCycleReceipt,
    exactCanonicalCycleReceipt: exactCanonicalCycleReceipt,
    authorityEffect: "NONE_RECOVERY_AND_CARRIER_ONLY",
    custodyAuthority: false,
    executionAuthority: false,
    humanApprovalRequired: false,
    sv001RerunAllowed: false
  };

  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", function () { recoverNow(); }); }
  else { recoverNow(); }
  document.addEventListener("visibilitychange", function () { if (!document.hidden) { recoverNow(); } });
  root.addEventListener("pageshow", function () { recoverNow(); });
}(window));
