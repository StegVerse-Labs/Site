// WorkSpace universal search (Site#1509 WS-SEARCH): stegverse.workspace.search/v1.
// Searches only the KV projections handed to it, for the active context only, and only through the capability
// contract: a field is searchable exactly when its capability status does not withhold rows, STALE and
// FRESHNESS_UNKNOWN hits are labelled, a second source for one capability fails the whole search closed, and a
// projection for another context is never searched. Every hit carries the provenance of the projection it came
// from. There is no index: each call recomputes over the supplied projections and nothing is stored anywhere.
// Results are informational only; a hit is not a permission to act (action_eligible: false).
(function(root){
"use strict";
if(!root)return;
var SCHEMA="stegverse.workspace.search/v1";
var MAX_HITS=50;
var KIND_ORDER=["assistant","principal","organization","membership","task","commitment","feed","portfolio","email_account","email_message"];
// Searchable states are an explicit allow-list, never "not withheld": only an observed, stale or freshness-unknown
// source for THIS context is searched, and the source projection itself must declare the same context.
var SEARCHABLE=["OBSERVED","STALE","FRESHNESS_UNKNOWN"];
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function text(v){return v===null||v===undefined?"":String(v);}
function tokens(q){return text(q).toLowerCase().trim().split(/\s+/).filter(Boolean);}
function hay(parts){return parts.map(text).join(" ").toLowerCase();}
// A hit shows its label, detail and id; one whose text holds hidden characters (control, format, surrogate, separator)
// or exceeds the display bound is withheld and counted, never shown (same rule as the panels and tasks card, Site#1555/#1556).
var HIDDEN_TEXT=/[\p{Cc}\p{Cf}\p{Cs}\p{Zl}\p{Zp}]/u;
function shown(v,limit){return v.length<=limit&&!HIDDEN_TEXT.test(v);}
function displayable(row){return row.label.trim().length>0&&shown(row.label,256)&&shown(row.detail,1024)&&shown(row.id,256);}
function matches(parts,toks){var h=hay(parts);for(var i=0;i<toks.length;i++)if(h.indexOf(toks[i])<0)return false;return true;}
// Field extractors: projection field -> candidate rows. Only fields with an extractor are searchable.
var EXTRACT={
 principals:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(p){return {kind:p.principal_type==="ORGANIZATION"?"organization":"principal",id:text(p.principal_id),label:text(p.display_name||p.principal_id),detail:text(p.principal_type)+(Array.isArray(p.roles)&&p.roles.length?" · "+p.roles.join(", "):""),parts:[p.display_name,p.principal_id,p.principal_type,Array.isArray(p.roles)?p.roles.join(" "):""]};});},
 organizations:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(o){return {kind:"organization",id:text(o.principal_id),label:text(o.display_name||o.principal_id),detail:text(o.principal_type||"ORGANIZATION"),parts:[o.display_name,o.principal_id,o.principal_type]};});},
 memberships:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(m){return {kind:"membership",id:text(m.organization_id||m.organization_name),label:text(m.organization_name||m.organization_id),detail:[m.role,m.department,m.status].filter(Boolean).map(text).join(" · "),parts:[m.organization_name,m.organization_id,m.role,m.department,m.status]};});},
 feed:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(e){return {kind:"feed",id:text(e.event_id||e.actor_id),label:text(e.actor_name||e.actor_id),detail:text(e.text||e.activity||e.event_type||"Activity"),visibility:text(e.visibility||"PRIVATE"),row:e,parts:[e.actor_name,e.actor_id,e.text,e.activity,e.event_type]};});},
 assistant:function(v){return isObject(v)?[{kind:"assistant",id:text(v.principal_id),label:text(v.display_name||v.principal_id),detail:"WORKSPACE_ASSISTANT (display only; no invocation route)",parts:[v.display_name,v.principal_id,"assistant"]}]:[];},
 tasks:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(t){return {kind:"task",id:text(t.task_id),label:text(t.title),detail:[t.status,t.due_at?"due "+text(t.due_at):null].filter(Boolean).map(text).join(" · ")+" · action_eligible: false",parts:[t.title,t.task_id,t.status,t.source_ref]};});},
 commitments:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(c){return {kind:"commitment",id:text(c.commitment_id),label:text(c.statement),detail:[c.status,c.counterparty_principal_id?"with "+text(c.counterparty_principal_id):null,c.due_at?"due "+text(c.due_at):null].filter(Boolean).map(text).join(" · ")+" · action_eligible: false",parts:[c.statement,c.commitment_id,c.status,c.counterparty_principal_id,c.source_ref]};});},
 portfolio:function(v){var rows=isObject(v)&&Array.isArray(v.positions)?v.positions:[];return rows.filter(isObject).map(function(p){return {kind:"portfolio",id:text(p.product_id||p.asset),label:text(p.asset||p.product_id),detail:[p.product_id,p.quantity!==undefined?"qty "+text(p.quantity):null,p.value_usd!==undefined?"usd "+text(p.value_usd):null].filter(Boolean).join(" · "),parts:[p.asset,p.product_id,p.chain,p.contract]};});},
 // Email family (stegverse.kv.email-family-projection/v1, Site#1509): searches exactly what the EMAIL panel shows and
 // nothing else. A mailbox mapping matches on its provider_id, mapping_state and mapping_id; a message row matches on its
 // canonical_message_id, ADMIT receipt_id and mapping_id. skap_ref, cursor internals, staged_content_hash and every
 // other field are never searched or shown. Message rows of a mapping that is not SESSION_VERIFIED, or that carry a
 // payload, are not searched (the panel withholds them too). A repeated mapping or a message naming an unlisted mapping
 // excludes the whole capability (accounts are never merged), as the panel downgrades it.
 accounts:function(v,source){
  if(!Array.isArray(v)||!isObject(source)||!Array.isArray(source.messages))return {problem:"EMAIL_ACCOUNTS_INVALID"};
  var groups={},order=[],rows=[];
  for(var i=0;i<v.length;i++){var a=v[i],id=isObject(a)&&typeof a.mapping_id==="string"?a.mapping_id:null;
   if(id===null)continue;
   if(Object.prototype.hasOwnProperty.call(groups,id))return {problem:"EMAIL_ACCOUNTS_MIXED"};
   groups[id]={account:a,messages:[]};order.push(id);
  }
  for(var j=0;j<source.messages.length;j++){var m=source.messages[j];
   if(!isObject(m)||typeof m.mapping_id!=="string"||!Object.prototype.hasOwnProperty.call(groups,m.mapping_id))return {problem:"EMAIL_ACCOUNTS_MIXED"};
   groups[m.mapping_id].messages.push(m);
  }
  order.forEach(function(id){var a=groups[id].account;
   rows.push({kind:"email_account",id:id,label:id,detail:["mailbox mapping","provider "+text(a.provider_id),text(a.mapping_state)].join(" · ")+" · action_eligible: false",parts:[a.provider_id,a.mapping_state,id]});
   if(a.mapping_state!=="SESSION_VERIFIED")return;
   groups[id].messages.forEach(function(m){
    if(m.payload_present!==false||typeof m.sequence!=="number")return;
    rows.push({kind:"email_message",id:text(m.canonical_message_id),label:text(m.canonical_message_id),detail:"mapping "+id+" · ADMIT receipt "+text(m.receipt_id)+" · sequence "+text(m.sequence)+" · payload not present · action_eligible: false",parts:[m.canonical_message_id,m.receipt_id,id]});
   });
  });
  return rows;
 }
};
// Fields admitted only in some contexts: a personal email projection is never searched outside the personal context,
// even if a projection declaring another context were handed in (no Org-KV email projection exists yet).
var FIELD_CONTEXTS={accounts:["PERSONAL"]};
function result(disposition,predicate,extra){
 var r={schema:SCHEMA,disposition:disposition,predicate:predicate,query:"",workspace_type:null,hits:[],hit_count:0,truncated:false,excluded:[],visibility_withheld:0,display_withheld:0,ambiguous:[],index:"NONE_EPHEMERAL_QUERY_ONLY",action_eligible:false,authority_effect:"NONE"};
 if(extra)for(var k in extra)if(Object.prototype.hasOwnProperty.call(extra,k))r[k]=extra[k];
 return r;
}
function provenanceOf(status,projection){
 return {projection_schema:text(projection&&projection.schema),freshness_state:status.state,freshness_predicate:status.predicate,observed_at:status.observed_at||null,age_seconds:status.age_seconds===undefined?null:status.age_seconds,provenance_ref:status.provenance_ref||null,source_revision:status.source_revision||null,source_cursor:status.source_cursor||null,grant_state:status.grant_state||null,replay_status:status.replay_status||"REPLAY_STATUS_UNKNOWN"};
}
function search(input){
 var C=root.StegVerseWorkspaceCapabilities;
 if(!C||typeof C.evaluateAll!=="function"||typeof C.withholdsRows!=="function")return result("FAIL_CLOSED","CAPABILITY_CONTRACT_UNAVAILABLE");
 var inp=isObject(input)?input:{};
 var q=text(inp.query),wt=text(inp.workspace_type)||null,descs=inp.descriptors,projs=Array.isArray(inp.projections)?inp.projections:[],now=typeof inp.now_ms==="number"?inp.now_ms:Date.now();
 var visible=typeof inp.visibility==="function"?inp.visibility:null;
 if(!Array.isArray(descs))return result("FAIL_CLOSED","CAPABILITY_DESCRIPTORS_UNAVAILABLE",{query:q,workspace_type:wt});
 if(wt!=="PERSONAL"&&wt!=="ORGANIZATIONAL")return result("FAIL_CLOSED","WORKSPACE_CONTEXT_INVALID",{query:q,workspace_type:wt});
 var statuses=C.evaluateAll(descs,projs,wt,now);
 var ambiguous=statuses.filter(function(s){return s.predicate==="PROJECTION_SOURCE_AMBIGUOUS";}).map(function(s){return s.capability;});
 if(ambiguous.length)return result("FAIL_CLOSED","PROJECTION_SOURCE_AMBIGUOUS",{query:q,workspace_type:wt,ambiguous:ambiguous});
 var toks=tokens(q),excluded=[],hits=[],withheld=0,displayWithheld=0;
 for(var i=0;i<descs.length;i++){
  var d=descs[i],s=statuses[i],field=s.projection_field;
  if(C.withholdsRows(s)||SEARCHABLE.indexOf(s.state)<0){excluded.push({capability:s.capability,projection_field:field,state:s.state,predicate:s.predicate});continue;}
  if(!EXTRACT[field]){excluded.push({capability:s.capability,projection_field:field,state:s.state,predicate:"SEARCH_EXTRACTOR_NOT_DEFINED"});continue;}
  var schemas=Array.isArray(d.allowed_projection_schemas)?d.allowed_projection_schemas:[];
  var source=null;for(var j=0;j<projs.length;j++){if(isObject(projs[j])&&schemas.indexOf(projs[j].schema)>=0){source=projs[j];break;}}
  if(!source){excluded.push({capability:s.capability,projection_field:field,state:s.state,predicate:"PROJECTION_SOURCE_NOT_FOUND"});continue;}
  if(source.workspace_type!==wt){excluded.push({capability:s.capability,projection_field:field,state:"CONTEXT_MISMATCH",predicate:"PROJECTION_WORKSPACE_TYPE_MISMATCH"});continue;}
  if(FIELD_CONTEXTS[field]&&FIELD_CONTEXTS[field].indexOf(wt)<0){excluded.push({capability:s.capability,projection_field:field,state:"CONTEXT_MISMATCH",predicate:"SEARCH_CONTEXT_NOT_ADMITTED"});continue;}
  if(!toks.length)continue;
  var rows=EXTRACT[field](source[field],source),prov=provenanceOf(s,source);
  if(!Array.isArray(rows)){excluded.push({capability:s.capability,projection_field:field,state:"MALFORMED",predicate:text(rows&&rows.problem)||"SEARCH_SOURCE_MALFORMED"});continue;}
  for(var r=0;r<rows.length;r++){
   var row=rows[r];
   if(row.kind==="feed"&&visible&&!visible(row.row)){withheld++;continue;}
   if(!matches(row.parts,toks))continue;
   if(!displayable(row)){displayWithheld++;continue;}
   hits.push({kind:row.kind,id:row.id,label:row.label,detail:row.detail,capability:s.capability,projection_field:field,context:{workspace_type:wt},provenance:prov,action_eligible:false});
  }
 }
 hits.sort(function(a,b){var ka=KIND_ORDER.indexOf(a.kind),kb=KIND_ORDER.indexOf(b.kind);if(ka!==kb)return ka-kb;return a.label<b.label?-1:a.label>b.label?1:0;});
 var truncated=hits.length>MAX_HITS;if(truncated)hits=hits.slice(0,MAX_HITS);
 return result("ALLOW",toks.length?"SEARCH_COMPLETED":"QUERY_EMPTY",{query:q,workspace_type:wt,hits:hits,hit_count:hits.length,truncated:truncated,excluded:excluded,visibility_withheld:withheld,display_withheld:displayWithheld});
}
root.StegVerseWorkspaceSearch=Object.freeze({schema:SCHEMA,search:search,max_hits:MAX_HITS,index:"NONE_EPHEMERAL_QUERY_ONLY",authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
