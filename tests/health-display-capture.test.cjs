const assert = require('node:assert/strict');
const test = require('node:test');

if (!globalThis.TextEncoder) globalThis.TextEncoder = require('node:util').TextEncoder;
if (!globalThis.crypto) globalThis.crypto = require('node:crypto').webcrypto;

require('../assets/health-display-capture.js');

const capture = globalThis.StegHealthDisplayedCapture;

test('parses a multi-result laboratory list in one pass', () => {
  const rows = capture.parseLabText([
    'Creatinine\t1.29\tmg/dL\t0.70-1.30',
    'Glucose\t106\tmg/dL\t70-99\tH',
    'HDL  36  mg/dL  40-60  L'
  ].join('\n'));

  assert.equal(rows.length, 3);
  assert.equal(rows[0].display, 'Creatinine');
  assert.equal(rows[0].value, 1.29);
  assert.equal(rows[0].unit, 'mg/dL');
  assert.equal(rows[0].reference_low, 0.70);
  assert.equal(rows[0].reference_high, 1.30);
  assert.equal(rows[1].flag, 'H');
  assert.equal(rows[2].flag, 'L');
});

test('builds provenance-bearing lab import bundle and leaves fasting unknown', async () => {
  const bundle = await capture.buildBundle({
    text: 'Creatinine\t1.29\tmg/dL\t0.70-1.30',
    displayName: 'Displayed portal list',
    sourceType: 'displayed_surface',
    originalFilename: null
  });

  assert.equal(bundle.schema_version, 'steghealth.lab-import-bundle.v0.1');
  assert.equal(bundle.source.source_type, 'displayed_surface');
  assert.equal(bundle.panels[0].fasting_state, 'unknown');
  assert.equal(bundle.panels[0].results.length, 1);
  assert.equal(bundle.provenance.raw_preserved, true);
  assert.match(bundle.provenance.content_hash, /^sha256:[0-9a-f]{64}$/);
  assert.equal(bundle.patient_match.state, 'unconfirmed');
});

test('does not manufacture a result from unstructured prose without numeric columns', () => {
  const rows = capture.parseLabText('Your results are available in the portal.');
  assert.deepEqual(rows, []);
});
