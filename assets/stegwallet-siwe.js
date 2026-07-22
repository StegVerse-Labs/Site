const CONFIG_URL = 'data/stegwallet-siwe-runtime.json';
const $ = (id) => document.getElementById(id);
const state = {config: null, session: null};

function setStatus(message, kind = '') {
  const element = $('siwe-status');
  element.textContent = message;
  element.classList.remove('ok', 'bad');
  if (kind) element.classList.add(kind);
}

function provider() {
  if (!globalThis.ethereum || typeof globalThis.ethereum.request !== 'function') {
    throw new Error('No injected EIP-1193 wallet is available.');
  }
  return globalThis.ethereum;
}

function validateEndpoint(value, canonicalOrigin) {
  const url = new URL(value);
  if (url.protocol !== 'https:') throw new Error('SIWE endpoints must use HTTPS.');
  if (url.origin !== canonicalOrigin) throw new Error('SIWE endpoints must use the canonical Site origin.');
  return url.href;
}

function validateConfig(config) {
  if (config.schema !== 'stegwallet.siwe_runtime_configuration.v1') throw new Error('Unsupported SIWE runtime configuration.');
  if (config.chain_id !== 8453) throw new Error('SIWE runtime must be bound to Base chain 8453.');
  if (config.transaction_authority !== false || config.execution_authority !== false || config.delegation_authority !== false) {
    throw new Error('SIWE configuration claims forbidden authority.');
  }
  if (config.wallet_authentication_enabled !== true) return false;
  if (config.state !== 'READY') throw new Error('Enabled SIWE configuration must be READY.');
  if (location.origin !== config.canonical_origin) throw new Error('Current Site origin does not match the SIWE canonical origin.');
  config.challenge_endpoint = validateEndpoint(config.challenge_endpoint, config.canonical_origin);
  config.verify_endpoint = validateEndpoint(config.verify_endpoint, config.canonical_origin);
  config.session_endpoint = validateEndpoint(config.session_endpoint, config.canonical_origin);
  return true;
}

async function loadConfig() {
  const response = await fetch(CONFIG_URL, {cache: 'no-store', credentials: 'same-origin'});
  if (!response.ok) throw new Error(`SIWE configuration unavailable (${response.status}).`);
  const config = await response.json();
  state.config = config;
  const enabled = validateConfig(config);
  $('siwe-sign-in').disabled = !enabled;
  if (!enabled) {
    setStatus(`CONFIGURATION_REQUIRED\n${(config.blockers || []).join('\n')}\n\nNo signature can be requested.`, 'bad');
    return;
  }
  setStatus('READY\nSIWE authentication endpoint configured. No transaction authority is granted.', 'ok');
}

async function accountAndChain() {
  const p = provider();
  const [accounts, chainId] = await Promise.all([
    p.request({method: 'eth_accounts'}),
    p.request({method: 'eth_chainId'})
  ]);
  const account = Array.isArray(accounts) && accounts.length ? String(accounts[0]).toLowerCase() : null;
  if (!account) throw new Error('Connect the wallet before signing in.');
  if (String(chainId).toLowerCase() !== '0x2105') throw new Error('Switch the wallet to Base mainnet before signing in.');
  return {account, chainId: 8453};
}

async function postJson(url, body) {
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'include',
    headers: {'content-type': 'application/json', 'accept': 'application/json'},
    body: JSON.stringify(body)
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || `SIWE endpoint failed (${response.status}).`);
  return payload;
}

function validateChallenge(challenge, account) {
  if (challenge.schema !== 'stegwallet.siwe_challenge.v1') throw new Error('Unsupported SIWE challenge.');
  if (String(challenge.address || '').toLowerCase() !== account) throw new Error('SIWE challenge wallet mismatch.');
  if (challenge.domain !== new URL(state.config.canonical_origin).host) throw new Error('SIWE challenge domain mismatch.');
  if (challenge.uri !== state.config.canonical_origin) throw new Error('SIWE challenge URI mismatch.');
  if (challenge.chain_id !== 8453) throw new Error('SIWE challenge chain mismatch.');
  if (challenge.wallet_authenticated !== false || challenge.transaction_authority !== false || challenge.execution_authority !== false) {
    throw new Error('SIWE challenge claims forbidden authority.');
  }
  if (typeof challenge.message !== 'string' || !challenge.message.includes('wants you to sign in with your Ethereum account:')) {
    throw new Error('Malformed EIP-4361 message.');
  }
}

function validateSession(receipt, account) {
  if (receipt.schema !== 'stegwallet.siwe_session_receipt.v1') throw new Error('Unsupported SIWE session receipt.');
  if (String(receipt.wallet_address || '').toLowerCase() !== account) throw new Error('SIWE session wallet mismatch.');
  if (receipt.wallet_authenticated !== true) throw new Error('SIWE session is not authenticated.');
  if (receipt.transaction_authority !== false || receipt.execution_authority !== false || receipt.delegation_authority !== false) {
    throw new Error('SIWE session claims forbidden authority.');
  }
  if (!/^sha256:[a-f0-9]{64}$/.test(String(receipt.session_sha256 || ''))) throw new Error('SIWE session hash missing.');
}

async function signIn() {
  if (!state.config || !validateConfig(state.config)) throw new Error('SIWE runtime is not ready.');
  const {account, chainId} = await accountAndChain();
  setStatus('REQUESTING CHALLENGE\nNo wallet signature has been requested yet.');
  const challenge = await postJson(state.config.challenge_endpoint, {
    schema: 'stegwallet.siwe_challenge_request.v1',
    wallet_address: account,
    chain_id: chainId,
    origin: location.origin,
    transaction_authority: false,
    execution_authority: false
  });
  validateChallenge(challenge, account);
  const signature = await provider().request({method: 'personal_sign', params: [challenge.message, account]});
  const receipt = await postJson(state.config.verify_endpoint, {
    schema: 'stegwallet.siwe_verification_request.v1',
    challenge,
    signature,
    transaction_authority: false,
    execution_authority: false
  });
  validateSession(receipt, account);
  state.session = receipt;
  $('siwe-output').value = JSON.stringify(receipt, null, 2);
  setStatus(`AUTHENTICATED\nWallet: ${account}\nSession: ${receipt.session_id}\nExpires: ${receipt.expires_at}\nTransaction authority: false`, 'ok');
}

function clearSession() {
  state.session = null;
  $('siwe-output').value = '';
  setStatus(state.config?.wallet_authentication_enabled ? 'LOCAL SESSION CLEARED\nServer revocation remains a separate authenticated operation.' : 'CONFIGURATION_REQUIRED\nNo active SIWE runtime.', '');
}

function downloadSession() {
  if (!$('siwe-output').value) throw new Error('No SIWE session receipt is available.');
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([$('siwe-output').value + '\n'], {type: 'application/json'}));
  link.download = 'stegwallet-siwe-session-receipt.json';
  link.click();
  URL.revokeObjectURL(link.href);
}

function guard(action) {
  return async () => {
    try { await action(); }
    catch (error) { setStatus(`FAIL_CLOSED\n${error.message}`, 'bad'); }
  };
}

$('siwe-sign-in').addEventListener('click', guard(signIn));
$('siwe-clear').addEventListener('click', clearSession);
$('download-siwe').addEventListener('click', guard(downloadSession));
loadConfig().catch((error) => setStatus(`FAIL_CLOSED\n${error.message}`, 'bad'));
