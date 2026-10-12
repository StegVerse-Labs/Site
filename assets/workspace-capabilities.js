// Workspace capability descriptors and per-capability freshness/provenance status (Site#1509).
// Descriptors are static, non-authorizing labels: they may never assert availability, admission,
// freshness or ALLOW. Every observed state is derived only from the authenticated KV projection
// handed over by the Workspace KV bridge; anything missing stays NOT_OBSERVED or UNAVAILABLE.
(function(root){
"use strict";
if(!root)return;
// Plain-language reason per capability-status predicate, for the explanation contract
// (stegverse.user-facing-explanation/v1, .github#3106). Explanatory only: never changes a state or predicate.
var REASONS={
 "DESCRIPTOR_NOT_OBJECT":"this capability's description is not valid, so it is not evaluated",
 "DESCRIPTOR_FIELD_FORBIDDEN":"this capability's description contains a field that is not allowed, so it is not evaluated",
 "DESCRIPTOR_CAPABILITY_REQUIRED":"this capability's description does not name the capability, so it is not evaluated",
 "DESCRIPTOR_LABEL_REQUIRED":"this capability's description has no label, so it is not evaluated",
 "DESCRIPTOR_WORKSPACE_TYPES_INVALID":"this capability's description does not say which workspaces it belongs to, so it is not evaluated",
 "DESCRIPTOR_SCHEMAS_INVALID":"this capability's description lists its data formats incorrectly, so it is not evaluated",
 "DESCRIPTOR_PROJECTION_FIELD_REQUIRED":"this capability's description does not say where its data comes from, so it is not evaluated",
 "DESCRIPTOR_MAX_AGE_INVALID":"this capability's description sets an invalid freshness limit, so it is not evaluated",
 "DESCRIPTOR_DEFAULT_STATE_MUST_BE_NOT_OBSERVED":"this capability's description assumes data is present before any is observed, so it is not evaluated",
 "DESCRIPTOR_AUTHORITY_EFFECT_MUST_BE_NONE":"this capability's description claims authority, so it is not evaluated",
 "NO_KV_PROJECTION_CONTRACT":"no KnowledgeVault data format has been defined for this capability yet",
 "CAPABILITY_NOT_DEFINED_FOR_CONTEXT":"this capability is not offered in this kind of workspace",
 "KV_PROJECTION_NOT_OBSERVED":"no projection of your KnowledgeVault has reached this page",
 "ORG_KV_PROJECTION_NOT_OBSERVED":"no projection of the organization's KnowledgeVault has reached this page, and your personal one is never reused for it",
 "PROJECTION_SCHEMA_NOT_ALLOWED":"the projection is not in a format this capability accepts",
 "PROJECTION_WORKSPACE_TYPE_MISMATCH":"the projection is for a different kind of workspace than the one open",
 "PROJECTION_AUTHORITY_EFFECT_INVALID":"the projection claims authority, but a projection is only a read-only view",
 "PROJECTION_METADATA_INVALID":"the projection's details about whose it is and when it was observed are malformed",
 "PROJECTION_METADATA_SCHEMA_INVALID":"the projection's details are not in the expected format",
 "PROJECTION_GRANT_REVOKED":"access to this data has been revoked",
 "PROJECTION_FIELD_ABSENT":"the projection does not include data for this capability",
 "PROJECTION_FIELD_TYPE_INVALID":"the projection's data for this capability is malformed",
 "PROJECTION_OBSERVED_AT_ABSENT":"the projection does not say when it was observed, so its freshness is unknown",
 "PROJECTION_OBSERVED_AT_INVALID":"the projection's observation time is not a valid time",
 "PROJECTION_OBSERVED_AT_IN_FUTURE":"the projection says it was observed in the future, which cannot be right",
 "PROJECTION_METADATA_NOT_DISPLAYABLE":"the projection's provenance details contain hidden characters or are too long to show safely, so nothing from it is shown",
 "PROJECTION_OLDER_THAN_MAX_AGE":"the projection is older than this capability allows, so it may be out of date",
 "PROJECTION_OBSERVED_WITHIN_MAX_AGE":"the projection was observed recently enough for this capability; it is shown for information and permits no action",
 "PROJECTION_SOURCE_AMBIGUOUS":"more than one projection could supply this capability, and one is never chosen silently"
};
var DESCRIPTOR_SCHEMA="stegverse.workspace.capability-descriptor/v1";
var STATUS_SCHEMA="stegverse.workspace.capability-status/v1";
var DESCRIPTOR_KEYS=["capability","label","projection_field","allowed_projection_schemas","workspace_types","max_age_seconds","default_state","authority_effect"];
var WORKSPACE_TYPES=["PERSONAL","ORGANIZATIONAL","DEVELOPER"];
var METADATA_SCHEMA="stegverse.kv.workspace-projection-metadata/v1";
var CLOCK_SKEW_MS=5*60*1000;
// Replay/rollback refusal belongs to an authenticated KV/SKAP continuity checkpoint enforced by the producer, receiver
// or governed projection admission (Site#1509 ChatGPT cycle-3 review). None exists yet, so replay status is always
// UNKNOWN. Projection metadata and browser storage can never assert it.
var REPLAY_STATUS="REPLAY_STATUS_UNKNOWN";
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
function status(state,predicate,extra){var s={schema:STATUS_SCHEMA,state:state,predicate:predicate,action_eligible:false,authority_effect:"NONE"};if(extra)for(var k in extra)if(own(extra,k))s[k]=extra[k];s.replay_status=REPLAY_STATUS;return s;}
var HIDDEN_TEXT=/[\p{Cc}\p{Cf}\p{Cs}\p{Zl}\p{Zp}]/u;
var METADATA_TEXT_BOUNDS={provenance_ref:256,source_cursor:256,source_revision:256,grant_state:64};
function metadataDisplayable(p){for(var k in METADATA_TEXT_BOUNDS){if(own(p,k)){var v=p[k];if(v.trim().length===0||v.length>METADATA_TEXT_BOUNDS[k]||HIDDEN_TEXT.test(v))return false;}}return true;}
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
 // Provenance strings are shown on the capabilities card, panels and search hits; one that holds hidden characters
 // (control, format, surrogate, separator) or exceeds its bound could display as something else, so the status fails closed.
 if(!metadataDisplayable(provenance))return status("MALFORMED","PROJECTION_METADATA_NOT_DISPLAYABLE");
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
// Each capability family has its own KV projection. Given a list of projections, a descriptor is evaluated against
// the one projection whose schema it allows; no match leaves it NOT_OBSERVED, and two matches fail closed rather than
// letting one source stand in for another. A single projection keeps strict schema checking (MALFORMED on mismatch).
function sourceFor(d,projections){
 if(!Array.isArray(projections))return {projection:projections};
 var schemas=d&&Array.isArray(d.allowed_projection_schemas)?d.allowed_projection_schemas:[];
 var hits=projections.filter(function(p){return p&&typeof p==="object"&&schemas.indexOf(p.schema)>=0;});
 if(hits.length>1)return {ambiguous:true};
 return {projection:hits.length?hits[0]:null};
}
function evaluateAll(descriptors,projection,workspaceType,nowMs){
 if(!Array.isArray(descriptors))return [];
 return descriptors.map(function(d){var src=sourceFor(d,projection),s=src.ambiguous?(descriptorProblem(d)?status("DESCRIPTOR_REJECTED",descriptorProblem(d)):status("MALFORMED","PROJECTION_SOURCE_AMBIGUOUS")):evaluate(d,src.projection,workspaceType,nowMs);s.capability=d&&typeof d.capability==="string"?d.capability:"UNKNOWN";s.label=d&&typeof d.label==="string"?d.label:s.capability;s.projection_field=d&&typeof d.projection_field==="string"?d.projection_field:null;return s;});
}
function withholdsRows(s){return !s||WITHHELD.indexOf(s.state)>=0;}
root.StegVerseWorkspaceCapabilities=Object.freeze({reasons:Object.freeze(Object.assign({},REASONS)),descriptor_schema:DESCRIPTOR_SCHEMA,status_schema:STATUS_SCHEMA,descriptorProblem:descriptorProblem,evaluate:evaluate,evaluateAll:evaluateAll,withholdsRows:withholdsRows,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
