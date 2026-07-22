(() => {
  'use strict';
  const MODEL_KEY='stegmusic.trait-model.v1';
  const TRANSITION_KEY='stegmusic.transition-model.v1';
  const defaults={
    [MODEL_KEY]:{version:3,observations:0,targets:{energy:58,brightness:38,bass:72,exploration:32},last_selection:null,last_transition:null},
    [TRANSITION_KEY]:{version:1,observations:0,pairs:{},last_outcome:null}
  };
  const validObject=value=>value&&typeof value==='object'&&!Array.isArray(value);
  for(const [key,fallback] of Object.entries(defaults)){
    let parsed=null;
    try{parsed=JSON.parse(localStorage.getItem(key));}catch(_){parsed=null;}
    if(!validObject(parsed)) localStorage.setItem(key,JSON.stringify(fallback));
  }
  window.StegMusicModelBootstrap=Object.freeze({model_key:MODEL_KEY,transition_key:TRANSITION_KEY,fail_safe_initialization:true,authority:'none'});
})();
