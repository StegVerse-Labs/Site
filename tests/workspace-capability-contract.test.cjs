// Capability descriptor / freshness / provenance contract (Site#1509): descriptors never assert
// availability, and status is derived only from authenticated KV projection metadata.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const caps=fs.readFileSync(path.join(root,'assets/workspace-capabilities.js'),'utf8');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
const bootstrap=JSON.parse(fs.readFileSync(path.join(root,'data/workspace/bootstrap.json'),'utf8'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
const sandbox={};vm.createContext(sandbox);vm.runInContext(caps,sandbox);
const C=sandbox.StegVerseWorkspaceCapabilities;
const NOW=Date.parse('2026-10-10T12:00:00Z');
const descs=bootstrap.capability_descriptors;
const byCap=Object.fromEntries(descs.map(d=>[d.capability,d]));
function projection(extra){return Object.assign({schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',state:'KV_WORKSPACE_PROJECTED',
  principals:[{principal_id:'P-1',principal_type:'HUMAN',display_name:'Friend'}],organizations:[],memberships:[],feed:[],assistant:null,
  credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,authority_effect:'NONE'},extra||{});}
const ev=(cap,p,type)=>C.evaluate(byCap[cap],p,type||'PERSONAL',NOW);

// Shipped descriptors are valid and non-asserting.
assert(bootstrap.capability_descriptor_schema===C.descriptor_schema,'descriptor schema mismatch');
for(const d of descs){assert(C.descriptorProblem(d)===null,'shipped descriptor invalid: '+d.capability);assert(d.default_state==='NOT_OBSERVED'&&d.authority_effect==='NONE','descriptor asserts state');}
for(const cap of ['FEED','CONTACTS','ORGANIZATIONS','MEMBERSHIPS','AI_ASSISTANT','ORG_WORKSPACE','CALENDAR','EMAIL','MESSAGING','DOCUMENTS','SOCIAL','TASKS','GITHUB_GOVERNANCE','CRYPTOBOT_PORTFOLIO'])assert(byCap[cap],'missing descriptor '+cap);

// Descriptors that try to assert availability, admission, freshness or ALLOW are rejected.
for(const forged of [{available:true},{admitted:true},{fresh:true},{disposition:'ALLOW'},{observed_at:'2026-10-10T12:00:00Z'},{default_state:'OBSERVED'},{authority_effect:'ALLOW'}]){
  const s=C.evaluate(Object.assign({},byCap.FEED,forged),projection({projection_metadata:{observed_at:'2026-10-10T11:59:00Z'}}),'PERSONAL',NOW);
  assert(s.state==='DESCRIPTOR_REJECTED'&&C.withholdsRows(s),'forged descriptor accepted: '+JSON.stringify(forged));
}
assert(C.evaluate(null,projection(),'PERSONAL',NOW).state==='DESCRIPTOR_REJECTED','null descriptor accepted');

// Capabilities without a KV projection contract are UNAVAILABLE regardless of projection content.
for(const cap of ['CALENDAR','EMAIL','MESSAGING','DOCUMENTS','SOCIAL','TASKS','GITHUB_GOVERNANCE','CRYPTOBOT_PORTFOLIO']){
  const s=ev(cap,projection({calendar:[{}],projection_metadata:{observed_at:'2026-10-10T11:59:00Z'}}));
  assert(s.state==='UNAVAILABLE'&&s.predicate==='NO_KV_PROJECTION_CONTRACT','unbacked capability not UNAVAILABLE: '+cap);
}

// Absent projection.
assert(ev('FEED',null).state==='NOT_OBSERVED'&&ev('FEED',null).predicate==='KV_PROJECTION_NOT_OBSERVED','absent projection not NOT_OBSERVED');
assert(C.withholdsRows(undefined),'missing status must withhold rows');

// Cross-context: personal capabilities are not defined for org context; org has no projection.
assert(ev('FEED',projection(),'ORGANIZATIONAL').state==='UNAVAILABLE','personal capability leaked into org context');
assert(ev('ORG_WORKSPACE',null,'ORGANIZATIONAL').predicate==='NO_KV_PROJECTION_CONTRACT','org workspace must have no contract yet');
const mismatch=C.evaluate(Object.assign({},byCap.FEED,{workspace_types:['ORGANIZATIONAL']}),projection(),'ORGANIZATIONAL',NOW);
assert(mismatch.state==='CONTEXT_MISMATCH'&&C.withholdsRows(mismatch),'personal projection accepted for org context');

// Malformed projections.
assert(ev('FEED',projection({schema:'stegverse.kv.other/v1'})).state==='MALFORMED','foreign schema accepted');
assert(ev('FEED',projection({authority_effect:'ALLOW'})).state==='MALFORMED','authority-asserting projection accepted');
assert(ev('FEED',projection({projection_metadata:'yesterday'})).state==='MALFORMED','string metadata accepted');
assert(ev('FEED',projection({feed:'x'})).state==='MALFORMED','scalar field accepted');
assert(ev('FEED',projection({projection_metadata:{observed_at:'not-a-date'}})).state==='MALFORMED','bad observed_at accepted');
assert(ev('FEED',projection({projection_metadata:{observed_at:'2026-10-11T12:00:00Z'}})).predicate==='PROJECTION_OBSERVED_AT_IN_FUTURE','future observed_at accepted');
const absentField=projection();delete absentField.feed;
assert(ev('FEED',absentField).state==='UNAVAILABLE','absent field not UNAVAILABLE');

// Revoked grants withhold rows.
for(const meta of [{revoked:true,observed_at:'2026-10-10T11:59:00Z'},{grant_state:'REVOKED'}]){const s=ev('CONTACTS',projection({projection_metadata:meta}));assert(s.state==='REVOKED'&&C.withholdsRows(s),'revocation ignored');}

// Freshness: current CVK projections carry no observed_at, so freshness is UNKNOWN, never OBSERVED.
const unknown=ev('CONTACTS',projection());
assert(unknown.state==='FRESHNESS_UNKNOWN'&&unknown.predicate==='PROJECTION_OBSERVED_AT_ABSENT'&&!C.withholdsRows(unknown),'missing observed_at must be FRESHNESS_UNKNOWN');
const stale=ev('CONTACTS',projection({projection_metadata:{observed_at:'2026-10-08T12:00:00Z',provenance_ref:'kv://receipt/1'}}));
assert(stale.state==='STALE'&&stale.age_seconds===172800&&stale.provenance_ref==='kv://receipt/1'&&!C.withholdsRows(stale),'stale projection not labelled STALE');
const fresh=ev('CONTACTS',projection({projection_metadata:{observed_at:'2026-10-10T11:59:00Z',source_cursor:'c-9'}}));
assert(fresh.state==='OBSERVED'&&fresh.age_seconds===60&&fresh.source_cursor==='c-9','fresh projection not OBSERVED');

// No status ever carries an authorizing disposition.
const all=C.evaluateAll(descs,projection({projection_metadata:{observed_at:'2026-10-10T11:59:00Z'}}),'PERSONAL',NOW).concat(C.evaluateAll(descs,null,'ORGANIZATIONAL',NOW));
for(const s of all){assert(s.authority_effect==='NONE','status asserts authority');assert(!/ALLOW|ADMITTED/.test(JSON.stringify(s)),'status asserts ALLOW/ADMITTED: '+s.capability);}

// Statuses are informational only, whatever their state.
for(const s of all)assert(s.action_eligible===false,'status must never be action-eligible: '+s.capability+' '+s.state);
assert(fresh.action_eligible===false&&stale.action_eligible===false&&unknown.action_eligible===false,'OBSERVED/STALE/FRESHNESS_UNKNOWN must not be action-eligible');

// Metadata exactly as continuity-vault-kit runtime/workspace_projection.py emits it (CVK PR #237).
const cvkMeta={schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-10T11:58:00Z',observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',
  source_revision:'a'.repeat(64),provenance_ref:'kv-workspace-source:sha256:'+'a'.repeat(64),workspace_type:'PERSONAL',workspace_id:null,owner_principal_id:null,
  grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'};
const cvk=ev('CONTACTS',projection({projection_metadata:cvkMeta}));
assert(cvk.state==='OBSERVED'&&cvk.source_revision==='a'.repeat(64)&&cvk.grant_state==='UNKNOWN'&&cvk.provenance_ref===cvkMeta.provenance_ref&&cvk.action_eligible===false,'CVK metadata not consumed as informational OBSERVED');
assert(ev('CONTACTS',projection({projection_metadata:Object.assign({},cvkMeta,{schema:'stegverse.kv.other-metadata/v1'})})).predicate==='PROJECTION_METADATA_SCHEMA_INVALID','foreign metadata schema accepted');
assert(ev('CONTACTS',projection({projection_metadata:Object.assign({},cvkMeta,{grant_state:'REVOKED'})})).state==='REVOKED','CVK REVOKED grant ignored');

// UI integration: rows are withheld when descriptors are missing or the grant is revoked.
function ui_harness(boot,proj){
  const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities'];
  const els={};ids.forEach(i=>els[i]={innerHTML:'',textContent:'',className:'',value:'',dataset:{},listeners:{},addEventListener(t,f){this.listeners[t]=f}});
  const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener(){}},
    console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(boot)}),window:{StegVerseWorkspaceKVBridge:{loadPersonalWorkspace:()=>Promise.resolve(proj)}}};
  vm.createContext(ctx);vm.runInContext(caps,ctx);ctx.window.StegVerseWorkspaceCapabilities=ctx.StegVerseWorkspaceCapabilities;vm.runInContext(ui,ctx);return els;
}
(async()=>{
  let els=ui_harness({},projection());await new Promise(r=>setTimeout(r,10));
  assert(!els.contacts.innerHTML.includes('Friend')&&els.capabilities.innerHTML.includes('FAIL_CLOSED'),'missing descriptors must fail closed');
  els=ui_harness(bootstrap,projection({projection_metadata:{grant_state:'REVOKED'}}));await new Promise(r=>setTimeout(r,10));
  assert(!els.contacts.innerHTML.includes('Friend')&&els.capabilities.innerHTML.includes('REVOKED'),'revoked grant rows rendered');
  els=ui_harness(bootstrap,projection());await new Promise(r=>setTimeout(r,10));
  assert(els.contacts.innerHTML.includes('Friend'),'freshness-unknown rows should render');
  assert(els.capabilities.innerHTML.includes('FRESHNESS_UNKNOWN')&&els.capabilities.innerHTML.includes('NO_KV_PROJECTION_CONTRACT'),'capability card missing states');
  assert(!/>OBSERVED</.test(els.capabilities.innerHTML),'capability card forged OBSERVED without observed_at');
  assert(els.capabilities.innerHTML.includes('action_eligible: false'),'capability card must state informational-only');
  console.log('WORKSPACE_CAPABILITY_CONTRACT_PASS');
})().catch(e=>{console.error(e);process.exit(1)});
