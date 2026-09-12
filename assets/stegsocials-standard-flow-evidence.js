(function(root,factory){
  "use strict";
  var api=factory(root||{});
  if(typeof module==="object"&&module.exports) module.exports=api;
  if(root) root.StegVerseStegSocialsStandardFlowEvidence=api;
}(typeof globalThis!=="undefined"?globalThis:this,function(root){
  "use strict";

  var PREPARATION_SCHEMA="stegverse.stegsocials.post-preparation/v1";
  var ADMISSION_SCHEMA="stegverse.site.stegsocials-kv-draft-admission-result/v1";
  var READBACK_SCHEMA="stegverse.site.stegsocials-kv-exact-content-readback/v1";
  var EVIDENCE_SCHEMA="stegverse.site.stegsocials-standard-flow-evidence/v1";
  var TASK_ID="SS-EVIDENCE-COMPARISON-001";
  var DRAFT_RE=/^02_Research\/StegSocials\/Drafts\/(LinkedIn|Facebook|Instagram|X|Other)\/[A-Za-z0-9._-]+\.json$/;
  var HASH_RE=/^sha256:[a-f0-9]{64}$/;

  function requireValue(ok,message){if(!ok)throw new Error("FAIL_CLOSED: "+message);}
  function clone(value){return JSON.parse(JSON.stringify(value));}
  function falseBoundary(value,label){
    requireValue(value&&value.provider_call_performed===false,label+" provider boundary invalid");
    requireValue(value.credential_material_present===false,label+" credential boundary invalid");
    if(Object.prototype.hasOwnProperty.call(value,"provider_operation_authorized")){
      requireValue(value.provider_operation_authorized===false,label+" provider-operation boundary invalid");
    }
  }
  function validate(input){
    requireValue(input&&typeof input==="object","standard-flow evidence input required");
    var preparation=input.preparation,admission=input.admission,readback=input.readback;
    requireValue(preparation&&preparation.schema===PREPARATION_SCHEMA,"preparation schema invalid");
    requireValue(preparation.task_id===TASK_ID,"preparation task binding invalid");
    requireValue(typeof preparation.bundle_id==="string"&&preparation.bundle_id.length>0,"preparation bundle id missing");
    requireValue(preparation.kv_context&&DRAFT_RE.test(String(preparation.kv_context.draft_path||"")),"preparation draft path invalid");
    requireValue(preparation.execution&&preparation.execution.publication_authority_effect==="NONE_PREPARATION_ONLY","preparation authority boundary invalid");
    falseBoundary(preparation.execution,"preparation");

    requireValue(admission&&admission.schema===ADMISSION_SCHEMA,"admission schema invalid");
    requireValue(admission.state==="KV_DRAFT_ADMITTED_HASH_READBACK","admission state invalid");
    requireValue(admission.bundle_id===preparation.bundle_id,"admission bundle mismatch");
    requireValue(admission.canonical_path===preparation.kv_context.draft_path,"admission path mismatch");
    requireValue(HASH_RE.test(String(admission.sha256||"")),"admission SHA-256 invalid");
    requireValue(Number.isInteger(admission.size_bytes)&&admission.size_bytes>0,"admission size invalid");
    requireValue(admission.canonical_kv_admission_observed===true&&admission.admitted_hash_readback_verified===true,"admission observation incomplete");
    falseBoundary(admission,"admission");

    requireValue(readback&&readback.schema===READBACK_SCHEMA,"readback schema invalid");
    requireValue(readback.state==="EXACT_CONTENT_BYTES_READBACK_VERIFIED","readback state invalid");
    requireValue(readback.canonical_path===admission.canonical_path,"readback path mismatch");
    requireValue(readback.sha256===admission.sha256,"readback SHA-256 mismatch");
    requireValue(readback.size_bytes===admission.size_bytes,"readback size mismatch");
    requireValue(readback.exact_content_bytes_readback_verified===true,"exact readback incomplete");
    requireValue(readback.cloud_provider_readback_observed===false,"cloud/provider readback may not be inferred");
    falseBoundary(readback,"readback");

    requireValue(typeof input.observed_at==="string"&&!isNaN(Date.parse(input.observed_at)),"observation timestamp invalid");

    return {preparation:clone(preparation),admission:clone(admission),readback:clone(readback),observed_at:input.observed_at};
  }
  function materialize(input){
    var v=validate(input);
    return {
      schema:EVIDENCE_SCHEMA,
      state:"STANDARD_FLOW_EVIDENCE_READY",
      task_id:TASK_ID,
      bundle_id:v.preparation.bundle_id,
      observed_at:v.observed_at,
      preparation:{schema:v.preparation.schema,publication_plan:v.preparation.publication_plan,erl_refs:v.preparation.kv_context.erl_refs},
      kv_evidence:{
        canonical_path:v.readback.canonical_path,
        sha256:v.readback.sha256,
        size_bytes:v.readback.size_bytes,
        admission_state:v.admission.state,
        materialization_id:v.admission.materialization_id||null,
        request_hash:v.admission.request_hash||null,
        exact_content_readback_state:v.readback.state,
        canonical_kv_admission_observed:true,
        admitted_hash_readback_verified:true,
        exact_content_bytes_readback_verified:true,
        cloud_provider_readback_observed:false
      },
      identity_authority_source:"KV_SKAP_ONLY",
      transport_node_role:"NON_AUTHORITATIVE_INTERCHANGEABLE",
      publication_state:"PREPARED_NOT_PUBLISHED",
      provider_call_performed:false,
      credential_material_present:false,
      provider_operation_authorized:false,
      authority_effect:"NONE_OBSERVATION_ONLY"
    };
  }
  function filename(evidence){
    requireValue(evidence&&evidence.schema===EVIDENCE_SCHEMA&&evidence.state==="STANDARD_FLOW_EVIDENCE_READY","export evidence invalid");
    return "stegsocials-standard-flow-evidence-"+String(evidence.bundle_id).replace(/[^A-Za-z0-9._-]+/g,"-")+".json";
  }
  function download(evidence){
    requireValue(root.Blob&&root.URL&&typeof root.URL.createObjectURL==="function","browser download API unavailable");
    requireValue(root.document&&typeof root.document.createElement==="function","browser document unavailable");
    var data=JSON.stringify(evidence,null,2)+"\n",blob=new root.Blob([data],{type:"application/json"}),url=root.URL.createObjectURL(blob),a=root.document.createElement("a");
    a.href=url;a.download=filename(evidence);a.rel="noopener";a.style.display="none";
    root.document.body.appendChild(a);a.click();a.remove();
    if(typeof root.setTimeout==="function")root.setTimeout(function(){root.URL.revokeObjectURL(url);},0);
    else root.URL.revokeObjectURL(url);
    return {filename:a.download,size_bytes:data.length};
  }

  return Object.freeze({SCHEMA:EVIDENCE_SCHEMA,TASK_ID:TASK_ID,validate:validate,materialize:materialize,filename:filename,download:download});
}));
