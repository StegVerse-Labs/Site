/* Read-only candidate consumer. Filed verification is reported, never performed by this module. */
(function(root){
  'use strict';
  const SCHEMA='stegverse.kv.ecosystem-coordination-review-projection/v1';
  const CATEGORIES=['OWNER_FORM','OWNER_BINDING','AUTHORITY','TASK','HANDOFF','CLAIM','MANIFEST','NATIVE_EXECUTION','NEGATIVE_CONTROL','INDEPENDENT_REPLAY','RUNTIME_OWNERSHIP','CONTINUITY'];
  const EVIDENCE=['VERIFIED','REPORTED','UNKNOWN','CONFLICTING'];
  const WORK=['COMPLETED','STILL_REQUIRED','NOT_APPLICABLE','UNKNOWN'];
  const TEXT=/[\p{Cc}\p{Cf}\p{Cs}\p{Zl}\p{Zp}]/u;
  const DIGEST=/^sha256:[a-f0-9]{64}$/;
  const REV=/^[a-f0-9]{40,64}$/;
  const own=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
  const object=o=>!!o&&typeof o==='object'&&!Array.isArray(o);
  const text=(s,n=1024)=>typeof s==='string'&&s.trim().length>0&&s.length<=n&&!TEXT.test(s);
  const exact=(o,keys)=>object(o)&&Object.keys(o).every(k=>keys.includes(k))&&keys.every(k=>own(o,k));
  const list=(a,max=500)=>Array.isArray(a)&&a.length<=max;
  const unique=(a,key)=>new Set(a.map(x=>x&&x[key])).size===a.length;
  const refs=(a,set)=>list(a,100)&&a.every(x=>text(x,256)&&set.has(x))&&new Set(a).size===a.length;
  function refusal(code){return {schema:'stegverse.workspace.ecosystem-review/v1',state:'WITHHELD',failure_code:code,failed_predicate:code,required_evidence_or_repair:'The existing KV producer and admitted DEVICE_KV delivery must supply a current, scoped Ecosystem coordination review projection matching the candidate contract.',retry_entrypoint:'StegVerseWorkspaceKVBridge.loadEcosystemCoordinationReview',owning_existing_goal:'STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001',next_attempt:'Refresh after the owning producer or delivery condition changes; the page does not poll.',reviews:[],action_eligible:false,authority_effect:'NONE'};}
  function secretLike(o,depth=0){
    if(depth>12)return true;
    if(typeof o==='string')return /-----BEGIN .*PRIVATE KEY-----|\bBearer\s+\S+|\bgh[pousr]_[A-Za-z0-9]{20,}|\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}/i.test(o);
    if(!o||typeof o!=='object')return false;
    return Object.keys(o).some(k=>/^(?:password|secret|access_token|refresh_token|private_key|authorization|payload|body|content)$/i.test(k.normalize('NFKC'))||secretLike(o[k],depth+1));
  }
  function queueProblem(q){
    if(!exact(q,['state','source_ref','observed_at','read_complete','error']))return true;
    if(!['HAS_WORK','EMPTY','ERROR','UNKNOWN'].includes(q.state)||!text(q.source_ref)||!text(q.observed_at,64)||!Number.isFinite(Date.parse(q.observed_at))||typeof q.read_complete!=='boolean')return true;
    if(q.state==='EMPTY'&&q.read_complete!==true)return true;
    if(q.state!=='ERROR')return q.error!==null;
    const keys=['failure_code','failed_predicate','required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'];
    return !exact(q.error,keys)||keys.some(k=>!text(q.error[k]));
  }
  function reviewProblem(r){
    if(!exact(r,['goal','inputs','evidence','facts','checks','continuity']))return 'REVIEW_SHAPE_INVALID';
    const g=r.goal;
    if(!exact(g,['task_id','state','cosv','handoff_ref','source_ref','source_revision'])||!text(g.task_id,256)||!text(g.state,128)||!text(g.cosv,128)||!text(g.handoff_ref)||!text(g.source_ref)||!REV.test(g.source_revision))return 'GOAL_SOURCE_INVALID';
    if(!list(r.inputs)||!unique(r.inputs,'input_id')||r.inputs.some(i=>!exact(i,['input_id','source_ref','source_revision','digest','filed_at'])||!text(i.input_id,256)||!text(i.source_ref)||!text(i.source_revision,256)||!DIGEST.test(i.digest)||!text(i.filed_at,64)||!Number.isFinite(Date.parse(i.filed_at))))return 'INPUT_IDENTITY_INVALID';
    if(!list(r.evidence)||!unique(r.evidence,'evidence_id')||r.evidence.some(e=>!exact(e,['evidence_id','source_ref','digest','state','filed_by','verified_by','verification_ref'])||!text(e.evidence_id,256)||!text(e.source_ref)||!DIGEST.test(e.digest)||!EVIDENCE.includes(e.state)||!text(e.filed_by,256)||(e.verified_by!==null&&!text(e.verified_by,256))||(e.verification_ref!==null&&!text(e.verification_ref))||(e.state==='VERIFIED'&&(!e.verified_by||e.verified_by===e.filed_by||!e.verification_ref))))return 'EVIDENCE_SUPPORT_INVALID';
    const evidenceIds=new Set(r.evidence.map(e=>e.evidence_id));
    if(!list(r.facts)||!unique(r.facts,'fact_id')||r.facts.some(f=>!exact(f,['fact_id','category','statement','evidence_state','work_state','evidence_refs'])||!text(f.fact_id,256)||!CATEGORIES.includes(f.category)||!text(f.statement)||!EVIDENCE.includes(f.evidence_state)||!WORK.includes(f.work_state)||!refs(f.evidence_refs,evidenceIds)||(['VERIFIED'].includes(f.evidence_state)&&(!f.evidence_refs.length||f.evidence_refs.some(id=>r.evidence.find(e=>e.evidence_id===id).state!=='VERIFIED')))||(f.work_state==='COMPLETED'&&!f.evidence_refs.length)))return 'FACT_SUPPORT_INVALID';
    const inputs=new Map(r.inputs.map(i=>[i.input_id,i]));
    if(!list(r.checks)||!unique(r.checks,'check_id')||r.checks.some(c=>!exact(c,['check_id','input_id','input_digest','source_revision','goal_revision','predicate','rule_revision','state','result_ref'])||!text(c.check_id,256)||!inputs.has(c.input_id)||!DIGEST.test(c.input_digest)||!text(c.source_revision,256)||!REV.test(c.goal_revision)||!text(c.predicate,256)||!text(c.rule_revision,256)||!['FILED','ERROR','UNKNOWN'].includes(c.state)||!text(c.result_ref)))return 'CHECK_IDENTITY_INVALID';
    if(!exact(r.continuity,['source_ref','next_step','required_owner','handoff_ref'])||Object.values(r.continuity).some(v=>!text(v)))return 'CONTINUITY_INVALID';
    return null;
  }
  function checkGroups(r){
    const groups=new Map();
    for(const c of r.checks){
      const input=r.inputs.find(i=>i.input_id===c.input_id);
      const current=input.digest===c.input_digest&&input.source_revision===c.source_revision&&r.goal.source_revision===c.goal_revision;
      const key=JSON.stringify([r.goal.task_id,c.goal_revision,c.input_id,c.input_digest,c.source_revision,c.predicate,c.rule_revision]);
      if(!groups.has(key))groups.set(key,{key,current,checks:[],state:c.state});
      const group=groups.get(key);group.checks.push(c);if(group.state!==c.state)group.state='CONFLICTING';
    }
    return Array.from(groups.values()).map(g=>Object.assign(g,{duplicate_count:g.checks.length-1,repeat_review:g.current&&g.state==='FILED'?'EXACT_VERSION_RESULT_FILED':'REVIEW_REQUIRED'}));
  }
  function evaluate(projection,context,now=Date.now()){
    if(!context||context.workspace_type!=='DEVELOPER'||context.kv_scope!=='ECOSYSTEM')return refusal('ECOSYSTEM_CONTEXT_NOT_SELECTED');
    if(!projection)return refusal('ECOSYSTEM_REVIEW_PROJECTION_NOT_OBSERVED');
    if(secretLike(projection))return refusal('CREDENTIAL_OR_PAYLOAD_REFUSED');
    const p=projection;
    if(!exact(p,['schema','workspace_type','kv_scope','kv_account','projection_metadata','queue','reviews','credential_material_present','provider_operation_authorized','workspace_grants_authority','authority_effect'])||p.schema!==SCHEMA||p.workspace_type!=='DEVELOPER'||p.kv_scope!=='ECOSYSTEM'||p.kv_account!=='stegverse@gmail.com')return refusal('ECOSYSTEM_PROJECTION_CONTEXT_MISMATCH');
    if(p.credential_material_present!==false||p.provider_operation_authorized!==false||p.workspace_grants_authority!==false||p.authority_effect!=='NONE')return refusal('PROJECTION_AUTHORITY_ASSERTED');
    const m=p.projection_metadata;
    if(!exact(m,['schema','observed_at','source_revision','provenance_ref','owner_principal_id','workspace_id','grant_state','authority_effect'])||m.schema!=='stegverse.kv.workspace-projection-metadata/v1'||!text(m.observed_at,64)||!text(m.provenance_ref)||!REV.test(m.source_revision)||!text(m.owner_principal_id,256)||!text(m.workspace_id,256)||m.authority_effect!=='NONE')return refusal('PROJECTION_METADATA_INVALID');
    if(!text(context.principal_id,256)||!text(context.workspace_id,256)||context.principal_id!==m.owner_principal_id||context.workspace_id!==m.workspace_id)return refusal('PRINCIPAL_OR_WORKSPACE_MISMATCH');
    if(m.grant_state!=='ACTIVE')return refusal('ECOSYSTEM_GRANT_NOT_ACTIVE');
    const age=(now-Date.parse(m.observed_at))/1000;
    if(!Number.isFinite(age)||age< -60)return refusal('PROJECTION_TIME_INVALID');
    if(queueProblem(p.queue)||Date.parse(p.queue.observed_at)>Date.parse(m.observed_at)+60000)return refusal('QUEUE_DISPOSITION_INVALID');
    if(!list(p.reviews,100)||p.reviews.some(r=>!object(r)||!object(r.goal))||!unique(p.reviews.map(r=>r.goal),'task_id'))return refusal('REVIEW_LIST_INVALID');
    for(const r of p.reviews){const problem=reviewProblem(r);if(problem)return refusal(problem);}
    return {schema:'stegverse.workspace.ecosystem-review/v1',state:age>86400?'STALE':'SOURCE_VIEW_READY',observed_at:m.observed_at,source_revision:m.source_revision,provenance_ref:m.provenance_ref,queue:JSON.parse(JSON.stringify(p.queue)),reviews:JSON.parse(JSON.stringify(p.reviews)).map(r=>Object.assign(r,{check_groups:checkGroups(r),unassessed_categories:CATEGORIES.filter(category=>!r.facts.some(f=>f.category===category))})),verification:'FILED_SUPPORT_ONLY_NOT_PAGE_VERIFIED',replay_status:'REPLAY_STATUS_UNKNOWN',action_eligible:false,authority_effect:'NONE'};
  }
  function selectFacts(review,evidence='ALL',work='ALL'){
    if(!review)return [];
    const missing=(review.unassessed_categories||[]).map(category=>({fact_id:'unassessed:'+category,category,statement:'No filed assessment for this category is included in the projection.',evidence_state:'UNKNOWN',work_state:'UNKNOWN',evidence_refs:[]}));
    return review.facts.concat(missing).filter(f=>(evidence==='ALL'||(evidence==='UNRESOLVED'?f.evidence_state!=='VERIFIED':f.evidence_state===evidence))&&(work==='ALL'||f.work_state===work));
  }
  function drafts(view,taskId){
    const r=view&&view.reviews&&view.reviews.find(x=>x.goal.task_id===taskId);
    if(!r||view.state==='WITHHELD')return null;
    const header='REVIEW DRAFT — unsubmitted; filed support only, not page verification.\nGoal: '+r.goal.task_id+'; recorded state: '+r.goal.state+'; COSV: '+r.goal.cosv+'.\nHandoff: '+r.goal.handoff_ref+'\nSource: '+r.goal.source_ref+' @ '+r.goal.source_revision+'\nProjection: '+view.provenance_ref+'; observed '+view.observed_at+'; '+view.state+'; '+view.replay_status+'.';
    const facts=r.facts.map(f=>'- '+f.category+': '+f.statement+' ['+f.evidence_state+' / '+f.work_state+']; evidence: '+(f.evidence_refs.map(id=>r.evidence.find(e=>e.evidence_id===id).source_ref).join(', ')||'NONE FILED'));
    const gaps=r.facts.filter(f=>f.evidence_state!=='VERIFIED'||f.work_state==='STILL_REQUIRED'||f.work_state==='UNKNOWN').map(f=>'- '+f.category+': '+f.statement+' ['+f.evidence_state+' / '+f.work_state+']');
    for(const category of r.unassessed_categories||[])gaps.push('- '+category+': no filed assessment in this projection [UNKNOWN / UNKNOWN]');
    const q=view.queue;
    const queue='Queue: '+q.state+'; '+q.source_ref+'; observed '+q.observed_at+'; complete read: '+q.read_complete+'.'+(q.error?'\n'+Object.entries(q.error).map(([k,v])=>k+': '+v).join('\n'):'');
    const next='Next step: '+r.continuity.next_step+'\nRequired owner: '+r.continuity.required_owner+'\nContinuity: '+r.continuity.source_ref+'\nHandoff: '+r.continuity.handoff_ref;
    const checks=r.check_groups.map(g=>'- '+g.checks[0].predicate+': '+g.repeat_review+'; '+g.state+'; duplicate rows '+g.duplicate_count+'; '+g.checks.map(c=>c.result_ref).join(', '));
    return {coordination_update:header+'\n'+queue+'\n'+facts.join('\n')+'\n'+next,issue_comment:header+'\n'+facts.join('\n')+'\n'+next,evidence_gaps:header+'\n'+(gaps.join('\n')||'No evidence gaps recorded in this projection; completeness beyond its scope is unknown.')+'\n'+queue,next_session:header+'\n'+next+'\nPrior checks (same-version matches are advisory; no new check is performed):\n'+(checks.join('\n')||'No prior checks projected.')};
  }
  const api={SCHEMA,CATEGORIES,evaluate,refusal,selectFacts,drafts,checkGroups};
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.StegVerseWorkspaceEcosystemReview=api;
})(typeof globalThis!=='undefined'?globalThis:this);
