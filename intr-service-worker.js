"use strict";

/* Root-scoped Universal InTr service worker.
 * The prior runtime is retained byte-for-byte in intr-service-worker-base-v1.js.
 * Canonical Work is layered onto that same worker/runtime through bounded extensions.
 *
 * Compatibility contract retained at the canonical root for existing source validators.
 * These exact markers describe behavior implemented by the imported base worker; they
 * do not create authority or substitute for runtime observation:
 * "KV:KnowledgeVaultInterlock"
 * "HIL:Ingress"
 * "SDK:EvaluatorReviewIngress"
 * "MasterRecords:SV001Custody"
 * "CanonicalWork:Ingress"
 * "MIR:MirrorRoundTrip"
 * MR_SV001_OWNER="master-records/orchestration#73"
 * MR_SV001_TRANSITION="SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION"
 * authority_class==="MACHINE_GOVERNED"
 * human_approval_required===false
 * current_governance_required===true
 * prior_receipt_authorizes_transition===false
 * STEGVERSE_INTR_LOCAL_TRIGGER
 * current_governance_decision_observed:true
 * site_custody_authority:false
 * site_execution_authority:false
 * sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35
 * runtime_surface:"CURRENT_USER_IPHONE_SERVICE_WORKER"
 * credential_authority:"TV/TVC"
 * github_token_runtime_authority:"NONE"
 * execution_authority:"NONE"
 */
importScripts("/intr-service-worker-base-v1.js");
importScripts("/intr-kv-installation-recovery-extension.js");
importScripts("/intr-canonical-work-extension.js");
importScripts("/intr-mir-roundtrip-extension.js");

/* Direct discovery channel for pages controlled by a more-specific nested service
 * worker scope. This exposes only the same non-authorizing profile already available
 * at /intr/profile and does not create another runtime or admission path.
 */
self.addEventListener("message", function (event) {
  var data = event.data || {};
  if (data.type !== "STEGVERSE_INTR_PROFILE_QUERY" || !event.ports || !event.ports.length) return;
  var port = event.ports[0];
  try {
    port.postMessage({ ok: true, profile: profile() });
  } catch (error) {
    port.postMessage({ ok: false, reason: String(error && error.message ? error.message : error), authority_effect: "NONE" });
  }
});
