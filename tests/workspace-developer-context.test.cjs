// Developer context (Site#1509 owner-approved scope, ChatGPT relay 6104968277): Code, Tasks, Build, Governance, Runtime,
// Evidence and AI Collaboration as a third WorkSpace context that is projection-only and ACTION BY MANIFEST. No developer
// KV projection is published yet, so every area is FAIL_CLOSED/UNAVAILABLE with its producer owner named; actions compose
// unsubmitted manifest request drafts; personal rows never appear in the developer context and developer drafts cannot be
// composed from other contexts; the AI collaborator is the same MyKV assistant, never an independent one.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const ui=read('assets/workspace.js'),caps=read('assets/workspace-capabilities.js'),panels=read('assets/workspace-panels.js'),search=read('assets/workspace-search.js'),auth=read('assets/workspace-session-authentication.js'),binding=read('assets/workspace-assistant-binding.js'),continuity=read('assets/workspace-assistant-continuity.js'),device=read('assets/workspace-device-continuity.js'),page=read('workspace.html'),workflow=read('.github/workflows/workspace-kv-binding-validation.yml');
const bootstrap=JSON.parse(read('data/workspace/bootstrap.json'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
const sb={};vm.createContext(sb);vm.runInContext(caps,sb);vm.runInContext(panels,sb);
const C=sb.StegVerseWorkspaceCapabilities,P=sb.StegVerseWorkspacePanels;
const DEV=['DEV_CODE','DEV_TASKS','DEV_BUILD','DEV_GOVERNANCE','DEV_RUNTIME','DEV_EVIDENCE','DEV_AI_COLLABORATION'];
const descs=bootstrap.capability_descriptors;const byCap=Object.fromEntries(descs.map(d=>[d.capability,d]));
const NOW=Date.parse('2026-10-11T04:00:00Z');

// 1. Bootstrap: a third mode and seven developer descriptors that assert nothing.
const mode=bootstrap.workspace_modes.find(m=>m.id==='developer');
check(mode&&mode.workspace_type==='DEVELOPER'&&mode.kv_context==='DEVELOPER_KV_PROJECTION'&&mode.label==='Developer Workspace','developer mode declared');
check(JSON.stringify(bootstrap.developer_gate_predicates)===JSON.stringify(['capability_scoped_principal_admitted','developer_kv_projection_observed','manifest_route_resolved','ai_collaboration_capability_policy_bound','evidence_projection_observed']),'developer gate predicates');
for(const cap of DEV){const d=byCap[cap];check(d&&C.descriptorProblem(d)===null&&d.workspace_types.join()==='DEVELOPER'&&d.allowed_projection_schemas.length===0&&d.default_state==='NOT_OBSERVED'&&d.authority_effect==='NONE','developer descriptor valid and non-asserting: '+cap);}
check(descs.filter(d=>d.workspace_types.includes('DEVELOPER')).length===7,'exactly the seven developer areas are defined for the DEVELOPER context');
check(descs.filter(d=>!d.workspace_types.includes('DEVELOPER')).every(d=>d.workspace_types.every(t=>t==='PERSONAL'||t==='ORGANIZATIONAL')),'no personal/org descriptor leaks into the developer context');

// 2. Capability status: developer areas are UNAVAILABLE in DEVELOPER (no KV contract) and not defined elsewhere; personal families are not defined in DEVELOPER.
const REV='a'.repeat(64);
const personal={schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',state:'KV_WORKSPACE_PROJECTED',principals:[{principal_id:'user:alice',principal_type:'HUMAN',display_name:'Alice'}],organizations:[],memberships:[],feed:[{id:'f1',text:'hello',visibility:'PERSONAL'}],assistant:null,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,authority_effect:'NONE',projection_metadata:{schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-11T03:59:00Z',source_revision:REV,provenance_ref:'kv-workspace-source:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',grant_state:'UNKNOWN',authority_effect:'NONE'}};
for(const cap of DEV){const s=C.evaluate(byCap[cap],null,'DEVELOPER',NOW);check(s.state==='UNAVAILABLE'&&s.predicate==='NO_KV_PROJECTION_CONTRACT','developer area has no KV contract yet: '+cap+' '+s.predicate);const p=C.evaluate(byCap[cap],personal,'PERSONAL',NOW);check(p.state==='UNAVAILABLE'&&(p.predicate==='CAPABILITY_NOT_DEFINED_FOR_CONTEXT'||p.predicate==='NO_KV_PROJECTION_CONTRACT'),'developer area unavailable in PERSONAL: '+cap);}
// A forged developer projection cannot light an area: descriptors allow no schema.
const forged={schema:'stegverse.kv.developer-workspace-projection/v1',workspace_type:'DEVELOPER',code:[{repo:'x'}],build:[{run:1}],authority_effect:'NONE',workspace_grants_authority:false,projection_metadata:{observed_at:'2026-10-11T03:59:00Z'}};
for(const cap of DEV){const s=C.evaluate(byCap[cap],forged,'DEVELOPER',NOW);check(s.state!=='OBSERVED'&&s.state!=='STALE'&&s.state!=='FRESHNESS_UNKNOWN','forged developer projection must not be observed: '+cap+' '+s.state);}
for(const cap of ['FEED','CONTACTS','TASKS','CRYPTOBOT_PORTFOLIO','AI_ASSISTANT']){const s=C.evaluate(byCap[cap],personal,'DEVELOPER',NOW);check(s.state==='UNAVAILABLE'&&s.predicate==='CAPABILITY_NOT_DEFINED_FOR_CONTEXT'&&C.withholdsRows(s)===false,'personal family not defined in DEVELOPER: '+cap);}
// Panels name a producer owner for every developer area; governance cites #3012 as read-only/proposal; AI collaboration names the same assistant.
const built=P.build({descriptors:descs,statuses:C.evaluateAll(descs,[],'DEVELOPER',NOW),projections:[],workspace_type:'DEVELOPER'});
const pm=Object.fromEntries(built.panels.map(p=>[p.capability,p]));
for(const cap of DEV){check(pm[cap].rows_withheld===true&&pm[cap].rows.length===0&&typeof pm[cap].producer_owner==='string'&&pm[cap].producer_owner.length>0,'developer panel withholds rows and names a producer: '+cap);}
check(/\.github#3012/.test(pm.DEV_GOVERNANCE.producer_owner)&&/read-only/.test(pm.DEV_GOVERNANCE.producer_owner)&&/P1/.test(pm.DEV_GOVERNANCE.producer_owner),'governance producer is #3012, read-only, proposal only');
check(/same MyKV assistant/.test(pm.DEV_AI_COLLABORATION.producer_owner)&&/ECOSYSTEM-INGRESS-AI-BOUNDARIES-001/.test(pm.DEV_AI_COLLABORATION.producer_owner),'AI collaboration is the same assistant under the canonical capability-scoped policy owner');
check(/canonical Task Registry/.test(pm.DEV_TASKS.producer_owner)&&/task_registry_event_sovereign_kv_binding/.test(pm.DEV_TASKS.producer_owner),'developer tasks reuse the canonical Task Registry custody path');
check(built.panels.filter(p=>!DEV.includes(p.capability)).every(p=>p.state==='UNAVAILABLE'&&p.rows_withheld===true),'personal/org panels withheld in DEVELOPER context');

// 3. Page source and layout.
check(/<option value="developer">Developer Workspace<\/option>/.test(page)&&/data-target="developerCard">Developer</.test(page)&&/<section class="card full" id="developerCard"><h2>Developer<\/h2><div id="developer"><\/div><\/section>/.test(page),'select option, nav target and card');
check(ui.includes('state.mode==="developer"?"DEVELOPER"')&&ui.includes('DEVELOPER_KV_PROJECTION_NOT_OBSERVED')&&ui.includes('AI_COLLABORATION_CAPABILITY_SCOPE_NOT_BOUND')&&ui.includes('CAPABILITY_SCOPED_PRINCIPAL_NOT_ADMITTED'),'page names the developer predicates');
check(!/localStorage|sessionStorage|indexedDB|registerDevice/.test(ui)&&!/api\.github\.com|github\.com\/[A-Za-z]/.test(ui),'no storage, no registration, no direct GitHub read');
check(workflow.includes('tests/workspace-developer-context.test.cjs')&&workflow.includes('node tests/workspace-developer-context.test.cjs'),'workflow runs the developer context test');

// 4. UI harness: isolation, gate, developer card, manifest drafts.
const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities','searchResults','tasks','deviceContinuity','developer'];
const live=(p)=>{p.projection_metadata.observed_at=new Date(Date.now()-60000).toISOString().replace(/\.\d{3}Z$/,'Z');return p;};
function harness(opts){const els={};ids.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
  const docListeners={};const bridge={loadPersonalWorkspace:()=>Promise.resolve(live(JSON.parse(JSON.stringify(Object.assign({},personal,{assistant:{principal_id:'auri:primary',principal_type:'AI_ENTITY',display_name:'Auri',roles:['WORKSPACE_ASSISTANT'],ai_label_required:true,authority_effect:'NONE'}}))))),lastNodeBinding:()=>null};
  const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener:(t,f)=>{docListeners[t]=f}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{StegVerseWorkspaceKVBridge:bridge}};
  vm.createContext(ctx);for(const s of [caps,search,panels,auth,binding,continuity,device])vm.runInContext(s,ctx);
  ['StegVerseWorkspaceCapabilities','StegVerseWorkspaceSearch','StegVerseWorkspacePanels','StegVerseWorkspaceSessionAuthentication','StegVerseWorkspaceAssistantBinding','StegVerseWorkspaceAssistantContinuity','StegVerseWorkspaceDeviceContinuity'].forEach(k=>{ctx.window[k]=ctx[k];});
  vm.runInContext(ui,ctx);
  const click=(attrs)=>docListeners.click({target:{closest:sel=>sel==='[data-developer-action]'&&attrs.developerAction?{dataset:attrs}:sel==='[data-action]'&&attrs.action?{dataset:attrs}:null}});
  return {els,click,type:v=>{els.search.value=v;els.search.listeners.input({target:{value:v}})},switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}})};}
