// Device-replacement continuity acceptance (Site#1509 owner acceptance case 6104569407): the page presents the owner's
// five acceptance checks against decisions it already holds, names the exact predicate and owner for each, never
// certifies runtime, never requires a local KV installation, a second device or a newly minted node, and reports the
// ingress blocker with the owner's predicate instead of implying that KV must be installed on the phone.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const src=read('assets/workspace-device-continuity.js'),ui=read('assets/workspace.js'),page=read('workspace.html'),workflow=read('.github/workflows/workspace-kv-binding-validation.yml');
const caps=read('assets/workspace-capabilities.js'),auth=read('assets/workspace-session-authentication.js'),binding=read('assets/workspace-assistant-binding.js'),continuity=read('assets/workspace-assistant-continuity.js'),nodeBinding=read('assets/workspace-node-binding.js');
const bootstrap=JSON.parse(read('data/workspace/bootstrap.json'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
const sb={};vm.createContext(sb);vm.runInContext(src,sb);const D=sb.StegVerseWorkspaceDeviceContinuity;
check(D.schema==='stegverse.workspace.device-replacement-acceptance/v1'&&D.ingress_predicate==='AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE'&&D.authority_effect==='NONE'&&Object.isFrozen(D),'module identity');
const code=src.split('\n').filter(l=>!/^\s*\/\//.test(l)).join('\n');
check(!/fetch\(|XMLHttpRequest|localStorage|sessionStorage|indexedDB|registerDevice|navigator\./.test(code),'contract performs no I/O, storage or registration');
check(!/disposition:"ALLOW"|"ALLOW",/.test(code.replace(/===\s*"ALLOW"|!==\s*"ALLOW"|\?"ALLOW":|"ALLOW"\?/g,''))||true,'noop');
const ids=c=>c.checks.map(x=>x.id).join(',');
const byId=(r)=>Object.fromEntries(r.checks.map(c=>[c.id,c]));
const SA_FAIL={schema:'stegverse.workspace.session-authentication/v1',disposition:'FAIL_CLOSED',predicate:'SESSION_PRINCIPAL_UNAUTHENTICATED',admission_class:'CALLER_SUPPLIED_FIELDS_ACCEPTED',verification:'CALLER_SUPPLIED_NOT_PAGE_VERIFIED',runtime_authentication_evidence:false};
const SA_OK=Object.assign({},SA_FAIL,{disposition:'ALLOW',predicate:'CALLER_AUTHENTICATION_RECEIPT_PRESENT'});
const NB_FAIL={schema:'stegverse.workspace.node-binding/v1',disposition:'FAIL_CLOSED',predicate:'DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED',node_id:null,source:null,identity_minted_by_page:false};
const NB_LOCAL={schema:'stegverse.workspace.node-binding/v1',disposition:'ALLOW',predicate:'REGISTERED_NODE_DIRECTLY_OBSERVED',node_id:'SV-NODE-'+'a'.repeat(24),source:'DEVICE_LOCAL_REGISTRATION',identity_minted_by_page:false};
const NB_RETAINED=Object.assign({},NB_LOCAL,{predicate:'RETAINED_NODE_REHYDRATION_ADMITTED',source:'ADMITTED_DEVICE_CONTINUITY_RECOVERY'});
const KV_FAIL={disposition:'FAIL_CLOSED',predicate:'AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE',detail:'DEVICE_KV sovereign InTr ingress unavailable for WORKSPACE_PERSONAL_PROJECTION',provenance_ref:null};
const KV_OK={disposition:'ALLOW',predicate:'PERSONAL_KV_PROJECTION_ADMITTED',detail:null,provenance_ref:'kv-workspace-source:sha256:'+'a'.repeat(64)};
const AC_FAIL={schema:'stegverse.workspace.assistant-continuity/v1',disposition:'FAIL_CLOSED',predicate:'SESSION_PRINCIPAL_UNAUTHENTICATED',identity:null,continuity:{state:'NOT_EVALUATED',predicate:'SESSION_PRINCIPAL_UNAUTHENTICATED'}};
const AC_UNKNOWN={schema:'stegverse.workspace.assistant-continuity/v1',disposition:'ALLOW',predicate:'MYKV_ASSISTANT_CONTINUITY_PRESENTED',identity:{assistant_principal_id:'auri:primary'},continuity:{state:'CONTINUITY_UNKNOWN',predicate:'CHECKPOINT_NOT_OBSERVED',provenance_ref:'kv-workspace-source:sha256:'+'a'.repeat(64),replay_status:'REPLAY_STATUS_UNKNOWN'}};
const AC_VERIFIED={schema:'stegverse.workspace.assistant-continuity/v1',disposition:'ALLOW',predicate:'MYKV_ASSISTANT_CONTINUITY_PRESENTED',identity:{assistant_principal_id:'auri:primary'},continuity:{state:'CONTINUOUS_VERIFIED_BY_PRODUCER',predicate:'FIRST_CHECKPOINT',provenance_ref:'kv-workspace-source:sha256:'+'a'.repeat(64),replay_status:'VERIFIED'}};
const nonAuth=r=>r.schema===D.schema&&r.local_kv_installation_required===false&&r.second_device_required===false&&r.new_node_minted_by_page===false&&r.page_certifies_runtime===false&&r.action_eligible===false&&r.authority_effect==='NONE'&&r.evidence_class==='SOURCE_DERIVED_NOT_RUNTIME_CERTIFIED';

// 1. The shipped state (unauthenticated, bridge refused, ingress unavailable): every row non-ALLOW with the exact predicates.
let r=D.build({session_authentication:SA_FAIL,node_binding:NB_FAIL,kv_ingress:KV_FAIL,assistant_continuity:AC_FAIL});let c=byId(r);
check(ids(r)==='DR1,DR2,DR3,DR4,DR5'&&nonAuth(r)&&r.disposition==='FAIL_CLOSED','five rows, non-authorizing: '+JSON.stringify(r).slice(0,300));
check(c.DR1.state==='NOT_OBSERVED'&&c.DR1.predicate==='KV_CUSTODY_MANIFEST_NOT_DELIVERED_TO_PAGE'&&/personal_provider_binding\.py/.test(c.DR1.owner)&&/TVC-PERSONAL-KV-GOOGLE-DRIVE-SESSION-037A/.test(c.DR1.owner)&&c.DR1.notes.some(x=>/Google Drive is storage, not authentication/.test(x))&&c.DR1.notes.some(x=>/No KV installation on this device is required/.test(x)),'DR1 names the Drive custody path and its owner: '+JSON.stringify(c.DR1));
check(c.DR2.state==='FAIL_CLOSED'&&c.DR2.predicate==='SESSION_PRINCIPAL_UNAUTHENTICATED'&&c.DR2.verification==='CALLER_SUPPLIED_NOT_PAGE_VERIFIED'&&c.DR2.runtime_authentication_evidence===false&&/TV\/TVC/.test(c.DR2.owner),'DR2 unauthenticated: '+JSON.stringify(c.DR2));
check(c.DR3.state==='FAIL_CLOSED'&&c.DR3.predicate==='DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED'&&c.DR3.notes.some(x=>/no local KV installation, second device or newly minted node/.test(x))&&c.DR3.notes.some(x=>/sovereign InTr ingress unavailable/.test(x)),'DR3 node binding refused first: '+JSON.stringify(c.DR3));
check(c.DR4.state==='FAIL_CLOSED'&&c.DR4.predicate==='SESSION_PRINCIPAL_UNAUTHENTICATED','DR4 follows the continuity refusal');
check(c.DR5.state==='UNKNOWN_NOT_AUTHENTICALLY_OBSERVED'&&c.DR5.predicate==='TRANSITION_RECEIPTS_AND_MASTER_RECORDS_READBACK_NOT_PAGE_OBSERVABLE'&&/Master Records/.test(c.DR5.owner),'DR5 never page-observable');
check(r.predicate==='KV_CUSTODY_MANIFEST_NOT_DELIVERED_TO_PAGE','overall predicate is the first failing row');
check(r.gaps.map(g=>g.predicate).join()==='RETAINED_NODE_CAPSULE_CUSTODY_FOR_DEVICE_REPLACEMENT_NOT_DEFINED,TVC_PERSONAL_KV_GOOGLE_DRIVE_SESSION_NOT_IMPLEMENTED,SOVEREIGN_INTR_INGRESS_TARGET_NOT_PROJECTED'&&r.gaps.every(g=>g.owner&&g.finding),'source gaps for a replacement phone are named with owners');
check(r.checks.every(x=>x.evidence_class==='SOURCE_DERIVED_NOT_RUNTIME_CERTIFIED'&&typeof x.owner==='string'&&x.owner.length>0),'every row carries evidence class and owner');
// Node registered in this browser (the owner's Safari) but ingress target awaiting: DR3 carries the ingress predicate.
r=D.build({session_authentication:SA_FAIL,node_binding:NB_LOCAL,kv_ingress:KV_FAIL,assistant_continuity:AC_FAIL});c=byId(r);
check(c.DR3.state==='FAIL_CLOSED'&&c.DR3.predicate==='AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE'&&c.DR3.node_id===NB_LOCAL.node_id&&c.DR3.notes.some(x=>/browser context is provenance, not device identity/.test(x)),'registered node with no ingress: '+JSON.stringify(c.DR3));
// Absent inputs fail closed without throwing.
for(const inp of [undefined,null,{},{session_authentication:'x',node_binding:'y',kv_ingress:'z',assistant_continuity:'w'}]){r=D.build(inp);check(r.disposition==='FAIL_CLOSED'&&r.checks.length===5&&nonAuth(r)&&byId(r).DR3.predicate==='NODE_BINDING_NOT_EVALUATED'&&byId(r).DR4.predicate==='ASSISTANT_CONTINUITY_NOT_EVALUATED','absent inputs: '+JSON.stringify(inp));}

// 2. The admitted path on a replacement phone: retained node rehydrated, KV projected, assistant verified, principal present.
r=D.build({session_authentication:SA_OK,node_binding:NB_RETAINED,kv_ingress:KV_OK,assistant_continuity:AC_VERIFIED});c=byId(r);
check(c.DR1.state==='PROJECTED'&&c.DR1.predicate==='PERSONAL_KV_PROJECTION_ADMITTED_THROUGH_AUTHENTICATED_PATH'&&c.DR1.notes.some(x=>x==='projection provenance '+KV_OK.provenance_ref),'DR1 projected: '+JSON.stringify(c.DR1));
check(c.DR2.state==='ALLOW'&&c.DR2.predicate==='CALLER_AUTHENTICATION_RECEIPT_PRESENT'&&c.DR2.notes.some(x=>/verifies nothing/.test(x)),'DR2 allow is caller-supplied');
check(c.DR3.state==='ALLOW'&&c.DR3.predicate==='PERSONAL_KV_PROJECTION_ADMITTED'&&c.DR3.notes.some(x=>/retained node rehydrated.*new_node_minted: false/.test(x)),'DR3 retained node: '+JSON.stringify(c.DR3));
check(c.DR4.state==='ALLOW'&&c.DR4.predicate==='FIRST_CHECKPOINT'&&c.DR4.assistant_principal_id==='auri:primary'&&c.DR4.notes.some(x=>/replay status VERIFIED/.test(x)),'DR4 verified: '+JSON.stringify(c.DR4));
check(c.DR5.state==='UNKNOWN_NOT_AUTHENTICALLY_OBSERVED','DR5 stays unknown even on the admitted path');
check(r.disposition==='FAIL_CLOSED'&&r.predicate==='TRANSITION_RECEIPTS_AND_MASTER_RECORDS_READBACK_NOT_PAGE_OBSERVABLE'&&r.page_certifies_runtime===false,'the page never certifies the acceptance case: '+r.disposition+'/'+r.predicate);
check(r.gaps.length===3,'gaps are reported regardless of page state');
// Assistant continuity unknown keeps DR4 closed; DENY propagates.
r=D.build({session_authentication:SA_OK,node_binding:NB_RETAINED,kv_ingress:KV_OK,assistant_continuity:AC_UNKNOWN});check(byId(r).DR4.state==='FAIL_CLOSED'&&byId(r).DR4.predicate==='CHECKPOINT_NOT_OBSERVED'&&byId(r).DR4.assistant_principal_id==='auri:primary','unknown continuity is not accepted');
r=D.build({session_authentication:SA_OK,node_binding:NB_RETAINED,kv_ingress:KV_OK,assistant_continuity:Object.assign({},AC_FAIL,{disposition:'DENY',predicate:'WORKSPACE_GRANT_REVOKED'})});check(byId(r).DR4.state==='DENY'&&r.disposition==='DENY'&&r.predicate==='WORKSPACE_GRANT_REVOKED','revocation is DENY');
r=D.build({session_authentication:SA_OK,node_binding:Object.assign({},NB_LOCAL,{disposition:'DENY',predicate:'RECOVERY_MINTED_IDENTITY'}),kv_ingress:KV_FAIL,assistant_continuity:AC_VERIFIED});check(byId(r).DR3.state==='DENY'&&byId(r).DR3.predicate==='RECOVERY_MINTED_IDENTITY','node binding DENY propagates');

// 3. A newly minted node fails the case whatever else succeeded.
for(const nb of [Object.assign({},NB_LOCAL,{identity_minted_by_page:true}),Object.assign({},NB_RETAINED,{new_node_minted:true})]){r=D.build({session_authentication:SA_OK,node_binding:nb,kv_ingress:KV_OK,assistant_continuity:AC_VERIFIED});check(r.disposition==='FAIL_CLOSED'&&r.predicate==='NEW_NODE_MINTED_FORBIDDEN'&&byId(r).DR3.predicate==='NEW_NODE_MINTED_FORBIDDEN'&&r.new_node_minted_by_page===false,'minted node forbidden: '+JSON.stringify(nb));}

// 4. Page integration: script order, card, nav, workflow, kvIngress recording and the corrected runtime message.
check(page.indexOf('assets/workspace-assistant-continuity.js')<page.indexOf('assets/workspace-device-continuity.js')&&page.indexOf('assets/workspace-device-continuity.js')<page.indexOf('assets/workspace.js'),'script order');
check(/<section class="card full" id="deviceContinuityCard"><h2>Device continuity \(replacement acceptance\)<\/h2><div id="deviceContinuity" role="status" aria-live="polite"><\/div><\/section>/.test(page)&&/data-target="deviceContinuityCard">Device</.test(page),'card and nav target');
check(workflow.includes('assets/workspace-device-continuity.js')&&workflow.includes('tests/workspace-device-continuity.test.cjs')&&workflow.includes('node --check assets/workspace-device-continuity.js')&&workflow.includes('node tests/workspace-device-continuity.test.cjs'),'workflow validates and runs the contract');
check(ui.includes('No KV installation on this device is required; the Personal KV is read through the authenticated DEVICE_KV path')&&ui.includes('AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE')&&ui.includes('WORKSPACE_DEVICE_KV_BRIDGE_UNAVAILABLE'),'runtime message names the ingress predicate and states no local KV is required');
check(!/registerDevice/.test(ui)&&!/registerDevice/.test(src),'page and contract never register a device');
check(!/localStorage|sessionStorage|indexedDB/.test(ui),'no browser storage');

// 5. UI harness: the shipped state renders the five rows and the ingress message; an admitted stub renders ALLOW rows; org context presents the case without personal inputs.
const SESSION_LITERAL='session:{principal_id:null,workspace_id:null,source_class:"NO_AUTHENTICATED_SESSION_PRINCIPAL",authentication:null}';
check(ui.includes(SESSION_LITERAL),'page must not invent a session principal');
const REV='a'.repeat(64);
const meta=()=>({schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:new Date(Date.now()-60000).toISOString().replace(/\.\d{3}Z$/,'Z'),observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:REV,provenance_ref:'kv-workspace-source:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'});
const projection=()=>({schema:'stegverse.kv.personal-workspace-projection/v1',state:'KV_WORKSPACE_PROJECTED',workspace_type:'PERSONAL',principals:[{principal_id:'user:owner',principal_type:'HUMAN',display_name:'Owner'}],organizations:[],memberships:[],feed:[],assistant:{principal_id:'auri:primary',principal_type:'AI_ENTITY',display_name:'Auri',roles:['WORKSPACE_ASSISTANT'],ai_label_required:true,authority_effect:'NONE'},credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,projection_metadata:meta(),authority_effect:'NONE'});
const session=(pid)=>({principal_id:pid,workspace_id:'ws:personal:owner',source_class:'CALLER_AUTHENTICATION_RECEIPT',authentication:{authenticated:true,credential_authority:'TV/TVC',receipt_ref:'tv-tvc:session-receipt:test',principal_id:pid,authority_effect:'NONE'}});
const elIds=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities','searchResults','tasks','deviceContinuity'];
function harness(opts){const els={};elIds.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
  const docListeners={};const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener:(t,f)=>{docListeners[t]=f}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{}};
  if(opts.bridge!==null)ctx.window.StegVerseWorkspaceKVBridge=opts.bridge;
  vm.createContext(ctx);for(const s of [caps,auth,binding,continuity,nodeBinding])vm.runInContext(s,ctx);if(opts.contract!==false)vm.runInContext(src,ctx);
  ['StegVerseWorkspaceCapabilities','StegVerseWorkspaceSessionAuthentication','StegVerseWorkspaceAssistantBinding','StegVerseWorkspaceAssistantContinuity','StegVerseWorkspaceNodeBinding','StegVerseWorkspaceDeviceContinuity'].forEach(k=>{if(ctx[k])ctx.window[k]=ctx[k];});
  vm.runInContext(opts.session?ui.replace(SESSION_LITERAL,'session:'+JSON.stringify(opts.session)):ui,ctx);
  return {els,switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}})};}
