"use strict";

(function () {
  var PROFILE = "STEGVERSE001_BOUNDED_CONTINUITY_AUDIT_V1";
  var TASK_ID = "SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001";
  var WORKER_ID = "stegverse001-bounded-autonomy-runtime-worker";

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }

  function validateInput(body) {
    if (!body || body.execution_surface !== "CURRENT_USER_IPHONE") { fail("CURRENT_USER_IPHONE execution surface required"); }
    if (!body.node_id) { fail("established StegOS node id required"); }
    if (body.request_tvc_lease !== true) { fail("explicit TVC portable lease request required"); }
    if (body.credential_authority !== "TV/TVC") { fail("TV/TVC credential authority required"); }
    if (body.github_token_runtime_authority !== "NONE") { fail("GitHub runtime authority prohibited"); }
    if (body.heartbeat_granted_authority !== false) { fail("HB cannot grant authority"); }
    return body;
  }

  function validateCheckout(checkout) {
    var receipt = checkout && checkout.receipt;
    if (!receipt || receipt.authority_effect !== "CANONICAL_WORKERCOORDINATOR_CLAIM_FENCE") { fail("canonical checkout receipt required"); }
    if (receipt.task_id !== TASK_ID || receipt.worker_id !== WORKER_ID) { fail("portable checkout task/worker mismatch"); }
    if (!Number.isInteger(receipt.fencing_token) || receipt.fencing_token < 23) { fail("portable WorkerCoordinator fence below canonical floor"); }
    if (!receipt.claim_id || !/^sha256:[a-f0-9]{64}$/.test(receipt.receipt_sha256 || "")) { fail("canonical checkout receipt identity incomplete"); }
    if (receipt.global_workercoordinator_authority !== true || receipt.stegos_device_task_authority !== false) {
      fail("portable authority lineage mismatch");
    }
    if (receipt.parallel_workercoordinator_claim_issuance_allowed !== false || receipt.governed_transfer_required_before_other_surface_claims !== true) {
      fail("parallel WorkerCoordinator issuance boundary drift");
    }
    if (receipt.credential_authority !== "TV/TVC" || receipt.github_token_runtime_authority !== "NONE" || receipt.heartbeat_granted_authority !== false) {
      fail("portable checkout authority boundary drift");
    }
    return receipt;
  }

  function buildEnvelope(body, checkout, lease) {
    var receipt = validateCheckout(checkout);
    if (!lease || lease.issuer !== "TV/TVC" || lease.credential_authority !== "TV/TVC" || lease.lease_state !== "ACTIVE") {
      fail("exact active TVC lease required");
    }
    return {
      schema: "stegverse.external-resident-task-envelope/v1",
      profile_id: PROFILE,
      task_id: TASK_ID,
      execution_surface: "CURRENT_USER_IPHONE",
      node_id: body.node_id,
      worker_admission: {
        authority_source: "WorkerCoordinator",
        admitted: true,
        task_id: TASK_ID,
        worker_id: WORKER_ID,
        claim_id: receipt.claim_id,
        fencing_token: receipt.fencing_token,
        admission_receipt_sha256: receipt.receipt_sha256
      },
      lease: lease,
      credential_authority: "TV/TVC",
      github_token_required: false,
      external_non_stegverse_machine_required: false,
      canonical_workercoordinator_checkout_receipt: receipt,
      canonical_workercoordinator_state: checkout.state,
      portable_authority_epoch: receipt.portable_authority_epoch,
      heartbeat_granted_authority: false,
      global_workercoordinator_authority_owned_by_browser: false,
      stegos_tvc_issuance_authority: false,
      authority_effect: "PORTABLE_CANONICAL_ADMISSION_TO_SUBORDINATE_DEVICE_EXECUTION"
    };
  }

  self.StegOSPortableWorkerCoordinatorAdapter = {
    executeSv001: function (body, api) {
      validateInput(body);
      if (!self.StegVersePortableWorkerCoordinator || typeof self.StegVersePortableWorkerCoordinator.checkout !== "function") {
        return Promise.reject(new Error("FAIL_CLOSED: canonical portable WorkerCoordinator module unavailable"));
      }
      if (!api || typeof api.loadPackage !== "function" || typeof api.portableStateStore !== "function" ||
          typeof api.appendReceipt !== "function" || typeof api.issueTvcLease !== "function" ||
          typeof api.consumeTvcLease !== "function" || typeof api.executeExternalResidentTask !== "function") {
        return Promise.reject(new Error("FAIL_CLOSED: portable adapter API incomplete"));
      }

      var checkoutResult;
      var checkoutJournalEntry;
      var tvcResult;
      var tvcIssuanceJournalEntry;
      var executionProof;
      return api.loadPackage().then(function (pkg) {
        if (!pkg || pkg.task.task_id !== TASK_ID || pkg.execution_surface !== "CURRENT_USER_IPHONE") {
          fail("canonical portable SV001 package mismatch");
        }
        return self.StegVersePortableWorkerCoordinator.checkout(pkg, api.portableStateStore());
      }).then(function (checkout) {
        checkoutResult = checkout;
        validateCheckout(checkout);
        return api.appendReceipt(checkout.receipt);
      }).then(function (entry) {
        checkoutJournalEntry = entry;
        return api.issueTvcLease(checkoutResult.receipt);
      }).then(function (result) {
        tvcResult = result;
        if (!result || !result.lease || !result.issuance_receipt ||
            result.issuance_receipt.transition_id !== "TVC_SV001_BOUNDED_AUTONOMY_LEASE_ISSUED") {
          fail("authentic portable TVC lease issuance result required");
        }
        return api.appendReceipt(result.issuance_receipt);
      }).then(function (entry) {
        tvcIssuanceJournalEntry = entry;
        var envelope = buildEnvelope(body, checkoutResult, tvcResult.lease);
        envelope.canonical_workercoordinator_checkout_journal_entry_sha256 = checkoutJournalEntry.entry_sha256;
        envelope.tvc_issuance_receipt_hash = tvcResult.issuance_receipt.receipt_hash;
        envelope.tvc_issuance_journal_entry_sha256 = tvcIssuanceJournalEntry.entry_sha256;
        return api.executeExternalResidentTask(envelope);
      }).then(function (proof) {
        executionProof = proof;
        if (!proof || proof.state !== "COMPLETED" || proof.transition_id !== "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED" ||
            !proof.cycle_receipt || !/^sha256:[a-f0-9]{64}$/.test(proof.cycle_receipt.receipt_hash || "")) {
          fail("terminal SV001 execution proof required before TVC lease consumption");
        }
        return api.consumeTvcLease(tvcResult.lease.lease_id, proof.cycle_receipt.receipt_hash);
      }).then(function (consumedState) {
        if (!consumedState || consumedState.lease_consumption_state !== "CONSUMED") {
          fail("TVC portable lease consumption did not commit");
        }
        return api.appendReceipt({
          schema: "stegos.tvc_portable_sv001_lease_consumption_projection/v1",
          lease_id: tvcResult.lease.lease_id,
          lease_hash: tvcResult.lease.lease_hash,
          tvc_issuance_receipt_hash: tvcResult.issuance_receipt.receipt_hash,
          execution_receipt_sha256: executionProof.cycle_receipt.receipt_hash,
          tvc_state_sequence: consumedState.state_sequence,
          lease_consumption_state: consumedState.lease_consumption_state,
          source_authority: "TV/TVC",
          stegos_tvc_issuance_authority: false,
          credential_authority: "TV/TVC",
          github_token_runtime_authority: "NONE",
          heartbeat_granted_authority: false,
          authority_effect: "TVC_STATE_PROJECTION_ONLY",
          projected_at: new Date().toISOString()
        });
      }).then(function (consumptionEntry) {
        return {
          schema: "stegos.workercoordinator_tvc_portable_sv001_execution_proof/v1",
          state: "COMPLETED",
          task_id: TASK_ID,
          execution_surface: "CURRENT_USER_IPHONE",
          claim_id: checkoutResult.receipt.claim_id,
          fencing_token: checkoutResult.receipt.fencing_token,
          checkout_receipt_sha256: checkoutResult.receipt.receipt_sha256,
          checkout_journal_entry_sha256: checkoutJournalEntry.entry_sha256,
          tvc_lease_id: tvcResult.lease.lease_id,
          tvc_lease_hash: tvcResult.lease.lease_hash,
          tvc_issuance_receipt_hash: tvcResult.issuance_receipt.receipt_hash,
          tvc_issuance_journal_entry_sha256: tvcIssuanceJournalEntry.entry_sha256,
          tvc_consumption_journal_entry_sha256: consumptionEntry.entry_sha256,
          tvc_lease_consumption_state: "CONSUMED",
          subordinate_execution_proof: executionProof,
          global_workercoordinator_authority_owned_by_browser: false,
          stegos_device_task_generation_used_as_workercoordinator_fence: false,
          stegos_tvc_issuance_authority: false,
          credential_authority: "TV/TVC",
          github_token_runtime_authority: "NONE",
          heartbeat_granted_authority: false,
          external_non_stegverse_machine_required: false,
          authority_effect: "DEVICE_LOCAL_EXECUTION_OF_CANONICALLY_ADMITTED_TVC_LEASED_TASK"
        };
      });
    },
    profileId: PROFILE,
    taskId: TASK_ID
  };
}());
