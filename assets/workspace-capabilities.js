// Workspace capability descriptors and per-capability freshness/provenance status (Site#1509).
// Descriptors are static, non-authorizing labels: they may never assert availability, admission,
// freshness or ALLOW. Every observed state is derived only from the authenticated KV projection
// handed over by the Workspace KV bridge; anything missing stays NOT_OBSERVED or UNAVAILABLE.
(function(root){
"use strict";
if(!root)return;
var DESCRIPTOR_SCHEMA="stegverse.workspace.capability-descriptor/v1";
var STATUS_SCHEMA="stegverse.workspace.capability-status/v1";
var DESCRIPTOR_KEYS=["capability","label","projection_field","allowed_projection_schemas","workspace_types","max_age_seconds","default_state","authority_effect"];
var WORKSPACE_TYPES=["PERSONAL","ORGANIZATIONAL"];
var METADATA_SCHEMA="stegverse.kv.workspace-projection-metadata/v1";
var CLOCK_SKEW_MS=5*60*1000;
// States that withdraw projected rows from rendering; STALE rows remain visible but labelled.
var WITHHELD=["DESCRIPTOR_REJECTED","MALFORMED","CONTEXT_MISMATCH","REVOKED"];
function own(o,k){return Object.prototype.hasOwnProperty.call(o,k);}
function descriptorProblem(d){
 if(!d||typeof d!=="object"||Array.isArray(d))return "DESCRIPTOR_NOT_OBJECT";
 for(var k in d)if(own(d,k)&&DESCRIPTOR_KEYS.indexOf(k)<0)return "DESCRIPTOR_FIELD_FORBIDDEN:"+k;
 if(typeof d.capability!=="string"||!d.capability)return "DESCRIPTOR_CAPABILITY_REQUIRED";
 if(typeof d.label!=="string"||!d.label)return "DESCRIPTOR_LABEL_REQUIRED";
 if(d.default_state!=="NOT_OBSERVED")return "DESCRIPTOR_DEFAULT_STATE_MUST_BE_NOT_OBSERVED";
 if(d.authority_effect!=="NONE")return "DESCRIPTOR_AUTHORITY_EFFECT_MUST_BE_NONE";
 if(!Array.isArray(d.allowed_projection_schemas)||!d.allowed_projection_schemas.every(function(s){return typeof s==="string"&&s;}))return "DESCRIPTOR_SCHEMAS_INVALID";
 if(!Array.isArray(d.workspace_types)||!d.workspace_types.length||!d.workspace_types.every(function(t){return WORKSPACE_TYPES.indexOf(t)>=0;}))return "DESCRIPTOR_WORKSPACE_TYPES_INVALID";
 if(d.allowed_projection_schemas.length){
  if(typeof d.projection_field!=="string"||!d.projection_field)return "DESCRIPTOR_PROJECTION_FIELD_REQUIRED";
  if(!(typeof d.max_age_seconds==="number"&&isFinite(d.max_age_seconds)&&d.max_age_seconds>0))return "DESCRIPTOR_MAX_AGE_INVALID";
 }
 return null;
}
// Every status, OBSERVED included, is informational only: no write or action interface may treat it as current, admitted or eligible.
function status(state,predicate,extra){var s={schema:STATUS_SCHEMA,state:state,predicate:predicate,action_eligible:false,authority_effect:"NONE"};if(extra)for(var k in extra)if(own(extra,k))s[k]=extra[k];return s;}
function evaluate(descriptor,projection,workspaceType,nowMs){
 var problem=descriptorProblem(descriptor);
 if(problem)return status("DESCRIPTOR_REJECTED",problem);
 if(!descriptor.allowed_projection_schemas.length)return status("UNAVAILABLE","NO_KV_PROJECTION_CONTRACT");
 if(descriptor.workspace_types.indexOf(workspaceType)<0)return status("UNAVAILABLE","CAPABILITY_NOT_DEFINED_FOR_CONTEXT");
 if(!projection)return status("NOT_OBSERVED",workspaceType==="ORGANIZATIONAL"?"ORG_KV_PROJECTION_NOT_OBSERVED":"KV_PROJECTION_NOT_OBSERVED");
 if(typeof projection!=="object"||descriptor.allowed_projection_schemas.indexOf(projection.schema)<0)return status("MALFORMED","PROJECTION_SCHEMA_NOT_ALLOWED");
 if(projection.workspace_type!==workspaceType)return status("CONTEXT_MISMATCH","PROJECTION_WORKSPACE_TYPE_MISMATCH");
 if(projection.authority_effect!=="NONE")return status("MALFORMED","PROJECTION_AUTHORITY_EFFECT_INVALID");
 var meta=own(projection,"projection_metadata")?projection.projection_metadata:undefined;
 if(meta!==undefined&&(meta===null||typeof meta!=="object"||Array.isArray(meta)))return status("MALFORMED","PROJECTION_METADATA_INVALID");
 if(meta&&meta.schema!==undefined&&meta.schema!==METADATA_SCHEMA)return status("MALFORMED","PROJECTION_METADATA_SCHEMA_INVALID");
 if(meta&&(meta.revoked===true||meta.grant_state==="REVOKED"))return status("REVOKED","PROJECTION_GRANT_REVOKED");
 if(!own(projection,descriptor.projection_field))return status("UNAVAILABLE","PROJECTION_FIELD_ABSENT");
 var value=projection[descriptor.projection_field];
 if(value!==null&&typeof value!=="object")return status("MALFORMED","PROJECTION_FIELD_TYPE_INVALID");
 var provenance={};
 if(meta&&typeof meta.provenance_ref==="string")provenance.provenance_ref=meta.provenance_ref;
 if(meta&&typeof meta.source_cursor==="string")provenance.source_cursor=meta.source_cursor;
 if(meta&&typeof meta.source_revision==="string")provenance.source_revision=meta.source_revision;
 if(meta)provenance.grant_state=typeof meta.grant_state==="string"?meta.grant_state:"UNKNOWN";
 if(!meta||meta.observed_at===undefined)return status("FRESHNESS_UNKNOWN","PROJECTION_OBSERVED_AT_ABSENT",provenance);
 var observed=typeof meta.observed_at==="string"?Date.parse(meta.observed_at):NaN;
 if(!isFinite(observed))return status("MALFORMED","PROJECTION_OBSERVED_AT_INVALID");
 if(observed-nowMs>CLOCK_SKEW_MS)return status("MALFORMED","PROJECTION_OBSERVED_AT_IN_FUTURE");
 provenance.observed_at=meta.observed_at;
 var ageSeconds=Math.max(0,Math.floor((nowMs-observed)/1000));
 provenance.age_seconds=ageSeconds;
 if(ageSeconds>descriptor.max_age_seconds)return status("STALE","PROJECTION_OLDER_THAN_MAX_AGE",provenance);
 return status("OBSERVED","PROJECTION_OBSERVED_WITHIN_MAX_AGE",provenance);
}
function evaluateAll(descriptors,projection,workspaceType,nowMs){
 if(!Array.isArray(descriptors))return [];
 return descriptors.map(function(d){var s=evaluate(d,projection,workspaceType,nowMs);s.capability=d&&typeof d.capability==="string"?d.capability:"UNKNOWN";s.label=d&&typeof d.label==="string"?d.label:s.capability;s.projection_field=d&&typeof d.projection_field==="string"?d.projection_field:null;return s;});
}
function withholdsRows(s){return !s||WITHHELD.indexOf(s.state)>=0;}
root.StegVerseWorkspaceCapabilities=Object.freeze({descriptor_schema:DESCRIPTOR_SCHEMA,status_schema:STATUS_SCHEMA,descriptorProblem:descriptorProblem,evaluate:evaluate,evaluateAll:evaluateAll,withholdsRows:withholdsRows,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
