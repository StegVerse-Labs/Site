# Q-67 — hosted framework suite on-ramp (source candidate)

ProjectID: Q-67 (queue identity; native Goal/COSV UNBOUND).
Funding: principal-directed build compute; no sale or service price quoted.
Commercial arrangement: no new arrangement established by this source build.

This service runs account-free intake, evidence-location analysis, canonical
SUITE__TEMPLATE GEN 01 instantiation, final in-suite conformance installation,
and downloadable delivery. **It is SPECIMEN_ONLY.** S4 production connection,
rail registration, matched remote receipt pairs, badges, pass-through and
probe-gated directory registration remain unimplemented. The page states
that the full connected product is not offered today. It cannot report S4
available or silently turn a local fixture into production acceptance.

Canonical continuation: [SUITES_ONRAMP_MIRROR_HANDOFF.md](../docs/SUITES_ONRAMP_MIRROR_HANDOFF.md).
Original task: StegVerse-Labs/.github#3443, comment 7068049479, Q-67.
Spec: principal attachment CODEX__SUITES__PAGE__INSTRUCTIONS__01.json,
issued 2026-11-22. Q-68 and existing rail changes are excluded.

## Run on the existing ecosystem host

Runtime: Python 3 standard library only. No packages, framework, account,
wallet, credentials, new host or provider are required by this component.
The following command is for the existing authorized runtime owner; it does
not authorize a new resident deployment or substitute for manifest routing.

```sh
python3 suites/server.py --bind 127.0.0.1 --port 8810 --storage /existing/operator-selected/private/q67-state
```

8810 is a configurable local development default, not a reserved production
port. The existing host owner selects an unused local route under the existing
manifest/proxy, then binds suites.stegverse.org to that route. Serve the page
and API together. GitHub Pages alone cannot execute the Python service.
Never put the state directory under a static website root. The source server
serves only allowlisted page assets, API status and receipt-scoped resources.

Operator integration still owes its existing proxy request/body/rate limits,
storage ownership and lifecycle policy. This component caps JSON requests at
64 KiB, evidence bodies at 1 MiB, claims at 12, intakes at 1000, concurrent
connections at 32 and build slots at 2. Public evidence GETs reject private,
loopback and metadata addresses, DNS responses containing any non-global
address, non-HTTPS URLs, credentials, nonstandard ports and redirects. The
socket is pinned to the checked address and TLS verifies the original host.
No cookies, ambient proxy or caller headers cross into the evidence fetch.

The receipt identifier is an unguessable access capability (128 random bits).
Do not log it, list intakes or publish someone else's pointer. Intake JSON and
the bundle remain in operator storage until the declared retention policy
removes them. Failed derivation trees are disposable and automatically removed.

## Evidence semantics

- Every submitted claim is retained verbatim, including unsupported claims.
- LOCATED requires lives_at within a declared public framework surface, the
  literal submitted text in its lives_at body and direct
  HTTPS 200 reads from all three evidence URLs. Download hashes are recorded.
- LOCATED is an **evidence-location grade**, never a semantic truth or replay
  verification verdict. Arbitrary receipt formats need framework-specific
  verification; this build does not invent a verifier for them.
- EVIDENCE_NOT_FOUND claims appear as named gaps, excluded from CLAIMS__01.json.
- Template manifest SHA-256 is pinned to
  f63d612c15e2ee364f3df651da8c11948846c61c897899aa45f8e9f6324bcc4e.
  All nine original component hashes and lengths are checked before executing
  even the instantiator. Original template/prover bytes are unchanged.
- The canonical instantiator runs; instance members are filled and analysis
  attached; prove_conformance.py --install runs again on final bytes. The
  unchanged template checker verifies those final members. No failed proof
  produces a download. Structural conformance does not prove S4 completion.
- The protocol section is copied verbatim from the index source at this
  revision; protocol-source.json pins the extracted section. Future protocol
  revisions must be harmonized by the source owner.
- Observation timestamps have authority_effect NONE. No rail is mutated and
  no value is signed, broadcast, transferred or settled.

## Reproduce the builder checks

```sh
python3 -B -m unittest discover -s suites/tests -v
```

The development-only browser smoke test needs an existing Playwright/Chromium
installation (neither is a production service dependency):

```sh
python3 -B suites/tests/page_specimen.py
```

It opens the actual form at 390×844, submits a supported fixture claim and an
unsupported negative control, waits for the on-screen receipt, downloads the
ZIP via the page, and executes its exact self-check and canonical prover.
Evidence bodies are deterministic fixtures at example.org URL labels;
**this is not a real external-framework run, live rail crossing, independent
validation or V1–V5 production acceptance**. Its output is retained under
evidence/. The local specimen is a complete suite, with its analysis and proof
inside it. It is not registered as a production directory entry.

## Before the full offer can be made

Existing runtime/rail owner must bind the actual documented registration,
badge and receipt-pair APIs, retain original paired outcomes, and gate directory
admission on live probes. API shapes must be authenticated from the current
rail source rather than guessed. Keep FAIL_CLOSED six-field dispositions until
these predicates hold. Do not edit existing rail chains or the index's honest
"not offered today" line to manufacture acceptance.

A separate non-author lane must execute V1–V5 at the final HTTPS hostname,
including page-driven specimen generation, matched pair replay, badge origin
binding, live directory probes, the missing-evidence control and regression
replays for both original rails. A localhost test never discharges those items.
