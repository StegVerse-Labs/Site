"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const projectionApi = require("../assets/ecosystem-visual-projection.js");
const transport = require("../assets/ecosystem-visual-render-transport.js");

const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, "fixtures/ecosystem-visual-projection/canonical-events.json"), "utf8"));

function clone(value) { return JSON.parse(JSON.stringify(value)); }
function authority() {
  return {
    renderer_role: "PROJECTION_ONLY",
    canonical_event_mutation: false,
    admission_granted: false,
    evidence_invented: false,
    credential_authorized: false,
    publication_authorized: false,
    custody_authority: false,
    execution_authority: false
  };
}

async function expectFail(label, fn) {
  let failed = false;
  try { await fn(); } catch (error) {
    failed = true;
    assert.match(String(error && error.message), /^FAIL_CLOSED:/, label);
  }
  assert.equal(failed, true, label + " did not fail closed");
}

(async () => {
  const projection = projectionApi.buildProjection(fixture, {
    projection_id: "projection:test-visual-render-001",
    provider_id: "ai-siteflow-compatible",
    capabilities: ["2d", "3d", "animation", "bounded-refinement", "interactive-selection", "topology"],
    canonical_stream: "ecosystem-chat:test-fixture"
  });

  const requestA = await transport.buildRenderRequest(projection, {
    provider_id: "ai-siteflow-compatible",
    requested_capabilities: ["3d", "topology", "interactive-selection"],
    correlation_refs: ["corr:test-001", "session:test-001"]
  });
  const requestB = await transport.buildRenderRequest(projection, {
    provider_id: "ai-siteflow-compatible",
    requested_capabilities: ["interactive-selection", "topology", "3d"],
    correlation_refs: ["session:test-001", "corr:test-001"]
  });
  assert.deepEqual(requestA, requestB, "request construction must be deterministic");
  assert.equal(requestA.authority.renderer_role, "PROJECTION_ONLY");
  assert.equal(requestA.authority.renderer_may_grant_admission, false);
  assert.equal(Object.prototype.hasOwnProperty.call(requestA, "endpoint"), false);
  assert.equal(Object.prototype.hasOwnProperty.call(requestA, "credential_ref"), false);

  const requestSha = await transport.hashRenderRequest(requestA);
  assert.match(requestSha, /^[0-9a-f]{64}$/);
  await transport.validateRenderRequest(requestA, projection);

  const renderedReceipt = {
    schema: transport.RECEIPT_SCHEMA,
    receipt_id: "render-receipt:test-001",
    request_id: requestA.request_id,
    request_sha256: requestSha,
    projection: {
      projection_id: requestA.projection.projection_id,
      sha256: requestA.projection.sha256
    },
    source_event_ids: requestA.source_event_ids.slice(),
    provider: {
      provider_id: "ai-siteflow-compatible",
      capabilities_used: ["3d", "interactive-selection", "topology"]
    },
    status: "RENDERED",
    artifact: {
      artifact_id: "render-artifact:test-001",
      sha256: "a".repeat(64)
    },
    intents: [
      { kind: "SELECT", payload: { node_id: projection.nodes[0].id }, state_change_authorized: false },
      { kind: "REFINE", payload: { focus: "decision-path" }, state_change_authorized: false }
    ],
    observed_at: "2026-09-05T03:20:00Z",
    provenance: {
      request_bound: true,
      projection_bound: true,
      correlation_refs: requestA.correlation_refs.slice()
    },
    authority: authority()
  };
  await transport.validateRenderReceipt(renderedReceipt, requestA, projection);

  const refusedReceipt = clone(renderedReceipt);
  refusedReceipt.receipt_id = "render-receipt:test-refused";
  refusedReceipt.status = "REFUSED";
  refusedReceipt.artifact = null;
  refusedReceipt.intents = [];
  await transport.validateRenderReceipt(refusedReceipt, requestA, projection);

  await expectFail("unsupported requested capability", async () => {
    await transport.buildRenderRequest(projection, { requested_capabilities: ["3d", "state-write"] });
  });

  await expectFail("canonical endpoint embedding", async () => {
    await transport.buildRenderRequest(projection, { requested_capabilities: ["3d"], endpoint: "https://renderer.invalid" });
  });

  await expectFail("projection hash tamper", async () => {
    const alteredProjection = clone(projection);
    alteredProjection.presentation.layout = "tampered-layout";
    await transport.validateRenderRequest(requestA, alteredProjection);
  });

  await expectFail("source event mismatch", async () => {
    const alteredRequest = clone(requestA);
    alteredRequest.source_event_ids = alteredRequest.source_event_ids.slice(1);
    await transport.validateRenderRequest(alteredRequest, projection);
  });

  await expectFail("request hash mismatch", async () => {
    const bad = clone(renderedReceipt);
    bad.request_sha256 = "0".repeat(64);
    await transport.validateRenderReceipt(bad, requestA, projection);
  });

  await expectFail("capability escalation", async () => {
    const bad = clone(renderedReceipt);
    bad.provider.capabilities_used.push("animation");
    await transport.validateRenderReceipt(bad, requestA, projection);
  });

  await expectFail("rendered artifact identity missing", async () => {
    const bad = clone(renderedReceipt);
    bad.artifact = null;
    await transport.validateRenderReceipt(bad, requestA, projection);
  });

  await expectFail("receipt source event mismatch", async () => {
    const bad = clone(renderedReceipt);
    bad.source_event_ids = bad.source_event_ids.slice().reverse();
    await transport.validateRenderReceipt(bad, requestA, projection);
  });

  await expectFail("intent authority escalation", async () => {
    const bad = clone(renderedReceipt);
    bad.intents[0].state_change_authorized = true;
    await transport.validateRenderReceipt(bad, requestA, projection);
  });

  await expectFail("receipt authority escalation", async () => {
    const bad = clone(renderedReceipt);
    bad.authority.admission_granted = true;
    await transport.validateRenderReceipt(bad, requestA, projection);
  });

  console.log("ECOSYSTEM_VISUAL_RENDER_TRANSPORT_TESTS_PASS");
  console.log("cases=12_positive_and_negative_contract_groups");
  console.log("renderer_role=PROJECTION_ONLY");
  console.log("authority_effect=NONE");
})().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exit(1);
});
