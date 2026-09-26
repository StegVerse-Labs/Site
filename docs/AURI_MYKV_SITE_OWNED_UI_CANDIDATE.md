# Auri live controls — Site #239 owner candidate (unadmitted)

Parent goal: `SHWP-ECOSYSTEM-CHAT-INFERENCE-001`
Canonical COSV: `50000000100000`
Registry read: generation 251
Existing Site owner: [Site #239](https://github.com/StegVerse-Labs/Site/issues/239)
Existing StegOS owner: [StegOS #213](https://github.com/StegVerse-Labs/StegOS/issues/213)
Existing runtime owner: [central #60](https://github.com/StegVerse-Labs/.github/issues/60)

## Source only, not merged or live

This draft branch stages `assets/auri-live-site-controls.js` and its Node source tests. The module targets the **existing** `chatForm` and `chatLog`; it never creates another chat shell or generates a substitute KV session. It provides three mode buttons and separate direct `Mute`, `Video off`, and `Stop` actions. Starts are disabled when the trusted native owner is not installed; the standalone UI never opens microphone/camera permissions, emits runtime dispositions, or writes receipts.

The source must not be imported into `index.html`, `ecosystem-chat.html`, or `assets/ecosystem-chat-simple.js` or merged into main until the **existing** Site machine orchestrator has legitimately selected this bounded UI integration under Site #239. At the last verified state the orchestrator published `admitted_tasks=[]`, `external_tasks_allowed=false`, and `external_session_ownership_allowed=false`. This draft does not assign a new canonical task/COSV, issue a WorkerCoordinator claim, or modify Site orchestration state.

## Exact existing upstream sources

- MyKV profiles: `continuity-vault-kit` PR #223, merged `c6d4a9c29350b9b5fcb8b9a0ceee8b9a0a84f773`.
- StegOS preflight: `mobile/web-bootstrap/auri-mykv-live-mode.js`, PR #413, merged `14fd948be9fc40613065df33b3a0a185cac04943`. Its CANDIDATE status is not native permission.
- StegOS media controller: `mobile/web-bootstrap/auri-permissioned-media-controller.js`, PR #415, merged `0a395eb152e0b4e99368a35eddcf86ffba7fcc21`, blob `ea55c26694823facd0524be061d72a1ee7600b34`. It requires **actual** existing SDK/native authorization and independently trusted receipt verification before platform capture.
- Canonical SDK ingress: `StegVerse-org/StegVerse-SDK/stegverse/manifest_state_transition_runtime.py::execute_manifest`. Its validation of runtime response fields does not, by itself, independently authenticate original organization and Master Records ledger readback.
- Current public Site conversation script: `assets/ecosystem-chat-simple.js`, pre-candidate blob `01d2d41c61d48c2a4a97e8be77e641ac9fa2c46d`, shared with `index.html` and `ecosystem-chat.html`.

## Owner integration contract

Once the native Site orchestrator admits the existing Site #239 work, have its source owner package the already-merged StegOS controller on the existing same-origin Site delivery path and load both source modules into the current primary conversation. The owner must install genuine **native-authorized** implementations of `getVerifiedKvSession`, `proposeCurrentScopedManifest`, `submitThroughExistingUniversalInTr`, `independentlyVerifyOrganizationAndMasterRecords`, and `platformGetUserMedia`. These callbacks are a wiring interface, **not** proof that a JavaScript object bearing their names is trustworthy. The actual native and TV/TVC owners must verify their session-bound caller, latest SKAP relationship and consent, fresh transport admission, exact manifest digest, immediate predecessor, native disposition and original organization/Master Records reconstructed receipt. SDK `verify_receipt` and the source-only `CANDIDATE_ALLOW` are insufficient.

Audio, video and combined starts must each obtain a fresh scope-specific manifest and genuine independently verified ALLOW. Platform capture must be prompted only as a deliberate user action after that gate. For node interchange, retain the same KV session but recheck the fresh node-specific transport, authorization, consent and predecessor. Any revocation calls local track-level stop immediately without model inference; canonical event custody for that stop is a separate native transition.

## Current genuine execution boundary

Original resident request `RESIDENT-EXEC-ECOSYSTEM-CHAT-PARENT-002` remains REQUESTED and requires a fresh parent fence >24, first eligible G25. The public G20 carrier receipt remains incomplete. Current Master Records custody activation is `CUSTODY_ACTIVATION_PENDING_EXTERNAL_EVIDENCE`; authentic live capture, per-hop disposition and same-execution reconstruction have not been observed. No AI_SESSION_GATE, additional resident runtime or second-device prerequisite may be introduced to compensate for this missing observation.

The draft branch tests are **synthetic source tests only** and cannot authorize capture, production deployment, publication, or task closure.
