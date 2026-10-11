/* DEV-P6 source-only, non-authorizing framework integration contract. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.StegVerseGovernanceIntegration=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const MODES=Object.freeze(['DIRECT_INTEGRATION','GUIDED_INTEGRATION','ASSISTANCE_ON_DEMAND']);
const DISPOSITIONS=Object.freeze(['ALLOW','DENY','FAIL_CLOSED']);
function validate(input){
  if(!input||typeof input!=='object'||Array.isArray(input))return refusal('INVALID_ADAPTER_DESCRIPTOR');
  if(input.schema!=='stegverse.workspace.governance-integration/v1')return refusal('ADAPTER_SCHEMA_NOT_SUPPORTED');
  if(typeof input.framework_id!=='string'||!/^[a-z][a-z0-9._-]{1,63}$/.test(input.framework_id))return refusal('FRAMEWORK_ID_INVALID');
  if(typeof input.adapter_version!=='string'||!/^\d+\.\d+\.\d+$/.test(input.adapter_version))return refusal('ADAPTER_VERSION_INVALID');
  if(!Array.isArray(input.capabilities)||!input.capabilities.length||input.capabilities.some(c=>typeof c!=='string'||!/^[A-Z][A-Z0-9_]{1,63}$/.test(c)))return refusal('CAPABILITIES_INVALID');
  if(input.authority_effect!== 'NONE')return refusal('ADAPTER_MUST_NOT_GRANT_AUTHORITY');
  if(input.governance_route!== 'SDK_MANIFEST_INTR')return refusal('CANONICAL_GOVERNANCE_ROUTE_REQUIRED');
  if(input.tutorial_required!==false)return refusal('TUTORIAL_MUST_NOT_GATE_INTEGRATION');
  if(input.mode!==undefined&&!MODES.includes(input.mode))return refusal('INTEGRATION_MODE_INVALID');
  return Object.freeze({schema:'stegverse.workspace.governance-integration-validation/v1',disposition:'FAIL_CLOSED',predicate:'AUTHENTIC_MANIFEST_BOUND_GOVERNANCE_TRANSITION_NOT_OBSERVED',descriptor_valid:true,mode:input.mode||MODES[0],guidance_required:false,authority_effect:'NONE',submitted:false,certified:false,execution_observed:false});
}
function refusal(predicate){return Object.freeze({schema:'stegverse.workspace.governance-integration-validation/v1',disposition:'FAIL_CLOSED',predicate,descriptor_valid:false,guidance_required:false,authority_effect:'NONE',submitted:false,certified:false,execution_observed:false});}
return Object.freeze({MODES,DISPOSITIONS,validate});
});
