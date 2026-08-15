const READINESS_URL = "../task-state/STEGFIN-LIVE-ENTRY-003-READINESS.json";
const WALLET_READY = "WALLET_HANDOFF_READY";

const el = (id) => document.getElementById(id);

function shortWallet(value) {
  if (!value || value.length < 12) return value || "—";
  return `${value.slice(0, 6)}…${value.slice(-4)}`;
}

function localPhoneResult() {
  try {
    const value = JSON.parse(localStorage.getItem('stegverse.stegfin.wallet-handoff-ready.v1') || 'null');
    if (value?.receipt?.state !== WALLET_READY) return null;
    if (value.receipt.credential_authority !== 'TV/TVC') return null;
    if (value.receipt.credential_requirement !== 'NONE') return null;
    if (value.receipt.non_tv_tvc_secret_or_token_used !== false) return null;
    if (value.receipt.provider_secret_required !== false || value.receipt.provider_secret_exported !== false) return null;
    if (value.receipt.hosted_runtime_required !== false) return null;
    if (value.receipt.signed !== false || value.receipt.broadcast !== false) return null;
    return value;
  } catch { return null; }
}

function gateRows(state) {
  const local = localPhoneResult();
  const rows = [
    ["Source trade contract", state?.source_readiness?.exact_validation_trade_request],
    ["Phone sovereign carrier", local ? WALLET_READY : "READY_TO_RUN_ON_DEVICE"],
    ["TV/TVC direct-route admission", local ? "ROUTE_ADMITTED" : "READY_TO_RUN_ON_DEVICE"],
    ["Direct quote / allowance / simulation", local ? "COMPLETE" : "WAITING_FOR_DEVICE_EXECUTION"],
    ["Live receipt convergence", local ? "COMPLETE" : "WAITING_FOR_DEVICE_EXECUTION"],
    ["Wallet handoff", local ? WALLET_READY : "WAITING_FOR_LIVE_EVIDENCE"],
  ];
  return rows;
}

function render(state) {
  const boundary = state.trade_boundary || {};
  const credential = state.credential_boundary || {};
  const local = localPhoneResult();
  const ready = Boolean(local);

  el("stateBadge").textContent = ready ? WALLET_READY : (state.state || "READY_TO_RUN_ON_DEVICE");
  el("stateBadge").className = `badge ${ready ? "ready" : "pending"}`;
  el("chainLabel").textContent = `${boundary.chain || "Base"} · ${boundary.chain_id || "0x2105"}`;
  el("wallet").textContent = shortWallet(boundary.wallet || local?.wallet_handoff?.wallet_address);
  el("slippage").textContent = `${boundary.maximum_slippage_bps ?? 50} bps`;
  el("gasTx").textContent = `$${boundary.maximum_gas_per_transaction_usd ?? "1.00"}`;
  el("gasSession").textContent = `$${boundary.maximum_session_gas_usd ?? "3.00"}`;
  el("githubToken").textContent = "No";

  el("gateList").replaceChildren(...gateRows(state).map(([name, status]) => {
    const li = document.createElement("li");
    const terminal = String(status || "").includes("COMPLETE") || status === WALLET_READY || status === "READY_TO_RUN_ON_DEVICE" || status === "ROUTE_ADMITTED";
    li.innerHTML = `<span>${name}</span><strong class="${terminal ? "ok" : "wait"}">${status || "UNKNOWN"}</strong>`;
    return li;
  }));

  const button = el("reviewButton");
  button.disabled = !ready;
  button.dataset.authority = "USER_ONLY";
  el("actionMessage").textContent = ready
    ? "Canonical wallet-handoff evidence is present on this phone. Review the exact unsigned handoff before any USER_ONLY action."
    : "Use the phone-sovereign carrier above. This phone executes the TV/TVC-admitted credential-free direct Base route; signing and broadcast remain USER_ONLY.";

  button.onclick = () => {
    if (!ready) return;
    el("evidence").scrollIntoView({ behavior: "smooth", block: "start" });
  };

  el("evidence").textContent = JSON.stringify(local || {
    task_id: "STEGFIN-PHONE-DIRECT-ROUTE-010",
    state: "READY_TO_RUN_ON_DEVICE",
    trade_boundary: state.trade_boundary,
    credential_boundary: {
      credential_authority: "TV/TVC",
      credential_requirement: "NONE",
      non_tv_tvc_secret_or_token_used: false,
      provider_secret_required: false,
      github_token_required: false,
      hosted_runtime_required: false,
      wallet_signing_authority: "USER_ONLY",
      broadcast_authority: "USER_ONLY"
    },
    live_activation_pending: true
  }, null, 2);
}

async function loadCanonicalState() {
  const response = await fetch(READINESS_URL, { cache: "no-store", credentials: "omit" });
  if (!response.ok) throw new Error(`readiness HTTP ${response.status}`);
  const state = await response.json();
  if (state?.credential_boundary?.github_token_required !== false) throw new Error("canonical state violates no-GitHub-token boundary");
  return state;
}

async function main() {
  let state;
  try {
    state = await loadCanonicalState();
    render(state);
  } catch (error) {
    state = { state: "READY_TO_RUN_ON_DEVICE", trade_boundary: {}, credential_boundary: { github_token_required: false } };
    render(state);
    el("evidence").textContent = JSON.stringify({
      task_id: "STEGFIN-PHONE-DIRECT-ROUTE-010",
      state: "READY_TO_RUN_ON_DEVICE",
      canonical_readiness_document_unavailable: true,
      live_activation_pending: true,
      credential_authority: "TV/TVC",
      credential_requirement: "NONE",
      non_tv_tvc_secret_or_token_used: false,
      hosted_runtime_required: false,
      note: String(error)
    }, null, 2);
  }

  const prepare = el('prepareOnPhone');
  const phoneStatus = el('phoneStatus');
  prepare.onclick = async () => {
    if (!window.StegFinPhoneContinuity) {
      phoneStatus.textContent = 'Phone continuity runtime did not load. No wallet action occurred.';
      return;
    }
    prepare.disabled = true;
    phoneStatus.textContent = 'Preparing on this phone: StegID device verification → Inventory N → TV/TVC-admitted direct quote → allowance → gas → read-only simulation → unsigned wallet handoff…';
    try {
      const result = await window.StegFinPhoneContinuity.run();
      if (result?.receipt?.state !== WALLET_READY) throw new Error('terminal WALLET_HANDOFF_READY receipt missing');
      phoneStatus.textContent = 'WALLET_HANDOFF_READY produced and retained on this phone. Signing and broadcast remain USER_ONLY.';
      render(state);
    } catch (error) {
      phoneStatus.textContent = `Fail closed: ${String(error?.message || error)}`;
    } finally {
      prepare.disabled = false;
    }
  };
}

main();
