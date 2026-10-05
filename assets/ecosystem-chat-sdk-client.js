/* Ecosystem Chat conversational client for the existing StegVerse SDK lifecycle.
 * This is a client only. It creates no SDK, ingress, route, standing, authority,
 * credential, runtime or result semantics.
 */
(function(root){
  'use strict';
  const ACTIONS=Object.freeze({
    EXPLAIN:'EXPLAIN',
    BUILD:'BUILD',
    VALIDATE:'VALIDATE',
    SUBMIT:'SUBMIT',
    REPORT:'REPORT'
  });
  const ENDPOINTS=Object.freeze({
    CONTRACT:'/api/sdk/contract',
    BUILD:'/api/sdk/manifest/build',
    VALIDATE:'/api/sdk/manifest/validate',
    SUBMIT:'/api/sdk/manifest/submit'
  });
  const STORE_KEY='ecosystemChatSdkLifecycleEvidenceV1';

  function canonicalAction(value){
    const action=String(value||'').trim().toUpperCase();
    if(!Object.values(ACTIONS).includes(action))throw new Error('SDK_LIFECYCLE_ACTION_REQUIRED');
    return action;
  }
  function readEvidence(){
    try{const value=JSON.parse(sessionStorage.getItem(STORE_KEY)||'[]');return Array.isArray(value)?value:[]}catch{return []}
  }
  function retain(action,payload){
    const evidence=readEvidence();
    evidence.push({
      schema:'stegverse.ecosystem-chat.sdk-lifecycle-evidence.v1',
      action,
      observed_at:new Date().toISOString(),
      exact_sdk_response:payload,
      sdk_response_embellished:false,
      authority_effect:'NONE_CLIENT_RETENTION_ONLY'
    });
    sessionStorage.setItem(STORE_KEY,JSON.stringify(evidence.slice(-20)));
    return evidence[evidence.length-1];
  }
  function hasStanding(value){
    return !!value&&typeof value==='object'&&!Array.isArray(value);
  }
  async function postSdk(endpoint,body){
    const response=await fetch(endpoint,{
      method:'POST',
      credentials:'same-origin',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(body)
    });
    let payload;
    try{payload=await response.json()}catch{throw new Error('SDK_RESPONSE_NOT_JSON')}
    if(!response.ok){
      const exact=payload?.detail&&typeof payload.detail==='object'?payload.detail:payload;
      retain('REFUSED',exact);
      const error=new Error('SDK_CROSSING_REFUSED');
      error.sdk_response=exact;
      error.http_status=response.status;
      throw error;
    }
    return payload;
  }
  async function contract(standing){
    if(!hasStanding(standing))throw new Error('SDK_STANDING_REQUIRED');
    const result=await postSdk(ENDPOINTS.CONTRACT,{standing});
    retain('CONTRACT',result);
    return result;
  }
  async function build(argumentsValue,standing,capabilityDescriptor){
    if(!hasStanding(standing))throw new Error('SDK_STANDING_REQUIRED');
    if(!argumentsValue||typeof argumentsValue!=='object'||Array.isArray(argumentsValue))throw new Error('SDK_BUILD_ARGUMENTS_REQUIRED');
    const body={standing,arguments:argumentsValue};
    if(capabilityDescriptor!==undefined)body.capability_descriptor=capabilityDescriptor;
    const result=await postSdk(ENDPOINTS.BUILD,body);
    retain(ACTIONS.BUILD,result);
    return result;
  }
  async function validate(manifest,standing){
    if(!hasStanding(standing))throw new Error('SDK_STANDING_REQUIRED');
    if(!manifest||typeof manifest!=='object'||Array.isArray(manifest))throw new Error('SDK_MANIFEST_REQUIRED');
    const result=await postSdk(ENDPOINTS.VALIDATE,{standing,manifest});
    retain(ACTIONS.VALIDATE,result);
    return result;
  }
  async function submit(manifest,standing,mode){
    if(!hasStanding(standing))throw new Error('SDK_STANDING_REQUIRED');
    if(!manifest||typeof manifest!=='object'||Array.isArray(manifest))throw new Error('SDK_MANIFEST_REQUIRED');
    const result=await postSdk(ENDPOINTS.SUBMIT,{standing,manifest,mode});
    retain(ACTIONS.SUBMIT,result);
    return result;
  }
  function reportExact(value){
    if(!value||typeof value!=='object'||Array.isArray(value))throw new Error('SDK_RESULT_EVIDENCE_REQUIRED');
    if(value.surface==='MANIFEST_SUBMIT'&&value.result_is_a_handoff_not_a_runtime_result===true){
      return {
        schema:'stegverse.ecosystem-chat.sdk-result-report.v1',
        report_class:'SDK_MANIFEST_HANDOFF',
        disposition:value.envelope?.disposition||null,
        runtime_result_observed:false,
        exact_sdk_evidence:value,
        narrative_ceiling:'HANDOFF_ONLY_DO_NOT_REPORT_RUNTIME_RESULT',
        authority_effect:'NONE_REPORT_ONLY'
      };
    }
    const disposition=value.disposition;
    if(!['ALLOW','DENY','FAIL_CLOSED'].includes(disposition))throw new Error('SDK_RUNTIME_DISPOSITION_REQUIRED');
    return {
      schema:'stegverse.ecosystem-chat.sdk-result-report.v1',
      report_class:'ADMITTED_RUNTIME_RESULT',
      disposition,
      runtime_result_observed:true,
      exact_sdk_evidence:value,
      narrative_ceiling:'REPORT_EXACT_DISPOSITION_AND_MANIFEST_REQUESTED_EVIDENCE_ONLY',
      authority_effect:'NONE_REPORT_ONLY'
    };
  }
  async function perform(request){
    if(!request||typeof request!=='object'||Array.isArray(request))throw new Error('SDK_LIFECYCLE_REQUEST_REQUIRED');
    const action=canonicalAction(request.action);
    if(action===ACTIONS.EXPLAIN){
      return {
        schema:'stegverse.ecosystem-chat.sdk-lifecycle-response.v1',
        action,
        execution_performed:false,
        sdk_crossing_performed:false,
        guidance:'Explain the SDK from its canonical machine contract and capability map. Informational questions never build, validate or submit a manifest.',
        authority_effect:'NONE_INFORMATION_ONLY'
      };
    }
    if(action===ACTIONS.BUILD)return build(request.arguments,request.standing,request.capability_descriptor);
    if(action===ACTIONS.VALIDATE)return validate(request.manifest,request.standing);
    if(action===ACTIONS.SUBMIT)return submit(request.manifest,request.standing,request.mode);
    if(action===ACTIONS.REPORT){
      const report=reportExact(request.evidence);
      retain(ACTIONS.REPORT,report);
      return report;
    }
    throw new Error('SDK_LIFECYCLE_ACTION_UNSUPPORTED');
  }

  root.EcosystemChatSDKClient={
    ACTIONS,ENDPOINTS,perform,contract,build,validate,submit,reportExact,readEvidence,
    authority_effect:'NONE_CLIENT_ONLY',
    standing_is_never_synthesized:true,
    informational_questions_execute:false
  };
}(window));