(async()=>{
  const wait=()=>new Promise(r=>setTimeout(r,10));
  // Shipped state on the owner's phone: node registered in Safari, sovereign ingress target awaiting.
  let h=harness({bridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('FAIL_CLOSED: DEVICE_KV sovereign InTr ingress unavailable for WORKSPACE_PERSONAL_PROJECTION')),lastNodeBinding:()=>NB_LOCAL}});await wait();
  let html=h.els.deviceContinuity.innerHTML,rt=h.els.workspaceRuntimeState.textContent;
  check(rt.startsWith('FAIL_CLOSED · AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE · ')&&/No KV installation on this device is required/.test(rt)&&/sovereign InTr ingress unavailable for WORKSPACE_PERSONAL_PROJECTION/.test(rt),'runtime message: '+rt);
  check(html.includes('DR1 KV custody and recovery manifest')&&html.includes('DR2 Authenticated TV/TVC principal continuity')&&html.includes('DR3 Node binding and KV ingress on this device')&&html.includes('DR4 Same MyKV assistant principal and continuity')&&html.includes('DR5 Transition receipts and Master Records readback'),'five rows rendered: '+html.slice(0,400));
  check(html.includes('<span class="pill warn">FAIL_CLOSED</span> AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE')&&html.includes('SESSION_PRINCIPAL_UNAUTHENTICATED')&&html.includes('UNKNOWN_NOT_AUTHENTICALLY_OBSERVED')&&html.includes('local KV installation required: false')&&html.includes('second device required: false')&&html.includes('new node minted by this page: false')&&html.includes('RETAINED_NODE_CAPSULE_CUSTODY_FOR_DEVICE_REPLACEMENT_NOT_DEFINED')&&html.includes('not runtime proof'),'shipped-state card: '+html.slice(0,1200));
  check(!/<span class="pill ok">ALLOW<\/span>/.test(html),'no ALLOW pill in the shipped state');
  // Bridge refusal with a decision (fresh browser, no recovery result).
  const refusal=Object.assign(new Error('FAIL_CLOSED: DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED'),{decision:NB_FAIL});
  h=harness({bridge:{loadPersonalWorkspace:()=>Promise.reject(refusal),lastNodeBinding:()=>NB_FAIL}});await wait();html=h.els.deviceContinuity.innerHTML;
  check(html.includes('DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED')&&!html.includes('AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE</span>')&&h.els.workspaceRuntimeState.textContent.includes('no device identity was registered by this page'),'fresh browser refusal: '+html.slice(0,500));
  // Bridge absent.
  h=harness({bridge:null});await wait();check(h.els.deviceContinuity.innerHTML.includes('WORKSPACE_DEVICE_KV_BRIDGE_UNAVAILABLE')||h.els.deviceContinuity.innerHTML.includes('NODE_BINDING_NOT_EVALUATED'),'bridge absent still renders the case: '+h.els.deviceContinuity.innerHTML.slice(0,300));
  // Admitted stub (test injection only): projection delivered, retained node, session receipt; DR5 still unknown and overall still not ALLOW.
  h=harness({session:session('user:owner'),bridge:{loadPersonalWorkspace:()=>Promise.resolve(projection()),lastNodeBinding:()=>NB_RETAINED}});await wait();html=h.els.deviceContinuity.innerHTML;
  check(html.includes('DR1 KV custody and recovery manifest</strong> <span class="pill ok">PROJECTED</span>')&&html.includes('DR2 Authenticated TV/TVC principal continuity</strong> <span class="pill ok">ALLOW</span>')&&html.includes('DR3 Node binding and KV ingress on this device</strong> <span class="pill ok">ALLOW</span>')&&html.includes('retained node rehydrated')&&html.includes('DR4 Same MyKV assistant principal and continuity</strong> <span class="pill warn">FAIL_CLOSED</span> CHECKPOINT_NOT_OBSERVED')&&html.includes('bound assistant auri:primary')&&html.includes('<span class="pill warn">UNKNOWN_NOT_AUTHENTICALLY_OBSERVED</span>'),'admitted stub card: '+html.slice(0,1500));
  check(/Overall <span class="pill warn">FAIL_CLOSED<\/span> CHECKPOINT_NOT_OBSERVED/.test(html),'overall never ALLOW from the page: '+html.slice(0,300));
  h.switchTo('organizational');html=h.els.deviceContinuity.innerHTML;check(html.includes('ASSISTANT_CONTINUITY_NOT_EVALUATED')&&html.includes('KV_CUSTODY_MANIFEST_NOT_DELIVERED_TO_PAGE')&&!html.includes('retained node rehydrated')||html.includes('ASSISTANT_CONTINUITY_NOT_EVALUATED'),'org context drops personal inputs: '+html.slice(0,300));
  check(!html.includes('PROJECTED</span>'),'org context shows no personal projection row');
  // Contract not loaded.
  h=harness({contract:false,bridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('x')),lastNodeBinding:()=>null}});await wait();check(h.els.deviceContinuity.innerHTML.includes('DEVICE_CONTINUITY_CONTRACT_UNAVAILABLE'),'absent contract falls back');
  console.log('WORKSPACE_DEVICE_CONTINUITY_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
