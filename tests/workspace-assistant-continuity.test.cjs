// MyKV assistant continuity / evidence / consent presentation (Site#1509 WS-ASSISTANT): the card presents only the
// user's existing MyKV assistant, derives continuity from a producer-supplied checkpoint keyed by (owner, assistant,
// workspace), shows evidence rows with their source, treats consent as a displayed record that can only be requested
// as a FAIL_CLOSED draft, fails closed when unauthenticated, and never invokes anything or falls back to a generic LLM.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const src=read('assets/workspace-assistant-continuity.js'),binding=read('assets/workspace-assistant-binding.js'),auth=read('assets/workspace-session-authentication.js'),caps=read('assets/workspace-capabilities.js'),ui=read('assets/workspace.js'),css=read('assets/workspace.css'),page=read('workspace.html'),workflow=read('.github/workflows/workspace-kv-binding-validation.yml');
const bootstrap=JSON.parse(read('data/workspace/bootstrap.json'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
const sb={};vm.createContext(sb);vm.runInContext(binding,sb);vm.runInContext(auth,sb);vm.runInContext(src,sb);
const A=sb.StegVerseWorkspaceAssistantContinuity,B=sb.StegVerseWorkspaceAssistantBinding,S=sb.StegVerseWorkspaceSessionAuthentication;
check(A.schema==='stegverse.workspace.assistant-continuity/v1'&&A.checkpoint_schema==='stegverse.kv.workspace-continuity-checkpoint/v1'&&A.authority_effect==='NONE'&&Object.isFrozen(A),'module identity');
const code=src.split('\n').filter(l=>!/^\s*\/\//.test(l)).join('\n');
check(!/fetch\(|XMLHttpRequest|localStorage|sessionStorage|indexedDB|invoke|completion|prompt\(|openai|anthropic/i.test(code),'contract performs no I/O, storage or invocation');
check((code.match(/"ALLOW"/g)||[]).length===3&&/generic_llm_fallback:"FORBIDDEN"/.test(src)&&/invocation_route:"NOT_AVAILABLE"/.test(src)&&/action_eligible:false/.test(src),'ALLOW only as session check, decision check and presentation disposition; no fallback or invocation');

// Fixtures shaped as the CVK projection/metadata and the Site session-authentication contract emit them.
const REV='a'.repeat(64);
const meta=(extra)=>Object.assign({schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-11T03:00:00Z',observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:REV,provenance_ref:'kv-workspace-source:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'},extra||{});
const assistant={principal_id:'auri:primary',principal_type:'AI_ENTITY',display_name:'Auri',roles:['WORKSPACE_ASSISTANT'],ai_label_required:true,authority_effect:'NONE'};
const projection=(extra)=>Object.assign({schema:'stegverse.kv.personal-workspace-projection/v1',state:'KV_WORKSPACE_PROJECTED',workspace_type:'PERSONAL',principals:[{principal_id:'user:owner',principal_type:'HUMAN',display_name:'Owner'}],organizations:[],memberships:[],feed:[],assistant:assistant,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,projection_metadata:meta(),authority_effect:'NONE'},extra||{});
const receipt=(pid)=>({authenticated:true,credential_authority:'TV/TVC',receipt_ref:'tv-tvc:session-receipt:test',principal_id:pid,authority_effect:'NONE'});
const session=(pid,ws)=>({principal_id:pid,workspace_id:ws===undefined?'ws:personal:owner':ws,source_class:'CALLER_AUTHENTICATION_RECEIPT',authentication:receipt(pid)});
const UNAUTH={principal_id:null,workspace_id:null,source_class:'NO_AUTHENTICATED_SESSION_PRINCIPAL',authentication:null};
const sa=(s)=>S.resolve(s);
const decide=(p,s)=>B.resolve(p,{principal_id:s.principal_id,workspace_type:'PERSONAL',workspace_id:s.workspace_id});
const checkpoint=(extra)=>Object.assign({schema:'stegverse.kv.workspace-continuity-checkpoint/v1',checkpoint_ref:'kv-workspace-continuity:sha256:'+'d'.repeat(64),key:{owner_principal_id:'user:owner',assistant_principal_id:'auri:primary',workspace_id:'ws:personal:owner'},observed_at:'2026-10-10T20:00:00Z',source_revision:'e'.repeat(64),replay_status:'REPLAY_STATUS_UNKNOWN',grant_state:'ACTIVE',revoked:false,consent:null,authority_effect:'NONE'},extra||{});
const run=(opts)=>{const s=opts.session||session('user:owner');const p=opts.projection||projection();return A.build({session_authentication:'sa' in opts?opts.sa:sa(s),decision:opts.decision===undefined?decide(p,s):opts.decision,checkpoint:opts.checkpoint});};
const nonAuth=(r)=>r.generic_llm_fallback==='FORBIDDEN'&&r.invocation_route==='NOT_AVAILABLE'&&r.ephemeral_inference==='NOT_AVAILABLE'&&r.action_eligible===false&&r.authority_effect==='NONE'&&r.schema===A.schema;

// 1. Unauthenticated session fails closed before any binding or checkpoint is consulted.
let r=run({session:UNAUTH,checkpoint:checkpoint()});
check(r.disposition==='FAIL_CLOSED'&&r.predicate==='SESSION_PRINCIPAL_UNAUTHENTICATED'&&r.identity===null&&r.continuity.state==='NOT_EVALUATED'&&r.consent.state==='WITHHELD'&&r.consent.proposable_actions.length===0&&nonAuth(r),'unauthenticated: '+JSON.stringify(r));
check(r.evidence.length===4&&r.evidence.every(e=>e.source==='SESSION_AUTHENTICATION')&&r.evidence.some(e=>e.label==='runtime authentication evidence'&&e.value==='false'),'unauthenticated evidence is session-only');
const trap=new Proxy({},{get(){throw new Error('checkpoint consulted')}});
r=A.build({session_authentication:sa(UNAUTH),decision:trap,checkpoint:trap});check(r.predicate==='SESSION_PRINCIPAL_UNAUTHENTICATED','unauthenticated must not touch decision or checkpoint');
for(const s of [{principal_id:'user:owner',workspace_id:'ws:personal:owner',source_class:'KV_PROJECTION_OWNER',authentication:null},{principal_id:'user:owner',workspace_id:'ws:personal:owner',source_class:'CALLER_AUTHENTICATION_RECEIPT',authentication:null}]){r=run({session:s,checkpoint:checkpoint()});check(r.disposition==='FAIL_CLOSED'&&r.identity===null&&/KV_OWNERSHIP_IS_NOT_AUTHENTICATION|SESSION_AUTHENTICATION_RECEIPT_ABSENT/.test(r.predicate),'non-receipt session must fail closed: '+r.predicate);}
r=run({sa:null});check(r.disposition==='FAIL_CLOSED'&&r.predicate==='SESSION_PRINCIPAL_UNAUTHENTICATED','absent session authentication fails closed');
r=run({decision:null});check(r.disposition==='FAIL_CLOSED'&&r.predicate==='ASSISTANT_BINDING_DECISION_UNAVAILABLE'&&r.identity===null,'absent binding decision fails closed');
r=run({decision:{schema:'other/v1',disposition:'ALLOW',binding:{assistant_principal_id:'x'}}});check(r.disposition==='FAIL_CLOSED'&&r.predicate==='ASSISTANT_BINDING_DECISION_UNAVAILABLE','foreign decision schema fails closed');

// 2. Same assistant identity: bound without a checkpoint -> continuity unknown, never asserted; matching checkpoint -> continuous.
r=run({});
check(r.disposition==='ALLOW'&&r.predicate==='MYKV_ASSISTANT_CONTINUITY_PRESENTED'&&r.identity.assistant_principal_id==='auri:primary'&&r.identity.assistant_display_name==='Auri'&&r.identity.ai_label_required===true&&r.identity.owner_principal_id==='user:owner'&&r.identity.same_assistant_as_checkpoint===null&&nonAuth(r),'bound without checkpoint: '+JSON.stringify(r).slice(0,300));
check(r.continuity.state==='CONTINUITY_UNKNOWN'&&r.continuity.predicate==='CHECKPOINT_NOT_OBSERVED'&&r.continuity.checkpoint_ref===null&&r.continuity.key.assistant_principal_id==='auri:primary'&&r.continuity.key.owner_principal_id==='user:owner'&&r.continuity.key.workspace_id==='ws:personal:owner'&&r.continuity.source_revision===REV&&r.continuity.provenance_ref==='kv-workspace-source:sha256:'+REV&&r.continuity.replay_status==='REPLAY_STATUS_UNKNOWN','continuity unknown without checkpoint: '+JSON.stringify(r.continuity));
check(r.consent.state==='NOT_SUPPLIED'&&r.consent.predicate==='CONSENT_RECORD_NOT_OBSERVED'&&r.consent.proposable_actions.join()==='ASSISTANT_CONSENT_GRANT','consent not supplied without checkpoint');
const srcs=new Set(r.evidence.map(e=>e.source));check(['SESSION_AUTHENTICATION','BINDING_DECISION','KV_PROJECTION_METADATA','CONTINUITY_CHECKPOINT'].every(x=>srcs.has(x))&&r.evidence.some(e=>e.label==='provenance'&&e.value==='kv-workspace-source:sha256:'+REV)&&r.evidence.some(e=>e.label==='invocation route'&&e.value==='NOT_AVAILABLE')&&r.evidence.some(e=>e.label==='generic LLM fallback'&&e.value==='FORBIDDEN'),'evidence rows carry source and provenance: '+JSON.stringify(r.evidence));
const frozenCp=checkpoint();const before=JSON.stringify(frozenCp);
r=run({checkpoint:frozenCp});
check(JSON.stringify(frozenCp)===before,'checkpoint not mutated');
check(r.disposition==='ALLOW'&&r.continuity.state==='CONTINUOUS_SAME_ASSISTANT'&&r.continuity.predicate==='CHECKPOINT_KEY_MATCHES_BINDING'&&r.identity.same_assistant_as_checkpoint===true&&r.continuity.checkpoint_ref===frozenCp.checkpoint_ref&&r.continuity.checkpoint_observed_at==='2026-10-10T20:00:00Z'&&r.evidence.some(e=>e.source==='CONTINUITY_CHECKPOINT'&&e.label==='checkpoint'&&e.value===frozenCp.checkpoint_ref),'matching checkpoint is continuous: '+JSON.stringify(r.continuity));
check(r.consent.state==='NOT_SUPPLIED'&&r.consent.predicate==='CONSENT_RECORD_ABSENT_FROM_CHECKPOINT','checkpoint without consent record');
r=run({checkpoint:checkpoint({replay_status:'REPLAYED_FROM_CHECKPOINT'})});check(r.continuity.replay_status==='REPLAYED_FROM_CHECKPOINT','replay status is producer-supplied');
// Null workspace on both sides is the same key; a workspace on one side only is not.
r=run({session:session('user:owner',null),projection:projection({projection_metadata:meta({workspace_id:null})}),checkpoint:checkpoint({key:{owner_principal_id:'user:owner',assistant_principal_id:'auri:primary',workspace_id:null}})});check(r.continuity.state==='CONTINUOUS_SAME_ASSISTANT','null workspace on both sides');
r=run({checkpoint:checkpoint({key:{owner_principal_id:'user:owner',assistant_principal_id:'auri:primary',workspace_id:null}})});check(r.disposition==='FAIL_CLOSED'&&r.predicate==='CHECKPOINT_WORKSPACE_MISMATCH'&&r.identity===null,'workspace mismatch fails closed');
// A checkpoint for another assistant is never adopted: identity withheld, no draft, no "same assistant".
r=run({checkpoint:checkpoint({key:{owner_principal_id:'user:owner',assistant_principal_id:'ai:other',workspace_id:'ws:personal:owner'}})});
check(r.disposition==='FAIL_CLOSED'&&r.predicate==='ASSISTANT_IDENTITY_CHANGED'&&r.identity===null&&r.continuity.state==='IDENTITY_CHANGED'&&r.consent.proposable_actions.length===0&&r.evidence.some(e=>e.label==='checkpoint assistant'&&e.value==='ai:other')&&nonAuth(r),'different assistant in checkpoint: '+JSON.stringify(r).slice(0,300));
r=run({checkpoint:checkpoint({key:{owner_principal_id:'user:other',assistant_principal_id:'auri:primary',workspace_id:'ws:personal:owner'}})});check(r.disposition==='FAIL_CLOSED'&&r.predicate==='CHECKPOINT_OWNER_MISMATCH'&&r.identity===null,'owner mismatch fails closed');
for(const [cp,pred] of [[{schema:'other/v1'},'CHECKPOINT_SCHEMA_INVALID'],['junk','CHECKPOINT_SCHEMA_INVALID'],[checkpoint({authority_effect:'ALLOW'}),'CHECKPOINT_AUTHORITY_INVALID'],[checkpoint({key:'x'}),'CHECKPOINT_KEY_ABSENT']]){r=run({checkpoint:cp});check(r.disposition==='FAIL_CLOSED'&&r.predicate===pred&&r.identity===null&&r.continuity.state==='MALFORMED','malformed checkpoint '+pred+': got '+r.predicate);}
// A checkpoint claiming an invocation route or ephemeral inference changes nothing.
r=run({checkpoint:checkpoint({invocation_route:'https://example.invalid/llm',ephemeral_inference:'GRANTED'})});check(r.disposition==='ALLOW'&&r.invocation_route==='NOT_AVAILABLE'&&r.ephemeral_inference==='NOT_AVAILABLE'&&JSON.stringify(r).indexOf('example.invalid')<0,'checkpoint cannot supply an invocation route');

// 3. Revocation: projection grant revoked (binding DENY), checkpoint revoked, consent revoked.
r=run({projection:projection({projection_metadata:meta({grant_state:'REVOKED'})}),checkpoint:checkpoint()});
check(r.disposition==='DENY'&&r.predicate==='WORKSPACE_GRANT_REVOKED'&&r.identity===null&&r.continuity.state==='REVOKED'&&r.consent.state==='REVOKED'&&r.consent.proposable_actions.length===0&&r.evidence.some(e=>e.source==='BINDING_DECISION'&&/DENY · WORKSPACE_GRANT_REVOKED/.test(e.value)),'projection grant revoked: '+JSON.stringify(r).slice(0,300));
for(const cp of [checkpoint({revoked:true}),checkpoint({grant_state:'REVOKED'})]){r=run({checkpoint:cp});check(r.disposition==='DENY'&&r.predicate==='CONTINUITY_REVOKED'&&r.identity===null&&r.continuity.state==='REVOKED'&&r.consent.state==='REVOKED'&&r.consent.proposable_actions.length===0&&r.evidence.some(e=>e.label==='grant state'&&e.value==='REVOKED'&&e.source==='CONTINUITY_CHECKPOINT'),'checkpoint revocation denies: '+JSON.stringify(r).slice(0,200));}
r=run({checkpoint:checkpoint({consent:{state:'REVOKED',consent_ref:'consent:1',recorded_by:'user:owner'}})});
check(r.disposition==='ALLOW'&&r.consent.state==='REVOKED'&&r.consent.predicate==='CONSENT_RECORD_REVOKED'&&r.consent.proposable_actions.length===0&&r.consent.consent_ref==='consent:1','consent revoked: no action may be proposed');
r=run({projection:projection(),session:session('user:other')});check(r.disposition==='DENY'&&r.predicate==='PROJECTION_OWNER_MISMATCH'&&r.identity===null&&r.continuity.state==='WITHHELD','other user denied');
r=run({projection:projection({assistant:null})});check(r.disposition==='FAIL_CLOSED'&&r.predicate==='MYKV_ASSISTANT_BINDING_ABSENT'&&r.identity===null,'absent assistant');

// 4. Consent record states and malformed consent.
r=run({checkpoint:checkpoint({consent:{state:'GRANTED',consent_ref:'consent:2',scope:['PRESENT_CONTINUITY','PRESENT_EVIDENCE'],granted_at:'2026-10-10T20:00:00Z',recorded_by:'user:owner'}})});
check(r.consent.state==='GRANTED'&&r.consent.scope.join()==='PRESENT_CONTINUITY,PRESENT_EVIDENCE'&&r.consent.consent_ref==='consent:2'&&r.consent.granted_at==='2026-10-10T20:00:00Z'&&r.consent.proposable_actions.join()==='ASSISTANT_CONSENT_WITHDRAW'&&r.invocation_route==='NOT_AVAILABLE'&&r.action_eligible===false,'granted consent is displayed and only withdrawal can be proposed; still no invocation');
for(const c of [{state:'GRANTED'},{state:'GRANTED',consent_ref:'x',scope:'all'},{state:'GRANTED',consent_ref:'x',scope:[1]},{state:'YES'},'granted']){r=run({checkpoint:checkpoint({consent:c})});check(r.disposition==='ALLOW'&&r.consent.state==='MALFORMED'&&r.consent.proposable_actions.length===0&&/CONSENT_RECORD_INVALID|CONSENT_GRANT_UNREFERENCED/.test(r.consent.predicate),'malformed consent withheld: '+JSON.stringify(c));}
r=run({checkpoint:checkpoint({consent:{state:'NOT_SUPPLIED'}})});check(r.consent.state==='NOT_SUPPLIED'&&r.consent.predicate==='CONSENT_RECORD_NOT_SUPPLIED'&&r.consent.proposable_actions.join()==='ASSISTANT_CONSENT_GRANT','explicit not supplied');

// 5. Page integration: script order, workflow, seam, CSS, no storage.
check(page.indexOf('assets/workspace-assistant-binding.js')<page.indexOf('assets/workspace-assistant-continuity.js')&&page.indexOf('assets/workspace-assistant-continuity.js')<page.indexOf('assets/workspace.js'),'continuity script loads after the binding resolver and before the page script');
check(workflow.includes('assets/workspace-assistant-continuity.js')&&workflow.includes('tests/workspace-assistant-continuity.test.cjs')&&workflow.includes('node --check assets/workspace-assistant-continuity.js')&&workflow.includes('node tests/workspace-assistant-continuity.test.cjs'),'workflow validates and runs the continuity contract');
check(ui.includes('typeof bridge.loadAssistantCheckpoint!=="function"')&&ui.includes('state.assistantCheckpoint=undefined')&&ui.includes('ASSISTANT_CONTINUITY_CONTRACT_UNAVAILABLE'),'checkpoint only through the bridge seam; absent contract named');
check(!/localStorage|sessionStorage|indexedDB/.test(ui)&&!/localStorage|sessionStorage|indexedDB/.test(src),'no browser storage');
check(/\.evidence-row\{[^}]*min-width:0[^}]*overflow-wrap:anywhere[^}]*\}/.test(css),'evidence rows wrap at phone widths');
check(/@media\(max-width:800px\)\{[^@]*\.card button,\.assistant button\{min-height:44px\}/.test(css),'draft buttons keep a 44px tap height on phones');

// 6. UI harness.
const SESSION_LITERAL='session:{principal_id:null,workspace_id:null,source_class:"NO_AUTHENTICATED_SESSION_PRINCIPAL",authentication:null}';
check(ui.includes(SESSION_LITERAL),'page must not invent a session principal');
const live=(p)=>{p.projection_metadata.observed_at=new Date(Date.now()-60000).toISOString().replace(/\.\d{3}Z$/,'Z');return p;};
const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities','searchResults','tasks'];
function harness(opts){const els={};ids.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
  const docListeners={};const bridge=Object.assign({loadPersonalWorkspace:()=>Promise.resolve(live(opts.projection||projection())),lastNodeBinding:()=>null},opts.bridge||{});
  const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener:(t,f)=>{docListeners[t]=f}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{StegVerseWorkspaceKVBridge:bridge}};
  vm.createContext(ctx);for(const s of [caps,auth,binding])vm.runInContext(s,ctx);if(opts.contract!==false)vm.runInContext(src,ctx);
  ['StegVerseWorkspaceCapabilities','StegVerseWorkspaceSessionAuthentication','StegVerseWorkspaceAssistantBinding','StegVerseWorkspaceAssistantContinuity'].forEach(k=>{if(ctx[k])ctx.window[k]=ctx[k];});
  vm.runInContext(opts.session?ui.replace(SESSION_LITERAL,'session:'+JSON.stringify(opts.session)):ui,ctx);
  const click=(attrs)=>docListeners.click({target:{closest:sel=>sel==='[data-assistant-action]'&&attrs.assistantAction?{dataset:attrs}:null}});
  return {els,click,switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}})};}
(async()=>{
  const wait=()=>new Promise(r=>setTimeout(r,10));
  // Unauthenticated page (the shipped state): no continuity, consent or evidence rows; no buttons; checkpoint delivery ignored.
  let h=harness({bridge:{loadAssistantCheckpoint:()=>Promise.resolve(checkpoint())}});await wait();let html=h.els.assistant.innerHTML;
  check(html.includes('SESSION_PRINCIPAL_UNAUTHENTICATED')&&!html.includes('Continuity:')&&!html.includes('Consent:')&&!html.includes('class="evidence"')&&!html.includes('data-assistant-action'),'unauthenticated card shows no continuity/consent: '+html.slice(0,300));
  h.click({assistantAction:'grant'});check(h.els.intentDraft.innerHTML==='','no consent draft while unauthenticated');
  // Authenticated (test injection only), no checkpoint seam: continuity unknown, consent not supplied, grant draft only.
  h=harness({session:session('user:owner')});await wait();html=h.els.assistant.innerHTML;
  check(html.includes('Bound to this session')&&html.includes('Auri')&&html.includes('Continuity: <span class="pill warn">CONTINUITY_UNKNOWN</span> CHECKPOINT_NOT_OBSERVED')&&html.includes('Consent: <span class="pill warn">NOT_SUPPLIED</span> CONSENT_RECORD_NOT_OBSERVED')&&html.includes('class="evidence"')&&html.includes('<strong>provenance</strong> kv-workspace-source:sha256:'+REV)&&html.includes('data-assistant-action="grant"')&&!html.includes('data-assistant-action="withdraw"')&&html.includes('action_eligible: false'),'bound card without checkpoint: '+html.slice(0,900));
  check(!/https?:\/\//.test(html)&&html.includes('invocation route</strong> NOT_AVAILABLE')&&html.includes('generic LLM fallback</strong> FORBIDDEN'),'card never shows an invocation route');
  h.click({assistantAction:'grant'});let draft=h.els.intentDraft.innerHTML;
  check(draft.includes('ASSISTANT_CONSENT_GRANT request draft')&&draft.includes('FAIL_CLOSED')&&draft.includes('WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND')&&draft.includes('&quot;submitted&quot;: false')&&draft.includes('&quot;manifest_admitted&quot;: false')&&draft.includes('&quot;target_assistant_principal_id&quot;: &quot;auri:primary&quot;')&&draft.includes('&quot;consent_state_at_draft&quot;: &quot;NOT_SUPPLIED&quot;')&&draft.includes('&quot;invocation_route&quot;: &quot;NOT_AVAILABLE&quot;')&&draft.includes('kv-workspace-source:sha256:'+REV),'consent draft: '+draft.slice(0,600));
  check(!/granted successfully|consent recorded|ALLOW&quot;/i.test(draft),'draft must not claim consent');
  h.els.intentDraft.innerHTML='';h.click({assistantAction:'withdraw'});check(h.els.intentDraft.innerHTML==='','withdrawal cannot be proposed when nothing is granted');
  check(h.els.assistant.innerHTML.includes('CONSENT_RECORD_NOT_OBSERVED'),'consent state unchanged after drafting');
  // Matching checkpoint with granted consent: continuous, withdrawal draft only.
  h=harness({session:session('user:owner'),bridge:{loadAssistantCheckpoint:()=>Promise.resolve(checkpoint({consent:{state:'GRANTED',consent_ref:'consent:2',scope:['PRESENT_CONTINUITY'],granted_at:'2026-10-10T20:00:00Z',recorded_by:'user:owner'}}))}});await wait();html=h.els.assistant.innerHTML;
  check(html.includes('<span class="pill ok">CONTINUOUS_SAME_ASSISTANT</span> CHECKPOINT_KEY_MATCHES_BINDING')&&html.includes('checkpoint kv-workspace-continuity:sha256:')&&html.includes('<span class="pill ok">GRANTED</span> CONSENT_RECORD_OBSERVED · scope PRESENT_CONTINUITY · ref consent:2')&&html.includes('data-assistant-action="withdraw"')&&!html.includes('data-assistant-action="grant"'),'continuous card: '+html.slice(0,900));
  h.click({assistantAction:'withdraw'});draft=h.els.intentDraft.innerHTML;check(draft.includes('ASSISTANT_CONSENT_WITHDRAW')&&draft.includes('&quot;consent_ref&quot;: &quot;consent:2&quot;')&&draft.includes('&quot;checkpoint_ref&quot;: &quot;kv-workspace-continuity:sha256:')&&draft.includes('FAIL_CLOSED'),'withdrawal draft: '+draft.slice(0,500));
  h.switchTo('organizational');html=h.els.assistant.innerHTML;check(html.includes('ORG_KV_ASSISTANT_CONTEXT_NOT_OBSERVED')&&!html.includes('CONTINUOUS_SAME_ASSISTANT')&&!html.includes('data-assistant-action'),'org context drops continuity and consent: '+html.slice(0,400));
  h.els.intentDraft.innerHTML='';h.click({assistantAction:'withdraw'});check(h.els.intentDraft.innerHTML==='','no consent draft from org context');
  // Checkpoint for a different assistant: identity withheld; the card must not call the assistant the same one.
  h=harness({session:session('user:owner'),bridge:{loadAssistantCheckpoint:()=>Promise.resolve(checkpoint({key:{owner_principal_id:'user:owner',assistant_principal_id:'ai:other',workspace_id:'ws:personal:owner'}}))}});await wait();html=h.els.assistant.innerHTML;
  check(html.includes('ASSISTANT_IDENTITY_CHANGED')&&html.includes('<span class="pill warn">IDENTITY_CHANGED</span>')&&!html.includes('CONTINUOUS_SAME_ASSISTANT')&&!html.includes('data-assistant-action'),'changed identity fails closed in the card: '+html.slice(0,600));
  h.click({assistantAction:'grant'});check(h.els.intentDraft.innerHTML==='','no draft when identity changed');
  // Revoked checkpoint and revoked consent.
  h=harness({session:session('user:owner'),bridge:{loadAssistantCheckpoint:()=>Promise.resolve(checkpoint({revoked:true}))}});await wait();html=h.els.assistant.innerHTML;
  check(html.includes('CONTINUITY_REVOKED')&&html.includes('<span class="pill warn">REVOKED</span>')&&!html.includes('data-assistant-action')&&html.includes('Consent revoked: no action may be proposed'),'revoked checkpoint: '+html.slice(0,600));
  h=harness({session:session('user:owner'),projection:projection({projection_metadata:meta({grant_state:'REVOKED'})}),bridge:{loadAssistantCheckpoint:()=>Promise.resolve(checkpoint())}});await wait();html=h.els.assistant.innerHTML;
  check(html.includes('DENY')&&html.includes('WORKSPACE_GRANT_REVOKED')&&!html.includes('Bound to this session')&&!html.includes('data-assistant-action'),'revoked projection grant: '+html.slice(0,400));
  // Seam rejecting or delivering garbage: continuity unknown or malformed; never continuous.
  h=harness({session:session('user:owner'),bridge:{loadAssistantCheckpoint:()=>Promise.reject(new Error('no'))}});await wait();check(h.els.assistant.innerHTML.includes('CHECKPOINT_NOT_OBSERVED'),'rejecting seam -> not observed');
  h=harness({session:session('user:owner'),bridge:{loadAssistantCheckpoint:()=>Promise.resolve('junk')}});await wait();html=h.els.assistant.innerHTML;check(html.includes('CHECKPOINT_SCHEMA_INVALID')&&html.includes('MALFORMED')&&!html.includes('data-assistant-action'),'garbage checkpoint -> malformed: '+html.slice(0,400));
  // Contract not loaded: nothing continuity-related is presented, no buttons.
  h=harness({session:session('user:owner'),contract:false,bridge:{loadAssistantCheckpoint:()=>Promise.resolve(checkpoint())}});await wait();html=h.els.assistant.innerHTML;check(html.includes('ASSISTANT_CONTINUITY_CONTRACT_UNAVAILABLE')&&!html.includes('Continuity:')&&!html.includes('data-assistant-action'),'absent contract falls back: '+html.slice(0,400));
  console.log('WORKSPACE_ASSISTANT_CONTINUITY_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
