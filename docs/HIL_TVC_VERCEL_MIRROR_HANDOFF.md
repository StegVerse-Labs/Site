# HIL TVC/Vercel Mirror Handoff

Updated: 2026-07-31
Repository: `StegVerse-Labs/Site`

## Scope

This is the most specific Site handoff for the no-user-managed-secret HIL activation path. Read it after the canonical HIL handoffs and before continuing production deployment work.

## Superseding deployment decision

The Cloudflare GitHub-secret path is no longer the selected activation path.

The connected Vercel project:

```text
team: Rigel Randolph's projects
project: site
project ID: prj_xHOgZyCUzb37Zs7gyYVPCMb2OIl8
production domain: stegverse.org
latest observed deployment: dpl_8UwhvCtqe9pquQd1tXY9ue4JejBF
latest observed deployment state: READY
```

is the selected public ingress candidate.

TVC is the selected package-authority and evidence layer. `StegVerse-org/TV` is not the public runtime because its canonical role is private ephemeral token distribution.

## Provider-neutral architecture

```text
Vercel Site project
  /api/hil/* public ingress and readiness projection

GitHub-native participant return
  authenticated attachment transport and immutable source-object reference

StegVerse-Labs/TVC
  commit-pinned ingestion package
  scoped authority
  exact-byte verification
  deterministic chunking/reconstruction
  receipt and lifecycle evidence

CGE/downstream governance
  admissibility, review, publication, release, and propagation
```

No user-managed Cloudflare, Vercel, GitHub, or database secret is required by this design. Native platform authority may be used only inside its bounded platform context and must not be exported into application data.

## Required Site implementation

Destination: `StegVerse-Labs/Site`

1. Add Vercel functions or rewrites for only `/api/hil/*`.
2. Preserve every unrelated Site route and domain behavior.
3. Expose provider-neutral probes and readiness without claiming unavailable custody.
4. Introduce and validate an explicit custody-backend identifier for GitHub-source/TVC verification.
5. Bind participant return to an authenticated GitHub-native source object.
6. Import TVC receiver/reconstruction/lifecycle receipts before participant readiness can become true.
7. Prove a genuine Vercel redeployment or replacement and persistence of source-object identity and TVC receipts.

## State invariants

Both model entries remain:

```text
MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED
```

All response, package, acknowledgment, custody, registry, review, publication, endorsement, projection, and Master Record counts remain zero until authentic PDF bytes and package evidence are supplied and verified.

The existing `portable-sqlite-chunks-v1` identifier must not be reused for a different implementation. The provider-neutral chain needs a truthful new backend identity before readiness may be `READY`.

## Remaining modules and destinations

```text
StegVerse-Labs/Site:
- Vercel /api/hil/* ingress
- provider-neutral readiness/probes
- GitHub-native return surface
- TVC receipt import
- controlled cycle and redeployment persistence

StegVerse-Labs/TVC:
- HIL package registry entry
- exact-byte source-object verifier
- chunk/reconstruction engine
- scoped receipt/lifecycle tasks
- activation-readiness evidence

After authorization only:
- master-records/orchestration
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/Sit after identity/role verification
```

## Release posture

No tag or release is authorized. Provider-neutral ingress, authentic participant source-object custody, TVC verification, reconstruction, redeployment persistence, private review, publication, Site projection, Master Record release, and downstream verification remain unproven.

## Next execution direction

Implement the minimal Vercel `/api/hil/probes` and `/api/hil/readiness` surface first, explicitly reporting degraded/noncustodial state until the TVC source-object verification path is complete. Then register the HIL ingestion package in TVC and add the exact-byte verification task. Do not promote participant readiness from endpoint availability alone.

## Archive readiness

This handoff contains the complete provider-neutral continuation boundary. The complete prior thread is not required to continue.
