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

function atomicDisplay(value, decimals, symbol) {
  if (value === undefined || value === null || value === "") return "—";
  const text = String(value);
  if (!/^\d+$/.test(text) || !Number.isInteger(decimals) || decimals < 0) return `${text}${symbol ? ` atomic ${symbol}` : " atomic"}`;
  const padded = text.padStart(decimals + 1, '0');
  const whole = decimals ? padded.slice(0, -decimals) : padded;
  const fraction = decimals ? padded.slice(-decimals).replace(/0+$/, '') : '';
  return `${whole}${fraction ? `.${fraction}` : ''}${symbol ? ` ${symbol}` : ''}`;
}

function candidateAsset(local, candidate) {
  const assets = local?.inventory?.assets || [];
  const target = String(candidate?.to || '').toLowerCase();
  return assets.find((asset) => String(asset?.contract_address || '').toLowerCase() === target)
    || assets.find((asset) => asset?.symbol === 'USDC')
    || null;
}

function validateReviewableHandoff(local) {
  const receipt = local?.receipt || {};
  const handoff = local?.wallet_handoff || {};
  const candidate = handoff?.transaction_candidate || {};
  const route = local?.route_admission || {};
  if (receipt.state !== WALLET_READY) throw new Error('wallet handoff is not terminal');
  if (receipt.credential_authority !== 'TV/TVC' || receipt.credential_requirement !== 'NONE') throw new Error('wallet handoff credential boundary mismatch');
  if (receipt.non_tv_tvc_secret_or_token_used !== false || receipt.hosted_runtime_required !== false) throw new Error('wallet handoff authority boundary mismatch');
  if (handoff.chain_id !== '0x2105' || candidate.chain_id !== '0x2105') throw new Error('wallet handoff must target Base 0x2105');
  if (!handoff.wallet_address || String(candidate.from || '').toLowerCase() !== String(handoff.wallet_address).toLowerCase()) throw new Error('wallet handoff sender mismatch');
  if (!candidate.to || !candidate.purpose) throw new Error('wallet transaction candidate incomplete');
  if (candidate.requires_user_wallet_signature !== true) throw new Error('wallet signature must remain explicitly USER_ONLY');
  if (handoff.wallet_is_only_signing_authority !== true || handoff.explicit_wallet_confirmation_required !== true) throw new Error('wallet authority confirmation missing');
  if (handoff.automatic_signing !== false || handoff.automatic_broadcast !== false) throw new Error('automatic wallet action prohibited');
  if (handoff.signed !== false || handoff.broadcast !== false || receipt.signed !== false || receipt.broadcast !== false) throw new Error('review requires unsigned/unbroadcast handoff');
  if (route.decision !== 'ROUTE_ADMITTED' || route.authority !== 'TV/TVC' || route.credential_requirement !== 'NONE') throw new Error('TV/TVC route admission missing');
  return { receipt, handoff, candidate, route };
}

function walletReviewRows(local) {
  const { receipt, handoff, candidate, route } = validateReviewableHandoff(local);
  const asset = candidateAsset(local, candidate);
  const quote = local?.quote || {};
  const capability = receipt?.stegid_admission_evidence?.wallet_capability || {};
  const device = receipt?.stegid_admission_evidence?.device_admission || {};
  const rows = [
    ["State", WALLET_READY],
    ["Chain", "Base · 0x2105"],
    ["Wallet", handoff.wallet_address],
    ["Candidate purpose", candidate.purpose],
    [candidate.purpose === 'exact_erc20_approval' ? "Approval token contract" : "Transaction target", candidate.to],
  ];
  if (candidate.purpose === 'exact_erc20_approval') {
    rows.push(["Exact approval", atomicDisplay(candidate.exact_allowance_atomic, asset?.decimals, asset?.symbol)]);
    rows.push(["Unlimited allowance", candidate.unlimited_allowance === false ? "No" : String(candidate.unlimited_allowance)]);
    rows.push(["Spender / SwapRouter02", route?.route?.swap_router_02 || "—"]);
  } else {
    rows.push(["Amount in", atomicDisplay(quote.amount_in, asset?.decimals, asset?.symbol)]);
  }
  rows.push(
    ["Quote minimum out", quote.amount_out_minimum ? `${quote.amount_out_minimum} atomic WETH` : "—"],
    ["Fee tier", quote.fee !== undefined ? String(quote.fee) : "—"],
    ["Slippage ceiling", route.maximum_slippage_bps !== undefined ? `${route.maximum_slippage_bps} bps` : "—"],
    ["Gas estimate", candidate.gas_estimate_usd !== undefined ? `$${candidate.gas_estimate_usd}` : "—"],
    ["Gas reserve sufficient", candidate.gas_reserve_sufficient === true ? "Yes" : String(candidate.gas_reserve_sufficient ?? "—")],
    ["TV/TVC route", `${route.decision} · credentials ${route.credential_requirement}`],
    ["StegID device", device.decision || receipt.stegid_device_id || "Bound by receipt hash"],
    ["StegID capability", Array.isArray(capability.granted_capabilities) ? capability.granted_capabilities.join(' + ') : "Bound by capability receipt hash"],
    ["Wallet signature required", candidate.requires_user_wallet_signature === true ? "Yes · USER_ONLY" : "No"],
    ["Signed", "No"],
    ["Broadcast", "No"],
  );
  return rows;
}

