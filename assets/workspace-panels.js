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
 EMAIL:"continuity-vault-kit runtime/email_family_projection.py (stegverse.kv.email-family-projection/v1, from governed ADMIT receipts; Personal KV only, no Org-KV email projection yet)",
 MESSAGING:"no KV projection contract published yet (existing authorized integration owner)",
 DOCUMENTS:"no KV projection contract published yet (existing authorized integration owner)",
 SOCIAL:"no KV projection contract published yet (existing authorized integration owner)",
 VOIP:"no KV projection contract published yet (existing authorized telephony integration owner; call records only, never call control)",
 SPREADSHEETS:"no KV projection contract published yet (existing authorized document integration owner)",
 PRESENTATIONS:"no KV projection contract published yet (existing authorized document integration owner)",
 DEV_CODE:"no developer KV projection contract published yet (repository/source custody owner; GitHub is never read directly by this page)",
 DEV_TASKS:"canonical Task Registry (StegVerse-Labs/.github data/canonical-task-records) — custody write path exists (continuity-vault-kit task_registry_event_sovereign_kv_binding) but no KV read projection is published yet",
 DEV_BUILD:"no developer KV projection contract published yet (build/CI evidence owner; GitHub Actions is never read directly by this page)",
 DEV_GOVERNANCE:"StegVerse-Labs/.github#3012 (governance product producer; read-only dependency of this page; proposal P1 only)",
 DEV_RUNTIME:"no developer KV projection contract published yet (sovereign resident runtime / StegHealth owners)",
 DEV_EVIDENCE:"no developer KV projection contract published yet (Interlock/InTr receipts and Master Records readback owners)",
 DEV_AI_COLLABORATION:"same MyKV assistant under a capability-scoped policy (StegVerse-Labs/.github ECOSYSTEM-INGRESS-AI-BOUNDARIES-001, component RTC-NONCHATGPT-AI-DECISION-SANDBOX-011); no policy projection is published yet"
};
// Plain-language reason for every predicate a panel can carry when it downgrades its capability status, so the
// "Why?" explanation states the panel's own outcome rather than the status it overrode.
var REASONS={
 CAPABILITY_STATUS_ABSENT:"no capability status was produced for this panel, so nothing from its projection is shown",
 PROJECTION_SOURCE_NOT_FOUND:"no projection matching this capability was supplied, so the panel has nothing it may show",
 PROJECTION_WORKSPACE_TYPE_MISMATCH:"the projection belongs to a different workspace context than the one being viewed",
 PROJECTION_TRADE_AUTHORITY_INVALID:"the portfolio projection does not state plainly that it grants no trading authority, so it is refused",
 PORTFOLIO_FIELD_INVALID:"the portfolio projection has no readable portfolio section",
 PORTFOLIO_DRAWDOWN_INVALID:"the portfolio drawdown is not a percentage between 0 and 100",
 PORTFOLIO_TOTAL_INVALID:"the portfolio total is not a finite amount of zero or more",
 PORTFOLIO_PROVIDER_INVALID:"the portfolio provider name is empty, too long or contains hidden characters",
 PORTFOLIO_OBSERVED_AT_INVALID:"the provider observation time is empty, too long or contains hidden characters",
 PORTFOLIO_SOURCE_AUTHORITY_INVALID:"the portfolio source authority is empty, too long or contains hidden characters",
 PORTFOLIO_SNAPSHOT_ID_INVALID:"the portfolio snapshot identifier is empty, too long or contains hidden characters",
 PORTFOLIO_UNAVAILABLE_FIELDS_INVALID:"the list of fields the provider could not supply contains text that is empty, too long or hidden",
 EMAIL_ACCOUNTS_INVALID:"the email projection has no readable list of accounts",
 EMAIL_ACCOUNTS_MIXED:"the email projection names an account twice or puts a message under the wrong account, and accounts are never merged",
 PANEL_CONTEXT_NOT_ADMITTED:"this family is projected from Personal KV only, so it is never shown in another workspace context"
};
var RENDERED_ELSEWHERE={FEED:"Feed card",CONTACTS:"Friends & Contacts card",ORGANIZATIONS:"Organizations card",MEMBERSHIPS:"Memberships card",AI_ASSISTANT:"MyKV assistant card",TASKS:"Tasks & commitments card",COMMITMENTS:"Tasks & commitments card"};
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function text(v){return v===null||v===undefined?"":String(v);}
function isNum(v){return typeof v==="number"&&isFinite(v);}
// Producer bounds (crypto-bot project_portfolio_snapshot_for_workspace.py), re-checked here so a projection that did
// not come through that producer cannot render a label that displays as something else or an impossible figure.
var HIDDEN_TEXT=/[\p{Cc}\p{Cf}\p{Cs}\p{Zl}\p{Zp}]/u,MAX_LABEL=64,MAX_SNAPSHOT_ID=128;
function displayable(v,limit){return typeof v==="string"&&v.trim().length>0&&v.length<=limit&&!HIDDEN_TEXT.test(v);}
function amount(v){return isNum(v)&&v>=0;}
function sourceFor(descriptor,projections){
 var schemas=isObject(descriptor)&&Array.isArray(descriptor.allowed_projection_schemas)?descriptor.allowed_projection_schemas:[];
 for(var i=0;i<(projections||[]).length;i++){var p=projections[i];if(isObject(p)&&schemas.indexOf(p.schema)>=0)return p;}
 return null;
}
// Shared EMAIL validation (one source of truth for the EMAIL panel and WorkSpace search, Site#1509): returns
// {problem} or {accounts:[{mapping_id, provider_id, mapping_state, cursor, verified, message_count, messages}],
// malformed_rows, withheld}. Only accounts and message rows that pass every display bound are returned; messages of a
// mapping that is not SESSION_VERIFIED are withheld; skap_ref and staged_content_hash are never copied out.
function emailView(p){
 var bad=function(problem){return {problem:problem,accounts:[],malformed_rows:0,withheld:0};};
 if(!isObject(p)||!Array.isArray(p.accounts)||!Array.isArray(p.messages))return bad("EMAIL_ACCOUNTS_INVALID");
 var groups=new Map(),order=[],malformed=0,withheld=0,accounts=[];
 for(var i=0;i<p.accounts.length;i++){var a=p.accounts[i],id=isObject(a)?a.mapping_id:null;
  if(typeof id==="string"&&groups.has(id))return bad("EMAIL_ACCOUNTS_MIXED");
  if(!displayable(id,MAX_SNAPSHOT_ID)){malformed++;continue;}
  groups.set(id,{account:a,rows:[]});order.push(id);
 }
 for(var j=0;j<p.messages.length;j++){var m=p.messages[j];
  if(!isObject(m)||typeof m.mapping_id!=="string"||!groups.has(m.mapping_id))return bad("EMAIL_ACCOUNTS_MIXED");
  groups.get(m.mapping_id).rows.push(m);
 }
 order.forEach(function(id){var g=groups.get(id),a=g.account,c=a.cursor;
  if(!displayable(a.provider_id,MAX_LABEL)||!displayable(a.mapping_state,MAX_LABEL)||!isObject(c)||!isNum(c.sequence)||!(c.head_receipt_id===null||displayable(c.head_receipt_id,MAX_SNAPSHOT_ID))||!(c.chain_digest===null||displayable(c.chain_digest,MAX_SNAPSHOT_ID))||!(c.provider_position===null||Number.isSafeInteger(c.provider_position))||!(c.provider_cursor_ref===undefined||c.provider_cursor_ref===null||displayable(c.provider_cursor_ref,MAX_SNAPSHOT_ID))){malformed+=1+g.rows.length;return;}
  var verified=a.mapping_state==="SESSION_VERIFIED",messages=[];
  if(!verified)withheld+=g.rows.length;
  else g.rows.forEach(function(m){
   if(!displayable(m.canonical_message_id,256)||!displayable(m.receipt_id,MAX_SNAPSHOT_ID)||!isNum(m.sequence)||m.payload_present!==false){malformed++;return;}
   messages.push({canonical_message_id:m.canonical_message_id,receipt_id:m.receipt_id,sequence:m.sequence});
  });
  accounts.push({mapping_id:id,provider_id:a.provider_id,mapping_state:a.mapping_state,cursor:{sequence:c.sequence,head_receipt_id:c.head_receipt_id,chain_digest:c.chain_digest,provider_position:c.provider_position,provider_cursor_ref:c.provider_cursor_ref},verified:verified,message_count:g.rows.length,messages:messages});
 });
 return {problem:null,accounts:accounts,malformed_rows:malformed,withheld:withheld};
}
// Families admitted only in some contexts: the email projection is Personal KV only (no Org-KV email projection
// exists), so an EMAIL panel never renders rows outside the personal context, whatever the source declares.
var PANEL_CONTEXTS={EMAIL:["PERSONAL"]};
// Adapters return {rows, notes, malformed_rows, problem}. problem (if set) downgrades the panel to MALFORMED.
var ADAPTERS={
 CRYPTOBOT_PORTFOLIO:function(p){
  var out={rows:[],notes:[],malformed_rows:0,problem:null},pf=p.portfolio;
  if(p.trade_authority_granted!==false)return {rows:[],notes:[],malformed_rows:0,problem:"PROJECTION_TRADE_AUTHORITY_INVALID"};
  if(!isObject(pf))return {rows:[],notes:[],malformed_rows:0,problem:"PORTFOLIO_FIELD_INVALID"};
  var bad=function(problem){return {rows:[],notes:[],malformed_rows:0,problem:problem};};
  if(pf.drawdown_percent!==null&&pf.drawdown_percent!==undefined&&!(isNum(pf.drawdown_percent)&&pf.drawdown_percent>=0&&pf.drawdown_percent<=100))return bad("PORTFOLIO_DRAWDOWN_INVALID");
  if(pf.total_value_usd!==null&&pf.total_value_usd!==undefined&&!amount(pf.total_value_usd))return bad("PORTFOLIO_TOTAL_INVALID");
  if(pf.provider!==null&&pf.provider!==undefined&&!displayable(pf.provider,MAX_LABEL))return bad("PORTFOLIO_PROVIDER_INVALID");
  if(pf.source_observed_at!==null&&pf.source_observed_at!==undefined&&!displayable(pf.source_observed_at,MAX_SNAPSHOT_ID))return bad("PORTFOLIO_OBSERVED_AT_INVALID");
  if(isObject(p.source)&&p.source.authority!==null&&p.source.authority!==undefined&&!displayable(p.source.authority,MAX_SNAPSHOT_ID))return bad("PORTFOLIO_SOURCE_AUTHORITY_INVALID");
  if(isObject(p.source)&&p.source.snapshot_id!==null&&p.source.snapshot_id!==undefined&&!displayable(p.source.snapshot_id,MAX_SNAPSHOT_ID))return bad("PORTFOLIO_SNAPSHOT_ID_INVALID");
  if(isObject(pf.unavailable_fields)&&!Object.keys(pf.unavailable_fields).every(function(k){return displayable(k,MAX_LABEL)&&displayable(pf.unavailable_fields[k],MAX_SNAPSHOT_ID);}))return bad("PORTFOLIO_UNAVAILABLE_FIELDS_INVALID");
  var positions=Array.isArray(pf.positions)?pf.positions:[];
  for(var i=0;i<positions.length;i++){var x=positions[i];
   if(!isObject(x)||!displayable(x.asset,MAX_LABEL)||!amount(x.quantity)||(x.product_id!==undefined&&x.product_id!==null&&!displayable(x.product_id,MAX_LABEL))||(x.value_usd!==undefined&&x.value_usd!==null&&!amount(x.value_usd))||(x.price_usd!==undefined&&x.price_usd!==null&&!amount(x.price_usd))){out.malformed_rows++;continue;}
   out.rows.push({label:x.asset,detail:[x.product_id?"product "+text(x.product_id):null,"qty "+text(x.quantity),isNum(x.value_usd)?"usd "+text(x.value_usd):"value UNAVAILABLE",isNum(x.price_usd)?"price "+text(x.price_usd):null].filter(Boolean).join(" · ")});
  }
  if(amount(pf.total_value_usd))out.notes.push("total usd "+text(pf.total_value_usd));
  out.notes.push("drawdown "+(isNum(pf.drawdown_percent)?text(pf.drawdown_percent)+"%":"UNAVAILABLE"));
  if(pf.provider)out.notes.push("provider "+text(pf.provider));
  if(pf.source_observed_at)out.notes.push("provider observation "+text(pf.source_observed_at)+" (distinct from projection time)");
  if(isObject(pf.unavailable_fields)){Object.keys(pf.unavailable_fields).sort().forEach(function(k){out.notes.push(k+": "+text(pf.unavailable_fields[k]));});}
  if(isObject(p.source)&&p.source.authority)out.notes.push("source authority "+text(p.source.authority));
  out.notes.push("trade_authority_granted: false · provider_operation_authorized: "+text(p.provider_operation_authorized));
  return out;
 },
 // Email family (Site#1509 lane B), keyed to the lane A producer (continuity-vault-kit runtime/email_family_projection.py,
 // stegverse.kv.email-family-projection/v1): one provenance row per mailbox mapping (provider, mapping state, cursor
 // sequence, head ADMIT receipt, chain digest, provider position shown as text only) followed by that mapping's
 // payload-free message rows (withheld when the mapping is not SESSION_VERIFIED),
 // each naming its own mapping and receipt. Accounts are never merged: a repeated mapping or a message naming a mapping
 // not listed downgrades the whole panel. No skap:// reference, body or credential is shown; nothing can operate on a
 // mailbox. Display bounds are re-checked here independently of the bridge and the producer.
 EMAIL:function(p){
  var v=emailView(p),out={rows:[],notes:[],malformed_rows:v.malformed_rows,problem:null};
  if(v.problem)return {rows:[],notes:[],malformed_rows:0,problem:v.problem};
  v.accounts.forEach(function(a){var c=a.cursor;
   out.rows.push({label:a.mapping_id,detail:["mailbox mapping","provider "+text(a.provider_id),text(a.mapping_state),"cursor sequence "+text(c.sequence),"head ADMIT receipt "+(c.head_receipt_id?text(c.head_receipt_id):"none"),"chain "+(c.chain_digest?text(c.chain_digest):"none"),"provider position "+(c.provider_position===null?"none":text(c.provider_position)),c.provider_cursor_ref?"provider cursor "+text(c.provider_cursor_ref):null,a.verified?a.message_count+" message(s)":a.message_count+" message row(s) withheld: mapping is not SESSION_VERIFIED"].filter(Boolean).join(" · "),account_id:a.mapping_id});
   a.messages.forEach(function(m){out.rows.push({label:m.canonical_message_id,detail:"mapping "+text(a.mapping_id)+" · ADMIT receipt "+text(m.receipt_id)+" · sequence "+text(m.sequence)+" · payload not present",account_id:a.mapping_id});});
  });
  out.notes.push(v.accounts.length+" mailbox mapping(s) shown separately; each row names its own mapping, and accounts are never merged");
  if(v.withheld)out.notes.push(v.withheld+" message row(s) withheld because their mapping is not SESSION_VERIFIED");
  out.notes.push("message rows are payload-free admission records; credential material is held only in SKAP Vault; credential_material_present: "+text(p.credential_material_present)+" · provider_operation_authorized: "+text(p.provider_operation_authorized));
  return out;
 },
 // Re-check consumer display bounds independently of the KV producer. Never render hidden Unicode or
 // oversized untrusted labels/status/due strings, even if the upstream projection was malformed.
 TASKS:function(p){var out={rows:[],notes:[],malformed_rows:0,problem:null};(Array.isArray(p.tasks)?p.tasks:[]).forEach(function(t){if(!isObject(t)||!displayable(t.title,256)||!displayable(t.status,64)||(t.due_at!==undefined&&t.due_at!==null&&!displayable(t.due_at,128))){out.malformed_rows++;return;}out.rows.push({label:t.title,detail:t.status+(t.due_at?" · due "+t.due_at:"")});});return out;},
 COMMITMENTS:function(p){var out={rows:[],notes:[],malformed_rows:0,problem:null};(Array.isArray(p.commitments)?p.commitments:[]).forEach(function(c){if(!isObject(c)||!displayable(c.statement,256)||!displayable(c.status,64)||(c.due_at!==undefined&&c.due_at!==null&&!displayable(c.due_at,128))){out.malformed_rows++;return;}out.rows.push({label:c.statement,detail:c.status+(c.due_at?" · due "+c.due_at:"")});});return out;}
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
  if(PANEL_CONTEXTS[panel.capability]&&PANEL_CONTEXTS[panel.capability].indexOf(wt)<0){panel.state="CONTEXT_MISMATCH";panel.predicate="PANEL_CONTEXT_NOT_ADMITTED";panel.rows_withheld=true;return panel;}
  var adapter=ADAPTERS[panel.capability];
  if(adapter){var a=adapter(source);if(a.problem){panel.state="MALFORMED";panel.predicate=a.problem;panel.rows_withheld=true;return panel;}panel.rows=a.rows;panel.notes=a.notes;panel.malformed_rows=a.malformed_rows;}
  else if(panel.rendered_in){panel.notes.push(countRows(source,panel.projection_field)+" row(s) rendered in the "+panel.rendered_in);}
  else{panel.notes.push(countRows(source,panel.projection_field)+" row(s) present; no panel adapter defined for this family");}
  return panel;
 });
 return {schema:SCHEMA,disposition:"ALLOW",predicate:"PANELS_DERIVED_FROM_CAPABILITY_STATUS",workspace_type:wt,panels:panels,action_eligible:false,authority_effect:"NONE"};
}
function panel_cap(d,s){return text((s&&s.capability)||(d&&d.capability));}
root.StegVerseWorkspacePanels=Object.freeze({schema:SCHEMA,build:build,emailView:emailView,panelContexts:Object.freeze({EMAIL:Object.freeze(PANEL_CONTEXTS.EMAIL.slice())}),reasons:Object.freeze(REASONS),row_states:ROW_STATES.slice(),authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
