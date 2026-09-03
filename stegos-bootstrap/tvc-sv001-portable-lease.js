"use strict";

(function (root) {
  var PACKAGE_SCHEMA="stegverse.tvc.sv001-portable-lease-package/v1";
  var STATE_SCHEMA="stegverse.tvc.sv001-portable-lease-state/v1";
  var WC_RECEIPT_SCHEMA="stegverse.workercoordinator-portable-checkout-receipt/v1";
  var LEASE_SCHEMA="stegverse.stegverse001.bounded-autonomy-lease/v1";
  var ISSUANCE_SCHEMA="stegverse.tvc.stegverse001-bounded-autonomy-portable-lease-issuance/v1";
  var TASK_ID="SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001";
  var WORKER_ID="stegverse001-bounded-autonomy-runtime-worker";
  var REQUEST_ID="TV-REQUEST-STEGVERSE001-BOUNDED-AUTONOMY-001";
  var REQUEST_HASH="sha256:c4b3e35d5ecf2246e0e082a591e3144bd61b32cb02133d12a89226cf362f4def";

  function fail(reason){throw new Error("FAIL_CLOSED: "+reason);}
  function canonicalize(value){
    if(value===null||typeof value!=="object"){return JSON.stringify(value);}
    if(Array.isArray(value)){return "["+value.map(canonicalize).join(",")+"]";}
    return "{"+Object.keys(value).sort().map(function(key){return JSON.stringify(key)+":"+canonicalize(value[key]);}).join(",")+"}";
  }
  function bytesToHex(bytes){var out="";for(var i=0;i<bytes.length;i+=1){out+=bytes[i].toString(16).padStart(2,"0");}return out;}
  function sha256Hex(value){
    var text=typeof value==="string"?value:canonicalize(value);
    return crypto.subtle.digest("SHA-256",new TextEncoder().encode(text)).then(function(d){return bytesToHex(new Uint8Array(d));});
  }
  function without(obj,key){var copy={};Object.keys(obj||{}).forEach(function(k){if(k!==key){copy[k]=obj[k];}});return copy;}
  function stamp(ms){
    var d=new Date(Math.floor(ms/1000)*1000);
    if(Number.isNaN(d.getTime())){fail("invalid issuance time");}
    return d.toISOString().replace(".000Z","Z");
  }
  function validatePackage(pkg){
    if(!pkg||pkg.schema!==PACKAGE_SCHEMA){fail("portable TVC package schema mismatch");}
    if(pkg.execution_surface!=="CURRENT_USER_IPHONE"){fail("portable TVC execution surface mismatch");}
    if(pkg.credential_authority!=="TV/TVC"||pkg.github_token_runtime_authority!=="NONE"){fail("TVC authority boundary drift");}
    if(pkg.second_user_operated_device_required!==false||pkg.always_on_external_host_required!==false){fail("external device dependency prohibited");}
    if(pkg.tv_request_git_blob_sha!=="94f37d7ac794e0028411681747db2a4f1e2c4806"){fail("TV request source blob mismatch");}
    if(pkg.tvc_policy_git_blob_sha!=="f2e902679ce7e53ce06efe703a16743656f41790"){fail("TVC policy source blob mismatch");}
    var p=pkg.policy||{},r=pkg.tv_request||{};
    if(p.credential_authority!=="TV/TVC"||p.github_actions_runtime_authority!=="NONE"){fail("TVC policy authority drift");}
    if(p.default_lifetime_minutes!==30||p.max_lifetime_minutes!==60||p.max_consequential_steps!==2||p.lease_consumption!=="SINGLE_AUTONOMY_CYCLE"){fail("TVC lease policy mismatch");}
    if(r.request_id!==REQUEST_ID||r.request_hash!==REQUEST_HASH||r.credential_authority!=="TV/TVC"||r.github_actions_runtime_authority!=="NONE"){fail("TV request identity/authority mismatch");}
    return sha256Hex(without(r,"request_hash")).then(function(hash){
      if("sha256:"+hash!==REQUEST_HASH){fail("TV request self-hash mismatch");}
      var allowed=(r.allowed_transition_classes||[]).slice().sort().join("|");
      var policyAllowed=(p.allowed_transition_classes||[]).slice().sort().join("|");
      if(allowed!==policyAllowed){fail("allowed transition scope mismatch");}
      var forbidden=r.forbidden_transition_classes||[];
      (p.forbidden_transition_floor||[]).forEach(function(item){if(forbidden.indexOf(item)===-1){fail("forbidden transition floor missing");}});
      return pkg;
    });
  }
  function validateWorkerCoordinatorReceipt(receipt){
    if(!receipt||receipt.schema!==WC_RECEIPT_SCHEMA){fail("WorkerCoordinator checkout receipt schema mismatch");}
    if(receipt.task_id!==TASK_ID||receipt.worker_id!==WORKER_ID){fail("WorkerCoordinator task/worker mismatch");}
    if(receipt.authority_domain!=="INDEPENDENT_TASK_CONTROL"||receipt.global_workercoordinator_authority!==true||receipt.stegos_device_task_authority!==false){fail("WorkerCoordinator authority mismatch");}
    if(receipt.execution_surface!=="CURRENT_USER_IPHONE"||receipt.credential_authority!=="TV/TVC"||receipt.github_token_runtime_authority!=="NONE"){fail("WorkerCoordinator execution/credential boundary mismatch");}
    if(!Number.isInteger(receipt.fencing_token)||receipt.fencing_token<=22){fail("WorkerCoordinator fresh fencing token required");}
    if(!receipt.claim_id||!/^SHWP-SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001-G[0-9]+$/.test(receipt.claim_id)){fail("WorkerCoordinator claim id invalid");}
    if(!receipt.receipt_sha256||!/^sha256:[a-f0-9]{64}$/.test(receipt.receipt_sha256)){fail("WorkerCoordinator receipt hash missing");}
    return sha256Hex(without(receipt,"receipt_sha256")).then(function(hash){
      if("sha256:"+hash!==receipt.receipt_sha256){fail("WorkerCoordinator receipt self-hash mismatch");}
      return receipt;
    });
  }
  function initialState(){
    return {
      schema:STATE_SCHEMA,
      state_sequence:0,
      active_lease:null,
      issuance_receipt:null,
      lease_consumption_state:null,
      last_workercoordinator_receipt_sha256:null,
      credential_authority:"TV/TVC",
      execution_surface:"CURRENT_USER_IPHONE",
      authority_effect:"TVC_PORTABLE_LEASE_STATE"
    };
  }
  function buildLease(pkg,wcReceipt,nowMs){
    var p=pkg.policy;
    var issued=stamp(nowMs);
    var expires=stamp(nowMs+p.default_lifetime_minutes*60*1000);
    return sha256Hex(REQUEST_HASH+"|"+issued).then(function(seedHash){
      var body={
        schema:LEASE_SCHEMA,
        lease_id:"SV001-LEASE-"+seedHash.slice(0,24),
        entity_id:"StegVerse-001",
        entity_alias:"Beta_Orionis",
        goal_id:"STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001",
        request_id:REQUEST_ID,
        request_hash:REQUEST_HASH,
        lease_state:"ACTIVE",
        issuer:"TV/TVC",
        issued_at:issued,
        expires_at:expires,
        allowed_transition_classes:(p.allowed_transition_classes||[]).slice(),
        forbidden_transition_classes:(p.forbidden_transition_floor||[]).slice(),
        max_consequential_steps:p.max_consequential_steps,
        lease_consumption:"SINGLE_AUTONOMY_CYCLE",
        receipt_required:true,
        denial_reachable_required:true,
        denial_reachable:true,
        repair_replanning_allowed:false,
        network_access_allowed:false,
        repository_writeback_allowed:false,
        financial_binding_allowed:false,
        credential_creation_allowed:false,
        self_accreditation_allowed:false,
        sovereign_authority_granted:false,
        credential_authority:"TV/TVC",
        github_actions_runtime_authority:"NONE",
        authority_effect:"BOUNDED_PREAUTHORIZED_TRANSITION_CLASSES_ONLY",
        workercoordinator_claim_id:wcReceipt.claim_id,
        workercoordinator_fencing_token:wcReceipt.fencing_token,
        workercoordinator_checkout_receipt_sha256:wcReceipt.receipt_sha256
      };
      return sha256Hex(body).then(function(hash){body.lease_hash="sha256:"+hash;return body;});
    });
  }
  function issue(pkg,wcReceipt,store,options){
    if(!store||typeof store.read!=="function"||typeof store.atomicCompareAndSwap!=="function"){fail("atomic TVC state store required");}
    var nowMs=options&&Number.isFinite(options.now_ms)?options.now_ms:Date.now();
    return validatePackage(pkg).then(function(){return validateWorkerCoordinatorReceipt(wcReceipt);}).then(function(){
      return store.read();
    }).then(function(existing){
      var state=existing||initialState();
      if(state.schema!==STATE_SCHEMA||state.credential_authority!=="TV/TVC"){fail("portable TVC state lineage mismatch");}
      var active=state.active_lease;
      if(active&&active.lease_state==="ACTIVE"&&state.lease_consumption_state!=="CONSUMED"){
        var expiry=Date.parse(active.expires_at);
        if(Number.isFinite(expiry)&&expiry>nowMs){fail("ACTIVE_LEASE_ALREADY_EXISTS");}
      }
      return buildLease(pkg,wcReceipt,nowMs).then(function(lease){
        var issuance={
          schema:ISSUANCE_SCHEMA,
          status:"ok",
          transition_id:"TVC_SV001_BOUNDED_AUTONOMY_LEASE_ISSUED",
          request_id:lease.request_id,
          request_hash:lease.request_hash,
          lease_id:lease.lease_id,
          lease_hash:lease.lease_hash,
          portable_state_namespace:"tvc-sv001-portable-lease-authority",
          issued_at:lease.issued_at,
          expires_at:lease.expires_at,
          single_cycle:true,
          credential_value_exposed:false,
          secret_values_present:false,
          github_actions_runtime_authority:"NONE",
          workercoordinator_checkout_receipt_sha256:wcReceipt.receipt_sha256,
          workercoordinator_claim_id:wcReceipt.claim_id,
          workercoordinator_fencing_token:wcReceipt.fencing_token,
          authority_effect:"BOUNDED_LEASE_ISSUANCE_ONLY"
        };
        return sha256Hex(issuance).then(function(hash){
          issuance.receipt_hash="sha256:"+hash;
          var next={
            schema:STATE_SCHEMA,
            state_sequence:Number(state.state_sequence||0)+1,
            active_lease:lease,
            issuance_receipt:issuance,
            lease_consumption_state:"AVAILABLE_SINGLE_CYCLE",
            last_workercoordinator_receipt_sha256:wcReceipt.receipt_sha256,
            credential_authority:"TV/TVC",
            execution_surface:"CURRENT_USER_IPHONE",
            authority_effect:"TVC_PORTABLE_LEASE_STATE"
          };
          return store.atomicCompareAndSwap(state,next).then(function(committed){
            if(committed!==true){fail("atomic TVC lease issuance lost race or stale state");}
            return {state:next,lease:lease,issuance_receipt:issuance};
          });
        });
      });
    });
  }
  function markConsumed(leaseId,executionReceiptHash,store){
    if(!leaseId||!executionReceiptHash){fail("lease consumption evidence required");}
    return store.read().then(function(state){
      if(!state||state.schema!==STATE_SCHEMA||!state.active_lease||state.active_lease.lease_id!==leaseId){fail("portable TVC lease state not found");}
      if(state.lease_consumption_state!=="AVAILABLE_SINGLE_CYCLE"){fail("lease not available for single-cycle consumption");}
      var next=Object.assign({},state,{
        state_sequence:Number(state.state_sequence||0)+1,
        lease_consumption_state:"CONSUMED",
        consumed_execution_receipt_sha256:executionReceiptHash,
        consumed_at:stamp(Date.now())
      });
      return store.atomicCompareAndSwap(state,next).then(function(committed){
        if(committed!==true){fail("atomic TVC lease consumption lost race or stale state");}
        return next;
      });
    });
  }

  root.StegVerseTVCPortableSv001Lease={
    packageSchema:PACKAGE_SCHEMA,
    stateSchema:STATE_SCHEMA,
    canonicalize:canonicalize,
    sha256Hex:sha256Hex,
    validatePackage:validatePackage,
    validateWorkerCoordinatorReceipt:validateWorkerCoordinatorReceipt,
    initialState:initialState,
    issue:issue,
    markConsumed:markConsumed
  };
}(typeof self!=="undefined"?self:globalThis));
