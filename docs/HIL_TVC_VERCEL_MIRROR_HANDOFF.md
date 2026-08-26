# HIL TVC Provider-Neutral Mirror Handoff

Updated: 2026-08-26
Repository: `StegVerse-Labs/Site`
Branch: `main`
Canonical issue: `StegVerse-Labs/Site#497`

## Status

This handoff supersedes the 2026-07-31 Vercel-selected diagnostic-ingress architecture.

Vercel is **not** a canonical Site, HIL, publication, activation, recovery, custody, or readiness dependency. Historical Vercel project/deployment observations remain evidence only and must never satisfy or block a current acceptance gate.

## Canonical architecture

```text
Static/public Site publication
  -> canonical repository publication path
  -> custom-domain routing owned independently of Vercel

Dynamic governed runtime when required
  -> heartbeat-owned ephemeral StegVerse runtime/tunnel
  -> independently verified current lease and health
  -> provider transport never becomes policy authority

HIL participant return
  -> authenticated GitHub-native source object or attachment
  -> reconstructable immutable source identity

StegVerse-Labs/TVC
  -> commit-pinned package authority
  -> exact-byte verification
  -> deterministic chunking and reconstruction
  -> scoped execution and lifecycle receipts

CGE/downstream governance
  -> admissibility, review, publication, release
```

## Non-dependency invariant

A Vercel outage, account removal, project deletion, alias removal, build failure, quota exhaustion, credential loss, or complete unavailability MUST NOT change the canonical Site/HIL readiness verdict.

No current or future source-of-truth document may use any of the following as a required transition:

```text
Vercel deployment READY
Vercel production alias present
Vercel build minutes available
Vercel token/credential present
Vercel function reachable
Vercel project connected
```

## Historical Vercel evidence

The former Vercel project and deployment identifiers may be retained only as historical provenance. They do not establish present liveness or authority and are not part of the activation path.

Former project evidence included:

```text
team: team_tb2tGtHkSFhg5cpTMCvAhQJi
project: site
project id: prj_xHOgZyCUzb37Zs7gyYVPCMb2OIl8
former aliases included stegverse.org and *.vercel.app names
```

These values are intentionally non-authoritative.

## HIL surface migration

The existing `api/hil/*` contracts remain protocol references, not a requirement to execute as Vercel serverless functions. Any dynamic implementation must be exposed through the provider-neutral governed runtime path and preserve the same fail-closed semantics.

Required contracts remain:

```text
GET /api/hil/probes
GET /api/hil/readiness
POST /api/hil/submissions/validate
```

The implementation may move behind the heartbeat-owned runtime/rendezvous path without changing the protocol semantics.

## Participant and custody invariants

```text
participant PDF/provenance must be genuine
source object must be authenticated and reconstructable
exact-byte hashes must verify
TVC reconstruction/custody authority remains separate from transport
endpoint availability grants no publication or release authority
```

No synthetic participant object is authorized.

## Current activation objective

`StegVerse.ai` must be activated through the selected non-Vercel Site publication path. Domain activation is a routing/publication concern and must not introduce a new provider as policy or runtime authority.

## Required remaining work

Destination: `StegVerse-Labs/Site`

- verify the canonical static/public Site publication mechanism currently serving `stegverse.org`;
- bind and verify `StegVerse.ai` on that non-Vercel publication path;
- migrate or route any required dynamic HIL functions through the heartbeat-owned provider-neutral runtime;
- add repository validation that fails if canonical handoffs or activation scripts reintroduce Vercel as a required gate;
- record live public observation after `StegVerse.ai` resolves and serves the intended Site surface.

Destination: `StegVerse-Labs/TVC`

- keep HIL source verification, exact-byte reconstruction, provenance validation, lifecycle receipts, and custody identity provider-neutral;
- do not register a Vercel deployment identity as execution authority.

## Release posture

No release claim is created by this documentation transition alone. Vercel dependency removal is architecturally selected and recorded; live `StegVerse.ai` routing and any dynamic HIL runtime migration still require direct validation evidence.

## Exact next action

Inspect and verify the current non-Vercel publication path that owns `stegverse.org`, then attach `StegVerse.ai` to that same canonical publication mechanism and validate DNS/TLS/public content. Do not deploy or reconnect Vercel.

## Archive readiness

This handoff contains the complete provider-neutral continuation rule. Earlier Vercel-specific instructions are superseded and are not required to continue work.
