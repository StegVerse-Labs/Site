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
check(R && Object.isFrozen(R) && R.predicates.length === 7, 'module loads with seven predicates');

// Every code the pages throw is explained by a specific predicate, never the catch-all.
const codes = new Set();
for (const f of ['hil-receipt.html', 'assets/hil-direct-upload-v1.js', 'assets/hil-post-submit-continuity.js']) for (const m of read(f).matchAll(/Error\('([a-z_]+)'\)/g)) codes.add(m[1]);
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
  canonical_intr_connector_unavailable: 'HIL_PAGE_COMPONENT_UNAVAILABLE', something_new: 'HIL_OUTCOME_UNEXPLAINED', '': 'HIL_OUTCOME_UNEXPLAINED',
  stored_packet_unavailable: 'HIL_STORED_PACKET_NOT_VERIFIED', retrieved_packet_hash_mismatch: 'HIL_STORED_PACKET_NOT_VERIFIED', submission_status_unavailable: 'HIL_STORED_PACKET_NOT_VERIFIED', submission_not_found: 'HIL_STORED_PACKET_NOT_VERIFIED', accepted_receipt_invalid: 'HIL_RECEIPT_NOT_VERIFIED'
};
for (const [code, p] of Object.entries(expect)) check(R.classify(code) === p, `classify(${JSON.stringify(code)}) = ${R.classify(code)}, expected ${p}`);

// The upload page treats receiver refusals of the packet as final (shown, not queued for retry) using the same
// meaning as the classifier, and refuses an oversize packet before staging it, at the receiver's own limit.
{
  const up = read('assets/hil-direct-upload-v1.js');
  const final = new RegExp(up.match(/const FINAL_PACKET_REFUSAL = \/(.+)\/;/)[1]);
  const all = [...codes, 'response_pdf_size_invalid', 'response_pdf_required', 'ingress_http_503', 'Load failed', 'intr_receipt_chain_invalid'];
  const disagree = all.filter((c) => final.test(c) !== (R.classify(c) === 'HIL_PACKET_REJECTED'));
  check(disagree.length === 0, 'upload final-refusal rule disagrees with the classifier on: ' + disagree.join(','));
  const max = up.match(/const MAX_RESPONSE_BYTES = ([0-9 *]+);/)[1], workerMax = read('src/worker.js').match(/const MAX_BYTES = ([0-9 *]+);/)[1];
  check(eval(max) === eval(workerMax) && eval(max) === 10 * 1024 * 1024, 'upload size limit equals the receiver limit');
  const i = (t) => up.indexOf(t);
  check(i("throw new Error('response_pdf_size_invalid')") > 0 && i("throw new Error('response_pdf_size_invalid')") < i('const staged = await stageTransportPacket('), 'oversize packets are refused before anything is staged');
  check(i('if (FINAL_PACKET_REFUSAL.test(') > i('} catch (ingressError) {') && i('if (FINAL_PACKET_REFUSAL.test(') < i('const submissionId = `HIL-LOCAL-'), 'final refusals are rethrown before the local retry fallback');
}

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
// Every non-ALLOW record carries the six disposition fields, each non-empty, with a retry entrypoint that is a real page.
const SIX = ['failure_code', 'failed_predicate', 'required_evidence_or_repair', 'retry_entrypoint', 'owning_existing_goal', 'next_attempt'];
for (const p of R.predicates) {
  const rec = R.explanationRecord(p);
  check(rec.disposition !== 'ALLOW', 'HIL records never claim ALLOW: ' + p);
  check(SIX.every((k) => typeof rec[k] === 'string' && rec[k].trim().length > 0), 'six disposition fields present for ' + p + ': ' + JSON.stringify(SIX.filter((k) => !rec[k])));
  check(rec.owning_existing_goal === 'SHWP-HIL-SOVEREIGN-RECEIVER-001' && rec.failure_code === p && rec.failed_predicate !== p, 'goal, failure code and failed predicate for ' + p);
  check(fs.existsSync(path.join(root, rec.retry_entrypoint.split('#')[0])), 'retry entrypoint is a page that exists: ' + rec.retry_entrypoint);
}
const d = R.describe('intr_receipt_chain_invalid');
check(d.sentence.startsWith('Because an answer came back') && !JSON.stringify(d.record).includes('intr_receipt_chain_invalid'), 'describe leads with prose and keeps the code out of the record');

// A surface whose every failure has one meaning names it; the record then carries that surface's own action.
{
  const v = R.describe('Load failed', 'HIL_STORED_PACKET_NOT_VERIFIED');
  check(v.predicate === 'HIL_STORED_PACKET_NOT_VERIFIED' && v.record.requested_action.startsWith('verify a submitted HIL response packet'), 'predicate override is honoured with its own requested action');
  check(R.describe('Load failed', 'NOT_A_PREDICATE').predicate === 'HIL_RECEIVER_UNREACHABLE', 'an unknown override falls back to classification');
  check(R.explanationRecord('HIL_RECEIVER_UNREACHABLE').requested_action === 'submit a HIL response packet to the StegVerse receiver', 'submission predicates keep the submission action');
}

