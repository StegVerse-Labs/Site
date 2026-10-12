// Tasks/commitments consumer (Site#1509 WS-TASKS): presentation of the read-only tasks projection with provenance,
// timeline order, revocation handling, and proposed-action composition that never executes anything.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
const caps=fs.readFileSync(path.join(root,'assets/workspace-capabilities.js'),'utf8');
const search=fs.readFileSync(path.join(root,'assets/workspace-search.js'),'utf8');
const page=fs.readFileSync(path.join(root,'workspace.html'),'utf8');
const bootstrap=JSON.parse(fs.readFileSync(path.join(root,'data/workspace/bootstrap.json'),'utf8'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
assert(/<section class="card" id="tasksCard"><h2>Tasks &amp; commitments<\/h2><div id="tasks"><\/div><\/section>/.test(page)&&/data-target="tasksCard">Tasks</.test(page),'tasks card and nav target');
const byCap={};bootstrap.capability_descriptors.forEach(d=>byCap[d.capability]=d);
assert(byCap.TASKS.projection_field==='tasks'&&byCap.COMMITMENTS.projection_field==='commitments'&&byCap.TASKS.allowed_projection_schemas[0]==='stegverse.kv.workspace-tasks-projection/v1'&&byCap.TASKS.default_state==='NOT_OBSERVED'&&byCap.TASKS.authority_effect==='NONE','descriptors bound to the producer contract and non-asserting');
assert(!/localStorage|sessionStorage|indexedDB/.test(ui),'no browser storage');
assert(ui.includes('typeof bridge.loadPersonalTasks!=="function"')&&ui.includes('applyTasksProjection(null)'),'tasks projection only through the bridge seam; absent -> not observed');

// Read-only fixture shaped exactly as continuity-vault-kit runtime/workspace_tasks_projection.py emits it.
const REV='b'.repeat(64);
const meta=(extra)=>Object.assign({schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:new Date(Date.now()-60000).toISOString().replace(/\.\d{3}Z$/,'Z'),observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:REV,provenance_ref:'kv-workspace-tasks-source:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'},extra||{});
const row=(o)=>Object.assign({action_eligible:false,execution_requires_admitted_manifest:true,authority_effect:'NONE'},o);
function tasksProjection(extra){return Object.assign({schema:'stegverse.kv.workspace-tasks-projection/v1',state:'KV_TASKS_PROJECTED',workspace_type:'PERSONAL',
  tasks:[row({task_id:'t-2',title:'Review aurora release',status:'OPEN',due_at:'2026-10-12T09:00:00Z',created_at:null,source_ref:'kv:tasks/t-2'}),row({task_id:'t-1',title:'Undated chore',status:'IN_PROGRESS',due_at:null,created_at:null,source_ref:null})],
  commitments:[row({commitment_id:'c-1',statement:'Send Alice the draft',status:'ACTIVE',counterparty_principal_id:'user:alice',due_at:'2026-10-11T18:00:00Z',source_ref:null}),row({commitment_id:'c-2',statement:'Old promise',status:'REVOKED',counterparty_principal_id:null,due_at:'2026-10-01T00:00:00Z',source_ref:null})],
  timeline:[row({kind:'commitment',id:'c-2',label:'Old promise',status:'REVOKED',due_at:'2026-10-01T00:00:00Z'}),row({kind:'commitment',id:'c-1',label:'Send Alice the draft',status:'ACTIVE',due_at:'2026-10-11T18:00:00Z'}),row({kind:'task',id:'t-2',label:'Review aurora release',status:'OPEN',due_at:'2026-10-12T09:00:00Z'}),row({kind:'task',id:'t-1',label:'Undated chore',status:'IN_PROGRESS',due_at:null})],
  credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,action_authority:'NONE',projection_metadata:meta(),authority_effect:'NONE'},extra||{});}
const personal={schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',state:'KV_WORKSPACE_PROJECTED',principals:[{principal_id:'user:alice',principal_type:'HUMAN',display_name:'Alice'}],organizations:[],memberships:[],feed:[],assistant:null,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,authority_effect:'NONE',projection_metadata:meta({provenance_ref:'kv-workspace-source:sha256:'+REV})};

const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities','searchResults','tasks'];
function harness(tasksProj,bridgeExtra){const els={};ids.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
  const docListeners={};const bridge=Object.assign({loadPersonalWorkspace:()=>Promise.resolve(JSON.parse(JSON.stringify(personal))),lastNodeBinding:()=>null},tasksProj===undefined?{}:{loadPersonalTasks:()=>Promise.resolve(tasksProj)},bridgeExtra||{});
  const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener:(t,f)=>{docListeners[t]=f}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{StegVerseWorkspaceKVBridge:bridge}};
  vm.createContext(ctx);vm.runInContext(caps,ctx);vm.runInContext(search,ctx);ctx.window.StegVerseWorkspaceCapabilities=ctx.StegVerseWorkspaceCapabilities;ctx.window.StegVerseWorkspaceSearch=ctx.StegVerseWorkspaceSearch;vm.runInContext(ui,ctx);
  const click=(attrs)=>docListeners.click({target:{closest:sel=>sel==='[data-task-action]'&&attrs.taskAction?{dataset:attrs}:sel==='[data-action]'&&attrs.action?{dataset:attrs}:null}});
  return {els,click,type:v=>{els.search.value=v;els.search.listeners.input({target:{value:v}})},switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}})};}
