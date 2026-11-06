grep -F 'location.protocol==="https:"' assets/sv002-runtime-evidence-test.js
grep -F 'location.hostname.toLowerCase()==="stegverse.org"' assets/sv002-runtime-evidence-test.js
grep -F 'AUTHENTIC_EXTERNAL_CONTEXT_REQUIRED' assets/sv002-runtime-evidence-test.js
grep -F 'device_node_revalidation_performed:false' assets/sv002-runtime-evidence-test.js
! grep -F 'registerDevice(' assets/sv002-runtime-evidence-test.js
