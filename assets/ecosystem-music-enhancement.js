(() => {
  'use strict';

  const $ = id => document.getElementById(id);
  const clamp = (n, min, max) => Math.max(min, Math.min(max, n));
  const midiToHz = midi => 440 * Math.pow(2, (midi - 69) / 12);
  const delay = ms => new Promise(resolve => window.setTimeout(resolve, ms));
  const emit = (type, human, captured = {}, derived = {}) => window.dispatchEvent(new CustomEvent('stegmusic:emit', {
    detail: { type, human, governed: {
      rights_status: 'stegdj_generated_local_prototype',
      source_class: 'generated_media_enhancement',
      captured_records: [captured], derived_records: [derived],
      contribution_eligibility: 'not_evaluated', royalty_state: 'not_realized', fixture: false,
      policy_refs: ['stegmusic-rights-boundary-v0', 'stegmusic-loudness-harmony-v0', 'stegmusic-arrangement-arc-v0', 'stegmusic-style-characteristics-v1']
    }}
  }));

  const state = { audio: null, objectUrl: null, trackId: null, playing: false, rendering: false, renderProfileId: null };
  const chordProgressions = [
    [[0,3,7],[5,8,12],[3,7,10],[7,10,14]],
    [[0,4,7],[7,11,14],[9,12,16],[5,9,12]],
    [[0,3,7,10],[5,8,12,15],[7,10,14,17],[3,7,10,14]]
  ];
  const defaultPhases = [
    {id:'intro',bars:4,density:.48,leadOctave:0,bass:.62},
    {id:'build',bars:4,density:.72,leadOctave:0,bass:.72},
    {id:'peak',bars:4,density:1,leadOctave:12,bass:1},
    {id:'breakdown',bars:4,density:.38,leadOctave:-12,bass:.34},
    {id:'return',bars:4,density:.86,leadOctave:0,bass:.86}
  ];
  const edmDropPhases = [
    {id:'intro',bars:4,density:.38,leadOctave:0,bass:.42},
    {id:'buildup',bars:4,density:.64,leadOctave:0,bass:.48,riser:true},
    {id:'pre_drop_tension',bars:2,density:.28,leadOctave:12,bass:.08,riser:true,withholdKick:true},
    {id:'bass_drop',bars:6,density:1.08,leadOctave:12,bass:1.18,drop:true},
    {id:'development',bars:4,density:.9,leadOctave:0,bass:.96},
    {id:'breakdown',bars:4,density:.3,leadOctave:-12,bass:.28},
    {id:'second_buildup',bars:3,density:.72,leadOctave:0,bass:.42,riser:true},
    {id:'larger_drop',bars:7,density:1.18,leadOctave:12,bass:1.28,drop:true,larger:true},
    {id:'return_or_outro',bars:2,density:.68,leadOctave:0,bass:.72}
  ];

  const controls = () => ({
    energy:Number($('energy')?.value||58), brightness:Number($('brightness')?.value||38),
    bass:Number($('bass')?.value||72), exploration:Number($('exploration')?.value||32),
    volume:Number($('volume')?.value||32), intent:$('sessionIntent')?.value||'fine_tune'
  });
  const activeProfile = () => window.StegMusicStyleResolver?.getActiveProfile?.() || null;
  const phasesFor = profile => profile?.profile_id === 'edm_high_energy_bass_drop' ? edmDropPhases : defaultPhases;

  function setNotice(text, failed=false) {
    if ($('audioNotice')) $('audioNotice').textContent=text;
    const status=$('statusAudio'); if(status){status.textContent=failed?'AUDIO ENHANCEMENT · BLOCKED':'AUDIO ENHANCEMENT · ACTIVE';status.classList.remove('pending','active','failed');status.classList.add(failed?'failed':'active');}
  }

  function audioElement() {
    if(state.audio)return state.audio;
    state.audio=$('generatedMediaPlayer')||document.createElement('audio');
    if(!state.audio.id){state.audio.id='generatedMediaPlayer';state.audio.preload='auto';state.audio.playsInline=true;state.audio.style.display='none';document.body.appendChild(state.audio);}
    state.audio.addEventListener('play',()=>{state.playing=true;if($('playPause'))$('playPause').textContent='Pause';setNotice('AUDIO · profile-governed normalized mix playing');});
    state.audio.addEventListener('pause',()=>{state.playing=false;if($('playPause'))$('playPause').textContent='Play';});
    state.audio.addEventListener('timeupdate',()=>{if($('progress')&&Number.isFinite(state.audio.duration)&&state.audio.duration>0)$('progress').value=String(state.audio.currentTime/state.audio.duration*100);});
    return state.audio;
  }

  function voice(ctx,destination,frequency,start,duration,type,level,cutoff,pan=0,attack=.015){
    const oscillator=ctx.createOscillator(),filter=ctx.createBiquadFilter(),gain=ctx.createGain(),panner=ctx.createStereoPanner?ctx.createStereoPanner():null;
    oscillator.type=type;oscillator.frequency.setValueAtTime(frequency,start);filter.type='lowpass';filter.frequency.setValueAtTime(cutoff,start);
    gain.gain.setValueAtTime(.0001,start);gain.gain.exponentialRampToValueAtTime(Math.max(.0002,level),start+attack);gain.gain.exponentialRampToValueAtTime(.0001,start+duration);
    oscillator.connect(filter);filter.connect(gain);if(panner){panner.pan.setValueAtTime(clamp(pan,-1,1),start);gain.connect(panner);panner.connect(destination);}else gain.connect(destination);
    oscillator.start(start);oscillator.stop(start+duration+.04);
  }

  function percussion(ctx,destination,start,level,bright,duration=.1){
    const length=Math.max(1,Math.floor(ctx.sampleRate*duration)),buffer=ctx.createBuffer(1,length,ctx.sampleRate),data=buffer.getChannelData(0);
    for(let i=0;i<length;i+=1)data[i]=(Math.random()*2-1)*Math.pow(1-i/length,2.5);
    const source=ctx.createBufferSource(),filter=ctx.createBiquadFilter(),gain=ctx.createGain();source.buffer=buffer;filter.type='highpass';filter.frequency.value=1800+bright*45;
    gain.gain.setValueAtTime(level,start);gain.gain.exponentialRampToValueAtTime(.0001,start+duration);source.connect(filter);filter.connect(gain);gain.connect(destination);source.start(start);
  }

  function impact(ctx,destination,start,level){
    voice(ctx,destination,48,start,.32,'sine',level,120,0,.004);
    percussion(ctx,destination,start,level*.34,72,.22);
  }

  function normalize(buffer,targetPeak=.94){
    let peak=0;for(let channel=0;channel<buffer.numberOfChannels;channel+=1){const data=buffer.getChannelData(channel);for(let i=0;i<data.length;i+=1)peak=Math.max(peak,Math.abs(data[i]));}
    const gain=peak>0?Math.min(8,targetPeak/peak):1;for(let channel=0;channel<buffer.numberOfChannels;channel+=1){const data=buffer.getChannelData(channel);for(let i=0;i<data.length;i+=1)data[i]=clamp(data[i]*gain,-1,1);}
    return {peakBefore:peak,normalizationGain:gain,targetPeak};
  }

  function encodeWav(buffer){
    const channels=buffer.numberOfChannels,frames=buffer.length,sampleRate=buffer.sampleRate,out=new ArrayBuffer(44+frames*channels*2),view=new DataView(out);
    const text=(offset,value)=>{for(let i=0;i<value.length;i+=1)view.setUint8(offset+i,value.charCodeAt(i));};
    text(0,'RIFF');view.setUint32(4,36+frames*channels*2,true);text(8,'WAVE');text(12,'fmt ');view.setUint32(16,16,true);view.setUint16(20,1,true);view.setUint16(22,channels,true);
    view.setUint32(24,sampleRate,true);view.setUint32(28,sampleRate*channels*2,true);view.setUint16(32,channels*2,true);view.setUint16(34,16,true);text(36,'data');view.setUint32(40,frames*channels*2,true);
    let offset=44;for(let frame=0;frame<frames;frame+=1){for(let channel=0;channel<channels;channel+=1){const sample=clamp(buffer.getChannelData(channel)[frame],-1,1);view.setInt16(offset,sample<0?sample*0x8000:sample*0x7fff,true);offset+=2;}}
    return new Blob([out],{type:'audio/wav'});
  }

  async function render(){
    if(state.rendering)return null;
    const track=window.StegMusicRuntime?.getCurrentTrack?.();if(!track)throw new Error('No generated track is selected.');
    state.rendering=true;
    const profile=activeProfile(),phases=phasesFor(profile),profileName=profile?.display_name||'adaptive long-form';
    setNotice(`AUDIO · building ${profileName} mix for “${track.title}”`);
    try{
      const c=controls(),OfflineCtor=window.OfflineAudioContext||window.webkitOfflineAudioContext;if(!OfflineCtor)throw new Error('Offline audio rendering is unavailable.');
      const sampleRate=44100,preferredBpm=profile?.characteristics?.tempo_bpm?.preferred,renderBpm=preferredBpm||track.bpm,beat=60/renderBpm;
      const totalBars=phases.reduce((sum,phase)=>sum+phase.bars,0),duration=totalBars*beat*4+2,ctx=new OfflineCtor(2,Math.ceil(sampleRate*duration),sampleRate);
      const mix=ctx.createGain(),compressor=ctx.createDynamicsCompressor(),output=ctx.createGain();
      compressor.threshold.value=-20;compressor.knee.value=18;compressor.ratio.value=4.5;compressor.attack.value=.008;compressor.release.value=.18;output.gain.value=1.28;
      mix.connect(compressor);compressor.connect(output);output.connect(ctx.destination);
      const progression=chordProgressions[c.exploration>66?2:c.brightness>48?1:0],complexity=clamp(Math.round(1+c.exploration/22+c.energy/35),2,8);
      let barOffset=0,dropCount=0;
      phases.forEach((phase,phaseIndex)=>{
        if(phase.drop){dropCount+=1;impact(ctx,mix,barOffset*beat*4,.36+(phase.larger?.12:0));}
        for(let localBar=0;localBar<phase.bars;localBar+=1){
          const bar=barOffset+localBar,chord=progression[(bar+(phaseIndex>=2?phaseIndex:0))%progression.length],start=bar*beat*4;
          chord.forEach((interval,index)=>voice(ctx,mix,midiToHz(track.root+interval+(phase.larger&&index===0?12:0)),start,beat*3.88,index%2?'triangle':'sine',(.043+c.energy/5800)*phase.density,780+c.brightness*27,(index-1.5)*.28,phase.id==='intro'?.22:.1));
          const bassRoot=track.root-24+chord[0],bassLevel=(.12+c.bass/900)*phase.bass;
          if(phase.bass>.15)voice(ctx,mix,midiToHz(bassRoot),start,beat*3.9,'sine',bassLevel,145+c.bass*5.5,0,.025);
          if(phase.drop)voice(ctx,mix,midiToHz(bassRoot+12),start,beat*3.82,'sawtooth',bassLevel*.34,320+c.bass*7,0,.01);
          if(phase.riser){for(let q=0;q<8;q+=1)voice(ctx,mix,340+q*44,start+q*beat/2,beat*.45,'sawtooth',.012+.004*q,1200+q*260,(q-3.5)*.12,.01);}
        }
        barOffset+=phase.bars;
      });
      const totalSteps=totalBars*8;
      for(let step=0;step<totalSteps;step+=1){
        const time=step*beat/2,bar=Math.floor(step/8);let traversed=0;
        const phase=phases.find(candidate=>{traversed+=candidate.bars;return bar<traversed;})||phases[phases.length-1];
        let note=track.root+track.pattern[step%track.pattern.length]+phase.leadOctave;if(phase.drop&&step%16===12)note+=7;if(phase.larger&&step%8>=4)note+=5;
        const leadActive=!phase.withholdKick&&(phase.id!=='breakdown'||step%4===0),leadType=c.brightness>60?'sawtooth':c.brightness>35?'triangle':'sine';
        if(leadActive)voice(ctx,mix,midiToHz(note),time,beat*(phase.id==='intro'?.7:.42),leadType,(.062+c.energy/1900)*phase.density,650+c.brightness*42,step%2?.2:-.2);
        if(complexity>=4&&step%2===1&&phase.density>.5)voice(ctx,mix,midiToHz(note-12+(step%8===7?5:0)),time+beat*.08,beat*.34,'triangle',.034*phase.density,950+c.brightness*18,step%4===1?-.44:.44);
        if(!phase.withholdKick&&step%4===0)voice(ctx,mix,52+c.energy/8,time,.16,'sine',(.16+(phase.drop?.08:0))*phase.density,140,0,.004);
        if(step%2===0&&complexity>=3&&phase.density>.42)percussion(ctx,mix,time+beat*.25,(.04+c.energy/5200)*phase.density,c.brightness);
        if(phase.drop&&step%2===1)percussion(ctx,mix,time+beat*.03,.026*phase.density,c.brightness+18,.07);
      }
      const rendered=await ctx.startRendering(),normalized=normalize(rendered,.94),blob=encodeWav(rendered);if(state.objectUrl)URL.revokeObjectURL(state.objectUrl);state.objectUrl=URL.createObjectURL(blob);
      const audio=audioElement();audio.pause();audio.src=state.objectUrl;audio.volume=1;audio.load();state.trackId=track.id;state.renderProfileId=profile?.profile_id||null;
      emit('generated_harmonic_mix_rendered',`Rendered profile-governed StegDJ mix “${track.title}”.`,{
        track_id:track.id,title:track.title,style_profile_id:state.renderProfileId,style_profile_name:profileName,render_bpm:renderBpm,duration_seconds:duration,total_bars:totalBars,
        arrangement_phases:phases.map(phase=>phase.id),drop_count:dropCount,required_events:profile?.required_events||[],bass_strategy:profile?'profile_governed_sub_bass_drop_contrast':'sustained_sub_bass_harmonic_pulses',
        compressor:{threshold_db:-20,knee_db:18,ratio:4.5,attack_seconds:.008,release_seconds:.18},output_gain:1.28,peak_before_normalization:normalized.peakBefore,normalization_gain:normalized.normalizationGain,
        normalized_target_peak:normalized.targetPeak,harmony_voice_count:progression[0].length,complexity_level:complexity,html_audio_volume:1,controls:c,source_bytes_uploaded:false
      },{
        perceived_loudness_strategy:'compression_output_gain_peak_normalization',harmony_strategy:'progressive_chord_pad_bass_countermelody',arrangement_strategy:profile?'explicit_style_profile_contract':'long_form_intro_build_peak_breakdown_return',
        profile_required_events_encoded:Boolean(profile),clear_buildup_encoded:phases.some(p=>p.riser),audible_pre_drop_contrast_encoded:phases.some(p=>p.id==='pre_drop_tension'),sub_bass_entry_at_drop_encoded:phases.some(p=>p.drop),
        rhythmic_density_increase_at_drop_encoded:phases.some(p=>p.drop&&p.density>=1),secondary_release_encoded:dropCount>=2,clipping_prevention:'normalized_peak_0_94',human_audibility_confirmed:false
      });
      return audio;
    }finally{state.rendering=false;}
  }

  async function play(){
    try{window.StegMusicMediaTransport?.stop?.(false);const track=window.StegMusicRuntime?.getCurrentTrack?.(),profileId=activeProfile()?.profile_id||null;let audio=audioElement();if(!audio.src||state.trackId!==track?.id||state.renderProfileId!==profileId)audio=await render();audio.volume=1;await audio.play();emit('enhanced_media_playback_started',`Playing profile-governed mix “${track.title}”.`,{track_id:track.id,style_profile_id:profileId,html_audio_volume:audio.volume,player_volume_control:Number($('volume')?.value||32),user_agent:navigator.userAgent},{transport:'normalized_compressed_wav_html_audio'});}catch(error){setNotice(`AUDIO · ${error.message}`,true);emit('enhanced_media_playback_refused',`Enhanced playback failed: ${error.message}`,{error:error.message},{authority:'none'});}
  }
  function pause(){audioElement().pause();}
  function stop(){const audio=audioElement();audio.pause();audio.currentTime=0;if($('progress'))$('progress').value='0';}
  function replaceButton(id,handler){const old=$(id);if(!old)return;const fresh=old.cloneNode(true);old.replaceWith(fresh);fresh.addEventListener('click',event=>{event.preventDefault();handler();});}

  async function initialize(){
    for(let i=0;i<80&&!window.StegMusicRuntime;i+=1)await delay(50);if(!window.StegMusicRuntime)return;
    replaceButton('playPause',()=>state.playing?pause():play());replaceButton('stopButton',stop);
    ['previousButton','nextButton','adaptiveNext','surpriseButton'].forEach(id=>$(id)?.addEventListener('click',()=>{const resume=state.playing;stop();window.setTimeout(async()=>{state.trackId=null;if(resume)await play();},20);}));
    ['volume','energy','brightness','bass','exploration'].forEach(id=>$(id)?.addEventListener('input',()=>{state.trackId=null;setNotice('AUDIO · preference change will be applied on the next rendered mix');}));
    window.addEventListener('stegmusic:emit',event=>{if(event.detail?.type==='stegmusic_style_profile_applied'){state.trackId=null;state.renderProfileId=null;setNotice('AUDIO · style profile applied · next Play will render its full composition contract');}});
    window.StegMusicEnhancement=Object.freeze({play,pause,stop,render,getState:()=>({...state,audio:undefined}),getActiveArrangement:()=>phasesFor(activeProfile()).map(p=>({...p}))});
    emit('stegmusic_loudness_harmony_ready','Loudness normalization, harmonic complexity, and profile-governed arrangement are ready.',{compressor_available:typeof OfflineAudioContext!=='undefined'||typeof webkitOfflineAudioContext!=='undefined',target_peak:.94,html_audio_volume:1,style_resolver_ready:Boolean(window.StegMusicStyleResolver)},{double_attenuation_removed:true,harmony_enabled:true,style_profile_rendering_enabled:true});
  }
  initialize();
})();
