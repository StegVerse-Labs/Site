const BASE_CHAIN_ID = '0x2105';
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

function injectedProvider() {
  const candidate = globalThis.ethereum;
  return candidate && typeof candidate.request === 'function' ? candidate : null;
}

async function runReadinessSelfTest() {
  const checks = {
    secure_context: globalThis.isSecureContext === true,
    https_origin: location.protocol === 'https:',
    injected_eip1193: false,
    account_visible: false,
    base_chain_active: false,
    balance_readable: false
  };
  const blockers = [];
  const provider = injectedProvider();
  checks.injected_eip1193 = Boolean(provider);
  let account = null;
  let chainId = null;
  let balance = null;

  if (!checks.secure_context) blockers.push('secure_context_required');
  if (!checks.https_origin) blockers.push('https_origin_required');
  if (!provider) blockers.push('injected_eip1193_missing');

  if (provider) {
    const [accounts, observedChain] = await Promise.all([
      provider.request({method: 'eth_accounts'}),
      provider.request({method: 'eth_chainId'})
    ]);
    account = Array.isArray(accounts) && accounts.length ? String(accounts[0]).toLowerCase() : null;
    chainId = String(observedChain || '').toLowerCase();
    checks.account_visible = Boolean(account);
    checks.base_chain_active = chainId === BASE_CHAIN_ID;
    if (!checks.account_visible) blockers.push('wallet_account_not_visible');
    if (!checks.base_chain_active) blockers.push('base_chain_not_active');
    if (account) {
      try {
        balance = await provider.request({method: 'eth_getBalance', params: [account, 'latest']});
        checks.balance_readable = typeof balance === 'string' && balance.startsWith('0x');
      } catch (_) {
        checks.balance_readable = false;
      }
      if (!checks.balance_readable) blockers.push('native_balance_unreadable');
    }
  }

  const environment = {
    origin: location.origin,
    secure_context: checks.secure_context,
    injected_eip1193: checks.injected_eip1193,
    user_agent_hint_sha256: await sha256({user_agent: String(navigator.userAgent || '')}),
    environment_hints_grant_authority: false
  };
  environment.environment_sha256 = await sha256(environment);

  const receipt = {
    schema: 'stegwallet.wallet_browser_readiness.v1',
    receipt_id: `wallet-browser-readiness:${crypto.randomUUID()}`,
    observed_at: new Date().toISOString(),
    canonical_web_origin: location.origin,
    chain_id: chainId,
    wallet_address: account,
    native_balance_hex: balance,
    checks,
    blockers,
    state: blockers.length ? 'NOT_READY' : 'READY_FOR_GOAL_CONFIGURATION',
    environment_sha256: environment.environment_sha256,
    wallet_authenticated: false,
    signature_requested: false,
    transaction_requested: false,
    execution_authority: false,
    custody_recorded: false
  };
  receipt.receipt_sha256 = await sha256(receipt);
  $('readiness-output').value = JSON.stringify(receipt, null, 2);
}

function downloadReadiness() {
  const content = $('readiness-output').value;
  if (!content) throw new Error('No readiness receipt is available.');
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([content + '\n'], {type: 'application/json'}));
  link.download = 'stegwallet-wallet-browser-readiness.json';
  link.click();
  URL.revokeObjectURL(link.href);
}

$('run-readiness').addEventListener('click', () => {
  runReadinessSelfTest().catch((error) => {
    $('readiness-output').value = JSON.stringify({
      schema: 'stegwallet.wallet_browser_readiness.v1',
      state: 'FAIL_CLOSED',
      blockers: [String(error?.message || error)],
      wallet_authenticated: false,
      signature_requested: false,
      transaction_requested: false,
      execution_authority: false,
      custody_recorded: false
    }, null, 2);
  });
});
$('download-readiness').addEventListener('click', downloadReadiness);
