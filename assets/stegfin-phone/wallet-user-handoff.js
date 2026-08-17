(() => {
  'use strict';

  const WALLET_HANDOFF_KEY = 'stegverse.stegfin.wallet-handoff-ready.v1';
  const USER_HANDOFF_STATE_KEY = 'stegverse.stegfin.user-wallet-handoff.v1';
  const EXPECTED_CHAIN_ID = '0x2105';
  const EXPECTED_WALLET = '0xA503DCe5471492bbA2D06e9f78F4d9D6Bcc852aA'.toLowerCase();
  const PREPARE_MIN_VALIDITY_MS = 5 * 60 * 1000;
  const RPC_URL = 'https://mainnet.base.org';
  const RECEIPT_POLL_MS = 1500;
  const RECEIPT_MAX_POLLS = 40;

  function stable(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stable(value[key])}`).join(',')}}`;
  }

  function hex(buffer) {
    return [...new Uint8Array(buffer)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  async function sha256(value) {
    return `sha256:${hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(stable(value))))}`;
  }

  function parseTime(value, label) {
    const parsed = Date.parse(String(value || ''));
    if (!Number.isFinite(parsed)) throw new Error(`${label} timestamp missing or invalid`);
    return parsed;
  }

  function assertCurrentPrepareEvidence(result) {
    const receipt = result?.receipt || {};
    const evidence = receipt.stegid_admission_evidence || {};
    const identity = evidence.identity_continuity || {};
    const device = evidence.device_admission || {};
    const capability = evidence.wallet_capability || {};
    const now = Date.now();
    if (receipt.state !== 'WALLET_HANDOFF_READY') throw new Error('terminal wallet handoff missing');
    if (receipt.credential_authority !== 'TV/TVC' || receipt.credential_requirement !== 'NONE') throw new Error('credential boundary mismatch');
    if (receipt.non_tv_tvc_secret_or_token_used !== false || receipt.hosted_runtime_required !== false) throw new Error('hosted/non-TV authority prohibited');
    if (receipt.signed !== false || receipt.broadcast !== false) throw new Error('wallet handoff must remain unsigned/unbroadcast');
    if (identity.decision !== 'IDENTITY_CONTINUITY_VALID' || device.decision !== 'DEVICE_ADMITTED' || capability.decision !== 'ALLOW_DEVICE_WALLET_CAPABILITY') {
      throw new Error('current StegID admission evidence missing');
    }
    for (const [label, row] of [['identity', identity], ['device', device], ['capability', capability]]) {
      const expires = parseTime(row.expires_at, `${label} expires_at`);
      if (expires <= now + PREPARE_MIN_VALIDITY_MS) throw new Error(`${label} PREPARE evidence expired or expires too soon`);
    }
    const steps = Array.isArray(device.validation_steps) ? device.validation_steps : [];
    for (const required of ['DEVICE_POSSESSION', 'HUMAN_CONTINUITY', 'IDENTITY_CONTINUITY']) {
      if (!steps.includes(required)) throw new Error(`device evidence missing ${required}`);
    }
    const grants = Array.isArray(capability.granted_capabilities) ? capability.granted_capabilities : [];
    if (!grants.includes('PREPARE') || grants.includes('SIGN') || grants.includes('BROADCAST')) throw new Error('PREPARE capability boundary mismatch');
    return result;
  }

  async function validateCandidate(result) {
    assertCurrentPrepareEvidence(result);
    const handoff = result.wallet_handoff || {};
    const candidate = handoff.transaction_candidate || {};
    if (handoff.chain_id !== EXPECTED_CHAIN_ID || candidate.chain_id !== EXPECTED_CHAIN_ID) throw new Error('candidate chain mismatch');
    if (String(handoff.wallet_address || '').toLowerCase() !== EXPECTED_WALLET) throw new Error('wallet handoff address mismatch');
    if (String(candidate.from || '').toLowerCase() !== EXPECTED_WALLET) throw new Error('candidate sender mismatch');
    if (!candidate.to || !candidate.data || !candidate.candidate_hash) throw new Error('candidate incomplete');
    if (candidate.value === undefined || candidate.value === null) throw new Error('candidate value missing');
    if (candidate.requires_user_wallet_signature !== true) throw new Error('USER_ONLY wallet signature boundary missing');
    if (candidate.signed !== false || candidate.broadcast !== false) throw new Error('candidate must be unsigned/unbroadcast');
    if (handoff.wallet_is_only_signing_authority !== true || handoff.explicit_wallet_confirmation_required !== true) throw new Error('wallet authority confirmation boundary missing');
    if (handoff.automatic_signing !== false || handoff.automatic_broadcast !== false) throw new Error('automatic wallet action prohibited');
    const candidateMaterial = { ...candidate };
    delete candidateMaterial.candidate_hash;
    if (candidate.candidate_hash !== await sha256(candidateMaterial)) throw new Error('candidate hash mismatch');
    return { handoff, candidate };
  }

  function getRetainedResult() {
    try { return JSON.parse(localStorage.getItem(WALLET_HANDOFF_KEY) || 'null'); } catch { return null; }
  }

  function persistState(state) {
    localStorage.setItem(USER_HANDOFF_STATE_KEY, JSON.stringify(state));
    window.dispatchEvent(new CustomEvent('stegfin:user-wallet-handoff-state', { detail: state }));
    return state;
  }

  function getState() {
    try { return JSON.parse(localStorage.getItem(USER_HANDOFF_STATE_KEY) || 'null'); } catch { return null; }
  }

  function normalizeHexQuantity(value) {
    const text = String(value || '0x0').toLowerCase();
    if (!/^0x[0-9a-f]+$/.test(text)) throw new Error('invalid hex quantity');
    return `0x${BigInt(text).toString(16)}`;
  }

  function transactionRequest(candidate) {
    const tx = { from: candidate.from, to: candidate.to, value: normalizeHexQuantity(candidate.value), data: candidate.data };
    if (candidate.gas) tx.gas = normalizeHexQuantity(candidate.gas);
    if (candidate.gas_price) tx.gasPrice = normalizeHexQuantity(candidate.gas_price);
    return tx;
  }

  async function requireInjectedWallet() {
    const provider = window.ethereum;
    if (!provider || typeof provider.request !== 'function') throw new Error('No injected EIP-1193 wallet is available in this browser. No wallet action occurred.');
    const chainId = String(await provider.request({ method: 'eth_chainId' }) || '').toLowerCase();
    if (chainId !== EXPECTED_CHAIN_ID) throw new Error(`Wallet must already be on Base ${EXPECTED_CHAIN_ID}; automatic network switching is prohibited.`);
    const accounts = await provider.request({ method: 'eth_requestAccounts' });
    if (!Array.isArray(accounts) || String(accounts[0] || '').toLowerCase() !== EXPECTED_WALLET) throw new Error('Connected wallet account does not match the governed wallet');
    return provider;
  }

  async function rpc(method, params) {
    const response = await fetch(RPC_URL, {
      method: 'POST', credentials: 'omit', cache: 'no-store', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ jsonrpc: '2.0', id: Date.now(), method, params }),
    });
    if (!response.ok) throw new Error(`Base RPC HTTP ${response.status}`);
    const payload = await response.json();
    if (payload?.error) throw new Error(`Base RPC ${method} error: ${payload.error.message || payload.error.code}`);
    return payload?.result;
  }

  function sleep(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }

  async function observeReceipt(txHash) {
    for (let i = 0; i < RECEIPT_MAX_POLLS; i += 1) {
      const receipt = await rpc('eth_getTransactionReceipt', [txHash]);
      if (receipt) return receipt;
      await sleep(RECEIPT_POLL_MS);
    }
    return null;
  }

  function confirmedReprepareState(previous, chainReceipt) {
    localStorage.removeItem(WALLET_HANDOFF_KEY);
    return persistState({
      schema: 'stegwallet.user_only_wallet_handoff_state.v1',
      state: 'CONFIRMED_REPREPARE_REQUIRED',
      prior_candidate_sha256: previous.candidate_sha256,
      transaction_hash: previous.transaction_hash,
      block_number: chainReceipt?.blockNumber || null,
      transaction_success: true,
      settlement_observed: true,
      stale_quote_reuse_allowed: false,
      stale_simulation_reuse_allowed: false,
      stale_candidate_reuse_allowed: false,
      successor_prepare_requires_user_presence: true,
      wallet_signing_authority: 'USER_ONLY',
      broadcast_authority: 'USER_ONLY',
      automatic_signing: false,
      automatic_broadcast: false,
      credential_authority: 'TV/TVC',
      credential_requirement: 'NONE',
      non_tv_tvc_secret_or_token_used: false,
      updated_at: new Date().toISOString(),
    });
  }

  async function observeSubmittedTransaction() {
    const state = getState();
    if (!state?.transaction_hash || !['SUBMITTED_NOT_SETTLED', 'SUBMITTED_AWAITING_CHAIN_RECEIPT'].includes(state.state)) {
      throw new Error('no submitted transaction awaits chain observation');
    }
    const chainReceipt = await observeReceipt(state.transaction_hash);
    if (!chainReceipt) return persistState({ ...state, state: 'SUBMITTED_AWAITING_CHAIN_RECEIPT', updated_at: new Date().toISOString() });
    if (String(chainReceipt.status || '').toLowerCase() !== '0x1') {
      return persistState({ ...state, state: 'CHAIN_RECEIPT_FAILED', block_number: chainReceipt.blockNumber || null, settlement_observed: true, transaction_success: false, updated_at: new Date().toISOString() });
    }
    return confirmedReprepareState(state, chainReceipt);
  }

  async function prepareSuccessorByUserAction() {
    const state = getState();
    if (state?.state !== 'CONFIRMED_REPREPARE_REQUIRED' || !state.transaction_hash) throw new Error('confirmed transaction evidence required before successor PREPARE');
    const continuity = window.StegFinPhoneContinuity;
    if (!continuity || typeof continuity.run !== 'function') throw new Error('successor PREPARE runtime unavailable');
    const successor = await continuity.run();
    if (successor?.receipt?.state !== 'WALLET_HANDOFF_READY') throw new Error('successor PREPARE did not produce WALLET_HANDOFF_READY');
    const next = persistState({
      schema: 'stegwallet.user_only_wallet_handoff_state.v1',
      state: 'SUCCESSOR_WALLET_HANDOFF_READY',
      prior_transaction_hash: state.transaction_hash,
      prior_transaction_block: state.block_number || null,
      successor_receipt_sha256: successor.receipt.receipt_sha256,
      successor_bundle_sha256: successor.wallet_handoff?.bundle_sha256 || null,
      successor_candidate_sha256: successor.wallet_handoff?.transaction_candidate?.candidate_hash || null,
      successor_purpose: successor.wallet_handoff?.transaction_candidate?.purpose || null,
      wallet_signing_authority: 'USER_ONLY',
      broadcast_authority: 'USER_ONLY',
      automatic_signing: false,
      automatic_broadcast: false,
      credential_authority: 'TV/TVC',
      credential_requirement: 'NONE',
      non_tv_tvc_secret_or_token_used: false,
      updated_at: new Date().toISOString(),
    });
    return { state: next, successor };
  }

  async function submitExactCandidateByUserAction() {
    const retained = getRetainedResult();
    const { candidate } = await validateCandidate(retained);
    const provider = await requireInjectedWallet();
    const tx = transactionRequest(candidate);
    persistState({
      schema: 'stegwallet.user_only_wallet_handoff_state.v1',
      state: 'AWAITING_USER_WALLET_CONFIRMATION',
      candidate_sha256: candidate.candidate_hash,
      transaction_request_sha256: await sha256(tx),
      transaction_request: tx,
      wallet_signing_authority: 'USER_ONLY',
      broadcast_authority: 'USER_ONLY',
      automatic_signing: false,
      automatic_broadcast: false,
      updated_at: new Date().toISOString(),
    });

    let txHash;
    try {
      txHash = await provider.request({ method: 'eth_sendTransaction', params: [tx] });
    } catch (error) {
      persistState({
        schema: 'stegwallet.user_only_wallet_handoff_state.v1',
        state: 'USER_DECLINED_OR_WALLET_REJECTED',
        candidate_sha256: candidate.candidate_hash,
        wallet_signing_authority: 'USER_ONLY',
        broadcast_authority: 'USER_ONLY',
        automatic_signing: false,
        automatic_broadcast: false,
        error: String(error?.message || error),
        updated_at: new Date().toISOString(),
      });
      throw error;
    }
    if (!/^0x[0-9a-fA-F]{64}$/.test(String(txHash || ''))) throw new Error('wallet returned invalid transaction hash');

    persistState({
      schema: 'stegwallet.user_only_wallet_handoff_state.v1',
      state: 'SUBMITTED_NOT_SETTLED',
      candidate_sha256: candidate.candidate_hash,
      transaction_request_sha256: await sha256(tx),
      transaction_hash: txHash,
      wallet_signing_authority: 'USER_ONLY',
      broadcast_authority: 'USER_ONLY',
      wallet_submission_observed: true,
      settlement_observed: false,
      updated_at: new Date().toISOString(),
    });
    return observeSubmittedTransaction();
  }

  window.StegFinUserWalletHandoff = Object.freeze({
    schema: 'stegwallet.user_only_wallet_handoff_runtime.v1',
    submitExactCandidateByUserAction,
    observeSubmittedTransaction,
    prepareSuccessorByUserAction,
    getState,
    getRetainedResult,
    validateCandidate,
    credential_authority: 'TV/TVC',
    credential_requirement: 'NONE',
    non_tv_tvc_secret_or_token_used: false,
    hosted_runtime_required: false,
    render_required: false,
    wallet_signing_authority: 'USER_ONLY',
    broadcast_authority: 'USER_ONLY',
    automatic_signing: false,
    automatic_broadcast: false,
  });
})();
