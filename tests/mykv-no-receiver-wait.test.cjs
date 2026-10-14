// ACTIONS BY MANIFEST (.github data/task-registry-global-invariants.json semantics.actions_by_manifest): the MyKV and
// TestFlight DEVICE_KV bridges look a result up exactly once. The device-local consumer persists the result before it
// admits the request (intr-service-worker-base-v1.js admitValidatedTrigger -> persistQueryResult), so a missing result
// is an actionable FAIL_CLOSED disposition (Organization Role item 5), never a delay, retry or poll loop.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
let n=0;const check=(ok,msg)=>{n++;if(!ok)throw new Error(msg);};
const FILES=['assets/my-kv-device-kv-query-bridge.js','assets/kv-testflight-projection-entry.js','assets/my-kv-personal-profile-write-bridge.js','assets/my-kv-personal-form-profile-write-bridge.js'];
const SIX=['failure_code','failed_predicate','required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'];
const worker=fs.readFileSync(path.join(root,'intr-service-worker-base-v1.js'),'utf8');
check(/else if\(req\.kv_request\) action=persistQueryResult\(req,entry\);\s*return action\.then/.test(worker),'the consumer persists the query result before returning the ingress receipt');
for(const f of FILES){
  const src=fs.readFileSync(path.join(root,f),'utf8'),code=src.replace(/\/\/.*$/gm,'');
  check(!/\bdelay\(|\bpoll\(|pollResult|setInterval/.test(code),f+': no delay, poll or interval');
  check(!/device_kv_result_not_ready"\s*&&/.test(code),f+': a not-ready result is never a retry condition');
  const m=code.match(/function resultNotMaterialized\(lookup,detail\)\{[^\n]*\}/);
  check(m,f+': defines the actionable refusal');
  const ctx={};vm.createContext(ctx);vm.runInContext(m[0]+';this.make=resultNotMaterialized;',ctx);
  const e=ctx.make({materialization_id:'mat-1'},'device_kv_result_not_ready');
  check(/^FAIL_CLOSED: DEVICE_KV_RESULT_NOT_YET_MATERIALIZED/.test(e.message)&&e.materialization_id==='mat-1',f+': FAIL_CLOSED naming the queued request');
  const d=e.actionable_disposition;
  check(d&&SIX.every(k=>typeof d[k]==='string'&&d[k].trim()),f+': carries the six actionable fields');
  check(d.failed_predicate==='DEVICE_KV_RESULT_NOT_YET_MATERIALIZED'&&d.owning_existing_goal==='STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001',f+': predicate and owning goal');
  check(fs.existsSync(path.join(root,d.retry_entrypoint)),f+': retry entry point exists: '+d.retry_entrypoint);
  check(!/\bwait (for|on|until)\b/i.test(d.next_attempt+' '+d.required_evidence_or_repair),f+': nothing tells a person to wait');
}
console.log('mykv-no-receiver-wait: '+n+' checks passed');
