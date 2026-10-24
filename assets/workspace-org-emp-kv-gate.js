(function(root){
"use strict";
// Org-Emp-KV gate rule, consumed by reference from the proposed contract stegverse.org-emp-kv-projection/v1
// (StegVerse-org/.github orchestration/schemas/org-emp-kv-projection.v1.schema.json, x-stegverse-gate-rule).
// The gate opens only for a conforming projection whose five predicates are all OBSERVED_TRUE with a receipt,
// delivered under Interlock/InTr admission. Anything else fails closed with six fields. Browser storage, page
// sessions and clicks are never inputs; this module reads only the projection object it is handed.
var SCHEMA="stegverse.org-emp-kv-projection/v1";
var SCHEMA_REF="StegVerse-org/.github:orchestration/schemas/org-emp-kv-projection.v1.schema.json";
var KEYS=["employee_identity_matches","machine_identity_matches","active_membership","role_capability_admitted","transition_admitted"];
var STATES=["OBSERVED_TRUE","OBSERVED_FALSE","NOT_OBSERVED"];
var REF=/^[A-Za-z0-9_./:#-]{1,240}$/,ID=/^[A-Za-z0-9_.:-]{1,160}$/,ORG=/^[A-Za-z0-9_.-]{1,100}$/,SHA=/^[0-9a-f]{64}$/,TS=/^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$/;
var TOP=["schema","projection_id","organization","principal_ref","ledger","predicates","admission","issued_at","authority_effect"];
function isObj(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function exactKeys(o,keys){var k=Object.keys(o);return k.length===keys.length&&keys.every(function(x){return Object.prototype.hasOwnProperty.call(o,x);});}
function str(v,re){return typeof v==="string"&&re.test(v);}
function predicateOk(p){return isObj(p)&&exactKeys(p,["state","receipt_ref"])&&STATES.indexOf(p.state)>=0&&(p.receipt_ref===null||str(p.receipt_ref,REF));}
// Mirrors the schema's constraints; returns the first violated path, or null when the projection conforms.
function violation(p){
 if(!isObj(p))return "$";
 if(!exactKeys(p,TOP))return "$.keys";
 if(p.schema!==SCHEMA)return "$.schema";
 if(!str(p.projection_id,ID))return "$.projection_id";
 if(!str(p.organization,ORG))return "$.organization";
 if(!str(p.principal_ref,ID))return "$.principal_ref";
 if(!isObj(p.ledger)||!exactKeys(p.ledger,["root","head_sha256"])||p.ledger.root!=="ORGANIZATION_LEDGER_ROOT"||!str(p.ledger.head_sha256,SHA))return "$.ledger";
 if(!isObj(p.predicates)||!exactKeys(p.predicates,KEYS))return "$.predicates";
 for(var i=0;i<KEYS.length;i++)if(!predicateOk(p.predicates[KEYS[i]]))return "$.predicates."+KEYS[i];
 var a=p.admission;
 if(!isObj(a)||!exactKeys(a,["transition_authority","credential_authority","receipt_ref"])||a.transition_authority!=="Interlock/InTr"||a.credential_authority!=="TV/TVC"||!str(a.receipt_ref,REF))return "$.admission";
 if(!str(p.issued_at,TS))return "$.issued_at";
 if(p.authority_effect!=="NONE")return "$.authority_effect";
 return null;
}
function evaluate(projection){
 var v=projection==null?"projection_absent":violation(projection);
 var states={};KEYS.forEach(function(k){states[k]=v===null?projection.predicates[k].state:"NOT_OBSERVED";});
 var open=v===null&&KEYS.every(function(k){var q=projection.predicates[k];return q.state==="OBSERVED_TRUE"&&q.receipt_ref!==null;});
 var out={schema_ref:SCHEMA_REF,gate_open:open,predicates:states,authority_effect:"NONE"};
 if(!open)out.actionable_disposition={failure_code:"ORG_KV_PROJECTION_NOT_OBSERVED",failed_predicate:"ADMITTED_ORG_LEDGER_PROJECTION_SCHEMA_DECLARED",
  required_evidence_or_repair:v===null?"the organizational runtime records every Org-Emp-KV predicate as OBSERVED_TRUE with its receipt and delivers the projection through Interlock/InTr":"the organizational runtime delivers a conforming "+SCHEMA+" projection through Interlock/InTr ("+v+")",
  retry_entrypoint:"Site assets/workspace.js renderKvGate",owning_existing_goal:"STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001",
  next_attempt:"the next load of this context evaluates the delivered projection again; nothing waits"};
 return out;
}
root.StegVerseWorkspaceOrgEmpKVGate=Object.freeze({schema:SCHEMA,schema_ref:SCHEMA_REF,keys:KEYS.slice(),authority_effect:"NONE",violation:violation,evaluate:evaluate});
}(typeof window!=="undefined"?window:globalThis));
