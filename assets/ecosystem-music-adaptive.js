(() => {
  'use strict';

  const TRACKS = [
    {index:0,id:'stegdj-night-drive',title:'Night Drive Boundary',energy:58,brightness:34,bass:78,exploration:36,bpm:96},
    {index:1,id:'stegdj-low-orbit',title:'Low Orbit Relay',energy:42,brightness:24,bass:84,exploration:24,bpm:78},
    {index:2,id:'stegdj-signal-rise',title:'Signal Rise',energy:72,brightness:52,bass:66,exploration:58,bpm:112}
  ];
  const INTENT_TARGETS = {
    fine_tune:{energy:58,brightness:38,bass:72,exploration:34},
    stay_alert:{energy:76,brightness:50,bass:64,exploration:42},
    focus:{energy:54,brightness:30,bass:74,exploration:18},
    settle:{energy:34,brightness:22,bass:76,exploration:12},
    explore:{energy:62,brightness:48,bass:66,exploration:78}
  };
  const KEY = 'stegmusic.trait-model.v1';
  const $ = id => document.getElementById(id);
  const clamp = (n,min,max) => Math.max(min,Math.min(max,n));
  const parse = (value,fallback) => { try { return JSON.parse(value); } catch (_) { return fallback; } };
  let model = parse(localStorage.getItem(KEY), {version:1,observations:0,targets:{energy:58,brightness:38,bass:72,exploration:32},last_selection:null});

  function observedControls(){
    return {
      energy:Number($('energy').value),
      brightness:Number($('brightness').value),
      bass:Number($('bass').value),
      exploration:Number($('exploration').value)
    };
  }

  function updateModel(reason){
    const observed = observedControls();
    const intent = INTENT_TARGETS[$('sessionIntent').value] || INTENT_TARGETS.fine_tune;
    const weight = model.observations ? .28 : .55;
    for (const key of Object.keys(observed)) {
      const blended = observed[key] * .7 + intent[key] * .3;
      model.targets[key] = Math.round(clamp(model.targets[key] * (1-weight) + blended * weight,0,100));
    }
    model.observations += 1;
    model.updated_at = new Date().toISOString();
    model.last_reason = reason;
    localStorage.setItem(KEY, JSON.stringify(model));
    renderModel();
  }

  function score(track){
    const weights = {energy:1.2,brightness:.9,bass:1.1,exploration:1};
    let distance = 0;
    for (const key of Object.keys(weights)) distance += Math.abs(track[key]-model.targets[key]) * weights[key];
    const samePenalty = model.last_selection === track.id ? 12 : 0;
    return Math.max(0,100 - distance/3.2 - samePenalty);
  }

  function rank(){ return TRACKS.map(track=>({...track,score:score(track)})).sort((a,b)=>b.score-a.score); }

  function renderModel(){
    const target = $('adaptiveModel');
    if (!target) return;
    const ranked = rank();
    target.textContent = JSON.stringify({
      model_version:model.version,
      observations:model.observations,
      learned_targets:model.targets,
      current_intent:$('sessionIntent').value,
      ranked_candidates:ranked.map(x=>({track_id:x.id,title:x.title,score:Number(x.score.toFixed(2))})),
      local_only:true,
      authority:'none'
    }, null, 2);
    $('adaptiveRecommendation').textContent = ranked.length ? `Recommended next: ${ranked[0].title} · fit ${ranked[0].score.toFixed(1)}%` : 'No candidate available.';
  }

  function chooseAdaptive(){
    updateModel('adaptive_next_requested');
    const next = rank()[0];
    if (!next) return;
    model.last_selection = next.id;
    localStorage.setItem(KEY, JSON.stringify(model));
    const card = document.querySelector(`[data-track="${next.index}"]`);
    if (card) card.click();
    $('adaptiveRecommendation').textContent = `Selected ${next.title} because its energy, brightness, bass texture, and exploration distance best matched the persistent local model.`;
  }

  $('adaptiveNext').addEventListener('click', chooseAdaptive);
  $('sessionIntent').addEventListener('change', () => { updateModel('session_intent_changed'); renderModel(); });
  document.querySelectorAll('[data-feedback]').forEach(button => button.addEventListener('click', () => window.setTimeout(()=>updateModel(`feedback:${button.dataset.feedback}`),0)));
  $('applyFeedback').addEventListener('click', () => window.setTimeout(()=>updateModel('free_text_feedback'),0));
  ['energy','brightness','bass','exploration'].forEach(id => $(id).addEventListener('change',()=>updateModel(`control:${id}`)));
  $('resetAdaptiveModel').addEventListener('click', () => {
    model = {version:1,observations:0,targets:{energy:58,brightness:38,bass:72,exploration:32},last_selection:null,reset_at:new Date().toISOString()};
    localStorage.setItem(KEY, JSON.stringify(model));
    renderModel();
  });
  renderModel();
})();