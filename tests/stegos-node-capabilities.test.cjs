"use strict";
const {test} = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const root = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(root, "assets/stegos-resident-health.js"), "utf8");
const discovery = JSON.parse(fs.readFileSync(path.join(root, "stegos-node/capabilities.json")));
const schema = JSON.parse(fs.readFileSync(path.join(root, "stegos-node/resident-health.schema.json")));

// Assert emitted reports against the keywords used by this data contract;
// this is a bounded test helper, not a general JSON Schema implementation.
function checkContract(value, contract) {
  if (Object.hasOwn(contract, "const")) assert.deepEqual(value, contract.const);
  if (contract.enum) assert.ok(contract.enum.includes(value), `unexpected value ${value}`);
  if (contract.type) {
    const type = value === null ? "null" : Array.isArray(value) ? "array" : typeof value;
    assert.ok([].concat(contract.type).includes(type), `unexpected type ${type}`);
  }
  for (const key of contract.required || []) assert.ok(Object.hasOwn(value, key), `missing ${key}`);
  for (const [key, child] of Object.entries(contract.properties || {})) {
    if (Object.hasOwn(value, key)) checkContract(value[key], child);
  }
  if (contract.items) value.forEach(item => checkContract(item, contract.items));
  if (contract.format === "date-time") assert.ok(Number.isFinite(Date.parse(value)));
}

function harness(options = {}) {
  const calls = {probe: 0, node: 0, repairs: 0, events: 0};
  const worker = {scriptURL: "https://stegverse.org/stegos-bootstrap/service-worker.js?v=1", state: "activated", ...options.worker};
  const registration = {scope: "https://stegverse.org/stegos-bootstrap/", active: worker, ...options.registration};
  const document = {readyState: "loading", body: null, getElementById: () => null, addEventListener() {}};
  const window = {
    document, location: {origin: "https://stegverse.org", pathname: "/my-kv.html", search: ""},
    isSecureContext: true, indexedDB: {}, crypto: {subtle: {}, getRandomValues() {}},
    navigator: {serviceWorker: {getRegistration: async () => {
      if (options.workerError) throw Error("worker lookup failed");
      return options.noWorker ? null : registration;
    }}},
    StegOSWebBootstrap: {
      probeOperationalReadiness: async () => {
        calls.probe++;
        if (options.probeError) throw Error("probe failed");
        return {state: "READY", indexeddb_operational: true, webcrypto_operational: true, ...options.runtime};
      },
      establishNode: () => {calls.repairs++; throw Error("unexpected repair");},
      registerOfflineShell: () => {calls.repairs++; throw Error("unexpected repair");}
    },
    StegVerseNodeContinuity: {status: async () => {
      calls.node++;
      if (options.nodeError) throw Error("invalid genesis");
      return {registered: true, registration: {node_id: "fixture-node"}, ...options.node};
    }},
    dispatchEvent() {calls.events++;}
  };
  if (options.capabilityOnly) delete window.StegOSWebBootstrap;
  if (options.continuityError) window.StegOSDeviceContinuity = {readRoot: async () => {throw Error("continuity failed");}};
  vm.runInNewContext(source, {window, URL, CustomEvent: function(type, data) {this.type = type; this.detail = data.detail;}});
  return {api: window.StegOSResidentHealth, calls};
}

test("discovery describes interfaces without asserting a live Node or remote runtime", () => {
  assert.equal(discovery.authority_effect, "NONE");
  assert.equal(discovery.discovery_is_read_only, true);
  assert.equal(discovery.discovery_proves_node_health, false);
  assert.equal(discovery.discovery_registers_node, false);
  assert.equal(discovery.discovery_grants_execution_authority, false);
  assert.equal(discovery.interfaces.health.schema, schema.properties.schema.const);
  assert.equal(discovery.interfaces.health.schema_path, schema.properties.schema_ref.const);
  for (const name of ["health", "genesis", "repair", "receipts"]) assert.equal(discovery.interfaces[name].http_endpoint, null);
  for (const name of ["node_id", "health", "receipts", "credentials"]) assert.equal(Object.hasOwn(discovery, name), false);
  assert.ok(fs.readFileSync(path.join(root, "stegos-node/index.html"), "utf8").includes('href="./capabilities.json"'));
});

