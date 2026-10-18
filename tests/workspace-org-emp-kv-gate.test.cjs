// Org-Emp-KV gate (WU-D8 / OQ-C17): the Org context opens only from a conforming stegverse.org-emp-kv-projection/v1
// projection with five receipt-backed OBSERVED_TRUE predicates under Interlock/InTr admission; storage never opens it.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
function assert(ok,msg){if(!ok)throw new Error(msg)}
const src=read('assets/workspace-org-emp-kv-gate.js'),ui=read('assets/workspace.js'),page=read('workspace.html'),workflow=read('.github/workflows/workspace-kv-binding-validation.yml');
const sb={};vm.createContext(sb);vm.runInContext(src,sb);const G=sb.StegVerseWorkspaceOrgEmpKVGate;
const KEYS=['employee_identity_matches','machine_identity_matches','active_membership','role_capability_admitted','transition_admitted'];
const SIX=['failure_code','failed_predicate','required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'];
assert(G&&Object.isFrozen(G)&&G.schema==='stegverse.org-emp-kv-projection/v1'&&G.authority_effect==='NONE'&&JSON.stringify(G.keys)===JSON.stringify(KEYS),'module identity');
assert(G.schema_ref==='StegVerse-org/.github:orchestration/schemas/org-emp-kv-projection.v1.schema.json','consumes the contract by reference');
// The page's own gate keys are exactly the contract's.
const m=/const ORG_GATE_KEYS=(\[[^\]]+\])/.exec(ui);assert(m&&JSON.stringify(JSON.parse(m[1]))===JSON.stringify(KEYS),'ORG_GATE_KEYS match the contract');
const proj=(state='OBSERVED_TRUE')=>({schema:'stegverse.org-emp-kv-projection/v1',projection_id:'org-emp-kv:example:0001',organization:'StegVerse-org',principal_ref:'principal:example',ledger:{root:'ORGANIZATION_LEDGER_ROOT',head_sha256:'a'.repeat(64)},predicates:Object.fromEntries(KEYS.map(k=>[k,{state,receipt_ref:state==='NOT_OBSERVED'?null:'receipt:'+k}])),admission:{transition_authority:'Interlock/InTr',credential_authority:'TV/TVC',receipt_ref:'receipt:intr-admission'},issued_at:'2026-10-18T23:00:00Z',authority_effect:'NONE'});
const closed=(g,why)=>{assert(g.gate_open===false&&g.authority_effect==='NONE'&&g.actionable_disposition,why+': closed');SIX.forEach(k=>assert(typeof g.actionable_disposition[k]==='string'&&g.actionable_disposition[k].length>0,why+': '+k));assert(g.actionable_disposition.failure_code==='ORG_KV_PROJECTION_NOT_OBSERVED'&&g.actionable_disposition.failed_predicate==='ADMITTED_ORG_LEDGER_PROJECTION_SCHEMA_DECLARED',why+': codes');};
// Opens only from a conforming, fully observed, receipt-backed projection.
let g=G.evaluate(proj());assert(g.gate_open===true&&!g.actionable_disposition&&KEYS.every(k=>g.predicates[k]==='OBSERVED_TRUE'),'opens on admitted projection');
// Absent, NOT_OBSERVED, OBSERVED_FALSE, one false, true-without-receipt: closed with six fields.
closed(G.evaluate(null),'absent');closed(G.evaluate(undefined),'undefined');
closed(G.evaluate(proj('NOT_OBSERVED')),'not observed');closed(G.evaluate(proj('OBSERVED_FALSE')),'observed false');
let p=proj();p.predicates.active_membership.state='OBSERVED_FALSE';g=G.evaluate(p);closed(g,'one false');assert(g.predicates.active_membership==='OBSERVED_FALSE'&&g.predicates.transition_admitted==='OBSERVED_TRUE','states reported from a conforming projection');
p=proj();p.predicates.transition_admitted.receipt_ref=null;closed(G.evaluate(p),'true without receipt');
// Storage alone never opens: a storage-shaped flag object, a cached boolean, a string.
closed(G.evaluate({employee_identity_matches:true,machine_identity_matches:true,active_membership:true,role_capability_admitted:true,transition_admitted:true}),'storage flags');
closed(G.evaluate(true),'boolean');closed(G.evaluate('{"gate":"open"}'),'string');
// Every non-conforming mutation fails closed and reports NOT_OBSERVED for all keys.
const muts={'missing predicate':v=>delete v.predicates.machine_identity_matches,'extra predicate':v=>v.predicates.extra={state:'OBSERVED_TRUE',receipt_ref:'x'},'authority claimed':v=>v.authority_effect='ALLOW','sessionStorage authority':v=>v.admission.transition_authority='sessionStorage','token credential':v=>v.admission.credential_authority='GITHUB_TOKEN','browser ledger':v=>v.ledger.root='BROWSER_STORAGE','bad head':v=>v.ledger.head_sha256='nope','unknown state':v=>v.predicates.active_membership.state='ASSUMED','extra field':v=>v.cached_from='sessionStorage','wrong schema':v=>v.schema='stegverse.org-emp-kv-projection/v0','no admission':v=>delete v.admission,'bad time':v=>v.issued_at='yesterday'};
for(const [name,mut] of Object.entries(muts)){p=proj();mut(p);g=G.evaluate(p);closed(g,name);assert(KEYS.every(k=>g.predicates[k]==='NOT_OBSERVED'),name+': nothing reported from a non-conforming projection');}
// The module reads no browser storage, performs no I/O and grants nothing.
assert(!/sessionStorage|localStorage|indexedDB|fetch\(|XMLHttpRequest|postMessage/.test(src),'no storage or I/O in the gate module');
// The page wires the module before workspace.js and renderKvGate evaluates only the delivered projection.
assert(page.indexOf('assets/workspace-org-emp-kv-gate.js')>0&&page.indexOf('assets/workspace-org-emp-kv-gate.js')<page.indexOf('<script src="assets/workspace.js"></script>'),'script order');
assert(ui.includes('G.evaluate(state.orgEmpKvProjection||null)')&&ui.includes('orgEmpKvProjection:null'),'renderKvGate consumes the projection slot only');
assert(!/orgEmpKvProjection\s*=\s*(?:window\.)?(?:sessionStorage|localStorage)/.test(ui),'the projection slot is never filled from storage');
assert(workflow.includes("'assets/workspace-org-emp-kv-gate.js'")&&workflow.includes('node tests/workspace-org-emp-kv-gate.test.cjs'),'workflow covers the module and test');
console.log('WORKSPACE_ORG_EMP_KV_GATE_PASS');
