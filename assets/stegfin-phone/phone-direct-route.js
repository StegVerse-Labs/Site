(() => {
  'use strict';

  const C = Object.freeze({
    wallet: '0xA503DCe5471492bbA2D06e9f78F4d9D6Bcc852aA',
    chainId: '0x2105',
    rpc: 'https://mainnet.base.org',
    usdc: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    weth: '0x4200000000000000000000000000000000000006',
    sellAtomic: 12500000n,
    slippageBps: 50n,
    maxGasUsd: 1,
    factory: '0x33128a8fC17869897dcE68Ed026d694621f6FDfD',
    quoterV2: '0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a',
    swapRouter02: '0x2626664c2603336E57B271c5C0b26F421741e481',
    allowedFeeTiers: [100, 500, 3000, 10000],
    transferTopic: '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
    discoveryChunk: 5000,
    claimTtlMs: 5 * 60 * 1000,
  });

  const ROUTE_ADMISSION = Object.freeze({
    schema: 'stegverse.tvc.stegfin_direct_route_admission.v1',
    goal_id: 'TVC-STEGFIN-PHONE-DIRECT-ROUTE-008',
    decision: 'ROUTE_ADMITTED',
    authority: 'TV/TVC',
    credential_requirement: 'NONE',
    consumer: 'StegVerse-Labs/stegfin-governance',
    device_role: 'SOLE_SOVEREIGN_STEGVERSE_MACHINE',
    chain_id: C.chainId,
    wallet_address: C.wallet,
    sell_token: C.usdc,
    buy_token: C.weth,
    sell_amount_atomic: C.sellAtomic.toString(),
    maximum_slippage_bps: Number(C.slippageBps),
    maximum_gas_usd_per_transaction: C.maxGasUsd,
    route: {
      protocol: 'UNISWAP_V3_DIRECT_ONCHAIN', factory: C.factory, quoter_v2: C.quoterV2,
      swap_router_02: C.swapRouter02, allowed_fee_tiers: C.allowedFeeTiers,
      quote_method: 'eth_call', simulation_method: 'eth_call', broadcast_method: 'USER_ONLY',
    },
    deployment_source: { repository: 'Uniswap/contracts', path: 'deployments/json/8453.json', commit: 'fcd90ad0d3ea5ca63c8deb779fa975c7a8444fe9' },
    provider_secret_required: false, provider_secret_exported: false, github_token_required: false,
    non_tv_tvc_secret_or_token_used: false, wallet_key_export_allowed: false,
    automatic_signing: false, automatic_broadcast: false, hosted_runtime_required: false,
    render_required: false, vercel_required: false, cloudflare_required: false, fail_closed: true,
  });

  function stable(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stable(value[key])}`).join(',')}}`;
  }
  function bytesHex(buffer) { return [...new Uint8Array(buffer)].map((b) => b.toString(16).padStart(2, '0')).join(''); }
  async function sha256(value) { return `sha256:${bytesHex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(stable(value))))}`; }
  function word(value) { return BigInt(value).toString(16).padStart(64, '0'); }
  function addressWord(address) {
    if (!/^0x[0-9a-fA-F]{40}$/.test(address)) throw new Error('invalid address');
    return address.slice(2).toLowerCase().padStart(64, '0');
  }
  function topicAddress(address) { return `0x${addressWord(address)}`; }

  let rpcId = 0;
  async function rpc(method, params) {
    const id = ++rpcId;
    const response = await fetch(C.rpc, {
      method: 'POST', headers: { 'content-type': 'application/json' }, credentials: 'omit', cache: 'no-store',
      body: JSON.stringify({ jsonrpc: '2.0', id, method, params }),
    });
    if (!response.ok) throw new Error(`Base RPC HTTP ${response.status}`);
    const body = await response.json();
    if (body.id !== id || body.error || !Object.prototype.hasOwnProperty.call(body, 'result')) throw new Error(`Base RPC ${method} failed`);
    return body.result;
  }

  function openDb() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('stegverse-stegfin-phone-v2', 1);
      request.onupgradeneeded = () => { if (!request.result.objectStoreNames.contains('state')) request.result.createObjectStore('state'); };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error || new Error('indexeddb_open_failed'));
    });
  }
  async function dbGet(key) {
    const db = await openDb();
    try { return await new Promise((resolve, reject) => {
      const req = db.transaction('state', 'readonly').objectStore('state').get(key);
      req.onsuccess = () => resolve(req.result); req.onerror = () => reject(req.error || new Error('indexeddb_read_failed'));
    }); } finally { db.close(); }
  }
  async function dbPut(key, value) {
    const db = await openDb();
    try { await new Promise((resolve, reject) => {
      const tx = db.transaction('state', 'readwrite'); tx.objectStore('state').put(value, key);
      tx.oncomplete = resolve; tx.onerror = () => reject(tx.error || new Error('indexeddb_write_failed')); tx.onabort = () => reject(tx.error || new Error('indexeddb_write_aborted'));
    }); } finally { db.close(); }
  }

  async function acquireClaim() {
    const now = Date.now();
    const prior = await dbGet('direct-route-active-claim');
    if (prior?.state === 'ACTIVE' && prior.expires_at_ms > now) throw new Error('another direct-route preparation is already active');
    const claim = {
      schema: 'stegverse.stegfin.direct_route_claim.v1', task_id: 'STEGFIN-PHONE-DIRECT-ROUTE-010', claim_id: `phone-direct:${crypto.randomUUID()}`,
      fencing_token: now, state: 'ACTIVE', created_at_ms: now, expires_at_ms: now + C.claimTtlMs,
      device_role: 'SOLE_SOVEREIGN_STEGVERSE_MACHINE', credential_authority: 'TV/TVC', credential_requirement: 'NONE',
      non_tv_tvc_secret_or_token_used: false, wallet_signing_authority: 'USER_ONLY', broadcast_authority: 'USER_ONLY',
    };
    claim.receipt_sha256 = await sha256(claim); await dbPut('direct-route-active-claim', claim); return claim;
  }
  async function releaseClaim(claim, state) {
    const current = await dbGet('direct-route-active-claim');
    if (current?.claim_id === claim.claim_id) { current.state = state; current.released_at_ms = Date.now(); await dbPut('direct-route-active-claim', current); }
  }

  async function discoverContracts(wallet, blockHex) {
    const toBlock = Number(BigInt(blockHex));
    const cacheKey = `erc20-discovery:${wallet.toLowerCase()}`;
    const cached = await dbGet(cacheKey) || { through_block: -1, addresses: [] };
    const addresses = new Set(Array.isArray(cached.addresses) ? cached.addresses : []);
    let start = Math.max(0, Number(cached.through_block || -1) + 1);
    const walletTopic = topicAddress(wallet);
    while (start <= toBlock) {
      const end = Math.min(start + C.discoveryChunk - 1, toBlock);
      const range = { fromBlock: `0x${start.toString(16)}`, toBlock: `0x${end.toString(16)}` };
      for (const filter of [{ ...range, topics: [C.transferTopic, walletTopic] }, { ...range, topics: [C.transferTopic, null, walletTopic] }]) {
        const logs = await rpc('eth_getLogs', [filter]);
        if (!Array.isArray(logs)) throw new Error('invalid transfer-log response');
        for (const log of logs) if (/^0x[0-9a-fA-F]{40}$/.test(log?.address || '')) addresses.add(log.address.toLowerCase());
      }
      await dbPut(cacheKey, { through_block: end, addresses: [...addresses].sort() });
      start = end + 1;
    }
    addresses.add(C.usdc.toLowerCase()); addresses.add(C.weth.toLowerCase());
    return [...addresses].sort();
  }

  async function tokenDecimals(address, block) {
    if (address.toLowerCase() === C.usdc.toLowerCase()) return 6;
    if (address.toLowerCase() === C.weth.toLowerCase()) return 18;
    try { return Number(BigInt(await rpc('eth_call', [{ to: address, data: '0x313ce567' }, block]))); } catch { return 0; }
  }

  async function observeInventory() {
    const chain = await rpc('eth_chainId', []);
    if (String(chain).toLowerCase() !== C.chainId) throw new Error(`unexpected chain ${chain}`);
    const block = await rpc('eth_blockNumber', []);
    const contracts = await discoverContracts(C.wallet, block);
    const nativeAtomic = BigInt(await rpc('eth_getBalance', [C.wallet, block])).toString();
    const assets = [{ asset_id: `${C.chainId}:native:ETH`, symbol: 'ETH', asset_type: 'NATIVE', contract_address: null, amount_atomic: nativeAtomic, decimals: 18, state: 'OBSERVED', boundary: 'GAS_RESERVE', evidence_refs: [`base:block:${String(block).toLowerCase()}`] }];
    for (const address of contracts) {
      const knownUsdc = address.toLowerCase() === C.usdc.toLowerCase();
      const knownWeth = address.toLowerCase() === C.weth.toLowerCase();
      let amount = '0'; let state = knownUsdc || knownWeth ? 'OBSERVED' : 'QUARANTINED';
      let boundary = knownUsdc ? 'IDLE_CAPITAL' : knownWeth ? 'ACTIVE_POSITION_CAPACITY' : 'QUARANTINE_REVIEW';
      try {
        amount = BigInt(await rpc('eth_call', [{ to: address, data: `0x70a08231${addressWord(C.wallet)}` }, block])).toString();
        if (knownWeth && BigInt(amount) > 0n) boundary = 'ACTIVE_POSITION';
      } catch { state = 'QUARANTINED'; boundary = 'QUARANTINE_REVIEW'; }
      assets.push({
        asset_id: `${C.chainId}:erc20:${address.toLowerCase()}`, symbol: knownUsdc ? 'USDC' : knownWeth ? 'WETH' : `UNKNOWN_${address.slice(2, 8).toUpperCase()}`,
        asset_type: knownUsdc || knownWeth ? 'ERC20' : 'UNKNOWN', contract_address: address, amount_atomic: amount,
        decimals: await tokenDecimals(address, block), state, boundary,
        evidence_refs: [`base:block:${String(block).toLowerCase()}`, `base:erc20-transfer-discovery:cached-through:${String(block).toLowerCase()}`],
      });
    }
    const basis = { wallet_address: C.wallet, chain_id: C.chainId, observation_block: String(block).toLowerCase(), discovery_complete: true, assets };
    const inventoryStateHash = await sha256(basis);
    return {
      schema: 'stegwallet.base_asset_lounge_snapshot.v1', snapshot_id: `base-inventory-${inventoryStateHash.split(':')[1].slice(0, 24)}`,
      ...basis, inventory_state_hash: inventoryStateHash,
      boundary_state_hash: await sha256(assets.map((asset) => ({ asset_id: asset.asset_id, state: asset.state, boundary: asset.boundary }))),
      wallet_contacted: false, signed: false, broadcast: false,
    };
  }

  async function attestRoute() {
    if (await rpc('eth_chainId', []) !== C.chainId) throw new Error('Base chain mismatch');
    for (const [name, address] of [['factory', C.factory], ['quoter_v2', C.quoterV2], ['swap_router_02', C.swapRouter02]]) {
      const code = await rpc('eth_getCode', [address, 'latest']);
      if (typeof code !== 'string' || code === '0x') throw new Error(`${name} code unavailable`);
    }
    return { ...ROUTE_ADMISSION, admission_sha256: await sha256(ROUTE_ADMISSION) };
  }

  function quoterCalldata(fee) { return `0xc6a5026a${addressWord(C.usdc)}${addressWord(C.weth)}${word(C.sellAtomic)}${word(fee)}${word(0)}`; }
  async function quoteFee(fee) {
    try {
      const result = await rpc('eth_call', [{ to: C.quoterV2, data: quoterCalldata(fee) }, 'latest']);
      if (!/^0x[0-9a-fA-F]{256,}$/.test(result || '')) return null;
      const amountOut = BigInt(`0x${result.slice(2, 66)}`);
      return amountOut > 0n ? { fee, amountOut } : null;
    } catch { return null; }
  }
  async function getDirectQuote(admission) {
    const quotes = (await Promise.all(C.allowedFeeTiers.map(quoteFee))).filter(Boolean);
    if (!quotes.length) throw new Error('no admitted direct on-chain quote available');
    quotes.sort((a, b) => a.amountOut === b.amountOut ? 0 : a.amountOut > b.amountOut ? -1 : 1);
    const best = quotes[0];
    const minimumOut = best.amountOut * (10000n - C.slippageBps) / 10000n;
    const quote = {
      schema: 'stegwallet.direct_onchain_quote.v1', protocol: 'UNISWAP_V3_DIRECT_ONCHAIN', chain_id: C.chainId,
      token_in: C.usdc, token_out: C.weth, amount_in: C.sellAtomic.toString(), amount_out: best.amountOut.toString(), amount_out_minimum: minimumOut.toString(),
      fee: best.fee, quoter: C.quoterV2, router: C.swapRouter02, credential_requirement: 'NONE', credential_authority: 'TV/TVC', provider_secret_required: false,
      signed: false, broadcast: false, route_admission_sha256: admission.admission_sha256,
    };
    quote.quote_sha256 = await sha256(quote); return quote;
  }

  async function observeAllowance() {
    const result = await rpc('eth_call', [{ to: C.usdc, data: `0xdd62ed3e${addressWord(C.wallet)}${addressWord(C.swapRouter02)}` }, 'latest']);
    const allowance = BigInt(result || '0x0');
    const receipt = { schema: 'stegwallet.allowance_observation.v1', owner: C.wallet, token: C.usdc, spender: C.swapRouter02, allowance_atomic: allowance.toString(), exact_required_atomic: C.sellAtomic.toString(), block: 'latest' };
    receipt.receipt_hash = await sha256(receipt); return receipt;
  }

  async function candidateFromQuote(quote, allowance) {
    let candidate;
    if (BigInt(allowance.allowance_atomic) < C.sellAtomic) {
      candidate = { schema: 'stegwallet.wallet_transaction_candidate.v1', purpose: 'exact_erc20_approval', chain_id: C.chainId, from: C.wallet, to: C.usdc, value: '0x0', data: `0x095ea7b3${addressWord(C.swapRouter02)}${word(C.sellAtomic)}`, exact_allowance_atomic: C.sellAtomic.toString(), unlimited_allowance: false, requires_user_wallet_signature: true, signed: false, broadcast: false };
    } else {
      candidate = { schema: 'stegwallet.wallet_transaction_candidate.v1', purpose: 'validation_swap_usdc_to_weth', chain_id: C.chainId, from: C.wallet, to: C.swapRouter02, value: '0x0', data: `0x04e45aaf${addressWord(C.usdc)}${addressWord(C.weth)}${word(quote.fee)}${addressWord(C.wallet)}${word(C.sellAtomic)}${word(quote.amount_out_minimum)}${word(0)}`, sell_amount_atomic: C.sellAtomic.toString(), minimum_buy_amount_atomic: quote.amount_out_minimum, direct_quote_sha256: quote.quote_sha256, fee: quote.fee, requires_user_wallet_signature: true, signed: false, broadcast: false };
    }
    candidate.candidate_hash = await sha256(candidate); return candidate;
  }

  async function bindGas(candidate, quote) {
    const tx = { from: candidate.from, to: candidate.to, value: candidate.value, data: candidate.data };
    const gas = BigInt(await rpc('eth_estimateGas', [tx]));
    const gasPrice = BigInt(await rpc('eth_gasPrice', []));
    const quotedWeth = Number(BigInt(quote.amount_out)) / 1e18;
    if (!(quotedWeth > 0)) throw new Error('quote valuation invalid');
    const gasUsd = Number(gas * gasPrice) / 1e18 * (12.5 / quotedWeth);
    if (!Number.isFinite(gasUsd) || gasUsd > C.maxGasUsd) throw new Error(`gas risk exceeds $${C.maxGasUsd}`);
    const bound = { ...candidate, gas: `0x${gas.toString(16)}`, gas_price: `0x${gasPrice.toString(16)}`, gas_estimate_usd: gasUsd.toFixed(8) };
    delete bound.candidate_hash; bound.candidate_hash = await sha256(bound); return bound;
  }

  async function simulate(candidate) {
    const tx = { from: candidate.from, to: candidate.to, value: candidate.value, data: candidate.data };
    let result = null, error = null, decision = 'PASS';
    try { result = await rpc('eth_call', [tx, 'latest']); } catch (e) { decision = 'FAIL'; error = String(e?.message || e); }
    const receipt = { schema: 'stegwallet.read_only_simulation_receipt.v1', candidate_hash: candidate.candidate_hash, chain_id: C.chainId, decision, result, error, wallet_contacted: false, signed: false, broadcast: false };
    receipt.receipt_hash = await sha256(receipt); return receipt;
  }

  async function run() {
    const claim = await acquireClaim();
    try {
      const admission = await attestRoute();
      const inventory = await observeInventory();
      const quote = await getDirectQuote(admission);
      const allowance = await observeAllowance();
      let candidate = await candidateFromQuote(quote, allowance);
      candidate = await bindGas(candidate, quote);
      const simulation = await simulate(candidate);
      if (simulation.decision !== 'PASS') throw new Error('passing read-only simulation required');
      const evidence = { inventory_sha256: await sha256(inventory), route_admission_sha256: admission.admission_sha256, quote_sha256: quote.quote_sha256, allowance_sha256: allowance.receipt_hash, candidate_sha256: candidate.candidate_hash, simulation_sha256: simulation.receipt_hash };
      const handoff = { schema: 'stegwallet.wallet_handoff_bundle.v1', chain_id: C.chainId, wallet_address: C.wallet, purpose: candidate.purpose, transaction_candidate: candidate, evidence_commitments: evidence, wallet_is_only_signing_authority: true, explicit_wallet_confirmation_required: true, automatic_signing: false, automatic_broadcast: false, signed: false, broadcast: false, settled: false };
      handoff.bundle_sha256 = await sha256(handoff);
      const receipt = {
        schema: 'stegwallet.phone_continuity_pretrade_receipt.v1', state: 'WALLET_HANDOFF_READY', carrier: 'PHONE_SOVEREIGN_BROWSER_DIRECT_ONCHAIN', task_id: 'STEGFIN-PHONE-DIRECT-ROUTE-010',
        claim_id: claim.claim_id, fencing_token: claim.fencing_token, device_role: 'SOLE_SOVEREIGN_STEGVERSE_MACHINE', credential_authority: 'TV/TVC', credential_requirement: 'NONE',
        non_tv_tvc_secret_or_token_used: false, github_token_required: false, provider_secret_required: false, provider_secret_exported: false, hosted_runtime_required: false,
        render_required: false, vercel_required: false, cloudflare_required: false, wallet_signing_authority: 'USER_ONLY', broadcast_authority: 'USER_ONLY', signed: false, broadcast: false,
        wallet_handoff_bundle_sha256: handoff.bundle_sha256, inventory_state_hash: inventory.inventory_state_hash, route_admission_sha256: admission.admission_sha256,
        quote_sha256: quote.quote_sha256, allowance_receipt_sha256: allowance.receipt_hash, simulation_receipt_sha256: simulation.receipt_hash,
      };
      receipt.receipt_sha256 = await sha256(receipt);
      const terminal = { receipt, wallet_handoff: handoff, route_admission: admission, quote, inventory };
      await dbPut('latest-terminal', terminal); localStorage.setItem('stegverse.stegfin.wallet-handoff-ready.v1', JSON.stringify(terminal));
      await releaseClaim(claim, 'COMPLETE'); return terminal;
    } catch (error) {
      const failure = { schema: 'stegwallet.phone_continuity_failure_receipt.v1', state: 'BLOCKED', carrier: 'PHONE_SOVEREIGN_BROWSER_DIRECT_ONCHAIN', task_id: 'STEGFIN-PHONE-DIRECT-ROUTE-010', claim_id: claim.claim_id, credential_authority: 'TV/TVC', credential_requirement: 'NONE', non_tv_tvc_secret_or_token_used: false, hosted_runtime_required: false, signed: false, broadcast: false, at: new Date().toISOString(), detail: String(error?.message || error) };
      failure.receipt_sha256 = await sha256(failure); await dbPut('latest-failure', failure); localStorage.setItem('stegverse.stegfin.latest-failure.v1', JSON.stringify(failure));
      await releaseClaim(claim, 'BLOCKED'); throw error;
    }
  }

  window.StegFinDirectRoute = Object.freeze({ run, observeInventory, attestRoute, getDirectQuote, constants: C, routeAdmission: ROUTE_ADMISSION });
})();
