"use strict";

(function () {
  var ENVELOPE_SCHEMA = "stegverse.external-resident-task-envelope/v1";
  var PROFILE = "STEGVERSE001_BOUNDED_CONTINUITY_AUDIT_V1";
  var TASK_ID = "SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001";
  var WORKER_ID = "stegverse001-bounded-autonomy-runtime-worker";
  var LEASE_SCHEMA = "stegverse.stegverse001.bounded-autonomy-lease/v1";
  var REQUIRED_REQUEST_ID = "TV-REQUEST-STEGVERSE001-BOUNDED-AUTONOMY-001";
  var REQUIRED_REQUEST_HASH = "sha256:c4b3e35d5ecf2246e0e082a591e3144bd61b32cb02133d12a89226cf362f4def";
  var REQUIRED_ALLOWED = ["AUTONOMOUS_TASK_DISCOVERY", "LOCAL_STATE_OBSERVATION", "RECEIPT_EMISSION"];
  var REQUIRED_FORBIDDEN = ["SELF_ACCREDITATION", "SOVEREIGN_AUTHORITY_CHANGE", "FINANCIAL_BINDING", "REPOSITORY_WRITEBACK", "EXTERNAL_NETWORK_ACCESS", "CREDENTIAL_CREATION"];

  function fail(message) { throw new Error("FAIL_CLOSED: " + message); }
  function isInt(value) { return Number.isInteger(value) && value > 0; }
  function containsAll(values, required) {
    if (!Array.isArray(values)) { return false; }
    return required.every(function (value) { return values.indexOf(value) !== -1; });
  }
  function withoutLeaseHash(lease) {
    var copy = {};
    Object.keys(lease || {}).forEach(function (key) { if (key !== "lease_hash") { copy[key] = lease[key]; } });
    return copy;
  }
  function validateAdmission(envelope) {
    var admission = envelope && envelope.worker_admission;
    if (!admission || admission.authority_source !== "WorkerCoordinator" || admission.admitted !== true) {
      fail("external WorkerCoordinator admission required");
    }
    if (admission.task_id !== TASK_ID || admission.worker_id !== WORKER_ID) { fail("task/worker identity mismatch"); }
    if (!admission.claim_id || !isInt(admission.fencing_token)) { fail("external claim/fence required"); }
    if (!admission.admission_receipt_sha256 || !/^sha256:[a-f0-9]{64}$/.test(admission.admission_receipt_sha256)) {
      fail("external admission receipt hash required");
    }
    return admission;
  }
  function validateLease(lease, sha256Hex) {
    if (!lease || lease.schema !== LEASE_SCHEMA) { fail("SV001 lease schema mismatch"); }
    var required = {
      request_id: REQUIRED_REQUEST_ID,
      request_hash: REQUIRED_REQUEST_HASH,
      entity_id: "StegVerse-001",
      entity_alias: "Beta_Orionis",
      lease_state: "ACTIVE",
      credential_authority: "TV/TVC",
      issuer: "TV/TVC",
      receipt_required: true,
      denial_reachable_required: true,
      denial_reachable: true,
      self_accreditation_allowed: false,
      sovereign_authority_granted: false,
      authority_effect: "BOUNDED_PREAUTHORIZED_TRANSITION_CLASSES_ONLY",
      lease_consumption: "SINGLE_AUTONOMY_CYCLE"
    };
    Object.keys(required).forEach(function (key) {
      if (lease[key] !== required[key]) { fail("lease " + key + " mismatch"); }
    });
    if (!lease.lease_id) { fail("lease_id required"); }
    if (!containsAll(lease.allowed_transition_classes, REQUIRED_ALLOWED)) { fail("lease lacks required transition classes"); }
    if (!containsAll(lease.forbidden_transition_classes, REQUIRED_FORBIDDEN)) { fail("lease forbidden-transition floor incomplete"); }
    if (!lease.expires_at || Number.isNaN(Date.parse(lease.expires_at)) || Date.parse(lease.expires_at) <= Date.now()) { fail("lease expired or invalid"); }
    if (!lease.lease_hash || !/^sha256:[a-f0-9]{64}$/.test(lease.lease_hash)) { fail("lease self-hash required"); }
    return sha256Hex(withoutLeaseHash(lease)).then(function (digest) {
      if ("sha256:" + digest !== lease.lease_hash) { fail("lease self-hash mismatch"); }
      return lease;
    });
  }
  function validateEnvelope(envelope, api) {
    if (!envelope || envelope.schema !== ENVELOPE_SCHEMA) { fail("resident task envelope schema mismatch"); }
    if (envelope.profile_id !== PROFILE) { fail("unregistered resident task profile"); }
    if (envelope.task_id !== TASK_ID) { fail("resident task id mismatch"); }
    if (envelope.execution_surface !== "CURRENT_USER_IPHONE") { fail("execution surface must be CURRENT_USER_IPHONE"); }
    if (!envelope.node_id) { fail("established StegOS node id required"); }
    if (envelope.credential_authority !== "TV/TVC" || envelope.github_token_required !== false) { fail("credential boundary drift"); }
    if (envelope.external_non_stegverse_machine_required !== false) { fail("second/external machine dependency prohibited"); }
    var admission = validateAdmission(envelope);
    return validateLease(envelope.lease, api.sha256Hex).then(function (lease) {
      return { admission: admission, lease: lease };
    });
  }

  function executeSv001(envelope, validated, api) {
    var admission = validated.admission;
    var lease = validated.lease;
    var replayBefore;
    var bindingEntry;
    var candidate;
    var plan;
    var cycleReceipt;

    return api.reserveExternalTask({
      task_id: TASK_ID,
      profile_id: PROFILE,
      claim_id: admission.claim_id,
      fencing_token: admission.fencing_token,
      node_id: envelope.node_id,
      lease_id: lease.lease_id,
      admission_receipt_sha256: admission.admission_receipt_sha256
    }).then(function () {
      return api.replayJournal();
    }).then(function (report) {
      if (!report || report.state !== "PASS") { fail("resident journal replay did not pass"); }
      replayBefore = report;
      candidate = {
        schema: "stegverse.stegverse001.autonomous-task-candidate/v1",
        candidate_id: "SV001-CONTINUITY-AUDIT-001",
        discovered_by: "StegVerse-001/Beta_Orionis",
        discovery_basis: ["stegos_device_continuity_present", "journal_reconstruction_pass"],
        goal: "verify current resident continuity and emit a bounded audit receipt",
        authority_effect: "NONE_CANDIDATE_ONLY"
      };
      plan = {
        schema: "stegverse.stegverse001.autonomy-plan/v1",
        candidate_id: candidate.candidate_id,
        steps: [
          { sequence: 1, transition_class: "LOCAL_STATE_OBSERVATION", effect: "READ_ONLY" },
          { sequence: 2, transition_class: "RECEIPT_EMISSION", effect: "LOCAL_RECEIPT_ONLY" }
        ],
        lease_id: lease.lease_id,
        denial_reachable: true,
        authority_widening: false
      };
      return api.appendReceipt({
        schema: "stegos.external_worker_admission_binding_receipt/v1",
        task_id: TASK_ID,
        profile_id: PROFILE,
        node_id: envelope.node_id,
        claim_id: admission.claim_id,
        fencing_token: admission.fencing_token,
        external_authority_source: "WorkerCoordinator",
        admission_receipt_sha256: admission.admission_receipt_sha256,
        lease_id: lease.lease_id,
        lease_hash: lease.lease_hash,
        global_workercoordinator_authority: false,
        external_claim_promoted_to_browser_authority: false,
        carrier_granted_authority: false,
        credential_authority: "TV/TVC",
        authority_effect: "EXTERNAL_ADMISSION_BINDING_ONLY",
        bound_at: new Date().toISOString()
      });
    }).then(function (entry) {
      bindingEntry = entry;
      cycleReceipt = {
        schema: "stegverse.stegverse001.bounded-autonomy-cycle-receipt/v1",
        state: "COMPLETED",
        transition_id: "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED",
        entity_id: "StegVerse-001",
        entity_alias: "Beta_Orionis",
        task_id: TASK_ID,
        claim_id: admission.claim_id,
        fencing_token: admission.fencing_token,
        lease_id: lease.lease_id,
        lease_sha256: lease.lease_hash,
        candidate_task: candidate,
        plan: plan,
        observations: {
          execution_surface: "CURRENT_USER_IPHONE",
          stegos_node_id: envelope.node_id,
          pre_execution_journal_entries: replayBefore.entries,
          pre_execution_journal_tail_sha256: replayBefore.tail_sha256
        },
        authorized_execution_source: "EXTERNAL_WORKERCOORDINATOR_TVC_BOUND_ENVELOPE",
        self_directed_task_discovery: true,
        autonomous_plan_selection: true,
        external_side_effects: false,
        network_access_performed: false,
        repository_writeback_performed: false,
        financial_binding_performed: false,
        credential_created_or_used: false,
        denial_reachable_at_commit: true,
        self_accreditation: false,
        sovereign_authority_claimed: false,
        global_workercoordinator_authority: false,
        external_claim_promoted_to_browser_authority: false,
        master_records_custody: "PENDING",
        sv002_adversarial_observation: "PENDING",
        completed_at: new Date().toISOString(),
        authority_effect: "BOUNDED_LOCAL_AUTONOMY_ONLY"
      };
      return api.sha256Hex(cycleReceipt);
    }).then(function (digest) {
      cycleReceipt.receipt_hash = "sha256:" + digest;
      return api.appendReceipt({
        schema: "stegos.external_resident_task_terminal_receipt/v1",
        task_id: TASK_ID,
        profile_id: PROFILE,
        claim_id: admission.claim_id,
        fencing_token: admission.fencing_token,
        state: "COMPLETED",
        transition_id: "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED",
        cycle_receipt_hash: cycleReceipt.receipt_hash,
        binding_entry_sha256: bindingEntry.entry_sha256,
        global_workercoordinator_authority: false,
        credential_authority: "TV/TVC",
        authority_effect: "DEVICE_LOCAL_TASK_EXECUTION_ONLY",
        completed_at: new Date().toISOString()
      });
    }).then(function (terminalEntry) {
      return api.replayJournal().then(function (report) {
        if (!report || report.state !== "PASS") { fail("post-terminal journal replay did not pass"); }
        return api.appendReceipt({
          schema: "stegos.external_resident_task_reconstruction_receipt/v1",
          task_id: TASK_ID,
          profile_id: PROFILE,
          claim_id: admission.claim_id,
          fencing_token: admission.fencing_token,
          state: "PASS",
          terminal_entry_sha256: terminalEntry.entry_sha256,
          replayed_entries: report.entries,
          replay_tail_sha256: report.tail_sha256,
          same_execution: true,
          authority_effect: "NONE",
          reconstructed_at: new Date().toISOString()
        });
      }).then(function (reconstructionEntry) {
        return api.replayJournal().then(function (finalReport) {
          if (!finalReport || finalReport.state !== "PASS") { fail("final journal replay did not pass"); }
          return api.completeExternalTask({
            task_id: TASK_ID,
            claim_id: admission.claim_id,
            fencing_token: admission.fencing_token,
            cycle_receipt_hash: cycleReceipt.receipt_hash,
            reconstruction_entry_sha256: reconstructionEntry.entry_sha256,
            final_replay_tail_sha256: finalReport.tail_sha256
          }).then(function () {
            return {
              schema: "stegos.external_resident_task_execution_proof/v1",
              task_id: TASK_ID,
              profile_id: PROFILE,
              state: "COMPLETED",
              transition_id: "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED",
              node_id: envelope.node_id,
              claim_id: admission.claim_id,
              fencing_token: admission.fencing_token,
              lease_id: lease.lease_id,
              cycle_receipt: cycleReceipt,
              reconstruction_state: "PASS",
              reconstruction_entry_sha256: reconstructionEntry.entry_sha256,
              final_replay_tail_sha256: finalReport.tail_sha256,
              same_execution: true,
              external_workercoordinator_admission_bound: true,
              global_workercoordinator_authority: false,
              external_claim_promoted_to_browser_authority: false,
              carrier_granted_authority: false,
              credential_authority: "TV/TVC",
              external_non_stegverse_machine_required: false,
              authority_effect: "DEVICE_LOCAL_TASK_EXECUTION_ONLY"
            };
          });
        });
      });
    }).catch(function (error) {
      return api.failExternalTask({
        task_id: TASK_ID,
        claim_id: admission.claim_id,
        fencing_token: admission.fencing_token,
        reason: String(error && error.message ? error.message : error)
      }).then(function () { throw error; });
    });
  }

  self.StegOSExternalResidentTask = {
    execute: function (envelope, api) {
      return validateEnvelope(envelope, api).then(function (validated) {
        return executeSv001(envelope, validated, api);
      });
    },
    profileId: PROFILE
  };
}());
