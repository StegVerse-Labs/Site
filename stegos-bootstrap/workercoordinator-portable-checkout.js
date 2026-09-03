"use strict";

(function (root) {
  var PACKAGE_SCHEMA = "stegverse.workercoordinator-portable-checkout-package/v1";
  var STATE_SCHEMA = "stegverse.workercoordinator-portable-state/v1";
  var RECEIPT_SCHEMA = "stegverse.workercoordinator-portable-checkout-receipt/v1";

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }
  function isObject(value) { return value && typeof value === "object" && !Array.isArray(value); }
  function asPositiveInt(value, name) {
    if (!Number.isInteger(value) || value < 0) { fail(name + " must be a nonnegative integer"); }
    return value;
  }
  function hasAll(values, required) {
    return Array.isArray(values) && required.every(function (item) { return values.indexOf(item) !== -1; });
  }
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
  function sha256Hex(value) {
    var text = typeof value === "string" ? value : canonicalize(value);
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(function (digest) {
      return bytesToHex(new Uint8Array(digest));
    });
  }
  function validatePackage(pkg) {
    if (!isObject(pkg) || pkg.schema !== PACKAGE_SCHEMA) { fail("package schema mismatch"); }
    if (pkg.canonical_authority_owner !== "StegVerse-Labs/.github WorkerCoordinator") { fail("canonical authority owner mismatch"); }
    if (pkg.authority_domain !== "INDEPENDENT_TASK_CONTROL") { fail("authority domain mismatch"); }
    if (pkg.execution_surface !== "CURRENT_USER_IPHONE") { fail("portable execution surface mismatch"); }
    if (pkg.credential_authority !== "TV/TVC" || pkg.github_token_runtime_authority !== "NONE") { fail("credential boundary drift"); }
    if (pkg.heartbeat_grants_execution_authority !== false) { fail("heartbeat authority widening"); }
    if (pkg.parallel_workercoordinator_claim_issuance_allowed !== false) { fail("parallel WorkerCoordinator issuance prohibited"); }
    if (pkg.governed_transfer_required_before_other_surface_claims !== true) { fail("governed transfer invariant missing"); }
    asPositiveInt(pkg.predecessor_generation_floor, "predecessor_generation_floor");
    if (!/^([a-f0-9]{40})$/.test(pkg.predecessor_registry_git_blob_sha || "")) { fail("predecessor registry blob required"); }
    if (!pkg.portable_authority_epoch) { fail("portable authority epoch required"); }

    var task = pkg.task;
    var admission = task && task.admission;
    if (!task || task.state !== "HANDOFF_READY" || task.claim_id || task.worker_id) { fail("task not clean HANDOFF_READY"); }
    if (!admission || admission.authority_domain !== "INDEPENDENT_TASK_CONTROL") { fail("independent admission missing"); }
    if (admission.claim_state !== "AUTHORIZED_FOR_INDEPENDENT_TASK_CONTROL_CLAIM") { fail("claim state not authorized"); }
    if (admission.fresh_fence_required !== true || admission.heartbeat_grants_execution_authority !== false) { fail("fresh fence/heartbeat invariant invalid"); }
    if (pkg.dependencies_complete !== true || pkg.execution_authorized !== true || pkg.semantic_state_current !== true || pkg.worker_resolved !== true) {
      fail("portable preclaim predicates incomplete");
    }
    if (!isObject(pkg.handoff_authority) || pkg.handoff_authority.credential_authority !== "TV/TVC") { fail("handoff TV/TVC authority missing"); }
    if (pkg.handoff_authority.github_token_required !== false || pkg.handoff_authority.github_token_runtime_authority !== "NONE") {
      fail("handoff GitHub runtime authority drift");
    }
    if (pkg.handoff_authority.heartbeat_grants_execution_authority !== false) { fail("handoff heartbeat authority drift"); }
    if (!isObject(pkg.worker) || pkg.worker.status !== "AVAILABLE" || !pkg.worker.worker_id) { fail("worker unresolved/unavailable"); }
    if (!hasAll(pkg.worker.capabilities, pkg.required_capabilities || [])) { fail("worker capability mismatch"); }
    if (!isObject(pkg.source_binding) || !pkg.source_binding.task_fragment_git_blob_sha || !pkg.source_binding.handoff_git_blob_sha || !pkg.source_binding.state_vector_git_blob_sha) {
      fail("source binding incomplete");
    }
    return pkg;
  }
  function initialState(pkg) {
    return {
      schema: STATE_SCHEMA,
      portable_authority_epoch: pkg.portable_authority_epoch,
      canonical_authority_owner: pkg.canonical_authority_owner,
      execution_surface: "CURRENT_USER_IPHONE",
      predecessor_generation_floor: pkg.predecessor_generation_floor,
      predecessor_registry_git_blob_sha: pkg.predecessor_registry_git_blob_sha,
      generation: pkg.predecessor_generation_floor,
      checkout_tail_sha256: null,
      parallel_workercoordinator_claim_issuance_allowed: false,
      governed_transfer_required_before_other_surface_claims: true,
      credential_authority: "TV/TVC",
      authority_effect: "CANONICAL_WORKERCOORDINATOR_STATE"
    };
  }
  function checkout(pkg, store) {
    validatePackage(pkg);
    if (!store || typeof store.atomicCompareAndSwap !== "function") { fail("atomic state store required"); }
    return store.read().then(function (existing) {
      var state = existing || initialState(pkg);
      if (state.schema !== STATE_SCHEMA || state.portable_authority_epoch !== pkg.portable_authority_epoch) { fail("portable state lineage mismatch"); }
      if (state.predecessor_registry_git_blob_sha !== pkg.predecessor_registry_git_blob_sha) { fail("predecessor registry mismatch"); }
      if (state.parallel_workercoordinator_claim_issuance_allowed !== false) { fail("parallel issuance state invalid"); }
      var generation = asPositiveInt(state.generation, "state generation");
      if (generation < pkg.predecessor_generation_floor) { fail("portable generation regressed below predecessor floor"); }
      var minimum = pkg.minimum_fencing_token_exclusive;
      if (Number.isInteger(minimum) && generation <= minimum) { generation = minimum; }
      var nextGeneration = generation + 1;
      var claimId = "SHWP-" + pkg.task.task_id + "-G" + nextGeneration;
      var beforeHashPromise = sha256Hex(state);
      return beforeHashPromise.then(function (beforeHash) {
        var receiptBody = {
          schema: RECEIPT_SCHEMA,
          portable_authority_epoch: pkg.portable_authority_epoch,
          canonical_authority_owner: pkg.canonical_authority_owner,
          authority_domain: "INDEPENDENT_TASK_CONTROL",
          task_id: pkg.task.task_id,
          worker_id: pkg.worker.worker_id,
          claim_id: claimId,
          fencing_token: nextGeneration,
          predecessor_generation: state.generation,
          predecessor_state_sha256: "sha256:" + beforeHash,
          predecessor_registry_git_blob_sha: pkg.predecessor_registry_git_blob_sha,
          task_fragment_git_blob_sha: pkg.source_binding.task_fragment_git_blob_sha,
          handoff_git_blob_sha: pkg.source_binding.handoff_git_blob_sha,
          state_vector_git_blob_sha: pkg.source_binding.state_vector_git_blob_sha,
          execution_surface: "CURRENT_USER_IPHONE",
          heartbeat_reference: pkg.heartbeat_reference || null,
          heartbeat_granted_authority: false,
          credential_authority: "TV/TVC",
          github_token_runtime_authority: "NONE",
          global_workercoordinator_authority: true,
          stegos_device_task_authority: false,
          external_non_stegverse_machine_required: false,
          parallel_workercoordinator_claim_issuance_allowed: false,
          governed_transfer_required_before_other_surface_claims: true,
          authority_effect: "CANONICAL_WORKERCOORDINATOR_CLAIM_FENCE"
        };
        return sha256Hex(receiptBody).then(function (receiptHash) {
          receiptBody.receipt_sha256 = "sha256:" + receiptHash;
          var nextState = {
            schema: STATE_SCHEMA,
            portable_authority_epoch: pkg.portable_authority_epoch,
            canonical_authority_owner: pkg.canonical_authority_owner,
            execution_surface: "CURRENT_USER_IPHONE",
            predecessor_generation_floor: pkg.predecessor_generation_floor,
            predecessor_registry_git_blob_sha: pkg.predecessor_registry_git_blob_sha,
            generation: nextGeneration,
            checkout_tail_sha256: receiptBody.receipt_sha256,
            last_claim_id: claimId,
            last_task_id: pkg.task.task_id,
            parallel_workercoordinator_claim_issuance_allowed: false,
            governed_transfer_required_before_other_surface_claims: true,
            credential_authority: "TV/TVC",
            authority_effect: "CANONICAL_WORKERCOORDINATOR_STATE"
          };
          return store.atomicCompareAndSwap(state, nextState).then(function (committed) {
            if (committed !== true) { fail("atomic WorkerCoordinator checkout lost race or stale state"); }
            return { state: nextState, receipt: receiptBody };
          });
        });
      });
    });
  }

  root.StegVersePortableWorkerCoordinator = {
    packageSchema: PACKAGE_SCHEMA,
    stateSchema: STATE_SCHEMA,
    receiptSchema: RECEIPT_SCHEMA,
    canonicalize: canonicalize,
    sha256Hex: sha256Hex,
    validatePackage: validatePackage,
    initialState: initialState,
    checkout: checkout
  };
}(typeof self !== "undefined" ? self : globalThis));
