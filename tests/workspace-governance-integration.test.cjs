const assert=require('node:assert/strict');
const G=require('../assets/workspace-governance-integration.js');
const base={schema:'stegverse.workspace.governance-integration/v1',framework_id:'generic.framework',adapter_version:'1.0.0',capabilities:['READ_PROJECTION'],authority_effect:'NONE',governance_route:'SDK_MANIFEST_INTR',tutorial_required:false};
for(const mode of G.MODES){const v=G.validate({...base,mode});assert.equal(v.descriptor_valid,true);assert.equal(v.mode,mode);assert.equal(v.guidance_required,false);assert.equal(v.submitted,false);assert.equal(v.certified,false);assert.equal(v.execution_observed,false);assert.equal(v.disposition,'FAIL_CLOSED');}
assert.equal(G.validate(base).mode,'DIRECT_INTEGRATION');
for(const [change,predicate] of [[{tutorial_required:true},'TUTORIAL_MUST_NOT_GATE_INTEGRATION'],[{authority_effect:'ALLOW'},'ADAPTER_MUST_NOT_GRANT_AUTHORITY'],[{governance_route:'DIRECT_GITHUB'},'CANONICAL_GOVERNANCE_ROUTE_REQUIRED'],[{mode:'FORCED_TUTORIAL'},'INTEGRATION_MODE_INVALID'],[{capabilities:[]},'CAPABILITIES_INVALID']]){const v=G.validate({...base,...change});assert.equal(v.descriptor_valid,false);assert.equal(v.predicate,predicate);assert.equal(v.disposition,'FAIL_CLOSED');}
assert.equal(G.validate(null).predicate,'INVALID_ADAPTER_DESCRIPTOR');
console.log('DEV_P6_CONTRACT_TEST_PASS');
