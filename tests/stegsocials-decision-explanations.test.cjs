// StegSocials preparation refusals carry a plain-language reason and a portable explanation
// (StegVerse-Labs/.github#3106 universal explanation contract, compatibility requirements 7-9).
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const src=f=>fs.readFileSync(path.join(root,f),'utf8');
let n=0;function check(ok,msg){n++;if(!ok)throw new Error(msg);}
function load(files,extra){const ctx=Object.assign({},extra||{});ctx.globalThis=ctx;ctx.window=ctx;vm.createContext(ctx);for(const f of files)vm.runInContext(src(f),ctx,{filename:f});return ctx;}
const ctx=load(['assets/workspace-explanation.js','assets/stegsocials-decision-reasons.js']);
const E=ctx.StegVerseWorkspaceExplanation,R=ctx.StegVerseStegSocialsDecisionReasons;
const TOKEN=/\b[A-Z]{2,}(?:_[A-Z0-9]+)+\b/;
check(Object.isFrozen(R)&&Object.isFrozen(R.reasons)&&R.predicates.length===6,'reasons exported and frozen');
for(const [p,r] of Object.entries(R.reasons)){
  check(typeof r==='string'&&r.trim()===r&&r.length>20&&!TOKEN.test(r)&&/^[a-z]/.test(r)&&!r.endsWith('.'),'reason is plain language: '+p);
  const rec=R.explanationRecord(p);
  check(rec&&rec.predicate===p&&rec.why===r&&rec.consequence_observation==='NOT_AUTHENTICALLY_OBSERVED'&&['DENY','FAIL_CLOSED'].includes(rec.disposition),'record copies the decision: '+p);
  check(JSON.stringify(Object.keys(rec).sort())===JSON.stringify(['authority_source','consequence_observation','disposition','predicate','requested_action','safe_next_steps','why']),'record carries no draft content: '+p);
  const a=E.build(rec,{repository:'StegVerse-Labs/Site',surface_id:'stegsocials-prepare'});
  check(a&&E.conforms(a).ok===true&&a.prose.why==='Because '+r+'.'&&a.execution.executed===false&&a.authorization.authorized===false&&a.authority.authority_effect==='NONE','record builds a conformant non-authorizing explanation: '+p);
  check(JSON.stringify(a.prose.what_you_can_safely_do_next)===JSON.stringify(rec.safe_next_steps),'surface next steps are carried: '+p);
}
check(R.explanationRecord('NOT_A_STEGSOCIALS_PREDICATE')===null,'unknown predicate yields no record');
check(R.reasons.STEGSOCIALS_PREPARATION_REFUSED&&R.explanationRecord('STEGSOCIALS_PREPARATION_REFUSED').disposition==='DENY','input refusal is DENY, not FAIL_CLOSED');
// Source coverage both ways: every predicate the page can return has a reason, and every reason is reachable.
const page=src('stegsocials-prepare.html');
const used=new Set([...page.matchAll(/refuse\("([A-Z0-9_]+)"/g)].map(m=>m[1]));
for(const p of used)check(p in R.reasons,'page predicate has a reason: '+p);
for(const p of R.predicates)check(used.has(p),'reason is reachable from the page: '+p);
check(!/status\.textContent=e\.message/.test(page)&&!/status\.textContent=error&&error\.message/.test(page),'no refusal shows only a raw technical message');
check(page.indexOf('assets/workspace-explanation.js')<page.indexOf('assets/stegsocials-decision-reasons.js')&&page.indexOf('assets/stegsocials-decision-reasons.js')<page.indexOf('<script>\n(function(){'),'explanation modules load before the page script');
// Drive the real inline page script with a minimal DOM: an empty draft is refused with the reason first, the
// technical message after it, and copyable JSON that never contains the user's draft text.
const inline=page.slice(page.indexOf('<script>\n(function(){')+'<script>'.length,page.lastIndexOf('</script>'));
const els={};
function el(id){return els[id]||(els[id]={id,value:'',textContent:'',className:'',hidden:id==='explanation'||id==='preview-panel',open:false,disabled:false,listeners:{},addEventListener(t,f){this.listeners[t]=f;}});}
let clip=null;
const dom={document:{getElementById:el},location:{search:'?platform=linkedin'},URLSearchParams,navigator:{clipboard:{writeText(t){clip=t;return Promise.resolve();}}},JSON,Promise,Date};
const page_ctx=load(['assets/stegsocials-post-preparation.js','assets/workspace-explanation.js','assets/stegsocials-decision-reasons.js'],dom);
vm.runInContext(inline,page_ctx,{filename:'stegsocials-prepare.html#inline'});
el('erl-ref').value='02_Research/ERL/example.md';el('body').value='   ';
el('prepare').listeners.click();
check(el('status').className==='status error','refusal is shown as an error');
check(el('status').textContent.startsWith('Because '+R.reasons.STEGSOCIALS_PREPARATION_REFUSED+'.')&&/ Detail: \S/.test(el('status').textContent),'reason first, technical message after: '+el('status').textContent);
check(el('explanation').hidden===false&&el('explanation-prose').textContent.includes('What happened:')&&el('explanation-prose').textContent.includes('Why: Because '),'prose explanation is shown');
el('body').value='A private draft sentence that must stay on the page';el('erl-ref').value='outside/lane.md';
el('prepare').listeners.click();
el('copy-explanation').listeners.click();
check(typeof clip==='string'&&!clip.includes('private draft sentence')&&E.conforms(JSON.parse(clip)).ok===true,'copied explanation JSON conforms and carries no draft text');
el('erl-ref').value='02_Research/ERL/example.md';el('prepare').listeners.click();
check(el('explanation').hidden===true&&el('status').className==='status','a successful preparation clears the explanation');
el('save-kv').listeners.click();
check(el('status').textContent.startsWith('Because '+R.reasons.STEGSOCIALS_KV_COMPONENT_UNAVAILABLE+'.')&&el('explanation').hidden===false,'missing KV writer is explained');
// An assisted draft that then breaks a preparation rule is a preparation refusal, not an unverified ERL read.
page_ctx.StegVerseStegSocialsERLDraftAssistant={assist:()=>Promise.resolve({body:'',hashtags:[],source_url:null})};
vm.runInContext(inline,page_ctx,{filename:'stegsocials-prepare.html#inline-2'});
el('erl-ref').value='02_Research/ERL/example.md';
el('assist').listeners.click();
setImmediate(()=>{
check(el('status').textContent.startsWith('Because '+R.reasons.STEGSOCIALS_PREPARATION_REFUSED+'.')&&el('assist').disabled===false,'assisted draft failing a rule is a preparation refusal: '+el('status').textContent);
console.log('PASS stegsocials decision explanations ('+n+' checks)');
});
