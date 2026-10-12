// HIL failures under the universal explanation contract (StegVerse-Labs/.github#3106): every failure code the upload
// and retry pages can raise maps to a plain-language predicate, each predicate builds a conforming explanation
// artifact, and the pages lead with the prose sentence while keeping the code as a technical detail.
const fs = require('fs'); const path = require('path'); const vm = require('vm');
const root = path.join(__dirname, '..');
let n = 0; function check(ok, msg) { n++; if (!ok) throw new Error(msg); }
const read = (p) => fs.readFileSync(path.join(root, p), 'utf8');
const ctx = {}; ctx.globalThis = ctx; vm.createContext(ctx);
vm.runInContext(read('assets/workspace-explanation.js'), ctx);
vm.runInContext(read('assets/hil-decision-reasons.js'), ctx);
const R = ctx.StegVerseHilDecisionReasons, X = ctx.StegVerseWorkspaceExplanation;
check(R && Object.isFrozen(R) && R.predicates.length === 6, 'module loads with six predicates');

// Every code the pages throw is explained by a specific predicate, never the catch-all.
const codes = new Set();
for (const f of ['hil-receipt.html', 'assets/hil-direct-upload-v1.js']) for (const m of read(f).matchAll(/Error\('([a-z_]+)'\)/g)) codes.add(m[1]);
for (const c of ['primary_prompt_response_chain_invalid', 'provenance_manifest_invalid_json', 'response_pdf_extension_invalid', 'response_pdf_signature_invalid', 'response_pdf_size_invalid', 'multipart_form_data_required', 'response_pdf_and_provenance_manifest_required', 'durable_receiver_unavailable', 'registry_unavailable', 'receiver_internal_error']) codes.add(c);
check(codes.size >= 60, 'page and receiver failure codes collected: ' + codes.size);
const unexplained = [...codes].filter((c) => R.classify(c) === 'HIL_OUTCOME_UNEXPLAINED');
check(unexplained.length === 0, 'codes without a specific explanation: ' + unexplained.join(','));

const expect = {
  intr_receipt_chain_invalid: 'HIL_RECEIPT_NOT_VERIFIED', ingress_custody_not_durable: 'HIL_RECEIPT_NOT_VERIFIED',
  'invalid_ingress_response [http=405; class=OTHER; content_type=text/html]': 'HIL_RECEIVER_UNREACHABLE', ingress_http_503: 'HIL_RECEIVER_UNREACHABLE',
  'Load failed': 'HIL_RECEIVER_UNREACHABLE', 'Failed to fetch': 'HIL_RECEIVER_UNREACHABLE',
  response_pdf_signature_invalid: 'HIL_PACKET_REJECTED', primary_prompt_response_chain_invalid: 'HIL_PACKET_REJECTED', invalid_pdf_signature: 'HIL_PACKET_REJECTED',
  indexeddb_open_failed: 'HIL_LOCAL_PACKET_UNAVAILABLE', response_pdf_hash_mismatch: 'HIL_LOCAL_PACKET_UNAVAILABLE', stored_provenance_unavailable: 'HIL_LOCAL_PACKET_UNAVAILABLE',
  canonical_intr_connector_unavailable: 'HIL_PAGE_COMPONENT_UNAVAILABLE', something_new: 'HIL_OUTCOME_UNEXPLAINED', '': 'HIL_OUTCOME_UNEXPLAINED'
};
for (const [code, p] of Object.entries(expect)) check(R.classify(code) === p, `classify(${JSON.stringify(code)}) = ${R.classify(code)}, expected ${p}`);

// Each predicate builds a conforming, non-authoritative artifact; the record carries the predicate, not the code.
const disp = { HIL_PACKET_REJECTED: 'DENY', HIL_OUTCOME_UNEXPLAINED: 'UNKNOWN' };
for (const p of R.predicates) {
  const rec = R.explanationRecord(p);
  check(rec && rec.disposition === (disp[p] || 'FAIL_CLOSED') && rec.predicate === p, 'record disposition for ' + p);
  const a = X.build(rec, { repository: 'StegVerse-Labs/Site', surface_id: 'hil-receipt' });
  check(a && a.prose && X.conforms(a).ok, 'conforming artifact for ' + p + ': ' + JSON.stringify(a && (a.reason || X.conforms(a))));
  check(a.authorization.authorized === false && a.execution.executed === false && a.authority.authority_effect === 'NONE', 'no authority or execution claimed for ' + p);
  check(a.prose.why === 'Because ' + R.reasons[p] + '.', 'prose why is the plain-language reason for ' + p);
}
const d = R.describe('intr_receipt_chain_invalid');
check(d.sentence.startsWith('Because an answer came back') && !JSON.stringify(d.record).includes('intr_receipt_chain_invalid'), 'describe leads with prose and keeps the code out of the record');

// Render into a stub container: details + prose + copy button.
const made = [];
const el = (tag) => { const e = { tag, children: [], textContent: '', hidden: true, append(...c) { this.children.push(...c); }, appendChild(c) { this.children.push(c); }, replaceChildren() { this.children = []; }, addEventListener(t, f) { this.on = f; } }; made.push(e); return e; };
ctx.document = { createElement: el };
const box = el('div');
const art = R.renderExplanation(box, 'response_pdf_signature_invalid', 'hil-submit');
const det = box.children[0];
check(art && box.hidden === false && det.tag === 'details' && det.children.map((c) => c.tag).join() === 'summary,pre,button', 'explanation renders as details/summary/pre/button');
check(det.children[1].textContent.includes('What happened:') && det.children[1].textContent.includes('Denied'), 'rendered prose is the contract prose');
vm.runInContext('globalThis.StegVerseWorkspaceExplanation = undefined;', ctx);
const box2 = el('div'); box2.hidden = false;
check(R.renderExplanation(box2, 'x', 'hil-submit') === null && box2.hidden === true, 'without the contract the container stays hidden');

// Page wiring.
const receipt = read('hil-receipt.html');
check(/<script src="assets\/workspace-explanation\.js"><\/script><script src="assets\/hil-decision-reasons\.js"><\/script>/.test(receipt) && receipt.indexOf('hil-decision-reasons.js') < receipt.indexOf('async function retry('), 'retry page loads the contract and reasons before its script');
check(receipt.includes("reasons.describe(code).sentence") && receipt.includes("Technical detail: '+code") && receipt.includes('<div id="retry-explanation" hidden></div>'), 'retry failure leads with prose, keeps the code as detail, and renders the explanation');
const submit = read('humans-as-interoperability-layer.html'), upload = read('assets/hil-direct-upload-v1.js');
check(submit.includes('<div id="intake-explanation" hidden></div>') && submit.indexOf('hil-decision-reasons.js') < submit.indexOf('hil-direct-upload-v1.js'), 'upload page has the explanation container and loads reasons first');
check(upload.includes("reasons.describe(code).sentence") && upload.includes("renderExplanation(document.getElementById('intake-explanation'), code, 'hil-submit')"), 'upload failure leads with prose and renders the explanation');
console.log('PASS hil decision reasons (' + n + ' checks)');
