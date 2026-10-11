// Session-authentication and MyKV assistant-binding decisions carry explanation-ready records with a plain-language
// reason (StegVerse-Labs/.github#3106 universal explanation contract). Reasons mirror continuity-vault-kit
// runtime/workspace_decision_reasons.py and never change a disposition or predicate.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
function load(file){const ctx={};ctx.globalThis=ctx;vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx);return ctx;}
let n=0;function check(ok,msg){n++;if(!ok)throw new Error(msg);}
const S=load('assets/workspace-session-authentication.js').StegVerseWorkspaceSessionAuthentication;
const B=load('assets/workspace-assistant-binding.js').StegVerseWorkspaceAssistantBinding;
const E=load('assets/workspace-explanation.js').StegVerseWorkspaceExplanation;
const TOKEN=/\b[A-Z]{2,}(?:_[A-Z0-9]+)+\b/;
for(const [name,reasons] of [['session',S.reasons],['binding',B.reasons]]){
  check(Object.isFrozen(reasons)&&Object.keys(reasons).length>=12,name+' reasons exported and frozen');
  for(const [p,r] of Object.entries(reasons)){check(typeof r==='string'&&r.trim()===r&&r.length>20&&!TOKEN.test(r)&&/^[a-z]/.test(r)&&!r.endsWith('.'),name+' reason is plain language: '+p);}
}
const receipt=(over)=>Object.assign({source_class:'CALLER_AUTHENTICATION_RECEIPT',principal_id:'user:owner',workspace_id:'ws:personal:owner',authentication:{authenticated:true,credential_authority:'TV/TVC',receipt_ref:'tv://receipt/1',principal_id:'user:owner'}},over||{});
const cases=[receipt(),{},receipt({source_class:'KV_PROJECTION_OWNER'}),receipt({source_class:'DEVICE_REGISTRATION'}),receipt({source_class:'BROWSER_STORAGE'}),receipt({source_class:'OTHER'}),receipt({authentication:null}),
  receipt({authentication:{authenticated:false,credential_authority:'TV/TVC',receipt_ref:'r',principal_id:'user:owner'}}),receipt({authentication:{authenticated:true,credential_authority:'X',receipt_ref:'r',principal_id:'user:owner'}}),
  receipt({authentication:{authenticated:true,credential_authority:'TV/TVC',receipt_ref:'',principal_id:'user:owner'}}),receipt({authentication:{authenticated:true,credential_authority:'TV/TVC',receipt_ref:'r',principal_id:'user:other'}}),
  receipt({authentication:{authenticated:true,credential_authority:'TV/TVC',receipt_ref:'r',principal_id:'user:owner',execution_authority:true}})];
const seen=new Set();
for(const c of cases){const d=S.resolve(c),r=d.explanation_record;seen.add(d.predicate);
  check(r&&r.disposition===d.disposition&&r.predicate===d.predicate&&r.why===S.reasons[d.predicate]&&r.authority_source==='NONE'&&r.consequence_observation==='NOT_AUTHENTICALLY_OBSERVED'&&d.action_eligible===false,'session record matches decision: '+d.predicate);
  const a=E.build(r,{repository:'StegVerse-Labs/Site',surface_id:'workspace'});
  check(a&&E.conforms(a).ok===true&&a.prose.why==='Because '+r.why+'.'&&a.execution.executed===false,'session record builds a conformant explanation: '+d.predicate);}
