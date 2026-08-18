#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / 'assets' / 'stegfin-phone' / 'wallet-user-handoff.js'
UI = ROOT / 'assets' / 'stegfin-phone' / 'wallet-user-handoff-ui.js'
HTML = ROOT / 'stegfin-trade.html'

EXPECTED = {
    RUNTIME: 'c9c0688ab58e1a196bd777c45fa6f33fa7b9601b',
    UI: '114b3c39052d5b1622407080407259a0040a1369',
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = f'blob {len(data)}\0'.encode() + data
    return hashlib.sha1(payload).hexdigest()


def require(text: str, *markers: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise SystemExit('missing required markers: ' + ', '.join(missing))


def forbid(text: str, *markers: str) -> None:
    found = [marker for marker in markers if marker in text]
    if found:
        raise SystemExit('forbidden markers present: ' + ', '.join(found))


def main() -> int:
    for path, expected in EXPECTED.items():
        if not path.is_file():
            raise SystemExit(f'missing projection asset: {path.relative_to(ROOT)}')
        actual = git_blob_sha(path)
        if actual != expected:
            raise SystemExit(f'upstream blob drift: {path.relative_to(ROOT)} {actual} != {expected}')

    runtime = RUNTIME.read_text(encoding='utf-8')
    ui = UI.read_text(encoding='utf-8')
    html = HTML.read_text(encoding='utf-8')

    require(
        runtime,
        "EXPECTED_CHAIN_ID = '0x2105'",
        "EXPECTED_WALLET = '0xA503DCe5471492bbA2D06e9f78F4d9D6Bcc852aA'",
        'PREPARE_MIN_VALIDITY_MS = 5 * 60 * 1000',
        "identity.decision !== 'IDENTITY_CONTINUITY_VALID'",
        "device.decision !== 'DEVICE_ADMITTED'",
        "capability.decision !== 'ALLOW_DEVICE_WALLET_CAPABILITY'",
        'DEVICE_POSSESSION',
        'HUMAN_CONTINUITY',
        'IDENTITY_CONTINUITY',
        "grants.includes('PREPARE')",
        "grants.includes('SIGN')",
        "grants.includes('BROADCAST')",
        "credential_authority: 'TV/TVC'",
        "credential_requirement: 'NONE'",
        'non_tv_tvc_secret_or_token_used: false',
        'hosted_runtime_required: false',
        'render_required: false',
        "wallet_signing_authority: 'USER_ONLY'",
        "broadcast_authority: 'USER_ONLY'",
        'automatic_signing: false',
        'automatic_broadcast: false',
        'async function submitExactCandidateByUserAction()',
        "provider.request({ method: 'eth_sendTransaction'",
        "provider.request({ method: 'eth_chainId'",
        "provider.request({ method: 'eth_requestAccounts'",
        "rpc('eth_getTransactionReceipt'",
        "state: 'SUBMITTED_NOT_SETTLED'",
        "state: 'CONFIRMED_REPREPARE_REQUIRED'",
        'stale_quote_reuse_allowed: false',
        'stale_simulation_reuse_allowed: false',
        'stale_candidate_reuse_allowed: false',
        'successor_prepare_requires_user_presence: true',
        'async function prepareSuccessorByUserAction()',
        'window.StegFinPhoneContinuity',
    )
    forbid(runtime, 'wallet_switchEthereumChain', 'WalletConnect', 'walletconnect', 'render.com', 'api_key', 'github_token')

    send_fn = runtime.index('async function submitExactCandidateByUserAction()')
    send_call = runtime.index("provider.request({ method: 'eth_sendTransaction'", send_fn)
    if 'validateCandidate(retained)' not in runtime[send_fn:send_call] or 'requireInjectedWallet()' not in runtime[send_fn:send_call]:
        raise SystemExit('wallet send is not preceded by exact candidate/freshness validation')

    observe_fn = runtime.index('async function observeSubmittedTransaction()')
    successor_fn = runtime.index('async function prepareSuccessorByUserAction()', observe_fn)
    if 'StegFinPhoneContinuity' in runtime[observe_fn:successor_fn]:
        raise SystemExit('chain receipt observer must not silently trigger user-verifying PREPARE')

    require(
        ui,
        'Hand exact candidate to wallet',
        'Open StegVerse in local wallet browser',
        'Check submitted transaction',
        'Verify phone and prepare successor',
        'submitExactCandidateByUserAction',
        'observeSubmittedTransaction',
        'prepareSuccessorByUserAction',
        "STEGID_CAPABILITY_KEY = 'stegverse.stegid.wallet-capability.v1'",
        'localStorage.removeItem(STEGID_CAPABILITY_KEY)',
        "NO_INJECTED_WALLET_ERROR = 'No injected EIP-1193 wallet is available in this browser. No wallet action occurred.'",
        'https://metamask.app.link/dapp/',
        'Re-run Verify this phone and prepare wallet handoff there',
        'Safari candidate is not transferred or reused',
        'No wallet relay or hosted wallet middleware is used for transaction authority',
    )
    if ui.index('localStorage.removeItem(STEGID_CAPABILITY_KEY)') > ui.index('runtime().prepareSuccessorByUserAction()'):
        raise SystemExit('successor PREPARE does not force fresh StegID capability before invocation')

    browser_start = ui.index('walletBrowser.onclick')
    browser_end = ui.index('observe.onclick', browser_start)
    browser_block = ui[browser_start:browser_end]
    forbid(browser_block, 'transaction_request', 'candidate_sha256', 'eth_sendTransaction', 'private_key', 'seed', 'signature')
    require(browser_block, 'window.location.assign(localWalletBrowserUrl())')

    no_provider_fn = ui.index('function noInjectedWalletFailure()')
    render_fn = ui.index('function renderState()', no_provider_fn)
    if 'persistentFailure.includes(NO_INJECTED_WALLET_ERROR)' not in ui[no_provider_fn:render_fn]:
        raise SystemExit('wallet-browser continuation is not bound to exact no-injected-provider failure')

    # Preserve the predecessor validator's exact six defer-script contract, then
    # append wallet continuity only after those defer scripts have executed and
    # DOMContentLoaded fires. This avoids racing the PREPARE/evidence stack.
    base_order = [
        './assets/stegfin-phone/rpc-resilience.js',
        './assets/stegfin-phone/phone-direct-route.js',
        './assets/stegfin-phone/stegid-device-wallet-bootstrap.js',
        './assets/stegfin-phone/device-wallet-identity.js',
        './assets/stegfin-phone/app.js',
        './assets/stegfin-phone/evidence-export.js',
    ]
    positions = [html.find(marker) for marker in base_order]
    if any(pos < 0 for pos in positions) or positions != sorted(positions):
        raise SystemExit('canonical predecessor script load order is incomplete or unsafe')
    require(
        html,
        "window.addEventListener('DOMContentLoaded'",
        "'./assets/stegfin-phone/wallet-user-handoff.js'",
        "'./assets/stegfin-phone/wallet-user-handoff-ui.js'",
        'script.async = false',
        'wallet continuity load failed',
        'No wallet action occurred.',
    )
    evidence_pos = html.index('./assets/stegfin-phone/evidence-export.js')
    runtime_pos = html.index("'./assets/stegfin-phone/wallet-user-handoff.js'", evidence_pos)
    ui_pos = html.index("'./assets/stegfin-phone/wallet-user-handoff-ui.js'", runtime_pos)
    if not evidence_pos < runtime_pos < ui_pos:
        raise SystemExit('wallet continuity loader order is unsafe')

    print('STEGFIN_USER_ONLY_WALLET_HANDOFF_PROJECTION_PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
