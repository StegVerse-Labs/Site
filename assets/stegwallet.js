const BASE_CHAIN_ID = '0x2105';
const BASE_CHAIN = {
  chainId: BASE_CHAIN_ID,
  chainName: 'Base Mainnet',
  nativeCurrency: {name: 'Ether', symbol: 'ETH', decimals: 18},
  rpcUrls: ['https://mainnet.base.org'],
  blockExplorerUrls: ['https://basescan.org']
};

const state = {account: null, chainId: null, verifiedRequest: null, environment: null};
const $ = (id) => document.getElementById(id);

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonicalize(value[key])]));
  }
  return value;
}

async function sha256(value) {
  const bytes = new TextEncoder().encode(JSON.stringify(canonicalize(value)));
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return 'sha256:' + [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function provider() {
  if (!globalThis.ethereum || typeof globalThis.ethereum.request !== 'function') {
    throw new Error('No injected EIP-1193 wallet found. Open this page inside Base App, MetaMask, or another compatible wallet.');
  }
  return globalThis.ethereum;
}

function setStatus(element, message, kind = '') {
  element.textContent = message;
  element.classList.remove('ok', 'bad');
  if (kind) element.classList.add(kind);
}

function environmentRecord() {
  const injected = Boolean(globalThis.ethereum?.request);
  const ua = String(navigator.userAgent || '');
  const hints = [];
  if (/CoinbaseWallet|Base/i.test(ua)) hints.push('base_or_coinbase_browser_hint');
  if (/MetaMask/i.test(ua) || globalThis.ethereum?.isMetaMask) hints.push('metamask_hint');
  return {
    schema: 'stegwallet.browser_environment.v1',
    origin: location.origin,
    secure_context: globalThis.isSecureContext === true,
    injected_eip1193: injected,
    environment_hints: hints,
    environment_trusted_for_authority: false,
    observed_at: new Date().toISOString()
  };
}

async function refreshEnvironment() {
  state.environment = environmentRecord();
  state.environment.environment_sha256 = await sha256(state.environment);
  setStatus(
    $('environment-status'),
    `Origin: ${state.environment.origin}\nSecure context: ${state.environment.secure_context}\nInjected wallet: ${state.environment.injected_eip1193}\nHints: ${state.environment.environment_hints.join(', ') || 'none'}\nEnvironment grants authority: false`,
    state.environment.secure_context ? 'ok' : 'bad'
  );
}

function parseBasename(value) {
  const name = String(value || '').trim().toLowerCase();
  if (!name) return null;
  if (!/^[a-z0-9-]+\.base\.eth$/.test(name)) throw new Error('Basename alias must use the form name.base.eth.');
  return name;
}

function parseAddressAllowlist(value) {
  const addresses = [...new Set(String(value || '').split(',').map((item) => item.trim().toLowerCase()).filter(Boolean))];
  if (!addresses.length) throw new Error('At least one verified router address is required.');
  const invalid = addresses.find((address) => !/^0x[a-f0-9]{40}$/.test(address));
  if (invalid) throw new Error(`Invalid EVM router address: ${invalid}`);
  return addresses;
}

async function refreshWallet() {
  const p = provider();
  const [accounts, chainId] = await Promise.all([
    p.request({method: 'eth_accounts'}),
    p.request({method: 'eth_chainId'})
  ]);
  state.account = Array.isArray(accounts) && accounts.length ? accounts[0].toLowerCase() : null;
  state.chainId = String(chainId).toLowerCase();
  let balance = null;
  if (state.account) balance = await p.request({method: 'eth_getBalance', params: [state.account, 'latest']});
  const eth = balance ? Number(BigInt(balance)) / 1e18 : null;
  const alias = parseBasename($('basename-alias').value);
  setStatus(
    $('wallet-status'),
    state.account
      ? `Account: ${state.account}\nDisplay alias: ${alias || 'none'}\nChain: ${state.chainId}\nNative balance: ${eth?.toFixed(6) ?? 'unknown'} ETH\nCanonical identity: wallet address`
      : `Wallet available, but no account is connected.\nChain: ${state.chainId}`,
    state.account ? 'ok' : ''
  );
  $('send-request').disabled = !state.verifiedRequest;
}

async function connectWallet() {
  await provider().request({method: 'eth_requestAccounts'});
  await refreshWallet();
}

async function switchBase() {
  const p = provider();
  try {
    await p.request({method: 'wallet_switchEthereumChain', params: [{chainId: BASE_CHAIN_ID}]});
  } catch (error) {
    if (error?.code !== 4902) throw error;
    await p.request({method: 'wallet_addEthereumChain', params: [BASE_CHAIN]});
  }
  await refreshWallet();
}

function isoFromLocal(value) {
  if (!value) return new Date(Date.now() + 6 * 60 * 60 * 1000).toISOString();
  return new Date(value).toISOString();
}

async function buildGoal() {
  if (!state.account) throw new Error('Connect a wallet before creating the mandate.');
  if (!state.environment?.secure_context) throw new Error('A secure HTTPS context is required.');
  const mode = $('execution-mode').value;
  const delegationRef = $('delegation-ref').value.trim() || null;
  if (mode === 'delegated_bounded' && !delegationRef) throw new Error('Delegated mode requires a delegation reference.');
  if (mode === 'user_signature_required' && delegationRef) throw new Error('Remove the delegation reference for user-signature mode.');
  const routers = parseAddressAllowlist($('router-allowlist').value);
  const goalId = `goal:crypto:${crypto.randomUUID()}`;
  const mandate = {
    schema: 'stegwallet.goal_mandate.v1',
    goal_id: goalId,
    owner_id: `wallet:${state.account}`,
    wallet_address: state.account,
    basename_display_alias: parseBasename($('basename-alias').value),
    canonical_web_origin: location.origin,
    browser_environment_sha256: state.environment.environment_sha256,
    execution_mode: mode,
    allowed_chain_ids: [BASE_CHAIN_ID],
    allowed_assets: ['USDC', 'WETH'],
    allowed_router_addresses: routers,
    capital_limit_usd: Number($('capital-limit').value),
    max_position_usd: Number($('position-limit').value),
    max_realized_loss_usd: Number($('loss-limit').value),
    max_drawdown_usd: Number($('drawdown-limit').value),
    max_slippage_bps: Number($('slippage-limit').value),
    max_gas_usd: Number($('gas-limit').value),
    max_open_positions: Number($('position-count-limit').value),
    expires_at: isoFromLocal($('goal-expiry').value),
    signature_required_per_trade: mode === 'user_signature_required',
    delegation_ref: delegationRef,
    domain_grants_authority: false,
    basename_grants_authority: false,
    authority_granted: false,
    raw_private_key_allowed: false,
    created_at: new Date().toISOString()
  };
  if (mandate.max_position_usd > mandate.capital_limit_usd) throw new Error('Maximum position cannot exceed the capital ceiling.');
  mandate.mandate_sha256 = await sha256({...mandate});
  $('goal-output').value = JSON.stringify(mandate, null, 2);
}

async function verifySignatureRequest() {
  state.verifiedRequest = null;
  $('send-request').disabled = true;
  const payload = JSON.parse($('signature-input').value);
  const blockers = [];
  if (payload.schema !== 'stegwallet.signature_request.v1') blockers.push('unsupported_schema');
  if (payload.method !== 'eth_sendTransaction') blockers.push('unsupported_method');
  if (payload.private_key_requested !== false) blockers.push('private_key_boundary_violation');
  if (!payload.transaction || typeof payload.transaction !== 'object') blockers.push('transaction_missing');
  if (!state.account) blockers.push('wallet_not_connected');
  if (String(payload.wallet_address || '').toLowerCase() !== state.account) blockers.push('wallet_identity_mismatch');
  if (String(payload.chain_id || '').toLowerCase() !== state.chainId) blockers.push('chain_identity_mismatch');
  if (payload.requires_user_signature !== true) blockers.push('delegated_request_cannot_use_user_signing_surface');
  if (payload.delegation_ref) blockers.push('delegation_reference_present_in_user_mode');
  if (!String(payload.decision_sha256 || '').match(/^sha256:[a-f0-9]{64}$/)) blockers.push('decision_hash_missing');
  if (payload.transaction) {
    const actual = await sha256(payload.transaction);
    if (actual !== payload.transaction_sha256) blockers.push('transaction_commitment_mismatch');
    if (String(payload.transaction.from || '').toLowerCase() !== state.account) blockers.push('transaction_sender_mismatch');
    if (String(payload.transaction.chainId || '').toLowerCase() !== state.chainId) blockers.push('transaction_chain_mismatch');
  }
  if (blockers.length) {
    setStatus($('request-status'), `FAIL_CLOSED\n${blockers.join('\n')}`, 'bad');
    return;
  }
  state.verifiedRequest = payload;
  $('send-request').disabled = false;
  setStatus(
    $('request-status'),
    `VERIFIED FOR WALLET PROMPT\nGoal: ${payload.goal_id}\nProposal: ${payload.proposal_id}\nDecision: ${payload.decision_id}\nTransaction: ${payload.transaction_sha256}\n\nThe connected wallet remains the final execution authority.`,
    'ok'
  );
}

async function waitForReceipt(txHash, attempts = 120) {
  const p = provider();
  for (let i = 0; i < attempts; i += 1) {
    const receipt = await p.request({method: 'eth_getTransactionReceipt', params: [txHash]});
    if (receipt) return receipt;
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
  return null;
}

async function sendVerifiedRequest() {
  const request = state.verifiedRequest;
  if (!request) throw new Error('Verify an admitted signature request first.');
  const currentHash = await sha256(request.transaction);
  if (currentHash !== request.transaction_sha256) throw new Error('Transaction changed after verification.');
  const txHash = await provider().request({method: 'eth_sendTransaction', params: [request.transaction]});
  setStatus($('request-status'), `SUBMITTED\n${txHash}\nWaiting for settlement observation...`, 'ok');
  const receipt = await waitForReceipt(txHash);
  const observation = {
    schema: 'stegwallet.browser_settlement_observation.v1',
    goal_id: request.goal_id,
    proposal_id: request.proposal_id,
    signature_request_sha256: request.signature_request_sha256,
    transaction_sha256: request.transaction_sha256,
    transaction_hash: txHash,
    chain_id: state.chainId,
    wallet_address: state.account,
    basename_display_alias: parseBasename($('basename-alias').value),
    canonical_web_origin: location.origin,
    browser_environment_sha256: state.environment.environment_sha256,
    observed_at: new Date().toISOString(),
    settled: Boolean(receipt),
    receipt: receipt || null,
    execution_authority: 'wallet_user_signature',
    domain_granted_authority: false,
    custody_recorded: false,
    objective_verified: false
  };
  observation.observation_sha256 = await sha256(observation);
  $('settlement-output').value = JSON.stringify(observation, null, 2);
}

function download(id, name) {
  const content = $(id).value;
  if (!content) throw new Error('No record is available.');
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([content + '\n'], {type: 'application/json'}));
  link.download = name;
  link.click();
  URL.revokeObjectURL(link.href);
}

function guard(action) {
  return async () => {
    try { await action(); }
    catch (error) { setStatus($('request-status'), `FAIL_CLOSED\n${error.message}`, 'bad'); }
  };
}

$('connect-wallet').addEventListener('click', guard(connectWallet));
$('switch-base').addEventListener('click', guard(switchBase));
$('build-goal').addEventListener('click', guard(buildGoal));
$('verify-request').addEventListener('click', guard(verifySignatureRequest));
$('send-request').addEventListener('click', guard(sendVerifiedRequest));
$('download-goal').addEventListener('click', () => download('goal-output', 'stegwallet-goal-mandate.json'));
$('download-settlement').addEventListener('click', () => download('settlement-output', 'stegwallet-settlement-observation.json'));
$('copy-goal').addEventListener('click', guard(async () => navigator.clipboard.writeText($('goal-output').value)));
$('basename-alias').addEventListener('change', () => refreshWallet().catch(() => {}));

refreshEnvironment().catch(() => {});
if (globalThis.ethereum?.on) {
  globalThis.ethereum.on('accountsChanged', () => refreshWallet().catch(() => {}));
  globalThis.ethereum.on('chainChanged', () => refreshWallet().catch(() => {}));
  refreshWallet().catch(() => {});
}
