const assert = require("node:assert/strict");
const api = require("../assets/evaluator-review.js");

function review(){
  return {
    review_schema:"stegverse.evaluator-review.v1",
    test:{id:"t1",version:4,state:"DRAFT",validation_state:"PASS"},
    manifest:{request_id:"t1",b:2,a:1},
    parties:[
      {party_id:"a",label:"A",required:true},
      {party_id:"b",label:"B",required:true}
    ],
    approvals:[],
    blocking_change_requests:[]
  };
}

(async function(){
  assert.equal(api.canonicalize({b:2,a:{d:4,c:3}}),'{"a":{"c":3,"d":4},"b":2}');
  assert.equal(await api.sha256Hex({a:1,b:2}), await api.sha256Hex({b:2,a:1}));

  const r=review(), hash=await api.sha256Hex(r.manifest);
  assert.equal(api.deriveDisplayState(r,hash),"READY_FOR_APPROVAL");
  assert.equal(api.freezeEligibility(r,hash).eligible,false);

  r.approvals=[
    {party_id:"a",status:"APPROVED",version:4,manifest_hash:hash},
    {party_id:"b",status:"APPROVED",version:4,manifest_hash:hash}
  ];
  assert.equal(api.approvalSummary(r,hash).allRequiredApproved,true);
  assert.equal(api.deriveDisplayState(r,hash),"APPROVED");
  assert.equal(api.freezeEligibility(r,hash).eligible,true);

  r.approvals[1].manifest_hash="stale";
  assert.equal(api.approvalSummary(r,hash).allRequiredApproved,false);
  assert.equal(api.deriveDisplayState(r,hash),"PARTIALLY_APPROVED");
  assert.equal(api.freezeEligibility(r,hash).eligible,false);

  r.approvals[1].manifest_hash=hash;
  r.blocking_change_requests=[{id:"c1",status:"OPEN"}];
  assert.equal(api.deriveDisplayState(r,hash),"CHANGES_REQUESTED");
  assert.equal(api.freezeEligibility(r,hash).eligible,false);

  r.blocking_change_requests=[];
  const approvalPayload=api.exactApprovalPayload(r,hash);
  assert.deepEqual(approvalPayload,{testId:"t1",revision:4,manifestHash:hash,attestation:"TEST_SPECIFICATION_ONLY"});
  assert.throws(()=>api.exactChangePayload(r,hash,"","general"),/reason is required/i);

  const frozen=review();
  frozen.test.state="FROZEN";
  frozen.test.frozen_manifest_hash=hash;
  assert.equal(api.validateReviewModel(frozen).ok,true);
  assert.equal(api.isFrozen(frozen),true);
  assert.equal(api.frozenHash(frozen),hash);

  const bad=review();
  bad.test.state="FROZEN";
  assert.equal(api.validateReviewModel(bad).ok,false);

  console.log("EVALUATOR_REVIEW_UI_LOGIC_PASS");
})().catch(err=>{console.error(err);process.exit(1);});
