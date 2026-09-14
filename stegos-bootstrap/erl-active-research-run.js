"use strict";

(function (root) {
  var PROFILE_ID = "ERL_ACTIVE_RESEARCH_INTR_SAME_DEVICE_V1";
  var TASK_ID = "SS-ERL-ACTIVE-RESEARCH-INTR-RUNTIME-BINDING-001";
  var COMPONENT_TASK_ID = "SS-ERL-SAME-DEVICE-PORTABLE-EXECUTION-001";
  var COSV = "40000100100000";
  var RECEIPT_SCHEMA = "stegverse.erl.same-device-portable-execution-receipt/v1";
  var ENDPOINT = "./resident-task";

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }

  function retainedExecution() {
    if (!root.StegOSWebBootstrap || typeof root.StegOSWebBootstrap.exportEvidence !== "function") {
      return Promise.reject(new Error("FAIL_CLOSED: StegOS evidence API unavailable"));
    }
    return root.StegOSWebBootstrap.exportEvidence().then(function (bundle) {
      var rows = bundle && Array.isArray(bundle.receipts) ? bundle.receipts : [];
      for (var i = rows.length - 1; i >= 0; i -= 1) {
        var receipt = rows[i] && rows[i].receipt;
        if (!receipt || receipt.schema !== RECEIPT_SCHEMA) { continue; }
        if (receipt.parent_task_id !== TASK_ID || receipt.component_task_id !== COMPONENT_TASK_ID || receipt.cosv_task_vector !== COSV) { continue; }
        if (receipt.state !== "ERL_TERMINAL_DEVICE_KV_OBSERVED" || receipt.complete_three_hop_chain_verified !== true || receipt.durable_payload_readback_verified !== true) { continue; }
        return { entry: rows[i], receipt: receipt, bundle: bundle };
      }
      return null;
    });
  }

  function envelope() {
    return {
      schema: "stegverse.external-resident-task-envelope/v1",
      profile_id: PROFILE_ID,
      task_id: TASK_ID,
      component_task_id: COMPONENT_TASK_ID,
      cosv_task_vector: COSV,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      heartbeat_granted_authority: false,
      provider_operation_reexecution_authorized: false,
      external_non_stegverse_machine_required: false,
      authority_effect: "NONE_REQUEST_ONLY"
    };
  }

  function submit() {
    if (!root.StegOSWebBootstrap || typeof root.StegOSWebBootstrap.registerOfflineShell !== "function") {
      return Promise.reject(new Error("FAIL_CLOSED: StegOS bootstrap API unavailable"));
    }
    return retainedExecution().then(function (retained) {
      if (retained) {
        return {
          schema: "stegverse.erl.authentic-intr-execution-invocation-result/v1",
          state: "ALREADY_OBSERVED_NO_RESUBMISSION",
          runtime_submission_performed: false,
          retained_entry_sha256: retained.entry.entry_sha256,
          execution_receipt: retained.receipt,
          authority_effect: "NONE_RETAINED_EVIDENCE_ONLY"
        };
      }
      return root.StegOSWebBootstrap.registerOfflineShell().then(function (registration) {
        if (!registration || registration.state !== "REGISTERED") { fail("StegOS service worker registration required"); }
        return navigator.serviceWorker.ready;
      }).then(function () {
        return fetch(new URL(ENDPOINT, root.location.href).toString(), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "same-origin",
          cache: "no-store",
          body: JSON.stringify(envelope())
        });
      }).then(function (response) {
        return response.json().then(function (payload) {
          if (!response.ok || !payload || payload.state !== "ERL_TERMINAL_DEVICE_KV_OBSERVED") {
            fail(payload && payload.reason ? payload.reason : "ERL resident task execution failed");
          }
          return payload;
        });
      }).then(function (payload) {
        return retainedExecution().then(function (retained) {
          if (!retained) { fail("terminal ERL execution returned without retained evidence receipt"); }
          return {
            schema: "stegverse.erl.authentic-intr-execution-invocation-result/v1",
            state: "ERL_TERMINAL_DEVICE_KV_OBSERVED",
            runtime_submission_performed: true,
            execution_result: payload,
            retained_entry_sha256: retained.entry.entry_sha256,
            execution_receipt: retained.receipt,
            authority_effect: "NONE_MACHINE_TRANSITION_EVIDENCE"
          };
        });
      });
    });
  }

  function masterRecordsEvidence(result) {
    var receipt = result && result.execution_receipt;
    if (!receipt || receipt.schema !== RECEIPT_SCHEMA || !Array.isArray(receipt.hop_receipts) || receipt.hop_receipts.length !== 3) {
      fail("complete retained ERL receipt required for Master Records evidence projection");
    }
    return {
      schema: "stegverse.master-records.universal-intr-receipt-chain-evidence/v1",
      artifact_id: "erl-active-research-" + receipt.operation_id,
      task_id: "SS-ERL-AUTHENTIC-INTR-EXECUTION-EVIDENCE-002",
      cosv_task_vector: COSV,
      operation_id: receipt.operation_id,
      packet_id: receipt.packet_id,
      payload_hash: receipt.payload_hash,
      boundary_path: ["EXTERNAL_SYSTEM", "STEGOS_ECOSYSTEM", "DEVICE_SYSTEM", "KV"],
      initial_prior_receipt_hash: null,
      receipts: receipt.hop_receipts,
      terminal_readback: {
        payload_hash: receipt.payload_hash,
        readback_hash: receipt.kv_payload_readback_sha256,
        exact_bytes_readback_verified: receipt.durable_payload_readback_verified === true
      },
      provider_proof_binding: receipt.provider_proof_binding,
      synthetic_evidence: false,
      authority_effect: "NONE_CUSTODY_INPUT_ONLY"
    };
  }

  root.StegOSERLActiveResearchInvoker = {
    profileId: PROFILE_ID,
    submit: submit,
    retainedExecution: retainedExecution,
    masterRecordsEvidence: masterRecordsEvidence
  };
}(window));
