"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");
const projection = require("../assets/ecosystem-visual-projection.js");

const fixturePath = path.join(__dirname, "fixtures", "ecosystem-visual-projection", "canonical-events.json");
const events = JSON.parse(fs.readFileSync(fixturePath, "utf8"));

const first = projection.buildProjection(events, {
  projection_id: "projection:test-001",
  provider_id: "ai-siteflow-compatible",
  capabilities: ["3d", "topology", "interactive-selection", "animation"],
  mode: "3d"
});
const second = projection.buildProjection(events, {
  projection_id: "projection:test-001",
  provider_id: "ai-siteflow-compatible",
  capabilities: ["3d", "topology", "interactive-selection", "animation"],
  mode: "3d"
});

assert.deepStrictEqual(first, second, "projection must be deterministic for identical canonical inputs");
assert.strictEqual(first.authority.renderer_role, "PROJECTION_ONLY");
assert.strictEqual(first.authority.renderer_may_grant_admission, false);
assert.strictEqual(first.nodes.length, 3);
assert.strictEqual(first.edges.length, 2);
assert.strictEqual(first.nodes[1].state, "ADMITTED");
assert.ok(first.provenance.evidence_refs.includes("evidence:constraint-set-001"));
assert.ok(first.provenance.policy_refs.includes("policy:entity-neutral-transition-evaluation"));
assert.ok(first.provenance.artifact_refs.includes("artifact:receipt-001"));

const descriptor = projection.siteFlowCapabilityDescriptor();
assert.strictEqual(descriptor.integration_state, "CAPABILITY_DESCRIPTOR_ONLY");
assert.strictEqual(descriptor.endpoint, null);
assert.strictEqual(descriptor.credential_ref, null);
assert.ok(descriptor.capabilities.includes("3d"));

assert.throws(
  () => projection.buildProjection([{ event_id: "orphan", event_type: "message", parent_event_id: "missing" }]),
  /FAIL_CLOSED: unresolved parent_event_id/,
  "unresolved canonical references must fail closed"
);

const escalated = JSON.parse(JSON.stringify(first));
escalated.authority.renderer_may_grant_admission = true;
assert.throws(
  () => projection.validateProjection(escalated),
  /FAIL_CLOSED: renderer admission authority prohibited/,
  "renderer authority escalation must fail closed"
);

const noProvenance = JSON.parse(JSON.stringify(first));
delete noProvenance.provenance;
assert.throws(
  () => projection.validateProjection(noProvenance),
  /FAIL_CLOSED: projection provenance missing/,
  "missing provenance must fail closed"
);

console.log("ecosystem visual projection contract: PASS");
