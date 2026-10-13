// DEV-P6 Universal Governance Integration (Site#1509 owner-approved scope 6112777652): the three developer experience
// modes are presentation only and validate through the one framework-neutral contract (ChatGPT, Site#1537); GitHub is
// the first conforming REFERENCE adapter and gets no privilege; the eight synthetic conformance fixtures never
// masquerade as authenticated transitions; the page explains every outcome through the merged explanation card and
// executes, submits, certifies and persists nothing. GUIDANCE-NEVER-GATES: switching modes changes no authority and no
// state, and educational completion is never an authorization, certification or prerequisite.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const src=read('assets/workspace-integration-conformance.js'),contract=read('assets/workspace-governance-integration.js'),explanation=read('assets/workspace-explanation.js'),ui=read('assets/workspace.js'),page=read('workspace.html'),css=read('assets/workspace.css'),workflow=read('.github/workflows/workspace-kv-binding-validation.yml');
const caps=read('assets/workspace-capabilities.js'),auth=read('assets/workspace-session-authentication.js'),binding=read('assets/workspace-assistant-binding.js'),continuity=read('assets/workspace-assistant-continuity.js'),nodeBinding=read('assets/workspace-node-binding.js'),device=read('assets/workspace-device-continuity.js');
const bootstrap=JSON.parse(read('data/workspace/bootstrap.json'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
// Browser-like sandbox: no `module`, so the UMD contract must bind its global the way a <script> tag does.
const sb={};vm.createContext(sb);vm.runInContext(contract,sb);vm.runInContext(explanation,sb);vm.runInContext(src,sb);
const G=sb.StegVerseGovernanceIntegration,E=sb.StegVerseWorkspaceExplanation,C=sb.StegVerseWorkspaceIntegrationConformance;
const SURFACE={repository:'StegVerse-Labs/Site',surface_id:'workspace'};
const MODES=['DIRECT_INTEGRATION','GUIDED_INTEGRATION','ASSISTANCE_ON_DEMAND'];
const IDS=['CONF-ALLOW','CONF-DENY','CONF-FAIL-CLOSED','CONF-INVALID-MANIFEST','CONF-REVOKED-CONSENT','CONF-MISSING-CREDENTIAL','CONF-ABSENT-RECEIPT','CONF-UNOBSERVED-RUNTIME'];
const DESCRIPTOR_SCHEMA='stegverse.workspace.governance-integration/v1';

// 1. Module identity; everything exported is frozen; the UMD contract binds its global without `module`.
check(typeof sb.module==='undefined'&&G&&typeof G.validate==='function'&&eq(G.MODES,MODES),'UMD contract binds globalThis.StegVerseGovernanceIntegration when module is undefined');
check(C&&C.schema==='stegverse.workspace.integration-conformance/v1'&&C.authority_effect==='NONE'&&C.DEFAULT_MODE==='DIRECT_INTEGRATION'&&eq(C.MODES,MODES)&&C.descriptor_schema===DESCRIPTOR_SCHEMA&&C.contract_ref==='StegVerse-Labs/Site:assets/workspace-governance-integration.js','module identity');
check(Object.isFrozen(C)&&Object.isFrozen(C.MODES)&&Object.isFrozen(C.REFERENCE_ADAPTER)&&Object.isFrozen(C.REFERENCE_ADAPTER.capabilities)&&Object.isFrozen(C.FIXTURES)&&C.FIXTURES.every(f=>Object.isFrozen(f)&&Object.isFrozen(f.outcome)&&Object.isFrozen(f.outcome.evidence)&&(!f.outcome.remediation_draft||Object.isFrozen(f.outcome.remediation_draft))),'contract, reference adapter and fixtures are deep-frozen');
for(const k of ['selectMode','validateDescriptor','runConformance','buildIntegrationDraft','findFixture'])check(typeof C[k]==='function','exports '+k);

// 2. Source scope: no I/O, no browser access, no runtime, no scheduler, no dependency; ALLOW appears only as the
// presentation-only mode selection. Receipt invariant: the synthetic admitted-manifest fixture holds no receipt, so it is
// UNKNOWN to this surface, never ALLOW.
const code=src.split('\n').filter(l=>!/^\s*\/\//.test(l)).join('\n');
check(!/fetch\(|XMLHttpRequest|localStorage|sessionStorage|indexedDB|navigator|window|document/.test(code),'contract performs no I/O and reads nothing from the browser');
check(!/registerDevice|setTimeout|setInterval|Promise|async |import\(|require\(|eval\(|new Function/.test(code),'no scheduler, runtime, dependency or dynamic code');
check((code.match(/disposition:"ALLOW"/g)||[]).length===1&&/disposition:"ALLOW",predicate:"INTEGRATION_MODE_PRESENTATION_ONLY"/.test(code)&&/disposition:"UNKNOWN",predicate:"INTEGRATION_MANIFEST_RECEIPT_NOT_HELD"/.test(code)&&!/NOT_VERIFIED/.test(code),'ALLOW only as presentation-only mode selection; the synthetic admitted manifest is UNKNOWN (receipt not held)');
check(/evidence_class:"SYNTHETIC_TEST"/.test(code)&&/certified:false/.test(code)&&/submitted:false/.test(code)&&/authority_effect:"NONE"/.test(code)&&!/certified:true|submitted:true|execution_observed:true/.test(code),'contract never certifies, submits or observes execution');
check(!/ghp_|Bearer |PRIVATE KEY|sk-[A-Za-z0-9]{16}/.test(src),'fixtures carry no secret-shaped material');
check(!/api\.github\.com|github\.com\/[A-Za-z]/.test(src)&&!/api\.github\.com|github\.com\/[A-Za-z]/.test(ui),'nothing reads GitHub');

// 3. Reference adapter: a conforming GitHub descriptor validated through the ChatGPT validator, with no privilege.
const R=C.REFERENCE_ADAPTER;
check(R.schema===DESCRIPTOR_SCHEMA&&R.framework_id==='github'&&R.adapter_version==='1.0.0'&&eq(R.capabilities,['READ_PROJECTION','SUBMIT_MANIFEST','OBSERVE_RECEIPT'])&&R.authority_effect==='NONE'&&R.governance_route==='SDK_MANIFEST_INTR'&&R.tutorial_required===false&&R.role==='REFERENCE_ADAPTER'&&R.mode===undefined,'reference adapter shape');
const rv=C.validateDescriptor(R,G.validate);
check(rv.descriptor_valid===true&&rv.disposition==='FAIL_CLOSED'&&rv.predicate==='AUTHENTIC_MANIFEST_BOUND_GOVERNANCE_TRANSITION_NOT_OBSERVED'&&rv.mode==='DIRECT_INTEGRATION'&&rv.guidance_required===false&&rv.submitted===false&&rv.certified===false&&rv.execution_observed===false&&rv.authority_effect==='NONE'&&rv.mode_independent===true&&rv.schema==='stegverse.workspace.governance-integration-validation/v1','reference adapter validates descriptor_valid:true through the contract: '+JSON.stringify(rv));
check(eq(Object.assign({},G.validate(R),{mode_independent:true}),rv),'validator result is returned unchanged plus mode_independent');
const external={schema:DESCRIPTOR_SCHEMA,framework_id:'gitlab.example',adapter_version:'0.1.0',capabilities:['READ_PROJECTION'],authority_effect:'NONE',governance_route:'SDK_MANIFEST_INTR',tutorial_required:false};
check(eq(C.validateDescriptor(external,G.validate),rv),'an externally supplied adapter validates identically (GitHub is a reference, not privileged)');
check(C.validateDescriptor(Object.assign({},R,{authority_effect:'ALLOW'}),G.validate).predicate==='ADAPTER_MUST_NOT_GRANT_AUTHORITY'&&C.validateDescriptor(Object.assign({},R,{governance_route:'DIRECT_GITHUB'}),G.validate).predicate==='CANONICAL_GOVERNANCE_ROUTE_REQUIRED','the GitHub reference gets no privilege: authority or route deviations are refused');
check(C.validateDescriptor(R,null).predicate==='INTEGRATION_CONTRACT_UNAVAILABLE'&&C.validateDescriptor(R,null).descriptor_valid===false&&C.validateDescriptor(R,null).disposition==='FAIL_CLOSED','absent validator fails closed');
check(C.validateDescriptor(R,()=>{throw new Error('x')}).predicate==='INTEGRATION_VALIDATOR_FAILED'&&C.validateDescriptor(R,()=>'nope').predicate==='INTEGRATION_VALIDATOR_RESULT_INVALID','throwing or malformed validator fails closed');
const foreign=C.validateDescriptor(R,()=>({disposition:'ALLOW',descriptor_valid:'yes'}));
check(foreign.disposition==='FAIL_CLOSED'&&foreign.descriptor_valid===false&&foreign.mode_independent===true,'a foreign validator cannot make the surface claim ALLOW or a non-boolean validity');

// 4. Mode selection is presentation only; unknown modes are refused.
for(const m of MODES){const s=C.selectMode(m);check(Object.isFrozen(s)&&s.schema===C.schema&&s.mode===m&&s.disposition==='ALLOW'&&s.predicate==='INTEGRATION_MODE_PRESENTATION_ONLY'&&s.guidance_required===false&&s.tutorial_required===false&&s.authority_effect==='NONE'&&s.state_changed===false,'selectMode '+m+': '+JSON.stringify(s));}
for(const bad of ['FORCED_TUTORIAL','direct_integration','',null,undefined,42,{},[]]){const s=C.selectMode(bad);check(s.disposition==='FAIL_CLOSED'&&s.predicate==='INTEGRATION_MODE_INVALID'&&s.mode===null&&s.state_changed===false&&s.authority_effect==='NONE'&&s.guidance_required===false,'selectMode refuses '+JSON.stringify(bad));}

// 5. Fixtures: eight synthetic records in the explanation-contract input shape; each explains and conforms; none can
// read as a verified execution.
check(C.FIXTURES.length===8&&eq(C.FIXTURES.map(f=>f.id),IDS),'eight fixtures with the required ids in order');
const AUTH=['TASK_REGISTRY','WORKERCOORDINATOR','INTERLOCK_INTR','MANIFEST','TV_TVC','KV_SKAP_VAULT','NONE'];
for(const f of C.FIXTURES){
  const o=f.outcome;
  check(f.evidence_class==='SYNTHETIC_TEST'&&f.synthetic===true&&f.authenticated_transition===false&&typeof f.title==='string'&&f.title.length>0,'fixture is synthetic: '+f.id);
  check(['ALLOW','DENY','FAIL_CLOSED','UNKNOWN'].includes(o.disposition)&&/^[A-Z][A-Z0-9_]+$/.test(o.predicate)&&typeof o.requested_action==='string'&&o.requested_action.includes(f.id)&&AUTH.includes(o.authority_source)&&['NOT_AUTHENTICALLY_OBSERVED','UNKNOWN'].includes(o.consequence_observation)&&typeof o.why==='string'&&o.why.startsWith('Synthetic fixture')&&Array.isArray(o.evidence)&&o.evidence.length===1&&o.evidence.every(e=>e.kind==='SOURCE_REF'&&e.ref==='StegVerse-Labs/Site:assets/workspace-integration-conformance.js#'+f.id&&typeof e.description==='string'),'fixture outcome shape: '+f.id+' '+JSON.stringify(o).slice(0,200));
  check(!(o.disposition==='ALLOW'&&o.consequence_observation==='OBSERVED'),'never ALLOW+OBSERVED: '+f.id);
  if(o.remediation_draft!==undefined)check(o.remediation_draft.submitted===false&&o.remediation_draft.manifest_admitted===false&&o.remediation_draft.authority_effect==='NONE_REQUEST_ONLY'&&o.remediation_draft.disposition==='FAIL_CLOSED'&&o.remediation_draft.fixture_id===f.id&&o.remediation_draft.tutorial_required===false&&o.remediation_draft.guidance_required===false,'fixture remediation draft is unsubmitted and non-authorizing: '+f.id);
  const a=E.build(o,SURFACE);
  check(a&&a.schema==='stegverse.user-facing-explanation/v1'&&a.predicate!=='EXPLANATION_NOT_BUILDABLE'&&E.conforms(a).ok===true,'fixture builds a conforming explanation artifact: '+f.id+' '+JSON.stringify(a&&(a.reason||E.conforms(a))));
  check(a.outcome.predicate===o.predicate&&a.outcome.disposition===o.disposition&&a.execution.executed===false&&a.execution.execution_state!=='VERIFIED'&&a.outcome.outcome_class!=='SUCCESS_VERIFIED'&&a.evidence.every(e=>e.kind==='SOURCE_REF')&&a.remediation_draft===(o.remediation_draft===undefined?null:a.remediation_draft)&&(a.remediation_draft===null||a.remediation_draft.submitted===false),'fixture never explains as a verified execution: '+f.id);
}
const by=Object.fromEntries(C.FIXTURES.map(f=>[f.id,f.outcome]));
const cls=id=>E.build(by[id],SURFACE).outcome.outcome_class;
check(by['CONF-ALLOW'].disposition==='UNKNOWN'&&by['CONF-ALLOW'].consequence_observation==='UNKNOWN'&&by['CONF-ALLOW'].predicate==='INTEGRATION_MANIFEST_RECEIPT_NOT_HELD'&&by['CONF-ALLOW'].authority_source==='MANIFEST'&&cls('CONF-ALLOW')==='UNOBSERVED','CONF-ALLOW: a synthetic admitted manifest holds no receipt, so it reads UNOBSERVED, never ALLOW');
check(by['CONF-DENY'].disposition==='DENY'&&by['CONF-DENY'].predicate==='INTEGRATION_MANIFEST_DENIED_BY_POLICY'&&cls('CONF-DENY')==='DENIED','CONF-DENY');
check(by['CONF-FAIL-CLOSED'].disposition==='FAIL_CLOSED'&&by['CONF-FAIL-CLOSED'].predicate==='AUTHENTIC_MANIFEST_BOUND_GOVERNANCE_TRANSITION_NOT_OBSERVED'&&cls('CONF-FAIL-CLOSED')==='FAILED_CLOSED','CONF-FAIL-CLOSED');
check(by['CONF-INVALID-MANIFEST'].disposition==='FAIL_CLOSED'&&by['CONF-INVALID-MANIFEST'].predicate==='ADAPTER_MANIFEST_SCHEMA_INVALID','CONF-INVALID-MANIFEST');
check(by['CONF-REVOKED-CONSENT'].disposition==='DENY'&&by['CONF-REVOKED-CONSENT'].predicate==='INTEGRATION_CONSENT_REVOKED','CONF-REVOKED-CONSENT');
check(by['CONF-MISSING-CREDENTIAL'].disposition==='FAIL_CLOSED'&&by['CONF-MISSING-CREDENTIAL'].predicate==='CAPABILITY_SCOPED_CREDENTIAL_MISSING','CONF-MISSING-CREDENTIAL');
check(by['CONF-ABSENT-RECEIPT'].disposition==='FAIL_CLOSED'&&by['CONF-ABSENT-RECEIPT'].predicate==='TRANSITION_RECEIPT_ABSENT','CONF-ABSENT-RECEIPT');
check(by['CONF-UNOBSERVED-RUNTIME'].disposition==='UNKNOWN'&&by['CONF-UNOBSERVED-RUNTIME'].predicate==='RUNTIME_NOT_AUTHENTICALLY_OBSERVED'&&by['CONF-UNOBSERVED-RUNTIME'].consequence_observation==='UNKNOWN'&&cls('CONF-UNOBSERVED-RUNTIME')==='UNOBSERVED','CONF-UNOBSERVED-RUNTIME is UNKNOWN');
check(C.findFixture('CONF-ALLOW')===C.FIXTURES[0]&&C.findFixture('CONF-NOPE')===null&&C.findFixture(undefined)===null,'findFixture');

// 6. runConformance never authorizes, certifies or submits; fixtures are listed even for an invalid descriptor.
const run=C.runConformance(R,G.validate);
check(run.schema===C.schema&&run.disposition==='FAIL_CLOSED'&&run.predicate==='SYNTHETIC_CONFORMANCE_ONLY'&&run.certified===false&&run.submitted===false&&run.authority_effect==='NONE'&&run.authenticated_transition_observed===false&&run.evidence_class==='SYNTHETIC_TEST','run never ALLOW/certified/submitted: '+JSON.stringify(run).slice(0,200));
check(eq(run.descriptor_validation,rv)&&run.fixtures.length===8&&run.fixtures.every((f,i)=>f.id===IDS[i]&&f.synthetic===true&&f.evidence_class==='SYNTHETIC_TEST'&&f.authenticated_transition===false&&f.outcome===C.FIXTURES[i].outcome&&f.disposition===f.outcome.disposition&&f.predicate===f.outcome.predicate&&f.consequence_observation===f.outcome.consequence_observation),'run lists each fixture with its outcome and synthetic marker');
const badRun=C.runConformance({schema:'x'},G.validate);
check(badRun.descriptor_validation.descriptor_valid===false&&badRun.descriptor_validation.predicate==='ADAPTER_SCHEMA_NOT_SUPPORTED'&&badRun.fixtures.length===8&&badRun.disposition==='FAIL_CLOSED'&&badRun.certified===false,'invalid descriptor: fixtures still listed, descriptor_valid false');
check(C.runConformance(null,null).descriptor_validation.predicate==='INTEGRATION_CONTRACT_UNAVAILABLE'&&C.runConformance(null,null).fixtures.length===8,'absent validator: run fails closed and still lists fixtures');
const runText=JSON.stringify(run);
check(!runText.includes('"certified":true')&&!runText.includes('"submitted":true')&&!runText.includes('"OBSERVED"')&&!runText.includes('"execution_observed":true'),'run output never claims certification, submission or observation');

// 7. Draft invariants.
const d=C.buildIntegrationDraft(R,rv,'DIRECT_INTEGRATION');
check(d.schema_version==='stegverse.workspace.interaction-request.v1'&&d.action==='DEVELOPER_INTEGRATION_SUBMISSION_REQUEST'&&d.workspace_type==='DEVELOPER'&&d.framework_id==='github'&&d.adapter_version==='1.0.0'&&d.mode==='DIRECT_INTEGRATION'&&d.descriptor_valid===true&&d.descriptor_predicate===rv.predicate&&d.governance_route==='SDK_MANIFEST_INTR'&&d.interlock_required===true&&d.intr_required===true&&d.manifest_required===true&&d.manifest_admitted===false&&d.submitted===false&&d.disposition==='FAIL_CLOSED'&&d.failing_predicate==='WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND'&&d.authority_effect==='NONE_REQUEST_ONLY'&&d.tutorial_required===false&&d.guidance_required===false,'draft invariants: '+JSON.stringify(d));
const ex=E.build({disposition:d.disposition,predicate:d.failing_predicate,requested_action:d.action,authority_source:'MANIFEST',remediation_draft:d},SURFACE);
check(ex.remediation_draft&&ex.remediation_draft.submitted===false&&ex.remediation_draft.non_authorizing===true&&E.conforms(ex).ok===true,'draft explains as an unsubmitted, non-authorizing remediation draft');
const bd=C.buildIntegrationDraft({framework_id:'Bad Id',adapter_version:'1'},C.validateDescriptor({framework_id:'Bad Id'},G.validate),'NOPE');
check(bd.framework_id==='FRAMEWORK_ID_NOT_VALID'&&bd.adapter_version==='ADAPTER_VERSION_NOT_VALID'&&bd.mode==='DIRECT_INTEGRATION'&&bd.descriptor_valid===false&&bd.descriptor_predicate==='ADAPTER_SCHEMA_NOT_SUPPORTED'&&bd.disposition==='FAIL_CLOSED'&&bd.submitted===false&&bd.manifest_admitted===false,'invalid descriptor draft fails closed with the validator predicate');
check(C.buildIntegrationDraft(null,null,null).descriptor_predicate==='INTEGRATION_VALIDATION_ABSENT'&&C.buildIntegrationDraft(null,null,null).descriptor_valid===false&&C.buildIntegrationDraft(null,null,null).submitted===false,'draft without validation fails closed');
check(C.buildIntegrationDraft(R,{descriptor_valid:true,predicate:'X',disposition:'ALLOW'},'GUIDED_INTEGRATION').disposition==='FAIL_CLOSED','a validation claiming ALLOW cannot lift the draft out of FAIL_CLOSED');

// 8. GUIDANCE-NEVER-GATES regression: identical outputs across modes (draft `mode` aside), no state change on
// selection, no output requires guidance, and a tutorial-gated descriptor is refused in every mode.
const strip=x=>{const c=Object.assign({},x);delete c.mode;return c;};
const perMode=MODES.map(m=>({mode:m,v:C.validateDescriptor(R,G.validate),r:C.runConformance(R,G.validate),d:C.buildIntegrationDraft(R,C.validateDescriptor(R,G.validate),m),s:C.selectMode(m)}));
for(const b of perMode){
  check(eq(b.v,perMode[0].v)&&eq(b.r,perMode[0].r)&&eq(strip(b.d),strip(perMode[0].d))&&b.d.mode===b.mode,'GUIDANCE-NEVER-GATES: validate/conformance/draft identical across modes except the draft mode field: '+b.mode);
  check(b.s.state_changed===false&&b.s.guidance_required===false&&b.s.tutorial_required===false&&b.s.authority_effect==='NONE','GUIDANCE-NEVER-GATES: selecting a mode changes no state: '+b.mode);
  check(b.v.guidance_required===false&&b.r.descriptor_validation.guidance_required===false&&b.d.guidance_required===false&&b.d.tutorial_required===false&&b.v.certified===false&&b.r.certified===false,'GUIDANCE-NEVER-GATES: no output requires guidance or certifies: '+b.mode);
  const t=C.validateDescriptor(Object.assign({},R,{tutorial_required:true,mode:b.mode}),G.validate);
  check(t.descriptor_valid===false&&t.predicate==='TUTORIAL_MUST_NOT_GATE_INTEGRATION'&&t.disposition==='FAIL_CLOSED'&&C.runConformance(Object.assign({},R,{tutorial_required:true,mode:b.mode}),G.validate).descriptor_validation.predicate==='TUTORIAL_MUST_NOT_GATE_INTEGRATION','GUIDANCE-NEVER-GATES: tutorial_required:true refused in every mode: '+b.mode);
  const tagged=C.validateDescriptor(Object.assign({},R,{mode:b.mode}),G.validate);
  check(tagged.descriptor_valid===true&&tagged.mode===b.mode&&eq(strip(tagged),strip(perMode[0].v)),'a mode tag on the descriptor changes nothing but the echoed mode: '+b.mode);
}
const perModeText=JSON.stringify(perMode);
check(!perModeText.includes('"certified":true')&&!perModeText.includes('"submitted":true')&&!perModeText.includes('"guidance_required":true')&&!perModeText.includes('"tutorial_required":true')&&!perModeText.includes('"state_changed":true'),'no mode output certifies, submits, requires guidance or changes state');

// 9. Page source and layout.
check(page.includes('<script src="assets/workspace-governance-integration.js"></script>')&&page.includes('<script src="assets/workspace-integration-conformance.js"></script>')&&page.indexOf('assets/workspace-explanation.js')<page.indexOf('assets/workspace-governance-integration.js')&&page.indexOf('assets/workspace-governance-integration.js')<page.indexOf('assets/workspace-integration-conformance.js')&&page.indexOf('assets/workspace-integration-conformance.js')<page.indexOf('<script src="assets/workspace.js"></script>'),'script tags present and ordered before workspace.js');
check(ui.includes('integrationMode:"DIRECT_INTEGRATION"')&&/function setMode\(mode\)\{[^\n]*state\.integrationMode="DIRECT_INTEGRATION";state\.integrationDescriptorText=null;state\.integrationResult=null;/.test(ui)&&!/localStorage|sessionStorage|indexedDB/.test(ui),'integration mode is in-memory, defaults to DIRECT and is reset by setMode()');
check(ui.includes('INTEGRATION_CONTRACT_UNAVAILABLE')&&ui.includes('INVALID_ADAPTER_DESCRIPTOR_JSON')&&ui.includes('data-explain-integration')&&ui.includes('data-integration-mode')&&ui.includes('data-integration-action')&&ui.includes('im.dataset.integrationMode!==undefined')&&ui.includes('ia.dataset.integrationAction!==undefined')&&ui.includes('ix.dataset.explainIntegration!==undefined'),'page names the integration predicates and guards its click handlers');
check(/function renderDeveloper\(\)\{[^\n]*html\+=renderIntegration\(\);box\.innerHTML=html;\}/.test(ui)&&/if\(state\.mode!=="developer"\)return;const k=integrationContracts\(\);/.test(ui),'integration block renders inside the Developer card only; actions are developer-context only');
check(/\.mode-select button\[aria-pressed="true"\]\{/.test(css)&&/\.integration-descriptor\{[^}]*width:100%[^}]*\}/.test(css)&&/\.card button,\.assistant button\{min-height:44px\}/.test(css)&&/\.mode-select\{[^}]*flex-wrap:wrap[^}]*\}/.test(css),'mode selector, textarea and 44px phone rule');
check(workflow.includes("'assets/workspace-integration-conformance.js'")&&workflow.includes("'tests/workspace-integration-conformance.test.cjs'")&&workflow.includes('node --check assets/workspace-integration-conformance.js')&&workflow.includes('node tests/workspace-integration-conformance.test.cjs'),'workflow covers the asset and the test');

// 10. UI harness: Developer card integration block, mode switching, validate / conformance / draft, Why?, resets.
const elIds=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities','searchResults','tasks','deviceContinuity','developer','explanation','integrationDescriptor'];
const unesc=s=>s.replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
const preOf=html=>{const m=html.match(/<pre class="draft" id="explanationJson">([\s\S]*?)<\/pre>/);return m?unesc(m[1]):'';};
const jsonOf=html=>{const text=preOf(html);return text?JSON.parse(text):null;};
function harness(opts){const els={};elIds.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
  els.explanationJson={id:'explanationJson',get textContent(){return preOf(els.explanation.innerHTML);}};
  const docListeners={};const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener:(t,f)=>{docListeners[t]=f}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{StegVerseWorkspaceKVBridge:{loadPersonalWorkspace:()=>Promise.reject(new Error('FAIL_CLOSED: DEVICE_KV sovereign InTr ingress unavailable for WORKSPACE_PERSONAL_PROJECTION')),lastNodeBinding:()=>null}}};
  vm.createContext(ctx);for(const s of [caps,auth,binding,continuity,nodeBinding,device,explanation])vm.runInContext(s,ctx);
  if(opts.integration!==false){vm.runInContext(contract,ctx);vm.runInContext(src,ctx);}
  ['StegVerseWorkspaceCapabilities','StegVerseWorkspaceSessionAuthentication','StegVerseWorkspaceAssistantBinding','StegVerseWorkspaceAssistantContinuity','StegVerseWorkspaceNodeBinding','StegVerseWorkspaceDeviceContinuity','StegVerseWorkspaceExplanation','StegVerseGovernanceIntegration','StegVerseWorkspaceIntegrationConformance'].forEach(k=>{if(ctx[k])ctx.window[k]=ctx[k];});
  vm.runInContext(ui,ctx);
  const click=target=>docListeners.click({target:{closest:sel=>target[sel]||null}});
  return {els,click,switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}}),ctx,
    mode:m=>click({'[data-integration-mode]':{dataset:{integrationMode:m}}}),action:a=>click({'[data-integration-action]':{dataset:{integrationAction:a}}}),why:id=>click({'[data-explain-integration]':{dataset:{explainIntegration:id}}}),
    setText:t=>{els.integrationDescriptor.value=t;}};}
const resultOf=html=>html.slice(html.indexOf('<div class="evidence" id="integrationResult">'),html.indexOf('<div class="muted">Mode '));
const pressed=(html,m)=>html.includes('data-integration-mode="'+m+'" aria-pressed="true"');
(async()=>{
  const wait=()=>new Promise(r=>setTimeout(r,10));
  let h=harness({});await wait();
  // Personal context: no integration block; integration clicks are ignored.
  check(h.els.developer.innerHTML.includes('Developer context not active')&&!h.els.developer.innerHTML.includes('integration-title'),'no integration block outside the developer context');
  const personalExplanation=h.els.explanation.innerHTML;h.action('validate');h.mode('GUIDED_INTEGRATION');h.action('draft');
  check(h.els.explanation.innerHTML===personalExplanation&&h.els.intentDraft.innerHTML===''&&h.els.developer.innerHTML.includes('Developer context not active'),'integration actions and mode clicks do nothing outside the developer context');
  h.switchTo('developer');let dev=h.els.developer.innerHTML;
  check(dev.includes('<h3 class="integration-title">Integration</h3>')&&dev.includes('<div class="mode-select" role="group" aria-label="Integration mode">')&&dev.includes('<button type="button" data-integration-mode="DIRECT_INTEGRATION" aria-pressed="true">')&&dev.includes('data-integration-mode="GUIDED_INTEGRATION" aria-pressed="false"')&&dev.includes('data-integration-mode="ASSISTANCE_ON_DEMAND" aria-pressed="false"')&&(dev.match(/data-integration-mode="/g)||[]).length===3,'mode selector with three entry points and DIRECT default');
  check(dev.includes('Guidance is optional and never a gate')&&!dev.includes('integration-hints'),'guidance statement present; DIRECT shows no hints');
  check(dev.includes('<textarea id="integrationDescriptor" class="integration-descriptor" spellcheck="false">')&&dev.includes('reference adapter (GitHub); replace with your own')&&dev.includes('&quot;framework_id&quot;: &quot;github&quot;')&&dev.includes('&quot;role&quot;: &quot;REFERENCE_ADAPTER&quot;'),'textarea prefilled with the labelled GitHub reference descriptor');
  for(const a of [['validate','Validate adapter descriptor'],['reference','Load GitHub reference adapter'],['conformance','Run synthetic conformance fixtures'],['draft','Draft submission request']])check(dev.includes('<button type="button" data-integration-action="'+a[0]+'">'+a[1]+'</button>'),'action button '+a[0]);
  check(dev.includes('No descriptor validated yet')&&!/<span class="pill ok">/.test(dev)&&!/data-action=|data-task-action=/.test(dev),'nothing validated yet, no ok pill, no contact/task action controls');
  // Mode switching changes nothing but the selector and hints: every other card, the runtime state, the developer
  // area rows (statuses), the KV gate (kvIngress) and the intent draft are byte-identical before and after.
  const snap=()=>JSON.stringify(elIds.filter(k=>k!=='developer').map(k=>[k,h.els[k].innerHTML,h.els[k].textContent]))+'|'+h.els.developer.innerHTML.split('<h3 class="integration-title">')[0]+'|'+h.ctx.document.body.dataset.workspaceMode;
  const before=snap();
  h.mode('GUIDED_INTEGRATION');dev=h.els.developer.innerHTML;
  check(pressed(dev,'GUIDED_INTEGRATION')&&dev.includes('data-integration-mode="DIRECT_INTEGRATION" aria-pressed="false"')&&dev.includes('<ol class="muted integration-hints">')&&dev.includes('These steps are optional; skipping them changes nothing.'),'GUIDED shows optional step hints');
  check(snap()===before,'mode switch to GUIDED changes no statuses, KV ingress, intent draft or explanation');
  h.mode('ASSISTANCE_ON_DEMAND');dev=h.els.developer.innerHTML;
  check(pressed(dev,'ASSISTANCE_ON_DEMAND')&&dev.includes('<div class="muted integration-hints">Why?')&&!dev.includes('<ol'),'ASSISTANCE shows a Why?-style hint line only');
  check(snap()===before,'mode switch to ASSISTANCE changes no statuses, KV ingress, intent draft or explanation');
  h.mode('FORCED_TUTORIAL');check(h.els.developer.innerHTML===dev,'an invalid mode is refused and changes nothing');
  h.mode('DIRECT_INTEGRATION');check(pressed(h.els.developer.innerHTML,'DIRECT_INTEGRATION')&&!h.els.developer.innerHTML.includes('integration-hints')&&snap()===before,'back to DIRECT with no hints and nothing else changed');
  // Validate in DIRECT with no mode selection at all (fresh developer context): no tutorial step is required.
  h=harness({});await wait();h.switchTo('developer');h.setText(JSON.stringify(C.REFERENCE_ADAPTER,null,2));
  h.action('validate');dev=h.els.developer.innerHTML;let html=h.els.explanation.innerHTML;let j=jsonOf(html);
  check(dev.includes('<strong>Descriptor validation · github</strong> <span class="pill warn">FAIL_CLOSED</span> AUTHENTIC_MANIFEST_BOUND_GOVERNANCE_TRANSITION_NOT_OBSERVED <button type="button" class="why" data-explain-integration="validation" aria-label="Why?">Why?</button>')&&dev.includes('descriptor_valid: true')&&dev.includes('mode_independent: true')&&dev.includes('guidance_required: false')&&dev.includes('certified: false')&&dev.includes('submitted: false')&&dev.includes('execution_observed: false')&&pressed(dev,'DIRECT_INTEGRATION'),'validate in DIRECT without selecting a mode renders the contract result rows: '+resultOf(dev).slice(0,400));
  check(html.startsWith('<div class="muted explanation-selected">Explaining on request: integration outcome <strong>github</strong>. <button type="button" data-explain-clear>Back to latest outcome</button></div><div class="explanation-prose">')&&j&&j.outcome.disposition==='FAIL_CLOSED'&&j.outcome.outcome_class==='FAILED_CLOSED'&&j.outcome.predicate==='AUTHENTIC_MANIFEST_BOUND_GOVERNANCE_TRANSITION_NOT_OBSERVED'&&j.authorization.authorized===false&&j.authorization.requested_action==='Validate the github adapter descriptor against the governance integration contract'&&j.authorization.authority_source==='MANIFEST'&&j.execution.executed===false&&j.execution.consequence_observation==='NOT_AUTHENTICALLY_OBSERVED'&&j.evidence.length===1&&j.evidence[0].kind==='SOURCE_REF'&&j.evidence[0].ref==='StegVerse-Labs/Site:assets/workspace-governance-integration.js'&&E.conforms(j).ok===true,'validation is explained through the merged explanation card: '+html.slice(0,300));
  check(html.includes('GitHub is only the reference adapter')&&html.includes('same contract applies in every integration mode'),'explanation prose states the reference role and mode independence');
  // Byte-identical validation across modes: same result rows, same explanation artifact.
  const directRows=resultOf(dev),directArtifact=JSON.stringify(j);
  for(const m of ['GUIDED_INTEGRATION','ASSISTANCE_ON_DEMAND']){h.mode(m);h.action('validate');const d2=h.els.developer.innerHTML;check(pressed(d2,m)&&resultOf(d2)===directRows&&JSON.stringify(jsonOf(h.els.explanation.innerHTML))===directArtifact,'validate output byte-identical in '+m);}
  h.mode('DIRECT_INTEGRATION');
  // Invalid JSON renders a FAIL_CLOSED result instead of throwing.
  h.setText('{not json');h.action('validate');dev=h.els.developer.innerHTML;html=h.els.explanation.innerHTML;j=jsonOf(html);
  check(dev.includes('<strong>Descriptor validation</strong> <span class="pill warn">FAIL_CLOSED</span> INVALID_ADAPTER_DESCRIPTOR_JSON')&&dev.includes('descriptor_valid: false')&&dev.includes('mode_independent: true')&&html.includes('integration outcome <strong>descriptor</strong>')&&j&&j.outcome.predicate==='INVALID_ADAPTER_DESCRIPTOR_JSON'&&j.outcome.disposition==='FAIL_CLOSED'&&j.authorization.requested_action==='Validate the supplied adapter descriptor against the governance integration contract'&&E.conforms(j).ok===true,'invalid JSON renders INVALID_ADAPTER_DESCRIPTOR_JSON without throwing: '+resultOf(dev).slice(0,300));
  // A tutorial-gated descriptor is refused in the page too; a framework id that fails the contract pattern is not echoed.
  h.setText(JSON.stringify(Object.assign({},C.REFERENCE_ADAPTER,{tutorial_required:true,framework_id:'Bearer x'})));h.action('validate');dev=h.els.developer.innerHTML;j=jsonOf(h.els.explanation.innerHTML);
  check(dev.includes('<strong>Descriptor validation</strong> <span class="pill warn">FAIL_CLOSED</span> FRAMEWORK_ID_INVALID')&&j.outcome.predicate==='FRAMEWORK_ID_INVALID'&&j.authorization.requested_action==='Validate the supplied adapter descriptor against the governance integration contract','non-conforming framework id is refused and never echoed');
  h.setText(JSON.stringify(Object.assign({},C.REFERENCE_ADAPTER,{tutorial_required:true})));h.action('validate');dev=h.els.developer.innerHTML;j=jsonOf(h.els.explanation.innerHTML);
  check(dev.includes('TUTORIAL_MUST_NOT_GATE_INTEGRATION')&&dev.includes('descriptor_valid: false')&&j.outcome.predicate==='TUTORIAL_MUST_NOT_GATE_INTEGRATION','a tutorial-gated descriptor is refused in the page');
  // The validation row's own Why? re-selects the validation record.
  h.click({'[data-explain-clear]':{dataset:{explainClear:''}}});check(!h.els.explanation.innerHTML.includes('Explaining on request'),'clear restores the latest outcome');
  h.why('validation');check(jsonOf(h.els.explanation.innerHTML).outcome.predicate==='TUTORIAL_MUST_NOT_GATE_INTEGRATION','Why? on the validation row explains the last validation');
  // Reference action reloads the GitHub reference descriptor and clears the result.
  h.action('reference');dev=h.els.developer.innerHTML;
  check(dev.includes('&quot;framework_id&quot;: &quot;github&quot;')&&dev.includes('No descriptor validated yet')&&!dev.includes('TUTORIAL_MUST_NOT_GATE_INTEGRATION'),'reference action reloads the GitHub reference adapter');
  // Conformance: eight synthetic fixture rows, each with a Why? button; the run is FAIL_CLOSED and uncertified.
  h.setText(JSON.stringify(C.REFERENCE_ADAPTER));h.action('conformance');dev=h.els.developer.innerHTML;
  check(dev.includes('<strong>Synthetic conformance run</strong> <span class="pill warn">FAIL_CLOSED</span> SYNTHETIC_CONFORMANCE_ONLY')&&dev.includes('descriptor_valid: true (AUTHENTIC_MANIFEST_BOUND_GOVERNANCE_TRANSITION_NOT_OBSERVED)')&&dev.includes('evidence class SYNTHETIC_TEST')&&dev.includes('certified: false')&&dev.includes('submitted: false')&&dev.includes('authenticated transition observed: false'),'conformance header: '+resultOf(dev).slice(0,400));
  for(const id of IDS)check(new RegExp('<div class="evidence-row"><strong>'+id+'</strong> <span class="pill warn">(ALLOW|DENY|FAIL_CLOSED|UNKNOWN)</span> [A-Z_]+ <span class="badge synthetic">SYNTHETIC_TEST</span> <button type="button" class="why" data-explain-integration="'+id+'" aria-label="Why\\?">Why\\?</button><div class="muted">[^<]*synthetic fixture, not an authenticated transition</div></div>').test(dev),'fixture row '+id);
  check((dev.match(/data-explain-integration="CONF-/g)||[]).length===8&&!/<span class="pill ok">/.test(dev)&&!/data-action=|data-task-action=|data-developer-action="DEVELOPER_INTEGRATION/.test(resultOf(dev)),'eight fixture rows, no ok pill, no action controls among them');
  const conformanceRows=resultOf(dev);
  for(const m of ['GUIDED_INTEGRATION','ASSISTANCE_ON_DEMAND']){h.mode(m);h.action('conformance');check(resultOf(h.els.developer.innerHTML)===conformanceRows,'conformance output byte-identical in '+m);}
  h.mode('DIRECT_INTEGRATION');
  // Why? on a fixture explains that fixture through the card.
  h.why('CONF-REVOKED-CONSENT');html=h.els.explanation.innerHTML;j=jsonOf(html);
  check(html.startsWith('<div class="muted explanation-selected">Explaining on request: integration outcome <strong>CONF-REVOKED-CONSENT</strong>. <button type="button" data-explain-clear>Back to latest outcome</button></div>')&&html.includes('INTEGRATION_CONSENT_REVOKED')&&j&&j.outcome.predicate==='INTEGRATION_CONSENT_REVOKED'&&j.outcome.outcome_class==='DENIED'&&j.authorization.authority_source==='TV_TVC'&&j.remediation_draft&&j.remediation_draft.submitted===false&&E.conforms(j).ok===true,'Why? on a fixture names that fixture and its predicate: '+html.slice(0,300));
  h.why('CONF-ALLOW');j=jsonOf(h.els.explanation.innerHTML);
  check(j&&j.outcome.disposition==='UNKNOWN'&&j.outcome.outcome_class==='UNOBSERVED'&&j.execution.executed===false&&j.execution.execution_state==='NOT_EXECUTED'&&j.execution.consequence_observation==='UNKNOWN'&&j.evidence.every(e=>e.kind==='SOURCE_REF'),'the synthetic admitted-manifest fixture explains as UNKNOWN to this surface, never ALLOW');
  h.why('CONF-UNOBSERVED-RUNTIME');j=jsonOf(h.els.explanation.innerHTML);check(j&&j.outcome.disposition==='UNKNOWN'&&j.outcome.outcome_class==='UNOBSERVED','the unobserved-runtime fixture explains as UNOBSERVED');
  const unchanged=h.els.explanation.innerHTML;h.why('CONF-NOPE');check(h.els.explanation.innerHTML===unchanged,'unknown fixture id changes nothing');
  // Conformance with an unparseable descriptor: fixtures are still listed, the descriptor validation is false.
  h.setText('nope');h.action('conformance');dev=h.els.developer.innerHTML;
  check(dev.includes('descriptor_valid: false (INVALID_ADAPTER_DESCRIPTOR_JSON)')&&(dev.match(/data-explain-integration="CONF-/g)||[]).length===8&&dev.includes('SYNTHETIC_CONFORMANCE_ONLY'),'invalid descriptor: fixtures still listed, descriptor_valid false');
  // Draft: unsubmitted manifest request carrying the mode for the record only; explained through the card.
  h.setText(JSON.stringify(C.REFERENCE_ADAPTER));h.mode('GUIDED_INTEGRATION');h.action('draft');let draft=h.els.intentDraft.innerHTML;
  check(draft.includes('DEVELOPER_INTEGRATION_SUBMISSION_REQUEST request draft')&&draft.includes('FAIL_CLOSED')&&draft.includes('WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND')&&draft.includes('&quot;mode&quot;: &quot;GUIDED_INTEGRATION&quot;')&&draft.includes('&quot;framework_id&quot;: &quot;github&quot;')&&draft.includes('&quot;descriptor_valid&quot;: true')&&draft.includes('&quot;submitted&quot;: false')&&draft.includes('&quot;manifest_admitted&quot;: false')&&draft.includes('&quot;tutorial_required&quot;: false')&&draft.includes('&quot;guidance_required&quot;: false')&&draft.includes('NONE_REQUEST_ONLY')&&draft.includes('Not submitted; no message, profile access or other effect occurred.'),'draft rendered: '+draft.slice(0,500));
  check(!/started|succeeded|completed|certified&quot;: true|ALLOW&quot;/i.test(draft),'draft must not claim execution or certification');
  j=jsonOf(h.els.explanation.innerHTML);
  check(!h.els.explanation.innerHTML.includes('Explaining on request')&&j&&j.outcome.predicate==='WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND'&&j.remediation_draft&&j.remediation_draft.submitted===false&&j.remediation_draft.draft.action==='DEVELOPER_INTEGRATION_SUBMISSION_REQUEST'&&j.remediation_draft.draft.mode==='GUIDED_INTEGRATION'&&E.conforms(j).ok===true,'draft explained as an unsubmitted remediation draft');
  const guidedDraft=unesc(draft).replace(/"mode": "GUIDED_INTEGRATION"/,'"mode": "X"');
  for(const m of ['DIRECT_INTEGRATION','ASSISTANCE_ON_DEMAND']){h.mode(m);h.action('draft');const d3=unesc(h.els.intentDraft.innerHTML);check(d3.includes('"mode": "'+m+'"')&&d3.replace(/"mode": "[A-Z_]+"/,'"mode": "X"')===guidedDraft,'draft identical across modes except the mode field: '+m);}
  // Context switch resets the integration mode, result and descriptor text; nothing was persisted.
  h.switchTo('personal');check(h.els.developer.innerHTML.includes('Developer context not active')&&h.els.intentDraft.innerHTML===''&&!h.els.explanation.innerHTML.includes('Explaining on request'),'personal context clears the developer draft and selection');
  h.setText('');h.switchTo('developer');dev=h.els.developer.innerHTML;
  check(pressed(dev,'DIRECT_INTEGRATION')&&!dev.includes('integration-hints')&&dev.includes('No descriptor validated yet')&&dev.includes('&quot;framework_id&quot;: &quot;github&quot;'),'setMode() resets integrationMode to DIRECT, clears the result and restores the reference descriptor');
  // Absent contract: the block names the predicate and validates nothing; actions do nothing.
  h=harness({integration:false});await wait();h.switchTo('developer');dev=h.els.developer.innerHTML;
  check(dev.includes('<h3 class="integration-title">Integration</h3><div class="empty">Integration contract unavailable (INTEGRATION_CONTRACT_UNAVAILABLE); nothing is validated.</div>')&&!dev.includes('data-integration-action')&&!dev.includes('data-integration-mode')&&dev.includes('data-developer-action="DEVELOPER_BUILD_REQUEST"'),'absent contract: predicate shown, no integration controls, developer areas intact');
  const absentExplanation=h.els.explanation.innerHTML;h.action('validate');h.action('conformance');h.action('draft');h.mode('GUIDED_INTEGRATION');h.why('CONF-ALLOW');
  check(h.els.explanation.innerHTML===absentExplanation&&h.els.intentDraft.innerHTML===''&&h.els.developer.innerHTML===dev,'integration actions do nothing without the contract');
  console.log('WORKSPACE_INTEGRATION_CONFORMANCE_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
