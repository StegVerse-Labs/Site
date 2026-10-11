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
var KIND_ORDER=["assistant","principal","organization","membership","feed","portfolio"];
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function text(v){return v===null||v===undefined?"":String(v);}
function tokens(q){return text(q).toLowerCase().trim().split(/\s+/).filter(Boolean);}
function hay(parts){return parts.map(text).join(" ").toLowerCase();}
function matches(parts,toks){var h=hay(parts);for(var i=0;i<toks.length;i++)if(h.indexOf(toks[i])<0)return false;return true;}
// Field extractors: projection field -> candidate rows. Only fields with an extractor are searchable.
var EXTRACT={
 principals:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(p){return {kind:p.principal_type==="ORGANIZATION"?"organization":"principal",id:text(p.principal_id),label:text(p.display_name||p.principal_id),detail:text(p.principal_type)+(Array.isArray(p.roles)&&p.roles.length?" · "+p.roles.join(", "):""),parts:[p.display_name,p.principal_id,p.principal_type,Array.isArray(p.roles)?p.roles.join(" "):""]};});},
 organizations:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(o){return {kind:"organization",id:text(o.principal_id),label:text(o.display_name||o.principal_id),detail:text(o.principal_type||"ORGANIZATION"),parts:[o.display_name,o.principal_id,o.principal_type]};});},
 memberships:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(m){return {kind:"membership",id:text(m.organization_id||m.organization_name),label:text(m.organization_name||m.organization_id),detail:[m.role,m.department,m.status].filter(Boolean).map(text).join(" · "),parts:[m.organization_name,m.organization_id,m.role,m.department,m.status]};});},
 feed:function(v){return (Array.isArray(v)?v:[]).filter(isObject).map(function(e){return {kind:"feed",id:text(e.event_id||e.actor_id),label:text(e.actor_name||e.actor_id),detail:text(e.text||e.activity||e.event_type||"Activity"),visibility:text(e.visibility||"PRIVATE"),row:e,parts:[e.actor_name,e.actor_id,e.text,e.activity,e.event_type]};});},
 assistant:function(v){return isObject(v)?[{kind:"assistant",id:text(v.principal_id),label:text(v.display_name||v.principal_id),detail:"WORKSPACE_ASSISTANT (display only; no invocation route)",parts:[v.display_name,v.principal_id,"assistant"]}]:[];},
 portfolio:function(v){var rows=isObject(v)&&Array.isArray(v.positions)?v.positions:[];return rows.filter(isObject).map(function(p){return {kind:"portfolio",id:text(p.product_id||p.asset),label:text(p.asset||p.product_id),detail:[p.product_id,p.quantity!==undefined?"qty "+text(p.quantity):null,p.value_usd!==undefined?"usd "+text(p.value_usd):null].filter(Boolean).join(" · "),parts:[p.asset,p.product_id,p.chain,p.contract]};});}
};
function result(disposition,predicate,extra){
 var r={schema:SCHEMA,disposition:disposition,predicate:predicate,query:"",workspace_type:null,hits:[],hit_count:0,truncated:false,excluded:[],visibility_withheld:0,ambiguous:[],index:"NONE_EPHEMERAL_QUERY_ONLY",action_eligible:false,authority_effect:"NONE"};
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
 var toks=tokens(q),excluded=[],hits=[],withheld=0;
 for(var i=0;i<descs.length;i++){
  var d=descs[i],s=statuses[i],field=s.projection_field;
  if(C.withholdsRows(s)){excluded.push({capability:s.capability,projection_field:field,state:s.state,predicate:s.predicate});continue;}
  if(!EXTRACT[field]){excluded.push({capability:s.capability,projection_field:field,state:s.state,predicate:"SEARCH_EXTRACTOR_NOT_DEFINED"});continue;}
  var schemas=Array.isArray(d.allowed_projection_schemas)?d.allowed_projection_schemas:[];
  var source=null;for(var j=0;j<projs.length;j++){if(isObject(projs[j])&&schemas.indexOf(projs[j].schema)>=0){source=projs[j];break;}}
  if(!source){excluded.push({capability:s.capability,projection_field:field,state:s.state,predicate:"PROJECTION_SOURCE_NOT_FOUND"});continue;}
  if(!toks.length)continue;
  var rows=EXTRACT[field](source[field]),prov=provenanceOf(s,source);
  for(var r=0;r<rows.length;r++){
   var row=rows[r];
   if(row.kind==="feed"&&visible&&!visible(row.row)){withheld++;continue;}
   if(!matches(row.parts,toks))continue;
   hits.push({kind:row.kind,id:row.id,label:row.label,detail:row.detail,capability:s.capability,projection_field:field,context:{workspace_type:wt},provenance:prov,action_eligible:false});
  }
 }
 hits.sort(function(a,b){var ka=KIND_ORDER.indexOf(a.kind),kb=KIND_ORDER.indexOf(b.kind);if(ka!==kb)return ka-kb;return a.label<b.label?-1:a.label>b.label?1:0;});
 var truncated=hits.length>MAX_HITS;if(truncated)hits=hits.slice(0,MAX_HITS);
 return result("ALLOW",toks.length?"SEARCH_COMPLETED":"QUERY_EMPTY",{query:q,workspace_type:wt,hits:hits,hit_count:hits.length,truncated:truncated,excluded:excluded,visibility_withheld:withheld});
}
root.StegVerseWorkspaceSearch=Object.freeze({schema:SCHEMA,search:search,max_hits:MAX_HITS,index:"NONE_EPHEMERAL_QUERY_ONLY",authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