check(seen.size===Object.keys(S.reasons).length,'every session reason is reachable: '+[...seen].join(','));
const proj={schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',authority_effect:'NONE',workspace_grants_authority:false,projection_metadata:{schema:'stegverse.kv.workspace-projection-metadata/v1',owner_principal_id:'user:owner',workspace_id:'ws:personal:owner',grant_state:'ACTIVE'},principals:[],assistant:{principal_id:'auri:primary',principal_type:'AI_ENTITY',roles:['WORKSPACE_ASSISTANT']}};
for(const [p,sess] of [[proj,{principal_id:'user:owner',workspace_type:'PERSONAL',workspace_id:'ws:personal:owner'}],[proj,{}],[proj,{principal_id:'user:owner',workspace_type:'ORGANIZATION'}],[null,{principal_id:'user:owner',workspace_type:'PERSONAL'}],[Object.assign({},proj,{assistant:null}),{principal_id:'user:owner',workspace_type:'PERSONAL',workspace_id:'ws:personal:owner'}],[proj,{principal_id:'user:other',workspace_type:'PERSONAL',workspace_id:'ws:personal:owner'}]]){
  const d=B.resolve(p,sess),r=d.explanation_record;
  check(r&&r.disposition===d.disposition&&r.predicate===d.predicate&&r.why===B.reasons[d.predicate]&&r.consequence_observation==='NOT_AUTHENTICALLY_OBSERVED'&&d.generic_llm_fallback==='FORBIDDEN'&&d.action_eligible===false,'binding record matches decision: '+d.predicate);
  const a=E.build(r,{repository:'StegVerse-Labs/Site',surface_id:'workspace'});
  check(a&&E.conforms(a).ok===true&&a.prose.why==='Because '+r.why+'.'&&a.execution.executed===false,'binding record builds a conformant explanation: '+d.predicate);}
// Status and continuity catalogs: node binding, device continuity, assistant continuity, capabilities.
const src=f=>fs.readFileSync(path.join(root,f),'utf8');
const N=load('assets/workspace-node-binding.js').StegVerseWorkspaceNodeBinding,D=load('assets/workspace-device-continuity.js').StegVerseWorkspaceDeviceContinuity,A=load('assets/workspace-assistant-continuity.js').StegVerseWorkspaceAssistantContinuity,C=load('assets/workspace-capabilities.js').StegVerseWorkspaceCapabilities;
const lits=(text,re)=>{const out=new Set();let m;while((m=re.exec(text)))out.add(m[1]);return out;};
// Check states and continuity states are not predicates; CHECKPOINT_NOT_OBSERVED is the assistant catalog's.
const STATES=new Set(['ALLOW','DENY','FAIL_CLOSED','PROJECTED','NOT_OBSERVED','UNKNOWN','CALLER_SUPPLIED_NOT_PAGE_VERIFIED','CONTINUOUS_VERIFIED_BY_PRODUCER','CHECKPOINT_NOT_OBSERVED','REPLAY_STATUS_UNKNOWN']);
const produced={
  node:lits(src('assets/workspace-node-binding.js'),/decision\("[A-Z_]+","([A-Z0-9_]+)"/g),
  device:new Set([...lits(src('assets/workspace-device-continuity.js').split('\n').filter(l=>/check\("DR[1345]"/.test(l)).join('\n'),/"([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+)"/g)].filter(p=>!STATES.has(p)).concat([D.ingress_predicate])),
  assistant:new Set([...lits(src('assets/workspace-assistant-continuity.js'),/base\("[A-Z_]+","([A-Z0-9_]+)(?::|")/g),...lits(src('assets/workspace-assistant-continuity.js'),/return "(CHECKPOINT_DECISION_[A-Z_]+)"/g),...lits(src('assets/workspace-assistant-continuity.js'),/continuity\.predicate="([A-Z_]+)"/g),...lits(src('assets/workspace-assistant-continuity.js'),/base\([^;]*?\?[^;]*?:"([A-Z][A-Z_]+)"\)/g),'CHECKPOINT_NOT_OBSERVED','CHECKPOINT_MALFORMED']),
  capability:new Set([...lits(src('assets/workspace-capabilities.js'),/status\("[A-Z_]+","([A-Z0-9_]+)"/g),...lits(src('assets/workspace-capabilities.js'),/return "(DESCRIPTOR_[A-Z_]+)[":]/g),...lits(src('assets/workspace-capabilities.js'),/status\("[A-Z_]+",[^;]*?\?"([A-Z_]+)":/g),...lits(src('assets/workspace-capabilities.js'),/status\("[A-Z_]+",[^;]*?\?"[A-Z_]+":"([A-Z_]+)"/g)])};
for(const [name,mod] of [['node',N],['device',D],['assistant',A],['capability',C]]){
  const r=mod.reasons,set=produced[name];
  check(Object.isFrozen(r)&&set.size>=5,name+' catalog exported and predicates found: '+set.size);
  // DR4 also looks up the binding and session catalogs, so assistant predicates may be covered there.
  for(const p of set)check(typeof r[p]==='string'||(name==='assistant'&&(typeof B.reasons[p]==='string'||typeof S.reasons[p]==='string')),name+' predicate without a reason: '+p);
  for(const p of Object.keys(r))check(set.has(p),name+' reason for a predicate the module never returns: '+p);
  for(const [p,t] of Object.entries(r))check(t.trim()===t&&t.length>20&&!TOKEN.test(t)&&/^[a-z]/.test(t)&&!t.endsWith('.'),name+' reason is plain language: '+p);
  for(const p of Object.keys(r)){const a=E.build({disposition:'FAIL_CLOSED',predicate:p,requested_action:'Check '+name,authority_source:'NONE',why:r[p]},{repository:'StegVerse-Labs/Site',surface_id:'workspace'});check(a&&E.conforms(a).ok===true&&a.prose.why==='Because '+r[p]+'.',name+' reason builds a conformant explanation: '+p);}
}
// Statuses are unchanged by the catalogs: still action_eligible false and authority NONE.
const st=C.evaluate({capability:'FEED',label:'Feed',workspace_types:['PERSONAL'],allowed_projection_schemas:['stegverse.kv.personal-workspace-projection/v1'],projection_field:'feed',max_age_seconds:60,default_state:'NOT_OBSERVED',authority_effect:'NONE'},null,'PERSONAL',Date.now());
check(st.predicate==='KV_PROJECTION_NOT_OBSERVED'&&st.action_eligible===false&&st.authority_effect==='NONE'&&typeof C.reasons[st.predicate]==='string','capability status unchanged and explainable: '+JSON.stringify(st));
// KV bridge and page reasons.
{const KB=load('assets/workspace-kv-bridge.js').StegVerseWorkspaceKVBridge;const bsrc=src('assets/workspace-kv-bridge.js');
 const bridgePreds=lits(bsrc,/predicate:"([A-Z][A-Z0-9_]+)"/g);
 check(KB&&Object.isFrozen(KB.reasons)&&bridgePreds.size>=1,'kv bridge catalog exported');
 for(const p of bridgePreds)check(typeof KB.reasons[p]==='string','kv bridge predicate without a reason: '+p);
 for(const p of Object.keys(KB.reasons))check(bridgePreds.has(p),'kv bridge reason for a predicate it never returns: '+p);
 const ui=src('assets/workspace.js');const block=ui.slice(ui.indexOf('const PAGE_REASONS=Object.freeze({'),ui.indexOf('});',ui.indexOf('const PAGE_REASONS=Object.freeze({')));
 const page={};let m;const re=/([A-Z][A-Z0-9_]+):"([^"]+)"/g;while((m=re.exec(block)))page[m[1]]=m[2];
 const pagePreds=new Set([...lits(ui,/failing_predicate:"([A-Z_]+)"/g),...lits(ui,/predicate:"(WORKSPACE_DEVICE_KV_[A-Z_]+)"/g),...lits(ui,/"(WORKSPACE_DEVICE_KV_PATH_UNAVAILABLE)"/g)]);
 check(Object.keys(page).length===3,'page reasons parsed: '+Object.keys(page).join(','));
 for(const p of pagePreds)check(typeof page[p]==='string','page predicate without a reason: '+p);
 for(const [p,t] of Object.entries([...Object.entries(page),...Object.entries(KB.reasons)].reduce((o,[k,v])=>(o[k]=v,o),{})))check(t.trim()===t&&t.length>20&&!TOKEN.test(t)&&/^[a-z]/.test(t)&&!t.endsWith('.'),'reason is plain language: '+p);}
console.log('WORKSPACE_DECISION_EXPLANATIONS_PASS assertions='+n);
