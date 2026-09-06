"use strict";

(function (root) {
  var TASK_ID = "SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001";
  var PROFILE = "STEGVERSE001_BOUNDED_CONTINUITY_AUDIT_V1";
  var SOURCE_SCHEMA = "stegverse.stegverse001.bounded-autonomy-cycle-receipt/v1";
  var TERMINAL_SCHEMA = "stegos.external_resident_task_terminal_receipt/v1";
  var BINDING_SCHEMA = "stegos.external_worker_admission_binding_receipt/v1";
  var RECONSTRUCTION_SCHEMA = "stegos.external_resident_task_reconstruction_receipt/v1";
  var CONSUMPTION_SCHEMA = "stegos.tvc_portable_sv001_lease_consumption_projection/v1";
  var ISSUANCE_SCHEMA = "stegverse.tvc.stegverse001-bounded-autonomy-portable-lease-issuance/v1";
  var CHECKOUT_SCHEMA = "stegverse.workercoordinator-portable-checkout-receipt/v1";
  var TRANSITION = "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED";
  var AUTHORIZED_SOURCE = "EXTERNAL_WORKERCOORDINATOR_TVC_BOUND_ENVELOPE";
  var MAX_TIMESTAMP_SEARCH_MS = 5000;

  function fail(message) { throw new Error("FAIL_CLOSED: " + message); }
  function canonicalize(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(canonicalize).join(",") + "]"; }
    return "{" + Object.keys(value).sort().map(function (key) { return JSON.stringify(key) + ":" + canonicalize(value[key]); }).join(",") + "}";
  }
  function bytesToHex(bytes) { var out = ""; for (var i = 0; i < bytes.length; i += 1) { out += bytes[i].toString(16).padStart(2, "0"); } return out; }
  function shaHex(value) { return root.crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonicalize(value))).then(function (digest) { return bytesToHex(new Uint8Array(digest)); }); }
  function shaPrefixed(value) { return shaHex(value).then(function (digest) { return "sha256:" + digest; }); }
  function without(object, key) { var copy = {}; Object.keys(object || {}).forEach(function (name) { if (name !== key) { copy[name] = object[name]; } }); return copy; }
  function normalizeJournal(input) { var rows = Array.isArray(input) ? input : (input && Array.isArray(input.continued_receipts) ? input.continued_receipts : null); if (!rows || !rows.length) { fail("retained journal entries required"); } return rows.slice().sort(function (a, b) { return a.sequence - b.sequence; }); }
  function verifyJournal(rows) {
    var chain = Promise.resolve();
    rows.forEach(function (entry, index) {
      chain = chain.then(function () {
        if (!entry || entry.schema !== "stegos.web_bootstrap_journal_entry.v1") { fail("journal entry schema mismatch"); }
        if (!Number.isInteger(entry.sequence) || entry.sequence < 1) { fail("journal sequence invalid"); }
        if (index > 0) {
          if (entry.sequence !== rows[index - 1].sequence + 1) { fail("journal sequence gap"); }
          if (entry.previous_entry_sha256 !== rows[index - 1].entry_sha256) { fail("journal chain mismatch"); }
        }
        return shaHex(entry.receipt).then(function (receiptDigest) {
          if (receiptDigest !== entry.receipt_sha256) { fail("journal receipt hash mismatch"); }
          return shaHex(without(entry, "entry_sha256"));
        }).then(function (entryDigest) { if (entryDigest !== entry.entry_sha256) { fail("journal entry hash mismatch"); } });
      });
    });
    return chain.then(function () { return rows; });
  }
  function byEntryHash(rows, hash) { return rows.find(function (entry) { return entry.entry_sha256 === hash; }) || null; }
  function bySequence(rows, sequence) { return rows.find(function (entry) { return entry.sequence === sequence; }) || null; }
  function validateCheckout(entry, binding) {
    if (!entry || !entry.receipt || entry.receipt.schema !== CHECKOUT_SCHEMA) { fail("canonical WorkerCoordinator checkout receipt missing"); }
    var receipt = entry.receipt;
    if (receipt.task_id !== TASK_ID || receipt.claim_id !== binding.claim_id || receipt.fencing_token !== binding.fencing_token) { fail("WorkerCoordinator claim/fence lineage mismatch"); }
    if (receipt.global_workercoordinator_authority !== true || receipt.stegos_device_task_authority !== false) { fail("WorkerCoordinator authority lineage mismatch"); }
    if (receipt.execution_surface !== "CURRENT_USER_IPHONE" || receipt.credential_authority !== "TV/TVC" || receipt.github_token_runtime_authority !== "NONE") { fail("WorkerCoordinator execution/credential boundary mismatch"); }
    if (receipt.receipt_sha256 !== binding.admission_receipt_sha256) { fail("binding does not reference checkout receipt"); }
    return shaPrefixed(without(receipt, "receipt_sha256")).then(function (digest) { if (digest !== receipt.receipt_sha256) { fail("WorkerCoordinator receipt self-hash mismatch"); } return receipt; });
  }
  function validateIssuance(entry, binding) {
    if (!entry || !entry.receipt || entry.receipt.schema !== ISSUANCE_SCHEMA) { fail("TVC issuance receipt missing"); }
    var receipt = entry.receipt;
    if (receipt.transition_id !== "TVC_SV001_BOUNDED_AUTONOMY_LEASE_ISSUED" || receipt.workercoordinator_claim_id !== binding.claim_id || receipt.workercoordinator_fencing_token !== binding.fencing_token || receipt.lease_id !== binding.lease_id || receipt.lease_hash !== binding.lease_hash) { fail("TVC issuance lineage mismatch"); }
    if (receipt.single_cycle !== true || receipt.github_actions_runtime_authority !== "NONE") { fail("TVC issuance authority boundary mismatch"); }
    return shaPrefixed(without(receipt, "receipt_hash")).then(function (digest) { if (digest !== receipt.receipt_hash) { fail("TVC issuance receipt self-hash mismatch"); } return receipt; });
  }
  function buildCandidate(binding, preExecutionEntries, preExecutionTail, completedAt) {
    return {
      schema: SOURCE_SCHEMA, state: "COMPLETED", transition_id: TRANSITION, entity_id: "StegVerse-001", entity_alias: "Beta_Orionis", task_id: TASK_ID,
      claim_id: binding.claim_id, fencing_token: binding.fencing_token, lease_id: binding.lease_id, lease_sha256: binding.lease_hash,
      candidate_task: { schema: "stegverse.stegverse001.autonomous-task-candidate/v1", candidate_id: "SV001-CONTINUITY-AUDIT-001", discovered_by: "StegVerse-001/Beta_Orionis", discovery_basis: ["stegos_device_continuity_present", "journal_reconstruction_pass"], goal: "verify current resident continuity and emit a bounded audit receipt", authority_effect: "NONE_CANDIDATE_ONLY" },
      plan: { schema: "stegverse.stegverse001.autonomy-plan/v1", candidate_id: "SV001-CONTINUITY-AUDIT-001", steps: [{ sequence: 1, transition_class: "LOCAL_STATE_OBSERVATION", effect: "READ_ONLY" }, { sequence: 2, transition_class: "RECEIPT_EMISSION", effect: "LOCAL_RECEIPT_ONLY" }], lease_id: binding.lease_id, denial_reachable: true, authority_widening: false },
      observations: { execution_surface: "CURRENT_USER_IPHONE", stegos_node_id: binding.node_id, pre_execution_journal_entries: preExecutionEntries, pre_execution_journal_tail_sha256: preExecutionTail },
      authorized_execution_source: AUTHORIZED_SOURCE, self_directed_task_discovery: true, autonomous_plan_selection: true, external_side_effects: false, network_access_performed: false,
      repository_writeback_performed: false, financial_binding_performed: false, credential_created_or_used: false, denial_reachable_at_commit: true, self_accreditation: false,
      sovereign_authority_claimed: false, global_workercoordinator_authority: false, external_claim_promoted_to_browser_authority: false, master_records_custody: "PENDING",
      sv002_adversarial_observation: "PENDING", completed_at: completedAt, authority_effect: "BOUNDED_LOCAL_AUTONOMY_ONLY"
    };
  }
  async function recover(input, expectedReceiptHash) {
    if (!/^sha256:[a-f0-9]{64}$/.test(expectedReceiptHash || "")) { fail("canonical target receipt hash required"); }
    var rows = normalizeJournal(input); await verifyJournal(rows);
    var terminals = rows.filter(function (entry) { var receipt = entry.receipt || {}; return receipt.schema === TERMINAL_SCHEMA && receipt.task_id === TASK_ID && receipt.profile_id === PROFILE && receipt.state === "COMPLETED" && receipt.transition_id === TRANSITION && receipt.cycle_receipt_hash === expectedReceiptHash; });
    if (terminals.length !== 1) { fail("exactly one canonical terminal receipt required"); }
    var terminalEntry = terminals[0], terminal = terminalEntry.receipt, bindingEntry = byEntryHash(rows, terminal.binding_entry_sha256);
    if (!bindingEntry || !bindingEntry.receipt || bindingEntry.receipt.schema !== BINDING_SCHEMA) { fail("terminal binding entry missing"); }
    var binding = bindingEntry.receipt;
    if (binding.task_id !== TASK_ID || binding.profile_id !== PROFILE || binding.claim_id !== terminal.claim_id || binding.fencing_token !== terminal.fencing_token || binding.credential_authority !== "TV/TVC" || binding.global_workercoordinator_authority !== false || binding.external_claim_promoted_to_browser_authority !== false || binding.carrier_granted_authority !== false) { fail("external binding lineage/authority mismatch"); }
    if (terminalEntry.sequence !== bindingEntry.sequence + 1 || terminalEntry.previous_entry_sha256 !== bindingEntry.entry_sha256) { fail("terminal/binding adjacency mismatch"); }
    var issuanceEntry = byEntryHash(rows, bindingEntry.previous_entry_sha256); if (!issuanceEntry || issuanceEntry.sequence !== bindingEntry.sequence - 1) { fail("TVC issuance adjacency missing"); }
    var checkoutEntry = byEntryHash(rows, issuanceEntry.previous_entry_sha256); if (!checkoutEntry || checkoutEntry.sequence !== issuanceEntry.sequence - 1) { fail("WorkerCoordinator checkout adjacency missing"); }
    await validateCheckout(checkoutEntry, binding); await validateIssuance(issuanceEntry, binding);
    var reconstructionEntry = bySequence(rows, terminalEntry.sequence + 1);
    if (!reconstructionEntry || !reconstructionEntry.receipt || reconstructionEntry.receipt.schema !== RECONSTRUCTION_SCHEMA || reconstructionEntry.receipt.terminal_entry_sha256 !== terminalEntry.entry_sha256 || reconstructionEntry.receipt.state !== "PASS" || reconstructionEntry.receipt.same_execution !== true) { fail("same-execution reconstruction receipt missing"); }
    var consumptionEntry = bySequence(rows, reconstructionEntry.sequence + 1);
    if (!consumptionEntry || !consumptionEntry.receipt || consumptionEntry.receipt.schema !== CONSUMPTION_SCHEMA || consumptionEntry.receipt.lease_id !== binding.lease_id || consumptionEntry.receipt.lease_hash !== binding.lease_hash || consumptionEntry.receipt.execution_receipt_sha256 !== expectedReceiptHash || consumptionEntry.receipt.lease_consumption_state !== "CONSUMED" || consumptionEntry.receipt.credential_authority !== "TV/TVC" || consumptionEntry.receipt.github_token_runtime_authority !== "NONE" || consumptionEntry.receipt.heartbeat_granted_authority !== false) { fail("TVC lease-consumption evidence missing or inconsistent"); }
    var start = Date.parse(binding.bound_at), end = Date.parse(terminal.completed_at);
    if (!Number.isFinite(start) || !Number.isFinite(end) || end < start) { fail("recovery timestamp interval invalid"); }
    if (end - start > MAX_TIMESTAMP_SEARCH_MS) { fail("recovery timestamp interval exceeds bounded search ceiling"); }
    var matches = [];
    for (var timestamp = start; timestamp <= end; timestamp += 1) { var candidate = buildCandidate(binding, bindingEntry.sequence - 1, bindingEntry.previous_entry_sha256, new Date(timestamp).toISOString()); var digest = await shaPrefixed(candidate); if (digest === expectedReceiptHash) { matches.push(candidate); } }
    if (matches.length !== 1) { fail("canonical cycle receipt is not uniquely recoverable from retained journal"); }
    var source = matches[0]; source.receipt_hash = expectedReceiptHash;
    return { schema: "stegverse.master-records.sv001-canonical-journal-recovery/v1", state: "RECOVERED_HASH_VERIFIED", source_receipt: source, source_receipt_sha256: expectedReceiptHash,
      source_journal_window: { checkout_sequence: checkoutEntry.sequence, tvc_issuance_sequence: issuanceEntry.sequence, binding_sequence: bindingEntry.sequence, terminal_sequence: terminalEntry.sequence, reconstruction_sequence: reconstructionEntry.sequence, consumption_sequence: consumptionEntry.sequence },
      matched_completed_at: source.completed_at, unique_match_count: 1, journal_integrity_verified: true, same_execution_reconstruction_verified: true, tvc_single_cycle_consumption_verified: true,
      execution_authority: false, custody_authority: false, lease_issuance_authority: false, credential_authority: "TV/TVC", github_token_runtime_authority: "NONE", external_non_stegverse_machine_required: false, authority_effect: "NONE_RECOVERY_ONLY" };
  }
  root.StegVerseMasterRecordsSv001CanonicalJournalRecovery = { recover: recover, canonicalize: canonicalize, shaHex: shaHex, buildCandidate: buildCandidate };
}(typeof self !== "undefined" ? self : globalThis));
