"use strict";

/* Root-scoped Universal InTr service worker.
 * The prior runtime is retained byte-for-byte in intr-service-worker-base-v1.js.
 * Canonical Work is layered onto that same worker/runtime through one bounded extension.
 */
importScripts("/intr-service-worker-base-v1.js");
importScripts("/intr-canonical-work-extension.js");
