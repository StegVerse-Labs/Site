"use strict";

const assert = require("node:assert/strict");
const states = require("../stegos-node/services-state.js");

function service(overrides = {}) {
  return {
    entry_type: "SERVICE",
    entry_id: "email-continuity",
    local_materialization: "READY_FOR_LOCAL_UI",
    governed_action_readiness: "BLOCKED",
    governed_blockers: ["production_interlock_runtime_activated"],
    activation_performed: false,
    authority_effect: "NONE",
    ...overrides
  };
}

let result = states.classify(service(), {
  registration_verified: false,
  production_interlock_runtime_activated: false
});
assert.equal(result.service_state, "REVIEW");
assert.equal(result.color, "YELLOW");
assert.equal(result.required_action, "REGISTER DEVICE");
assert.equal(result.activation_performed, false);

result = states.classify(service(), {
  registration_verified: true,
  production_interlock_runtime_activated: false
});
assert.equal(result.service_state, "INACTIVE");
assert.equal(result.color, "GRAY");

result = states.classify(service({
  local_materialization: "BLOCKED_CURRENT_IDENTITY",
  governed_blockers: ["current_identity_continuity_receipt_observed"]
}), {
  registration_verified: true,
  production_interlock_runtime_activated: false
});
assert.equal(result.service_state, "REVIEW");
assert.equal(result.required_action, "RE-REGISTER DEVICE");

result = states.classify(service({
  local_materialization: "BLOCKED_PROVIDER",
  governed_blockers: ["provider_session_evidence_observed"]
}), {
  registration_verified: true,
  production_interlock_runtime_activated: false
});
assert.equal(result.service_state, "UNAVAILABLE");
assert.equal(result.color, "RED");

result = states.classify(service({
  governed_action_readiness: "READY_FOR_GOVERNED_ACTION",
  governed_blockers: []
}), {
  registration_verified: true,
  production_interlock_runtime_activated: true
});
assert.equal(result.service_state, "ACTIVE");
assert.equal(result.color, "GREEN");

result = states.classify(service({
  governed_action_readiness: "READY_FOR_GOVERNED_ACTION",
  governed_blockers: []
}), {
  registration_verified: true,
  production_interlock_runtime_activated: false
});
assert.equal(result.service_state, "UNAVAILABLE", "ACTIVE must fail closed without runtime activation");

result = states.classify(service({ authority_effect: "GRANTED" }), {
  registration_verified: true,
  production_interlock_runtime_activated: true
});
assert.equal(result.service_state, "UNAVAILABLE", "authority-bearing source must fail closed");

for (const name of ["ACTIVE", "REVIEW", "UNAVAILABLE", "INACTIVE"]) {
  assert.ok(states.COLORS[name], "missing color mapping for " + name);
}

console.log("STEGVERSE_ME_SERVICES_STATE_TEST_PASS");
console.log("AUTHORITY_EFFECT=NONE");
console.log("ACTIVATION_EFFECT=false");
