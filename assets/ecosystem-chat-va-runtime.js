(()=>{
  const PROJECTION_URL='api/va-claim-assistant/runtime-projection.json';
  const VA_TERMS=[
    'va ','veteran','disability claim','service connection','c&p','compensation and pension',
    'gi bill','home loan','certificate of eligibility','community care','va health','va medical',
    'vr&e','vocational rehabilitation','va pharmacy','va copay','va billing','burial','memorial',
    'caregiver benefit','va appeal','supplemental claim','higher-level review','blue button'
  ];
  let projection=null;
  let ready=false;

  function isSha256(v){return typeof v==='string'&&/^[a-f0-9]{64}$/i.test(v)}
  function isHttps(v){try{return new URL(v).protocol==='https:'}catch{return false}}
  function validProjection(p){
    return !!p&&p.schema==='stegverse.va_claims_chat.runtime_projection.v1'&&
      p.capability==='COORDINATED_VA_RESOURCES_LLM'&&p.state==='VERIFIED'&&p.active===true&&
      isHttps(p.endpoint)&&p.endpoint_method==='POST'&&
      isSha256(p.activation_receipt_sha256)&&isSha256(p.execution_receipt_sha256)&&
      p.custody_state==='RECORDED'&&p.reconstruction_state==='PASS'&&
      p.private_document_upload_active===false&&p.private_document_retrieval_active===false&&
      p.filing_active===false&&p.authority_effect===false&&p.activation_effect===false;
  }
  function isVA(message){
    const text=(' '+String(message||'').toLowerCase()+' ').replace(/\s+/g,' ');
    return VA_TERMS.some(term=>text.includes(term));
  }
  function sessionId(){
    let value=sessionStorage.getItem('ecosystemVaSession');
    if(!value){value='va-web-'+(globalThis.crypto?.randomUUID?.()||Date.now().toString(36));sessionStorage.setItem('ecosystemVaSession',value)}
    return value;
  }
  function append(kind,text){
    const log=document.getElementById('chatLog');if(!log)return;
    const item=document.createElement('div');item.className='chat-message '+kind;
    const body=document.createElement('div');body.className='body';body.textContent=text;
    item.appendChild(body);log.appendChild(item);log.scrollTop=log.scrollHeight;
  }
  async function init(){
    try{const r=await fetch(PROJECTION_URL,{cache:'no-store',credentials:'omit'});projection=r.ok?await r.json():null;ready=validProjection(projection)}
    catch{projection=null;ready=false}
    window.dispatchEvent(new CustomEvent('ecosystem-va-runtime-state',{detail:{ready}}));
  }
  async function ask(message){
    if(!ready||!projection)throw new Error('va_runtime_not_ready');
    const sid=sessionId();
    const id=globalThis.crypto?.randomUUID?.()||Date.now().toString(36);
    const payload={
      message,session_id:sid,route_scope:'VA_CLAIMS_CHAT',requested_capability:'COORDINATED_VA_RESOURCES_LLM',
      source_policy:'ADMITTED_OFFICIAL_VA_ONLY',private_document_context:false,filing_requested:false,
      authority_required:true,receipt_required:true,
      transition_identity:{transition_id:'site-va-'+id,run_id:'site-va-run-'+id,event_id:'site-va-event-'+id,origin_manifest_id:'StegVerse-Labs/Site:ecosystem-chat.html'}
    };
    const response=await fetch(projection.endpoint,{method:'POST',mode:'cors',credentials:'omit',headers:{'Content-Type':'application/json','X-SteGVerse-Session':sid},body:JSON.stringify(payload)});
    const data=await response.json().catch(()=>null);
    if(!response.ok||!data||typeof(data.response||data.answer||data.text)!=='string')throw new Error('va_runtime_request_failed');
    if(data.authority_effect===true||data.activation_effect===true)throw new Error('authority_escalation_rejected');
    return String(data.response||data.answer||data.text).trim();
  }
  function bind(){
    const form=document.getElementById('chatForm'),input=document.getElementById('messageInput');
    if(!form||!input)return;
    form.addEventListener('submit',async event=>{
      const message=input.value.trim();
      if(!message||!isVA(message))return;
      event.preventDefault();event.stopImmediatePropagation();
      append('user',message);input.value='';
      if(!ready){
        append('system','I can help with VA questions, but the live VA assistant is temporarily unavailable. Try again shortly.');
        return;
      }
      const pending=document.createElement('div');pending.className='chat-message system';pending.dataset.pending='va';
      const body=document.createElement('div');body.className='body';body.textContent='Checking the relevant VA information…';pending.appendChild(body);
      document.getElementById('chatLog')?.appendChild(pending);
      try{const answer=await ask(message);pending.remove();append('system',answer)}
      catch{pending.remove();append('system','I couldn’t reach the VA assistant just now. Please try again.')}
    },true);
  }
  window.EcosystemVARuntime={init,ask,isVA,status:()=>({ready,projection})};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
  init();
})();
