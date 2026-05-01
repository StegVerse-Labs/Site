const sampleRun = {
  source: "llm_adapter",
  demo_id: "stale_state_commit_demo",
  run_id: "browser_tier0_example_001",
  intent: {
    action: "delete_resource",
    target: "cloud_volume_123",
    reason: "cleanup unused infrastructure"
  },
  state_at_evaluation: {
    resource_exists: true,
    owner: "agent_a",
    locked: false,
    dependency_count: 0
  },
  state_at_commit: {
    resource_exists: true,
    owner: "agent_b",
    locked: true,
    dependency_count: 2
  },
  authority_at_commit: {
    actor: "agent_a",
    scope: "delete_resource",
    valid: true
  }
};

function stableStringify(value) {
  if (Array.isArray(value)) return "[" + value.map(stableStringify).join(",") + "]";
  if (value && typeof value === "object") {
    return "{" + Object.keys(value).sort().map(k => JSON.stringify(k) + ":" + stableStringify(value[k])).join(",") + "}";
  }
  return JSON.stringify(value);
}

async function sha256(text) {
  const data = new TextEncoder().encode(text);
  const hash = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, "0")).join("");
}

function diffState(before = {}, after = {}) {
  const keys = new Set([...Object.keys(before), ...Object.keys(after)]);
  const changes = [];
  for (const key of keys) {
    if (JSON.stringify(before[key]) !== JSON.stringify(after[key])) {
      changes.push({
        field: key,
        evaluated: before[key],
        commit: after[key]
      });
    }
  }
  return changes;
}

function evaluateRun(input) {
  const failed_checks = [];
  const warnings = [];

  if (!input || typeof input !== "object") {
    return {
      decision: "FAIL_CLOSED",
      execution_allowed: false,
      reason: "payload is not a JSON object",
      failed_checks: ["invalid_payload"]
    };
  }

  for (const field of ["intent", "state_at_evaluation", "state_at_commit", "authority_at_commit"]) {
    if (!input[field] || typeof input[field] !== "object") {
      failed_checks.push(`missing_${field}`);
    }
  }

  if (failed_checks.length) {
    return {
      decision: "FAIL_CLOSED",
      execution_allowed: false,
      reason: "required commit evidence is missing",
      failed_checks
    };
  }

  const intent = input.intent;
  const evalState = input.state_at_evaluation;
  const commitState = input.state_at_commit;
  const authority = input.authority_at_commit;
  const state_changes = diffState(evalState, commitState);

  if (!authority.valid) failed_checks.push("authority_invalid");
  if (authority.actor && commitState.owner && authority.actor !== commitState.owner) failed_checks.push("actor_not_current_owner");
  if (commitState.locked === true) failed_checks.push("resource_locked_at_commit");
  if (commitState.resource_exists === false) failed_checks.push("resource_missing_at_commit");
  if (Number(commitState.dependency_count || 0) > 0 && intent.action === "delete_resource") {
    failed_checks.push("delete_blocked_by_commit_dependencies");
  }

  if (state_changes.length) warnings.push("state_changed_between_evaluation_and_commit");

  if (failed_checks.length) {
    return {
      decision: "DENY",
      execution_allowed: false,
      reason: "commit-time state or authority invalidates the proposed action",
      boundary: "commit",
      failed_checks,
      warnings,
      state_changes
    };
  }

  if (state_changes.length) {
    return {
      decision: "FAIL_CLOSED",
      execution_allowed: false,
      reason: "state changed and no stronger proof was supplied to preserve admissibility",
      boundary: "commit",
      failed_checks: ["state_changed_without_reconciliation_proof"],
      warnings,
      state_changes
    };
  }

  return {
    decision: "ALLOW",
    execution_allowed: true,
    reason: "state, authority, and admissibility all hold at commit",
    boundary: "commit",
    failed_checks: [],
    warnings,
    state_changes
  };
}

async function runDemo() {
  const inputEl = document.getElementById("payload");
  const outputEl = document.getElementById("resultJson");
  const bannerEl = document.getElementById("resultBanner");

  let input;
  try {
    input = JSON.parse(inputEl.value);
  } catch (err) {
    const result = {
      decision: "FAIL_CLOSED",
      execution_allowed: false,
      reason: "invalid JSON",
      failed_checks: ["json_parse_error"],
      error: err.message
    };
    renderResult(result, outputEl, bannerEl);
    return;
  }

  const result = evaluateRun(input);
  const receiptBase = {
    receipt_type: "stegverse_browser_tier0_commit_receipt",
    generated_at: new Date().toISOString(),
    input_hash: await sha256(stableStringify(input)),
    result_hash_basis: result
  };
  const receipt_hash = await sha256(stableStringify(receiptBase));
  renderResult({ ...result, receipt_hash, receipt: receiptBase }, outputEl, bannerEl);
}

function renderResult(result, outputEl, bannerEl) {
  const cls = result.decision === "ALLOW" ? "allow" : result.decision === "DENY" ? "deny" : "fail";
  bannerEl.innerHTML = `
    <span class="kicker">Commit decision</span>
    <strong class="${cls}">${result.decision}</strong>
    <div class="small">${result.reason || ""}</div>
  `;
  outputEl.textContent = JSON.stringify(result, null, 2);
}

function loadSample() {
  document.getElementById("payload").value = JSON.stringify(sampleRun, null, 2);
  runDemo();
}

function copyResult() {
  const text = document.getElementById("resultJson").textContent;
  navigator.clipboard.writeText(text);
}

function downloadResult() {
  const text = document.getElementById("resultJson").textContent;
  const blob = new Blob([text], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "stegverse-commit-receipt.json";
  a.click();
  URL.revokeObjectURL(url);
}

window.addEventListener("DOMContentLoaded", () => {
  const payload = document.getElementById("payload");
  if (payload) loadSample();

  document.getElementById("runDemo")?.addEventListener("click", runDemo);
  document.getElementById("loadSample")?.addEventListener("click", loadSample);
  document.getElementById("copyResult")?.addEventListener("click", copyResult);
  document.getElementById("downloadResult")?.addEventListener("click", downloadResult);
});