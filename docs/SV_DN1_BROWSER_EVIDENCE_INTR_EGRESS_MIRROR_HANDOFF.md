# SV-DN-1 Browser Evidence Universal InTr Egress Mirror Handoff

Updated: 2026-08-30
Repository: `StegVerse-Labs/Site`
Goal: `SITE-SV-DN1-BROWSER-EVIDENCE-INTR-EGRESS-001`
Parent runtime handoff: `StegVerse-Labs/.github:docs/SV_DN1_BROWSER_EVIDENCE_INTR_INGRESS_MIRROR_HANDOFF.md`

## Goal

Allow the existing established `stegnode-web-*` SV-DN-1 resident observation page to send its authentic `stegverse.sv-dn1.browser-resident-observation-bundle/v3` directly into the canonical sovereign Universal InTr ingress without requiring manual file movement or minting a second StegVerse Node identity.

Canonical path:

```text
stegos-node/sv-dn1-resident-observation-v3.html
  authentic bundleOut already produced
        ↓
SV-DN-1 browser evidence InTr egress adapter
        ↓
source-side Interlock egress receipt
        ↓
InTr POST /intr/materialization
        ↓
StegVerse sovereign profiled ingress
```

The browser adapter is transport only. It does not perform SDK admission, StegCore/StegGate governance, Master Records custody, public-result promotion, or certification.

## Identity rule

This lane MUST continue the existing web-bootstrap identity already present in the bundle:

- `node_id` must be the bundle's existing `stegnode-web-*` identity;
- `device_continuity_id` must be the bundle's existing `stegdevice-*` continuity root;
- no `SV-NODE-*` identity is minted or substituted;
- `StegVerseNodeContinuity.registerDevice()` is not called by this lane.

The general Site `SV-NODE-*` outbox is a separate identity family and is not used as a shortcut for this transport.

## Discovery target

Target configuration:

`stegos-node/sv-dn1-browser-evidence-intr-target.json`

Schema:

`stegos.site.sv_dn1_browser_evidence_intr_target.v1`

Fail-closed default:

```text
state: AWAITING_SOVEREIGN_INTR_INGRESS
ingress_url: null
runtime_ingress_observed: false
```

The static target may be changed by the bounded projector `scripts/project_sv_dn1_browser_evidence_intr_target.py` only from an independently captured `stegverse.universal-intr-ingress-observation/v1` proving an HTTPS `/intr/profile` that advertises both `SV-DN1:BrowserObservation` and `STEGOS_WEB_BOOTSTRAP_EGRESS`.

The browser may also discover the same evidence directly at send time. When the static target is still `AWAITING_SOVEREIGN_INTR_INGRESS`, the egress adapter performs a credentialless same-origin HTTPS GET of `/intr/profile`. It accepts that live response only when the response URL is exact same-origin HTTPS, HTTP status is 200, the profile advertises `SV-DN1:BrowserObservation`, `STEGOS_WEB_BOOTSTRAP_EGRESS`, exact `/intr/materialization`, TV/TVC credential authority, zero execution authority, and the required event-triggered/write-once invariants. Only that live observed profile may be converted in-memory to:

```text
state: CONFORMING_SOVEREIGN_INTR_INGRESS
runtime_ingress_observed: true
ingress_url: https://.../intr/materialization
```

The page must not invent or guess an ingress URL.

## Transport request

Body schema:

`stegverse.sv-dn1.browser-observation-transport/v1`

Profile:

`SV-DN1:BrowserObservation`

The body carries:
- the complete already-authentic bundle;
- canonical bundle SHA-256;
- deterministic content-addressed materialization ID;
- existing node/device identities;
- source Interlock receipt;
- Universal InTr profile/policy;
- `DEVICE_SYSTEM -> STEGOS_ECOSYSTEM` boundary;
- zero-authority assertions.

The source Interlock receipt is chained from the final established web-bootstrap journal tail and binds the exact bundle hash. The transport request's `previous_receipt_hash` is the source Interlock receipt hash.

HTTP headers:

