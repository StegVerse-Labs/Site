// HIL result page (StegVerse-Labs/.github#3106): the browser-local history hides a pending local record once the
// same packet has a durable receiver receipt, and the verified PDF is offered as a direct link because some
// mobile browsers (iOS Safari) render an embedded PDF blank. Storage is never modified by the page.
const fs = require('fs'); const path = require('path'); const vm = require('vm'); const crypto = require('crypto');
const root = path.join(__dirname, '..');
let n = 0; function check(ok, msg) { n++; if (!ok) throw new Error(msg); }
const src = fs.readFileSync(path.join(root, 'assets/hil-post-submit-continuity.js'), 'utf8');
const html = fs.readFileSync(path.join(root, 'hil-accepted.html'), 'utf8');

function el(id) { return { id, children: [], dataset: {}, attrs: {}, hidden: id === 'open-response-pdf', textContent: '', disabled: true,
  replaceChildren() { this.children = []; }, appendChild(c) { this.children.push(c); }, append(...c) { this.children.push(...c); },
  removeAttribute(a) { delete this.attrs[a]; delete this[a]; }, addEventListener() {} }; }

async function run({ query, rows, fetchImpl }) {
  const els = {}; const store = { 'stegverse.hil.submissions.v1': JSON.stringify(rows) }; const before = JSON.stringify(store);
  const ctx = {
    window: { location: { search: query }, addEventListener() {} },
    document: { getElementById: (id) => (els[id] = els[id] || el(id)), createElement: () => el('x'), body: { appendChild() {} } },
    localStorage: { getItem: (k) => store[k] ?? null, setItem: (k, v) => { store[k] = v; } },
    URL: { createObjectURL: () => 'blob:verified-pdf', revokeObjectURL() {} }, URLSearchParams, Blob, crypto: crypto.webcrypto,
    fetch: fetchImpl, setTimeout, console
  };
  ctx.window.fetch = fetchImpl; vm.createContext(ctx); vm.runInContext(src, ctx);
  await new Promise((r) => setTimeout(r, 20));
  return { els, unchanged: JSON.stringify(store) === before };
}

(async () => {
  check(/<a id="open-response-pdf"[^>]*target="_blank"[^>]*rel="noopener"[^>]*hidden>/.test(html), 'result page has a hidden direct PDF link');
  const sha = 'a'.repeat(64);
  const rows = [
    { submission_id: 'HIL-SUBMISSION-1', durable_submission: true, submitted_file_sha256: sha, received_at: 't2' },
    { submission_id: 'HIL-LOCAL-2-aaaa', durable_submission: false, response_sha256: sha, recorded_at: 't1' },
    { submission_id: 'HIL-LOCAL-3-aaaa', durable_submission: false, response_sha256: sha, recorded_at: 't0' },
    { submission_id: 'HIL-LOCAL-4-bbbb', durable_submission: false, response_sha256: 'b'.repeat(64), recorded_at: 't3' }
  ];
  const a = await run({ query: '', rows, fetchImpl: async () => { throw new Error('no fetch expected'); } });
  const shown = a.els['submission-history'].children.map((c) => c.children[0].textContent);
  check(JSON.stringify(shown) === JSON.stringify(['HIL-SUBMISSION-1', 'HIL-LOCAL-4-bbbb']), 'pending duplicates of an accepted packet are hidden; other pending records remain: ' + shown);
  check(a.els['submission-history'].children[1].children[0].href.startsWith('hil-receipt.html'), 'a still-pending record keeps its retry link');
  check(a.unchanged, 'history rendering never modifies browser storage');
  check(!a.els['open-response-pdf'] || a.els['open-response-pdf'].hidden === true, 'no PDF link without a verified submission');

  const pdf = Buffer.from('%PDF-1.4 verified bytes');
  const digest = crypto.createHash('sha256').update(pdf).digest('hex');
  const receipt = { schema_version: 'HIL-RECEIVER-RECEIPT-v2', submission_id: 'HIL-SUBMISSION-9', receipt_id: 'R', submitted_file_sha256: digest,
    primary_sha256: 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462', prompt_sha256: 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c',
    chain_validation_state: 'PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED', custody_state: 'EXACT_BYTES_PERSISTED', registry_state: 'RECORDED', review_state: 'PENDING', publication_state: 'NOT_AUTHORIZED' };
  const respond = (body) => ({ ok: true, status: 200, json: async () => body, arrayBuffer: async () => pdf.buffer.slice(pdf.byteOffset, pdf.byteOffset + pdf.length) });
  const fetchOk = async (url) => /\/content$/.test(url) ? respond(null) : respond({ state: 'ACCEPTED', submitted_file_sha256: digest, receipt });
  const b = await run({ query: '?submission_id=HIL-SUBMISSION-9', rows: [], fetchImpl: fetchOk });
  check(b.els['result-packet-state'].dataset.state === 'ok', 'verified submission renders: ' + b.els['result-packet-state'].textContent);
  check(b.els['open-response-pdf'].hidden === false && b.els['open-response-pdf'].href === 'blob:verified-pdf', 'verified PDF bytes are offered as a direct link');

  const wrong = Buffer.from('%PDF-1.4 other bytes');
  const fetchBad = async (url) => /\/content$/.test(url) ? { ok: true, arrayBuffer: async () => wrong.buffer.slice(wrong.byteOffset, wrong.byteOffset + wrong.length) } : respond({ state: 'ACCEPTED', submitted_file_sha256: digest, receipt });
  const c = await run({ query: '?submission_id=HIL-SUBMISSION-9', rows: [], fetchImpl: fetchBad });
  check(c.els['result-packet-state'].dataset.state === 'error' && c.els['open-response-pdf'].hidden === true && !c.els['open-response-pdf'].href, 'mismatched bytes are never offered');
  console.log('PASS hil accepted page (' + n + ' checks)');
})().catch((e) => { console.error('FAIL hil accepted page: ' + e.message); process.exit(1); });
