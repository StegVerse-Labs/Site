(() => {
  'use strict';

  const tracks = [
    {id:'stegdj-night-drive',title:'Night Drive Boundary',genre:'dark electronic / steady drive',bpm:96,root:45,pattern:[0,3,7,10,7,3,5,8],brightness:34,energy:58,bass:78,license:'StegDJ generated · local prototype'},
    {id:'stegdj-low-orbit',title:'Low Orbit Relay',genre:'ambient bass / restrained motion',bpm:78,root:40,pattern:[0,7,5,10,3,8,7,5],brightness:24,energy:42,bass:84,license:'StegDJ generated · local prototype'},
    {id:'stegdj-signal-rise',title:'Signal Rise',genre:'progressive synth / alertness lift',bpm:112,root:48,pattern:[0,5,7,12,10,7,5,3],brightness:52,energy:72,bass:66,license:'StegDJ generated · local prototype'}
  ];
  const phases = [
    {name:'INTRO',start:0,end:15,density:.55,transpose:-5},
    {name:'BUILD',start:16,end:31,density:.78,transpose:0},
    {name:'LIFT',start:32,end:47,density:1,transpose:7},
    {name:'RESOLVE',start:48,end:63,density:.68,transpose:0}
  ];
  const safeParse = (key,fallback) => { try { return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback)); } catch (_) { return fallback; } };
  const state = {
    trackIndex:0,playing:false,context:null,master:null,timer:null,step:0,selectedEventId:null,
    events:safeParse('stegmusic.events.v1',[]),value:Number(localStorage.getItem('stegmusic.value.v1')||0),
    profile:safeParse('stegmusic.profile.v1',{name:'Default listener'}),
    permissions:safeParse('stegmusic.permissions.v1',{stegdj:true,aggregate:false,wellness:false,revoked:false})
  };
  const $ = id => document.getElementById(id);
  const uid = prefix => `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,8)}`;
  const now = () => new Date().toISOString();
  const clamp = (n,min,max) => Math.max(min,Math.min(max,n));
  const escapeHtml = value => String(value).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  const currentTrack = () => tracks[state.trackIndex];
  const currentPhase = () => phases.find(p => state.step >= p.start && state.step <= p.end) || phases[0];

  function setStatus(id,text,mode='active') {
    const el=$(id); if(!el) return; el.textContent=text; el.classList.remove('pending','active','failed'); el.classList.add(mode);
  }
  function setAudioNotice(text,failed=false){ $('audioNotice').textContent=text; setStatus('statusAudio',failed?'AUDIO ENGINE · BLOCKED':'AUDIO ENGINE · ACTIVE',failed?'failed':'active'); }
  function permissionSnapshot(){
    const permitted=['private_stegmusic_profile'],downstream=[];
    if(!state.permissions.revoked&&state.permissions.stegdj){permitted.push('selected_refinement_to_stegdj');downstream.push('StegDJ');}
    if(!state.permissions.revoked&&state.permissions.aggregate){permitted.push('aggregate_music_rule_with_separate_authorization');downstream.push('AggregateMusicRules');}
    if(!state.permissions.revoked&&state.permissions.wellness){permitted.push('bounded_alertness_preference');downstream.push('Wellness');}
    return {permitted,downstream};
  }
  function persist(){
    localStorage.setItem('stegmusic.events.v1',JSON.stringify(state.events));
    localStorage.setItem('stegmusic.value.v1',String(state.value));
    localStorage.setItem('stegmusic.profile.v1',JSON.stringify(state.profile));
    localStorage.setItem('stegmusic.permissions.v1',JSON.stringify(state.permissions));
  }
  function makeEvent(type,human,governed={}){
    const permissions=permissionSnapshot();
    const event=Object.freeze({
      event_id:uid('music'),parent_event_id:state.events.length?state.events[state.events.length-1].event_id:null,timestamp:now(),
      actor:{type:'human_or_service',id:type.startsWith('stegdj')?'StegDJ':'local-user',profile:state.profile.name},service:'StegMusic/StegDJ',medium:'audio',event_type:type,
      human_projection:{text:human},governed_projection:{
        rights_status:governed.rights_status||'stegdj_generated_local_prototype',source_class:governed.source_class||'generated',
        captured_records:governed.captured_records||[],derived_records:governed.derived_records||[],
        permitted_reuse:governed.permitted_reuse||permissions.permitted,prohibited_reuse:governed.prohibited_reuse||['external_training','public_disclosure','cross_user_raw_history'],
        downstream_services:governed.downstream_services||permissions.downstream,contribution_eligibility:governed.contribution_eligibility||'not_evaluated',
        royalty_state:governed.royalty_state||'not_realized',reuse_revoked:state.permissions.revoked,authority:'none',fixture:true
      },policy_refs:['stegmusic-rights-boundary-v0','governed-service-envelope-v0','cross-service-projection-v0'],evidence_refs:[],artifact_refs:governed.artifact_refs||[],continuity_refs:state.events.length?[state.events[state.events.length-1].event_id]:[],hash:'preview-only'
    });
    state.events.push(event);state.selectedEventId=event.event_id;persist();renderEvents();inspectEvent(event.event_id);return event;
  }
  function renderCatalog(filter=''){
    const q=filter.trim().toLowerCase();
    const list=tracks.filter(t=>!q||`${t.title} ${t.genre} ${t.license}`.toLowerCase().includes(q));
    $('catalog').innerHTML=list.map(t=>{const i=tracks.findIndex(x=>x.id===t.id);return `<article class="track ${i===state.trackIndex?'active':''}" data-track="${i}"><div><strong>${escapeHtml(t.title)}</strong><span>${escapeHtml(t.genre)} · ${t.bpm} BPM</span><span class="license">${escapeHtml(t.license)}</span></div><button class="sv-btn sv-btn-secondary" type="button">Select</button></article>`;}).join('')||'<p class="muted">No local prototype tracks match this search.</p>';
    document.querySelectorAll('[data-track]').forEach(el=>el.addEventListener('click',()=>selectTrack(Number(el.dataset.track))));
  }
  function selectTrack(index){
    const wasPlaying=state.playing;stopAudio(false);state.trackIndex=clamp(index,0,tracks.length-1);state.step=0;
    const t=currentTrack();$('trackTitle').textContent=t.title;$('trackInfo').textContent=`${t.genre} · ${t.bpm} BPM · source=StegDJ generated · four-phase composition`;
    $('rightsBadge').textContent='STEGDJ GENERATED · LOCAL PROTOTYPE · RIGHTS RECORD VISIBLE';
    $('energy').value=t.energy;$('brightness').value=t.brightness;$('bass').value=t.bass;$('progress').value=0;$('compositionPhase').textContent='COMPOSITION · INTRO';renderCatalog($('musicSearch').value);
    makeEvent('music_selection',`Selected “${t.title}”.`,{captured_records:[{track_id:t.id,title:t.title,genre:t.genre,bpm:t.bpm,source:'browser_generated'}],derived_records:[{selection_reason:'explicit_user_selection',composition_form:'intro_build_lift_resolve'}],artifact_refs:[t.id]});
    setStatus('statusProjection','PROJECTION · ACTIVE');if(wasPlaying) startAudio();
  }
  async function ensureAudio(){
    const AudioCtor=window.AudioContext||window.webkitAudioContext;
    if(!AudioCtor) throw new Error('Web Audio is not supported by this browser.');
    if(!state.context){state.context=new AudioCtor();state.master=state.context.createGain();state.master.connect(state.context.destination);}
    state.master.gain.value=Number($('volume').value)/100*.55;
    if(state.context.state==='suspended') await state.context.resume();
    if(state.context.state!=='running') throw new Error(`Audio context state is ${state.context.state}. Tap Play again or allow audio.`);
  }
  const midiToHz=m=>440*Math.pow(2,(m-69)/12);
  function playVoice(freq,start,duration,type,gainValue,cutoff){
    const ctx=state.context,osc=ctx.createOscillator(),gain=ctx.createGain(),filter=ctx.createBiquadFilter();
    osc.type=type;osc.frequency.setValueAtTime(freq,start);filter.type='lowpass';filter.frequency.setValueAtTime(cutoff,start);
    gain.gain.setValueAtTime(.0001,start);gain.gain.exponentialRampToValueAtTime(Math.max(.0002,gainValue),start+.02);gain.gain.exponentialRampToValueAtTime(.0001,start+duration);
    osc.connect(filter);filter.connect(gain);gain.connect(state.master);osc.start(start);osc.stop(start+duration+.03);
  }
  function scheduleStep(){
    if(!state.playing)return;
    const t=currentTrack(),phase=currentPhase(),beat=60/t.bpm,time=state.context.currentTime+.04,brightness=Number($('brightness').value),bass=Number($('bass').value),energy=Number($('energy').value),exploration=Number($('exploration').value);
    const patternIndex=state.step%t.pattern.length;let note=t.root+t.pattern[patternIndex]+phase.transpose;
    if(exploration>65&&state.step%16===12)note+=12;
    const leadType=brightness>60?'sawtooth':brightness>35?'triangle':'sine';
    playVoice(midiToHz(note),time,beat*(.52+phase.density*.28),leadType,(.018+energy/6500)*phase.density,450+brightness*34);
    if(state.step%2===0)playVoice(midiToHz(t.root-12+(phase.name==='LIFT'?5:0)),time,beat*.88,'sine',(.03+bass/3000)*phase.density,160+bass*6);
    if(state.step%4===0)playVoice(58+(energy/10),time,.12,'sine',.055*phase.density,130);
    if(state.step%2===1&&energy>48&&phase.name!=='INTRO')playVoice(1300+brightness*25,time,.035,'square',.0045*phase.density,4200);
    if(phase.name==='RESOLVE'&&state.step%4===2)playVoice(midiToHz(t.root+7),time,beat*1.6,'sine',.015,900);
    $('compositionPhase').textContent=`COMPOSITION · ${phase.name}`;setStatus('statusComposition',`COMPOSITION · ${phase.name}`);
    state.step=(state.step+1)%64;$('progress').value=state.step/64*100;state.timer=window.setTimeout(scheduleStep,beat*500);
  }
  async function startAudio(){
    if(state.playing)return;
    try{
      await ensureAudio();state.playing=true;$('playPause').textContent='Pause';setAudioNotice('AUDIO · running locally in this browser');scheduleStep();
      const t=currentTrack(),intent=$('sessionIntent').value;
      makeEvent('playback_started',`Playing “${t.title}”.`,{captured_records:[{track_id:t.id,source:'browser_generated',completed:false,profile:state.profile.name,volume:Number($('volume').value),session_intent:intent}],derived_records:[{session_intent:intent,composition_form:'intro_build_lift_resolve'}],contribution_eligibility:'candidate'});
      setStatus('statusPlayback','PLAYBACK · ACTIVE');
    }catch(error){state.playing=false;$('playPause').textContent='Play';setAudioNotice(`AUDIO · ${error.message}`,true);makeEvent('playback_refused',`Playback could not start: ${error.message}`,{captured_records:[{browser:navigator.userAgent,error:error.message}],derived_records:[{failure_class:'browser_audio_unavailable_or_blocked'}],rights_status:'not_applicable',source_class:'local_runtime',contribution_eligibility:'not_evaluated'});}
  }
  function pauseAudio(){state.playing=false;window.clearTimeout(state.timer);$('playPause').textContent='Play';setAudioNotice('AUDIO · paused; tap Play to resume');makeEvent('playback_paused',`Paused “${currentTrack().title}”.`,{captured_records:[{position:Number($('progress').value),phase:currentPhase().name}]});}
  function stopAudio(record=true){state.playing=false;window.clearTimeout(state.timer);state.step=0;if($('playPause'))$('playPause').textContent='Play';if($('progress'))$('progress').value=0;if($('compositionPhase'))$('compositionPhase').textContent='COMPOSITION · INTRO';if(record&&state.events.length)makeEvent('playback_stopped',`Stopped “${currentTrack().title}”.`);}
  function applyFeedback(text){
    const value=text.trim();if(!value)return;const derived=[],lower=value.toLowerCase();
    if(lower.includes('less bright')){$('brightness').value=clamp(Number($('brightness').value)-15,0,100);derived.push({trait:'brightness',direction:'decrease'});}
    if(lower.includes('low-end')||lower.includes('bass')){$('bass').value=clamp(Number($('bass').value)+8,0,100);derived.push({trait:'bass_texture',direction:'retain_or_increase'});}
    if(lower.includes('drive')){$('energy').value=clamp(Number($('energy').value)+10,0,100);derived.push({trait:'energy',direction:'increase'});}
    if(lower.includes('abrupt')){$('exploration').value=clamp(Number($('exploration').value)-10,0,100);derived.push({trait:'transition_distance',direction:'decrease'});}
    if(!derived.length)derived.push({trait:'unclassified_user_language',text:value});
    state.value+=.0005+derived.length*.00025;
    makeEvent('preference_refinement',`Refinement: ${value}`,{captured_records:[{explicit_feedback:value,track_id:currentTrack().id,composition_phase:currentPhase().name,trait_controls:{energy:Number($('energy').value),brightness:Number($('brightness').value),bass:Number($('bass').value),exploration:Number($('exploration').value)}}],derived_records:derived,contribution_eligibility:'candidate',royalty_state:'prototype_estimate_only'});
    setStatus('statusPreference','PREFERENCE · ACTIVE');setStatus('statusProjection','PROJECTION · ACTIVE');setStatus('statusRoyalty','ROYALTY · CANDIDATE');renderFinance();$('feedbackText').value='';
  }
  function eventCards(mode){return state.events.slice().reverse().map(e=>{const active=e.event_id===state.selectedEventId?' correlated-active':'';if(mode==='conversation')return `<div class="event${active}" data-event="${e.event_id}"><strong>${escapeHtml(e.human_projection.text)}</strong><br>${new Date(e.timestamp).toLocaleTimeString()}</div>`;return `<div class="event${active}" data-event="${e.event_id}"><strong>${escapeHtml(e.event_type)}</strong><br>event_id=${escapeHtml(e.event_id)}<br>rights=${escapeHtml(e.governed_projection.rights_status)}<br>reuse=${escapeHtml(e.governed_projection.permitted_reuse.join(', '))}<br>royalty=${escapeHtml(e.governed_projection.royalty_state)}<br>revoked=${e.governed_projection.reuse_revoked}</div>`;}).join('')||'<p class="muted">Events will appear as you search, select, play, and refine.</p>';}
  function renderEvents(){$('conversationEvents').innerHTML=eventCards('conversation');$('governedEvents').innerHTML=eventCards('governed');$('splitConversation').innerHTML=eventCards('conversation');$('splitGoverned').innerHTML=eventCards('governed');$('rawEvents').textContent=state.events.map(e=>JSON.stringify(e)).join('\n');document.querySelectorAll('[data-event]').forEach(el=>el.addEventListener('click',()=>inspectEvent(el.dataset.event)));}
  function inspectEvent(eventId){const event=state.events.find(e=>e.event_id===eventId);if(!event)return;state.selectedEventId=eventId;$('capturedInspection').textContent=JSON.stringify(event.governed_projection.captured_records,null,2);$('derivedInspection').textContent=JSON.stringify(event.governed_projection.derived_records,null,2);$('projectionInspection').textContent=JSON.stringify({permitted_reuse:event.governed_projection.permitted_reuse,prohibited_reuse:event.governed_projection.prohibited_reuse,downstream_services:event.governed_projection.downstream_services,reuse_revoked:event.governed_projection.reuse_revoked},null,2);renderEvents();}
  function renderFinance(){$('financeTotal').textContent=`$${state.value.toFixed(4)}`;const candidates=state.events.filter(e=>e.governed_projection.contribution_eligibility==='candidate').length;$('financeBreakdown').innerHTML=`<div class="event">candidate_events=${candidates}<br>realized_royalty=$0.0000<br>prototype_estimate=${state.value.toFixed(4)}<br>payable=false</div>`;}
  function exportSession(){const blob=new Blob([JSON.stringify({schema:'stegmusic-session-v1',exported_at:now(),profile:state.profile,permissions:state.permissions,events:state.events,prototype_value:state.value},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`stegmusic-session-${Date.now()}.json`;a.click();URL.revokeObjectURL(url);}
  function saveProfile(){state.profile.name=$('profileName').value.trim()||'Default listener';persist();makeEvent('profile_saved',`Listening profile saved as “${state.profile.name}”.`,{captured_records:[{profile_name:state.profile.name}],derived_records:[{profile_scope:'browser_local'}]});}
  function syncPermissions(record=true){state.permissions={stegdj:$('permitStegDJ').checked,aggregate:$('permitAggregate').checked,wellness:$('permitWellness').checked,revoked:state.permissions.revoked};persist();if(record)makeEvent('projection_permissions_changed','Updated cross-service projection permissions.',{captured_records:[{...state.permissions}],derived_records:[{projection_scope:permissionSnapshot()}]});}
  function revokeReuse(){state.permissions.revoked=true;$('permitStegDJ').checked=false;$('permitAggregate').checked=false;$('permitWellness').checked=false;persist();makeEvent('future_reuse_revoked','Revoked future cross-service reuse. Historical occurrence receipts remain.',{captured_records:[{revoked_at:now()}],derived_records:[{future_projection_state:'denied',historical_receipts_preserved:true}],permitted_reuse:['historical_occurrence_receipt_only'],downstream_services:[]});}
  function resetSession(){stopAudio(false);state.events=[];state.value=0;state.selectedEventId=null;state.permissions={stegdj:true,aggregate:false,wellness:false,revoked:false};persist();$('permitStegDJ').checked=true;$('permitAggregate').checked=false;$('permitWellness').checked=false;$('capturedInspection').textContent='Select any event to inspect direct observations.';$('derivedInspection').textContent='Select any event to inspect StegDJ interpretations.';$('projectionInspection').textContent='No event selected.';renderEvents();renderFinance();setAudioNotice('AUDIO · waiting for a user-initiated Play action');}

  $('searchButton').addEventListener('click',()=>{renderCatalog($('musicSearch').value);makeEvent('music_search',`Searched music for “${$('musicSearch').value||'all local tracks'}”.`,{captured_records:[{query:$('musicSearch').value}],derived_records:[{result_count:tracks.length}]});});
  $('musicSearch').addEventListener('input',e=>renderCatalog(e.target.value));$('surpriseButton').addEventListener('click',()=>selectTrack(Math.floor(Math.random()*tracks.length)));
  $('playPause').addEventListener('click',()=>state.playing?pauseAudio():startAudio());$('stopButton').addEventListener('click',()=>stopAudio(true));$('previousButton').addEventListener('click',()=>selectTrack((state.trackIndex-1+tracks.length)%tracks.length));$('nextButton').addEventListener('click',()=>selectTrack((state.trackIndex+1)%tracks.length));
  $('volume').addEventListener('input',()=>{if(state.master)state.master.gain.value=Number($('volume').value)/100*.55;});
  document.querySelectorAll('[data-feedback]').forEach(b=>b.addEventListener('click',()=>applyFeedback(b.dataset.feedback.replaceAll('-',' '))));$('applyFeedback').addEventListener('click',()=>applyFeedback($('feedbackText').value));
  $('financeButton').addEventListener('click',()=>{$('financePanel').hidden=!$('financePanel').hidden;renderFinance();});$('exportButton').addEventListener('click',exportSession);$('saveProfile').addEventListener('click',saveProfile);
  ['permitStegDJ','permitAggregate','permitWellness'].forEach(id=>$(id).addEventListener('change',()=>{state.permissions.revoked=false;syncPermissions(true);}));$('revokeButton').addEventListener('click',revokeReuse);$('resetButton').addEventListener('click',resetSession);
  document.querySelectorAll('[data-view]').forEach(tab=>tab.addEventListener('click',()=>{document.querySelectorAll('[data-view]').forEach(t=>t.classList.toggle('active',t===tab));document.querySelectorAll('.projection').forEach(v=>v.classList.remove('active'));$(`${tab.dataset.view}View`).classList.add('active');}));

  $('profileName').value=state.profile.name;$('permitStegDJ').checked=state.permissions.stegdj&&!state.permissions.revoked;$('permitAggregate').checked=state.permissions.aggregate&&!state.permissions.revoked;$('permitWellness').checked=state.permissions.wellness&&!state.permissions.revoked;
  selectTrack(0);renderEvents();renderFinance();
})();