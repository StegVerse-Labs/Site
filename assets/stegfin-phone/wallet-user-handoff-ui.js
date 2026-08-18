(() => {
  'use strict';

  const STEGID_CAPABILITY_KEY = 'stegverse.stegid.wallet-capability.v1';
  const NO_INJECTED_WALLET_ERROR = 'No injected EIP-1193 wallet is available in this browser. No wallet action occurred.';

  function el(tag, text, cls) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (cls) node.className = cls;
    return node;
  }

  function runtime() {
    const value = window.StegFinUserWalletHandoff;
    if (!value) throw new Error('USER_ONLY wallet handoff runtime unavailable');
    return value;
  }

  function stateText(state) {
    if (!state) return 'No wallet transaction has been submitted by this control.';
    const hash = state.transaction_hash ? ` · ${state.transaction_hash.slice(0, 10)}…` : '';
    switch (state.state) {
      case 'AWAITING_USER_WALLET_CONFIRMATION': return 'Wallet confirmation is open. The wallet remains the only signer and broadcaster.';
      case 'USER_DECLINED_OR_WALLET_REJECTED': return 'Wallet action was declined or rejected. No transaction authority was transferred.';
      case 'SUBMITTED_NOT_SETTLED': return `Wallet submitted a transaction${hash}; chain settlement is not yet proven.`;
      case 'SUBMITTED_AWAITING_CHAIN_RECEIPT': return `Transaction${hash} is still awaiting a Base receipt.`;
      case 'CHAIN_RECEIPT_FAILED': return `Transaction${hash} has a failed Base receipt. Successor PREPARE is disabled.`;
      case 'CONFIRMED_REPREPARE_REQUIRED': return `Transaction${hash} confirmed. The old quote/candidate is invalid; verify this phone again to prepare the successor.`;
      case 'SUCCESSOR_WALLET_HANDOFF_READY': return `Successor ${state.successor_purpose || 'candidate'} is WALLET_HANDOFF_READY and again stops at USER_ONLY.`;
      default: return String(state.state || 'UNKNOWN');
    }
  }

  function localWalletBrowserUrl() {
    const dappPath = `${window.location.host}${window.location.pathname}${window.location.search}`;
    return `https://metamask.app.link/dapp/${dappPath}`;
  }

  function mount() {
    if (document.getElementById('userWalletHandoffCard')) return;
    const evidence = document.querySelector('.evidence-card');
    if (!evidence) return;

    const card = el('section');
    card.id = 'userWalletHandoffCard';
    card.className = 'card';
    card.setAttribute('aria-labelledby', 'userWalletHandoffTitle');

    const head = el('div', undefined, 'card-head');
    const heading = el('div');
    heading.append(el('p', 'USER_ONLY transition', 'eyebrow'), el('h2', 'Wallet handoff → successor PREPARE'));
    heading.querySelector('h2').id = 'userWalletHandoffTitle';
    head.append(heading);

    const copy = el('p', 'This control can present the exact current candidate to an already-injected wallet only after your explicit tap. The wallet independently confirms or rejects. If Safari has no injected wallet, StegFin can reopen this same participant in a compatible local wallet browser; PREPARE must then be performed again inside that wallet browser before any candidate is handed to the wallet.', 'status-copy');
    const status = el('p', '', 'muted');
    status.id = 'userWalletHandoffStatus';

    const handoff = el('button', 'Hand exact candidate to wallet');
    handoff.id = 'handoffExactCandidate';
    handoff.type = 'button';

    const walletBrowser = el('button', 'Open StegVerse in local wallet browser');
    walletBrowser.id = 'openLocalWalletBrowser';
    walletBrowser.type = 'button';
    walletBrowser.hidden = true;

    const observe = el('button', 'Check submitted transaction');
    observe.id = 'observeSubmittedTransaction';
    observe.type = 'button';

    const successor = el('button', 'Verify phone and prepare successor');
    successor.id = 'prepareSuccessorCandidate';
    successor.type = 'button';

    const boundary = el('p', 'No wallet relay or hosted wallet middleware is used for transaction authority. No automatic signing, broadcast, network switching, or stale quote reuse is permitted. Opening a wallet browser never transfers the retained Safari candidate; a fresh PREPARE is required there.', 'muted');
    card.append(head, copy, handoff, walletBrowser, observe, successor, status, boundary);
    evidence.parentNode.insertBefore(card, evidence);

    let persistentFailure = '';

    function noInjectedWalletFailure() {
      return persistentFailure.includes(NO_INJECTED_WALLET_ERROR);
    }

    function renderState() {
      let rt;
      try { rt = runtime(); } catch (error) {
        handoff.disabled = true;
        walletBrowser.hidden = true;
        observe.disabled = true;
        successor.disabled = true;
        status.textContent = String(error.message || error);
        return;
      }
      const s = rt.getState();
      status.textContent = persistentFailure || stateText(s);
      walletBrowser.hidden = !noInjectedWalletFailure();
      observe.disabled = !s || !['SUBMITTED_NOT_SETTLED', 'SUBMITTED_AWAITING_CHAIN_RECEIPT'].includes(s.state);
      successor.disabled = !s || s.state !== 'CONFIRMED_REPREPARE_REQUIRED';
      handoff.disabled = false;
    }

    async function run(button, label, fn) {
      const original = button.textContent;
      persistentFailure = '';
      button.disabled = true;
      button.textContent = label;
      try {
        await fn();
      } catch (error) {
        persistentFailure = `Fail closed: ${String(error?.message || error)}`;
      } finally {
        button.textContent = original;
        renderState();
      }
    }

    handoff.onclick = () => run(handoff, 'Opening wallet confirmation…', async () => {
      await runtime().submitExactCandidateByUserAction();
    });

    walletBrowser.onclick = () => {
      persistentFailure = 'Opening the StegVerse participant in the local wallet browser. Re-run Verify this phone and prepare wallet handoff there; the Safari candidate is not transferred or reused.';
      renderState();
      window.location.assign(localWalletBrowserUrl());
    };

    observe.onclick = () => run(observe, 'Checking Base receipt…', async () => {
      await runtime().observeSubmittedTransaction();
    });

    successor.onclick = () => run(successor, 'Verifying phone and preparing…', async () => {
      localStorage.removeItem(STEGID_CAPABILITY_KEY);
      await runtime().prepareSuccessorByUserAction();
      window.dispatchEvent(new Event('stegfin:successor-prepared'));
    });

    window.addEventListener('stegfin:user-wallet-handoff-state', () => {
      persistentFailure = '';
      renderState();
    });
    renderState();

    const initial = runtime().getState();
    if (initial && ['SUBMITTED_NOT_SETTLED', 'SUBMITTED_AWAITING_CHAIN_RECEIPT'].includes(initial.state)) {
      runtime().observeSubmittedTransaction().then(renderState).catch((error) => {
        persistentFailure = `Fail closed: ${String(error?.message || error)}`;
        renderState();
      });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
  else mount();
})();
