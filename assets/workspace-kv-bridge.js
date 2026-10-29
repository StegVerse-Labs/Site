(function(root){
"use strict";
if(!root)return;
// Plain-language reason per kv-bridge predicate, for the explanation contract (.github#3106). Explanatory only.
var REASONS={
 "LOCAL_REHYDRATION_INTERFACE_NOT_AVAILABLE":"the interface that restores your existing device node in this browser is not available",
 "DEVICE_KV_RESULT_NOT_YET_MATERIALIZED":"your request was accepted and is held in this device's outbox, but its result has not been produced yet, so nothing is shown until it is",
 "DEVICE_KV_REQUEST_QUEUED_NOT_DELIVERED":"your request is held in this device's outbox and has not been delivered to your KnowledgeVault yet, so nothing is shown",
 "SOVEREIGN_INTR_INGRESS_TARGET_NOT_PROJECTED":"the destination that receives requests for your KnowledgeVault has not been published to this page, so the request stays in this device's outbox",
 "DEVICE_KV_RESULT_UNAVAILABLE":"your KnowledgeVault did not return a usable result for this request, so nothing is shown; the reason it gave is kept with this refusal",
 "WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD":"a delivered projection contains something shaped like a password, token or other credential, so it is not shown; inside an email projection only that projection is withheld, and credentials stay only in your SKAP Vault",
 "EMAIL_PROJECTION_ACCOUNT_INVALID":"the email projection is not in the shape your KnowledgeVault's email producer emits, so only the email projection is withheld",
 "EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT":"an email row or an account's latest entry has no admission receipt from your KnowledgeVault, so only the email projection is withheld",
 "EMAIL_PROJECTION_ADMIT_RECEIPT_STALE":"an email account's position does not match the admitted receipts it was built from, so only the email projection is withheld",
 "EMAIL_PROJECTION_ACCOUNTS_MIXED":"the email projection mixes messages between accounts or names one account twice, so only the email projection is withheld",
 "EMAIL_PROJECTION_RECORD_DUPLICATED":"an email account lists the same message or receipt more than once, which can mean a replay, and one copy is never chosen silently, so only the email projection is withheld",
 "EMAIL_PROJECTION_MESSAGE_UNADMITTED":"the email projection holds a message that was not admitted or that carries its content, so only the email projection is withheld",
 "EMAIL_PROJECTION_DIGEST_DRIFT":"the email projection was changed after your KnowledgeVault produced it, so only the email projection is withheld"
};
var RECORD_CLASS="WORKSPACE_PERSONAL_PROJECTION";
var TASKS_RECORD_CLASS="WORKSPACE_TASKS_PROJECTION";
var RESULT_SCHEMA="stegverse.device-kv.query-result-delivery/v1";
var RESULT_REQUEST_SCHEMA="stegverse.device-kv.query-result-request/v1";
var PROJECTION_SCHEMA="stegverse.kv.personal-workspace-projection/v1";
var TASKS_PROJECTION_SCHEMA="stegverse.kv.workspace-tasks-projection/v1";
var FAMILY_DELIVERY_SCHEMA="stegverse.kv.workspace-family-projections/v1";
var CHECKPOINT_DELIVERY_SCHEMA="stegverse.kv.workspace-continuity-checkpoint-delivery/v1";
var CHECKPOINT_DECISION_SCHEMA="stegverse.kv.workspace-continuity-checkpoint-decision/v1";
var RESERVED_FAMILY_SCHEMAS=[PROJECTION_SCHEMA,TASKS_PROJECTION_SCHEMA,"stegverse.kv.workspace-continuity-checkpoint/v1"];
// Each record class is one bounded DEVICE_KV query: its scope list, purpose and projection validator. The same node binding,
// InTr request, HB return and exact-recovery checks apply to every class; nothing here grants authority.
var QUERY_CLASSES={
 WORKSPACE_PERSONAL_PROJECTION:{scopes:["workspace_identity","principals","relationships","organizations","memberships","feed","assistant"],purpose:"Project the current owner's admitted Personal KnowledgeVault Workspace identity and relationship context.",justification:"Return only Workspace metadata explicitly present in the current Personal KV; no credential material or provider authority.",validate:validateProjection},
 WORKSPACE_TASKS_PROJECTION:{scopes:["tasks","commitments","timeline"],purpose:"Project the current owner's admitted Personal KnowledgeVault tasks and commitments.",justification:"Return only task and commitment rows explicitly present in the current Personal KV; no execution, credential material or provider authority.",validate:validateTasksProjection},
 WORKSPACE_FAMILY_PROJECTIONS:{scopes:["projections"],purpose:"Deliver the current owner's persisted capability-family KV projections to the Workspace page.",justification:"Return only family projections explicitly persisted in the current Personal KV, each with its own metadata; no credential material, provider operation or trade authority.",validate:validateFamilyDelivery},
 WORKSPACE_CONTINUITY_CHECKPOINT:{scopes:["checkpoint","decision"],purpose:"Deliver the current owner's stored Workspace continuity checkpoint and its transition decision.",justification:"Return only the stored checkpoint and the verifier's decision; nothing is anchored, verified or executed by this page.",validate:validateCheckpointDelivery}
};
function requireValue(ok,msg){if(!ok)throw new Error("FAIL_CLOSED: "+msg);}
function randomId(){var b=new Uint8Array(16);crypto.getRandomValues(b);return "SITE-WORKSPACE-KV-"+Array.from(b,x=>x.toString(16).padStart(2,"0")).join("");}
function hex(buf){return Array.from(new Uint8Array(buf),x=>x.toString(16).padStart(2,"0")).join("");}
function shaBytes(bytes){return crypto.subtle.digest("SHA-256",bytes).then(hex);}
function buildQuery(nodeId,recordClass){var c=QUERY_CLASSES[recordClass||RECORD_CLASS];return {
 schema_version:"kv.interlock.request.v1",operation:"REQUEST",request_id:randomId(),
 requester:{module:"Site",component:"Workspace"},
 purpose:c.purpose,
 record_class:recordClass||RECORD_CLASS,
 requested_scope:c.scopes.slice(),
 minimum_necessary_justification:c.justification,
 authority_ref:"stegos-node://"+nodeId,disclosure_mode:"BOUNDED_CONTEXT",selector:{workspace_type:"PERSONAL"}
};}
function postResult(target,lookup){
 var intr=root.StegVerseGeneratedInTr;requireValue(intr&&typeof intr.canonical==="function","canonical InTr connector unavailable");
 var text=intr.canonical(lookup),bytes=new TextEncoder().encode(text);
 return shaBytes(bytes).then(function(hash){return fetch(target.result_url,{method:"POST",mode:"cors",cache:"no-store",credentials:"omit",headers:{"Content-Type":"application/json","X-StegVerse-Transport":"InTr","X-StegVerse-Transport-Origin":"STEGOS_NODE_OUTBOX","X-StegVerse-Payload-SHA256":hash},body:text}).then(async function(r){return {status:r.status,body:await r.json().catch(()=>null)};});});
}
// ACTIONS BY MANIFEST (Task Registry invariant NO_EXTERNAL_MACHINE_AWAITING_AS_TRANSITION_PREDICATE): the request is
// already durably queued in the node outbox, so the result is looked up exactly once. A result that is not yet
// materialized is an actionable FAIL_CLOSED disposition naming the queued materialization, never a wait or retry loop.
// Organization Role conformance standard (.github docs/ORGANIZATION_ROLE_RUNTIME_REALITY_DEPLOYMENT.md): a non-ALLOW
// result carries failure_code, failed_predicate, required_evidence_or_repair, retry_entrypoint, owning_existing_goal
// and next_attempt; a bare not-ready or unavailable is not a finding.
var OWNING_GOAL="STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001",RETRY_ENTRYPOINT="StegVerseWorkspaceKVBridge.loadPersonalWorkspace (Site assets/workspace-kv-bridge.js)";
function actionable(predicate,repair,next,extra){return refusal(Object.assign({disposition:"FAIL_CLOSED",predicate:predicate,failure_code:predicate,failed_predicate:predicate,required_evidence_or_repair:repair,retry_entrypoint:RETRY_ENTRYPOINT,owning_existing_goal:OWNING_GOAL,next_attempt:next,authority_effect:"NONE"},extra||{}));}
function lookupResult(target,lookup){return postResult(target,lookup).then(function(r){if(r.status===200)return r.body;if(r.status===400&&r.body&&r.body.reason==="device_kv_result_not_ready")throw actionable("DEVICE_KV_RESULT_NOT_YET_MATERIALIZED","the resident DEVICE_KV consumer materializes the result of the queued request "+lookup.materialization_id,"the next WorkSpace load queues a new request and looks its result up once; nothing waits",{materialization_id:lookup.materialization_id,request_hash:lookup.request_hash});throw actionable("DEVICE_KV_RESULT_UNAVAILABLE","a result delivery for the queued request "+lookup.materialization_id+" from the DEVICE_KV result interface (it answered HTTP "+r.status+(r.body&&r.body.reason?" with reason "+r.body.reason:"")+")","the next WorkSpace load queues a new request and looks its result up once; nothing waits",{materialization_id:lookup.materialization_id,request_hash:lookup.request_hash,http_status:r.status,reason:(r.body&&typeof r.body.reason==="string")?r.body.reason:null});});}
function validateProjection(p){
 requireValue(p&&p.schema===PROJECTION_SCHEMA,"Personal Workspace projection schema invalid");
 requireValue(p.workspace_type==="PERSONAL","Personal Workspace projection type invalid");
 requireValue(["KV_WORKSPACE_PROJECTED","KV_WORKSPACE_EMPTY"].includes(p.state),"Personal Workspace projection state invalid");
 requireValue(p.credential_material_present===false&&p.provider_operation_authorized===false&&p.workspace_grants_authority===false&&p.authority_effect==="NONE","Personal Workspace projection authority invalid");
 for(var row of (p.principals||[]))requireValue(row.ai_label_required===(row.principal_type==="AI_ENTITY"),"AI label derivation mismatch");
 for(var org of (p.organizations||[]))requireValue(org.principal_type==="ORGANIZATION","organization principal type invalid");
 if(p.assistant)requireValue(p.assistant.principal_type==="AI_ENTITY"&&p.assistant.ai_label_required===true&&Array.isArray(p.assistant.roles)&&p.assistant.roles.includes("WORKSPACE_ASSISTANT"),"Workspace assistant identity invalid");
 return p;
}
function validateTasksProjection(p){
 requireValue(p&&p.schema===TASKS_PROJECTION_SCHEMA,"Workspace tasks projection schema invalid");
 requireValue(p.workspace_type==="PERSONAL","Workspace tasks projection type invalid");
 requireValue(["KV_TASKS_PROJECTED","KV_TASKS_EMPTY"].includes(p.state),"Workspace tasks projection state invalid");
 requireValue(p.credential_material_present===false&&p.provider_operation_authorized===false&&p.workspace_grants_authority===false&&p.action_authority==="NONE"&&p.authority_effect==="NONE","Workspace tasks projection authority invalid");
 requireValue(Array.isArray(p.tasks)&&Array.isArray(p.commitments)&&Array.isArray(p.timeline),"Workspace tasks projection rows invalid");
 for(var row of p.tasks.concat(p.commitments,p.timeline))requireValue(row&&typeof row==="object"&&row.action_eligible===false&&row.execution_requires_admitted_manifest===true,"Workspace tasks row claims eligibility");
 requireValue(p.projection_metadata&&p.projection_metadata.schema==="stegverse.kv.workspace-projection-metadata/v1","Workspace tasks projection metadata invalid");
 return p;
}
function nonAuthorizing(p,label){requireValue(p&&typeof p==="object"&&p.workspace_type==="PERSONAL",label+" type invalid");requireValue(p.credential_material_present===false&&p.provider_operation_authorized===false&&p.workspace_grants_authority===false&&p.action_authority==="NONE"&&p.authority_effect==="NONE",label+" authority invalid");requireValue(p.projection_metadata&&p.projection_metadata.schema==="stegverse.kv.workspace-projection-metadata/v1",label+" metadata invalid");}
// Site#1509 lane B (Goal StegVerse-org/.github#164): the consumer does not trust credential_material_present alone.
// Every key in a family delivery is checked at any depth after NFKC normalisation: a key with hidden or non-ASCII
// characters is refused outright (confusable spellings such as a Greek omicron cannot slip past), and the folded key
// (lowercase, separators removed) is substring-matched against credential words. String values are checked, unanchored,
// for bearer/basic authorization material, JWTs, GitHub tokens and private keys. The only credential-named fields
// allowed are the false credential flags and skap:// references (SKAP Vault alone holds credentials). Deliberate
// choice: any key containing "token" (token_count, tokens) is refused too; no shipped family projection uses one.
var FAMILY_RETRY_ENTRYPOINT="StegVerseWorkspaceKVBridge.loadPersonalProjections (Site assets/workspace-kv-bridge.js)",FAMILY_NEXT="the next WorkSpace load queues a new family request and evaluates the delivered projections again; nothing waits";
var SECRET_WORDS=["password","passwd","passphrase","passcode","pwd","secret","token","oauth","apikey","accesskey","privatekey","signingkey","sshkey","encryptionkey","bearer","cookie","authorization","credential","sessionkey","jwt","totp","mfaseed","mnemonic","recoverycode"];
var SECRET_VALUE=/\bbearer\s+[A-Za-z0-9\-._~+\/]{16,}|\bbasic\s+(?=[A-Za-z0-9+\/]*[0-9+\/])[A-Za-z0-9+\/]{12,}={0,2}|\beyJ[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}|\bgh[pousr]_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----/i;
var REF_KEYS=["credentialref","skapref","skapcredentialref"],FLAG_KEYS=["credentialmaterialpresent","credentialsecretpresentinkv"];
function familyExtra(extra){return Object.assign({retry_entrypoint:FAMILY_RETRY_ENTRYPOINT},extra||{});}
function nfkc(v){return String(v).normalize("NFKC");}
function foldKey(k){var n=nfkc(k);if(/[^\x21-\x7e]/.test(n))return null;return n.toLowerCase().replace(/[^a-z0-9]+/g,"");}
function secretPath(v,path,depth){
 if(depth>32)return path+" (nesting deeper than 32)";
 if(typeof v==="string")return SECRET_VALUE.test(nfkc(v).replace(/\p{Cf}/gu,""))?path:null;
 if(!v||typeof v!=="object")return null;
 if(Array.isArray(v)){for(var i=0;i<v.length;i++){var hit=secretPath(v[i],path+"["+i+"]",depth+1);if(hit)return hit;}return null;}
 for(var k in v){if(!Object.prototype.hasOwnProperty.call(v,k))continue;var n=foldKey(k),x=v[k],here=path+"."+(n===null?"<non-ASCII key>":k);
  if(n===null)return here;
  if(FLAG_KEYS.indexOf(n)>=0){if(x!==false)return here;continue;}
  if(REF_KEYS.indexOf(n)>=0){if(!(x===null||(typeof x==="string"&&SKAP_REF.test(x))))return here;continue;}
  for(var w=0;w<SECRET_WORDS.length;w++)if(n.indexOf(SECRET_WORDS[w])>=0)return here;
  var hit2=secretPath(x,here,depth+1);if(hit2)return hit2;}
 return null;
}
function secretRefusal(secret,extra){return actionable("WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD","the KV projection producer removes credential-shaped material; credentials stay in SKAP Vault and only skap:// references may be projected (found at "+secret+")",FAMILY_NEXT,familyExtra(Object.assign({secret_path:secret},extra||{})));}
// Email-family projections travel in the existing WORKSPACE_FAMILY_PROJECTIONS list; no email query class exists. The
// consumer is keyed to the lane A producer, continuity-vault-kit runtime/email_family_projection.py
// (stegverse.kv.email-family-projection/v1, PR #278): accounts {mapping_id, provider_id, mapping_state, skap_ref,
// cursor {sequence, head_receipt_id, chain_digest, provider_position}} and a top-level list of payload-free message rows
// {mapping_id, canonical_message_id, receipt_id, staged_content_hash, trust_state, payload_present, sequence}. It
// recomputes what the producer defines: each account's receipt chain (chain_digest = "sha256:" + sha256 of canonical
// {previous: <prior chain_digest or null>, receipt_id}, folded in sequence order; head_receipt_id is the last receipt)
// and the projection_digest. These are integrity checks only, not authentication: anyone can recompute them.
// A mapping_state other than SESSION_VERIFIED is accepted here; the panel withholds that mapping's rows. A receipt
// the cursor names but no row carries is ABSENT; a cursor that does not recompute from its rows is STALE. The receipt_id
// itself cannot be recomputed here (its material includes the ingress reason, which the projection does not carry).
// A failure inside an email projection withholds only that projection, with a six-field refusal readable through
// lastFamilyRefusals(); other family members stay deliverable. Cross-delivery replay stays REPLAY_STATUS_UNKNOWN.
var EMAIL_FAMILY_SCHEMA=/^stegverse\.kv\.email(?:-[a-z0-9]+)*-projection\/v[0-9]+$/;
var MAPPING_ID=/^kv-email:[0-9a-f]{64}$/,RECEIPT_ID=/^kv-email-receipt:[0-9a-f]{64}$/,MESSAGE_ID=/^kv-email-message:[0-9a-f]{64}$/,DIGEST=/^sha256:[0-9a-f]{64}$/,SKAP_REF=/^skap:\/\/\S+$/u;
function isRecord(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function nonEmpty(v){return typeof v==="string"&&v.trim().length>0;}
// Integers must be exact in JS: a provider_position beyond 2^53 cannot be represented, so it fails closed rather than
// being rounded. provider_position is display-only and never compared numerically here.
function isCount(v){return typeof v==="number"&&Number.isSafeInteger(v)&&v>=0;}
// Byte-identical to the producer's json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False).
function pyCanonical(v){if(Array.isArray(v))return "["+v.map(pyCanonical).join(",")+"]";if(v&&typeof v==="object")return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+pyCanonical(v[k]);}).join(",")+"}";return JSON.stringify(v);}
function pySha(v){return shaBytes(new TextEncoder().encode(pyCanonical(v))).then(function(h){return "sha256:"+h;});}
function validateEmailFamily(f){
 var extra={projection_schema:f.schema};
 var invalid=function(what){return actionable("EMAIL_PROJECTION_ACCOUNT_INVALID","the email-family projection exactly as runtime/email_family_projection.py emits it ("+what+")",FAMILY_NEXT,familyExtra(extra));};
 if(!Array.isArray(f.accounts)||!Array.isArray(f.messages))throw invalid("accounts and messages must be lists");
 var accounts=new Map();
 f.accounts.forEach(function(a,i){
  if(!isRecord(a)||typeof a.mapping_id!=="string"||!MAPPING_ID.test(a.mapping_id))throw invalid("account "+i+" has no kv-email mapping_id");
  if(accounts.has(a.mapping_id))throw actionable("EMAIL_PROJECTION_ACCOUNTS_MIXED","the producer emits each mailbox mapping exactly once; mapping "+a.mapping_id+" appears twice",FAMILY_NEXT,familyExtra(extra));
  if(!nonEmpty(a.provider_id)||!nonEmpty(a.mapping_state))throw invalid("mapping "+a.mapping_id+" has no provider_id or mapping_state");
  if(!(a.skap_ref===null||(typeof a.skap_ref==="string"&&SKAP_REF.test(a.skap_ref))))throw secretRefusal("$.accounts["+i+"].skap_ref",extra);
  var c=a.cursor;
  if(!isRecord(c)||!isCount(c.sequence)||!(c.head_receipt_id===null||(typeof c.head_receipt_id==="string"&&RECEIPT_ID.test(c.head_receipt_id)))||!(c.chain_digest===null||(typeof c.chain_digest==="string"&&DIGEST.test(c.chain_digest)))||!(c.provider_position===null||isCount(c.provider_position))||!(c.provider_cursor_ref===undefined||c.provider_cursor_ref===null||(typeof c.provider_cursor_ref==="string"&&DIGEST.test(c.provider_cursor_ref))))throw invalid("mapping "+a.mapping_id+" cursor is not {sequence, head_receipt_id, sha256 chain_digest, safe-integer provider_position, optional sha256 provider_cursor_ref}");
  accounts.set(a.mapping_id,{account:a,rows:[]});
 });
 var messageOwner=new Map(),receipts=new Set();
 f.messages.forEach(function(m,j){
  if(!isRecord(m)||typeof m.mapping_id!=="string"||typeof m.canonical_message_id!=="string"||!MESSAGE_ID.test(m.canonical_message_id)||typeof m.staged_content_hash!=="string"||!DIGEST.test(m.staged_content_hash)||!isCount(m.sequence))throw invalid("message "+j+" has no mapping_id, kv-email-message canonical_message_id, sha256 staged_content_hash or sequence");
  if(!accounts.has(m.mapping_id))throw actionable("EMAIL_PROJECTION_ACCOUNTS_MIXED","every message bound to a mailbox mapping listed in accounts; message "+j+" names an absent mapping",FAMILY_NEXT,familyExtra(extra));
  if(m.trust_state!=="TRUSTED_ADMITTED"||m.payload_present!==false)throw actionable("EMAIL_PROJECTION_MESSAGE_UNADMITTED","only payload-free TRUSTED_ADMITTED rows from an ADMIT decision; message "+j+" is not one",FAMILY_NEXT,familyExtra(extra));
  if(typeof m.receipt_id!=="string"||!RECEIPT_ID.test(m.receipt_id))throw actionable("EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT","the kv-email-receipt ADMIT receipt id on message "+j,FAMILY_NEXT,familyExtra(extra));
  if(messageOwner.has(m.canonical_message_id)){if(messageOwner.get(m.canonical_message_id)!==m.mapping_id)throw actionable("EMAIL_PROJECTION_ACCOUNTS_MIXED","each message under exactly one mailbox mapping; message "+j+" also appears under another mapping",FAMILY_NEXT,familyExtra(extra));throw actionable("EMAIL_PROJECTION_RECORD_DUPLICATED","each admitted message once per mapping; message "+j+" repeats one already listed",FAMILY_NEXT,familyExtra(extra));}
  if(receipts.has(m.receipt_id))throw actionable("EMAIL_PROJECTION_RECORD_DUPLICATED","each ADMIT receipt projected once; message "+j+" repeats a receipt",FAMILY_NEXT,familyExtra(extra));
  messageOwner.set(m.canonical_message_id,m.mapping_id);receipts.add(m.receipt_id);
  accounts.get(m.mapping_id).rows.push(m);
 });
 var checks=[];
 accounts.forEach(function(entry,mid){
  var c=entry.account.cursor,rows=entry.rows;
  rows.forEach(function(m,k){if(m.sequence!==k+1)throw actionable("EMAIL_PROJECTION_ADMIT_RECEIPT_STALE","rows of mapping "+mid+" in sequence order 1..n as the producer chains them",FAMILY_NEXT,familyExtra(extra));});
  if(c.head_receipt_id!==null&&!rows.some(function(m){return m.receipt_id===c.head_receipt_id;}))throw actionable("EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT","the ADMIT receipt "+c.head_receipt_id+" that the cursor of mapping "+mid+" names as its head",FAMILY_NEXT,familyExtra(extra));
  var last=rows.length?rows[rows.length-1].receipt_id:null;
  if(c.sequence!==rows.length||c.head_receipt_id!==last||(rows.length===0&&c.chain_digest!==null))throw actionable("EMAIL_PROJECTION_ADMIT_RECEIPT_STALE","a cursor for mapping "+mid+" whose sequence and head receipt match its admitted rows",FAMILY_NEXT,familyExtra(extra));
  checks.push(rows.reduce(function(prev,m){return prev.then(function(h){return pySha({previous:h,receipt_id:m.receipt_id});});},Promise.resolve(null)).then(function(h){if(h!==c.chain_digest)throw actionable("EMAIL_PROJECTION_ADMIT_RECEIPT_STALE","a cursor for mapping "+mid+" whose chain_digest recomputes from its admitted receipts",FAMILY_NEXT,familyExtra(extra));}));
 });
 return Promise.all(checks).then(function(){return pySha({schema:f.schema,workspace_type:f.workspace_type,accounts:f.accounts,messages:f.messages});}).then(function(d){if(d!==f.projection_digest)throw actionable("EMAIL_PROJECTION_DIGEST_DRIFT","the email-family projection unaltered; its projection_digest must recompute from accounts and messages",FAMILY_NEXT,familyExtra(extra));return f;});
}
// Family projections are returned as the list the page's capability contract evaluates; each must be a PERSONAL,
// non-authorizing projection with its own metadata, and no reserved class may hide inside the list. Envelope and
// structural failures refuse the whole delivery; a failure inside an email projection withholds only that projection.
var lastFamilyRefusals=[];
function validateFamilyDelivery(p){
 lastFamilyRefusals=[];
 requireValue(p&&p.schema===FAMILY_DELIVERY_SCHEMA,"Workspace family delivery schema invalid");
 requireValue(["KV_FAMILY_PROJECTIONS_PROJECTED","KV_FAMILY_PROJECTIONS_EMPTY"].includes(p.state),"Workspace family delivery state invalid");
 nonAuthorizing(p,"Workspace family delivery");
 requireValue(Array.isArray(p.projections),"Workspace family delivery rows invalid");
 var envelope={};for(var ek in p)if(Object.prototype.hasOwnProperty.call(p,ek)&&ek!=="projections")envelope[ek]=p[ek];
 var secret=secretPath(envelope,"$",0);
 if(secret)throw secretRefusal(secret);
 var seen=Object.create(null);
 p.projections.forEach(function(f,i){
  requireValue(f&&typeof f==="object"&&typeof f.schema==="string"&&/^stegverse\.kv\.[a-z0-9-]+-projection\/v[0-9]+$/.test(f.schema),"Workspace family projection schema invalid");
  requireValue(!RESERVED_FAMILY_SCHEMAS.includes(f.schema),"Workspace family projection schema reserved");
  requireValue(!seen[f.schema],"Workspace family projection schema ambiguous");seen[f.schema]=true;
  requireValue(f.workspace_type==="PERSONAL"&&f.authority_effect==="NONE"&&f.credential_material_present===false&&f.provider_operation_authorized===false&&f.workspace_grants_authority===false&&f.trade_authority_granted!==true,"Workspace family projection authority invalid");
  requireValue(f.projection_metadata&&f.projection_metadata.schema==="stegverse.kv.workspace-projection-metadata/v1"&&f.projection_metadata.workspace_type==="PERSONAL","Workspace family projection metadata invalid");
  if(!EMAIL_FAMILY_SCHEMA.test(f.schema)){var hit=secretPath(f,"$.projections["+i+"]",0);if(hit)throw secretRefusal(hit);}
 });
 var refusals=[];
 return Promise.all(p.projections.map(function(f,i){
  if(!EMAIL_FAMILY_SCHEMA.test(f.schema))return Promise.resolve(f);
  return Promise.resolve().then(function(){var hit=secretPath(f,"$.projections["+i+"]",0);if(hit)throw secretRefusal(hit,{projection_schema:f.schema});return validateEmailFamily(f);}).catch(function(e){if(e&&e.decision){refusals.push(e.decision);return null;}throw e;});
 })).then(function(list){lastFamilyRefusals=refusals;return list.filter(function(f){return f!==null;});});
}
// The checkpoint delivery is handed to the assistant continuity contract as {checkpoint, decision}; the page verifies
// nothing itself, and a delivery that claims verification or an ALLOW decision is refused.
function validateCheckpointDelivery(p){
 requireValue(p&&p.schema===CHECKPOINT_DELIVERY_SCHEMA,"Workspace checkpoint delivery schema invalid");
 requireValue(["KV_CHECKPOINT_PROJECTED","KV_CHECKPOINT_ABSENT"].includes(p.state),"Workspace checkpoint delivery state invalid");
 nonAuthorizing(p,"Workspace checkpoint delivery");
 requireValue(p.anchor_verified===false,"Workspace checkpoint delivery claims verification");
 if(p.state==="KV_CHECKPOINT_ABSENT"){requireValue(p.checkpoint===null&&p.decision===null,"Workspace checkpoint delivery absent state invalid");return null;}
 requireValue(p.checkpoint&&typeof p.checkpoint==="object"&&p.checkpoint.schema==="stegverse.kv.workspace-continuity-checkpoint/v1","Workspace checkpoint schema invalid");
 var d=p.decision;
 requireValue(d&&typeof d==="object"&&d.schema===CHECKPOINT_DECISION_SCHEMA&&d.authority_effect==="NONE"&&["DENY","FAIL_CLOSED"].includes(d.disposition)&&typeof d.predicate==="string"&&["UNKNOWN","REFUSED"].includes(d.replay_status),"Workspace checkpoint decision invalid");
 return {checkpoint:p.checkpoint,decision:d};
}
var lastNodeBinding=null;
function refusal(d){var e=new Error("FAIL_CLOSED: "+d.predicate);e.decision=d;return e;}
// WU2: the page never registers a device identity. A directly observed registration binds; otherwise only an admitted
// stegos.device_continuity_recovery_result.v1 (StegOS#347 owner) may rehydrate the retained node, and only through a
// node-continuity rehydration interface. Absent both, the Personal KV path fails closed with the work unit named.
function bindNode(node,options){
 var binding=root.StegVerseWorkspaceNodeBinding;requireValue(binding&&typeof binding.resolve==="function","Workspace node-binding contract unavailable");
 var recovery=options&&Object.prototype.hasOwnProperty.call(options,"recovery_result")?options.recovery_result:null;
 return node.status().then(function(s){return binding.resolve(s,recovery).then(function(d){
  lastNodeBinding=d;
  if(d.disposition!=="ALLOW")throw refusal(d);
  if(d.source==="DEVICE_LOCAL_REGISTRATION")return s;
  if(typeof node.rehydrateRegistration!=="function"){
   lastNodeBinding=Object.assign({},d,{disposition:"FAIL_CLOSED",predicate:"LOCAL_REHYDRATION_INTERFACE_NOT_AVAILABLE",rehydration_owner:"StegOS node continuity (assets/stegverse-node-continuity-impl.js)"});
   throw refusal(lastNodeBinding);
  }
  return node.rehydrateRegistration(recovery).then(function(){return node.status();}).then(function(s2){
   requireValue(s2&&s2.registered===true&&s2.registration&&s2.registration.node_id===d.node_id,"rehydrated registration does not match the admitted retained node");
   return s2;
  });
 });});
}
function loadPersonalWorkspace(options){return loadProjection(RECORD_CLASS,options);}
// WS-TASKS delivery: the same DEVICE_KV query path, bound to the WORKSPACE_TASKS_PROJECTION record class that the
// resident consumer serves from continuity-vault-kit runtime/workspace_tasks_projection.py.
function loadPersonalTasks(options){return loadProjection(TASKS_RECORD_CLASS,options);}
// P4 delivery: the list of persisted family projections (e.g. the CryptoBot portfolio) for the capability contract.
function loadPersonalProjections(options){return loadProjection("WORKSPACE_FAMILY_PROJECTIONS",options);}
// WS-ASSISTANT delivery: {checkpoint, decision} for the assistant continuity contract, or null when none is stored.
function loadAssistantCheckpoint(options){return loadProjection("WORKSPACE_CONTINUITY_CHECKPOINT",options);}
function loadProjection(recordClass,options){
 var cls=QUERY_CLASSES[recordClass];requireValue(!!cls,"Workspace record class not admitted");
 var intr=root.StegVerseGeneratedInTr,hb=root.StegVerseHBInTrCarrier,node=root.StegVerseNodeContinuity,sync=root.StegVerseDeviceKVInTrSync;
 requireValue(intr&&typeof intr.buildIntent==="function"&&typeof intr.buildMaterializationRequest==="function","generated DEVICE_KV connector unavailable");
 requireValue(hb&&typeof hb.buildBinding==="function"&&typeof hb.recoverSignal==="function","HB/InTr carrier unavailable");
 requireValue(node&&typeof node.status==="function"&&typeof node.queueIntrMaterializationRequest==="function","registered Node continuity unavailable");
 requireValue(sync&&typeof sync.synchronizeMaterialization==="function"&&typeof sync.loadTarget==="function"&&typeof sync.getDeliveryReceipt==="function","DEVICE_KV sync unavailable");
 return bindNode(node,options).then(function(s){
  var nodeId=s.registration.node_id,q=buildQuery(nodeId,recordClass),bytes=new TextEncoder().encode(intr.canonical(q));
  return intr.buildIntent("device-kv",bytes,"REQUEST",q.request_id).then(intent=>hb.buildBinding(intent.packet_id,intent.payload_hash).then(binding=>intr.buildMaterializationRequest("device-kv",intent,"inline://materialization_request.kv_request",binding,{kv_request:q}))).then(function(m){
   return node.queueIntrMaterializationRequest(m).then(()=>sync.synchronizeMaterialization(m.materialization_id)).then(()=>Promise.all([sync.getDeliveryReceipt(m.materialization_id),sync.loadTarget(recordClass)])).then(function(v){
    // Destination existence is sufficient; destination liveness is never a predicate (Organization Role conformance
    // standard, item 2). The target must exist (a projected result locator); whether its runtime was observed is not read.
    if(!(v[1]&&v[1].state==="CONFORMING_SOVEREIGN_INTR_INGRESS"&&typeof v[1].result_url==="string"&&v[1].result_url))throw actionable("SOVEREIGN_INTR_INGRESS_TARGET_NOT_PROJECTED","the StegOS node owner projects stegos-node/device-kv-intr-sync-target.json with the existing sovereign InTr ingress and result locators","the next WorkSpace load reads the projected target; the request is already held in the node outbox",{materialization_id:m.materialization_id});
    // The delivery receipt is the egress record of this transition; without it the request is still durably queued.
    if(!(v[0]&&v[0].network_delivery_observed===true))throw actionable("DEVICE_KV_REQUEST_QUEUED_NOT_DELIVERED","the node outbox delivers the queued request "+m.materialization_id+" to the projected ingress and records its delivery receipt","the next WorkSpace load delivers from the outbox and looks the result up once; nothing waits",{materialization_id:m.materialization_id});
    var lookup={schema:RESULT_REQUEST_SCHEMA,materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:nodeId,authority_effect:"NONE_RESULT_LOOKUP_ONLY"};
    return lookupResult(v[1],lookup).then(function(delivery){
     requireValue(delivery&&delivery.schema===RESULT_SCHEMA&&delivery.state==="RESULT_AVAILABLE","Workspace result delivery invalid");
     requireValue(delivery.materialization_id===m.materialization_id&&delivery.request_hash===m.request_hash&&delivery.node_id===nodeId,"Workspace result binding mismatch");
     requireValue(delivery.authority_effect==="NONE_RESULT_DELIVERY_ONLY"&&delivery.result_lookup_grants_authority===false,"Workspace result authority invalid");
     var response=delivery.response;
     requireValue(response&&response.schema==="stegverse.device-kv.query-response/v1"&&response.state==="QUERY_COMPLETE"&&response.record_class===recordClass,"Workspace response invalid");
     requireValue(response.query_request_id===q.request_id&&response.request_grants_authority===false&&response.response_grants_authority===false&&response.authority_effect==="NONE","Workspace response authority/binding invalid");
     return hb.recoverSignal(delivery.response_carrier_signal).then(function(recovered){
      return intr.sha256Bytes(recovered).then(function(hash){requireValue(hash===delivery.response_payload_hash,"Workspace HB return payload mismatch");var decoded=JSON.parse(new TextDecoder().decode(recovered));requireValue(intr.canonical(decoded)===intr.canonical(response),"Workspace exact response recovery mismatch");return cls.validate(response.projection);});
     });
    });
   });
  });
 });
}
root.StegVerseWorkspaceKVBridge=Object.freeze({reasons:Object.freeze(Object.assign({},REASONS)),bridge_kind:"DEVICE_KV_QUERY_RETURN",record_classes:Object.keys(QUERY_CLASSES),loadPersonalWorkspace:loadPersonalWorkspace,loadPersonalTasks:loadPersonalTasks,loadPersonalProjections:loadPersonalProjections,loadAssistantCheckpoint:loadAssistantCheckpoint,lastNodeBinding:function(){return lastNodeBinding;},lastFamilyRefusals:function(){return lastFamilyRefusals.slice();},authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
