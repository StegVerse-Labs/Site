// HIL receiver contract in CI (StegVerse-Labs/.github#3106, docs/HIL_PARTICIPANT_READINESS_GATE.md): runs the real
// src/worker.js against an in-memory SQLite stand-in for the HIL_REGISTRY D1 binding and checks the readiness gate's
// positive cycle and its six deterministic rejections before a change deploys, instead of only after the owner runs
// the gate against production. The positive cycle is checked with the gate's own verifier
// (scripts/verify_hil_controlled_cycle.py). Synthetic fixture only; nothing leaves the process.
const fs = require('fs'); const path = require('path'); const os = require('os'); const crypto = require('crypto');
const { execFileSync } = require('child_process');
const { DatabaseSync } = require('node:sqlite');
const root = path.join(__dirname, '..');
let n = 0; function check(ok, msg) { n++; if (!ok) throw new Error(msg); }
const PRIMARY = 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462';
const PROMPT = 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c';
const sha = (b) => crypto.createHash('sha256').update(b).digest('hex');

// Minimal D1 surface the worker uses: prepare().bind().first()/all()/run() and batch() (atomic).
function d1() {
  const db = new DatabaseSync(':memory:');
  const stmt = (sql, args = []) => ({
    sql, args,
    bind: (...a) => stmt(sql, a),
    first: async () => db.prepare(sql).get(...args) ?? null,
    all: async () => ({ results: db.prepare(sql).all(...args) }),
    run: async () => { db.prepare(sql).run(...args); return { success: true }; }
  });
  return {
    db,
    prepare: (sql) => stmt(sql),
    batch: async (list) => {
      db.exec('BEGIN');
      try { for (const s of list) db.prepare(s.sql).run(...s.args); db.exec('COMMIT'); } catch (e) { db.exec('ROLLBACK'); throw e; }
      return list.map(() => ({ success: true }));
    }
  };
}

function fixturePdf(padBytes) {
  const text = 'StegVerse HIL-E2E-001 synthetic receiver validation packet. Not participant research; not a review determination; not a publication candidate; not a Master Record; no authority effect.';
  const pad = padBytes ? '%' + 'x'.repeat(padBytes) + '\n' : '';
  return Buffer.from(`%PDF-1.4\n${pad}1 0 obj << /Type /Catalog >> endobj\nBT (${text}) Tj ET\n%%EOF\n`, 'latin1');
}

function provenanceFor(pdf, over = {}) {
  return Object.assign({
    schema_version: 'HIL-RESPONSE-PROVENANCE-v1.1', test_case_id: 'HIL-E2E-001', artifact_type: 'HIL_TEST_RESPONSE_PACKET',
    participant_type: 'SYNTHETIC_VALIDATION_ACTOR', primary_version: 'v1.1', primary_sha256: PRIMARY, protocol_version: 'HIL-PROTOCOL-v1.1',
    prompt_version: 'HIL-PROMPT-v1.1', prompt_sha256: PROMPT, response_sha256: sha(pdf), model: 'SYNTHETIC-INFRASTRUCTURE-FIXTURE',
    provider: 'StegVerse-Labs/Site CI', generated_at: '2000-01-01T00:00:00Z', participant_identifier: 'CONTROLLED-INFRASTRUCTURE-CYCLE',
    publication_consent: 'NOT_APPLICABLE_SYNTHETIC', research_data: false, authority_effect: false
  }, over);
}

function form({ pdf, name = 'ORIGINAL.pdf', provenance, primary = PRIMARY, prompt = PROMPT }) {
  const f = new FormData();
  if (pdf) f.append('response_pdf', new Blob([pdf], { type: 'application/pdf' }), name);
  if (provenance !== undefined) f.append('provenance_manifest', new Blob([JSON.stringify(provenance)], { type: 'application/json' }), 'provenance.json');
  f.append('primary_sha256', primary); f.append('prompt_sha256', prompt);
  f.append('participant_identifier', 'CONTROLLED-INFRASTRUCTURE-CYCLE'); f.append('publication_consent', 'NOT_APPLICABLE_SYNTHETIC');
  return f;
}

