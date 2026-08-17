(() => {
  "use strict";

  const CONTRACT = Object.freeze({
    schema: "stegverse.iphone-heartbeat-transition-receipt/v1",
    contractId: "SHWP-IPHONE-HB30-TRANSITION-CAPSULE-001",
    sourceMerge: "9015c67d8356bf7e9e3db71488b2468581829e7a",
    seed: Object.freeze({
      repository: "StegVerse-Labs/.github",
      legacy_state_ref: "control/heartbeat-state.json",
      legacy_state_git_blob_sha: "d18d57d83cf19b7799cde1a1b4487e496eca7f76",
      epoch: 29,
      generation: 29
    }),
    successor: Object.freeze({
      schema: "stegverse.heartbeat-carrier-runtime-state/v1",
      epoch: 30,
      generation: 30,
      reference_frame: "heartbeat_epoch:30",
      activation_state: "ACTIVE",
      authority_effect: "NONE",
      legacy_hb29_immutable: true
    })
  });

  const STORAGE_KEY = "stegverse.iphone-heartbeat-transition-receipt.v1";
  const encoder = new TextEncoder();
  const byId = (id) => document.getElementById(id);

  function canonical(value) {
    if (value === null || typeof value !== "object") {
      return JSON.stringify(value);
    }
    if (Array.isArray(value)) {
      return "[" + value.map(canonical).join(",") + "]";
    }
    const keys = Object.keys(value).sort();
    return "{" + keys.map((key) => JSON.stringify(key) + ":" + canonical(value[key])).join(",") + "}";
  }

  async function sha256Hex(value) {
    const digest = await crypto.subtle.digest("SHA-256", encoder.encode(value));
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  }

  function isIPhone() {
    return /iPhone/i.test(navigator.userAgent || "");
  }

  function readiness() {
    const originOk = location.protocol === "https:" && location.hostname === "stegverse.org";
    const secureContext = window.isSecureContext === true;
    const webcrypto = Boolean(window.crypto && window.crypto.subtle && window.TextEncoder);
    const iphone = isIPhone();
    return {
      origin_ok: originOk,
      secure_context: secureContext,
      webcrypto,
      iphone,
      ready: originOk && secureContext && webcrypto && iphone
    };
  }

  function setReadiness() {
    const state = readiness();
    byId("origin-state").textContent = state.origin_ok ? "PASS" : "FAIL";
    byId("secure-state").textContent = state.secure_context ? "PASS" : "FAIL";
    byId("crypto-state").textContent = state.webcrypto ? "PASS" : "FAIL";
    byId("iphone-state").textContent = state.iphone ? "PASS" : "FAIL";
    byId("capsule-readiness").textContent = state.ready ? "READY" : "BLOCKED";
    byId("emit-transition").disabled = !state.ready;
    if (!state.ready) {
      byId("runtime-message").textContent = "Fail closed: exact HTTPS stegverse.org + secure context + WebCrypto + iPhone execution are required.";
    } else {
      byId("runtime-message").textContent = "Ready to emit a non-authorizing HB30 candidate receipt. No network request or credential is used.";
    }
    return state;
  }

  function baseReceipt() {
    return {
      schema: CONTRACT.schema,
      contract_id: CONTRACT.contractId,
      physical_execution_surface: "CURRENT_USER_IPHONE",
      executed_at: new Date().toISOString(),
      seed: {
        repository: CONTRACT.seed.repository,
        legacy_state_ref: CONTRACT.seed.legacy_state_ref,
        legacy_state_git_blob_sha: CONTRACT.seed.legacy_state_git_blob_sha,
        epoch: CONTRACT.seed.epoch,
        generation: CONTRACT.seed.generation
      },
      successor: {
        schema: CONTRACT.successor.schema,
        epoch: CONTRACT.successor.epoch,
        generation: CONTRACT.successor.generation,
        reference_frame: CONTRACT.successor.reference_frame,
        activation_state: CONTRACT.successor.activation_state,
        authority_effect: CONTRACT.successor.authority_effect,
        legacy_hb29_immutable: CONTRACT.successor.legacy_hb29_immutable
      },
      authority: {
        credential_authority: "TV/TVC",
        credential_requirement: "NONE",
        github_token_runtime_authority: "NONE",
        non_tv_tvc_secret_or_token_used: false,
        worker_authority: false,
        claim_or_fence_mutation: false,
        route_authority: false,
        wallet_authority: false,
        model_output_authority: "NONE",
        hosted_runtime_production_authority: "NONE",
        another_physical_machine_required: false
      },
      browser: {
        origin: location.origin,
        user_agent: navigator.userAgent,
        secure_context: window.isSecureContext === true,
        webcrypto: Boolean(window.crypto && window.crypto.subtle)
      }
    };
  }

  function showReceipt(receipt, persisted = false) {
    byId("transition-state").textContent = "HB30_CANDIDATE_EMITTED";
    byId("receipt-digest").textContent = receipt.receipt_sha256;
    byId("receipt-json").textContent = JSON.stringify(receipt, null, 2);
    byId("receipt-panel").hidden = false;
    byId("copy-receipt").disabled = false;
    byId("share-receipt").disabled = false;
    byId("runtime-message").textContent = persisted
      ? "Persisted portable receipt restored locally. Canonical HB30 is still NOT materialized until independent verification/materialization and WorkerCoordinator observation."
      : "Portable receipt emitted and persisted locally. Canonical HB30 is still NOT materialized until independent verification/materialization and WorkerCoordinator observation.";
  }

  async function emitTransition() {
    const state = setReadiness();
    if (!state.ready) return;
    const button = byId("emit-transition");
    button.disabled = true;
    byId("transition-state").textContent = "COMPUTING";
    try {
      const receipt = baseReceipt();
      receipt.receipt_sha256 = await sha256Hex(canonical(receipt));
      localStorage.setItem(STORAGE_KEY, JSON.stringify(receipt));
      showReceipt(receipt, false);
    } catch (error) {
      byId("transition-state").textContent = "FAIL_CLOSED";
      byId("runtime-message").textContent = "Receipt emission failed closed: " + String(error && error.message ? error.message : error);
    } finally {
      button.disabled = !readiness().ready;
    }
  }

  function currentReceipt() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (_) {
      return null;
    }
  }

  async function copyReceipt() {
    const receipt = currentReceipt();
    if (!receipt) return;
    const text = JSON.stringify(receipt, null, 2);
    try {
      await navigator.clipboard.writeText(text);
      byId("runtime-message").textContent = "Receipt copied. Copying grants no execution or authority.";
    } catch (_) {
      byId("receipt-json").focus();
      byId("runtime-message").textContent = "Clipboard API unavailable; the complete receipt remains visible for preservation.";
    }
  }

  async function shareReceipt() {
    const receipt = currentReceipt();
    if (!receipt) return;
    const text = JSON.stringify(receipt, null, 2);
    if (navigator.share) {
      try {
        await navigator.share({ title: "StegVerse HB30 transition receipt", text });
        return;
      } catch (_) {
        return;
      }
    }
    await copyReceipt();
  }

  function restore() {
    const receipt = currentReceipt();
    if (!receipt) return;
    if (receipt.schema !== CONTRACT.schema || receipt.contract_id !== CONTRACT.contractId) return;
    showReceipt(receipt, true);
  }

  function bindAction(id, handler) {
    const element = byId(id);
    element.addEventListener("click", handler, { passive: false });
    element.addEventListener("touchend", (event) => {
      event.preventDefault();
      handler();
    }, { passive: false });
  }

  document.addEventListener("DOMContentLoaded", () => {
    byId("source-merge").textContent = CONTRACT.sourceMerge;
    byId("seed-blob").textContent = CONTRACT.seed.legacy_state_git_blob_sha;
    setReadiness();
    restore();
    bindAction("emit-transition", emitTransition);
    bindAction("copy-receipt", copyReceipt);
    bindAction("share-receipt", shareReceipt);
  });
})();
