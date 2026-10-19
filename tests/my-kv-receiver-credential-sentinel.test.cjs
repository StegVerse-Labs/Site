// MyKV N-device receiver: declared-absence sentinels (credential_material_present / _included === false) are not
// credential fields. They must be false; any other credential_material key, or a true sentinel, stays forbidden.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
function assert(ok,msg){if(!ok)throw new Error(msg)}
const file=process.env.RECEIVER_UNDER_TEST||path.join(root,'assets/my-kv-n-device-kv-receiver.js');
const sb={addEventListener(){},console};sb.self=sb;vm.createContext(sb);vm.runInContext(fs.readFileSync(file,'utf8'),sb);
const R=sb.rejectSensitive;assert(typeof R==='function','rejectSensitive loaded');
const ok=(v,why)=>{try{R(v,'t');}catch(e){throw new Error(why+': '+e.message);}};
const refused=(v,why)=>{let threw=false;try{R(v,'t');}catch(e){threw=true;}assert(threw,why+' must be refused');};
// The receiver's own provider-request and set-projection shapes carry false sentinels and must pass.
ok({governance_state:'PENDING_INTERLOCK_INTR',credential_material_present:false,provider_operation_authorized:false},'provider request with false sentinel');
ok({private_content_included:false,credential_material_included:false,entries:[{credential_material_present:false}]},'set projection with false sentinels');
// A true or non-boolean sentinel is refused.
refused({credential_material_present:true},'true present sentinel');
refused({credential_material_included:'no'},'non-boolean included sentinel');
// Real credential fields stay forbidden, at any depth.
['credential_material','credential_material_ref','password','access_token','private_key','skap_credential_ref','intr_receipt_ref'].forEach(k=>refused({nested:{[k]:'x'}},k));
console.log('MY_KV_RECEIVER_CREDENTIAL_SENTINEL_PASS');