(async()=>{
  // Read-only fixture renders rows, timeline order and provenance; the projection object is not mutated.
  const proj=tasksProjection();const frozen=JSON.stringify(proj);
  let h=harness(proj);await new Promise(r=>setTimeout(r,10));
  let html=h.els.tasks.innerHTML;
  assert(JSON.stringify(proj)===frozen,'consumer must not mutate the projection');
  assert(html.includes('Tasks: OBSERVED')&&html.includes('Commitments: OBSERVED')&&html.includes('provenance kv-workspace-tasks-source:sha256:'+REV)&&html.includes('REPLAY_STATUS_UNKNOWN'),'provenance line: '+html);
  const order=['Old promise','Send Alice the draft','Review aurora release','Undated chore'].map(l=>html.indexOf(l));
  assert(order.every((v,i)=>v>=0&&(i===0||v>order[i-1])),'timeline keeps the producer order: '+order.join(','));
  assert(html.includes('Timeline (derived order only; not a schedule)'),'timeline labelled as derived order');
  assert(html.includes('execution requires an admitted manifest (action_eligible: false)')&&html.includes('data-task-action="complete" data-task-id="t-2"'),'task rows present with propose button');
  assert(html.includes('revoked: no action may be proposed')&&!html.includes('data-commitment-id="c-2"')&&html.includes('data-commitment-id="c-1"'),'revoked commitment shown as REVOKED without an action button');
  assert(h.els.capabilities.innerHTML.includes('Tasks')&&h.els.capabilities.innerHTML.includes('Commitments'),'capability card lists tasks and commitments');
  // Proposed-action composition: only an unsubmitted FAIL_CLOSED draft bound to the row's provenance; status unchanged.
  h.click({taskAction:'complete',taskId:'t-2'});
  let draft=h.els.intentDraft.innerHTML;
  assert(draft.includes('TASK_COMPLETE request draft')&&draft.includes('FAIL_CLOSED')&&draft.includes('WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND'),'task draft: '+draft);
  assert(draft.includes('&quot;submitted&quot;: false')&&draft.includes('&quot;manifest_admitted&quot;: false')&&draft.includes('NONE_REQUEST_ONLY')&&draft.includes('&quot;target_task_id&quot;: &quot;t-2&quot;')&&draft.includes('&quot;target_status_at_draft&quot;: &quot;OPEN&quot;')&&draft.includes('kv-workspace-tasks-source:sha256:'+REV),'draft is non-authorizing and provenance-bound');
  assert(!/completed|done successfully|ALLOW&quot;/i.test(draft),'draft must not claim completion');
  assert(h.els.tasks.innerHTML.includes('Review aurora release')&&h.els.tasks.innerHTML.includes('<span class="pill">OPEN</span>'),'task status unchanged after proposing');
  h.click({taskAction:'withdraw',commitmentId:'c-1'});
  draft=h.els.intentDraft.innerHTML;assert(draft.includes('COMMITMENT_WITHDRAW')&&draft.includes('FAIL_CLOSED')&&draft.includes('&quot;target_commitment_id&quot;: &quot;c-1&quot;'),'commitment draft: '+draft);
  h.els.intentDraft.innerHTML='';h.click({taskAction:'withdraw',commitmentId:'c-2'});
  assert(h.els.intentDraft.innerHTML==='','revoked commitment yields no draft');
  h.click({taskAction:'complete',taskId:'nope'});assert(h.els.intentDraft.innerHTML==='','unknown task yields no draft');
  // Search finds tasks and commitments through the same contract with the tasks projection's provenance.
  h.type('aurora');assert(h.els.searchResults.innerHTML.includes('Review aurora release')&&h.els.searchResults.innerHTML.includes('TASKS · OBSERVED')&&h.els.searchResults.innerHTML.includes('kv-workspace-tasks-source'),'search surfaces tasks: '+h.els.searchResults.innerHTML);
  // Context separation: organizational context shows no personal tasks and offers no actions.
  h.switchTo('organizational');html=h.els.tasks.innerHTML;
  assert(!html.includes('aurora')&&!html.includes('Alice')&&html.includes('No admitted tasks or commitments')&&!html.includes('data-task-action'),'org context must not show personal tasks: '+html);
  h.click({taskAction:'complete',taskId:'t-2'});assert(h.els.intentDraft.innerHTML==='','org context cannot act on personal tasks');
  h.switchTo('personal');assert(h.els.tasks.innerHTML.includes('Review aurora release'),'personal tasks restored');
  // Revocation of the projection grant withholds every row and every action.
  h=harness(tasksProjection({projection_metadata:meta({grant_state:'REVOKED'})}));await new Promise(r=>setTimeout(r,10));
  html=h.els.tasks.innerHTML;
  assert(html.includes('Tasks: REVOKED')&&!html.includes('aurora')&&!html.includes('data-task-action'),'revoked grant withholds rows: '+html);
  h.click({taskAction:'complete',taskId:'t-2'});assert(h.els.intentDraft.innerHTML==='','revoked grant: no draft');
  // Stale projection: rows remain, labelled STALE.
  h=harness(tasksProjection({projection_metadata:meta({observed_at:'2026-10-01T00:00:00Z'})}));await new Promise(r=>setTimeout(r,10));
  assert(h.els.tasks.innerHTML.includes('Tasks: STALE')&&h.els.tasks.innerHTML.includes('Review aurora release'),'stale rows labelled');
  // Malformed or authority-asserting projection: withheld.
  h=harness(tasksProjection({authority_effect:'ALLOW'}));await new Promise(r=>setTimeout(r,10));
  assert(h.els.tasks.innerHTML.includes('Tasks: MALFORMED')&&!h.els.tasks.innerHTML.includes('aurora'),'authority-asserting projection withheld');
  // No bridge method: NOT_OBSERVED, nothing rendered, nothing read from elsewhere.
  h=harness(undefined);await new Promise(r=>setTimeout(r,10));
  assert(h.els.tasks.innerHTML.includes('Tasks: NOT_OBSERVED')&&h.els.tasks.innerHTML.includes('No admitted tasks or commitments'),'absent projection is NOT_OBSERVED: '+h.els.tasks.innerHTML);
  // A failing loader is the same as absent.
  h=harness(null,{loadPersonalTasks:()=>Promise.reject(new Error('FAIL_CLOSED: no tasks path'))});await new Promise(r=>setTimeout(r,10));
  assert(h.els.tasks.innerHTML.includes('Tasks: NOT_OBSERVED'),'failing loader is not observed');
  // Card-level display bounds (Site#1509, same rule as the #1555 panel adapters): a row whose visible text has hidden
  // characters or exceeds the bound is withheld from the card and counted; valid rows still render; the projection is untouched.
  {const bad=tasksProjection();
   bad.tasks.push(row({task_id:'t-bidi',title:'Pay inv\u202Eoice',status:'OPEN',due_at:null,source_ref:null}),row({task_id:'t-long',title:'x'.repeat(257),status:'OPEN',due_at:null,source_ref:null}),row({task_id:'t-zw',title:'Hidden',status:'OP\u200BEN',due_at:null,source_ref:null}),row({task_id:'t-src',title:'Bad source',status:'OPEN',due_at:null,source_ref:'kv:\u0007'}));
   bad.commitments.push(row({commitment_id:'c-bidi',statement:'Refund \u2066Bob',status:'ACTIVE',counterparty_principal_id:null,due_at:null,source_ref:null}),row({commitment_id:'c-cp',statement:'Call',status:'ACTIVE',counterparty_principal_id:'user:\u2028x',due_at:null,source_ref:null}));
   bad.timeline.push(row({kind:'task',id:'t-bidi',label:'Pay inv\u202Eoice',status:'OPEN',due_at:null}),row({kind:'task',id:'t-due',label:'Due',status:'OPEN',due_at:7}));
   const before=JSON.stringify(bad);
   const hb=harness(bad);await new Promise(r=>setTimeout(r,10));const card=hb.els.tasks.innerHTML;
   assert(JSON.stringify(bad)===before,'bounding must not mutate the projection');
   assert(!/[\u202E\u200B\u2066\u2028\u0007]/.test(card)&&!card.includes('x'.repeat(257))&&!card.includes('Bad source')&&!card.includes('data-task-id="t-bidi"')&&!card.includes('data-commitment-id="c-cp"'),'hidden or overlong rows must not reach the card: '+card);
   assert(card.includes('8 row(s) withheld: text not displayable'),'withheld rows are counted on the card: '+card);
   assert(card.includes('Review aurora release')&&card.includes('Send Alice the draft')&&card.includes('data-task-id="t-2"'),'valid rows still render beside withheld ones');}
  console.log('WORKSPACE_TASKS_PASS');
})().catch(e=>{console.error(e);process.exit(1)});
