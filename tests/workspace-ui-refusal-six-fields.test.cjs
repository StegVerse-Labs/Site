'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {test} = require('node:test');

const source = fs.readFileSync(path.join(__dirname, '..', 'assets', 'workspace.js'), 'utf8');
function extract(name) {
  const start = source.indexOf('function ' + name + '(');
  assert.notEqual(start, -1, name + ' exists');
  const open = source.indexOf('{', start);
  let depth = 0, quote = null, escaped = false;
  for (let i = open; i < source.length; i++) {
    const ch = source[i];
    if (quote) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === quote) quote = null;
    } else if (ch === '"' || ch === "'" || ch === '`') quote = ch;
    else if (ch === '{') depth++;
    else if (ch === '}' && --depth === 0) return source.slice(source.slice(Math.max(0,start-6),start)==='async '?start-6:start, i + 1);
  }
  throw Error('Unclosed ' + name);
}
const keys = ['failure_code','failed_predicate','required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'];
async function run(bridge) {
  const state = {kvIngress: null, projection: null};
  const context = {
    window: {StegVerseWorkspaceKVBridge: bridge},
    state,
    OWNING_GOAL: 'STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001',
    setRuntime() {}, renderAll() {}, recordNodeBinding() {},
    pickActionable() { return {}; },
  };
  vm.createContext(context);
  vm.runInContext(extract('actionableFor') + '\n' + extract('loadPersonalKV') + '\nthis.runKV=loadPersonalKV;', context);
  await context.runKV();
  return state.kvIngress;
}
function assertSixFields(d, predicate) {
  assert.equal(d.disposition, 'FAIL_CLOSED');
  assert.equal(d.predicate, predicate);
  for (const k of keys) assert.equal(typeof d[k], 'string', k + ' is present');
  for (const k of keys) assert.ok(d[k].trim(), k + ' is nonempty');
  assert.equal(d.failure_code, predicate);
  assert.equal(d.failed_predicate, predicate);
  assert.equal(d.owning_existing_goal, 'STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001');
}
test('absent DEVICE_KV bridge preserves six actionable refusal fields', async () => {
  assertSixFields(await run(null), 'WORKSPACE_DEVICE_KV_BRIDGE_UNAVAILABLE');
});
test('generic bridge exception preserves six actionable refusal fields', async () => {
  assertSixFields(await run({loadPersonalWorkspace: async () => {throw Error('unavailable');}}), 'WORKSPACE_DEVICE_KV_PATH_UNAVAILABLE');
});
test('unbound ingress exception preserves six actionable refusal fields', async () => {
  assertSixFields(await run({loadPersonalWorkspace: async () => {throw Error('sovereign InTr ingress unavailable');}}), 'AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE');
});
