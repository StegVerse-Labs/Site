const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');

const worker = fs.readFileSync('intr-service-worker.js', 'utf8');
const recovery = fs.readFileSync('intr-kv-installation-recovery-extension.js', 'utf8');

test('bounded recovery extension stays on the existing root service worker', () => {
  const base = worker.indexOf('importScripts("/intr-service-worker-base-v1.js")');
  const fix = worker.indexOf('importScripts("/intr-kv-installation-recovery-extension.js")');
  const canonical = worker.indexOf('importScripts("/intr-canonical-work-extension.js")');
  assert.ok(base >= 0 && fix > base && canonical > fix);
  assert.doesNotMatch(recovery, /addEventListener\("fetch"|serviceWorker\.register|new Worker/);
});

test('recovery is scoped only to canonical installation receipt admission', () => {
  assert.match(recovery, /payload\.canonical_path === "_System"/);
  assert.match(recovery, /files\.length === 1/);
  assert.match(recovery, /files\[0\]\.name === "installation\.receipt\.json"/);
  assert.match(recovery, /if\(!isCanonicalInstallationPayload\(payload\)\) return priorPersistPortable\(req\)/);
});

test('incoming replacement must pass canonical receipt validation first', () => {
  assert.match(recovery, /validateInstallationReceiptRow\(candidate\)/);
  assert.match(recovery, /portable_file_sha256_mismatch/);
  assert.match(recovery, /credential_material_present:false/);
  assert.match(recovery, /provider_operation_authorized:false/);
  assert.match(recovery, /authority_effect:"NONE"/);
});

test('valid existing receipt remains write-once and only invalid resident row may be replaced', () => {
  assert.match(recovery, /CANONICAL_INSTALLATION_RECEIPT_IDEMPOTENT_REUSE/);
  assert.match(recovery, /validateInstallationReceiptRow\(existing\)/);
  assert.match(recovery, /throw new Error\("write_once_collision:"\+FILES\)/);
  assert.match(recovery, /REPLACE_INVALID_CANONICAL_INSTALLATION_RECEIPT/);
  assert.match(recovery, /replaced_invalid_row_sha256/);
  assert.match(recovery, /return put\(FILES,candidate\)/);
});
