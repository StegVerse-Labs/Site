(()=>{
  const PROJECTION_URL='api/va-claim-assistant/runtime-projection.json';
  let projection=null;
  let ready=false;

  function isSha256(value){return typeof value==='string'&&/^[a-f0-9]{64}$/i.test(value)}
  function isHttps(value){try{const u=new URL(value);return u.protocol==='https:'}catch{return false}}
  function validActiveProjection(p){
    return !!p&&p.schema==='stegverse.va_claims_chat.runtime_projection.v1'&&
      p.capability==='COORDINATED_VA_RESOURCES_LLM'&&p.state==='VERIFIED'&&p.active===true&&
      isHttps(p.endpoint)&&p.endpoint_method==='POST'&&
      isSha256(p.activation_receipt_sha256)&&isSha256(p.execution_receipt_sha256)&&
      p.custody_state==='RECORDED'&&p.reconstruction_state==='PASS'&&
      Array.isArray(p.evidence_refs)&&p.evidence_refs.length>0&&
      p.private_document_upload_active===false&&p.private_document_retrieval_active===false&&
      p.filing_active===false&&p.authority_effect===false&&p.activation_effect===false;
  }

  async function init(){
    try{
      const res=await fetch(PROJECTION_URL,{cache:'no-store',credentials:'omit'});
      if(!res.ok)throw new Error('runtime_projection_unavailable');
      projection=await res.json();
      ready=validActiveProjection(projection);
    }catch{
      projection=null;ready=false;
    }
    window.dispatchEvent(new CustomEvent('va-claims-runtime-state',{detail:status()}));
    return status();
  }

  function status(){return {ready,projection,mode:ready?'COORDINATED_VA_RESOURCES_LLM':'LOCAL_PROCEDURAL_FALLBACK'}}

  function id(prefix){
    if(globalThis.crypto&&crypto.randomUUID)return prefix+crypto.randomUUID();
    return prefix+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);
  }

  async function ask(message){
    if(!ready||!projection)return {used:false,reason:'runtime_not_verified'};
    const transitionId=id('va-site-transition-');
    const runId=id('va-site-run-');
    const eventId=id('va-site-event-');
    const payload={
      message:String(message||'').trim(),
      session_id:sessionStorage.getItem('vaClaimsRuntimeSession')||id('va-site-session-'),
      route_scope:'VA_CLAIMS_CHAT',
      requested_capability:'COORDINATED_VA_RESOURCES_LLM',
      source_policy:'ADMITTED_OFFICIAL_VA_ONLY',
      private_document_context:false,
      filing_requested:false,
      authority_required:true,
      receipt_required:true,
      transition_identity:{
        transition_id:transitionId,
        run_id:runId,
        event_id:eventId,
        origin_manifest_id:'StegVerse-Labs/Site:va-claims-chat.html'
      }
    };
    if(!payload.message)return {used:false,reason:'empty_message'};
    sessionStorage.setItem('vaClaimsRuntimeSession',payload.session_id);
    try{
      const res=await fetch(projection.endpoint,{
        method:'POST',
        mode:'cors',
        credentials:'omit',
        headers:{'Content-Type':'application/json','X-SteGVerse-Session':payload.session_id},
        body:JSON.stringify(payload)
      });
      const body=await res.json().catch(()=>null);
      if(!res.ok||!body)return {used:false,reason:'runtime_request_failed',status:res.status};
      if(body.authority_effect===true||body.activation_effect===true)return {used:false,reason:'authority_escalation_rejected'};
      const text=body.response||body.answer||body.text;
      if(typeof text!=='string'||!text.trim())return {used:false,reason:'runtime_response_missing'};
      return {used:true,text:text.trim(),record:body};
    }catch{
      return {used:false,reason:'runtime_unreachable'};
    }
  }

  window.VAClaimsRuntimeBridge={init,status,ask,validActiveProjection};
  init();
})();
