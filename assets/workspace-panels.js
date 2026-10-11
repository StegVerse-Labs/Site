// WorkSpace capability panels (Site#1509 WS-PANELS): stegverse.workspace.capability-panel/v1.
// One reusable renderer for every capability family. A panel is derived from the descriptor's capability status
// (stegverse.workspace.capability-status/v1) plus, when the status permits rows, the source projection for the
// active context. Per-family adapters validate row shape (malformed rows are counted and skipped, never guessed),
// declare fields the producer marks unavailable, and name the producer owner for families without a KV projection
// contract. Panels are informational only: no row, note or state is an availability claim or a permission to act.
(function(root){
"use strict";
if(!root)return;
var SCHEMA="stegverse.workspace.capability-panel/v1";
var ROW_STATES=["OBSERVED","STALE","FRESHNESS_UNKNOWN"];
var PRODUCER_OWNER={
 GITHUB_GOVERNANCE:"StegVerse-Labs/.github#3012 (governance product producer; read-only dependency of this page)",
 ORG_WORKSPACE:"StegOS organizational runtime (Org-KV / Org-Emp-KV projection; not Personal KV)",
 CALENDAR:"no KV projection contract published yet (existing authorized integration owner)",
 EMAIL:"no KV projection contract published yet (existing authorized integration owner)",
 MESSAGING:"no KV projection contract published yet (existing authorized integration owner)",
 DOCUMENTS:"no KV projection contract published yet (existing authorized integration owner)",
 SOCIAL:"no KV projection contract published yet (existing authorized integration owner)"
};
var RENDERED_ELSEWHERE={FEED:"Feed card",CONTACTS:"Friends & Contacts card",ORGANIZATIONS:"Organizations card",MEMBERSHIPS:"Memberships card",AI_ASSISTANT:"MyKV assistant card",TASKS:"Tasks & commitments card",COMMITMENTS:"Tasks & commitments card"};
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function text(v){return v===null||v===undefined?"":String(v);}
function isNum(v){return typeof v==="number"&&isFinite(v);}
function sourceFor(descriptor,projections){
 var schemas=isObject(descriptor)&&Array.isArray(descriptor.allowed_projection_schemas)?descriptor.allowed_projection_schemas:[];
 for(var i=0;i<(projections||[]).length;i++){var p=projections[i];if(isObject(p)&&schemas.indexOf(p.schema)>=0)return p;}
 return null;
}
// Adapters return {rows, notes, malformed_rows, problem}. problem (if set) downgrades the panel to MALFORMED.
var ADAPTERS={
 CRYPTOBOT_PORTFOLIO:function(p){
  var out={rows:[],notes:[],malformed_rows:0,problem:null},pf=p.portfolio;
  if(p.trade_authority_granted!==false)return {rows:[],notes:[],malformed_rows:0,problem:"PROJECTION_TRADE_AUTHORITY_INVALID"};
  if(!isObject(pf))return {rows:[],notes:[],malformed_rows:0,problem:"PORTFOLIO_FIELD_INVALID"};
  var positions=Array.isArray(pf.positions)?pf.positions:[];
  for(var i=0;i<positions.length;i++){var x=positions[i];
   if(!isObject(x)||!(typeof x.asset==="string"&&x.asset)||!isNum(x.quantity)){out.malformed_rows++;continue;}
   out.rows.push({label:x.asset,detail:[x.product_id?"product "+text(x.product_id):null,"qty "+text(x.quantity),isNum(x.value_usd)?"usd "+text(x.value_usd):"value UNAVAILABLE",isNum(x.price_usd)?"price "+text(x.price_usd):null].filter(Boolean).join(" · ")});
  }
  if(isNum(pf.total_value_usd))out.notes.push("total usd "+text(pf.total_value_usd));
  out.notes.push("drawdown "+(isNum(pf.drawdown_percent)?text(pf.drawdown_percent)+"%":"UNAVAILABLE"));
  if(pf.provider)out.notes.push("provider "+text(pf.provider));
  if(pf.source_observed_at)out.notes.push("provider observation "+text(pf.source_observed_at)+" (distinct from projection time)");
  if(isObject(pf.unavailable_fields)){Object.keys(pf.unavailable_fields).sort().forEach(function(k){out.notes.push(k+": "+text(pf.unavailable_fields[k]));});}
  if(isObject(p.source)&&p.source.authority)out.notes.push("source authority "+text(p.source.authority));
  out.notes.push("trade_authority_granted: false · provider_operation_authorized: "+text(p.provider_operation_authorized));
  return out;
 },
 TASKS:function(p){var out={rows:[],notes:[],malformed_rows:0,problem:null};(Array.isArray(p.tasks)?p.tasks:[]).forEach(function(t){if(!isObject(t)||!(typeof t.title==="string"&&t.title)||typeof t.status!=="string"){out.malformed_rows++;return;}out.rows.push({label:t.title,detail:t.status+(t.due_at?" · due "+text(t.due_at):"")});});return out;},
 COMMITMENTS:function(p){var out={rows:[],notes:[],malformed_rows:0,problem:null};(Array.isArray(p.commitments)?p.commitments:[]).forEach(function(c){if(!isObject(c)||!(typeof c.statement==="string"&&c.statement)||typeof c.status!=="string"){out.malformed_rows++;return;}out.rows.push({label:c.statement,detail:c.status+(c.due_at?" · due "+text(c.due_at):"")});});return out;}
};
function countRows(p,field){var v=p?p[field]:undefined;return Array.isArray(v)?v.length:(isObject(v)?1:0);}
function build(input){
 var inp=isObject(input)?input:{},descs=Array.isArray(inp.descriptors)?inp.descriptors:null,statuses=Array.isArray(inp.statuses)?inp.statuses:null,projs=Array.isArray(inp.projections)?inp.projections:[],wt=text(inp.workspace_type)||null;
 if(!descs||!statuses)return {schema:SCHEMA,disposition:"FAIL_CLOSED",predicate:"CAPABILITY_DESCRIPTORS_UNAVAILABLE",workspace_type:wt,panels:[],action_eligible:false,authority_effect:"NONE"};
 var panels=descs.map(function(d,i){
  var s=statuses[i]||{state:"NOT_OBSERVED",predicate:"CAPABILITY_STATUS_ABSENT"};
  var panel={schema:SCHEMA,capability:text(s.capability||(d&&d.capability)),label:text(s.label||(d&&d.label)||(d&&d.capability)),projection_field:s.projection_field||null,state:s.state,predicate:s.predicate,
   provenance:{observed_at:s.observed_at||null,age_seconds:s.age_seconds===undefined?null:s.age_seconds,provenance_ref:s.provenance_ref||null,source_revision:s.source_revision||null,source_cursor:s.source_cursor||null,grant_state:s.grant_state||null,replay_status:s.replay_status||"REPLAY_STATUS_UNKNOWN"},
   context:{workspace_type:wt},rows:[],notes:[],malformed_rows:0,rows_withheld:ROW_STATES.indexOf(s.state)<0,rendered_in:RENDERED_ELSEWHERE[panel_cap(d,s)]||null,producer_owner:PRODUCER_OWNER[panel_cap(d,s)]||null,action_eligible:false,authority_effect:"NONE"};
  if(panel.rows_withheld)return panel;
  var source=sourceFor(d,projs);
  if(!source||source.workspace_type!==wt){panel.state="CONTEXT_MISMATCH";panel.predicate=source?"PROJECTION_WORKSPACE_TYPE_MISMATCH":"PROJECTION_SOURCE_NOT_FOUND";panel.rows_withheld=true;return panel;}
  var adapter=ADAPTERS[panel.capability];
  if(adapter){var a=adapter(source);if(a.problem){panel.state="MALFORMED";panel.predicate=a.problem;panel.rows_withheld=true;return panel;}panel.rows=a.rows;panel.notes=a.notes;panel.malformed_rows=a.malformed_rows;}
  else if(panel.rendered_in){panel.notes.push(countRows(source,panel.projection_field)+" row(s) rendered in the "+panel.rendered_in);}
  else{panel.notes.push(countRows(source,panel.projection_field)+" row(s) present; no panel adapter defined for this family");}
  return panel;
 });
 return {schema:SCHEMA,disposition:"ALLOW",predicate:"PANELS_DERIVED_FROM_CAPABILITY_STATUS",workspace_type:wt,panels:panels,action_eligible:false,authority_effect:"NONE"};
}
function panel_cap(d,s){return text((s&&s.capability)||(d&&d.capability));}
root.StegVerseWorkspacePanels=Object.freeze({schema:SCHEMA,build:build,row_states:ROW_STATES.slice(),authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
