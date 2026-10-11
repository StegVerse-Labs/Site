// Universal user-facing explanation surface (stegverse.user-facing-explanation/v1): the Site consumer mirrors the
// canonical builder in StegVerse-Labs/.github (schemas/user-facing-explanation.v1.schema.json), renders prose by
// default with the complete JSON artifact available to copy, explains the most recent outcome the page holds, never
// claims ALLOW, never creates authority, never submits anything and performs no I/O inside the contract file. The
// expected artifact key set below is kept in sync with the canonical schema by hand (this test reads no other clone).
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const src=read('assets/workspace-explanation.js'),ui=read('assets/workspace.js'),page=read('workspace.html'),css=read('assets/workspace.css'),workflow=read('.github/workflows/workspace-kv-binding-validation.yml');
const caps=read('assets/workspace-capabilities.js'),auth=read('assets/workspace-session-authentication.js'),binding=read('assets/workspace-assistant-binding.js'),continuity=read('assets/workspace-assistant-continuity.js'),nodeBinding=read('assets/workspace-node-binding.js'),device=read('assets/workspace-device-continuity.js');
const bootstrap=JSON.parse(read('data/workspace/bootstrap.json'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
const sb={};vm.createContext(sb);vm.runInContext(src,sb);const E=sb.StegVerseWorkspaceExplanation;
const SURFACE={repository:'StegVerse-Labs/Site',surface_id:'workspace'};
const SCHEMA='stegverse.user-facing-explanation/v1';
// Canonical schema `required` list plus the optional remediation_draft the builder always emits (null when absent).
const REQUIRED_KEYS=['schema','ecosystem_identifier','explanation_type','explanation_version','surface','outcome','authorization','execution','prose','terminology','evidence','llm_interpretation','authority','sanitization','recognition_probe'];
const EXPECTED_KEYS=REQUIRED_KEYS.concat(['remediation_draft']).sort();
const refused=r=>r&&r.schema===SCHEMA&&r.disposition==='FAIL_CLOSED'&&r.predicate==='EXPLANATION_NOT_BUILDABLE'&&typeof r.reason==='string'&&r.reason.length>0;
const built=a=>a&&a.schema===SCHEMA&&a.predicate===undefined&&a.outcome&&typeof a.outcome.outcome_class==='string';

// 1. Module identity, frozen, source scope.
check(E.schema===SCHEMA&&E.explanation_version==='1.0.0'&&E.recognition_probe_literal==='STEGVERSE_ECOSYSTEM_KNOWLEDGE_PROBE_V1'&&E.authority_effect==='NONE'&&typeof E.build==='function'&&typeof E.prose==='function'&&Object.isFrozen(E),'module identity');
const code=src.split('\n').filter(l=>!/^\s*\/\//.test(l)).join('\n');
check(!/fetch\(|XMLHttpRequest|localStorage|sessionStorage|indexedDB|navigator\.|clipboard|registerDevice/.test(code),'contract performs no I/O, storage, clipboard or registration');
check(!/\bwindow\b|\bdocument\b/.test(code),'contract reads nothing from the page');
check(/authority_effect:"NONE",explanation_is_non_authoritative:true,canonical_record_mutation:false,alternate_governance_path:false/.test(code),'authority block is constant');
check(/secrets_present:false,personal_data_minimized:true,invented_evidence:false/.test(code),'sanitization block is constant');
check(/status:RECOGNITION_PROBE_STATUS/.test(code)&&/"CANDIDATE_NOT_CANONICAL"/.test(code),'recognition probe is a candidate, not canonical');

// 2. The five outcome classes build with the mapped authorization/execution facts.
const base={predicate:'PERSONAL_KV_PROJECTION_ADMITTED',requested_action:'Open your Personal KV Workspace from this device',authority_source:'INTERLOCK_INTR'};
const receipt=[{kind:'RECEIPT_REF',ref:'intr:receipt:1',description:'Transition receipt'}];
const cases=[
 [Object.assign({},base,{disposition:'ALLOW',consequence_observation:'OBSERVED',evidence:receipt}),'SUCCESS_VERIFIED',true,true,'VERIFIED','OBSERVED'],
 [Object.assign({},base,{disposition:'ALLOW',consequence_observation:'NOT_AUTHENTICALLY_OBSERVED'}),'AUTHORIZED_NOT_VERIFIED',true,false,'NOT_VERIFIED','NOT_AUTHENTICALLY_OBSERVED'],
 [Object.assign({},base,{disposition:'ALLOW'}),'AUTHORIZED_NOT_VERIFIED',true,false,'NOT_VERIFIED','UNKNOWN'],
 [Object.assign({},base,{disposition:'DENY',predicate:'WORKSPACE_GRANT_REVOKED'}),'DENIED',false,false,'NOT_EXECUTED','NOT_AUTHENTICALLY_OBSERVED'],
 [Object.assign({},base,{disposition:'FAIL_CLOSED',predicate:'AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE'}),'FAILED_CLOSED',false,false,'NOT_EXECUTED','NOT_AUTHENTICALLY_OBSERVED'],
 [Object.assign({},base,{disposition:'UNKNOWN',predicate:'NOT_EVALUATED'}),'UNOBSERVED',false,false,'NOT_EXECUTED','UNKNOWN'],
];
const summaries={SUCCESS_VERIFIED:'Succeeded and verified.',AUTHORIZED_NOT_VERIFIED:'Authorized; execution not verified.',DENIED:'Denied; nothing was executed.',FAILED_CLOSED:'Failed closed; nothing was executed.',UNOBSERVED:'Unknown; not success, not failure.'};
for(const [rec,cls,authorized,executed,execState,obs] of cases){
 const a=E.build(rec,SURFACE);
 check(built(a)&&a.outcome.outcome_class===cls&&a.outcome.disposition===rec.disposition&&a.outcome.observation_state===obs&&a.authorization.authorized===authorized&&a.execution.executed===executed&&a.execution.execution_state===execState&&a.execution.consequence_observation===obs,cls+' mapping: '+JSON.stringify(a).slice(0,300));
 check(a.outcome.predicate===rec.predicate&&a.outcome.predicates.length===1&&a.outcome.predicates[0]===rec.predicate&&a.authorization.requested_action===rec.requested_action&&a.authorization.authority_source===rec.authority_source,cls+' carries the record predicate and action exactly');
 check(a.prose.outcome_summary===summaries[cls]&&a.prose.why.startsWith('Because ')&&a.prose.why.includes(rec.predicate)&&a.prose.what_you_can_safely_do_next.length>=1&&a.prose.limitations.length===3,cls+' prose: '+JSON.stringify(a.prose).slice(0,300));
 check(Object.keys(a).sort().join()===EXPECTED_KEYS.join(),cls+' top-level keys equal the schema required list plus remediation_draft: '+Object.keys(a).sort().join());
 check(a.ecosystem_identifier==='STEGVERSE'&&a.explanation_type==='OUTCOME_EXPLANATION'&&a.explanation_version==='1.0.0'&&a.surface.repository==='StegVerse-Labs/Site'&&a.surface.surface_id==='workspace'&&a.surface.surface_version===undefined,cls+' constants and whitelisted surface');
 check(a.authority.authority_effect==='NONE'&&a.authority.explanation_is_non_authoritative===true&&a.authority.canonical_record_mutation===false&&a.authority.alternate_governance_path===false&&a.sanitization.secrets_present===false&&a.sanitization.personal_data_minimized===true&&a.sanitization.invented_evidence===false&&a.recognition_probe.literal==='STEGVERSE_ECOSYSTEM_KNOWLEDGE_PROBE_V1'&&a.recognition_probe.status==='CANDIDATE_NOT_CANONICAL'&&typeof a.recognition_probe.note==='string',cls+' authority, sanitization and probe blocks');
 check(a.llm_interpretation.self_contained===true&&a.llm_interpretation.instructions.length===6&&a.llm_interpretation.prohibited_assumptions.length===6&&a.terminology.length===11&&a.terminology.every(t=>t.term&&t.definition)&&a.remediation_draft===null,cls+' interpretation lists, terminology and no draft');
 const text=E.prose(a);
 check(text.startsWith('What happened: ')&&text.endsWith('\n')&&!/[{}]/.test(text),cls+' prose starts with What happened and carries no JSON braces');
 const lines=text.trimEnd().split('\n');
 check(lines[0].startsWith('What happened: ')&&lines[1].startsWith('Why: ')&&lines[2]==='Outcome: '+summaries[cls]&&lines[3].startsWith('What was authorized: ')&&lines[4].startsWith('What was executed: ')&&lines[5].startsWith('What evidence exists: ')&&lines[6]==='What you can safely do next:'&&lines.includes('Limitations:')&&lines.filter(l=>l.startsWith('  - ')).length===a.prose.what_you_can_safely_do_next.length+3,cls+' prose layout matches the reference render_prose');
}
// Evidence and remediation draft are carried; produced_at only when given; predicates list is de-duplicated with the predicate first.
let a=E.build({disposition:'DENY',predicate:'WORKSPACE_GRANT_REVOKED',predicates:['OTHER_CONDITION','OTHER_CONDITION'],requested_action:'MESSAGE',authority_source:'MANIFEST',why:'the grant was revoked by its owner',safe_next_steps:['Ask the owner to re-grant.'],canonical_record_ref:'kv:record:1',produced_at:'2026-10-11T00:00:00Z',evidence:[{kind:'PROVENANCE_REF',ref:'kv-workspace-source:sha256:'+'a'.repeat(64),description:'Personal KV projection provenance'},{kind:'NONE',ref:null,description:'No receipt'}],remediation_draft:{schema_version:'stegverse.workspace.interaction-request.v1',action:'MESSAGE',submitted:false,manifest_admitted:false,disposition:'FAIL_CLOSED',failing_predicate:'WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND',authority_effect:'NONE_REQUEST_ONLY'}},SURFACE);
check(built(a)&&a.outcome.predicates.join()==='WORKSPACE_GRANT_REVOKED,OTHER_CONDITION'&&a.outcome.canonical_record_ref==='kv:record:1'&&a.produced_at==='2026-10-11T00:00:00Z'&&Object.keys(a).sort().join()===EXPECTED_KEYS.concat(['produced_at']).sort().join(),'optional fields: '+JSON.stringify(a.outcome));
check(a.prose.why==='Because the grant was revoked by its owner.'&&a.prose.what_you_can_safely_do_next.length===2&&a.prose.what_you_can_safely_do_next[0]==='Ask the owner to re-grant.'&&/unsubmitted remediation draft is attached/.test(a.prose.what_you_can_safely_do_next[1]),'supplied reason and steps, draft note appended');
check(a.evidence.length===2&&a.evidence.every(e=>e.sanitized===true)&&a.prose.what_evidence_exists.startsWith('Evidence is referenced by locator: Personal KV projection provenance (kv-workspace-source:sha256:')&&a.prose.what_evidence_exists.endsWith('; No receipt.'),'evidence by locator and description only: '+a.prose.what_evidence_exists);
check(a.remediation_draft.submitted===false&&a.remediation_draft.manifest_admitted===false&&a.remediation_draft.authority_effect==='NONE_REQUEST_ONLY'&&a.remediation_draft.non_authorizing===true&&a.remediation_draft.draft.action==='MESSAGE'&&a.remediation_draft.draft.submitted===false,'remediation draft wrapped as unsubmitted and non-authorizing');
check(E.build(Object.assign({},base,{disposition:'DENY',extra_personal_field:'never copied',owner_email:'x@example.org'}),Object.assign({},SURFACE,{surface_version:'v1',operator:'never copied'})).surface.operator===undefined&&!JSON.stringify(E.build(Object.assign({},base,{disposition:'DENY',extra_personal_field:'never copied'}),SURFACE)).includes('never copied'),'only whitelisted record and surface fields reach the artifact');
check(E.build(Object.assign({},base,{disposition:'DENY'}),Object.assign({},SURFACE,{surface_version:'v1'})).surface.surface_version==='v1'&&refused(E.build(base,SURFACE))&&E.build(base,SURFACE).reason==='disposition_invalid','surface_version is whitelisted; a record without a disposition is refused');
check(E.prose({})===''&&E.prose(null)===''&&E.prose(E.build({},SURFACE))==='','prose of a non-artifact is empty, never a throw');

// 3. Invariants refused, never thrown.
const deny=Object.assign({},base,{disposition:'DENY'});
const refusals=[
 [Object.assign({},deny,{api_key:'zzz'}),'secret_material_present:api_key'],
 [Object.assign({},deny,{nested:{list:[{Password:'q'}]}}),'secret_material_present:nested.list[0].Password'],
 [Object.assign({},deny,{requested_action:'Bearer abcdef'}),'secret_material_present:requested_action'],
 [Object.assign({},deny,{why:'ghp_abcdefghijklmnopqrstuvwxyz'}),'secret_material_present:why'],
 [Object.assign({},deny,{secrets_present:'no'}),'secret_material_present:secrets_present'],
 [Object.assign({},base,{disposition:'ALLOW',consequence_observation:'OBSERVED'}),'observed_execution_requires_receipt_evidence'],
 [Object.assign({},base,{disposition:'ALLOW',consequence_observation:'OBSERVED',evidence:[{kind:'SOURCE_REF',ref:'s',description:'d'}]}),'observed_execution_requires_receipt_evidence'],
 [Object.assign({},deny,{consequence_observation:'OBSERVED'}),'non_allow_cannot_observe_consequence'],
 [Object.assign({},base,{disposition:'FAIL_CLOSED',consequence_observation:'OBSERVED'}),'non_allow_cannot_observe_consequence'],
 [Object.assign({},deny,{remediation_draft:{submitted:true,manifest_admitted:false,authority_effect:'NONE'}}),'remediation_draft_must_be_unsubmitted'],
 [Object.assign({},deny,{remediation_draft:{submitted:false,manifest_admitted:true,authority_effect:'NONE'}}),'remediation_draft_must_not_be_admitted'],
 [Object.assign({},deny,{remediation_draft:{submitted:false,manifest_admitted:false,authority_effect:'FULL'}}),'remediation_draft_must_be_non_authorizing'],
 [Object.assign({},deny,{remediation_draft:{submitted:false,manifest_admitted:false,authority_effect:'NONE',disposition:'ALLOW'}}),'remediation_draft_must_not_carry_allow'],
 [Object.assign({},deny,{remediation_draft:'draft'}),'remediation_draft_invalid'],
 [Object.assign({},deny,{predicate:'lower case'}),'predicate_invalid'],
 [Object.assign({},deny,{predicate:'A'.repeat(161)}),'predicate_invalid'],
 [Object.assign({},deny,{predicates:['bad predicate']}),'predicates_invalid'],
 [Object.assign({},deny,{disposition:'MAYBE'}),'disposition_invalid'],
 [Object.assign({},deny,{requested_action:' '}),'requested_action_required'],
 [Object.assign({},deny,{authority_source:'GITHUB'}),'authority_source_invalid'],
 [Object.assign({},deny,{consequence_observation:'SEEN'}),'consequence_observation_invalid'],
 [Object.assign({},deny,{evidence:[{kind:'RECEIPT_REF',ref:null,description:'d'}]}),'evidence_ref_required_for_kind:RECEIPT_REF'],
 [Object.assign({},deny,{evidence:[{kind:'PDF',ref:'r',description:'d'}]}),'evidence_kind_invalid'],
 [Object.assign({},deny,{evidence:[{kind:'RECEIPT_REF',ref:'r'}]}),'evidence_description_required'],
 [Object.assign({},deny,{why:''}),'why_invalid'],
 [Object.assign({},deny,{safe_next_steps:['ok','']}),'safe_next_steps_invalid'],
 [Object.assign({},deny,{canonical_record_ref:' '}),'canonical_record_ref_invalid'],
 ['notarecord','record_invalid'],
 [null,'record_invalid'],
];
for(const [rec,reason] of refusals){const r=E.build(rec,SURFACE);check(refused(r)&&r.reason===reason,'refusal '+reason+': '+JSON.stringify(r));}
check(refused(E.build(deny,'s'))&&E.build(deny,'s').reason==='surface_invalid'&&E.build(deny,{surface_id:'w'}).reason==='surface_repository_required'&&E.build(deny,{repository:'r'}).reason==='surface_id_required'&&E.build(deny,Object.assign({},SURFACE,{token:'t'})).reason==='secret_material_present:token','surface descriptor invariants');
check(E.build(Object.assign({},deny,{secrets_present:false,credential_material_present:false}),SURFACE).outcome.outcome_class==='DENIED','boolean sanitization flags are not secret material');
check(cases.filter(c=>c[0].disposition!=='ALLOW').every(c=>JSON.stringify(E.build(c[0],SURFACE)).includes('"authorized":false')&&!JSON.stringify(E.build(c[0],SURFACE).prose).includes('"ALLOW"')),'non-ALLOW outcomes never read as authorized');

// 4. Page integration: script order, card after KV Context, nav target, workflow, render path, copy handler location, styles.
check(page.indexOf('<script src="assets/workspace-device-continuity.js"></script>')<page.indexOf('<script src="assets/workspace-explanation.js"></script>')&&page.indexOf('<script src="assets/workspace-explanation.js"></script>')<page.indexOf('<script src="assets/workspace.js"></script>'),'explanation script loads before the page script');
check(/<section class="card full" id="explanationCard"><h2>Why did this happen\?<\/h2><div id="explanation" role="status" aria-live="polite"><\/div><\/section>/.test(page)&&page.indexOf('<h2>KV Context</h2>')<page.indexOf('id="explanationCard"')&&/data-target="explanationCard">Why</.test(page),'card after KV Context with a nav target');
check(workflow.includes("'assets/workspace-explanation.js'")&&workflow.includes("'tests/workspace-explanation.test.cjs'")&&workflow.includes('node --check assets/workspace-explanation.js')&&workflow.includes('node tests/workspace-explanation.test.cjs'),'workflow validates and runs the contract');
check(/function renderExplanation\(\)/.test(ui)&&/function renderAll\(\)\{[^\n]*renderExplanation\(\);\}/.test(ui),'renderExplanation defined and called from renderAll');
check(/function renderIntentDraft\(d\)\{[^\n]*state\.intentDraft=d;[^\n]*renderExplanation\(\);\}/.test(ui),'renderIntentDraft re-explains after setting the draft');
check(ui.includes('EXPLANATION_CONTRACT_UNAVAILABLE')&&ui.includes('EXPLANATION_NOT_BUILDABLE')&&ui.includes('NOT_EVALUATED · no governed outcome'),'page names the fallback, refusal and empty states');
check(/navigator\.clipboard\.writeText/.test(ui)&&!/clipboard/.test(code)&&/execCommand\("copy"\)/.test(ui)&&/function copyExplanation\(button\)/.test(ui),'copy handler lives in the page script with clipboard and textarea fallback');
const re=ui.slice(ui.indexOf('function renderExplanation()'),ui.indexOf('function copyExplanation'));
check(re.indexOf('<div class="explanation-prose">')<re.indexOf('<details class="explanation-json"><summary>Show the complete JSON explanation (copy it into any independent LLM)</summary><pre class="draft" id="explanationJson">')&&re.includes('<button type="button" data-copy-explanation>Copy JSON</button></details>'),'prose renders before the JSON details element');
check(re.includes('requested_action:"Open your Personal KV Workspace from this device",authority_source:"INTERLOCK_INTR"')||ui.includes('requested_action:"Open your Personal KV Workspace from this device",authority_source:"INTERLOCK_INTR"'),'KV ingress outcome is explained under INTERLOCK_INTR');
check(ui.includes('authority_source:"MANIFEST",remediation_draft:d')&&ui.includes('repository:"StegVerse-Labs/Site",surface_id:"workspace"'),'intent draft is explained under MANIFEST as its own unsubmitted remediation draft');
check(/\.explanation-json summary\{cursor:pointer/.test(css)&&/\.card button,\.assistant button\{min-height:44px\}/.test(css),'summary is clickable and the copy button inherits the 44px phone rule');
check(!/localStorage|sessionStorage|indexedDB/.test(ui)&&!/registerDevice/.test(ui),'page keeps no storage and registers nothing');

// 5. UI harness: KV ingress failure explained; intent draft takes precedence; NOT_EVALUATED before any outcome; copy never throws; absent contract.
const SESSION_LITERAL='session:{principal_id:null,workspace_id:null,source_class:"NO_AUTHENTICATED_SESSION_PRINCIPAL",authentication:null}';
check(ui.includes(SESSION_LITERAL),'page must not invent a session principal');
const elIds=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities','searchResults','tasks','deviceContinuity','developer','explanation'];
const unesc=s=>s.replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
const preOf=html=>{const m=html.match(/<pre class="draft" id="explanationJson">([\s\S]*?)<\/pre>/);return m?unesc(m[1]):'';};
function harness(opts){const els={};elIds.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
  // The JSON <pre> is rendered inside the explanation card; the fake DOM resolves it from that card's markup.
  els.explanationJson={id:'explanationJson',get textContent(){return preOf(els.explanation.innerHTML);}};
  const docListeners={};const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener:(t,f)=>{docListeners[t]=f}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{}};
  if(opts.bridge!==null)ctx.window.StegVerseWorkspaceKVBridge=opts.bridge;
  if(opts.navigator)ctx.navigator=opts.navigator;
  vm.createContext(ctx);for(const s of [caps,auth,binding,continuity,nodeBinding,device])vm.runInContext(s,ctx);if(opts.contract!==false)vm.runInContext(src,ctx);
  ['StegVerseWorkspaceCapabilities','StegVerseWorkspaceSessionAuthentication','StegVerseWorkspaceAssistantBinding','StegVerseWorkspaceAssistantContinuity','StegVerseWorkspaceNodeBinding','StegVerseWorkspaceDeviceContinuity','StegVerseWorkspaceExplanation'].forEach(k=>{if(ctx[k])ctx.window[k]=ctx[k];});
  vm.runInContext(ui,ctx);
  const click=target=>docListeners.click({target:{closest:sel=>target[sel]||null}});
  return {els,click,switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}})};}
const NB_LOCAL={schema:'stegverse.workspace.node-binding/v1',disposition:'ALLOW',predicate:'REGISTERED_NODE_DIRECTLY_OBSERVED',node_id:'SV-NODE-'+'a'.repeat(24),source:'DEVICE_LOCAL_REGISTRATION',identity_minted_by_page:false};
const jsonOf=html=>{const text=preOf(html);return text?JSON.parse(text):null;};
(async()=>{
  const wait=()=>new Promise(r=>setTimeout(r,10));
  // Shipped state on the owner's phone: the ingress failure is explained as FAILED_CLOSED with the bridge detail as the reason.
  let h=harness({bridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('FAIL_CLOSED: DEVICE_KV sovereign InTr ingress unavailable for WORKSPACE_PERSONAL_PROJECTION')),lastNodeBinding:()=>NB_LOCAL}});await wait();
  let html=h.els.explanation.innerHTML;
  check(html.startsWith('<div class="explanation-prose"><p><strong>What happened:</strong> The request &#39;Open your Personal KV Workspace from this device&#39; could not be evaluated because a required prerequisite is not established, so the system refused to act.</p>'),'prose first: '+html.slice(0,300));
  check(html.includes('<p><strong>Why:</strong> Because FAIL_CLOSED: DEVICE_KV sovereign InTr ingress unavailable for WORKSPACE_PERSONAL_PROJECTION.</p>')&&html.includes('<p><strong>Outcome:</strong> Failed closed; nothing was executed.</p>')&&html.includes('AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE')&&html.includes('<li>Nothing happened; your data and state are unchanged.</li>'),'reason, summary, predicate and safe steps rendered: '+html.slice(0,1200));
  check(html.indexOf('<div class="explanation-prose">')<html.indexOf('<details class="explanation-json"><summary>Show the complete JSON explanation (copy it into any independent LLM)</summary>')&&html.includes('<button type="button" data-copy-explanation>Copy JSON</button>')&&html.includes('authority_effect NONE'),'details element follows the prose');
  let j=jsonOf(html);
  check(j&&j.schema===SCHEMA&&j.outcome.outcome_class==='FAILED_CLOSED'&&j.outcome.predicate==='AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE'&&j.authorization.authority_source==='INTERLOCK_INTR'&&j.authorization.authorized===false&&j.execution.executed===false&&j.evidence.length===0&&j.remediation_draft===null&&j.surface.repository==='StegVerse-Labs/Site'&&Object.keys(j).sort().join()===EXPECTED_KEYS.join(),'complete artifact embedded: '+JSON.stringify(j).slice(0,300));
  check(!/"authorized": true|ALLOW<\/span>/.test(html),'nothing on the card claims ALLOW');
  // Copy handler: no clipboard and no DOM factory in the harness, so the fallback fails without throwing.
  const button={dataset:{copyExplanation:''},textContent:'Copy JSON'};
  h.click({'[data-copy-explanation]':button});await wait();
  check(button.textContent==='Copy failed; select the JSON above','copy without clipboard reports failure, never throws: '+button.textContent);
  check(h.els.intentDraft.innerHTML===''&&h.els.explanation.innerHTML===html,'copy changes no state');
  // A developer draft takes precedence: FAIL_CLOSED under MANIFEST with the draft as the unsubmitted remediation draft.
  h.switchTo('developer');h.click({'[data-developer-action]':{dataset:{developerAction:'DEVELOPER_CODE_CHANGE_REQUEST'}}});html=h.els.explanation.innerHTML;j=jsonOf(html);
  check(html.includes('<p><strong>What happened:</strong> The request &#39;DEVELOPER_CODE_CHANGE_REQUEST&#39; could not be evaluated')&&html.includes('WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND')&&html.includes('<li>An unsubmitted remediation draft is attached; it proposes nothing until you submit it through the governed path, where it receives its own decision.</li>'),'draft explained: '+html.slice(0,600));
  check(j&&j.outcome.outcome_class==='FAILED_CLOSED'&&j.authorization.authority_source==='MANIFEST'&&j.authorization.requested_action==='DEVELOPER_CODE_CHANGE_REQUEST'&&j.remediation_draft&&j.remediation_draft.submitted===false&&j.remediation_draft.manifest_admitted===false&&j.remediation_draft.authority_effect==='NONE_REQUEST_ONLY'&&j.remediation_draft.draft.submitted===false&&j.remediation_draft.draft.action==='DEVELOPER_CODE_CHANGE_REQUEST','draft artifact: '+JSON.stringify(j&&j.remediation_draft).slice(0,300));
  // Switching context clears the draft; the developer context holds no KV ingress outcome of its own but the page still holds the last one.
  h.switchTo('personal');html=h.els.explanation.innerHTML;check(!html.includes('DEVELOPER_CODE_CHANGE_REQUEST')&&html.includes('AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE'),'context switch drops the draft and falls back to the ingress outcome');
  // Clipboard available: reports success.
  const okButton={dataset:{copyExplanation:''},textContent:'Copy JSON'};let copied=null;
  h=harness({navigator:{clipboard:{writeText:t=>{copied=t;return Promise.resolve();}}},bridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('x')),lastNodeBinding:()=>null}});await wait();
  h.click({'[data-copy-explanation]':okButton});await wait();
  check(okButton.textContent==='Copied'&&typeof copied==='string'&&JSON.parse(copied).schema===SCHEMA&&JSON.parse(copied).outcome.predicate==='WORKSPACE_DEVICE_KV_PATH_UNAVAILABLE','clipboard copy carries the artifact JSON: '+okButton.textContent);
  // Admitted projection: AUTHORIZED_NOT_VERIFIED with provenance evidence; never SUCCESS_VERIFIED from the page.
  const REV='a'.repeat(64);
  const projection={schema:'stegverse.kv.personal-workspace-projection/v1',state:'KV_WORKSPACE_PROJECTED',workspace_type:'PERSONAL',principals:[],organizations:[],memberships:[],feed:[],assistant:null,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,projection_metadata:{schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:new Date(Date.now()-60000).toISOString().replace(/\.\d{3}Z$/,'Z'),observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:REV,provenance_ref:'kv-workspace-source:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'},authority_effect:'NONE'};
  h=harness({bridge:{loadPersonalWorkspace:()=>Promise.resolve(projection),lastNodeBinding:()=>NB_LOCAL}});await wait();html=h.els.explanation.innerHTML;j=jsonOf(html);
  check(j&&j.outcome.outcome_class==='AUTHORIZED_NOT_VERIFIED'&&j.outcome.predicate==='PERSONAL_KV_PROJECTION_ADMITTED'&&j.execution.executed===false&&j.evidence.length===1&&j.evidence[0].kind==='PROVENANCE_REF'&&j.evidence[0].ref==='kv-workspace-source:sha256:'+REV&&html.includes('<p><strong>Outcome:</strong> Authorized; execution not verified.</p>'),'admitted projection is authorized, not verified: '+JSON.stringify(j&&j.outcome));
  // Bridge absent: WORKSPACE_DEVICE_KV_BRIDGE_UNAVAILABLE explained.
  h=harness({bridge:null});await wait();check(h.els.explanation.innerHTML.includes('WORKSPACE_DEVICE_KV_BRIDGE_UNAVAILABLE')&&h.els.explanation.innerHTML.includes('<strong>What happened:</strong>'),'absent bridge explained');
  // No outcome yet (bridge never answers): NOT_EVALUATED empty state, no artifact.
  h=harness({bridge:{loadPersonalWorkspace:()=>new Promise(()=>{}),lastNodeBinding:()=>null}});await wait();
  check(h.els.explanation.innerHTML==='<div class="empty">NOT_EVALUATED · no governed outcome has been reported to this page yet, so there is nothing to explain.</div>','empty state before any outcome: '+h.els.explanation.innerHTML);
  // Contract not loaded.
  h=harness({contract:false,bridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('x')),lastNodeBinding:()=>null}});await wait();
  check(h.els.explanation.innerHTML==='<div class="empty">Explanation contract unavailable (EXPLANATION_CONTRACT_UNAVAILABLE); the canonical disposition above stands on its own.</div>','absent contract falls back');
  // Canonical producers may emit lower-case predicate names (crypto-bot snapshot_* refusals); they are copied verbatim.
{const E=sb.StegVerseWorkspaceExplanation;const low=E.build({disposition:'FAIL_CLOSED',predicate:'snapshot_position_field_missing:value_usd',requested_action:'Project the CryptoBot portfolio snapshot into the WorkSpace projection',authority_source:'NONE',consequence_observation:'NOT_AUTHENTICALLY_OBSERVED',evidence:[{kind:'SOURCE_REF',ref:'StegVerse-Labs/crypto-bot:scripts/project_portfolio_snapshot_for_workspace.py',description:'The producer that refused'}]},{repository:'StegVerse-Labs/crypto-bot',surface_id:'workspace-portfolio-projection'});check(low.schema==='stegverse.user-facing-explanation/v1'&&low.outcome&&low.outcome.predicate==='snapshot_position_field_missing:value_usd'&&low.outcome.outcome_class==='FAILED_CLOSED','lower-case producer predicate copied verbatim');}
console.log('WORKSPACE_EXPLANATION_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
