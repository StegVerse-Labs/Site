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

for(const marker of [
  'manifest_network_load_failed',
  'ipa_network_load_failed',
  'manifest_http_',
  'ipa_http_'
]) assert(ipa.includes(marker), marker);

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

console.log('TASK0011_BOOTSTRAP_LOAD_DIAGNOSTIC_PASS');