// Render into a stub container: details + prose + copy button.
const made = [];
const el = (tag) => { const e = { tag, children: [], textContent: '', hidden: true, parentNode: null, attrs: {}, setAttribute(k, v) { this.attrs[k] = v; }, append(...c) { c.forEach((x) => { x.parentNode = this; }); this.children.push(...c); }, appendChild(c) { c.parentNode = this; this.children.push(c); }, replaceChildren() { this.children = []; }, addEventListener(t, f) { this.on = f; } }; made.push(e); return e; };
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
const accepted = read('hil-accepted.html'), result = read('assets/hil-post-submit-continuity.js');
check(accepted.includes('<div id="result-explanation" hidden></div>') && accepted.indexOf('hil-decision-reasons.js') < accepted.indexOf('hil-post-submit-continuity.js') && accepted.indexOf('workspace-explanation.js') < accepted.indexOf('hil-decision-reasons.js'), 'result page loads the contract and reasons before its script and has the explanation container');
check(result.includes("reasons.describe(code, 'HIL_STORED_PACKET_NOT_VERIFIED').sentence") && result.includes('Technical detail: ${code}.') && result.includes("renderExplanation(byId('result-explanation'), code, 'hil-accepted', 'HIL_STORED_PACKET_NOT_VERIFIED')"), 'result-page failure leads with prose and keeps the code as detail');
check(!/Result-packet verification failed: \$\{error\.message/.test(result), 'result page no longer leads with the raw code');
check(read('hil-receipt.html').includes("'The appended PDF could not be read. Technical detail: '+code+'.'") && !read('hil-receipt.html').includes("'The appended PDF could not be read: '+e.message"), 'receipt-page PDF read failure leads with prose');
const receipt = read('hil-receipt.html');
check(/<script src="assets\/workspace-explanation\.js"><\/script><script src="assets\/hil-decision-reasons\.js"><\/script>/.test(receipt) && receipt.indexOf('hil-decision-reasons.js') < receipt.indexOf('async function retry('), 'retry page loads the contract and reasons before its script');
check(receipt.includes("reasons.describe(code).sentence") && receipt.includes("Technical detail: '+code") && receipt.includes('<div id="retry-explanation" hidden></div>'), 'retry failure leads with prose, keeps the code as detail, and renders the explanation');
const submit = read('humans-as-interoperability-layer.html'), upload = read('assets/hil-direct-upload-v1.js');
check(submit.includes('<div id="intake-explanation" hidden></div>') && submit.indexOf('hil-decision-reasons.js') < submit.indexOf('hil-direct-upload-v1.js'), 'upload page has the explanation container and loads reasons first');
check(upload.includes("reasons.describe(code).sentence") && upload.includes("renderExplanation(document.getElementById('intake-explanation'), code, 'hil-submit')"), 'upload failure leads with prose and renders the explanation');
// Copy control: the complete JSON stays reachable with or without clipboard access (compatibility requirement 2).
(async () => {
  vm.runInContext(read('assets/workspace-explanation.js'), ctx);
  const tick = () => new Promise((r) => setImmediate(r));
  const render = () => { const b = el('div'); const a = R.renderExplanation(b, 'intr_receipt_chain_invalid', 'hil-receipt'); return { a, d: b.children[0] }; };
  const jsonShown = (d, a) => d.children.length === 4 && d.children[3].tag === 'pre' && JSON.stringify(JSON.parse(d.children[3].textContent)) === JSON.stringify(a) && d.children[3].attrs['aria-label'] === 'Explanation JSON';
  ctx.navigator = undefined;
  let { a, d } = render();
  d.children[2].on(); d.children[2].on();
  check(jsonShown(d, a), 'no clipboard: the complete JSON is shown in its own block');
  check(d.children[2].textContent.includes('select the explanation JSON below'), 'no clipboard: the button says where the JSON is');
  ctx.navigator = { clipboard: { writeText: () => Promise.reject(new Error('denied')) } };
  ({ a, d } = render());
  d.children[2].on(); await tick();
  check(jsonShown(d, a), 'clipboard refused: the complete JSON is shown in its own block');
  let copied = null;
  ctx.navigator = { clipboard: { writeText: (t) => { copied = t; return Promise.resolve(); } } };
  ({ a, d } = render());
  d.children[2].on(); await tick();
  check(copied === JSON.stringify(a, null, 2) && d.children.length === 3 && d.children[2].textContent === 'Explanation JSON copied', 'clipboard available: the complete JSON is copied and no extra block is added');
  console.log('PASS hil decision reasons (' + n + ' checks)');
})().catch((e) => { console.error('FAIL hil decision reasons: ' + e.message); process.exit(1); });
