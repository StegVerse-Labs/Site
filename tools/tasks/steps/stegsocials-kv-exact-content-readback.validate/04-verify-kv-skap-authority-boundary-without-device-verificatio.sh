grep -q 'EXACT_CONTENT_BYTES_READBACK_VERIFIED' assets/stegsocials-kv-exact-content-readback.js
grep -q 'cloud_provider_readback_observed:false' assets/stegsocials-kv-exact-content-readback.js
grep -q 'provider_call_performed:false' assets/stegsocials-kv-exact-content-readback.js
grep -q 'authority_effect:"NONE_OBSERVATION_ONLY"' assets/stegsocials-kv-exact-content-readback.js
grep -q 'identity_authority_source:"KV_SKAP_ONLY"' assets/stegsocials-standard-flow-evidence.js
grep -q 'transport_node_role:"NON_AUTHORITATIVE_INTERCHANGEABLE"' assets/stegsocials-standard-flow-evidence.js
grep -q 'cloud_provider_readback_observed:false' assets/stegsocials-standard-flow-evidence.js
! grep -q 'physical_device_identity_claimed' assets/stegsocials-standard-flow-evidence.js
