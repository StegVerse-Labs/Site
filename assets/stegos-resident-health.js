(function(root){
"use strict";
if(!root||!root.document)return;
if(root.StegOSResidentHealth)return;

var HEALTH_SCHEMA="stegverse.stegos.resident-health-report/v1";
var REPAIR_SCHEMA="stegverse.stegos.resident-repair-report/v1";
var STEGOS_SCOPE_PATH="/stegos-bootstrap/";
var STEGOS_ENTRY_PATH="/stegos-bootstrap/index.html";
var STEGOS_WORKER_SUFFIX="/stegos-bootstrap/service-worker.js";
var UI_ID="stegos-resident-health-card";
var lastReport=null;

function safeText(value){return value==null?"":String(value);}
function clone(value){try{return JSON.parse(JSON.stringify(value));}catch(_){return null;}}
function surface(){return /\/my-kv(?:\.html)?(?:$|[?#])/.test(root.location.pathname+root.location.search)?"MYKV":"STEGOS_OR_SITE";}
function capability(name){return !!root[name];}
function noAuthority(){return {authority_effect:"NONE",provider_operation_authorized:false,kv_mutation_authorized:false};}

function nodeStatus(){
  var api=root.StegVerseNodeContinuity;
  if(api&&typeof api.status==="function"){
    return Promise.resolve().then(function(){return api.status();}).then(function(state){
      var id=state&&state.registration&&state.registration.node_id?state.registration.node_id:null;
      return {source:"STEGVERSE_NODE_CONTINUITY",registered:!!(state&&state.registered===true&&id),node_id:id,raw:state||null};
    }).catch(function(error){return {source:"STEGVERSE_NODE_CONTINUITY",registered:false,node_id:null,error:safeText(error&&error.message||error)};});
  }
  var boot=root.StegOSWebBootstrap;
  if(boot&&typeof boot.readExistingNode==="function"){
    return Promise.resolve().then(function(){return boot.readExistingNode();}).then(function(node){
      return {source:"STEGOS_WEB_BOOTSTRAP",registered:!!(node&&node.node_id),node_id:node&&node.node_id||null,raw:node||null};
    }).catch(function(error){return {source:"STEGOS_WEB_BOOTSTRAP",registered:false,node_id:null,error:safeText(error&&error.message||error)};});
  }
  return Promise.resolve({source:"UNAVAILABLE",registered:false,node_id:null,reason:"NODE_STATUS_SURFACE_UNAVAILABLE"});
}

function runtimeReadiness(){
  var boot=root.StegOSWebBootstrap;
  if(boot&&typeof boot.probeOperationalReadiness==="function"){
    return Promise.resolve().then(function(){return boot.probeOperationalReadiness();}).then(function(report){
      return {source:"STEGOS_WEB_BOOTSTRAP",state:report&&report.state||"UNKNOWN",report:report||null};
    }).catch(function(error){return {source:"STEGOS_WEB_BOOTSTRAP",state:"BLOCKED",reason:safeText(error&&error.message||error)};});
  }
  var secure=root.isSecureContext===true;
  var idb=!!root.indexedDB;
  var crypto=!!(root.crypto&&root.crypto.subtle&&root.crypto.getRandomValues);
  return Promise.resolve({
    source:"CAPABILITY_ONLY",
    state:(secure&&idb&&crypto)?"READY_CAPABILITY_ONLY":"BLOCKED",
    report:{secure_context:secure,indexeddb:idb,webcrypto:crypto,authority_effect:"NONE"}
  });
}

function serviceWorkerHealth(){
  if(!(root.navigator&&root.navigator.serviceWorker&&typeof root.navigator.serviceWorker.getRegistration==="function")){
    return Promise.resolve({state:"UNAVAILABLE",scope:null,script_url:null,freshness:"UNAVAILABLE"});
  }
  var scopeUrl=new URL(STEGOS_SCOPE_PATH,root.location.origin).toString();
  return root.navigator.serviceWorker.getRegistration(scopeUrl).then(function(reg){
    if(!reg)return {state:"NOT_REGISTERED",scope:scopeUrl,script_url:null,freshness:"REPAIR_REQUIRED"};
    var worker=reg.active||reg.waiting||reg.installing||null;
    var script=worker&&worker.scriptURL||null;
    var canonical=!!(script&&script.indexOf(STEGOS_WORKER_SUFFIX)>=0);
    return {
      state:worker?"REGISTERED":"REGISTERED_NO_WORKER",
      scope:reg.scope||scopeUrl,
      script_url:script,
      canonical_script:canonical,
      freshness:canonical?"CANONICAL_SCRIPT_OBSERVED":"REPAIR_REQUIRED",
      update_available:!!reg.waiting
    };
  }).catch(function(error){return {state:"CHECK_FAILED",scope:scopeUrl,script_url:null,freshness:"UNKNOWN",reason:safeText(error&&error.message||error)};});
}

function deviceContinuityHealth(){
  var api=root.StegOSDeviceContinuity;
  if(api&&typeof api.readRoot==="function"){
    return Promise.resolve().then(function(){return api.readRoot();}).then(function(value){
      return {state:value&&value.device_continuity_id?"BOUND":"NOT_ESTABLISHED",device_continuity_id:value&&value.device_continuity_id||null,source:"STEGOS_DEVICE_CONTINUITY"};
    }).catch(function(error){return {state:"CHECK_FAILED",device_continuity_id:null,source:"STEGOS_DEVICE_CONTINUITY",reason:safeText(error&&error.message||error)};});
  }
  return Promise.resolve({state:"NOT_EXPOSED_ON_THIS_SURFACE",device_continuity_id:null,source:"UNAVAILABLE_WITHOUT_MUTATION"});
}

function transitionHealth(){
  var generated=root.StegVerseGeneratedInTr;
  var sync=root.StegVerseDeviceKVInTrSync;
  var connector=root.StegVerseInterlockConnector||root.StegVerseInterlock||null;
  return {
    intr_connector_available:!!(generated&&(typeof generated.buildIntent==="function"||typeof generated.canonical==="function")),
    device_kv_transport_available:!!(sync&&typeof sync.synchronizeMaterialization==="function"),
    interlock_surface_available:!!connector,
    state:(generated||connector)?"AVAILABLE":"NOT_EXPOSED_ON_THIS_SURFACE",
    authority_effect:"NONE_DIAGNOSTIC_ONLY"
  };
}

function knownKvRelationship(){
  var stateNode=root.document.getElementById("kv-state-2");
  var statusNode=root.document.getElementById("kv-status-2");
  if(stateNode||statusNode){
    var state=safeText(stateNode&&stateNode.textContent).trim();
    var detail=safeText(statusNode&&statusNode.textContent).trim();
    var verified=/done|verified|connected/i.test(state+" "+detail);
    return {
      state:verified?"KNOWN_VERIFIED_FROM_CURRENT_PAGE":"NO_VERIFIED_RELATIONSHIP_OBSERVED_ON_CURRENT_PAGE",
      host_class:"UNSPECIFIED",
      detail:detail||null,
      source:"CURRENT_MYKV_PAGE_STATE",
      query_emitted:false,
      authority_effect:"NONE"
    };
  }
  return {state:"NOT_EXPOSED_ON_THIS_SURFACE",host_class:"UNSPECIFIED",source:"LOCAL_VISIBLE_STATE_ONLY",query_emitted:false,authority_effect:"NONE"};
}

function classify(parts){
  var reasons=[];
  if(!parts.runtime||String(parts.runtime.state).indexOf("READY")!==0)reasons.push("LOCAL_RUNTIME_NOT_READY");
  if(!parts.node||parts.node.registered!==true)reasons.push("VALID_NODE_NOT_OBSERVED");
  if(!parts.worker||parts.worker.state!=="REGISTERED"||parts.worker.canonical_script!==true)reasons.push("STEGOS_SERVICE_WORKER_REPAIR_REQUIRED");
  if(parts.continuity&&parts.continuity.state==="CHECK_FAILED")reasons.push("DEVICE_CONTINUITY_CHECK_FAILED");
  return {state:reasons.length?"REPAIR_REQUIRED":"HEALTHY",repair_required:reasons.length>0,reasons:reasons};
}

function diagnose(){
  return Promise.all([runtimeReadiness(),nodeStatus(),serviceWorkerHealth(),deviceContinuityHealth()]).then(function(values){
    var parts={runtime:values[0],node:values[1],worker:values[2],continuity:values[3],transition:transitionHealth(),kv_relationship:knownKvRelationship()};
    var classification=classify(parts);
    var report={
      schema:HEALTH_SCHEMA,
      observed_at:new Date().toISOString(),
      surface:surface(),
      resident_install_health:classification.state,
      repair_required:classification.repair_required,
      repair_reasons:classification.reasons,
      runtime:parts.runtime,
      node:{source:parts.node.source,registered:parts.node.registered,node_id:parts.node.node_id,error:parts.node.error||null},
      device_continuity:parts.continuity,
      schema_freshness:{node_schema_loader_present:capability("StegOSNodeSchemaCompat")||capability("StegVerseNodeContinuity")||capability("StegOSWebBootstrap"),state:"LOADER_PRESENT_OR_RUNTIME_COMPATIBILITY_DELEGATED"},
      service_worker:parts.worker,
      governed_transition:parts.transition,
      kv_host_relationship:parts.kv_relationship,
      diagnostic_is_read_only:true,
      device_kv_query_emitted:false,
      provider_operation_authorized:false,
      kv_mutation_authorized:false,
      authority_effect:"NONE"
    };
    lastReport=report;
    render(report);
    try{root.dispatchEvent(new CustomEvent("stegos-resident-health",{detail:clone(report)}));}catch(_){ }
    return report;
  });
}

function preserveBaseline(report){
  return {
    node_id:report&&report.node&&report.node.node_id||null,
    kv_relationship:report&&report.kv_host_relationship?clone(report.kv_host_relationship):null
  };
}

function refreshWorker(){
  var boot=root.StegOSWebBootstrap;
  if(boot&&typeof boot.registerOfflineShell==="function"){
    return Promise.resolve().then(function(){return boot.registerOfflineShell();}).then(function(registrationResult){
      if(root.navigator&&root.navigator.serviceWorker&&typeof root.navigator.serviceWorker.getRegistration==="function"){
        return root.navigator.serviceWorker.getRegistration(new URL(STEGOS_SCOPE_PATH,root.location.origin).toString()).then(function(reg){
          if(reg&&typeof reg.update==="function")return reg.update().catch(function(){return null;}).then(function(){return registrationResult;});
          return registrationResult;
        });
      }
      return registrationResult;
    });
  }
  if(root.navigator&&root.navigator.serviceWorker&&typeof root.navigator.serviceWorker.getRegistration==="function"){
    return root.navigator.serviceWorker.getRegistration(new URL(STEGOS_SCOPE_PATH,root.location.origin).toString()).then(function(reg){
      if(reg&&typeof reg.update==="function")return reg.update().then(function(){return {state:"UPDATED_EXISTING_REGISTRATION",authority_effect:"NONE"};});
      return {state:"STEGOS_BOOTSTRAP_REQUIRED",authority_effect:"NONE"};
    });
  }
  return Promise.resolve({state:"STEGOS_BOOTSTRAP_REQUIRED",authority_effect:"NONE"});
}

function reuseOrEstablishNode(baseline){
  if(baseline&&baseline.node_id)return Promise.resolve({state:"EXISTING_NODE_PRESERVED",node_id:baseline.node_id});
  var boot=root.StegOSWebBootstrap;
  if(boot&&typeof boot.establishNode==="function"){
    return boot.establishNode().then(function(state){return {state:state&&state.reused?"EXISTING_NODE_REUSED":"NODE_ESTABLISHED_DURING_EXPLICIT_REPAIR",node_id:state&&state.node&&state.node.node_id||null};});
  }
  return Promise.resolve({state:"STEGOS_BOOTSTRAP_REQUIRED",node_id:null});
}

function repair(){
  return diagnose().then(function(before){
    if(!before.repair_required){
      return {schema:REPAIR_SCHEMA,state:"NO_REPAIR_REQUIRED",before:before,after:before,node_identity_preserved:true,kv_relationship_preserved:true,authority_effect:"NONE"};
    }
    var baseline=preserveBaseline(before);
    return refreshWorker().then(function(workerAction){
      return reuseOrEstablishNode(baseline).then(function(nodeAction){
        if(nodeAction.state==="STEGOS_BOOTSTRAP_REQUIRED"){
          return {
            schema:REPAIR_SCHEMA,state:"OWNER_STEGOS_BOOTSTRAP_REQUIRED",before:before,worker_action:workerAction,node_action:nodeAction,
            redirect:new URL(STEGOS_ENTRY_PATH+"?resident_repair=1",root.location.origin).toString(),
            node_identity_preserved:true,kv_relationship_preserved:true,authority_effect:"NONE"
          };
        }
        return diagnose().then(function(after){
          var nodePreserved=!baseline.node_id||after.node.node_id===baseline.node_id;
          if(!nodePreserved)throw new Error("FAIL_CLOSED: resident repair changed valid Node identity");
          var kvAfter=after.kv_host_relationship;
          var kvPreserved=JSON.stringify(baseline.kv_relationship||null)===JSON.stringify(kvAfter||null);
          if(!kvPreserved)throw new Error("FAIL_CLOSED: resident repair changed visible KV relationship state");
          return {
            schema:REPAIR_SCHEMA,state:after.repair_required?"REPAIR_PARTIAL":"REPAIR_COMPLETE",before:before,after:after,
            worker_action:workerAction,node_action:nodeAction,node_identity_preserved:true,kv_relationship_preserved:true,
            kv_create_called:false,kv_replace_called:false,kv_renumber_called:false,kv_migrate_called:false,kv_rehost_called:false,
            authority_effect:"NONE"
          };
        });
      });
    });
  }).then(function(result){render(result.after||result.before||lastReport,result);return result;});
}

function ensureCard(){
  var existing=root.document.getElementById(UI_ID);if(existing)return existing;
  var card=root.document.createElement("section");
  card.id=UI_ID;
  card.setAttribute("data-stegos-resident-health","true");
  card.style.cssText="margin:10px auto 16px;max-width:920px;padding:12px 14px;border:1px solid rgba(127,127,127,.35);border-radius:14px;background:rgba(18,30,45,.72);font:13px/1.45 -apple-system,BlinkMacSystemFont,Helvetica Neue,sans-serif";
  card.innerHTML='<div style="display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap"><div><strong>StegOS resident health</strong><div data-health-summary style="opacity:.78">Checking resident installation…</div></div><button type="button" data-health-repair hidden style="padding:8px 11px;border-radius:9px">Repair StegOS</button></div><details style="margin-top:8px"><summary>Diagnostic details</summary><pre data-health-details style="white-space:pre-wrap;word-break:break-word;max-height:240px;overflow:auto"></pre></details>';
  var nav=root.document.querySelector("nav");
  if(nav&&nav.parentNode)nav.parentNode.insertBefore(card,nav.nextSibling);else if(root.document.body)root.document.body.insertBefore(card,root.document.body.firstChild);
  var button=card.querySelector("[data-health-repair]");
  button.addEventListener("click",function(){
    button.disabled=true;
    repair().then(function(result){
      if(result&&result.state==="OWNER_STEGOS_BOOTSTRAP_REQUIRED"&&result.redirect)root.location.assign(result.redirect);
    }).catch(function(error){
      var summary=card.querySelector("[data-health-summary]");if(summary)summary.textContent="Repair failed closed: "+safeText(error&&error.message||error);
    }).then(function(){button.disabled=false;});
  });
  return card;
}

function render(report,repairResult){
  if(!root.document.body)return;
  var card=ensureCard();
  if(!report)return;
  var summary=card.querySelector("[data-health-summary]");
  var details=card.querySelector("[data-health-details]");
  var button=card.querySelector("[data-health-repair]");
  var nodeId=report.node&&report.node.node_id?" · "+report.node.node_id:"";
  if(summary)summary.textContent=report.resident_install_health+nodeId+(repairResult&&repairResult.state?" · "+repairResult.state:"");
  if(details)details.textContent=JSON.stringify(report,null,2);
  if(button)button.hidden=!report.repair_required;
  card.setAttribute("data-health-state",report.resident_install_health||"UNKNOWN");
}

function autoRun(){
  diagnose().catch(function(error){
    var card=ensureCard();var summary=card.querySelector("[data-health-summary]");if(summary)summary.textContent="Diagnostic failed closed: "+safeText(error&&error.message||error);
  });
}

root.StegOSResidentHealth=Object.freeze({
  schema:HEALTH_SCHEMA,
  diagnose:diagnose,
  repair:repair,
  render:render,
  last:function(){return clone(lastReport);},
  authority_effect:"NONE",
  diagnostic_emits_device_kv_query:false,
  repair_can_create_replace_renumber_migrate_rehost_kv:false
});

if(root.document.readyState==="loading")root.document.addEventListener("DOMContentLoaded",autoRun,{once:true});else root.setTimeout(autoRun,0);
})(window);