(async()=>{
  const wait=()=>new Promise(r=>setTimeout(r,10));
  const h=harness({});await wait();
  check(h.els.contacts.innerHTML.includes('Alice')&&h.els.developer.innerHTML.includes('Developer context not active'),'personal context renders personal rows and no developer card content');
  // Developer drafts cannot be composed from the personal context.
  h.click({developerAction:'DEVELOPER_BUILD_REQUEST'});check(h.els.intentDraft.innerHTML==='','no developer draft from personal context');
  h.switchTo('developer');
  check(h.els.contextTitle.textContent==='Developer Workspace'&&h.els.workspaceRuntimeState.textContent.startsWith('FAIL_CLOSED · DEVELOPER_KV_PROJECTION_NOT_OBSERVED'),'developer title and runtime state: '+h.els.workspaceRuntimeState.textContent);
  check(!h.els.contacts.innerHTML.includes('Alice')&&!h.els.feed.innerHTML.includes('hello')&&!h.els.tasks.innerHTML.includes('OBSERVED'),'personal rows hidden in developer context');
  const gate=h.els.kvGate.innerHTML;check(gate.includes('Developer-KV')&&gate.includes('DEVELOPER_KV_PROJECTION_NOT_OBSERVED')&&gate.includes('capability_scoped_principal_admitted: NOT_OBSERVED')&&gate.includes('evidence_projection_observed: NOT_OBSERVED')&&gate.includes('ACTION BY MANIFEST')&&!gate.includes('Org-Emp-KV'),'developer gate: '+gate.slice(0,400));
  const dev=h.els.developer.innerHTML;
  for(const area of ['CODE','TASKS','BUILD','GOVERNANCE','RUNTIME','EVIDENCE','AI_COLLABORATION'])check(dev.includes('<strong>'+area+'</strong> <span class="pill warn">UNAVAILABLE</span> NO_KV_PROJECTION_CONTRACT'),'developer area row: '+area);
  check(dev.includes('CAPABILITY_SCOPED_PRINCIPAL_NOT_ADMITTED')&&dev.includes('data-developer-action="DEVELOPER_BUILD_REQUEST"')&&dev.includes('data-developer-action="DEVELOPER_CODE_CHANGE_REQUEST"')&&dev.includes('data-developer-action="DEVELOPER_TASK_CHECKOUT_REQUEST"')&&dev.includes('data-developer-action="DEVELOPER_RUNTIME_OBSERVATION_REQUEST"')&&dev.includes('data-developer-action="DEVELOPER_AI_COLLABORATION_REQUEST"')&&!dev.includes('data-developer-action="DEVELOPER_GOVERNANCE')&&!/<span class="pill ok">/.test(dev),'developer card actions: '+dev.slice(0,600));
  check(dev.includes('read-only; no action is defined')&&dev.includes('never reads GitHub directly'),'governance and evidence are read-only with no action');
  const caps_html=h.els.capabilities.innerHTML;check(caps_html.includes('Code (developer)')&&caps_html.includes('Producer: StegVerse-Labs/.github#3012')&&!caps_html.includes('<div class="panel-rows">'),'capabilities card lists developer areas with producers and no rows: '+caps_html.slice(0,300));
  const asst=h.els.assistant.innerHTML;check(asst.includes('AI_COLLABORATION_CAPABILITY_SCOPE_NOT_BOUND')&&asst.includes('same MyKV assistant')&&!asst.includes('Bound to this session')&&asst.includes('FORBIDDEN'),'developer assistant message: '+asst.slice(0,500));
  // Manifest draft composition: FAIL_CLOSED, unsubmitted, manifest not admitted.
  h.click({developerAction:'DEVELOPER_BUILD_REQUEST'});let draft=h.els.intentDraft.innerHTML;
  check(draft.includes('DEVELOPER_BUILD_REQUEST request draft')&&draft.includes('FAIL_CLOSED')&&draft.includes('WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND')&&draft.includes('&quot;manifest_required&quot;: true')&&draft.includes('&quot;manifest_admitted&quot;: false')&&draft.includes('&quot;submitted&quot;: false')&&draft.includes('&quot;workspace_type&quot;: &quot;DEVELOPER&quot;')&&draft.includes('&quot;developer_area&quot;: &quot;BUILD&quot;')&&draft.includes('&quot;capability_state_at_draft&quot;: &quot;UNAVAILABLE&quot;')&&draft.includes('CAPABILITY_SCOPED_PRINCIPAL_NOT_ADMITTED')&&draft.includes('NONE_REQUEST_ONLY'),'build manifest draft: '+draft.slice(0,700));
  check(!/started|succeeded|completed|ALLOW&quot;/i.test(draft),'draft must not claim execution');
  h.els.intentDraft.innerHTML='';h.click({developerAction:'DEVELOPER_MERGE_NOW'});check(h.els.intentDraft.innerHTML==='','unknown developer action yields no draft');
  h.click({developerAction:'DEVELOPER_AI_COLLABORATION_REQUEST'});draft=h.els.intentDraft.innerHTML;check(draft.includes('DEVELOPER_AI_COLLABORATION_REQUEST')&&draft.includes('&quot;capability&quot;: &quot;DEV_AI_COLLABORATION&quot;')&&draft.includes('FAIL_CLOSED'),'AI collaboration draft is a manifest request only');
  // Personal contact actions are not reachable from the developer context; search returns nothing personal.
  h.els.intentDraft.innerHTML='';h.click({action:'message',id:'user:alice'});check(h.els.intentDraft.innerHTML==='','personal contact action blocked in developer context');
  h.type('Alice');check(!h.els.searchResults.innerHTML.includes('Alice'),'search in developer context returns no personal rows');
  // Switching back restores personal rows and clears the developer draft.
  h.click({developerAction:'DEVELOPER_BUILD_REQUEST'});h.switchTo('personal');check(h.els.contacts.innerHTML.includes('Alice')&&h.els.intentDraft.innerHTML===''&&h.els.developer.innerHTML.includes('Developer context not active'),'switch back to personal');
  console.log('WORKSPACE_DEVELOPER_CONTEXT_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
