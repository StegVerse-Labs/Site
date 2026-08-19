(()=>{
  const PROJECTION_URL='api/va-claim-assistant/runtime-projection.json';
  let projection=null;
  let ready=false;
  let generalMode=false;

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

  function status(){return {ready,projection,mode:ready?'COORDINATED_VA_RESOURCES_LLM':'LOCAL_PROCEDURAL_FALLBACK'}}

  function updateCapabilityLabel(){
    const el=document.querySelector('#chat .state');
    if(!el)return;
    el.textContent=ready?'Current capability: COORDINATED VA RESOURCES LLM':'Current capability: SOURCE-GROUNDED PROCEDURAL HELP';
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
    updateCapabilityLabel();
    window.dispatchEvent(new CustomEvent('va-claims-runtime-state',{detail:status()}));
    return status();
  }

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
      transition_identity:{transition_id:transitionId,run_id:runId,event_id:eventId,origin_manifest_id:'StegVerse-Labs/Site:va-claims-chat.html'}
    };
    if(!payload.message)return {used:false,reason:'empty_message'};
    sessionStorage.setItem('vaClaimsRuntimeSession',payload.session_id);
    try{
      const res=await fetch(projection.endpoint,{method:'POST',mode:'cors',credentials:'omit',headers:{'Content-Type':'application/json','X-SteGVerse-Session':payload.session_id},body:JSON.stringify(payload)});
      const body=await res.json().catch(()=>null);
      if(!res.ok||!body)return {used:false,reason:'runtime_request_failed',status:res.status};
      if(body.authority_effect===true||body.activation_effect===true)return {used:false,reason:'authority_escalation_rejected'};
      const text=body.response||body.answer||body.text;
      if(typeof text!=='string'||!text.trim())return {used:false,reason:'runtime_response_missing'};
      return {used:true,text:text.trim(),record:body};
    }catch{return {used:false,reason:'runtime_unreachable'}}
  }

  function addMessage(kind,text){
    const log=document.getElementById('log');if(!log)return;
    const d=document.createElement('div');d.className='msg '+kind;d.textContent=text;log.appendChild(d);log.scrollTop=log.scrollHeight;
  }

  function loadSemanticCommands(){
    if(window.StegVerseSemanticCommands)return Promise.resolve(true);
    return new Promise(resolve=>{
      const existing=document.querySelector('script[data-stegverse-semantic-commands]');
      if(existing){existing.addEventListener('load',()=>resolve(!!window.StegVerseSemanticCommands),{once:true});existing.addEventListener('error',()=>resolve(false),{once:true});return}
      const script=document.createElement('script');
      script.src='assets/semantic-command-router.js';script.async=false;script.dataset.stegverseSemanticCommands='1';
      script.onload=()=>resolve(!!window.StegVerseSemanticCommands);script.onerror=()=>resolve(false);document.head.appendChild(script);
    });
  }

  async function interceptSemanticCommand(event){
    const input=document.getElementById('question');
    if(!input||!/^\/[a-z0-9_-]+(?:\s|$)/i.test(input.value.trim()))return false;
    event.preventDefault();event.stopImmediatePropagation();
    const q=input.value.trim();input.value='';addMessage('user',q);
    const loaded=await loadSemanticCommands();
    if(!loaded){addMessage('bot','Semantic shortcuts are unavailable right now. No intent was inferred and no action was taken.');return true}
    const result=window.StegVerseSemanticCommands.resolve(q,'VA_CLAIMS_CHAT');
    addMessage('bot',window.StegVerseSemanticCommands.renderText(result));
    return true;
  }

  async function interceptGeneralQuestion(event){
    if(await interceptSemanticCommand(event))return;
    if(!generalMode||!ready)return;
    const input=document.getElementById('question');
    if(!input||!input.value.trim())return;
    event.preventDefault();event.stopImmediatePropagation();
    const q=input.value.trim();input.value='';addMessage('user',q);addMessage('bot','Checking current admitted VA resources…');
    const pending=document.querySelector('#log .bot:last-child');
    const result=await ask(q);
    if(pending)pending.remove();
    if(result.used){addMessage('bot',result.text);return}
    addMessage('bot','The coordinated VA resource service is unavailable right now. No private records were sent. Please use the guided steps or try again later.');
  }

  function bind(){
    const questions=document.getElementById('questions');
    const guided=document.getElementById('guided');
    const send=document.getElementById('send');
    const input=document.getElementById('question');
    if(questions)questions.addEventListener('click',()=>{generalMode=true},true);
    if(guided)guided.addEventListener('click',()=>{generalMode=false},true);
    if(send)send.addEventListener('click',interceptGeneralQuestion,true);
    if(input)input.addEventListener('keydown',e=>{if(e.key==='Enter')interceptGeneralQuestion(e)},true);
    updateCapabilityLabel();
    loadSemanticCommands();
  }

  window.VAClaimsRuntimeBridge={init,status,ask,validActiveProjection};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
  init();
})();
