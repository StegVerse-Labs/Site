(()=>{
  'use strict';

  const form=document.getElementById('chatForm');
  const input=document.getElementById('messageInput');
  const log=document.getElementById('chatLog');
  const continuationSummary=document.getElementById('continuationSummary');
  const continuationGrid=document.getElementById('continuationGrid');
  const COMMAND_PATTERN=/^\/[a-z0-9_-]+(?:\s|$)/i;
  const STEGTALK_WIKI_URL='https://stegverse-labs.github.io/stegtalk-wiki/';
  const STEGTALK_WIKI_NAV_PATTERN=/\b(?:what(?:'s| is)?\s+(?:the\s+)?(?:url|link)|where\s+(?:is|can\s+i\s+find)|open|show|give\s+me)\b[^\n]{0,80}\bsteg\s*talk\b[^\n]{0,40}\bwiki\b|\bsteg\s*talk\b[^\n]{0,40}\bwiki\b[^\n]{0,80}\b(?:url|link)\b/i;

  if(!form||!input||!log)return;

  function resolve(value){
    if(!COMMAND_PATTERN.test(String(value||'').trim()))return null;
    if(!window.StegVerseSemanticCommands)return {recognized:false,unavailable:true,command:'unavailable'};
    return window.StegVerseSemanticCommands.resolve(value,'ECOSYSTEM_CHAT');
  }

  function resolveNavigation(value){
    const text=String(value||'').trim();
    if(!STEGTALK_WIKI_NAV_PATTERN.test(text))return null;
    return {
      recognized:true,
      intent:'STEGTALK_WIKI_NAVIGATION',
      answer:`StegTalk Wiki: ${STEGTALK_WIKI_URL}`,
      url:STEGTALK_WIKI_URL,
      canonical_source:'data/wiki-public-links.json',
      provider_call:false,
      model_execution:false,
      authority_effect:false,
      activation_effect:false
    };
  }

  function appendMessage(label,body,kind,receiptLine=''){
    const wrapper=document.createElement('div');
    wrapper.className=`chat-message ${kind}`;
    const labelNode=document.createElement('div');labelNode.className='label';labelNode.textContent=label;
    const bodyNode=document.createElement('div');bodyNode.className='body';bodyNode.textContent=body;
    wrapper.append(labelNode,bodyNode);
    if(receiptLine){const receipt=document.createElement('div');receipt.className='receipt-block';receipt.textContent=receiptLine;wrapper.appendChild(receipt)}
    log.appendChild(wrapper);log.scrollTop=log.scrollHeight;
  }

  function discoveryBoundary(result){
    if(!result||!result.recognized)return 'No intent inferred. Choose a known shorthand or continue in ordinary language.';
    return result.boundary;
  }

  function renderContinuation(result){
    if(!continuationSummary||!continuationGrid)return;
    continuationSummary.textContent=`Semantic discovery · commit_intent=false · ${discoveryBoundary(result)}`;
    continuationGrid.innerHTML='';
    if(!result||!result.recognized)return;
    result.topics.slice(0,8).forEach(topic=>{
      const card=document.createElement('div');card.className='continuation-item';
      const title=document.createElement('strong');title.textContent=topic;
      const summary=document.createElement('span');summary.textContent='Recognizable choice; selecting it narrows meaning without granting authority.';
      const button=document.createElement('button');button.className='sv-btn sv-btn-secondary';button.type='button';button.textContent='Use this topic';
      button.addEventListener('click',()=>{input.value=topic;input.focus();input.dispatchEvent(new Event('input',{bubbles:true}))});
      card.append(title,summary,button);continuationGrid.appendChild(card);
    });
  }

  function previewInput(event){
    const result=resolve(input.value);
    if(!result)return;
    event.stopImmediatePropagation();
    renderContinuation(result);
  }

  function submitCommand(event){
    const raw=input.value.trim();
    const navigation=resolveNavigation(raw);
    if(navigation){
      event.preventDefault();event.stopImmediatePropagation();
      appendMessage('User',raw,'user');input.value='';
      appendMessage('Navigation',navigation.answer,'system',`navigation_intent=${navigation.intent} · canonical_source=${navigation.canonical_source} · provider_call=false · model_execution=false · authority_effect=false · activation_effect=false`);
      return;
    }
    const result=resolve(raw);
    if(!result)return;
    event.preventDefault();event.stopImmediatePropagation();
    appendMessage('User',raw,'user');input.value='';
    if(result.unavailable){
      appendMessage('Semantic Discovery','Semantic shortcuts are unavailable. No intent was inferred and no action was taken.','system','semantic_command=unavailable · commit_intent=false · authority_effect=false · activation_effect=false · execution=not_attempted');
      renderContinuation(result);return;
    }
    const text=window.StegVerseSemanticCommands.renderText(result);
    appendMessage('Semantic Discovery',text,'system',`semantic_command=/${result.command} · recognized=${String(result.recognized)} · commit_intent=false · authority_effect=false · activation_effect=false · execution=not_attempted · provider_call=false`);
    renderContinuation(result);
  }

  input.addEventListener('input',previewInput,true);
  form.addEventListener('submit',submitCommand,true);

  window.StegVerseEcosystemSemanticCommands=Object.freeze({resolve,resolveNavigation,STEGTALK_WIKI_URL});
})();
