// MyKV assistant binding consumer contract (Site#1509 W4): the browser port must decide exactly as
// continuity-vault-kit runtime/workspace_assistant_binding.py, and the AI card renders the assistant as bound
// only on ALLOW, with no generic-LLM fallback and no identity taken from browser storage.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const src=fs.readFileSync(path.join(root,'assets/workspace-assistant-binding.js'),'utf8');
const caps=fs.readFileSync(path.join(root,'assets/workspace-capabilities.js'),'utf8');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
const page=fs.readFileSync(path.join(root,'workspace.html'),'utf8');
const bootstrap=JSON.parse(fs.readFileSync(path.join(root,'data/workspace/bootstrap.json'),'utf8'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
const sandbox={};vm.createContext(sandbox);vm.runInContext(src,sandbox);
const B=sandbox.StegVerseWorkspaceAssistantBinding;
assert(B.schema==='stegverse.kv.workspace-assistant-binding/v1'&&B.authority_effect==='NONE','module identity');
assert(page.includes('assets/workspace-assistant-binding.js'),'page must load the binding resolver');
for(const s of [src,ui])assert(!/localStorage|sessionStorage|indexedDB/.test(s),'identity must never come from browser storage');

// Projection shaped exactly as continuity-vault-kit runtime/workspace_projection.py emits it.
const REV='a'.repeat(64);
const meta=(extra)=>Object.assign({schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-10T12:00:00Z',observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',
  source_revision:REV,provenance_ref:'kv-workspace-source:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',
  grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'},extra||{});
const assistant={principal_id:'auri:primary',principal_type:'AI_ENTITY',display_name:'Auri',roles:['WORKSPACE_ASSISTANT'],ai_label_required:true,authority_effect:'NONE'};
function projection(extra){return Object.assign({schema:'stegverse.kv.personal-workspace-projection/v1',state:'KV_WORKSPACE_PROJECTED',workspace_type:'PERSONAL',
  workspace:{schema:'stegverse.kv.workspace-context/v1',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',authority_effect:'NONE'},
  principals:[{principal_id:'user:owner',principal_type:'HUMAN',display_name:'Owner',ai_label_required:false,authority_effect:'NONE'}],relationships:[],organizations:[],memberships:[],feed:[],
  assistant:assistant,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,projection_metadata:meta(),authority_effect:'NONE'},extra||{});}
const CTX={principal_id:'user:owner',workspace_type:'PERSONAL',workspace_id:'ws:personal:owner'};
const r=(p,ctx)=>B.resolve(p,Object.assign({},CTX,ctx||{}));

// ALLOW is display-only and keyed by (owner, assistant, workspace).
const ok=r(projection());
assert(ok.disposition==='ALLOW'&&ok.predicate==='MYKV_ASSISTANT_BOUND','bound');
assert(ok.action_eligible===false&&ok.authority_effect==='NONE'&&ok.generic_llm_fallback==='FORBIDDEN','ALLOW must stay display-only');
assert(ok.binding.assistant_principal_id==='auri:primary'&&ok.binding.owner_principal_id==='user:owner'&&ok.binding.ai_label_required===true,'binding identity');
assert(JSON.stringify(ok.binding.continuity.key)===JSON.stringify({owner_principal_id:'user:owner',assistant_principal_id:'auri:primary',workspace_id:'ws:personal:owner'}),'continuity key');
assert(ok.binding.continuity.replay_status==='UNKNOWN'&&ok.binding.continuity.source_revision===REV&&ok.binding.continuity.checkpoint_schema==='stegverse.kv.workspace-continuity-checkpoint/v1','continuity provenance');
assert(ok.binding.invocation_route==='NOT_AVAILABLE'&&ok.binding.ephemeral_inference==='NOT_AVAILABLE'&&ok.binding.relationship_state==='NOT_SUPPLIED','no invocation or inference may be implied');
assert(JSON.stringify(r(projection()))===JSON.stringify(r(JSON.parse(JSON.stringify(projection())))),'deterministic');
assert(!/device/i.test(JSON.stringify(ok)),'binding must not mention a device');

// Same predicates and dispositions as the CVK resolver.
const cases=[
  [projection(),{principal_id:null},'FAIL_CLOSED','SESSION_PRINCIPAL_UNAUTHENTICATED'],
  [projection(),{principal_id:''},'FAIL_CLOSED','SESSION_PRINCIPAL_UNAUTHENTICATED'],
  [projection(),{workspace_type:'ORGANIZATIONAL'},'FAIL_CLOSED','ORG_KV_ASSISTANT_CONTEXT_NOT_OBSERVED'],
  [null,{},'FAIL_CLOSED','PROJECTION_SCHEMA_INVALID'],
  [projection({schema:'other'}),{},'FAIL_CLOSED','PROJECTION_SCHEMA_INVALID'],
  [projection({authority_effect:'ALLOW'}),{},'FAIL_CLOSED','PROJECTION_AUTHORITY_INVALID'],
  [projection({workspace_grants_authority:true}),{},'FAIL_CLOSED','PROJECTION_AUTHORITY_INVALID'],
  [projection({projection_metadata:undefined}),{},'FAIL_CLOSED','PROJECTION_METADATA_INVALID'],
  [projection({projection_metadata:meta({schema:'stegverse.kv.other/v1'})}),{},'FAIL_CLOSED','PROJECTION_METADATA_INVALID'],
  [projection({projection_metadata:meta({grant_state:'REVOKED'})}),{},'DENY','WORKSPACE_GRANT_REVOKED'],
  [projection({projection_metadata:meta({owner_principal_id:null})}),{},'FAIL_CLOSED','PROJECTION_OWNER_UNBOUND'],
  [projection(),{principal_id:'user:other'},'DENY','PROJECTION_OWNER_MISMATCH'],
  [projection(),{workspace_id:'ws:personal:other'},'DENY','PROJECTION_WORKSPACE_MISMATCH'],
  [projection({assistant:null}),{},'FAIL_CLOSED','MYKV_ASSISTANT_BINDING_ABSENT'],
  [projection({assistant:Object.assign({},assistant,{principal_type:'HUMAN'})}),{},'FAIL_CLOSED','MYKV_ASSISTANT_RECORD_INVALID'],
  [projection({assistant:Object.assign({},assistant,{roles:[]})}),{},'FAIL_CLOSED','MYKV_ASSISTANT_RECORD_INVALID'],
  [projection({assistant:Object.assign({},assistant,{principal_id:'user:owner'})}),{},'FAIL_CLOSED','MYKV_ASSISTANT_IS_SESSION_PRINCIPAL'],
  [projection({principals:'x'}),{},'FAIL_CLOSED','PROJECTION_PRINCIPALS_INVALID'],
  [projection({principals:[{principal_id:'ai:other',principal_type:'AI_ENTITY',display_name:'Other',roles:['WORKSPACE_ASSISTANT']}]}),{},'FAIL_CLOSED','MYKV_ASSISTANT_AMBIGUOUS'],
];
for(const [p,ctx,disp,pred] of cases){const d=r(p,ctx);assert(d.disposition===disp&&d.predicate===pred&&d.binding===null&&d.generic_llm_fallback==='FORBIDDEN',pred+' expected '+disp+' got '+d.disposition+'/'+d.predicate);}
// An AI friend without the assistant role is not a second candidate.
assert(r(projection({principals:[{principal_id:'ai:friend',principal_type:'AI_ENTITY',display_name:'Friend'}]})).disposition==='ALLOW','AI friend treated as a second assistant');
// Null workspace on both sides binds; a workspace only on one side does not.
assert(r(projection({projection_metadata:meta({workspace_id:null})}),{workspace_id:null}).disposition==='ALLOW','null workspace on both sides');
assert(r(projection({projection_metadata:meta({workspace_id:null})})).predicate==='PROJECTION_WORKSPACE_MISMATCH','workspace on one side only');

// UI: the card renders the assistant as bound only on ALLOW. Today the page has no authenticated session
// principal, so the card must show FAIL_CLOSED / SESSION_PRINCIPAL_UNAUTHENTICATED even when KV carries an assistant,
// and must still label the observed KV assistant identity as not bound.
function harness(proj,sessionPatch){
  const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities'];
  const els={};ids.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
  const docListeners={};
  const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener:(t,f)=>{docListeners[t]=f}},console,
    fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{StegVerseWorkspaceKVBridge:{loadPersonalWorkspace:()=>Promise.resolve(proj)}}};
  vm.createContext(ctx);vm.runInContext(caps,ctx);vm.runInContext(src,ctx);ctx.window.StegVerseWorkspaceCapabilities=ctx.StegVerseWorkspaceCapabilities;ctx.window.StegVerseWorkspaceAssistantBinding=ctx.StegVerseWorkspaceAssistantBinding;
  if(sessionPatch)vm.runInContext(ui.replace('session:{principal_id:null,workspace_id:null,source:"NO_AUTHENTICATED_SESSION_PRINCIPAL"}','session:'+JSON.stringify(sessionPatch)),ctx);else vm.runInContext(ui,ctx);
  return {els,switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}})};
}
(async()=>{
  assert(ui.includes('session:{principal_id:null,workspace_id:null,source:"NO_AUTHENTICATED_SESSION_PRINCIPAL"}'),'page must not invent a session principal');
  let h=harness(projection());await new Promise(r=>setTimeout(r,10));
  let html=h.els.assistant.innerHTML;
  assert(html.includes('FAIL_CLOSED')&&html.includes('SESSION_PRINCIPAL_UNAUTHENTICATED'),'unauthenticated session must fail closed: '+html);
  assert(!html.includes('Bound to this session'),'assistant rendered as bound without ALLOW');
  assert(html.includes('not bound to this session')&&html.includes('Auri'),'observed KV assistant must be labelled as not bound');
  assert(html.includes('FORBIDDEN'),'card must state there is no generic LLM fallback');
  h.switchTo('organizational');html=h.els.assistant.innerHTML;
  // The session predicate comes first, as in the CVK resolver; the org-context message is still shown.
  assert(html.includes('SESSION_PRINCIPAL_UNAUTHENTICATED')&&html.includes('no authenticated Org-KV projection')&&!html.includes('Bound to this session'),'org context must fail closed: '+html);
  // With a matching authenticated session principal (test injection only; the page never supplies one itself).
  h=harness(projection(),{principal_id:'user:owner',workspace_id:'ws:personal:owner',source:'TEST_INJECTED'});await new Promise(r=>setTimeout(r,10));
  html=h.els.assistant.innerHTML;
  assert(html.includes('ALLOW')&&html.includes('Bound to this session')&&html.includes('Auri')&&html.includes('NOT_AVAILABLE')&&html.includes('action_eligible: false'),'bound card: '+html);
  h.switchTo('organizational');html=h.els.assistant.innerHTML;
  assert(html.includes('ORG_KV_ASSISTANT_CONTEXT_NOT_OBSERVED')&&!html.includes('Bound to this session'),'org switch must drop the binding: '+html);
  h=harness(projection(),{principal_id:'user:other',workspace_id:'ws:personal:owner',source:'TEST_INJECTED'});await new Promise(r=>setTimeout(r,10));
  html=h.els.assistant.innerHTML;
  assert(html.includes('DENY')&&html.includes('PROJECTION_OWNER_MISMATCH')&&!html.includes('Bound to this session'),'other user must be denied: '+html);
  h=harness(projection({assistant:null}),{principal_id:'user:owner',workspace_id:'ws:personal:owner',source:'TEST_INJECTED'});await new Promise(r=>setTimeout(r,10));
  html=h.els.assistant.innerHTML;
  assert(html.includes('MYKV_ASSISTANT_BINDING_ABSENT')&&html.includes('No Workspace Assistant identity is admitted'),'absent assistant: '+html);
  console.log('WORKSPACE_ASSISTANT_BINDING_PASS');
})().catch(e=>{console.error(e);process.exit(1)});