```text
X-StegVerse-Transport: InTr
X-StegVerse-Transport-Origin: STEGOS_WEB_BOOTSTRAP_EGRESS
X-StegVerse-Payload-SHA256: <exact canonical request-body sha256 hex>
Content-Type: application/json
```

No credential or authorization header is used.

## Successful browser evidence

A 202 response is accepted only when the sovereign receipt proves:

```text
schema=stegverse.sv-dn1.browser-observation-ingress-receipt/v1
state=INGRESS_ADMITTED
profile=SV-DN1:BrowserObservation
exact_bundle_validated=true
journal_replay_validated=true
source_interlock_validated=true
destination_validation=PASS
lineage_verified=true
write_once_persisted=true
locator_persisted=true
sdk_admitted=false
credential_used=false
authority_effect=NONE_INGRESS_ONLY
```

The response must match the browser's exact materialization ID, bundle hash, node ID, device continuity ID, source Interlock receipt hash, and transport payload hash.

`INGRESS_ADMITTED` means the authentic bundle became sovereign-local evidence. It does not mean the downstream SDK/StegCore/Master Records/publication chain completed.

## UI behavior

After an authentic observation finishes, the page immediately performs one bounded governed-delivery attempt using the exact frozen `bundleOut`. The Evidence card also exposes:

- `Send to governed first round` — retry control enabled only when `bundleOut` exists;
- `Export evidence bundle` — retained as offline/manual evidence fallback.

When no conforming ingress target is projected, the automatic attempt returns `AWAITING_SOVEREIGN_INTR_INGRESS` and does not downgrade or alter the already-authentic observation bundle. A later retry uses the same already-authentic bundle rather than re-running the observation.

## Explicit prohibitions

The adapter MUST NOT:
- create a new node/device identity;
- use `StegVerseNodeContinuity` registration as a substitute for the established web-bootstrap identity;
- add credentials or bearer tokens;
- send to a guessed/non-HTTPS target;
- claim TVC relay authorization;
- mutate the authentic browser bundle;
- claim SDK admission, governance, custody, deployment, public result, endorsement, or certification;
- automatically treat an HTTP response as downstream completion.

## Runtime truth at handoff creation

```text
authentic browser observation producer: MERGED / OBSERVED IN PRIOR RUN
authentic bundle export: IMPLEMENTED
browser -> sovereign automatic evidence transport: MERGED / VALIDATED
runtime-evidence target projector: MERGED / VALIDATED
browser same-origin live profile discovery: IMPLEMENTED ON BRANCH / VALIDATION PENDING
sovereign ingress target: NOT YET RUNTIME-OBSERVED
SDK first production round: NOT YET ANALYZED
main public governed result: WITHHELD
implementation PR: #749 / MERGED
implementation merge: 8fff6f9d18c18fcb6fd75d47557de74825d5c74d
implementation validation: Site Bootstrap PASS; Site Handoff Orchestrator PASS; Ecosystem Heartbeat PASS; StegOS Node Public Observation PASS
implementation claim release: PR #752 / dc9b61428a0588b507b0f4ae3861322f7d371228
current governed resident request: RESIDENT-EXEC-SV-DN1-FIRST-ROUND-006
runtime ingress admission: NOT YET OBSERVED
```

Newer authentic runtime evidence overrides this handoff.


## Automatic governed-round start — 2026-08-30

After established web-bootstrap continuity is independently verified, the v3 observation page now starts exactly one authentic observation automatically per page load. The existing manual `Run authentic observation` button remains available as an explicit retry control.

The automatic start does not bypass any existing gate:

```text
verified established continuity
  -> one bounded authentic Hugging Face observation
  -> existing frozen bundle construction
  -> existing automatic governed InTr send
  -> sovereign ingress validation
  -> resident request 006
```

A page-state guard prevents repeated automatic runs from repeated UI/state updates. Failure to discover or admit a sovereign ingress still fails closed and retains the authentic local bundle. No node identity, credential, claim/fence authority, SDK admission, governance decision, custody action, repository mutation, deployment, publication decision, release, or certification authority is added.
