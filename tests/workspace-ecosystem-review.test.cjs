'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const C=require('../assets/workspace-ecosystem-review.js');
const NOW=Date.parse('2026-11-19T20:00:00Z');
const rev='a'.repeat(40),digest='sha256:'+'b'.repeat(64);
const context={workspace_type:'DEVELOPER',kv_scope:'ECOSYSTEM',principal_id:'fixture:reviewer',workspace_id:'fixture:ecosystem'};
function fixture(){return {
  schema:C.SCHEMA,workspace_type:'DEVELOPER',kv_scope:'ECOSYSTEM',kv_account:'stegverse@gmail.com',
  projection_metadata:{schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-11-19T19:59:00Z',source_revision:rev,provenance_ref:'fixture:delivery:1',owner_principal_id:context.principal_id,workspace_id:context.workspace_id,grant_state:'ACTIVE',authority_effect:'NONE'},
  queue:{state:'HAS_WORK',source_ref:'fixture:queue',observed_at:'2026-11-19T19:58:00Z',read_complete:true,error:null},
  reviews:[{goal:{task_id:'FIXTURE-GOAL-001',state:'PROPOSED',cosv:'NONE',handoff_ref:'fixture:MIRROR_HANDOFF.md',source_ref:'fixture:registry',source_revision:rev},
    inputs:[{input_id:'input-1',source_ref:'fixture:original-input',source_revision:rev,digest,filed_at:'2026-11-19T19:00:00Z'}],
    evidence:[{evidence_id:'e1',source_ref:'fixture:manifest',digest,state:'VERIFIED',filed_by:'fixture:author',verified_by:'fixture:peer',verification_ref:'fixture:peer-verdict'}],
    facts:[{fact_id:'f1',category:'MANIFEST',statement:'Manifest is filed.',evidence_state:'VERIFIED',work_state:'COMPLETED',evidence_refs:['e1']},{fact_id:'f2',category:'RUNTIME_OWNERSHIP',statement:'Runtime owner is not established.',evidence_state:'UNKNOWN',work_state:'STILL_REQUIRED',evidence_refs:[]}],
    checks:[{check_id:'c1',input_id:'input-1',input_digest:digest,source_revision:rev,goal_revision:rev,predicate:'MANIFEST_SHAPE',rule_revision:'fixture:rule-1',state:'FILED',result_ref:'fixture:check-result'}],
    continuity:{source_ref:'fixture:continuity',next_step:'Obtain the existing owner decision.',required_owner:'fixture:owner',handoff_ref:'fixture:MIRROR_HANDOFF.md'}}],
  credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,authority_effect:'NONE'};}
function evaluate(p=fixture(),ctx=context){return C.evaluate(p,ctx,NOW);}
function reject(change,code){const p=fixture();change(p);assert.equal(evaluate(p).failure_code,code);}
test('filed source view is display-only, input remains unchanged',()=>{
  const p=fixture(),before=JSON.stringify(p),v=evaluate(p);
  assert.equal(v.state,'SOURCE_VIEW_READY');assert.equal(v.authority_effect,'NONE');assert.equal(v.action_eligible,false);assert.equal(v.replay_status,'REPLAY_STATUS_UNKNOWN');assert.equal(v.verification,'FILED_SUPPORT_ONLY_NOT_PAGE_VERIFIED');assert.equal(JSON.stringify(p),before);
  v.reviews[0].goal.state='ALTERED';assert.equal(p.reviews[0].goal.state,'PROPOSED');
});
test('personal, organizational, wrong principal and wrong workspace contexts are withheld',()=>{
  for(const type of ['PERSONAL','ORGANIZATIONAL'])assert.equal(evaluate(fixture(),{...context,workspace_type:type}).state,'WITHHELD');
  for(const [key,value] of [['principal_id','other'],['workspace_id','other']])assert.equal(evaluate(fixture(),{...context,[key]:value}).failure_code,'PRINCIPAL_OR_WORKSPACE_MISMATCH');
});
test('account and KV scope cannot fall back to Personal KV',()=>{
  reject(p=>p.kv_account='rigelrandolph@gmail.com','ECOSYSTEM_PROJECTION_CONTEXT_MISMATCH');
  reject(p=>p.kv_scope='PERSONAL','ECOSYSTEM_PROJECTION_CONTEXT_MISMATCH');
});
test('absent projection differs from empty queue',()=>{const v=evaluate(null);assert.equal(v.state,'WITHHELD');assert.equal(v.queue,undefined);});
test('revoked or unknown grants withhold every row',()=>{for(const value of ['REVOKED','UNKNOWN',null])reject(p=>p.projection_metadata.grant_state=value,'ECOSYSTEM_GRANT_NOT_ACTIVE');});
test('authority escalation is refused',()=>{for(const key of ['provider_operation_authorized','workspace_grants_authority','credential_material_present'])reject(p=>p[key]=true,'PROJECTION_AUTHORITY_ASSERTED');});
test('credentials and private original payloads are refused',()=>{
  reject(p=>p.reviews[0].inputs[0].payload='private original','CREDENTIAL_OR_PAYLOAD_REFUSED');
  reject(p=>p.reviews[0].facts[0].statement='Bearer abcdefghijklmnop','CREDENTIAL_OR_PAYLOAD_REFUSED');
  reject(p=>p.authorization='private','CREDENTIAL_OR_PAYLOAD_REFUSED');
});
test('malformed and future freshness fail; old data stays explicitly stale',()=>{
  reject(p=>p.projection_metadata.observed_at='invalid','PROJECTION_TIME_INVALID');
  reject(p=>p.projection_metadata.observed_at='2026-11-20T20:00:00Z','PROJECTION_TIME_INVALID');
  const v=C.evaluate(fixture(),context,NOW+172800000);assert.equal(v.state,'STALE');assert.match(C.drafts(v,'FIXTURE-GOAL-001').issue_comment,/STALE/);
});
test('empty queue requires a complete source read',()=>{
  reject(p=>Object.assign(p.queue,{state:'EMPTY',read_complete:false}),'QUEUE_DISPOSITION_INVALID');
  const p=fixture();p.queue.state='EMPTY';const v=evaluate(p);assert.equal(v.queue.state,'EMPTY');assert.equal(v.reviews[0].facts[1].work_state,'STILL_REQUIRED');
});
test('error queues preserve all six actionable fields',()=>{
  const p=fixture();p.queue.state='ERROR';p.queue.read_complete=false;p.queue.error={failure_code:'FIXTURE_READ_FAILED',failed_predicate:'FIXTURE_SOURCE_UNREADABLE',required_evidence_or_repair:'Restore source access.',retry_entrypoint:'fixture:read',owning_existing_goal:'FIXTURE-GOAL-001',next_attempt:'Retry after access changes.'};
  const v=evaluate(p);assert.deepEqual(v.queue.error,p.queue.error);assert.match(C.drafts(v,'FIXTURE-GOAL-001').coordination_update,/FIXTURE_READ_FAILED/);
  delete p.queue.error.next_attempt;assert.equal(evaluate(p).failure_code,'QUEUE_DISPOSITION_INVALID');
});
test('verified fact needs filed independent support; self-verification is refused',()=>{
  reject(p=>p.reviews[0].facts[0].evidence_refs=[],'FACT_SUPPORT_INVALID');
  reject(p=>p.reviews[0].evidence[0].verified_by='fixture:author','EVIDENCE_SUPPORT_INVALID');
  reject(p=>p.reviews[0].evidence[0].verification_ref=null,'EVIDENCE_SUPPORT_INVALID');
  reject(p=>p.reviews[0].evidence[0].state='REPORTED','FACT_SUPPORT_INVALID');
});
test('completed without filed support is refused; verification never completes unknown work',()=>{
  reject(p=>p.reviews[0].facts[1].work_state='COMPLETED','FACT_SUPPORT_INVALID');
  const r=evaluate().reviews[0];assert.equal(C.selectFacts(r,'VERIFIED','COMPLETED').length,1);assert.equal(C.selectFacts(r,'UNRESOLVED','STILL_REQUIRED')[0].category,'RUNTIME_OWNERSHIP');
});
test('missing review categories remain unknown instead of implying evidence completeness',()=>{
  const p=fixture();p.reviews[0].facts=[];const v=evaluate(p),r=v.reviews[0];
  assert.equal(r.unassessed_categories.length,C.CATEGORIES.length);
  assert.equal(C.selectFacts(r,'UNRESOLVED','UNKNOWN').length,C.CATEGORIES.length);
  assert.match(C.drafts(v,'FIXTURE-GOAL-001').evidence_gaps,/OWNER_BINDING: no filed assessment/);
  assert.match(C.drafts(v,'FIXTURE-GOAL-001').evidence_gaps,/INDEPENDENT_REPLAY: no filed assessment/);
});
test('unsupported categories, hidden text, extra fields and missing evidence locators are withheld',()=>{
  reject(p=>p.reviews[0].facts[0].category='EXECUTE_NOW','FACT_SUPPORT_INVALID');
  reject(p=>p.reviews[0].facts[0].statement='looks\u202eharmless','FACT_SUPPORT_INVALID');
  reject(p=>p.reviews[0].evidence[0].source_ref='','EVIDENCE_SUPPORT_INVALID');
  reject(p=>p.reviews[0].goal.owner_bound=true,'GOAL_SOURCE_INVALID');
});
test('null rows, duplicate identities and dangling references fail closed without throwing',()=>{
  reject(p=>p.reviews=[null],'REVIEW_LIST_INVALID');
  reject(p=>p.reviews[0].inputs=[null],'INPUT_IDENTITY_INVALID');
  reject(p=>p.reviews.push(p.reviews[0]),'REVIEW_LIST_INVALID');
  reject(p=>p.reviews[0].inputs.push(p.reviews[0].inputs[0]),'INPUT_IDENTITY_INVALID');
  reject(p=>p.reviews[0].facts[0].evidence_refs=['absent'],'FACT_SUPPORT_INVALID');
});
test('exact-version duplicate checks group once and retain all result locators',()=>{
  const p=fixture();p.reviews[0].checks.push({...p.reviews[0].checks[0],check_id:'c2',result_ref:'fixture:second-result'});
  const groups=evaluate(p).reviews[0].check_groups;assert.equal(groups.length,1);assert.equal(groups[0].duplicate_count,1);assert.equal(groups[0].repeat_review,'EXACT_VERSION_RESULT_FILED');assert.equal(groups[0].checks.length,2);
});
test('changed input bytes, source revision or goal revision requires new review',()=>{
  for(const change of [p=>p.reviews[0].inputs[0].digest='sha256:'+'c'.repeat(64),p=>p.reviews[0].inputs[0].source_revision='new',p=>p.reviews[0].goal.source_revision='d'.repeat(40)]){
    const p=fixture();change(p);assert.equal(evaluate(p).reviews[0].check_groups[0].repeat_review,'REVIEW_REQUIRED');
  }
});
test('rule changes do not share a duplicate group; error and conflicting checks require review',()=>{
  const p=fixture(),r=p.reviews[0];r.checks.push({...r.checks[0],check_id:'c2',rule_revision:'fixture:rule-2'});assert.equal(evaluate(p).reviews[0].check_groups.length,2);
  r.checks[1].rule_revision=r.checks[0].rule_revision;r.checks[1].state='ERROR';const g=evaluate(p).reviews[0].check_groups[0];assert.equal(g.state,'CONFLICTING');assert.equal(g.repeat_review,'REVIEW_REQUIRED');
});
test('four draft forms preserve facts, uncertainty, original anchors and next owner',()=>{
  const v=evaluate(),drafts=C.drafts(v,'FIXTURE-GOAL-001');assert.equal(Object.keys(drafts).length,4);
  for(const d of Object.values(drafts)){assert.match(d,/unsubmitted/);assert.match(d,/not page verification/);assert.match(d,/fixture:registry/);}
  assert.match(drafts.evidence_gaps,/Runtime owner is not established/);assert.match(drafts.next_session,/fixture:owner/);assert.equal(C.drafts(v,'MISSING'),null);
});
test('contract never reads providers, writes stores, or executes original input',()=>{
  const source=fs.readFileSync(path.join(__dirname,'../assets/workspace-ecosystem-review.js'),'utf8');
  assert.doesNotMatch(source,/fetch\s*\(|XMLHttpRequest|localStorage|sessionStorage|indexedDB|eval\s*\(|new Function|registerDevice/);
});
const uiSource=fs.readFileSync(path.join(__dirname,'../assets/workspace-ecosystem-review-ui.js'),'utf8');
function harness(loader){
  const box={innerHTML:'',listeners:{},addEventListener(k,v){this.listeners[k]=v;}};
  const switcher={value:'personal',listeners:{},addEventListener(k,v){this.listeners[k]=v;}};
  const docEvents={};
  const ctx={window:{StegVerseWorkspaceEcosystemReview:C,StegVerseWorkspaceKVBridge:loader?{loadEcosystemCoordinationReview:loader}:{}},document:{querySelector(s){return s==='#ecosystemReview'?box:s==='#workspaceSwitch'?switcher:null;},addEventListener(k,v){docEvents[k]=v;}},console};
  vm.runInNewContext(uiSource,ctx);
  return {box,switchTo(mode){switcher.value=mode;switcher.listeners.change();},click(attrs){box.listeners.click({target:{closest(){return {getAttribute(k){return attrs[k]||null;}};}}});},invalidate(){docEvents['stegverse:ecosystem-review-invalidated']();}};
}
const turn=()=>new Promise(resolve=>setImmediate(resolve));
test('UI missing owner bridge yields actionable unavailable, never empty queue',async()=>{
  const h=harness();h.switchTo('developer');h.click({'data-review-action':'refresh'});await turn();
  assert.match(h.box.innerHTML,/ECOSYSTEM_REVIEW_OWNER_BRIDGE_NOT_BOUND/);assert.doesNotMatch(h.box.innerHTML,/Queue: EMPTY/);
});
test('UI read error withholds old rows and does not expose exception payload',async()=>{
  let fail=false;const h=harness(async()=>{if(fail)throw Error('private-exception-material');return {projection:fixture(),context};});h.switchTo('developer');h.click({'data-review-action':'refresh'});await turn();assert.match(h.box.innerHTML,/FIXTURE-GOAL-001/);
  fail=true;h.click({'data-review-action':'refresh'});await turn();assert.match(h.box.innerHTML,/ECOSYSTEM_REVIEW_READ_FAILED/);assert.doesNotMatch(h.box.innerHTML,/private-exception-material|FIXTURE-GOAL-001|Queue: EMPTY/);
});
test('context switch discards in-flight delivery and drafts',async()=>{
  let resolve;const h=harness(()=>new Promise(r=>resolve=r));h.switchTo('developer');h.click({'data-review-action':'refresh'});h.switchTo('personal');resolve({projection:fixture(),context});await turn();assert.doesNotMatch(h.box.innerHTML,/FIXTURE-GOAL-001/);h.switchTo('developer');assert.doesNotMatch(h.box.innerHTML,/FIXTURE-GOAL-001/);
});
test('newest refresh wins and revocation invalidation removes rows',async()=>{
  const pending=[];const h=harness(()=>new Promise(r=>pending.push(r)));h.switchTo('developer');h.click({'data-review-action':'refresh'});h.click({'data-review-action':'refresh'});
  const newer=fixture();newer.reviews[0].goal.task_id='FIXTURE-NEWER';pending[1]({projection:newer,context});await turn();pending[0]({projection:fixture(),context});await turn();assert.match(h.box.innerHTML,/FIXTURE-NEWER/);assert.doesNotMatch(h.box.innerHTML,/FIXTURE-GOAL-001/);h.invalidate();assert.doesNotMatch(h.box.innerHTML,/FIXTURE-NEWER/);
});
test('UI escapes projected HTML and generates only unsubmitted drafts',async()=>{
  const p=fixture();p.reviews[0].facts[0].statement='<img src=x onerror=alert(1)>';
  const h=harness(async()=>({projection:p,context}));h.switchTo('developer');h.click({'data-review-action':'refresh'});await turn();assert.match(h.box.innerHTML,/&lt;img/);assert.doesNotMatch(h.box.innerHTML,/<img/);
  h.click({'data-review-draft':'issue_comment'});assert.match(h.box.innerHTML,/Unsubmitted draft/);assert.doesNotMatch(h.box.innerHTML,/<img/);
});
test('phone layout, accessible controls and existing shell integration are source-bound',()=>{
  const page=fs.readFileSync(path.join(__dirname,'../workspace.html'),'utf8');const css=fs.readFileSync(path.join(__dirname,'../assets/workspace.css'),'utf8');
  assert.match(page,/data-target="ecosystemReviewCard"/);assert.match(page,/id="ecosystemReviewCard"/);assert.match(page,/workspace-ecosystem-review-ui.js/);assert.match(css,/minmax\(min\(100%,220px\),1fr\)/);assert.match(css,/min-height:44px/);assert.match(uiSource,/<label>/);assert.match(uiSource,/aria-live="polite"/);assert.doesNotMatch(uiSource,/fetch\s*\(|localStorage|sessionStorage|indexedDB/);
});
