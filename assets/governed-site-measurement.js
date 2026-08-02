(()=>{
  'use strict';
  const PAGE='va-disability-claim-guide';
  const POLICY_VERSION='1.0.0';
  const ENDPOINT='/api/governed-measurement';
  const allowed={
    guide_opened:[],walkthrough_started:[],assistant_opened:[],assistant_question_submitted:[],
    quick_question_selected:['choice'],phase_reached:['phase'],official_source_opened:['destination_class'],
    claim_form_opened:[],status_page_opened:[],guide_completed:[],client_error:['error_class']
  };
  function emit(event,detail={}){
    if(!Object.prototype.hasOwnProperty.call(allowed,event)) return false;
    const payload={event,page:PAGE,policy_version:POLICY_VERSION,content_recorded:false};
    for(const key of allowed[event]) if(Object.prototype.hasOwnProperty.call(detail,key)) payload[key]=detail[key];
    const body=JSON.stringify(payload);
    if(navigator.sendBeacon){
      return navigator.sendBeacon(ENDPOINT,new Blob([body],{type:'application/json'}));
    }
    fetch(ENDPOINT,{method:'POST',headers:{'content-type':'application/json'},body,credentials:'omit',cache:'no-store',keepalive:true}).catch(()=>{});
    return true;
  }
  window.StegVerseGovernedMeasurement=Object.freeze({emit});
  emit('guide_opened');
  document.addEventListener('click',e=>{
    const el=e.target.closest('a,button'); if(!el) return;
    const href=el.getAttribute('href')||'';
    if(href==='#phase-1') emit('walkthrough_started');
    if(href==='#assistant') emit('assistant_opened');
    if(el.id==='va-send') emit('assistant_question_submitted');
    if(el.dataset.q){
      const label=(el.textContent||'').trim().toLowerCase();
      const choices={
        'blue button report':'blue_button','secondary claim':'secondary_claim',
        'intent to file':'intent_to_file','get human help':'human_help'
      };
      if(choices[label]) emit('quick_question_selected',{choice:choices[label]});
    }
    if(href.includes('file-disability-claim-form-21-526ez')) emit('claim_form_opened');
    else if(href.includes('claim-or-appeal-status')) emit('status_page_opened');
    else if(href.startsWith('https://www.va.gov')||href.startsWith('https://www.benefits.va.gov')) emit('official_source_opened',{destination_class:'official_va_source'});
    else if(href.startsWith('https://help.openai.com')) emit('official_source_opened',{destination_class:'openai_help'});
  });
  const seen=new Set();
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(!entry.isIntersecting) return;
    const heading=entry.target.querySelector('h2');
    const match=heading&&heading.textContent.match(/Phase\s+(\d+)/i);
    if(match&&!seen.has(match[1])){seen.add(match[1]);emit('phase_reached',{phase:Number(match[1])});}
  }),{threshold:.35});
  document.querySelectorAll('section.phase').forEach(section=>observer.observe(section));
  let completed=false;
  addEventListener('scroll',()=>{
    if(!completed&&innerHeight+scrollY>=document.documentElement.scrollHeight-40){completed=true;emit('guide_completed');}
  },{passive:true});
})();
