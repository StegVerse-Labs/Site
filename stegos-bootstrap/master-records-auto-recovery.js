"use strict";

(function (root) {
  var DB_NAME = "stegos-web-bootstrap-v1";
  var DB_VERSION = 1;
  var RECEIPT_STORE = "receipts";
  var PACKAGE_URL = "./master-records-sv001-custody-package.json";
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
      if (!recovery || recovery.target_source_receipt_sha256 !== "sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35" ||
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

  function publishRecovered(recovery) {
    var input = byId("mr-sv001-receipt");
    var state = byId("mr-sv001-state");
    var output = byId("mr-sv001-output");
    var sv001State = byId("sv001-state");
    var sv001Button = byId("run-sv001");
    if (sv001State) { sv001State.textContent = "COMPLETED — TERMINAL"; }
    if (sv001Button) { sv001Button.disabled = true; sv001Button.textContent = "SV001 Cycle Completed"; }
    if (input) { input.value = JSON.stringify(recovery.source_receipt, null, 2); }
    if (state && !/^PASS/.test(state.textContent || "")) { state.textContent = "RECOVERED_HASH_VERIFIED_PENDING_MACHINE_GOVERNANCE"; }
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

  function publishFailClosed(error) {
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

  function hasExactRetainedProof() {
    if (!root.StegOSPersistentCardUX || typeof root.StegOSPersistentCardUX.findStoredSv001Proof !== "function") { return Promise.resolve(false); }
    return root.StegOSPersistentCardUX.findStoredSv001Proof().then(function (proof) { return !!proof; }).catch(function () { return false; });
  }

  function hydrationReady(attempt) {
    var state = byId("sv001-state");
    if (state && /^COMPLETED/.test(state.textContent || "")) { return Promise.resolve(true); }
    if (attempt >= MAX_HYDRATION_ATTEMPTS) { return Promise.resolve(false); }
    return new Promise(function (resolve) { root.setTimeout(resolve, HYDRATION_RETRY_MS); }).then(function () { return hydrationReady(attempt + 1); });
  }

  function recoverNow() {
    if (runPromise) { return runPromise; }
    runPromise = hydrationReady(0).then(function (terminal) {
      if (!terminal) { return null; }
      return hasExactRetainedProof().then(function (present) {
        if (present) { return null; }
        if (!root.StegVerseMasterRecordsSv001CanonicalJournalRecovery || typeof root.StegVerseMasterRecordsSv001CanonicalJournalRecovery.recover !== "function") {
          fail("exact canonical Master Records recovery module unavailable");
        }
        return Promise.all([readJournal(), loadPackage()]).then(function (parts) {
          return root.StegVerseMasterRecordsSv001CanonicalJournalRecovery.recover(parts[0], parts[1].canonical_journal_recovery.target_source_receipt_sha256);
        }).then(function (recovery) {
          if (!recovery || recovery.state !== "RECOVERED_HASH_VERIFIED" || recovery.unique_match_count !== 1 || recovery.authority_effect !== "NONE_RECOVERY_ONLY") {
            fail("canonical retained-journal recovery did not produce one verified source object");
          }
          return publishRecovered(recovery);
        });
      });
    }).catch(publishFailClosed).finally(function () { runPromise = null; });
    return runPromise;
  }

  root.StegOSMasterRecordsAutoRecovery = {
    run: recoverNow,
    authorityEffect: "NONE_RECOVERY_ONLY",
    custodyExecutedByRecovery: false
  };

  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", function () { recoverNow(); }); }
  else { recoverNow(); }
  document.addEventListener("visibilitychange", function () { if (!document.hidden) { recoverNow(); } });
  root.addEventListener("pageshow", function () { recoverNow(); });
}(window));