function ensureWalletReviewCard() {
  let card = el('walletReviewCard');
  if (card) return card;
  const evidenceCard = document.querySelector('.evidence-card');
  card = document.createElement('section');
  card.id = 'walletReviewCard';
  card.className = 'card';
  card.hidden = true;
  card.setAttribute('aria-labelledby', 'walletReviewTitle');

  const head = document.createElement('div');
  head.className = 'card-head';
  const heading = document.createElement('div');
  const eyebrow = document.createElement('p');
  eyebrow.className = 'eyebrow';
  eyebrow.textContent = 'USER_ONLY review';
  const title = document.createElement('h2');
  title.id = 'walletReviewTitle';
  title.textContent = 'Unsigned wallet handoff';
  heading.append(eyebrow, title);
  head.append(heading);

  const copy = document.createElement('p');
  copy.className = 'status-copy';
  copy.textContent = 'Human-readable projection of the exact retained candidate. Review only: this control never contacts a wallet, signs, broadcasts, or settles.';

  const grid = document.createElement('div');
  grid.id = 'walletReviewGrid';
  grid.className = 'authority-grid';

  const warning = document.createElement('p');
  warning.className = 'muted';
  warning.textContent = 'Canonical JSON remains below for exact hash-bound evidence. Any mismatch fails closed and disables this review projection.';

  card.append(head, copy, grid, warning);
  evidenceCard?.parentNode?.insertBefore(card, evidenceCard);
  return card;
}

function renderWalletReview(local) {
  const card = ensureWalletReviewCard();
  const grid = el('walletReviewGrid');
  grid.replaceChildren();
  for (const [label, value] of walletReviewRows(local)) {
    const item = document.createElement('div');
    const name = document.createElement('span');
    const strong = document.createElement('strong');
    name.textContent = label;
    strong.textContent = value ?? '—';
    item.append(name, strong);
    grid.append(item);
  }
  card.hidden = false;
  return card;
}

function render(state) {
  const boundary = state.trade_boundary || {};
  const credential = state.credential_boundary || {};
  const local = localPhoneResult();
  let reviewable = false;
  if (local) {
    try { validateReviewableHandoff(local); reviewable = true; } catch { reviewable = false; }
  }
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
  button.disabled = !reviewable;
  button.dataset.authority = "USER_ONLY";
  el("actionMessage").textContent = reviewable
    ? "Canonical wallet-handoff evidence is present on this phone. Review the exact unsigned handoff before any USER_ONLY action."
    : ready
      ? "Wallet handoff exists, but the human-readable review failed a boundary check. Canonical evidence remains available; no wallet action is enabled."
      : "Use the phone-sovereign carrier above. This phone executes the TV/TVC-admitted credential-free direct Base route; signing and broadcast remain USER_ONLY.";

  button.onclick = () => {
    if (!reviewable) return;
    try {
      const card = renderWalletReview(local);
      card.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      button.disabled = true;
      el("actionMessage").textContent = `Fail closed: ${String(error?.message || error)}. No wallet action occurred.`;
    }
  };

  if (!reviewable) {
    const card = el('walletReviewCard');
    if (card) card.hidden = true;
  }

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
