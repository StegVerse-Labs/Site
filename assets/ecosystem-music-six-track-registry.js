(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const EXTRA = [
    {id:'stegdj-black-glass',title:'Black Glass Highway',genre:'darkwave / electronic drive',bpm:104,root:43,pattern:[0,3,7,10,12,10,7,5],brightness:30,energy:68,bass:88,license:'StegDJ generated · local prototype'},
    {id:'stegdj-slow-telemetry',title:'Slow Telemetry',genre:'minimal electronic / focus',bpm:72,root:38,pattern:[0,5,3,7,5,10,7,3],brightness:20,energy:34,bass:76,license:'StegDJ generated · local prototype'},
    {id:'stegdj-redline-signal',title:'Redline Signal',genre:'progressive electronic / high drive',bpm:124,root:50,pattern:[0,7,12,10,7,15,12,5],brightness:68,energy:86,bass:64,license:'StegDJ generated · local prototype'}
  ];
  const emit = (type,human,governed) => window.dispatchEvent(new CustomEvent('stegmusic:emit',{detail:{type,human,governed}}));
  let activeExtra = null;
  function install(){
    const runtime=window.StegMusicRuntime;
    if(!runtime||runtime.__sixTrackRegistry)return false;
    const originalSelect=runtime.selectGeneratedTrack.bind(runtime);
    const originalCurrent=runtime.getCurrentTrack.bind(runtime);
    const base=typeof runtime.getTracks==='function'?runtime.getTracks():[0,1,2].map(i=>{originalSelect(i,{reason:'registry_probe'});return originalCurrent();});
    const tracks=[...base,...EXTRA];
    runtime.selectGeneratedTrack=(index,selection={})=>{
      if(index<base.length){activeExtra=null;return originalSelect(index,selection);}
      const track=tracks[index]; if(!track)return null; activeExtra=track;
      if($('trackTitle'))$('trackTitle').textContent=track.title;
      if($('trackInfo'))$('trackInfo').textContent=`${track.genre} · ${track.bpm} BPM · enhanced harmonic renderer`;
      if($('energy'))$('energy').value=String(track.energy);
      if($('brightness'))$('brightness').value=String(track.brightness);
      if($('bass'))$('bass').value=String(track.bass);
      if($('progress'))$('progress').value='0';
      emit('music_selection',`Selected “${track.title}”.`,{rights_status:'stegdj_generated_local_prototype',source_class:'six_track_registry',captured_records:[{track_id:track.id,title:track.title,bpm:track.bpm,runtime_index:index}],derived_records:[{selection_reason:selection.reason||'registry_selection',enhanced_renderer_compatible:true,authority:'none'}],artifact_refs:[track.id],contribution_eligibility:'candidate',royalty_state:'not_realized'});
      return {...track};
    };
    runtime.getCurrentTrack=()=>activeExtra?({...activeExtra}):originalCurrent();
    runtime.getTracks=()=>tracks.map(t=>({...t}));
    runtime.getTrackCount=()=>tracks.length;
    runtime.__sixTrackRegistry=true;
    const host=document.querySelector('section[aria-labelledby="catalog-heading"]');
    if(host&&!$('sixTrackPlayground')){
      const panel=document.createElement('div'); panel.id='sixTrackPlayground'; panel.className='audio-notice';
      panel.innerHTML=`<strong>PLAY AROUND · SIX GENERATED TRACKS</strong><div class="player-actions">${tracks.map((t,i)=>`<button class="sv-btn sv-btn-secondary" type="button" data-six-track="${i}">${t.title}</button>`).join('')}</div>`;
      host.appendChild(panel);
      panel.querySelectorAll('[data-six-track]').forEach(b=>b.addEventListener('click',()=>runtime.selectGeneratedTrack(Number(b.dataset.sixTrack),{reason:'playground_selection'})));
    }
    window.StegMusicSixTrackRegistry=Object.freeze({track_count:tracks.length,track_ids:tracks.map(t=>t.id),authority:'none'});
    emit('stegmusic_six_track_registry_ready','Six-track StegMusic registry is ready.',{rights_status:'not_applicable',source_class:'browser_runtime_registry',captured_records:[{track_count:tracks.length,track_ids:tracks.map(t=>t.id)}],derived_records:[{enhanced_renderer_compatible:true,authority:'none'}],contribution_eligibility:'not_evaluated',royalty_state:'not_realized'});
    return true;
  }
  let tries=0; const timer=setInterval(()=>{tries+=1;if(install()||tries>80)clearInterval(timer);},50);
})();
