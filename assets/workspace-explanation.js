// Universal user-facing explanation (stegverse.user-facing-explanation/v1), Site consumer of the canonical contract in
// StegVerse-Labs/.github (schemas/user-facing-explanation.v1.schema.json, scripts/user_facing_explanation.py). Builds
// the one versioned explanation artifact the WorkSpace page shows for a governed outcome: prose by default, plus a
// complete, self-contained JSON artifact a person can copy into any independent LLM. Scaled-up Human-in-the-Loop (HIL)
// experiment in actual ecosystem use; owner-reported research origin is recorded in the mirror handoff.
// Non-authoritative by construction: the artifact is a projection of a canonical disposition record. It never
// authorizes, executes, records, verifies or mutates anything; it never carries secrets; it never invents evidence; a
// remediation draft inside it is unsubmitted and non-authorizing. The canonical receipt, predicate and evidence it
// describes remain the only authority. This file performs no I/O, touches no storage and reads nothing from the browser.
(function(root){
"use strict";
if(!root)return;
var SCHEMA="stegverse.user-facing-explanation/v1";
var ECOSYSTEM_IDENTIFIER="STEGVERSE";
var EXPLANATION_VERSION="1.0.0";
var RECOGNITION_PROBE_LITERAL="STEGVERSE_ECOSYSTEM_KNOWLEDGE_PROBE_V1";
var RECOGNITION_PROBE_STATUS="CANDIDATE_NOT_CANONICAL";
var DISPOSITIONS=["ALLOW","DENY","FAIL_CLOSED","UNKNOWN"];
var OBSERVATIONS=["OBSERVED","NOT_AUTHENTICALLY_OBSERVED","UNKNOWN"];
var AUTHORITY_SOURCES=["TASK_REGISTRY","WORKERCOORDINATOR","INTERLOCK_INTR","MANIFEST","TV_TVC","KV_SKAP_VAULT","NONE"];
var EVIDENCE_KINDS=["RECEIPT_REF","PROVENANCE_REF","SOURCE_REF","PUBLIC_URL","DIGEST","NONE"];
var PREDICATE_RE=/^[A-Za-z0-9_:.-]{1,160}$/;
var SECRET_KEY_RE=/(token|secret|credential|password|passwd|private[_-]?key|api[_-]?key|bearer|cookie|client[_-]?secret)/i;
// Boolean flags that *describe* sanitization are not secret material.
var FLAG_KEYS=["secrets_present","credential_material_present"];
var SECRET_VALUE_RE=/(^Bearer\s+\S+|-----BEGIN [A-Z ]*PRIVATE KEY-----|^ghp_[A-Za-z0-9]{20,}|^sk-[A-Za-z0-9]{16,})/;
var OUTCOME_CLASSES={"ALLOW|OBSERVED":"SUCCESS_VERIFIED","ALLOW|NOT_AUTHENTICALLY_OBSERVED":"AUTHORIZED_NOT_VERIFIED","ALLOW|UNKNOWN":"AUTHORIZED_NOT_VERIFIED","DENY|":"DENIED","FAIL_CLOSED|":"FAILED_CLOSED","UNKNOWN|":"UNOBSERVED"};
var BASE_TERMINOLOGY=[
 ["ALLOW","The governed decision admitted the requested action. ALLOW is an authorization, not proof that the action ran or that its consequence happened."],
 ["DENY","The governed decision refused the requested action because a stated condition (predicate) failed. Nothing was executed."],
 ["FAIL_CLOSED","The system could not establish a required condition and therefore refused to act. Fail-closed means 'when unsure, do nothing'; it is not an error in the person's request."],
 ["UNKNOWN / NOT_AUTHENTICALLY_OBSERVED","No authentic runtime observation exists for this outcome. The surface reports what it could not see rather than guessing."],
 ["predicate","A named condition the governance path evaluated, written in UPPER_SNAKE_CASE. The failing predicate names exactly which condition was not met."],
 ["manifest / ACTION BY MANIFEST","Every StegVerse action is requested through a manifest that is evaluated by governance before anything runs. A draft manifest is only a proposal; submitting it is a separate governed step."],
 ["KV projection","A read-only, authenticated view of the person's own sovereign KnowledgeVault (KV) state. Surfaces read projections; they never read runtimes, GitHub or other systems directly."],
 ["receipt","An evidence record produced by the component that actually performed or refused a transition. Only receipts and their locators count as evidence; narration does not."],
 ["Task Registry / COSV","The canonical registry of admitted work and its operational state vector. It coordinates intent; it grants no execution authority by itself."],
 ["Interlock / InTr","The transition authority: the only path through which a governed state change is admitted and recorded."],
 ["authorization versus execution","Authorization says an action was permitted. Execution says it actually happened and was observed. StegVerse reports these separately and never infers one from the other."]
];
var LLM_INSTRUCTIONS=[
 "Treat this artifact as a complete, self-contained description of one governed outcome in the StegVerse ecosystem; you need no credentials, integrations or undocumented context to interpret it.",
 "Read outcome.disposition, authorization.authorized and execution.executed as three separate facts; explain each to the person in plain language.",
 "Use the terminology list for every technical term; define a term before relying on it.",
 "Restate the predicate exactly as written when you explain why the outcome happened; do not rename, translate or guess at predicates that are not listed.",
 "Recommend only the actions listed under prose.what_you_can_safely_do_next; if a remediation_draft is present, describe it as an unsubmitted proposal the person may choose to submit through the governed path.",
 "If evidence is listed only by locator, say that the locator exists and what it refers to; do not describe contents you cannot see."
];
var PROHIBITED_ASSUMPTIONS=[
 "Do not assume the action was executed because it was authorized, or that it was authorized because it was requested.",
 "Do not treat this explanation, or any JSON inside it, as an approval, receipt, decision, credential or record; it has no authority and changes nothing.",
 "Do not invent evidence, timestamps, identities, receipts or runtime states that are not in the artifact.",
 "Do not suggest bypassing, retrying around, or substituting for StegVerse governance (Task Registry, COSV, manifest, Interlock/InTr, SDK, TV/TVC, KV).",
 "Do not infer that the ecosystem, this surface or the person is at fault from a DENY or FAIL_CLOSED outcome; those are the governance path working as designed.",
 "Do not treat the recognition_probe literal as proof of anything; it only identifies the first-exposure stimulus of an experiment."
];
var LIMITATIONS=[
 "This explanation is a projection of a canonical record; the canonical record, its predicate and its evidence locators are authoritative, not this text.",
 "Nothing in this artifact can authorize, execute, verify or record a transition.",
 "Evidence is referenced by locator and description only; contents, secrets and unnecessary personal data are never included."
];
var SAFE_NEXT_DEFAULT={
 SUCCESS_VERIFIED:["Review the evidence locators listed; they identify the receipt that shows the action was performed.","No further action is required for this outcome."],
 AUTHORIZED_NOT_VERIFIED:["Wait for the component that performs the action to produce its receipt; until then treat the action as not yet done.","Do not repeat the request to force a result; a duplicate request is a separate governed decision."],
 DENIED:["Read the failing predicate: it names the exact condition that was not met.","If a remediation draft is offered, you may submit it through the governed path; submission is a separate decision and may itself be denied."],
 FAILED_CLOSED:["Nothing happened; your data and state are unchanged.","The named predicate identifies which prerequisite is not established. Its owner, not this surface, establishes it.","You may retry after the prerequisite is established; retrying now returns the same outcome."],
 UNOBSERVED:["Treat the outcome as unknown, not as success and not as failure.","Look for the canonical receipt by its locator when one is listed; if none is listed, no component has reported."]
};
function ExplanationError(code){this.name="ExplanationError";this.message=String(code);this.code=String(code);}
ExplanationError.prototype=Object.create(Error.prototype);
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function isBlank(v){return typeof v!=="string"||v.trim()==="";}
function has(v){return v!==undefined&&v!==null;}
function fail(code){throw new ExplanationError(code);}
function require_(condition,code){if(!condition)fail(code);}
function rejectSecrets(value,path){
 path=path||"";
 if(isObject(value)){
  Object.keys(value).forEach(function(key){
   var inner=value[key];
   if(FLAG_KEYS.indexOf(key)>=0&&typeof inner==="boolean")return;
   if(SECRET_KEY_RE.test(String(key)))fail("secret_material_present:"+(path?path+".":"")+String(key));
   rejectSecrets(inner,(path?path+".":"")+String(key));
  });
 }else if(Array.isArray(value)){
  value.forEach(function(inner,index){rejectSecrets(inner,path+"["+index+"]");});
 }else if(typeof value==="string"&&SECRET_VALUE_RE.test(value))fail("secret_material_present:"+(path||"<root>"));
}
function str(value,code){require_(!isBlank(value),code);return value;}
function predicate_(value,code){require_(typeof value==="string"&&PREDICATE_RE.test(value),code);return value;}
function evidence_(items){
 require_(!has(items)||Array.isArray(items),"evidence_invalid");
 var out=[];
 (items||[]).forEach(function(item){
  require_(isObject(item),"evidence_item_invalid");
  var kind=item.kind;
  require_(EVIDENCE_KINDS.indexOf(kind)>=0,"evidence_kind_invalid");
  var ref=has(item.ref)?item.ref:null;
  require_(ref===null||!isBlank(ref),"evidence_ref_invalid");
  require_(!(kind!=="NONE"&&ref===null),"evidence_ref_required_for_kind:"+String(kind));
  out.push({kind:kind,ref:ref,description:str(item.description,"evidence_description_required"),sanitized:true});
 });
 return out;
}
function remediation_(draft){
 if(!has(draft))return null;
 require_(isObject(draft),"remediation_draft_invalid");
 require_(draft.submitted===false,"remediation_draft_must_be_unsubmitted");
 require_(draft.manifest_admitted===false,"remediation_draft_must_not_be_admitted");
 require_(draft.authority_effect==="NONE_REQUEST_ONLY"||draft.authority_effect==="NONE","remediation_draft_must_be_non_authorizing");
 require_(draft.disposition!=="ALLOW","remediation_draft_must_not_carry_allow");
 var copy={};Object.keys(draft).forEach(function(k){copy[k]=draft[k];});
 return {submitted:false,manifest_admitted:false,authority_effect:"NONE_REQUEST_ONLY",non_authorizing:true,draft:copy};
}
function prose_(outcomeClass,action,predicate,authoritySource,why,evidence,nextSteps,draftPresent){
 var ev=evidence.length?"Evidence is referenced by locator: "+evidence.map(function(e){return e.description+(e.ref?" ("+e.ref+")":"");}).join("; ")+".":"No evidence record is referenced for this outcome; nothing has been produced by a component that performs or refuses this action.";
 var defaultReason={
  SUCCESS_VERIFIED:"the condition "+predicate+" was satisfied and the performing component reported its receipt",
  AUTHORIZED_NOT_VERIFIED:"the condition "+predicate+" was satisfied, but no receipt from the performing component has been observed",
  DENIED:"the condition "+predicate+" failed",
  FAILED_CLOSED:"the prerequisite named by "+predicate+" is not established, and the system never acts on an unestablished prerequisite",
  UNOBSERVED:"no authentic observation reached this surface; the reported condition is "+predicate
 }[outcomeClass];
 var reason=why||defaultReason;
 var what,summary,authorized,executed;
 if(outcomeClass==="SUCCESS_VERIFIED"){
  what="The request '"+action+"' was authorized and its execution was observed.";
  summary="Succeeded and verified.";
  authorized="The action '"+action+"' was authorized by "+authoritySource+" under the condition "+predicate+".";
  executed="The action was executed and its consequence was observed by the component that performed it.";
 }else if(outcomeClass==="AUTHORIZED_NOT_VERIFIED"){
  what="The request '"+action+"' was authorized, but no authentic observation of its execution exists yet.";
  summary="Authorized; execution not verified.";
  authorized="The action '"+action+"' was authorized by "+authoritySource+" under the condition "+predicate+".";
  executed="Nothing is known to have been executed: no receipt from the performing component has been observed. Authorization is not execution.";
 }else if(outcomeClass==="DENIED"){
  what="The request '"+action+"' was refused.";
  summary="Denied; nothing was executed.";
  authorized="Nothing was authorized. The governed decision returned DENY because "+predicate+" failed.";
  executed="Nothing was executed and no state changed.";
 }else if(outcomeClass==="FAILED_CLOSED"){
  what="The request '"+action+"' could not be evaluated because a required prerequisite is not established, so the system refused to act.";
  summary="Failed closed; nothing was executed.";
  authorized="Nothing was authorized. The governance path returned FAIL_CLOSED on "+predicate+", which names the missing prerequisite.";
  executed="Nothing was executed and no state changed. Failing closed is the designed behaviour when a prerequisite is missing, not a fault in the request.";
 }else{
  what="The outcome of the request '"+action+"' is unknown: no authentic observation of a decision or an execution exists.";
  summary="Unknown; not success, not failure.";
  authorized="No authorization is known. The reported condition is "+predicate+".";
  executed="No execution is known. Treat the action as not done until a receipt is observed.";
 }
 var steps=nextSteps&&nextSteps.length?nextSteps.slice():SAFE_NEXT_DEFAULT[outcomeClass].slice();
 if(draftPresent)steps.push("An unsubmitted remediation draft is attached; it proposes nothing until you submit it through the governed path, where it receives its own decision.");
 return {what_happened:what,why:"Because "+reason+".",outcome_summary:summary,what_was_authorized:authorized,what_was_executed:executed,what_evidence_exists:ev,what_you_can_safely_do_next:steps,limitations:LIMITATIONS.slice()};
}
function isFalsy(v){return v===undefined||v===null||v===false||v===0||v===""||(Array.isArray(v)&&v.length===0)||(isObject(v)&&Object.keys(v).length===0);}
// Project a canonical outcome record into the explanation artifact. ``record`` is producer-supplied and already
// canonical; only whitelisted fields are read, so unnecessary personal data never reaches the artifact. Secrets
// anywhere in the record or surface descriptor abort the build. The surface descriptor is checked against the
// schema's surface requirements here because this consumer has no separate validator step.
function buildExplanation(record,surface,terminology){
 require_(isObject(record),"record_invalid");
 require_(isObject(surface),"surface_invalid");
 rejectSecrets(record);
 rejectSecrets(surface);
 require_(!isBlank(surface.repository),"surface_repository_required");
 require_(!isBlank(surface.surface_id),"surface_id_required");
 require_(!("surface_version" in surface)||typeof surface.surface_version==="string","surface_version_invalid");
 var disposition=record.disposition;
 require_(DISPOSITIONS.indexOf(disposition)>=0,"disposition_invalid");
 var predicate=predicate_(record.predicate,"predicate_invalid");
 var predicates=isFalsy(record.predicates)?[predicate]:record.predicates;
 require_(Array.isArray(predicates)&&predicates.every(function(p){return typeof p==="string"&&PREDICATE_RE.test(p);}),"predicates_invalid");
 if(predicates.indexOf(predicate)<0)predicates=[predicate].concat(predicates);
 predicates=predicates.filter(function(p,i,arr){return arr.indexOf(p)===i;});
 var action=str(record.requested_action,"requested_action_required");
 var authoritySource=record.authority_source===undefined?"NONE":record.authority_source;
 require_(AUTHORITY_SOURCES.indexOf(authoritySource)>=0,"authority_source_invalid");
 var observation=record.consequence_observation===undefined?"UNKNOWN":record.consequence_observation;
 require_(OBSERVATIONS.indexOf(observation)>=0,"consequence_observation_invalid");
 if(disposition!=="ALLOW")require_(observation!=="OBSERVED","non_allow_cannot_observe_consequence");
 var evidence=evidence_(record.evidence);
 if(disposition==="ALLOW"&&observation==="OBSERVED")require_(evidence.some(function(e){return e.kind==="RECEIPT_REF"||e.kind==="PROVENANCE_REF"||e.kind==="DIGEST";}),"observed_execution_requires_receipt_evidence");
 var outcomeClass=OUTCOME_CLASSES[disposition+"|"+(disposition==="ALLOW"?observation:"")];
 var authorized=disposition==="ALLOW";
 var executed=disposition==="ALLOW"&&observation==="OBSERVED";
 var executionState=executed?"VERIFIED":(authorized?"NOT_VERIFIED":"NOT_EXECUTED");
 var why=has(record.why)?record.why:null;
 require_(why===null||!isBlank(why),"why_invalid");
 var nextSteps=has(record.safe_next_steps)?record.safe_next_steps:null;
 require_(nextSteps===null||(Array.isArray(nextSteps)&&nextSteps.every(function(s){return !isBlank(s);})),"safe_next_steps_invalid");
 var draft=remediation_(record.remediation_draft);
 var canonicalRef=has(record.canonical_record_ref)?record.canonical_record_ref:null;
 require_(canonicalRef===null||!isBlank(canonicalRef),"canonical_record_ref_invalid");
 var extra=has(terminology)?terminology:[];
 require_(Array.isArray(extra)&&extra.every(function(t){return Array.isArray(t)&&t.length===2;}),"terminology_invalid");
 var terms=BASE_TERMINOLOGY.concat(extra.map(function(t){return [t[0],t[1]];}));
 var observationState=disposition==="ALLOW"?observation:(disposition==="UNKNOWN"?"UNKNOWN":"NOT_AUTHENTICALLY_OBSERVED");
 var surf={};["repository","surface_id","surface_version"].forEach(function(k){if(k in surface)surf[k]=surface[k];});
 var artifact={
  schema:SCHEMA,
  ecosystem_identifier:ECOSYSTEM_IDENTIFIER,
  explanation_type:"OUTCOME_EXPLANATION",
  explanation_version:EXPLANATION_VERSION,
  surface:surf,
  outcome:{disposition:disposition,observation_state:observationState,outcome_class:outcomeClass,predicate:predicate,predicates:predicates,canonical_record_ref:canonicalRef},
  authorization:{authorized:authorized,requested_action:action,authority_source:authoritySource},
  execution:{executed:executed,execution_state:executionState,consequence_observation:observationState},
  prose:prose_(outcomeClass,action,predicate,authoritySource,why,evidence,nextSteps,draft!==null),
  terminology:terms.map(function(t){return {term:t[0],definition:t[1]};}),
  evidence:evidence,
  remediation_draft:draft,
  llm_interpretation:{instructions:LLM_INSTRUCTIONS.slice(),prohibited_assumptions:PROHIBITED_ASSUMPTIONS.slice(),self_contained:true},
  authority:{authority_effect:"NONE",explanation_is_non_authoritative:true,canonical_record_mutation:false,alternate_governance_path:false},
  sanitization:{secrets_present:false,personal_data_minimized:true,invented_evidence:false},
  recognition_probe:{literal:RECOGNITION_PROBE_LITERAL,status:RECOGNITION_PROBE_STATUS,note:"Identifies the first-exposure stimulus of the scaled-up HIL experiment; echoing it proves nothing."}
 };
 if(typeof record.produced_at==="string"&&record.produced_at)artifact.produced_at=record.produced_at;
 require_(JSON.stringify(artifact).length>0,"artifact_unserializable");
 return artifact;
}
// Never throws: an outcome that cannot be explained without breaking an invariant yields a FAIL_CLOSED refusal object.
function build(record,surface,terminology){
 try{return buildExplanation(record,surface,terminology);}
 catch(error){return {schema:SCHEMA,disposition:"FAIL_CLOSED",predicate:"EXPLANATION_NOT_BUILDABLE",reason:error&&error.message?String(error.message):String(error)};}
}
// Default presentation: prose only, no predicates or JSON as the primary experience. Same layout as the reference
// render_prose; returns "" for anything that is not a built artifact.
function prose(artifact){
 if(!isObject(artifact)||!isObject(artifact.prose))return "";
 var p=artifact.prose;
 var lines=["What happened: "+p.what_happened,"Why: "+p.why,"Outcome: "+p.outcome_summary,"What was authorized: "+p.what_was_authorized,"What was executed: "+p.what_was_executed,"What evidence exists: "+p.what_evidence_exists,"What you can safely do next:"];
 (p.what_you_can_safely_do_next||[]).forEach(function(s){lines.push("  - "+s);});
 lines.push("Limitations:");
 (p.limitations||[]).forEach(function(s){lines.push("  - "+s);});
 return lines.join("\n")+"\n";
}
root.StegVerseWorkspaceExplanation=Object.freeze({schema:SCHEMA,explanation_version:EXPLANATION_VERSION,recognition_probe_literal:RECOGNITION_PROBE_LITERAL,authority_effect:"NONE",build:build,prose:prose});
}(typeof globalThis!=="undefined"?globalThis:this));
