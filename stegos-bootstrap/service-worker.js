"use strict";

// v14 is a propagation successor only. Runtime/governance behavior remains the
// exact released v13 implementation below; the successor cache generation forces
// installed current-device clients to refresh changed shell assets such as the
// automatic G23 -> contemporaneously governed Master Records continuation.
importScripts("./service-worker-v13-runtime.js");

CACHE_NAME = "stegos-web-bootstrap-v14";
