"use strict";

/* Root-scoped Universal InTr service worker.
 * The prior runtime is retained byte-for-byte in intr-service-worker-base-v1.js.
 * Canonical Work is layered onto that same worker/runtime through one bounded extension.
 *
 * Compatibility contract retained at the canonical root for existing source validators:
 * "KV:KnowledgeVaultInterlock"
 * "HIL:Ingress"
 * "SDK:EvaluatorReviewIngress"
 * "MasterRecords:SV001Custody"
 * "CanonicalWork:Ingress"
 * runtime_surface:"CURRENT_USER_IPHONE_SERVICE_WORKER"
 * credential_authority:"TV/TVC"
 * github_token_runtime_authority:"NONE"
 * execution_authority:"NONE"
 *
 * These markers document the profiles implemented by the imported base + bounded
 * extension; they do not create authority or substitute for runtime observation.
 */
importScripts("/intr-service-worker-base-v1.js");
importScripts("/intr-canonical-work-extension.js");