test("last is a passive snapshot, null before diagnosis and detached afterwards", async () => {
  const {api, calls} = harness();
  assert.equal(api.last(), null);
  assert.deepEqual(calls, {probe: 0, node: 0, repairs: 0, events: 0});
  const report = await api.diagnose();
  checkContract(report, schema);
  assert.equal(report.resident_install_health, "HEALTHY");
  assert.equal(report.repair_required, false);
  assert.equal(report.repair_reasons.length, 0);
  const before = {...calls};
  const snapshot = api.last();
  snapshot.node.node_id = "tampered";
  assert.equal(api.last().node.node_id, "fixture-node");
  assert.deepEqual(calls, before);
  assert.equal(report.diagnostic_is_read_only, false);
  assert.equal(report.node_authority, "NOT_EVALUATED");
  assert.equal(report.network_membership, "NOT_EVALUATED");
});

for (const [name, options, reason] of [
  ["browser capability alone", {capabilityOnly: true}, "LOCAL_RUNTIME_NOT_READY"],
  ["READY prefix spoof", {runtime: {state: "READY_FOR_ANYTHING"}}, "LOCAL_RUNTIME_NOT_READY"],
  ["missing operational crypto", {runtime: {webcrypto_operational: false}}, "LOCAL_RUNTIME_NOT_READY"],
  ["probe exception", {probeError: true}, "LOCAL_RUNTIME_NOT_READY"],
  ["absent Node", {node: {registered: false, registration: null}}, "VALID_NODE_NOT_OBSERVED"],
  ["invalid genesis", {nodeError: true}, "VALID_NODE_NOT_OBSERVED"],
  ["worker path suffix spoof", {worker: {scriptURL: "https://stegverse.org/stegos-bootstrap/service-worker.js.evil"}}, "STEGOS_SERVICE_WORKER_REPAIR_REQUIRED"],
  ["worker wrong origin", {worker: {scriptURL: "https://example.invalid/stegos-bootstrap/service-worker.js"}}, "STEGOS_SERVICE_WORKER_REPAIR_REQUIRED"],
  ["worker wrong scope", {registration: {scope: "https://stegverse.org/"}}, "STEGOS_SERVICE_WORKER_REPAIR_REQUIRED"],
  ["installing worker", {registration: {active: null, installing: {scriptURL: "https://stegverse.org/stegos-bootstrap/service-worker.js", state: "installing"}}}, "STEGOS_SERVICE_WORKER_REPAIR_REQUIRED"],
  ["redundant worker", {worker: {state: "redundant"}}, "STEGOS_SERVICE_WORKER_REPAIR_REQUIRED"],
  ["missing worker", {noWorker: true}, "STEGOS_SERVICE_WORKER_REPAIR_REQUIRED"],
  ["worker lookup error", {workerError: true}, "STEGOS_SERVICE_WORKER_REPAIR_REQUIRED"],
  ["continuity exception", {continuityError: true}, "DEVICE_CONTINUITY_CHECK_FAILED"]
]) {
  test(`${name} cannot report HEALTHY`, async () => {
    const {api, calls} = harness(options);
    const report = await api.diagnose();
    checkContract(report, schema);
    assert.equal(report.resident_install_health, "REPAIR_REQUIRED");
    assert.equal(report.repair_required, true);
    assert.ok(report.repair_reasons.includes(reason));
    assert.equal(report.authority_effect, "NONE");
    assert.equal(calls.repairs, 0);
  });
}

test("contract refuses authority escalation and missing structure", async () => {
  const report = JSON.parse(JSON.stringify(await harness().api.diagnose()));
  report.provider_operation_authorized = true;
  assert.throws(() => checkContract(report, schema));
  report.provider_operation_authorized = false;
  delete report.node;
  assert.throws(() => checkContract(report, schema));
});
