const fs=require('fs');
const assert=require('assert');
const bootstrap=fs.readFileSync('stegos-bootstrap/current-iphone-testflight-bootstrap.js','utf8');
const request=fs.readFileSync('stegos-bootstrap/current-iphone-tvc-testflight-upload-request.js','utf8');
const ingress=fs.readFileSync('stegos-bootstrap/current-iphone-tvc-testflight-byte-ingress.js','utf8');

assert(bootstrap.includes('buildCurrentIphoneTvcTestflightUploadRequest'));
assert(bootstrap.includes('executeCurrentIphoneTvcTestflightByteIngress'));
assert(bootstrap.includes('signedIpa: signing.signedIpa'));
assert(bootstrap.includes('TVC_NATIVE_BUILD_UPLOAD_COMMITTED'));
assert(bootstrap.includes('TESTFLIGHT_PROCESSING_INSTALL_OBSERVATION'));
assert(!bootstrap.includes('TESTFLIGHT_INSTALLED'));
assert(request.includes('provider_operation: "UPLOAD_TESTFLIGHT_BUILD"'));
assert(request.includes('artifact://stegos/current-iphone/'));
assert(ingress.includes('application/octet-stream'));
assert(ingress.includes('x-stegverse-provider-request'));
assert(ingress.includes('credentials: "omit"'));
assert(ingress.includes('cache: "no-store"'));
assert(ingress.includes('artifact_persisted_by_tvc !== false'));
for (const forbidden of ['ASC_KEY_ID','ASC_ISSUER_ID','ASC_PRIVATE_KEY_P8','GITHUB_TOKEN','Render','onrender.com']) {
  assert(!bootstrap.includes(forbidden));
  assert(!request.includes(forbidden));
  assert(!ingress.includes(forbidden));
}
console.log('TASK0011_TESTFLIGHT_BYTE_INGRESS_PROJECTION_PASS');