(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'hil-receiver-'));
  fs.writeFileSync(path.join(tmp, 'worker.mjs'), fs.readFileSync(path.join(root, 'src/worker.js'), 'utf8'));
  const worker = (await import('file://' + path.join(tmp, 'worker.mjs'))).default;
  const env = { HIL_REGISTRY: d1() };
  const call = (p, init) => worker.fetch(new Request('https://receiver.example' + p, init), env);
  const post = (body) => call('/api/hil/submissions', { method: 'POST', body });

  const ready = await call('/api/hil/readiness');
  const readyJson = await ready.json();
  check(ready.status === 200 && readyJson.state === 'READY' && readyJson.receiver_mode === 'FULL_CUSTODY' && readyJson.custody_backend === 'portable-sqlite-chunks-v1', 'readiness READY/FULL_CUSTODY with a working registry: ' + JSON.stringify(readyJson.state));
  fs.writeFileSync(path.join(tmp, 'readiness.json'), JSON.stringify(readyJson));
  execFileSync('python3', [path.join(root, 'scripts/verify_hil_readiness_record.py'), path.join(tmp, 'readiness.json')], { stdio: 'pipe' });
  check(true, 'readiness record passes the gate readiness verifier');

  // Positive cycle with a packet larger than one 192 KiB chunk, verified by the gate's own verifier.
  const pdf = fixturePdf(450 * 1024);
  const provenance = provenanceFor(pdf);
  const res = await post(form({ pdf, provenance }));
  const receipt = await res.json();
  check(res.status === 201, 'first submission is accepted with 201: ' + res.status + ' ' + JSON.stringify(receipt));
  const status = await (await call('/api/hil/submissions/' + encodeURIComponent(receipt.submission_id))).json();
  check(status.chunk_count >= 3, 'the packet spans several custody chunks: ' + status.chunk_count);
  const content = await call('/api/hil/submissions/' + encodeURIComponent(receipt.submission_id) + '/content');
  const retrieved = Buffer.from(await content.arrayBuffer());
  check(content.status === 200 && content.headers.get('x-content-sha256') === sha(pdf), 'content endpoint returns the exact bytes with their hash header');
  const files = { 'ORIGINAL.pdf': pdf, 'provenance.json': JSON.stringify(provenance), 'receipt.json': JSON.stringify(receipt), 'status.json': JSON.stringify(status), 'RETRIEVED.pdf': retrieved };
  for (const [k, v] of Object.entries(files)) fs.writeFileSync(path.join(tmp, k), v);
  const verdict = execFileSync('python3', [path.join(root, 'scripts/verify_hil_controlled_cycle.py'), ...Object.keys(files).map((k) => path.join(tmp, k))], { encoding: 'utf8' });
  check(verdict.includes('HIL_CONTROLLED_CYCLE=PASS') && verdict.includes('exact_bytes_retrieved=true') && verdict.includes('authority_granted=false'), 'gate verifier passes the positive cycle');

  // A held packet submitted again (days or weeks later) returns the same receipt, not a second record.
  const again = await post(form({ pdf, provenance }));
  const againJson = await again.json();
  check(again.status === 200 && againJson.receipt_id === receipt.receipt_id && againJson.submission_id === receipt.submission_id, 'resubmitting the same packet returns the existing receipt');
  check(env.HIL_REGISTRY.db.prepare('SELECT COUNT(*) AS c FROM hil_submissions').get().c === 1, 'no duplicate submission row');

  // The gate's six deterministic rejections, each leaving the registry unchanged.
  const small = fixturePdf(0), smallProv = provenanceFor(small);
  const cases = [
    ['missing-provenance', 400, 'response_pdf_and_provenance_manifest_required', form({ pdf: small })],
    ['wrong-extension', 400, 'response_pdf_extension_invalid', form({ pdf: small, name: 'wrong-extension.txt', provenance: smallProv })],
    ['invalid-signature', 400, 'response_pdf_signature_invalid', form({ pdf: Buffer.from('NOT-A-PDF'), provenance: smallProv })],
    ['wrong-response-hash', 422, 'primary_prompt_response_chain_invalid', form({ pdf: small, provenance: provenanceFor(small, { response_sha256: '0'.repeat(64) }) })],
    ['wrong-primary-hash', 422, 'primary_prompt_response_chain_invalid', form({ pdf: small, provenance: provenanceFor(small, { primary_sha256: '1'.repeat(64) }) })],
    ['wrong-prompt-hash', 422, 'primary_prompt_response_chain_invalid', form({ pdf: small, provenance: provenanceFor(small, { prompt_sha256: '2'.repeat(64) }) })],
    // Beyond the gate's six: the receiver's size limit, which the upload page mirrors (assets/hil-direct-upload-v1.js).
    ['oversize', 413, 'response_pdf_size_invalid', (() => { const big = fixturePdf(10 * 1024 * 1024); return form({ pdf: big, provenance: provenanceFor(big) }); })()]
  ];
  for (const [name, code, detail, body] of cases) {
    const r = await post(body); const j = await r.json();
    check(r.status === code && j.detail === detail, `${name}: expected ${code} ${detail}, got ${r.status} ${j.detail}`);
  }
  check(env.HIL_REGISTRY.db.prepare('SELECT COUNT(*) AS c FROM hil_submissions').get().c === 1 && env.HIL_REGISTRY.db.prepare('SELECT COUNT(*) AS c FROM hil_submission_chunks WHERE submission_id != ?1').get(receipt.submission_id).c === 0, 'rejections persist nothing');

  // Custody tampering is refused rather than served.
  env.HIL_REGISTRY.db.prepare("UPDATE hil_submission_chunks SET chunk_sha256 = ?1 WHERE submission_id = ?2 AND chunk_index = 0").run('f'.repeat(64), receipt.submission_id);
  const tampered = await call('/api/hil/submissions/' + encodeURIComponent(receipt.submission_id) + '/content');
  check(tampered.status === 500 && (await tampered.json()).detail === 'receiver_internal_error', 'a tampered chunk is never served');

  // Without the registry binding the receiver reports DEGRADED and refuses durable submission.
  const bare = { };
  const degraded = await worker.fetch(new Request('https://receiver.example/api/hil/readiness'), bare);
  const refused = await worker.fetch(new Request('https://receiver.example/api/hil/submissions', { method: 'POST', body: form({ pdf: small, provenance: smallProv }) }), bare);
  check(degraded.status === 207 && (await degraded.json()).state === 'DEGRADED' && refused.status === 503 && (await refused.json()).detail === 'durable_receiver_unavailable', 'no registry: DEGRADED readiness and no durable submission');

  // The readiness publisher must also publish the announcement status derived from it (checked on every PR).
  const pub = fs.readFileSync(path.join(root, '.github/workflows/hil-publish-readiness.yml'), 'utf8');
  const derive = pub.indexOf('python3 scripts/derive_hil_announcement_status.py\n'), add = pub.indexOf('git add data/hil-participant-readiness.json data/hil-controlled-cycle-latest.json data/hil-announcement-status.json');
  check(derive > 0 && add > derive && pub.indexOf('derive_hil_announcement_status.py --check', add) > add, 'readiness publisher regenerates and commits the derived announcement status');
  check(pub.indexOf("Path('data/hil-controlled-cycle-latest.json').write_text") > 0 && !/\bsleep\b|for attempt/.test(pub), 'readiness publisher records the controlled-cycle outcome on the gate completion without waiting or retrying');
  console.log('PASS hil receiver contract (' + n + ' checks)');
})().catch((e) => { console.error('FAIL hil receiver contract: ' + e.message); process.exit(1); });
