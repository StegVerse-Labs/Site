(function(root){
"use strict";
var GOAL_TASK_ID="STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001";
var COSV="40000100100000";
var MANIFEST_TASK_ID="STEG-BROWSER-RUNTIME-MATERIALIZATION-REMEDIATION-001";
var DESTINATION="StegBrowser:ManifestInvocation";
var PAYLOAD_SCHEMA="stegverse.stegbrowser-universal-intr-invocation-binding/v1";
var RUNTIME_SUBSTRATE="BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE";
var RUNTIME_CLASS="EVENT_EPHEMERAL";
var STORAGE_KEY="stegverse.stegbrowser.manifest-runtime.latest.v1";
var WORKER_SOURCE="(function(){\n\"use strict\";\nfunction req(ok,msg){if(!ok)throw new Error(msg);}\nself.postMessage({type:\"BOOTED\"});\nself.onmessage=function(event){\n var m=event.data||{};\n if(m.type!==\"EXECUTE_STEGBROWSER_MANIFEST\")return;\n try{\n  var b=m.binding||{};\n  req(b.schema===\"stegverse.stegbrowser-universal-intr-invocation-binding/v1\",\"binding_schema_mismatch\");\n  req(b.goal_task_id===\"STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001\",\"goal_task_mismatch\");\n  req(b.cosv_task_vector===\"40000100100000\",\"cosv_mismatch\");\n  req(b.route_owner===\"STEGVERSE\",\"route_owner_mismatch\");\n  req(b.outbound_interlock_intr_endpoint===\"STEGVERSE_OWNED_INTR_EGRESS_ENDPOINT\",\"owned_endpoint_mismatch\");\n  req(b.far_end_receiver===\"STEGVERSE_OWNED_MIRROR_REFLECTOR\",\"owned_receiver_mismatch\");\n  req(b.expected_action===\"REFLECT_DECLARED_RECORDS_PACKET\",\"expected_action_mismatch\");\n  req(b.authority_effect===\"NONE_ROUTE_BINDING_ONLY\",\"binding_authority_mismatch\");\n  self.postMessage({type:\"STEGBROWSER_MANIFEST_EXECUTION_READY\",receipt:{\n    schema:\"stegverse.stegbrowser-event-ephemeral-execution-readiness/v1\",\n    state:\"RUNTIME_READY_FOR_WORKERCOORDINATOR\",\n    goal_task_id:b.goal_task_id,\n    cosv_task_vector:b.cosv_task_vector,\n    manifest_task_id:b.manifest_task_id,\n    manifest_sha256:b.manifest_sha256,\n    node_id:m.node_id,\n    interlock_id:m.interlock_id,\n    registration_receipt_sha256:m.registration_receipt_sha256,\n    lease_id:m.lease_id,\n    runtime_id:m.runtime_id,\n    runtime_substrate:\"BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE\",\n    runtime_class:\"EVENT_EPHEMERAL\",\n    destination:\"StegBrowser:ManifestInvocation\",\n    claim_or_fence_minted:false,\n    request_grants_execution_authority:false,\n    github_runtime_authority:\"NONE\",\n    credential_authority:\"TV/TVC\",\n    authority_effect:\"NONE_RUNTIME_MATERIALIZATION_ONLY\"\n  }});\n }catch(err){self.postMessage({type:\"STEGBROWSER_MANIFEST_BLOCKED\",error:String(err&&err.message||err)});}\n};\n}());\n
function req(ok,msg){if(!ok)throw new Error(msg);}
function canonical(v){if(v===null||typeof v!=="object")return JSON.stringify(v);if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";}
async function sha256(v){var bytes=new TextEncoder().encode(typeof v==="string"?v:canonical(v));var d=await crypto.subtle.digest("SHA-256",bytes);return "sha256:"+Array.from(new Uint8Array(d)).map(function(b){return b.toString(16).padStart(2,"0");}).join("");}
function normalizeEntry(entry){
 req(entry&&entry.schema==="stegos.node_intr_outbox_entry.v1","outbox_schema_mismatch");
 var r=entry.materialization_request||{};
 req(r.schema==="stegverse.universal-intr-materialization-request/v1","materialization_schema_mismatch");
 req(r.destination&&r.destination.boundary==="STEGOS_ECOSYSTEM","destination_boundary_mismatch");
 req(r.destination&&r.destination.subsystem===DESTINATION,"destination_subsystem_mismatch");
 req(r.request_grants_execution_authority===false,"request_authority_forbidden");
 req(r.claim_or_fence_minted===false,"claim_fence_forbidden");
 req(r.credential_authority==="TV/TVC","credential_authority_mismatch");
 req(r.github_token_runtime_authority==="NONE","github_runtime_authority_forbidden");
 return r;
}
function validateBinding(binding){
 req(binding&&binding.schema===PAYLOAD_SCHEMA,"binding_schema_mismatch");
 req(binding.goal_task_id===GOAL_TASK_ID,"goal_task_mismatch");
 req(binding.cosv_task_vector===COSV,"cosv_mismatch");
 req(binding.manifest_task_id===MANIFEST_TASK_ID,"manifest_task_mismatch");
 req(/^sha256:[0-9a-f]{64}$/.test(String(binding.manifest_sha256||"")),"manifest_hash_invalid");
 req(binding.route_owner==="STEGVERSE","route_owner_mismatch");
 req(binding.outbound_interlock_intr_endpoint==="STEGVERSE_OWNED_INTR_EGRESS_ENDPOINT","owned_endpoint_mismatch");
 req(binding.far_end_receiver==="STEGVERSE_OWNED_MIRROR_REFLECTOR","owned_receiver_mismatch");
 req(binding.far_end_receiver_role==="OWNED_MIRROR_REFLECTOR","owned_receiver_role_mismatch");
 req(binding.expected_action==="REFLECT_DECLARED_RECORDS_PACKET","expected_action_mismatch");
 req(binding.authority_effect==="NONE_ROUTE_BINDING_ONLY","binding_authority_mismatch");
}
async function materialize(input){
 var entry=input&&input.entry?input.entry:input;
 var r=normalizeEntry(entry);
 var binding=input&&input.binding;
 validateBinding(binding);
 var node=input&&input.node||{};
 req(node.node_id&&node.interlock_id&&node.registration_receipt_sha256,"node_identity_missing");
 var leaseId=input&&input.lease_id||("STB-LEASE-"+crypto.randomUUID());
 var runtimeId=input&&input.runtime_id||("STB-WEBRUNTIME-"+crypto.randomUUID());
 var worker=new Worker(URL.createObjectURL(new Blob([WORKER_SOURCE],{type:"text/javascript"})));
 var receipt=await new Promise(function(resolve,reject){
  var timer=setTimeout(function(){try{worker.terminate();}catch(_e){}reject(new Error("stegbrowser_event_ephemeral_timeout"));},10000);
  worker.onmessage=function(event){var m=event.data||{};if(m.type==="BOOTED"){worker.postMessage({type:"EXECUTE_STEGBROWSER_MANIFEST",binding:binding,node_id:node.node_id,interlock_id:node.interlock_id,registration_receipt_sha256:node.registration_receipt_sha256,lease_id:leaseId,runtime_id:runtimeId});return;}if(m.type==="STEGBROWSER_MANIFEST_EXECUTION_READY"){clearTimeout(timer);try{worker.terminate();}catch(_e){}resolve(m.receipt);return;}if(m.type==="STEGBROWSER_MANIFEST_BLOCKED"){clearTimeout(timer);try{worker.terminate();}catch(_e){}reject(new Error(m.error||"stegbrowser_manifest_blocked"));}};
  worker.onerror=function(e){clearTimeout(timer);try{worker.terminate();}catch(_e){}reject(e.error||new Error("stegbrowser_worker_error"));};
 });
 receipt.materialization_id=r.materialization_id;
 receipt.request_hash=r.request_hash;
 receipt.binding_sha256=await sha256(binding);
 receipt.runtime_binding_sha256=await sha256({goal_task_id:GOAL_TASK_ID,cosv_task_vector:COSV,manifest_sha256:binding.manifest_sha256,node_id:node.node_id,interlock_id:node.interlock_id,registration_receipt_sha256:node.registration_receipt_sha256,lease_id:leaseId,runtime_id:runtimeId,destination:DESTINATION});
 receipt.receipt_sha256=await sha256(receipt);
 var state={state:"RUNTIME_READY_FOR_WORKERCOORDINATOR",goal_task_id:GOAL_TASK_ID,cosv_task_vector:COSV,runtime_substrate:RUNTIME_SUBSTRATE,runtime_class:RUNTIME_CLASS,runtime_id:runtimeId,lease_id:leaseId,node_id:node.node_id,interlock_id:node.interlock_id,receipt:receipt};
 root.__STEGVERSE_STEGBROWSER_MANIFEST_RUNTIME__=state;
 try{localStorage.setItem(STORAGE_KEY,JSON.stringify(state));}catch(_e){}
 return state;
}
root.StegVerseStegBrowserManifestRuntime={GOAL_TASK_ID:GOAL_TASK_ID,COSV:COSV,MANIFEST_TASK_ID:MANIFEST_TASK_ID,DESTINATION:DESTINATION,RUNTIME_SUBSTRATE:RUNTIME_SUBSTRATE,RUNTIME_CLASS:RUNTIME_CLASS,materialize:materialize,validateBinding:validateBinding};
}(typeof self!=="undefined"?self:globalThis));
