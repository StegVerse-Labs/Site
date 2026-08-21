(()=>{
  const PROJECTION_URL='api/va-claim-assistant/runtime-projection.json';
  const BRIDGE_URL='stegos-bootstrap/ecosystem-chat-bridge.html';
  const VA_TERMS=[
    'va ','veteran','disability claim','service connection','c&p','compensation and pension',
    'gi bill','home loan','certificate of eligibility','community care','va health','va medical',
    'vr&e','vocational rehabilitation','va pharmacy','va copay','va billing','burial','memorial',
    'caregiver benefit','va appeal','supplemental claim','higher-level review','blue button'
  ];
  const ROUTES=[
    ['home_loan',['home loan','va loan','mortgage','certificate of eligibility','coe']],
    ['education',['gi bill','education benefit','school benefit','tuition','chapter 33','chapter 35']],
    ['community_care',['community care','outside va doctor','referral authorization','community provider']],
    ['pharmacy_billing',['pharmacy','prescription','copay','billing','medical bill']],
    ['health_care',['va health care','va healthcare','healthcare eligibility','enroll in va health','medical care']],
    ['vre',['vr&e','vre','vocational rehabilitation','chapter 31']],
    ['caregiver_family',['caregiver','dependent','spouse benefit','family benefit','survivor benefit']],
    ['burial_memorial',['burial','cemetery','memorial','headstone']],
    ['appeal',['appeal','supplemental claim','higher-level review','board appeal','denial']],
    ['claim',['disability claim','service connection','c&p','compensation and pension','evidence','rating','nexus']]
  ];
  const GROUNDED={
    home_loan:{url:'https://www.va.gov/housing-assistance/home-loans/',text:'A VA-backed home loan usually starts with confirming eligibility and getting a Certificate of Eligibility (COE). A lender still makes the loan and applies its credit and underwriting requirements.',follow:'Are you buying a home, refinancing one you already own, or just checking whether you qualify?'},
    education:{url:'https://www.va.gov/education/',text:'VA education benefits depend on the program and your eligibility history.',follow:'Are you choosing a benefit, applying for one, or fixing a problem with benefits you already have?'},
    community_care:{url:'https://www.va.gov/COMMUNITYCARE/',text:'VA Community Care generally requires VA authorization before covered community treatment. If VA says an authorization was sent but the provider cannot find it, that should be traced as an authorization-workflow problem.',follow:'Is that what is happening in your case?'},
    pharmacy_billing:{url:'https://www.va.gov/health-care/about-va-health-benefits/cost-of-care/',text:'VA pharmacy and billing problems take different paths depending on whether the issue is a prescription, a copay, insurance billing, or a charge connected to community care.',follow:'Which of those is the problem you are dealing with?'},
    health_care:{url:'https://www.va.gov/health-care/',text:'VA health care help depends on whether you are enrolling, getting care, checking eligibility, or resolving an access problem.',follow:'Which of those are you trying to do?'},
    vre:{url:'https://www.va.gov/careers-employment/vocational-rehabilitation/',text:'Veteran Readiness and Employment (VR&E) can provide employment, training, education, and independent-living support depending on eligibility and need.',follow:'Are you checking eligibility, applying, or dealing with a current VR&E case?'},
    caregiver_family:{url:'https://www.va.gov/family-member-benefits/',text:'VA caregiver and family benefits vary by program, including caregiver support, dependent and spouse benefits, and survivor benefits.',follow:'Which benefit are you trying to get help with?'},
    burial_memorial:{url:'https://www.va.gov/burials-memorials/',text:'VA burial and memorial benefits can include burial allowances, national cemetery eligibility, headstones or markers, and other memorial benefits.',follow:'Which service do you need help with?'},
    appeal:{url:'https://www.va.gov/decision-reviews/',text:'The right review path depends on the decision you received and what you are trying to change.',follow:'What decision are you challenging, and when was the decision dated?'},
    claim:{url:'https://www.va.gov/disability/how-to-file-claim/evidence-needed/',text:'For a disability claim, the useful next step depends on the condition, the type of service connection, the evidence already available, and where the claim is in the process.',follow:'What condition or claim issue are you working on right now?'}
  };

  let projection=null;
  let serverReady=false;
  let bridgeFrame=null;
  let bridgeReady=false;
  let bridgeWaiters=[];
  const pending=new Map();

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
    if(VA_TERMS.some(term=>text.includes(term)))return true;
    const history=readHistory();
    return history.length>0&&history[history.length-1].domain==='va';
  }
  function classify(message){
    const text=String(message||'').toLowerCase();
    for(const [route,terms] of ROUTES){if(terms.some(term=>text.includes(term)))return route}
    const history=readHistory();
    for(let i=history.length-1;i>=0;i--){if(history[i].route&&GROUNDED[history[i].route])return history[i].route}
    return 'claim';
  }
  function sessionId(){
    let value=sessionStorage.getItem('ecosystemVaSession');
    if(!value){value='va-web-'+(globalThis.crypto?.randomUUID?.()||Date.now().toString(36));sessionStorage.setItem('ecosystemVaSession',value)}
    return value;
  }
  function readHistory(){
    try{const value=JSON.parse(sessionStorage.getItem('ecosystemVaHistory')||'[]');return Array.isArray(value)?value.slice(-8):[]}catch{return []}
  }
  function remember(role,text,route){
    const history=readHistory();history.push({role,text:String(text).slice(0,1800),route,domain:'va'});sessionStorage.setItem('ecosystemVaHistory',JSON.stringify(history.slice(-8)));
  }
  function contextualMessage(message){
    const history=readHistory().slice(-2);
    if(!history.length)return message;
    const context=history.map(turn=>(turn.role==='user'?'Veteran':'Assistant')+': '+turn.text).join('\n');
    return message+'\n\nConversation context for continuity only:\n'+context;
  }
  function append(kind,text){
    const log=document.getElementById('chatLog');if(!log)return;
    const item=document.createElement('div');item.className='chat-message '+kind;
    const body=document.createElement('div');body.className='body';body.textContent=text;
    item.appendChild(body);log.appendChild(item);log.scrollTop=log.scrollHeight;
  }
  function groundedResponse(message){
    const route=classify(message),g=GROUNDED[route]||GROUNDED.claim;
    return {text:g.text+'\n\n'+g.follow,route,url:g.url};
  }
  function modelPrompt(message){
    const grounded=groundedResponse(message);const history=readHistory().slice(-4);
    return 'Answer the veteran in plain language using only this supplied official-VA-grounded context. Do not invent facts, diagnoses, ratings, deadlines, eligibility decisions, or filing confirmations. Ask one useful follow-up question when needed.\nGrounding: '+grounded.text+'\nOfficial source: '+grounded.url+'\nConversation: '+history.map(x=>x.role+': '+x.text).join(' | ')+'\nVeteran: '+message;
  }

  function setupBridge(){
    if(bridgeFrame)return;
    bridgeFrame=document.createElement('iframe');
    bridgeFrame.src=BRIDGE_URL;
    bridgeFrame.title='';
    bridgeFrame.setAttribute('aria-hidden','true');
    bridgeFrame.tabIndex=-1;
    bridgeFrame.style.cssText='position:absolute;width:1px;height:1px;opacity:0;pointer-events:none;border:0;left:-9999px;';
    document.body.appendChild(bridgeFrame);
  }
  function waitForBridge(timeoutMs=12000){
    if(bridgeReady)return Promise.resolve(true);
    setupBridge();
    return new Promise((resolve,reject)=>{
      const token={resolve,reject};bridgeWaiters.push(token);
      setTimeout(()=>{const index=bridgeWaiters.indexOf(token);if(index>=0)bridgeWaiters.splice(index,1);reject(new Error('device_local_runtime_timeout'))},timeoutMs);
    });
  }
  window.addEventListener('message',event=>{
    if(event.origin!==location.origin||!event.data||event.data.source!=='stegverse-device-local-bridge')return;
    const data=event.data;
    if(data.type==='READY'){
      bridgeReady=true;const waiters=bridgeWaiters.splice(0);waiters.forEach(w=>w.resolve(true));
      window.dispatchEvent(new CustomEvent('ecosystem-va-runtime-state',{detail:{serverReady,deviceReady:true}}));return;
    }
    if((data.type==='ANSWER'||data.type==='ERROR')&&data.id&&pending.has(data.id)){
      const item=pending.get(data.id);pending.delete(data.id);clearTimeout(item.timer);
      if(data.type==='ANSWER')item.resolve(data);else item.reject(new Error(data.reason||'device_local_runtime_failed'));
    }
  });

  async function init(){
    try{const r=await fetch(PROJECTION_URL,{cache:'no-store',credentials:'omit'});projection=r.ok?await r.json():null;serverReady=validProjection(projection)}
    catch{projection=null;serverReady=false}
    setupBridge();
    window.dispatchEvent(new CustomEvent('ecosystem-va-runtime-state',{detail:{serverReady,deviceReady:bridgeReady}}));
  }
  async function askServer(message){
    if(!serverReady||!projection)throw new Error('server_runtime_not_ready');
    const sid=sessionId(),id=globalThis.crypto?.randomUUID?.()||Date.now().toString(36);
    const payload={
      message:contextualMessage(message),session_id:sid,route_scope:'VA_CLAIMS_CHAT',requested_capability:'COORDINATED_VA_RESOURCES_LLM',
      source_policy:'ADMITTED_OFFICIAL_VA_ONLY',private_document_context:false,filing_requested:false,
      authority_required:true,receipt_required:true,
      transition_identity:{transition_id:'site-va-'+id,run_id:'site-va-run-'+id,event_id:'site-va-event-'+id,origin_manifest_id:'StegVerse-Labs/Site:ecosystem-chat.html'}
    };
    const response=await fetch(projection.endpoint,{method:'POST',mode:'cors',credentials:'omit',headers:{'Content-Type':'application/json','X-SteGVerse-Session':sid},body:JSON.stringify(payload)});
    const data=await response.json().catch(()=>null);
    if(!response.ok||!data||typeof(data.response||data.answer||data.text)!=='string')throw new Error('server_runtime_request_failed');
    if(data.authority_effect===true||data.activation_effect===true)throw new Error('authority_escalation_rejected');
    return {text:String(data.response||data.answer||data.text).trim(),route:data.route||classify(message),source:'server'};
  }
  async function askDevice(message){
    await waitForBridge();
    const id='device-va-'+(globalThis.crypto?.randomUUID?.()||Date.now().toString(36));
    const result=await new Promise((resolve,reject)=>{
      const timer=setTimeout(()=>{pending.delete(id);reject(new Error('device_local_request_timeout'))},20000);
      pending.set(id,{resolve,reject,timer});
      bridgeFrame.contentWindow.postMessage({source:'stegverse-ecosystem-chat',type:'ASK',id,prompt:modelPrompt(message)},location.origin);
    });
    if(result.same_execution!==true||result.reconstruction_state!=='PASS')throw new Error('device_local_reconstruction_missing');
    const grounded=groundedResponse(message);
    const text=(result.model&&result.model!=='stegverse-reference-lm-v1'&&String(result.text||'').trim().length>=24)?String(result.text).trim():grounded.text;
    return {text,route:grounded.route,source:'device-local',receipt:result.receipt_sha256};
  }
  async function ask(message){
    let result;
    if(serverReady){try{result=await askServer(message)}catch{result=null}}
    if(!result){result=await askDevice(message)}
    remember('user',message,result.route);remember('assistant',result.text,result.route);
    return result.text;
  }
  function bind(){
    const form=document.getElementById('chatForm'),input=document.getElementById('messageInput');
    if(!form||!input)return;
    form.addEventListener('submit',async event=>{
      const message=input.value.trim();if(!message||!isVA(message))return;
      event.preventDefault();event.stopImmediatePropagation();append('user',message);input.value='';
      const pendingNode=document.createElement('div');pendingNode.className='chat-message system';pendingNode.dataset.pending='va';
      const body=document.createElement('div');body.className='body';body.textContent='Checking the relevant VA information…';pendingNode.appendChild(body);document.getElementById('chatLog')?.appendChild(pendingNode);
      try{const answer=await ask(message);pendingNode.remove();append('system',answer)}
      catch{pendingNode.remove();const grounded=groundedResponse(message);remember('user',message,grounded.route);remember('assistant',grounded.text,grounded.route);append('system',grounded.text)}
    },true);
  }
  window.EcosystemVARuntime={init,ask,isVA,status:()=>({serverReady,deviceReady:bridgeReady,projection})};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
  init();
})();
