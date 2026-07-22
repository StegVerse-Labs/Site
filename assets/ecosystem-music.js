(() => {
  'use strict';

  const tracks = [
    {id:'stegdj-night-drive', title:'Night Drive Boundary', genre:'dark electronic / steady drive', bpm:96, root:45, pattern:[0,3,7,10,7,3,5,8], brightness:34, energy:58, bass:78, license:'StegDJ generated · local prototype'},
    {id:'stegdj-low-orbit', title:'Low Orbit Relay', genre:'ambient bass / restrained motion', bpm:78, root:40, pattern:[0,7,5,10,3,8,7,5], brightness:24, energy:42, bass:84, license:'StegDJ generated · local prototype'},
    {id:'stegdj-signal-rise', title:'Signal Rise', genre:'progressive synth / alertness lift', bpm:112, root:48, pattern:[0,5,7,12,10,7,5,3], brightness:52, energy:72, bass:66, license:'StegDJ generated · local prototype'}
  ];

  const safeParse = (key, fallback) => {
    try { return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback)); }
    catch (_) { return fallback; }
  };

  const state = {
    trackIndex: 0,
    playing: false,
    context: null,
    master: null,
    timer: null,
    step: 0,
    selectedEventId: null,
    events: safeParse('stegmusic.events.v1', []),
    value: Number(localStorage.getItem('stegmusic.value.v1') || 0),
    profile: safeParse('stegmusic.profile.v1', {name:'Default listener'}),
    permissions: safeParse('stegmusic.permissions.v1', {stegdj:true, aggregate:false, wellness:false, revoked:false})
  };

  const $ = id => document.getElementById(id);
  const uid = prefix => `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,8)}`;
  const now = () => new Date().toISOString();
  const clamp = (n,min,max) => Math.max(min,Math.min(max,n));
  const escapeHtml = value => String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));

  function currentTrack(){ return tracks[state.trackIndex]; }

  function permissionSnapshot() {
    const permitted = ['private_stegmusic_profile'];
    const downstream = [];
    if (!state.permissions.revoked && state.permissions.stegdj) { permitted.push('selected_refinement_to_stegdj'); downstream.push('StegDJ'); }
    if (!state.permissions.revoked && state.permissions.aggregate) { permitted.push('aggregate_music_rule_with_separate_authorization'); downstream.push('AggregateMusicRules'); }
    if (!state.permissions.revoked && state.permissions.wellness) { permitted.push('bounded_alertness_preference'); downstream.push('Wellness'); }
    return {permitted, downstream};
  }

  function persist() {
    localStorage.setItem('stegmusic.events.v1', JSON.stringify(state.events));
    localStorage.setItem('stegmusic.value.v1', String(state.value));
    localStorage.setItem('stegmusic.profile.v1', JSON.stringify(state.profile));
    localStorage.setItem('stegmusic.permissions.v1', JSON.stringify(state.permissions));
  }

  function makeEvent(type, human, governed = {}) {
    const permissions = permissionSnapshot();
    const event = Object.freeze({
      event_id: uid('music'),
      parent_event_id: state.events.length ? state.events[state.events.length - 1].event_id : null,
      timestamp: now(),
      actor: {type:'human_or_service', id:type.startsWith('stegdj') ? 'StegDJ' : 'local-user', profile:state.profile.name},
      service: 'StegMusic/StegDJ',
      medium: 'audio',
      event_type: type,
      human_projection: {text: human},
      governed_projection: {
        rights_status: governed.rights_status || 'stegdj_generated_local_prototype',
        source_class: governed.source_class || 'generated',
        captured_records: governed.captured_records || [],
        derived_records: governed.derived_records || [],
        permitted_reuse: governed.permitted_reuse || permissions.permitted,
        prohibited_reuse: governed.prohibited_reuse || ['external_training','public_disclosure','cross_user_raw_history'],
        downstream_services: governed.downstream_services || permissions.downstream,
        contribution_eligibility: governed.contribution_eligibility || 'not_evaluated',
        royalty_state: governed.royalty_state || 'not_realized',
        reuse_revoked: state.permissions.revoked,
        authority: 'none',
        fixture: true
      },
      policy_refs: ['stegmusic-rights-boundary-v0','governed-service-envelope-v0','cross-service-projection-v0'],
      evidence_refs: [],
      artifact_refs: governed.artifact_refs || [],
      continuity_refs: state.events.length ? [state.events[state.events.length - 1].event_id] : [],
      hash: 'preview-only'
    });
    state.events.push(event);
    state.selectedEventId = event.event_id;
    persist();
    renderEvents();
    inspectEvent(event.event_id);
    return event;
  }

  function renderCatalog(filter='') {
    const query = filter.trim().toLowerCase();
    const list = tracks.filter(t => !query || `${t.title} ${t.genre} ${t.license}`.toLowerCase().includes(query));
    $('catalog').innerHTML = list.map(t => {
      const index = tracks.findIndex(x => x.id === t.id);
      return `<article class="track ${index===state.trackIndex?'active':''}" data-track="${index}"><div><strong>${escapeHtml(t.title)}</strong><span>${escapeHtml(t.genre)} · ${t.bpm} BPM</span><span class="license">${escapeHtml(t.license)}</span></div><button class="sv-btn sv-btn-secondary" type="button">Select</button></article>`;
    }).join('') || '<p class="muted">No local prototype tracks match this search.</p>';
    document.querySelectorAll('[data-track]').forEach(el => el.addEventListener('click', () => selectTrack(Number(el.dataset.track))));
  }

  function selectTrack(index) {
    const wasPlaying = state.playing;
    stopAudio(false);
    state.trackIndex = clamp(index,0,tracks.length-1);
    const t = currentTrack();
    $('trackTitle').textContent = t.title;
    $('trackInfo').textContent = `${t.genre} · ${t.bpm} BPM · source=StegDJ generated`;
    $('rightsBadge').textContent = 'STEGDJ GENERATED · LOCAL PROTOTYPE · RIGHTS RECORD VISIBLE';
    $('energy').value = t.energy;
    $('brightness').value = t.brightness;
    $('bass').value = t.bass;
    $('progress').value = 0;
    renderCatalog($('musicSearch').value);
    makeEvent('music_selection', `Selected “${t.title}”.`, {
      captured_records:[{track_id:t.id, title:t.title, genre:t.genre, bpm:t.bpm, source:'browser_generated'}],
      derived_records:[{selection_reason:'explicit_user_selection'}],
      artifact_refs:[t.id]
    });
    activate('statusProjection','PROJECTION · ACTIVE');
    if (wasPlaying) startAudio();
  }

  function ensureAudio(){
    if (!state.context) {
      state.context = new (window.AudioContext || window.webkitAudioContext)();
      state.master = state.context.createGain();
      state.master.gain.value = .22;
      state.master.connect(state.context.destination);
    }
  }

  function midiToHz(m){ return 440 * Math.pow(2,(m-69)/12); }

  function playVoice(freq, start, duration, type, gainValue, cutoff) {
    const ctx = state.context;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();
    osc.type = type;
    osc.frequency.setValueAtTime(freq,start);
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(cutoff,start);
    gain.gain.setValueAtTime(0.0001,start);
    gain.gain.exponentialRampToValueAtTime(gainValue,start+.02);
    gain.gain.exponentialRampToValueAtTime(0.0001,start+duration);
    osc.connect(filter); filter.connect(gain); gain.connect(state.master);
    osc.start(start); osc.stop(start+duration+.03);
  }

  function scheduleStep() {
    if (!state.playing) return;
    const t = currentTrack();
    const beat = 60 / t.bpm;
    const time = state.context.currentTime + .04;
    const note = t.root + t.pattern[state.step % t.pattern.length];
    const brightness = Number($('brightness').value);
    const bass = Number($('bass').value);
    const energy = Number($('energy').value);
    playVoice(midiToHz(note), time, beat*.72, brightness>55?'sawtooth':'triangle', .025 + energy/5000, 500 + brightness*35);
    if (state.step % 2 === 0) playVoice(midiToHz(t.root-12), time, beat*.9, 'sine', .04 + bass/2400, 180 + bass*6);
    if (state.step % 4 === 0) playVoice(65, time, .11, 'sine', .08, 120);
    if (state.step % 2 === 1 && energy > 50) playVoice(1800 + brightness*20, time, .035, 'square', .006, 4000);
    state.step += 1;
    $('progress').value = (state.step % 64) / 64 * 100;
    state.timer = window.setTimeout(scheduleStep, beat * 500);
  }

  function startAudio() {
    ensureAudio();
    state.context.resume();
    if (state.playing) return;
    state.playing = true;
    $('playPause').textContent = 'Pause';
    scheduleStep();
    const t = currentTrack();
    makeEvent('playback_started', `Playing “${t.title}”.`, {
      captured_records:[{track_id:t.id, source:'browser_generated', completed:false, profile:state.profile.name}],
      derived_records:[{session_intent:'interactive_fine_tuning'}],
      contribution_eligibility:'candidate'
    });
    activate('statusPlayback','PLAYBACK · ACTIVE');
  }

  function pauseAudio() {
    state.playing = false;
    window.clearTimeout(state.timer);
    $('playPause').textContent = 'Play';
    makeEvent('playback_paused', `Paused “${currentTrack().title}”.`, {captured_records:[{position:Number($('progress').value)}]});
  }

  function stopAudio(record=true) {
    state.playing = false;
    window.clearTimeout(state.timer);
    state.step = 0;
    if ($('playPause')) $('playPause').textContent = 'Play';
    if ($('progress')) $('progress').value = 0;
    if (record && state.events.length) makeEvent('playback_stopped', `Stopped “${currentTrack().title}”.`);
  }

  function applyFeedback(text) {
    const value = text.trim();
    if (!value) return;
    const derived = [];
    const lower = value.toLowerCase();
    if (lower.includes('less bright')) { $('brightness').value = clamp(Number($('brightness').value)-15,0,100); derived.push({trait:'brightness',direction:'decrease'}); }
    if (lower.includes('low-end') || lower.includes('bass')) { $('bass').value = clamp(Number($('bass').value)+8,0,100); derived.push({trait:'bass_texture',direction:'retain_or_increase'}); }
    if (lower.includes('drive')) { $('energy').value = clamp(Number($('energy').value)+10,0,100); derived.push({trait:'energy',direction:'increase'}); }
    if (lower.includes('abrupt')) { $('exploration').value = clamp(Number($('exploration').value)-10,0,100); derived.push({trait:'transition_distance',direction:'decrease'}); }
    if (!derived.length) derived.push({trait:'unclassified_user_language',text:value});

    const contribution = 0.0005 + derived.length * 0.00025;
    state.value += contribution;
    makeEvent('preference_refinement', `Refinement: ${value}`, {
      captured_records:[{explicit_feedback:value, track_id:currentTrack().id, trait_controls:{energy:Number($('energy').value),brightness:Number($('brightness').value),bass:Number($('bass').value),exploration:Number($('exploration').value)}}],
      derived_records:derived,
      contribution_eligibility:'candidate',
      royalty_state:'prototype_estimate_only'
    });
    activate('statusPreference','PREFERENCE · ACTIVE');
    activate('statusProjection','PROJECTION · ACTIVE');
    activate('statusRoyalty','ROYALTY · CANDIDATE');
    renderFinance();
    $('feedbackText').value = '';
  }

  function activate(id,text){ const el=$(id); el.textContent=text; el.classList.remove('pending'); el.classList.add('active'); }

  function eventCards(mode) {
    return state.events.slice().reverse().map(e => {
      const active = e.event_id === state.selectedEventId ? ' correlated-active' : '';
      if (mode === 'conversation') return `<div class="event${active}" data-event="${e.event_id}"><strong>${escapeHtml(e.human_projection.text)}</strong><br>${new Date(e.timestamp).toLocaleTimeString()}</div>`;
      return `<div class="event${active}" data-event="${e.event_id}"><strong>${escapeHtml(e.event_type)}</strong><br>event_id=${escapeHtml(e.event_id)}<br>rights=${escapeHtml(e.governed_projection.rights_status)}<br>reuse=${escapeHtml(e.governed_projection.permitted_reuse.join(', '))}<br>royalty=${escapeHtml(e.governed_projection.royalty_state)}<br>revoked=${e.governed_projection.reuse_revoked}</div>`;
    }).join('') || '<p class="muted">Events will appear as you search, select, play, and refine.</p>';
  }

  function renderEvents() {
    $('conversationEvents').innerHTML = eventCards('conversation');
    $('governedEvents').innerHTML = eventCards('governed');
    $('splitConversation').innerHTML = eventCards('conversation');
    $('splitGoverned').innerHTML = eventCards('governed');
    $('rawEvents').textContent = state.events.map(e => JSON.stringify(e)).join('\n');
    document.querySelectorAll('[data-event]').forEach(el => el.addEventListener('click', () => inspectEvent(el.dataset.event)));
  }

  function inspectEvent(eventId) {
    const event = state.events.find(e => e.event_id === eventId);
    if (!event) return;
    state.selectedEventId = eventId;
    $('capturedInspection').textContent = JSON.stringify(event.governed_projection.captured_records, null, 2);
    $('derivedInspection').textContent = JSON.stringify(event.governed_projection.derived_records, null, 2);
    $('projectionInspection').textContent = JSON.stringify({
      permitted_reuse:event.governed_projection.permitted_reuse,
      prohibited_reuse:event.governed_projection.prohibited_reuse,
      downstream_services:event.governed_projection.downstream_services,
      reuse_revoked:event.governed_projection.reuse_revoked
    }, null, 2);
    renderEvents();
  }

  function renderFinance() {
    $('financeTotal').textContent = `$${state.value.toFixed(4)}`;
    const candidates = state.events.filter(e => e.governed_projection.contribution_eligibility === 'candidate').length;
    $('financeBreakdown').innerHTML = `<div class="event">candidate_events=${candidates}<br>realized_royalty=$0.0000<br>prototype_estimate=${state.value.toFixed(4)}<br>payable=false<br>profile=${escapeHtml(state.profile.name)}</div>`;
  }

  function renderPermissions() {
    $('permitStegDJ').checked = state.permissions.stegdj;
    $('permitAggregate').checked = state.permissions.aggregate;
    $('permitWellness').checked = state.permissions.wellness;
  }

  function updatePermissions() {
    state.permissions = {
      stegdj:$('permitStegDJ').checked,
      aggregate:$('permitAggregate').checked,
      wellness:$('permitWellness').checked,
      revoked:false
    };
    persist();
    makeEvent('projection_permission_changed', 'Updated downstream music projection permissions.', {
      captured_records:[{permissions:{...state.permissions}}],
      derived_records:[{projection_scope_recomputed:true}],
      contribution_eligibility:'not_evaluated'
    });
    activate('statusProjection','PROJECTION · ACTIVE');
  }

  function saveProfile() {
    const name = $('profileName').value.trim() || 'Default listener';
    state.profile = {name, saved_at:now()};
    persist();
    makeEvent('listening_profile_saved', `Saved listening profile “${name}”.`, {
      captured_records:[{profile_name:name}],
      derived_records:[{persistent_profile:true}]
    });
  }

  function revokeFutureReuse() {
    state.permissions = {stegdj:false, aggregate:false, wellness:false, revoked:true};
    persist();
    renderPermissions();
    makeEvent('future_reuse_revoked', 'Revoked future downstream reuse of music-derived records.', {
      captured_records:[{revoked_at:now()}],
      derived_records:[{future_projection_allowed:false}],
      permitted_reuse:['private_stegmusic_profile'],
      downstream_services:[]
    });
    $('statusProjection').textContent = 'PROJECTION · REVOKED';
  }

  function resetSession() {
    stopAudio(false);
    const confirmed = window.confirm('Clear this browser-local StegMusic session, profile value estimate, and events?');
    if (!confirmed) return;
    state.events = [];
    state.value = 0;
    state.selectedEventId = null;
    localStorage.removeItem('stegmusic.events.v1');
    localStorage.removeItem('stegmusic.value.v1');
    $('capturedInspection').textContent = 'Select any event to inspect direct observations.';
    $('derivedInspection').textContent = 'Select any event to inspect StegDJ interpretations.';
    $('projectionInspection').textContent = 'No event selected.';
    renderEvents();
    renderFinance();
  }

  function exportSession() {
    const payload = {schema:'stegmusic-session-v0', exported_at:now(), profile:state.profile, permissions:state.permissions, events:state.events, prototype_value:state.value};
    const blob = new Blob([JSON.stringify(payload,null,2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `stegmusic-session-${Date.now()}.json`; a.click();
    URL.revokeObjectURL(url);
  }

  $('searchButton').addEventListener('click', () => {
    const query = $('musicSearch').value;
    renderCatalog(query);
    const resultCount = tracks.filter(t => !query || `${t.title} ${t.genre} ${t.license}`.toLowerCase().includes(query.toLowerCase())).length;
    makeEvent('music_search', `Searched music for “${query || 'all local tracks'}”.`, {captured_records:[{query}], derived_records:[{result_count:resultCount}]});
  });
  $('musicSearch').addEventListener('input', e => renderCatalog(e.target.value));
  $('surpriseButton').addEventListener('click', () => selectTrack(Math.floor(Math.random()*tracks.length)));
  $('playPause').addEventListener('click', () => state.playing ? pauseAudio() : startAudio());
  $('stopButton').addEventListener('click', () => stopAudio(true));
  $('previousButton').addEventListener('click', () => selectTrack((state.trackIndex-1+tracks.length)%tracks.length));
  $('nextButton').addEventListener('click', () => selectTrack((state.trackIndex+1)%tracks.length));
  document.querySelectorAll('[data-feedback]').forEach(b => b.addEventListener('click', () => applyFeedback(b.dataset.feedback.replaceAll('-',' '))));
  $('applyFeedback').addEventListener('click', () => applyFeedback($('feedbackText').value));
  $('financeButton').addEventListener('click', () => { $('financePanel').hidden = !$('financePanel').hidden; renderFinance(); });
  $('exportButton').addEventListener('click', exportSession);
  $('saveProfile').addEventListener('click', saveProfile);
  $('revokeButton').addEventListener('click', revokeFutureReuse);
  $('resetButton').addEventListener('click', resetSession);
  ['permitStegDJ','permitAggregate','permitWellness'].forEach(id => $(id).addEventListener('change', updatePermissions));
  document.querySelectorAll('[data-view]').forEach(tab => tab.addEventListener('click', () => {
    document.querySelectorAll('[data-view]').forEach(t => t.classList.toggle('active', t===tab));
    document.querySelectorAll('.projection').forEach(v => v.classList.remove('active'));
    $(`${tab.dataset.view}View`).classList.add('active');
  }));

  $('profileName').value = state.profile.name;
  renderPermissions();
  selectTrack(0);
  renderEvents();
  renderFinance();
})();