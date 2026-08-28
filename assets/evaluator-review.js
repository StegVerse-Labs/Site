(function(root,factory){
  var api=factory();
  if(typeof module!=="undefined"&&module.exports)module.exports=api;
  root.StegVerseEvaluatorReview=api;
}(typeof globalThis!=="undefined"?globalThis:this,function(){
"use strict";

var STATES=["DRAFT","CHANGES_REQUESTED","READY_FOR_APPROVAL","PARTIALLY_APPROVED","APPROVED","FROZEN","EXECUTING","EXECUTED","RESULTS_AVAILABLE"];

function sortValue(value){
  if(Array.isArray(value)) return value.map(sortValue);
  if(value&&typeof value==="object"){
    var out={};
    Object.keys(value).sort().forEach(function(k){out[k]=sortValue(value[k]);});
    return out;
  }
  return value;
}
function canonicalize(value){return JSON.stringify(sortValue(value));}

async function sha256Hex(value){
  var text=typeof value==="string"?value:canonicalize(value);
  if(typeof require==="function"){
    try{return require("node:crypto").createHash("sha256").update(text,"utf8").digest("hex");}catch(_e){}
  }
  if(!root.crypto||!root.crypto.subtle)throw new Error("SHA-256 unavailable in this runtime");
  var bytes=new TextEncoder().encode(text);
  var digest=await root.crypto.subtle.digest("SHA-256",bytes);
  return Array.from(new Uint8Array(digest)).map(function(b){return b.toString(16).padStart(2,"0");}).join("");
}
function humanize(value){
  return String(value==null?"":value).replace(/[_-]+/g," ").replace(/\b\w/g,function(c){return c.toUpperCase();});
}
function currentInput(review){return review&&review.manifest&&review.manifest.input&&review.manifest.input.input_data||{};}
function deriveVector(review){
  var data=currentInput(review);
  return {
    initial:data.initial_state||{},
    transition:data.transition||{},
    successor:data.successor_state||{},
    invariant:data.normative_invariant||""
  };
}
function approvalMatchesCurrent(approval,review,manifestHash){
  return !!approval &&
    approval.status==="APPROVED" &&
    Number(approval.version)===Number(review.test.version) &&
    approval.manifest_hash===manifestHash;
}
function approvalSummary(review,manifestHash){
  var required=(review.parties||[]).filter(function(p){return p.required!==false;});
  var approvals=review.approvals||[];
  var rows=required.map(function(p){
    var matching=approvals.find(function(a){return a.party_id===p.party_id&&approvalMatchesCurrent(a,review,manifestHash);})||null;
    return {party:p,approval:matching,approved:!!matching};
  });
  return {
    rows:rows,
    allRequiredApproved:rows.length>0&&rows.every(function(r){return r.approved;}),
    approvedCount:rows.filter(function(r){return r.approved;}).length,
    requiredCount:rows.length
  };
}
function unresolvedBlocking(review){
  return (review.blocking_change_requests||[]).filter(function(r){return r.status!=="RESOLVED";});
}
function freezeEligibility(review,manifestHash){
  var summary=approvalSummary(review,manifestHash);
  var blockers=unresolvedBlocking(review);
  var validation=review.test&&review.test.validation_state;
  var valid=validation==="PASS"||validation==="VALIDATED";
  var alreadyFrozen=review.test&&review.test.state==="FROZEN";
  var reasons=[];
  if(alreadyFrozen)reasons.push("Already frozen");
  if(!summary.allRequiredApproved)reasons.push("Required approvals do not all match this exact version and hash");
  if(blockers.length)reasons.push("Blocking change requests remain unresolved");
  if(!valid)reasons.push("Required manifest validation has not passed");
  return {eligible:!alreadyFrozen&&summary.allRequiredApproved&&!blockers.length&&valid,reasons:reasons,summary:summary,blockers:blockers};
}
function deriveDisplayState(review,manifestHash){
  var declared=review.test&&review.test.state||"DRAFT";
  if(["FROZEN","EXECUTING","EXECUTED","RESULTS_AVAILABLE"].includes(declared))return declared;
  if(unresolvedBlocking(review).length)return "CHANGES_REQUESTED";
  var a=approvalSummary(review,manifestHash);
  if(a.allRequiredApproved)return "APPROVED";
  if(a.approvedCount>0)return "PARTIALLY_APPROVED";
  if(review.test&&(review.test.validation_state==="PASS"||review.test.validation_state==="VALIDATED"))return "READY_FOR_APPROVAL";
  return STATES.includes(declared)?declared:"DRAFT";
}
function resultStatus(review){
  if(!review.results)return "INDETERMINATE";
  return review.results.overall||"INDETERMINATE";
}
function exactApprovalPayload(review,manifestHash){
  return {
    testId:review.test.id,
    revision:review.test.version,
    manifestHash:manifestHash,
    attestation:"TEST_SPECIFICATION_ONLY"
  };
}
function exactChangePayload(review,manifestHash,reason,section){
  if(!String(reason||"").trim())throw new Error("A reason is required");
  return {
    testId:review.test.id,
    reason:String(reason).trim(),
    section:section||"general",
    revision:review.test.version,
    manifestHash:manifestHash
  };
}
function bridge(){
  var b=root.StegVerseEvaluatorReviewBridge;
  return b&&typeof b==="object"?b:null;
}
async function invoke(name,payload){
  var b=bridge();
  if(!b||typeof b[name]!=="function")throw new Error("This action requires an authorized StegVerse review runtime. Public read mode cannot perform "+name+".");
  return b[name](payload);
}
async function loadReview(options){
  options=options||{};
  var b=bridge();
  if(b&&typeof b.loadReview==="function")return b.loadReview(options);
  var source=options.source||"data/evaluator-review/cross-framework-current-basis-001.json";
  var response=await fetch(source,{cache:"no-store"});
  if(!response.ok)throw new Error("Review data unavailable ("+response.status+")");
  return response.json();
}
function isFrozen(review){return review&&review.test&&review.test.state==="FROZEN";}
function frozenHash(review){return isFrozen(review)?review.test.frozen_manifest_hash||null:null;}
function validateReviewModel(review){
  var errors=[];
  if(!review||review.review_schema!=="stegverse.evaluator-review.v1")errors.push("unsupported review schema");
  if(!review||!review.test||!review.test.id)errors.push("missing test id");
  if(!review||!review.manifest||!review.manifest.request_id)errors.push("missing evaluator manifest");
  if(review&&review.test&&review.manifest&&review.test.id!==review.manifest.request_id)errors.push("test id does not match manifest request_id");
  if(isFrozen(review)&&!review.test.frozen_manifest_hash)errors.push("frozen review missing frozen manifest hash");
  return {ok:errors.length===0,errors:errors};
}
return {
  STATES:STATES,
  canonicalize:canonicalize,
  sha256Hex:sha256Hex,
  humanize:humanize,
  deriveVector:deriveVector,
  approvalMatchesCurrent:approvalMatchesCurrent,
  approvalSummary:approvalSummary,
  unresolvedBlocking:unresolvedBlocking,
  freezeEligibility:freezeEligibility,
  deriveDisplayState:deriveDisplayState,
  resultStatus:resultStatus,
  exactApprovalPayload:exactApprovalPayload,
  exactChangePayload:exactChangePayload,
  invoke:invoke,
  loadReview:loadReview,
  bridge:bridge,
  isFrozen:isFrozen,
  frozenHash:frozenHash,
  validateReviewModel:validateReviewModel
};
}));