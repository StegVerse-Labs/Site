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
check(E.schema===SCHEMA&&E.explanation_version==='1.1.0'&&E.recognition_probe_literal==='STEGVERSE_ECOSYSTEM_KNOWLEDGE_PROBE_V1'&&E.authority_effect==='NONE'&&typeof E.build==='function'&&typeof E.prose==='function'&&Object.isFrozen(E),'module identity');
check(typeof E.conforms==='function'&&Object.keys(E).sort().join()==='authority_effect,build,conforms,explanation_version,prose,recognition_probe_literal,schema','conforms exported on the frozen object');
const code=src.split('\n').filter(l=>!/^\s*\/\//.test(l)).join('\n');
check(!/fetch\(|XMLHttpRequest|localStorage|sessionStorage|indexedDB|navigator\.|clipboard|registerDevice/.test(code),'contract performs no I/O, storage, clipboard or registration');
check(!/\bwindow\b|\bdocument\b/.test(code),'contract reads nothing from the page');
check(/authority_effect:"NONE",explanation_is_non_authoritative:true,canonical_record_mutation:false,alternate_governance_path:false/.test(code),'authority block is constant');
check(/secrets_present:false,personal_data_minimized:true,invented_evidence:false/.test(code),'sanitization block is constant');
check(/status:RECOGNITION_PROBE_STATUS/.test(code)&&/"CANDIDATE_NOT_CANONICAL"/.test(code),'recognition probe is a candidate, not canonical');

// 2. The outcome classes build with the mapped authorization/execution facts. Receipt invariant: ALLOW exists only
// with its receipt, so ALLOW without an OBSERVED consequence or receipt-class evidence is not buildable.
const base={predicate:'PERSONAL_KV_PROJECTION_ADMITTED',requested_action:'Open your Personal KV Workspace from this device',authority_source:'INTERLOCK_INTR'};
const receipt=[{kind:'RECEIPT_REF',ref:'intr:receipt:1',description:'Transition receipt'}];
function receipt0(){return [{kind:'RECEIPT_REF',ref:'intr:receipt:1',description:'Transition receipt'}];}
const cases=[
 [Object.assign({},base,{disposition:'ALLOW',consequence_observation:'OBSERVED',evidence:receipt}),'SUCCESS_VERIFIED',true,true,'VERIFIED','OBSERVED'],
 [Object.assign({},base,{disposition:'DENY',predicate:'WORKSPACE_GRANT_REVOKED'}),'DENIED',false,false,'NOT_EXECUTED','NOT_AUTHENTICALLY_OBSERVED'],
 [Object.assign({},base,{disposition:'FAIL_CLOSED',predicate:'AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE'}),'FAILED_CLOSED',false,false,'NOT_EXECUTED','NOT_AUTHENTICALLY_OBSERVED'],
 [Object.assign({},base,{disposition:'UNKNOWN',predicate:'NOT_EVALUATED'}),'UNOBSERVED',false,false,'NOT_EXECUTED','UNKNOWN'],
];
for(const bad of [Object.assign({},base,{disposition:'ALLOW',consequence_observation:'NOT_AUTHENTICALLY_OBSERVED',evidence:receipt0()}),Object.assign({},base,{disposition:'ALLOW',evidence:receipt0()}),Object.assign({},base,{disposition:'ALLOW',consequence_observation:'OBSERVED'})])check(refused(E.build(bad,SURFACE))&&/allow_requires_receipt/.test(E.build(bad,SURFACE).reason),'ALLOW without its receipt is not buildable: '+JSON.stringify(bad));
const summaries={SUCCESS_VERIFIED:'Succeeded and verified.',DENIED:'Denied; nothing was executed.',FAILED_CLOSED:'Failed closed; nothing was executed.',UNOBSERVED:'Unknown to this surface; not success, not failure.'};
for(const [rec,cls,authorized,executed,execState,obs] of cases){
 const a=E.build(rec,SURFACE);
 check(built(a)&&a.outcome.outcome_class===cls&&a.outcome.disposition===rec.disposition&&a.outcome.observation_state===obs&&a.authorization.authorized===authorized&&a.execution.executed===executed&&a.execution.execution_state===execState&&a.execution.consequence_observation===obs,cls+' mapping: '+JSON.stringify(a).slice(0,300));
 check(a.outcome.predicate===rec.predicate&&a.outcome.predicates.length===1&&a.outcome.predicates[0]===rec.predicate&&a.authorization.requested_action===rec.requested_action&&a.authorization.authority_source===rec.authority_source,cls+' carries the record predicate and action exactly');
 check(a.prose.outcome_summary===summaries[cls]&&a.prose.why.startsWith('Because ')&&a.prose.why.includes(rec.predicate)&&a.prose.what_you_can_safely_do_next.length>=1&&a.prose.limitations.length===3,cls+' prose: '+JSON.stringify(a.prose).slice(0,300));
 check(Object.keys(a).sort().join()===EXPECTED_KEYS.join(),cls+' top-level keys equal the schema required list plus remediation_draft: '+Object.keys(a).sort().join());
 check(a.ecosystem_identifier==='STEGVERSE'&&a.explanation_type==='OUTCOME_EXPLANATION'&&a.explanation_version==='1.1.0'&&a.surface.repository==='StegVerse-Labs/Site'&&a.surface.surface_id==='workspace'&&a.surface.surface_version===undefined,cls+' constants and whitelisted surface');
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
 [Object.assign({},deny,{why:'see token ghp_'+'a'.repeat(36)}),'secret_material_present:why'],
 [Object.assign({},deny,{why:'Authorization: Bearer '+'b'.repeat(32)}),'secret_material_present:why'],
 [Object.assign({},deny,{why:'url ?t=github_pat_'+'c'.repeat(40)}),'secret_material_present:why'],
 [Object.assign({},deny,{why:'key AKIA'+'D'.repeat(16)+' in log'}),'secret_material_present:why'],
 [Object.assign({},deny,{why:'slack xoxb-'+'1'.repeat(24)}),'secret_material_present:why'],
 [Object.assign({},deny,{secrets_present:'no'}),'secret_material_present:secrets_present'],
 [Object.assign({},base,{disposition:'ALLOW',consequence_observation:'OBSERVED'}),'allow_requires_receipt'],
 [Object.assign({},base,{disposition:'ALLOW',consequence_observation:'OBSERVED',evidence:[{kind:'SOURCE_REF',ref:'s',description:'d'}]}),'allow_requires_receipt'],
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

// 3b. Conformance: conforms() mirrors the canonical schema's cross-field rules (repair for .github#3106 review finding
// EXPLANATION_SCHEMA_CROSS_FIELD_CONSISTENCY). Builder artifacts for every outcome class conform; named mutations are rejected.
for(const [rec,cls] of cases){const c=E.conforms(E.build(rec,SURFACE));check(c&&c.ok===true&&c.violations===undefined,cls+' builder artifact conforms: '+JSON.stringify(c));}
check(E.conforms(a).ok===true&&E.conforms(E.build(Object.assign({},deny,{produced_at:'2026-10-11T00:00:00Z'}),SURFACE)).ok===true,'artifacts with evidence, draft and produced_at conform');
for(const bad of [null,'x',[],{},{schema:SCHEMA},E.build({},SURFACE)]){const c=E.conforms(bad);check(c&&c.ok===false&&Array.isArray(c.violations)&&c.violations.length>0&&c.violations.every(v=>typeof v==='string'&&v.length),'non-artifact rejected, never thrown: '+JSON.stringify(c).slice(0,120));}
const clone=x=>JSON.parse(JSON.stringify(x));
const mutate0=(src,f)=>{const m=clone(src);f(m);return m;};
const SV=E.build(cases[0][0],SURFACE),DN=E.build(cases[1][0],SURFACE),FC=E.build(cases[2][0],SURFACE),UN=E.build(cases[3][0],SURFACE);
// ALLOW without execution: the receipt invariant makes this contradictory (no ALLOW without its receipt).
const ANV=mutate0(SV,m=>{m.execution.executed=false;m.execution.execution_state='NOT_EXECUTED';m.execution.consequence_observation='NOT_AUTHENTICALLY_OBSERVED';m.outcome.observation_state='NOT_AUTHENTICALLY_OBSERVED';m.outcome.outcome_class='FAILED_CLOSED';});
const mutate=(src,f)=>{const m=clone(src);f(m);return m;};
const mutations=[
 ['DENY + execution_state VERIFIED + consequence_observation OBSERVED',mutate(DN,m=>{m.execution.execution_state='VERIFIED';m.execution.consequence_observation='OBSERVED';}),/non_allow_requires_not_executed|non_allow_forbids_observed_consequence|verified_requires_executed|observed_consequence_requires_executed/],
 ['DENY + outcome_class SUCCESS_VERIFIED',mutate(DN,m=>{m.outcome.outcome_class='SUCCESS_VERIFIED';}),/success_verified_requires_executed|deny_requires_denied/],
 ['DENY + observation_state OBSERVED',mutate(DN,m=>{m.outcome.observation_state='OBSERVED';}),/observed_state_requires_executed|deny_requires_not_authentically_observed_observation_state/],
 ['SUCCESS_VERIFIED artifact with evidence lacking receipt-class kinds',mutate(SV,m=>{m.evidence=[{kind:'SOURCE_REF',ref:'s',description:'d',sanitized:true}];}),/executed_requires_receipt_class_evidence:\$\.evidence/],
 ['SUCCESS_VERIFIED artifact with no evidence at all',mutate(SV,m=>{m.evidence=[];}),/executed_requires_receipt_class_evidence/],
 ['ALLOW + executed false + outcome_class SUCCESS_VERIFIED',mutate(ANV,m=>{m.outcome.outcome_class='SUCCESS_VERIFIED';}),/not_executed_forbids_success_verified|success_verified_requires_executed/],
 ['ALLOW + executed false + execution_state VERIFIED',mutate(ANV,m=>{m.execution.execution_state='VERIFIED';}),/not_executed_forbids_verified|verified_requires_executed/],
 ['ALLOW + executed true without OBSERVED consequence',mutate(SV,m=>{m.execution.consequence_observation='NOT_AUTHENTICALLY_OBSERVED';}),/executed_requires_observed_consequence/],
 ['authorized true on DENY',mutate(DN,m=>{m.authorization.authorized=true;}),/non_allow_forbids_authorized|authorized_requires_allow/],
 ['authorized false on ALLOW',mutate(ANV,m=>{m.authorization.authorized=false;}),/allow_requires_authorized/],
 ['ALLOW without execution (no receipt)',ANV,/allow_requires_executed/],
 ['removed class AUTHORIZED_NOT_VERIFIED',mutate(DN,m=>{m.outcome.outcome_class='AUTHORIZED_NOT_VERIFIED';}),/schema:enum/],
 ['removed state NOT_VERIFIED',mutate(DN,m=>{m.execution.execution_state='NOT_VERIFIED';}),/schema:enum|non_allow_requires_not_executed/],
 ['FAIL_CLOSED + executed true',mutate(FC,m=>{m.execution.executed=true;}),/non_allow_forbids_executed|executed_requires_allow/],
 ['FAIL_CLOSED + outcome_class DENIED',mutate(FC,m=>{m.outcome.outcome_class='DENIED';}),/fail_closed_requires_failed_closed|denied_requires_deny/],
 ['UNKNOWN + consequence_observation NOT_AUTHENTICALLY_OBSERVED (observation state must mirror)',mutate(UN,m=>{m.execution.consequence_observation='NOT_AUTHENTICALLY_OBSERVED';}),/unknown_requires_unknown_consequence|observation_state_mirrors_consequence/],
 ['extra top-level key',mutate(DN,m=>{m.extra='x';}),/additionalProperties:\$\.extra/],
 ['missing required top-level key',mutate(DN,m=>{delete m.authority;}),/required:\$\.authority/],
 ['authority_effect not NONE',mutate(DN,m=>{m.authority.authority_effect='FULL';}),/const:\$\.authority\.authority_effect/],
 ['explanation_is_non_authoritative false',mutate(DN,m=>{m.authority.explanation_is_non_authoritative=false;}),/const:\$\.authority\.explanation_is_non_authoritative/],
 ['secrets_present true',mutate(DN,m=>{m.sanitization.secrets_present=true;}),/const:\$\.sanitization\.secrets_present/],
 ['invented_evidence true',mutate(DN,m=>{m.sanitization.invented_evidence=true;}),/const:\$\.sanitization\.invented_evidence/],
 ['recognition_probe status canonical',mutate(DN,m=>{m.recognition_probe.status='CANONICAL';}),/const:\$\.recognition_probe\.status/],
 ['remediation_draft.submitted true',mutate(a,m=>{m.remediation_draft.submitted=true;}),/const:\$\.remediation_draft\.submitted/],
 ['remediation_draft.draft.submitted true',mutate(a,m=>{m.remediation_draft.draft.submitted=true;}),/remediation_draft_submitted/],
 ['remediation_draft.authority_effect not NONE_REQUEST_ONLY',mutate(a,m=>{m.remediation_draft.authority_effect='NONE';}),/const:\$\.remediation_draft\.authority_effect/],
 ['predicate not in predicates',mutate(DN,m=>{m.outcome.predicate='OTHER_CONDITION';}),/predicate_not_in_predicates/],
 ['predicate with a space',mutate(DN,m=>{m.outcome.predicate='bad predicate';m.outcome.predicates=['bad predicate'];}),/pattern:\$\.outcome\.predicate/],
 ['evidence item not sanitized',mutate(a,m=>{m.evidence[0].sanitized=false;}),/const:\$\.evidence\[0\]\.sanitized/],
 ['evidence ref missing for a non-NONE kind',mutate(a,m=>{m.evidence[0].ref=null;}),/evidence_ref_missing:\$\.evidence\[0\]/],
 ['evidence kind unknown',mutate(a,m=>{m.evidence[0].kind='PDF';}),/enum:\$\.evidence\[0\]\.kind/],
 ['llm_interpretation.self_contained false',mutate(DN,m=>{m.llm_interpretation.self_contained=false;}),/const:\$\.llm_interpretation\.self_contained/],
 ['prose.limitations empty',mutate(DN,m=>{m.prose.limitations=[];}),/minItems:\$\.prose\.limitations/],
 ['secret material inside the artifact',mutate(DN,m=>{m.prose.why='Bearer abcdef';}),/secret_material_present:prose\.why/],
 ['schema identifier changed',mutate(DN,m=>{m.schema='other/v2';}),/const:\$\.schema/],
];
for(const [name,m,re] of mutations){const c=E.conforms(m);check(c&&c.ok===false&&Array.isArray(c.violations)&&c.violations.length>0&&c.violations.some(v=>re.test(v)),'conforms rejects '+name+': '+JSON.stringify(c).slice(0,300));}
check(E.conforms(SV).ok===true&&E.conforms(DN).ok===true&&E.conforms(a).ok===true,'mutations never touched the originals');
check(/var c=conforms\(artifact\);\n if\(!c\.ok\)return \{schema:SCHEMA,disposition:"FAIL_CLOSED",predicate:"EXPLANATION_NOT_BUILDABLE",reason:"artifact_nonconforming:"\+c\.violations\[0\]\};/.test(code),'build() re-checks its own output and refuses a non-conforming artifact');

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

// 4b. Page integration: conformance gate before display, explain-on-request controls, precedence, dispatcher guards, styles.
const re2=ui.slice(ui.indexOf('function renderExplanation()'),ui.indexOf('function copyExplanation'));
check(re2.indexOf('E.conforms(a)')>-1&&re2.indexOf('E.conforms(a)')<re2.indexOf('<div class="explanation-prose">')&&re2.indexOf('E.conforms(a)')<re2.indexOf('E.prose(a)'),'renderExplanation calls conforms before any prose or JSON is rendered');
check(re2.includes(`'<div class="empty">Explanation withheld (EXPLANATION_NONCONFORMING · '+safe(c&&c.violations&&c.violations[0])+'); the canonical disposition above stands on its own.</div>'`),'withheld message names EXPLANATION_NONCONFORMING and the first violation');
check(re2.includes('<button type="button" data-explain-clear>Back to latest outcome</button>'),'explanation card offers Back to latest outcome (data-explain-clear)');
const rc=ui.slice(ui.indexOf('function renderCapabilities()'),ui.indexOf('function renderDeviceContinuity()'));
check((rc.match(/whyButton\("data-explain-capability",(s|p)\.capability\)/g)||[]).length===2&&ui.includes(`function whyButton(attr,id){return ' <button type="button" class="why" '+attr+'="'+safe(id)+'" aria-label="Why?">Why?</button>';}`),'both capability render paths (Panels.build and legacy fallback) carry a data-explain-capability Why? button');
const rd=ui.slice(ui.indexOf('function renderDeviceContinuity()'),ui.indexOf('function whyButton('));
check(rd.includes('whyButton("data-explain-continuity",c.id)'),'each device-continuity check row carries a data-explain-continuity Why? button');
check(/function explanationRecord\(\)\{const x=state\.explainedOutcome;if\(x&&x\.record\)return x\.record;const d=state\.intentDraft;if\(d\)(return |\{const r=)/.test(ui),'explanationRecord precedence: explainedOutcome, then intent draft, then kvIngress');
check(ui.includes('xc.dataset.explainClear!==undefined')&&ui.includes('xb.dataset.explainCapability!==undefined')&&ui.includes('xd.dataset.explainContinuity!==undefined'),'dispatcher guards use dataset.<name>!==undefined like the copy handler');
check(ui.includes('function setMode(mode){state.mode=mode;state.intentDraft=null;state.explainedOutcome=null;'),'context switch clears the explicit selection');
check(ui.includes('receiptBacked(s.state==="OBSERVED",ref,')&&ui.includes('receiptBacked(c.state==="ALLOW"||c.state==="PROJECTED",c.provenance_ref,')&&ui.includes('receiptBacked(k.disposition==="ALLOW",k.provenance_ref,')&&/function receiptBacked\(allowed,ref,description,otherwise\)\{const evidence=provenanceEvidence\(ref,description\);if\(!allowed\)return \{disposition:otherwise,consequence_observation:"NOT_AUTHENTICALLY_OBSERVED",evidence:evidence\};return evidence\.length\?\{disposition:"ALLOW",consequence_observation:"OBSERVED",evidence:evidence\}:\{disposition:"UNKNOWN",consequence_observation:"UNKNOWN",evidence:\[\]\};\}/.test(ui)&&ui.includes('"CAPABILITY_STATUS_ABSENT"')&&ui.includes('requested_action:"Observe the "+String(s.label||id)+" capability projection in this Workspace",authority_source:"INTERLOCK_INTR"')&&ui.includes('requested_action:"Accept device continuity check "+String(c.id)+" "+String(c.title),authority_source:"NONE"'),'explained records are ALLOW only with a receipt (otherwise UNKNOWN) and name their authority source');
check(/\.item\.cap button\.why,\.evidence-row button\.why,\.panel-row button\.why\{[^}]*font-size:12px[^}]*max-width:100%\}/.test(css),'compact Why? button style for panel items, panel rows and evidence rows');
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
  vm.createContext(ctx);for(const s of [caps,auth,binding,continuity,nodeBinding,device].concat(opts.panels?[read('assets/workspace-panels.js')]:[]))vm.runInContext(s,ctx);if(opts.contract!==false)vm.runInContext(src,ctx);
  ['StegVerseWorkspaceCapabilities','StegVerseWorkspaceSessionAuthentication','StegVerseWorkspaceAssistantBinding','StegVerseWorkspaceAssistantContinuity','StegVerseWorkspaceNodeBinding','StegVerseWorkspaceDeviceContinuity','StegVerseWorkspaceExplanation','StegVerseWorkspacePanels'].forEach(k=>{if(ctx[k])ctx.window[k]=ctx[k];});
  vm.runInContext(ui,ctx);
  const click=target=>docListeners.click({target:{closest:sel=>target[sel]||null}});
  return {els,click,switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}}),ctx};}
