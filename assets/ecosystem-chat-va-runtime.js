(()=>{
  const PROJECTION_URL='api/va-claim-assistant/runtime-projection.json';
  const BRIDGE_URL='stegos-bootstrap/ecosystem-chat-bridge.html';
  const MATH_ACTIVATION_URL='data/math-solver-public-activation.latest.json';
  const VA_TERMS=[
    'va ','veteran','disability claim','service connection','c&p','compensation and pension',
    'gi bill','home loan','certificate of eligibility','community care','va health','va medical',
    'vr&e','vocational rehabilitation','va pharmacy','va copay','va billing','burial','memorial',
    'caregiver benefit','va appeal','supplemental claim','higher-level review','blue button'
  ];
  const MATH_TERMS=[
    'math','mathematics','arithmetic','algebra','equation','solve for','factor','polynomial','fraction','percent',
    'geometry','triangle','circle','trigonometry','sine','cosine','tangent','precalculus','calculus','derivative',
    'integral','limit','differential equation','linear algebra','matrix','vector','eigenvalue','discrete math',
    'probability','statistics','number theory','abstract algebra','real analysis','complex analysis','topology',
    'differential geometry','numerical analysis','optimization','set theory','category theory','mathematical physics',
    'theorem','proof','logarithm','exponent','sequence','series','combinatorics'
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
    const history=readVAHistory();
    return history.length>0&&history[history.length-1].domain==='va';
  }
  function isMath(message){
    const text=(' '+String(message||'').toLowerCase()+' ').replace(/\s+/g,' ');
    if(MATH_TERMS.some(term=>text.includes(term)))return true;
    if(/(?:^|\s)(?:\d+(?:\.\d+)?|[a-z])\s*(?:\+|\-|\*|\/|\^|=)\s*(?:\d+(?:\.\d+)?|[a-z])(?:\s|$)/i.test(text))return true;
    const history=readMathHistory();
    return history.length>0&&history[history.length-1].domain==='math';
  }
  function classify(message){
    const text=String(message||'').toLowerCase();
    for(const [route,terms] of ROUTES){if(terms.some(term=>text.includes(term)))return route}
    const history=readVAHistory();
    for(let i=history.length-1;i>=0;i--){if(history[i].route&&GROUNDED[history[i].route])return history[i].route}
    return 'claim';
  }
  function sessionId(){
    let value=sessionStorage.getItem('ecosystemVaSession');
    if(!value){value='va-web-'+(globalThis.crypto?.randomUUID?.()||Date.now().toString(36));sessionStorage.setItem('ecosystemVaSession',value)}
    return value;
  }
  function readHistory(key){
    try{const value=JSON.parse(sessionStorage.getItem(key)||'[]');return Array.isArray(value)?value.slice(-8):[]}catch{return []}
  }
  function readVAHistory(){return readHistory('ecosystemVaHistory')}
  function readGeneralHistory(){return readHistory('ecosystemGeneralHistory')}
  function readMathHistory(){return readHistory('ecosystemMathHistory')}
  function remember(key,role,text,route,domain){
    const history=readHistory(key);history.push({role,text:String(text).slice(0,1800),route:route||null,domain});sessionStorage.setItem(key,JSON.stringify(history.slice(-8)));
  }
  function contextualMessage(message){
    const history=readVAHistory().slice(-2);
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
    const grounded=groundedResponse(message);const history=readVAHistory().slice(-4);
    return 'Answer the veteran in plain language using only this supplied official-VA-grounded context. Do not invent facts, diagnoses, ratings, deadlines, eligibility decisions, or filing confirmations. Ask one useful follow-up question when needed.\nGrounding: '+grounded.text+'\nOfficial source: '+grounded.url+'\nConversation: '+history.map(x=>x.role+': '+x.text).join(' | ')+'\nVeteran: '+message;
  }
  function generalPrompt(message){
    const history=readGeneralHistory().slice(-6);
    return 'Have a direct, useful conversation with the user. Preserve continuity with the recent conversation when relevant. Do not claim that model output grants execution authority. If the local reference model cannot answer a factual question reliably, say so rather than inventing facts.\nRecent conversation: '+history.map(x=>x.role+': '+x.text).join(' | ')+'\nUser: '+message;
  }
  function mathPrompt(message){
    const history=readMathHistory().slice(-6);
    return [
      'Use the mathematics-educator specialty of the shared Ecosystem Chat conversation.',
      'Default to teaching rather than only giving an answer. Identify the kind of mathematics when useful; explain prerequisites; offer a hint or guided solution; check the user\'s work by finding the first incorrect transition; show alternate methods when useful; and explain why a method works.',
      'History, foundations, and philosophy of mathematics are in scope when relevant.',
      'The governed_math_solver and math_verifier are CANDIDATE_ONLY_NOT_EXECUTED. Do not claim a tool ran unless separate governed execution evidence is supplied. A successful calculation is not mathematical proof authority.',
      'If the user refers to an image or transcription that is not actually present in this request, do not invent its contents. source_image and interpreted_mathematical_transcription are distinct states and ambiguity must remain visible.',
      'Preserve recent Math conversation continuity when relevant.',
      'Recent Math conversation: '+history.map(x=>x.role+': '+x.text).join(' | '),
      'User: '+message
    ].join('\n');
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
      window.dispatchEvent(new CustomEvent('ecosystem-runtime-state',{detail:{serverReady,deviceReady:true}}));
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
    const detail={serverReady,deviceReady:bridgeReady};
    window.dispatchEvent(new CustomEvent('ecosystem-runtime-state',{detail}));
    window.dispatchEvent(new CustomEvent('ecosystem-va-runtime-state',{detail}));
  }
  async function executeDeviceRaw(prompt,prefix='device-chat'){
    await waitForBridge();
    const id=prefix+'-'+(globalThis.crypto?.randomUUID?.()||Date.now().toString(36));
    const result=await new Promise((resolve,reject)=>{
      const timer=setTimeout(()=>{pending.delete(id);reject(new Error('device_local_request_timeout'))},20000);
      pending.set(id,{resolve,reject,timer});
      bridgeFrame.contentWindow.postMessage({source:'stegverse-ecosystem-chat',type:'ASK',id,prompt},location.origin);
    });
    if(result.same_execution!==true||result.reconstruction_state!=='PASS')throw new Error('device_local_reconstruction_missing');
    if(typeof result.text!=='string')throw new Error('device_local_response_missing');
    return result;
  }
  async function askServer(message){
    if(!serverReady||!projection)throw new Error('server_runtime_not_ready');
    const sid=sessionId(),id=globalThis.crypto?.randomUUID?.()||Date.now().toString(36);
    const payload={message:contextualMessage(message),session_id:sid,route_scope:'VA_CLAIMS_CHAT',requested_capability:'COORDINATED_VA_RESOURCES_LLM',source_policy:'ADMITTED_OFFICIAL_VA_ONLY',private_document_context:false,filing_requested:false,authority_required:true,receipt_required:true,transition_identity:{transition_id:'site-va-'+id,run_id:'site-va-run-'+id,event_id:'site-va-event-'+id,origin_manifest_id:'StegVerse-Labs/Site:ecosystem-chat.html'}};
    const response=await fetch(projection.endpoint,{method:'POST',mode:'cors',credentials:'omit',headers:{'Content-Type':'application/json','X-SteGVerse-Session':sid},body:JSON.stringify(payload)});
    const data=await response.json().catch(()=>null);
    if(!response.ok||!data||typeof(data.response||data.answer||data.text)!=='string')throw new Error('server_runtime_request_failed');
    if(data.authority_effect===true||data.activation_effect===true)throw new Error('authority_escalation_rejected');
    return {text:String(data.response||data.answer||data.text).trim(),route:data.route||classify(message),source:'server'};
  }
  async function askDevice(message){
    const result=await executeDeviceRaw(modelPrompt(message),'device-va');
    const grounded=groundedResponse(message);
    const text=(result.model&&result.model!=='stegverse-reference-lm-v1'&&String(result.text||'').trim().length>=24)?String(result.text).trim():grounded.text+'\n\n'+(GROUNDED[grounded.route]?.follow||'');
    return {text,route:grounded.route,source:'device-local',receipt:result.receipt_sha256};
  }
  async function ask(message){
    let result;
    if(serverReady){try{result=await askServer(message)}catch{result=null}}
    if(!result){result=await askDevice(message)}
    remember('ecosystemVaHistory','user',message,result.route,'va');remember('ecosystemVaHistory','assistant',result.text,result.route,'va');
    return result.text;
  }
  async function sha256Hex(value){
    const bytes=new TextEncoder().encode(value);
    const digest=await crypto.subtle.digest('SHA-256',bytes);
    return Array.from(new Uint8Array(digest),byte=>byte.toString(16).padStart(2,'0')).join('');
  }
  function formatDeviceClock(epochMs,locale,timeZone){
    return new Intl.DateTimeFormat(locale,{
      hour:'numeric',minute:'2-digit',second:'2-digit',timeZoneName:'short',timeZone
    }).format(new Date(epochMs));
  }
  function readDeterministicReceipt(){
    try{return JSON.parse(sessionStorage.getItem('ecosystemLatestDeterministicReceipt')||'null')}catch{return null}
  }
  async function deterministicGeneralCapability(message){
    const text=String(message||'').trim();
    if(!(/^(?:what(?:'s| is)?\s+)?(?:the\s+)?(?:current\s+)?time(?:\s+is\s+it)?[?.!\s]*$/i.test(text)||/^(?:can you\s+)?tell me (?:the\s+)?time[?.!\s]*$/i.test(text)))return null;
    const now=new Date();
    const resolved=new Intl.DateTimeFormat().resolvedOptions();
    const locale=resolved.locale||'en-US';
    const timeZone=resolved.timeZone||'UTC';
    const formatted=formatDeviceClock(now.getTime(),locale,timeZone);
    const output='It is '+formatted+' on this device.';
    const reconstructedOutput='It is '+formatDeviceClock(now.getTime(),locale,timeZone)+' on this device.';
    const sameExecution=output===reconstructedOutput;
    const receiptPayload={
      schema:'stegverse.device-local-deterministic-execution.v1',
      capability:'device_clock',
      input:text,
      output,
      observed_at:now.toISOString(),
      epoch_ms:now.getTime(),
      locale,
      time_zone:timeZone,
      execution_surface:'site-shared-conversational-client',
      deterministic_execution:true,
      model_execution:false,
      reconstructed_output:reconstructedOutput,
      same_execution:sameExecution,
      reconstruction_state:sameExecution?'PASS':'FAIL',
      authority_effect:false,
      activation_effect:false
    };
    const receiptSha256=await sha256Hex(JSON.stringify(receiptPayload));
    const evidence={...receiptPayload,receipt_sha256:receiptSha256};
    sessionStorage.setItem('ecosystemLatestDeterministicReceipt',JSON.stringify(evidence));
    if(!sameExecution)throw new Error('deterministic_clock_reconstruction_failed');
    return {
      text:output,
      source:'device-local-deterministic',
      capability:'device_clock',
      deterministic_execution:true,
      model_execution:false,
      same_execution:true,
      reconstruction_state:'PASS',
      receipt:receiptSha256,
      evidence,
      authority_effect:'NONE'
    };
  }
  function isLiveWeatherRequest(message){
    const text=String(message||'').trim();
    const weatherSubject=/\b(weather|forecast|temperature|rain|snow|storm|humidity|wind)\b/i.test(text);
    const liveWindow=/\b(today|tonight|tomorrow|current|currently|now|this week|weekend|going to|will it)\b/i.test(text);
    return weatherSubject&&liveWindow;
  }
  function dynamicDataCapabilityGap(message,reason='unavailable'){
    if(!isLiveWeatherRequest(message))return null;
    const text=reason==='permission'
      ? "I need location permission to look up the local forecast. I won't use or persist your exact coordinates if you don't allow it."
      : "I couldn't reach the admitted live weather source just now, so I can't reliably give you the forecast. I won't guess.";
    return {
      text,
      source:'capability-gap',
      capability:'live_weather',
      gap_reason:reason,
      model_execution:false,
      deterministic_execution:false,
      same_execution:false,
      reconstruction_state:'NOT_APPLICABLE',
      authority_effect:'NONE'
    };
  }
  function requestWeatherPosition(){
    if(!navigator.geolocation)return Promise.reject(new Error('weather_geolocation_unavailable'));
    return new Promise((resolve,reject)=>{
      navigator.geolocation.getCurrentPosition(
        position=>resolve(position),
        error=>reject(new Error(error?.code===1?'weather_location_permission_denied':'weather_geolocation_failed')),
        {enableHighAccuracy:false,timeout:10000,maximumAge:300000}
      );
    });
  }
  function selectForecastPeriods(message,periods){
    if(!Array.isArray(periods)||!periods.length)return [];
    const text=String(message||'').toLowerCase();
    if(text.includes('tomorrow')){
      const now=new Date();
      const tomorrow=new Date(now.getFullYear(),now.getMonth(),now.getDate()+1);
      const key=[tomorrow.getFullYear(),tomorrow.getMonth(),tomorrow.getDate()].join('-');
      const matches=periods.filter(period=>{
        const start=new Date(period.startTime);
        return [start.getFullYear(),start.getMonth(),start.getDate()].join('-')===key;
      });
      return matches.slice(0,2);
    }
    if(text.includes('tonight')){
      const night=periods.find(period=>period.isDaytime===false);
      return night?[night]:periods.slice(0,1);
    }
    return periods.slice(0,2);
  }
  function formatForecastPeriod(period){
    const temp=Number.isFinite(Number(period.temperature))?Number(period.temperature):null;
    const unit=period.temperatureUnit||'F';
    const parts=[String(period.name||'Forecast')+': '+String(period.shortForecast||period.detailedForecast||'forecast available')];
    if(temp!==null)parts.push('around '+temp+'°'+unit);
    if(period.windSpeed)parts.push('wind '+String(period.windSpeed)+(period.windDirection?' '+String(period.windDirection):''));
    return parts.join(', ')+'.';
  }
  async function liveWeatherCapability(message){
    if(!isLiveWeatherRequest(message))return null;
    let position;
    try{position=await requestWeatherPosition()}
    catch(error){
      const reason=String(error?.message||'').includes('permission')?'permission':'unavailable';
      return dynamicDataCapabilityGap(message,reason);
    }
    const latitude=Number(position.coords.latitude);
    const longitude=Number(position.coords.longitude);
    if(!Number.isFinite(latitude)||!Number.isFinite(longitude))return dynamicDataCapabilityGap(message,'unavailable');
    const pointUrl='https://api.weather.gov/points/'+latitude.toFixed(4)+','+longitude.toFixed(4);
    try{
      const pointResponse=await fetch(pointUrl,{cache:'no-store',credentials:'omit',headers:{Accept:'application/geo+json'}});
      const point=await pointResponse.json().catch(()=>null);
      const forecastUrl=point?.properties?.forecast;
      if(!pointResponse.ok||typeof forecastUrl!=='string'||!forecastUrl.startsWith('https://api.weather.gov/'))throw new Error('weather_point_lookup_failed');
      const forecastResponse=await fetch(forecastUrl,{cache:'no-store',credentials:'omit',headers:{Accept:'application/geo+json'}});
      const forecast=await forecastResponse.json().catch(()=>null);
      if(!forecastResponse.ok||!forecast?.properties||!Array.isArray(forecast.properties.periods))throw new Error('weather_forecast_lookup_failed');
      const periods=selectForecastPeriods(message,forecast.properties.periods);
      if(!periods.length)throw new Error('weather_period_not_found');
      const relative=point.properties?.relativeLocation?.properties||{};
      const place=[relative.city,relative.state].filter(Boolean).join(', ');
      const output=(place?'For '+place+', ':'')+periods.map(formatForecastPeriod).join(' ');
      const evidencePayload={
        schema:'stegverse.live-weather-evidence.v1',
        capability:'live_weather',
        request:String(message||'').trim(),
        source:'api.weather.gov',
        source_role:'DATA_ONLY_NO_EXECUTION_AUTHORITY',
        forecast_url:forecastUrl,
        location_label:place||null,
        exact_coordinates_persisted:false,
        observed_at:new Date().toISOString(),
        authority_effect:false,
        activation_effect:false
      };
      const receiptSha256=await sha256Hex(JSON.stringify(evidencePayload));
      const evidence={...evidencePayload,receipt_sha256:receiptSha256};
      sessionStorage.setItem('ecosystemLatestWeatherReceipt',JSON.stringify(evidence));
      return {
        text:output,
        source:'admitted-live-weather-data',
        capability:'live_weather',
        source_provider:'National Weather Service',
        model_execution:false,
        deterministic_execution:false,
        same_execution:true,
        reconstruction_state:'PASS',
        receipt:receiptSha256,
        evidence,
        authority_effect:'NONE'
      };
    }catch{
      return dynamicDataCapabilityGap(message,'unavailable');
    }
  }
  async function askGeneral(message){
    const deterministic=await deterministicGeneralCapability(message);
    if(deterministic){
      remember('ecosystemGeneralHistory','user',message,null,'general');remember('ecosystemGeneralHistory','assistant',deterministic.text,null,'general');
      return deterministic;
    }
    const weather=await liveWeatherCapability(message);
    if(weather){
      remember('ecosystemGeneralHistory','user',message,null,'general');remember('ecosystemGeneralHistory','assistant',weather.text,null,'general');
      return weather;
    }
    const result=await executeDeviceRaw(generalPrompt(message),'device-general');
    const text=String(result.text||'').trim();
    if(!text)throw new Error('device_local_response_empty');
    remember('ecosystemGeneralHistory','user',message,null,'general');remember('ecosystemGeneralHistory','assistant',text,null,'general');
    return {text,source:'device-local',same_execution:true,reconstruction_state:'PASS',receipt:result.receipt_sha256||null};
  }
  function governedArithmeticCandidate(message){
    const raw=String(message||'').trim();
    const stripped=raw
      .replace(/^(?:please\s+)?(?:calculate|compute|evaluate|solve)\s+/i,'')
      .replace(/^(?:what(?:'s| is)\s+)/i,'')
      .replace(/[?!.]+$/,'')
      .trim();
    if(!stripped||stripped.length>256)return null;
    if(!/^[0-9eE+\-*/%().\s]+$/.test(stripped))return null;
    if(!/[+\-*/%]/.test(stripped))return null;
    return stripped;
  }
  async function loadVerifiedMathRuntime(){
    const response=await fetch(MATH_ACTIVATION_URL,{cache:'no-store',credentials:'omit'});
    if(!response.ok)throw new Error('math_activation_receipt_unavailable');
    const activation=await response.json();
    if(activation.schema_version!=='stegverse.site.math_solver_activation.v1'||activation.state!=='COMPLETE')throw new Error('math_runtime_not_activated');
    if(activation.authority_effect!==false)throw new Error('math_activation_authority_escalation');
    if(typeof activation.runtime_origin!=='string'||!activation.runtime_origin)throw new Error('math_runtime_origin_missing');
    const origin=new URL(activation.runtime_origin,location.href);
    if(origin.protocol!=='https:'&&origin.hostname!=='127.0.0.1'&&origin.hostname!=='localhost')throw new Error('math_runtime_origin_not_admitted');
    return {activation,origin:origin.origin};
  }
  async function executeGovernedMathCandidate(expression){
    const {activation,origin}=await loadVerifiedMathRuntime();
    const readinessResponse=await fetch(origin+'/api/math-solver/v1/readiness',{cache:'no-store',credentials:'omit'});
    const readiness=await readinessResponse.json().catch(()=>null);
    if(!readinessResponse.ok||!readiness||readiness.state!=='READY'||readiness.canonical_steggate_bound!==true)throw new Error('math_runtime_readiness_failed');
    const identity=readiness.steggate_runtime_identity||{};
    if(identity.runtime_identity!=='stegverse:steggate:canonical:three-layer:v1'||identity.canonical_owner!=='StegVerse-Labs/StegCore'||identity.transport_identity_authoritative!==false)throw new Error('math_steggate_identity_mismatch');
    const requestId='MATH-CHAT-'+(globalThis.crypto?.randomUUID?.()||Date.now().toString(36));
    const response=await fetch(origin+'/api/math-solver/v1/solve',{
      method:'POST',mode:'cors',credentials:'omit',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({expression,request_id:requestId})
    });
    const payload=await response.json().catch(()=>null);
    if(!response.ok||!payload)throw new Error('math_governed_execution_failed');
    if(payload.disposition!=='ALLOW'||payload.execution_state!=='EXECUTED'||payload.executor_invoked!==true)throw new Error('math_execution_not_admitted');
    if(!payload.request_hash||!payload.result_hash||!payload.decision_state_hash||!payload.response_hash)throw new Error('math_execution_evidence_incomplete');
    if((payload.steggate_runtime_identity||{}).runtime_identity!=='stegverse:steggate:canonical:three-layer:v1')throw new Error('math_response_runtime_identity_mismatch');
    return {
      text:'The governed solver returns '+String(payload.result)+'.',
      source:'governed-math-solver',
      specialty:'mathematics-educator',
      same_execution:true,
      reconstruction_state:'PASS',
      receipt:payload.response_hash,
      model_execution:false,
      deterministic_execution:true,
      governed_tool_execution:true,
      tool:'governed_math_solver',
      request_hash:payload.request_hash,
      result_hash:payload.result_hash,
      decision_state_hash:payload.decision_state_hash,
      steggate_package_hash:payload.steggate_package_hash||null,
      runtime_origin:activation.runtime_origin,
      authority_effect:'NONE'
    };
  }
  async function sha256File(file){
    const digest=await crypto.subtle.digest('SHA-256',await file.arrayBuffer());
    return Array.from(new Uint8Array(digest),byte=>byte.toString(16).padStart(2,'0')).join('');
  }
  async function reviewMathImage(file){
    if(!(file instanceof File)||!file.size)throw new Error('math_image_file_required');
    if(file.size>25*1024*1024)throw new Error('math_image_size_invalid');
    const {activation,origin}=await loadVerifiedMathRuntime();
    const readinessResponse=await fetch(origin+'/api/attachments/v1/readiness',{cache:'no-store',credentials:'omit'});
    const readiness=await readinessResponse.json().catch(()=>null);
    if(!readinessResponse.ok||!readiness||readiness.state!=='READY')throw new Error('math_attachment_runtime_not_ready');
    if(readiness.credential_authority!=='TV/TVC'||readiness.github_token_runtime_authority!=='NONE'||readiness.authority_granted!==false)throw new Error('math_attachment_authority_mismatch');
    const profile=readiness.profiles?.['math-image-v1'];
    if(!profile||profile.exact_bytes_preserved!==true||profile.review_endpoint!=='/api/math-solver/v1/image-review')throw new Error('math_attachment_profile_mismatch');
    const declaredHash=await sha256File(file);
    const attachmentId='MATH-IMG-'+(globalThis.crypto?.randomUUID?.()||Date.now().toString(36));
    const form=new FormData();
    form.append('artifact',file,file.name||'math-image');
    form.append('profile','math-image-v1');
    form.append('attachment_id',attachmentId);
    form.append('declared_sha256',declaredHash);
    const intakeResponse=await fetch(origin+'/api/attachments/v1/intake',{method:'POST',mode:'cors',credentials:'omit',body:form});
    const intake=await intakeResponse.json().catch(()=>null);
    if(!intakeResponse.ok||!intake||intake.schema!=='stegverse.attachment-receipt.v1'||intake.state!=='ACCEPTED')throw new Error('math_attachment_intake_failed');
    if(intake.attachment_id!==attachmentId||intake.content_hash!=='sha256:'+declaredHash||intake.artifact_state!=='EXACT_BYTES_PRESERVED')throw new Error('math_attachment_receipt_mismatch');
    if(intake.credential_authority!=='TV/TVC'||intake.github_token_runtime_authority!=='NONE')throw new Error('math_attachment_credential_boundary_mismatch');
    const authority=intake.authority||{};
    if(authority.execution!==false||authority.provider!==false||authority.publication!==false||authority.custody!==false)throw new Error('math_attachment_authority_escalation');
    const reviewResponse=await fetch(origin+'/api/math-solver/v1/image-review',{
      method:'POST',mode:'cors',credentials:'omit',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({attachment_id:attachmentId})
    });
    const review=await reviewResponse.json().catch(()=>null);
    if(!reviewResponse.ok||!review||review.schema!=='stegverse.math-image-review.v1')throw new Error('math_image_review_failed');
    if(review.attachment_id!==attachmentId||review.source_image?.content_hash!==intake.content_hash||review.source_image?.exact_uploaded_bytes_preserved!==true)throw new Error('math_image_review_source_mismatch');
    const transcription=review.interpreted_mathematical_transcription||{};
    if(transcription.state!=='NOT_PRODUCED'||transcription.content!==null||transcription.is_source_fact!==false||transcription.source_image_remains_immutable!==true)throw new Error('math_image_transcription_boundary_violated');
    const reviewAuthority=review.authority||{};
    if(reviewAuthority.execution!==false||reviewAuthority.provider!==false||reviewAuthority.publication!==false||reviewAuthority.custody!==false||reviewAuthority.mathematical_truth!==false)throw new Error('math_image_review_authority_escalation');
    const flags=Array.isArray(review.quality_review?.flags)?review.quality_review.flags:[];
    const text=flags.length
      ? 'I accepted the image and preserved its exact bytes. The image-quality review flagged: '+flags.join(', ')+'. I have not treated any equation transcription as a source fact.'
      : 'I accepted the image and preserved its exact bytes. The image-quality review passed. I have not treated any equation transcription as a source fact.';
    return {
      text,
      source:'governed-math-image-review',
      specialty:'mathematics-educator',
      attachment_id:attachmentId,
      attachment_hash:intake.content_hash,
      attachment_receipt:intake.receipt_sha256||null,
      review_receipt:review.review_sha256||null,
      review_state:review.quality_review?.state||null,
      review_flags:flags,
      transcription_state:'NOT_PRODUCED',
      exact_uploaded_bytes_preserved:true,
      governed_tool_execution:false,
      model_execution:false,
      deterministic_execution:true,
      runtime_origin:activation.runtime_origin,
      authority_effect:'NONE',
      receipt:review.review_sha256||intake.receipt_sha256||null,
      reconstruction_state:'PASS'
    };
  }
  async function askMath(message){
    const candidate=governedArithmeticCandidate(message);
    if(candidate){
      try{
        const governed=await executeGovernedMathCandidate(candidate);
        remember('ecosystemMathHistory','user',message,'mathematics-educator','math');
        remember('ecosystemMathHistory','assistant',governed.text,'mathematics-educator','math');
        return governed;
      }catch(_governedError){
        // Fail closed on tool execution, then continue through the existing conversational educator path.
      }
    }
    const result=await executeDeviceRaw(mathPrompt(message),'device-math');
    const text=String(result.text||'').trim();
    if(!text)throw new Error('device_local_math_response_empty');
    remember('ecosystemMathHistory','user',message,'mathematics-educator','math');
    remember('ecosystemMathHistory','assistant',text,'mathematics-educator','math');
    return {
      text,
      source:'device-local',
      specialty:'mathematics-educator',
      same_execution:true,
      reconstruction_state:'PASS',
      receipt:result.receipt_sha256||null,
      candidate_tools:[
        {name:'governed_math_solver',execution_state:'CANDIDATE_ONLY_NOT_EXECUTED',execution_authority:false},
        {name:'math_verifier',execution_state:'CANDIDATE_ONLY_NOT_EXECUTED',execution_authority:false}
      ]
    };
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
      catch{pendingNode.remove();const grounded=groundedResponse(message);remember('ecosystemVaHistory','user',message,grounded.route,'va');remember('ecosystemVaHistory','assistant',grounded.text,grounded.route,'va');append('system',grounded.text)}
    },true);
  }
  const api={init,ask,askGeneral,askMath,reviewMathImage,isVA,isMath,status:()=>({serverReady,deviceReady:bridgeReady,projection,deterministicReceipt:readDeterministicReceipt(),weatherReceipt:(()=>{try{return JSON.parse(sessionStorage.getItem('ecosystemLatestWeatherReceipt')||'null')}catch{return null}})()})};
  window.EcosystemRuntime=api;
  window.EcosystemVARuntime=api;
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
  init();
})();