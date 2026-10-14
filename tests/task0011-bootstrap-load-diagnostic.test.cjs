const fs=require('fs');
const assert=require('assert');

const bootstrap=fs.readFileSync('stegos-bootstrap/current-iphone-testflight-bootstrap.js','utf8');
const ipa=fs.readFileSync('stegos-bootstrap/current-iphone-unsigned-ipa-materializer.js','utf8');
const wasm=fs.readFileSync('stegos-bootstrap/current-iphone-wasm-materializer.js','utf8');

for(const marker of [
  'current_iphone_testflight_bootstrap:${stage}:${reason}',
  'projection_validation',
  'unsigned_ipa_materialization',
  'current_iphone_signing',
  'tvc_upload_request_build',
  'tvc_native_build_upload'
]) assert(bootstrap.includes(marker), marker);

// The IPA materializer builds its load diagnostics from a label ("manifest" or "ipa"), so assert the emitted
// reasons behaviourally rather than as source literals.
const ipaDiagnostics=(async()=>{
  const mod=await import(require('path').join(__dirname,'..','stegos-bootstrap','current-iphone-unsigned-ipa-materializer.js'));
  const reason=(fetchImpl)=>mod.loadValidatedCurrentIphoneUnsignedIpa({fetchImpl}).then(()=>'',e=>String(e&&e.message));
  const down=()=>Promise.reject(new Error('offline'));
  const status=(code)=>()=>Promise.resolve({ok:false,status:code});
  let calls=0;const manifestOkIpa=(next)=>()=>(++calls===1?Promise.resolve({ok:true,status:200}):next());
  assert((await reason(down)).includes('manifest_network_load_failed:offline'),'manifest_network_load_failed');
  assert((await reason(status(404))).includes('manifest_http_404'),'manifest_http_');
  calls=0;assert((await reason(manifestOkIpa(down))).includes('ipa_network_load_failed:offline'),'ipa_network_load_failed');
  calls=0;assert((await reason(manifestOkIpa(status(503)))).includes('ipa_http_503'),'ipa_http_');
})();

for(const marker of [
  'wasm_network_load_failed',
  'wasm_http_',
  'wasm_init_failed'
]) assert(wasm.includes(marker), marker);

for(const forbidden of ['GITHUB_TOKEN','Render','onrender.com','localStorage','sessionStorage']) {
  assert(!bootstrap.includes(forbidden));
  assert(!ipa.includes(forbidden));
  assert(!wasm.includes(forbidden));
}

ipaDiagnostics.then(()=>console.log('TASK0011_BOOTSTRAP_LOAD_DIAGNOSTIC_PASS'),e=>{console.error(e);process.exitCode=1;});