const NB_LOCAL={schema:'stegverse.workspace.node-binding/v1',disposition:'ALLOW',predicate:'REGISTERED_NODE_DIRECTLY_OBSERVED',node_id:'SV-NODE-'+'a'.repeat(24),source:'DEVICE_LOCAL_REGISTRATION',identity_minted_by_page:false};
const jsonOf=html=>{const text=preOf(html);return text?JSON.parse(text):null;};
(async()=>{
  const wait=()=>new Promise(r=>setTimeout(r,10));
  // Shipped state on the owner's phone: the ingress failure is explained as FAILED_CLOSED with the bridge detail as the reason.
  let h=harness({bridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('FAIL_CLOSED: DEVICE_KV sovereign InTr ingress unavailable for WORKSPACE_PERSONAL_PROJECTION')),lastNodeBinding:()=>NB_LOCAL}});await wait();
  let html=h.els.explanation.innerHTML;
  check(html.startsWith('<div class="explanation-prose"><p><strong>What happened:</strong> The request &#39;Open your Personal KV Workspace from this device&#39; could not be evaluated because a required prerequisite is not established, so the system refused to act.</p>'),'prose first: '+html.slice(0,300));
  check(html.includes('<p><strong>Why:</strong> Because no authorized route yet delivers your KnowledgeVault to this workspace independently of a particular device; FAIL_CLOSED: DEVICE_KV sovereign InTr ingress unavailable for WORKSPACE_PERSONAL_PROJECTION.</p>')&&html.includes('<p><strong>Outcome:</strong> Failed closed; nothing was executed.</p>')&&html.includes('AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE')&&html.includes('<li>Nothing happened; your data and state are unchanged.</li>'),'reason, summary, predicate and safe steps rendered: '+html.slice(0,1200));
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
  // Admitted projection: the bound KV delivery's provenance is the receipt of the read transition, so it is ALLOW with
  // that receipt (receipt invariant: no ALLOW without its receipt, and no authorized-but-unverified state).
  const REV='a'.repeat(64);
  const projection={schema:'stegverse.kv.personal-workspace-projection/v1',state:'KV_WORKSPACE_PROJECTED',workspace_type:'PERSONAL',principals:[],organizations:[],memberships:[],feed:[],assistant:null,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,projection_metadata:{schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:new Date(Date.now()-60000).toISOString().replace(/\.\d{3}Z$/,'Z'),observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:REV,provenance_ref:'kv-workspace-source:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'},authority_effect:'NONE'};
  h=harness({bridge:{loadPersonalWorkspace:()=>Promise.resolve(projection),lastNodeBinding:()=>NB_LOCAL}});await wait();html=h.els.explanation.innerHTML;j=jsonOf(html);
  check(j&&j.outcome.disposition==='ALLOW'&&j.outcome.outcome_class==='SUCCESS_VERIFIED'&&j.outcome.predicate==='PERSONAL_KV_PROJECTION_ADMITTED'&&j.execution.executed===true&&j.evidence.length===1&&j.evidence[0].kind==='PROVENANCE_REF'&&j.evidence[0].ref==='kv-workspace-source:sha256:'+REV&&E.conforms(j).ok===true&&!/AUTHORIZED_NOT_VERIFIED|not verified/.test(html),'admitted projection is ALLOW with its delivery receipt: '+JSON.stringify(j&&j.outcome));
  // Bridge absent: WORKSPACE_DEVICE_KV_BRIDGE_UNAVAILABLE explained.
  h=harness({bridge:null});await wait();check(h.els.explanation.innerHTML.includes('WORKSPACE_DEVICE_KV_BRIDGE_UNAVAILABLE')&&h.els.explanation.innerHTML.includes('<strong>What happened:</strong>'),'absent bridge explained');
  // No outcome yet (bridge never answers): NOT_EVALUATED empty state, no artifact.
  h=harness({bridge:{loadPersonalWorkspace:()=>new Promise(()=>{}),lastNodeBinding:()=>null}});await wait();
  check(h.els.explanation.innerHTML==='<div class="empty">NOT_EVALUATED · no governed outcome has been reported to this page yet, so there is nothing to explain.</div>','empty state before any outcome: '+h.els.explanation.innerHTML);
  // Contract not loaded.
  h=harness({contract:false,bridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('x')),lastNodeBinding:()=>null}});await wait();
  check(h.els.explanation.innerHTML==='<div class="empty">Explanation contract unavailable (EXPLANATION_CONTRACT_UNAVAILABLE); the canonical disposition above stands on its own.</div>','absent contract falls back');
  // Explain on request: a capability "Why?" click explains that status (legacy fallback path in this harness: no Panels contract loaded).
  h=harness({bridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('FAIL_CLOSED: DEVICE_KV sovereign InTr ingress unavailable for WORKSPACE_PERSONAL_PROJECTION')),lastNodeBinding:()=>NB_LOCAL}});await wait();
  const capsHtml=h.els.capabilities.innerHTML;
  const feedItem=capsHtml.match(/<div class="item cap"><strong>Feed<\/strong> <span class="pill warn">([A-Z_]+)<\/span> <button type="button" class="why" data-explain-capability="FEED" aria-label="Why\?">Why\?<\/button><div class="muted">([A-Za-z0-9_:.-]+)/);
  check(!!feedItem&&(capsHtml.match(/data-explain-capability="/g)||[]).length===(capsHtml.match(/<div class="item cap">/g)||[]).length&&!/data-action|data-task-action/.test(capsHtml),'every capability item carries exactly one Why? button and no action control: '+capsHtml.slice(0,300));
  const feedState=feedItem[1],feedPredicate=feedItem[2];
  const before=h.els.explanation.innerHTML;
  h.click({'[data-explain-capability]':{dataset:{explainCapability:'FEED'}}});html=h.els.explanation.innerHTML;j=jsonOf(html);
  check(html.startsWith('<div class="muted explanation-selected">Explaining on request: capability <strong>FEED</strong>. <button type="button" data-explain-clear>Back to latest outcome</button></div><div class="explanation-prose">')&&html.includes(feedPredicate),'capability Why? names that capability and its predicate: '+html.slice(0,400));
  check(j&&j.outcome.predicate===feedPredicate&&j.outcome.outcome_class===(feedState==='OBSERVED'?'SUCCESS_VERIFIED':'FAILED_CLOSED')&&j.authorization.requested_action==='Observe the Feed capability projection in this Workspace'&&j.authorization.authority_source==='INTERLOCK_INTR'&&j.execution.executed===(feedState==='OBSERVED')&&j.execution.consequence_observation===(feedState==='OBSERVED'?'OBSERVED':'NOT_AUTHENTICALLY_OBSERVED')&&E.conforms(j).ok===true,'capability artifact: '+JSON.stringify(j&&j.outcome)+' '+JSON.stringify(j&&j.execution));
  check(feedState!=='OBSERVED'&&j.outcome.disposition==='FAIL_CLOSED'&&j.authorization.authorized===false,'an unobserved capability explains as FAIL_CLOSED, never ALLOW: '+feedState);
  {const cctx={};cctx.globalThis=cctx;vm.createContext(cctx);vm.runInContext(caps,cctx);const capReasons=cctx.StegVerseWorkspaceCapabilities.reasons;
   check(typeof capReasons[feedPredicate]==='string'&&j.prose.why.startsWith('Because '+capReasons[feedPredicate])&&!/prerequisite named by/.test(j.prose.why),'capability Why? leads with the catalogued reason: '+j.prose.why);}
  // Unknown capability id: nothing changes.
  h.click({'[data-explain-capability]':{dataset:{explainCapability:'NOT_A_CAPABILITY'}}});check(h.els.explanation.innerHTML===html,'unknown capability id changes nothing');
  // Back to latest outcome restores the ingress explanation.
  h.click({'[data-explain-clear]':{dataset:{explainClear:''}}});check(h.els.explanation.innerHTML===before&&!before.includes('Explaining on request'),'Back to latest outcome restores the ingress explanation');
  // Device-continuity "Why?": the check row's state and predicate are explained under authority_source NONE.
  const devHtml=h.els.deviceContinuity.innerHTML;
  const dr3=devHtml.match(/<div class="evidence-row"><strong>DR3 ([^<]+)<\/strong> <span class="pill (ok|warn)">([A-Z_]+)<\/span> ([A-Za-z0-9_:.-]+) <button type="button" class="why" data-explain-continuity="DR3" aria-label="Why\?">Why\?<\/button>/);
  check(!!dr3&&(devHtml.match(/data-explain-continuity="/g)||[]).length===(devHtml.match(/<div class="evidence-row">/g)||[]).length,'every continuity check row carries one Why? button: '+devHtml.slice(0,400));
  h.click({'[data-explain-continuity]':{dataset:{explainContinuity:'DR3'}}});html=h.els.explanation.innerHTML;j=jsonOf(html);
  check(html.startsWith('<div class="muted explanation-selected">Explaining on request: device continuity check <strong>DR3</strong>. <button type="button" data-explain-clear>Back to latest outcome</button></div>')&&j&&j.outcome.predicate===dr3[4]&&((dr3[3]==='ALLOW'||dr3[3]==='PROJECTED')?((j.outcome.disposition==='ALLOW'&&j.outcome.outcome_class==='SUCCESS_VERIFIED'&&j.execution.executed===true)||(j.outcome.disposition==='UNKNOWN'&&j.outcome.outcome_class==='UNOBSERVED'&&j.execution.executed===false)):(j.outcome.disposition===(dr3[3]==='DENY'?'DENY':'FAIL_CLOSED')&&j.outcome.outcome_class===(dr3[3]==='DENY'?'DENIED':'FAILED_CLOSED')&&j.execution.executed===false))&&j.authorization.requested_action==='Accept device continuity check DR3 '+unesc(dr3[1])&&j.authorization.authority_source==='NONE'&&E.conforms(j).ok===true,'continuity artifact: '+JSON.stringify(j&&j.outcome)+' '+JSON.stringify(j&&j.authorization));
  // DR2 "Why?" carries the plain-language reason from the session-authentication reason catalog, not just the predicate.
  {const rctx={};rctx.globalThis=rctx;vm.createContext(rctx);vm.runInContext(auth,rctx);const reasons=rctx.StegVerseWorkspaceSessionAuthentication.reasons;
   h.click({'[data-explain-continuity]':{dataset:{explainContinuity:'DR2'}}});const j2=jsonOf(h.els.explanation.innerHTML);
   check(j2&&typeof reasons[j2.outcome.predicate]==='string'&&j2.prose.why.startsWith('Because '+reasons[j2.outcome.predicate])&&!/prerequisite named by/.test(j2.prose.why)&&E.conforms(j2).ok===true,'DR2 why uses the catalogued reason: '+JSON.stringify(j2&&j2.prose&&j2.prose.why));}
  // DR3 and DR4 "Why?" lead with a catalogued reason from the node-binding / device / assistant catalogs.
  {const rctx={};rctx.globalThis=rctx;vm.createContext(rctx);for(const src of [auth,binding,continuity,nodeBinding,device])vm.runInContext(src,rctx);
   const pick=(id,p)=>{const k=p.indexOf(':')>0?p.slice(0,p.indexOf(':')):p;const order=id==='DR3'?[rctx.StegVerseWorkspaceNodeBinding,rctx.StegVerseWorkspaceDeviceContinuity]:[rctx.StegVerseWorkspaceAssistantContinuity,rctx.StegVerseWorkspaceAssistantBinding,rctx.StegVerseWorkspaceSessionAuthentication,rctx.StegVerseWorkspaceDeviceContinuity];for(const m of order)if(m&&m.reasons&&typeof m.reasons[k]==='string')return m.reasons[k];return null;};
   for(const id of ['DR3','DR4']){h.click({'[data-explain-continuity]':{dataset:{explainContinuity:id}}});const jx=jsonOf(h.els.explanation.innerHTML);const r=jx&&pick(id,jx.outcome.predicate);
    check(jx&&typeof r==='string'&&jx.prose.why.startsWith('Because '+r)&&E.conforms(jx).ok===true,id+' why uses the catalogued reason: '+JSON.stringify(jx&&jx.outcome.predicate)+' '+JSON.stringify(jx&&jx.prose.why));}}
  // A DENY check is explained as DENY, not collapsed into FAIL_CLOSED: the contract keeps the two dispositions distinct.
  {const hd=harness({bridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('x')),lastNodeBinding:()=>Object.assign({},NB_LOCAL,{disposition:'DENY',predicate:'NODE_BINDING_REFUSED'})}});await wait();
   check(/<strong>DR3 [^<]+<\/strong> <span class="pill warn">DENY<\/span> NODE_BINDING_REFUSED/.test(hd.els.deviceContinuity.innerHTML),'fixture yields a DR3 DENY row: '+hd.els.deviceContinuity.innerHTML.slice(0,300));
   hd.click({'[data-explain-continuity]':{dataset:{explainContinuity:'DR3'}}});const jd=jsonOf(hd.els.explanation.innerHTML);
   check(jd&&jd.outcome.disposition==='DENY'&&jd.outcome.predicate==='NODE_BINDING_REFUSED'&&jd.authorization.authorized===false&&jd.execution.executed===false&&E.conforms(jd).ok===true,'a DENY continuity check must explain as DENY: '+JSON.stringify(jd&&jd.outcome));}
  // Precedence: an explicit selection outranks the intent draft; clearing it falls back to the draft; a context switch clears both.
  h.switchTo('developer');check(!h.els.explanation.innerHTML.includes('Explaining on request'),'context switch clears the selection');
  h.click({'[data-developer-action]':{dataset:{developerAction:'DEVELOPER_CODE_CHANGE_REQUEST'}}});check(jsonOf(h.els.explanation.innerHTML).authorization.requested_action==='DEVELOPER_CODE_CHANGE_REQUEST','draft explained in developer context');
  {const jd=jsonOf(h.els.explanation.innerHTML),pr=h.ctx&&h.ctx.StegVerseWorkspacePageReasons;const want='no governed route for submitting this request is connected to this page yet, so the draft is shown for review and nothing is sent';check(jd.outcome.predicate==='WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND'&&jd.prose.why==='Because '+want+'.'&&(!pr||pr.WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND===want)&&E.conforms(jd).ok===true,'intent-draft Why? uses the page reason: '+jd.prose.why);}
  h.click({'[data-explain-capability]':{dataset:{explainCapability:'DEV_CODE'}}});j=jsonOf(h.els.explanation.innerHTML);
  check(j&&j.authorization.requested_action==='Observe the Code (developer) capability projection in this Workspace'&&h.els.intentDraft.innerHTML.includes('DEVELOPER_CODE_CHANGE_REQUEST'),'explicit selection outranks the intent draft without discarding it: '+JSON.stringify(j&&j.authorization));
  h.click({'[data-explain-clear]':{dataset:{explainClear:''}}});check(jsonOf(h.els.explanation.innerHTML).authorization.requested_action==='DEVELOPER_CODE_CHANGE_REQUEST','clearing the selection falls back to the draft');
  // Observed capability (admitted projection): ALLOW with the projection provenance (the KV delivery receipt) as evidence.
  h=harness({bridge:{loadPersonalWorkspace:()=>Promise.resolve(projection),lastNodeBinding:()=>NB_LOCAL}});await wait();
  check(h.els.capabilities.innerHTML.includes('<strong>Feed</strong> <span class="pill ok">OBSERVED</span> <button type="button" class="why" data-explain-capability="FEED"'),'feed observed under the admitted projection');
  h.click({'[data-explain-capability]':{dataset:{explainCapability:'FEED'}}});html=h.els.explanation.innerHTML;j=jsonOf(html);
  check(j&&j.outcome.disposition==='ALLOW'&&j.outcome.outcome_class==='SUCCESS_VERIFIED'&&j.execution.executed===true&&j.execution.execution_state==='VERIFIED'&&j.evidence.length===1&&j.evidence[0].kind==='PROVENANCE_REF'&&j.evidence[0].ref==='kv-workspace-source:sha256:'+REV&&E.conforms(j).ok===true&&!/AUTHORIZED_NOT_VERIFIED|not verified/.test(html),'observed capability is ALLOW with its delivery receipt: '+JSON.stringify(j&&j.outcome));
  // Explanation fidelity with the panels contract loaded: when a panel downgrades an OBSERVED status (here a CryptoBot
  // projection that claims trade authority), "Why?" explains the panel's FAIL_CLOSED outcome and its catalogued reason,
  // never the ALLOW status it overrode.
  {const cb=Object.assign({},{schema:'stegverse.kv.cryptobot-portfolio-projection/v1',workspace_type:'PERSONAL',state:'KV_PORTFOLIO_PROJECTED',trade_authority_granted:true,provider_operation_authorized:false,credential_material_present:false,workspace_grants_authority:false,authority_effect:'NONE',portfolio:{positions:[{asset:'ETH',quantity:1}]},projection_metadata:projection.projection_metadata});
   const hp=harness({panels:true,bridge:{loadPersonalWorkspace:()=>Promise.resolve(projection),loadPersonalProjections:()=>Promise.resolve([cb]),lastNodeBinding:()=>NB_LOCAL}});await wait();
   check(hp.els.capabilities.innerHTML.includes('<strong>CryptoBot portfolio</strong> <span class="pill warn">MALFORMED</span>')||/CRYPTOBOT_PORTFOLIO[^]*MALFORMED|MALFORMED[^]*PROJECTION_TRADE_AUTHORITY_INVALID/.test(hp.els.capabilities.innerHTML),'panel downgraded to MALFORMED: '+hp.els.capabilities.innerHTML.slice(0,400));
   // The card itself leads with the plain-language reason (the predicate stays beside it for reference), for panel and capability predicates alike.
   {const PRS=hp.ctx.window.StegVerseWorkspacePanels.reasons,CRS=hp.ctx.window.StegVerseWorkspaceCapabilities.reasons,capHtml=hp.els.capabilities.innerHTML;const cap=t=>t.charAt(0).toUpperCase()+t.slice(1)+'.';
    check(capHtml.includes('PROJECTION_TRADE_AUTHORITY_INVALID')&&capHtml.includes('<div class="reason">'+cap(PRS.PROJECTION_TRADE_AUTHORITY_INVALID).replace(/'/g,'&#39;')+'</div>')||capHtml.includes('<div class="reason">'+cap(PRS.PROJECTION_TRADE_AUTHORITY_INVALID)+'</div>'),'MALFORMED panel card shows its plain-language reason: '+capHtml.slice(0,500));
    const reasonDivs=(capHtml.match(/<div class="reason">/g)||[]).length,items=(capHtml.match(/<div class="item cap">/g)||[]).length;
    check(reasonDivs>0&&reasonDivs<=items&&!/<div class="reason">[^<]*[A-Z]{2,}_[A-Z]/.test(capHtml),'reason lines are plain language, at most one per card: '+reasonDivs+'/'+items);
    check(Object.values(CRS).some(t=>capHtml.includes(cap(t).replace(/'/g,'&#39;'))||capHtml.includes(cap(t))),'capability-status predicates also show their catalogued reason');}
   hp.click({'[data-explain-capability]':{dataset:{explainCapability:'CRYPTOBOT_PORTFOLIO'}}});const jj=jsonOf(hp.els.explanation.innerHTML);
   const PR=hp.ctx.window.StegVerseWorkspacePanels.reasons;
   check(jj&&jj.outcome.disposition==='FAIL_CLOSED'&&jj.outcome.predicate==='PROJECTION_TRADE_AUTHORITY_INVALID'&&jj.authorization.authorized===false&&jj.prose.why.startsWith('Because '+PR.PROJECTION_TRADE_AUTHORITY_INVALID),'Why? must explain the panel outcome, not the overridden status: '+JSON.stringify(jj&&{o:jj.outcome,why:jj.prose&&jj.prose.why}));}
  // Every predicate the panels contract can put on a panel has a plain-language reason, and no reason is orphaned.
  {const ps=read('assets/workspace-panels.js');const produced=new Set([...ps.matchAll(/(?:problem:|bad\()"([A-Z][A-Z0-9_]+)"/g)].map(m=>m[1]).concat([...ps.matchAll(/panel\.predicate=([^;]*);/g)].flatMap(m=>[...m[1].matchAll(/"([A-Z][A-Z0-9_]+)"/g)].map(x=>x[1])),[...ps.matchAll(/predicate:"(CAPABILITY_STATUS_ABSENT)"/g)].map(m=>m[1])));
   const pctx={};pctx.globalThis=pctx;vm.createContext(pctx);vm.runInContext(ps,pctx);const R=pctx.StegVerseWorkspacePanels.reasons;
   check(Object.isFrozen(R)&&produced.size>=12,'panel predicates found: '+[...produced].join(','));
   for(const p of produced)check(typeof R[p]==='string','panel predicate without a reason: '+p);
   for(const p of Object.keys(R))check(produced.has(p),'reason for a predicate the panels never produce: '+p);
   for(const [p,t] of Object.entries(R))check(t.trim()===t&&t.length>20&&/^[a-z]/.test(t)&&!t.endsWith('.')&&!/[A-Z]{2,}_[A-Z]/.test(t),'panel reason is plain language: '+p);}
  // Conformance gate on the page: a contract whose conforms() fails withholds the artifact.
  const real=h.ctx.window.StegVerseWorkspaceExplanation;
  h.ctx.window.StegVerseWorkspaceExplanation={build:real.build,prose:real.prose,conforms:()=>({ok:false,violations:['cross_field:test_violation:$.outcome']})};
  h.click({'[data-explain-clear]':{dataset:{explainClear:''}}});
  check(h.els.explanation.innerHTML==='<div class="empty">Explanation withheld (EXPLANATION_NONCONFORMING · cross_field:test_violation:$.outcome); the canonical disposition above stands on its own.</div>','non-conforming artifact withheld: '+h.els.explanation.innerHTML);
  h.ctx.window.StegVerseWorkspaceExplanation={build:real.build,prose:real.prose};
  h.click({'[data-explain-clear]':{dataset:{explainClear:''}}});
  check(h.els.explanation.innerHTML.startsWith('<div class="empty">Explanation withheld (EXPLANATION_NONCONFORMING · conformance_check_unavailable)'),'a contract without conforms() withholds too');
  h.ctx.window.StegVerseWorkspaceExplanation=real;
  // Canonical producers may emit lower-case predicate names (crypto-bot snapshot_* refusals); they are copied verbatim.
{const E=sb.StegVerseWorkspaceExplanation;const low=E.build({disposition:'FAIL_CLOSED',predicate:'snapshot_position_field_missing:value_usd',requested_action:'Project the CryptoBot portfolio snapshot into the WorkSpace projection',authority_source:'NONE',consequence_observation:'NOT_AUTHENTICALLY_OBSERVED',evidence:[{kind:'SOURCE_REF',ref:'StegVerse-Labs/crypto-bot:scripts/project_portfolio_snapshot_for_workspace.py',description:'The producer that refused'}]},{repository:'StegVerse-Labs/crypto-bot',surface_id:'workspace-portfolio-projection'});check(low.schema==='stegverse.user-facing-explanation/v1'&&low.outcome&&low.outcome.predicate==='snapshot_position_field_missing:value_usd'&&low.outcome.outcome_class==='FAILED_CLOSED','lower-case producer predicate copied verbatim');}
{const E=sb.StegVerseWorkspaceExplanation;const ok=['No Bearer credentials are shown here.','task-runner ask-flow risk-score','The ghost_ ledger and akia notes','xox is not a token'].every(w=>{const r=E.build(Object.assign({},{disposition:'DENY',predicate:'WORKSPACE_GRANT_REVOKED',requested_action:'MESSAGE',authority_source:'MANIFEST',why:w}),SURFACE);return r&&r.schema===SCHEMA&&r.outcome;});check(ok,'ordinary words near secret prefixes are not refused');}
// Text that displays as something else (canonical parity with StegVerse-Labs/.github _reject_hidden_text): refused in every
// producer-controlled field by the builder, and flagged by conforms(); layout whitespace and non-Latin scripts still build.
{const E=sb.StegVerseWorkspaceExplanation;const base={disposition:'DENY',predicate:'WORKSPACE_GRANT_REVOKED',requested_action:'MESSAGE',authority_source:'MANIFEST',evidence:[{kind:'SOURCE_REF',ref:'kv:x',description:'d'}]};
 for(const ch of ['\u202E','\u2066','\u200B','\u0000','\u2028','\ud800']){
  for(const [patch,path] of [[{requested_action:'MESS'+ch+'AGE'},'requested_action'],[{why:'ok '+ch+'hidden'},'why'],[{evidence:[{kind:'SOURCE_REF',ref:'kv:'+ch+'x',description:'d'}]},'evidence[0].ref'],[{evidence:[{kind:'SOURCE_REF',ref:'kv:x',description:'d'+ch}]},'evidence[0].description']]){
   const r=E.build(Object.assign({},base,patch),SURFACE);check(refused(r)&&r.reason==='text_not_displayable:'+path,'hidden text refused at '+path+' for U+'+ch.charCodeAt(0).toString(16)+': '+JSON.stringify(r).slice(0,160));}
  const rs=E.build(base,{repository:'StegVerse-Labs/Site',surface_id:'work'+ch+'space'});check(refused(rs)&&rs.reason==='text_not_displayable:surface_id','hidden text in the surface descriptor refused');
  const good=E.build(base,SURFACE);const tampered=JSON.parse(JSON.stringify(good));tampered.evidence[0].description='Receipt'+ch;const c=E.conforms(tampered);check(c.ok===false&&c.violations.some(v=>v.startsWith('text_not_displayable')),'conforms() flags hidden text in an artifact: '+JSON.stringify(c.violations));}
 for(const w of ['line one\nline two','tab\tseparated','crlf\r\nend','Grüße — café','日本語の説明','عربي']){const r=E.build(Object.assign({},base,{why:w}),SURFACE);check(r&&r.schema===SCHEMA&&r.outcome&&E.conforms(r).ok===true,'layout whitespace and non-Latin text still build: '+JSON.stringify(w));}}
console.log('WORKSPACE_EXPLANATION_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
