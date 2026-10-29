grep -q 'Prepare a StegSocials post' stegsocials-prepare.html
grep -q 'does not contact a social provider' stegsocials-prepare.html
grep -q 'Save draft to My KV' stegsocials-prepare.html
grep -q 'provider_call_performed:false' assets/stegsocials-post-preparation.js
grep -q 'provider_call_performed:false' assets/stegsocials-kv-draft-write-bridge.js
grep -q 'exact_content_bytes_readback_verified:false' assets/stegsocials-kv-draft-write-bridge.js
grep -q '03_Records/StegSocials/PostGroupState/' assets/stegsocials-bounded-group-device-kv-cas-receiver.js
grep -q 'stegverse-device-local-intr-v1' assets/stegsocials-bounded-group-device-kv-cas-receiver.js
grep -q '/assets/my-kv-n-device-kv-receiver.js' assets/stegsocials-bounded-group-node-intr-bridge.js
grep -q 'carrier_grants_authority:false' assets/stegsocials-bounded-group-node-intr-bridge.js
grep -q 'external_intr_admission_observed:false' assets/stegsocials-bounded-group-node-intr-bridge.js
grep -q 'external_intr_admission_inferred:false' assets/stegsocials-bounded-group-runtime-proof.js
grep -q 'Run exact runtime proof' stegsocials-bounded-group-runtime-proof.html
grep -q '02_Research/StegSocials/Drafts' assets/stegsocials-post-preparation.js
