// MyKV consumer of the universal explanation contract (.github#3106): a MyKV refusal carrying the six actionable fields
// renders a conforming FAIL_CLOSED explanation with the complete JSON; anything else is withheld, never invented.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
function assert(ok,msg){if(!ok)throw new Error(msg)}
const sb={};vm.createContext(sb);vm.runInContext(read('assets/workspace-explanation.js'),sb);vm.runInContext(read('assets/my-kv-outcome-explanation.js'),sb);
const E=sb.StegVerseWorkspaceExplanation,M=sb.StegVerseMyKVOutcomeExplanation;
assert(M&&Object.isFrozen(M)&&M.authority_effect==='NONE'&&M.surface.surface_id==='my-kv','module identity');
const SIX={failure_code:'DEVICE_KV_RESULT_NOT_YET_MATERIALIZED',failed_predicate:'DEVICE_KV_RESULT_NOT_YET_MATERIALIZED',required_evidence_or_repair:'the device-local DEVICE_KV consumer materializes the result of request m-1 before it admits the request',retry_entrypoint:'my-kv.html',owning_existing_goal:'STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001',next_attempt:'the next action on this page queues a new request and looks its result up once; nothing waits'};
const refusal=()=>{const e=new Error('FAIL_CLOSED: DEVICE_KV_RESULT_NOT_YET_MATERIALIZED: not found');e.actionable_disposition=Object.assign({},SIX);return e;};
const ACTION='Load your Personal Information from your Personal KV';
// A six-field refusal builds a conforming, non-authorizing FAIL_CLOSED artifact.
const r=M.record(refusal(),ACTION);
assert(r&&r.disposition==='FAIL_CLOSED'&&r.predicate==='DEVICE_KV_RESULT_NOT_YET_MATERIALIZED'&&r.authority_source==='INTERLOCK_INTR','record from refusal');
const a=E.build(r,M.surface);
assert(a&&a.predicate===undefined&&E.conforms(a).ok===true,'artifact conforms');
assert(a.outcome.disposition==='FAIL_CLOSED'&&a.authorization.authorized===false&&a.execution.executed===false,'never authorized or executed');
assert(a.outcome.actionable_disposition&&Object.keys(SIX).every(k=>a.outcome.actionable_disposition[k]===SIX[k]),'six fields carried verbatim');
const h=M.html(refusal(),ACTION);
assert(h.includes('explanation-prose')&&h.includes('explanation-json')&&h.includes('stegverse.user-facing-explanation/v1')&&h.includes('authority_effect NONE'),'prose and JSON rendered');
// Withheld, never invented: no six fields, a partial set, a non-error, or a missing contract render nothing.
assert(M.record(new Error('FAIL_CLOSED: X'),ACTION)===null&&M.html(new Error('FAIL_CLOSED: X'),ACTION)==='','no six fields: withheld');
const partial=refusal();delete partial.actionable_disposition.next_attempt;
assert(M.html(partial,ACTION)==='','partial six fields: withheld');
assert(M.html(null,ACTION)===''&&M.html('text',ACTION)==='','non-error: withheld');
const bare={};vm.createContext(bare);vm.runInContext(read('assets/my-kv-outcome-explanation.js'),bare);
assert(bare.StegVerseMyKVOutcomeExplanation.html(refusal(),ACTION)==='','contract absent: withheld');
// render hides the box when nothing conforms and shows it when something does.
const box={innerHTML:'x',hidden:false};
assert(M.render(box,new Error('FAIL_CLOSED: X'),ACTION)===false&&box.hidden===true&&box.innerHTML==='','render hides on withhold');
assert(M.render(box,refusal(),ACTION)===true&&box.hidden===false&&box.innerHTML.length>0,'render shows on conformance');
// Escaping: page-supplied text never becomes markup.
const evil=refusal();evil.actionable_disposition.required_evidence_or_repair='<img src=x onerror=alert(1)>';
assert(!M.html(evil,ACTION).includes('<img'),'escaped');
// The page loads the contract before the consumer and renders only on the profile-load refusal path.
const page=read('my-kv.html');
const iE=page.indexOf('assets/workspace-explanation.js'),iM=page.indexOf('assets/my-kv-outcome-explanation.js');
assert(iE>0&&iM>iE&&page.includes('id="profile-explanation"')&&page.includes('StegVerseMyKVOutcomeExplanation.render(document.getElementById("profile-explanation"),e,'),'page wiring');
console.log('MY_KV_OUTCOME_EXPLANATION_PASS');
