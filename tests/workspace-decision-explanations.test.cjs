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
console.log('WORKSPACE_DECISION_EXPLANATIONS_PASS assertions='+n);
