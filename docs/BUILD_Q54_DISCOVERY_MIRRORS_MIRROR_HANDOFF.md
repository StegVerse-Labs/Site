# BUILD-Q-54 — Site discovery mirror handoff

Queue source: StegVerse-Labs/.github#3443 comment7014647758.
Claim: registry-current pairing#3472/7022189703; CODEX Cycle13.
Goal Task ID / COSV: UNBOUND. BUILD-Q-54 is a coordination queue identifier, not a native admission. The current GitHub Task Registry G326 was searched; no exact Q54 native row was authenticated. Binding/admission remains the existing Registry producer's act, routed to the coordinator. No adjacent Node/WorkSpace Goal is borrowed.
Source baseline: Site main82703dc88d05e61a11fc6c0015a9c35ac62a945b.
Branch: feat/build-q54-discovery-mirrors.
Authority NONE; no WorkerCoordinator claim/fence, service activation, signing, settlement, custody or production version step.

## Scope and contract
Implement only the ecosystem Site leg: retained read-only JSON snapshots of the public /offer, /openapi.json and /.well-known/x402 discovery documents, with exact captured-body hashes/lengths, source URLs and capture timestamps. A static mirror is historical evidence. It cannot establish current price, current settlement state, payment authorization, endpoint health or native execution.
The retained original documents keep their origin resource/payTo references unchanged. A separate mirror manifest and human landing page clearly label all snapshots historical/non-authorizing and link their live sources. A machine consumer must obtain fresh authoritative terms before any paid request; it must never substitute a captured challenge/authorization.

## Implementation and verification
Pre-work source claim and this handoff are created before implementation, using the existing Site claim registry and no-COSV publication exemption; native Goal/COSV stay UNBOUND.
Planned: dependency-free standard-library capture/validation tool, retained JSON documents and metadata manifest, landing page/README links. Validate all three offline without network; altered bytes/missing member or malformed/non-JSON origin refuse; capture failure preserves previous snapshots and manifest. Do not add a hosted dependency, scheduler, credential path or relaxation of existing claim gates.
Meaningful offline checks and ordinary exact-head CI precede source acceptance. Source PR integration and served readback remain explicit evidence steps; do not claim deployed or publication complete from local tests.

## Boundaries and continuation
Q54 lane-host/standing backup and production version-adoption legs are outside this claim. Q52 browser identity and Q53 DN1 observation work are separate. Existing production financial terms/endpoint code remain untouched.
Next: implement and test this scoped mirror; open source PR with exact checks and remaining predicates on the original task and registry pairing. Protected/native integration is not inferred from a coordination claim. Retain active source ownership through exact merge/readback, then release through the established registry-only terminalization route; if integration cannot proceed, file six-field condition and release coordination lease without falsely marking publication done.


## Implemented source and author evidence — 2026-11-19

Pre-work commit `145dd99a65d7f57cdd10ac47a0714f823257912d` was published on the
exact branch before implementation. Static generation
`31903cfa559739a0d5c034c9d3ffca4980e1aa1b3ed1a7dce545a38ba094ade9` retains:

| Source | UTC capture | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| /offer | 2026-11-19T21:10:32.134726Z | 5846 | 7ceb9d0aa623a38d35451ca69c9d990a5231d5952fc9f51fe6103d77d2ee279a |
| /openapi.json | 2026-11-19T21:10:35.178169Z | 3189 | 73a4c5068d6bef2727d5be0f65f39457de658fee05eabffdf058c3c8180ee382 |
| /.well-known/x402 | 2026-11-19T21:10:38.267814Z | 529 | 17216cccb308d7e03df6aed458d6eaa49a9c7a34c41f8fd702a8870d2ea3337f |

`current.json` is the single publication pointer. Retained generation bodies are
immutable and verified before that pointer switches. The landing page loads only
Site metadata and links the copies; it never requests a live price or signs/sends
a payment. Root 8374 index and README link the mirror. Existing domain Node
continuity script is present once on the new page; identity derivation is not changed.

Author checks: eight stdlib unit tests PASS under normal and optimized Python;
o-network verification of all three actual captures PASS; inline JavaScript syntax
PASS; exact-branch handoff orchestration PASS; source-claim/COSV validator PASS;
new `8374-discovery-mirrors.verify` catalog group ALLOW. The catalog uses existing
3.11 dispatcher provisioning, no new workflow, package, service, schedule or credential.

A prior source claim `SITE-DOMAIN-NODE-CONNECTION-001` is active and unindexed
in the inherited task-vector index. This branch indexes only its own no-COSV
publication exemption and recomputes actual counts (69 active, one unindexed),
sets `repository_vector_present=false` and retains the explicit blocker. It does
not manufacture a foreign vector or release the other author's claim. Owner return:
.github#3443 comment7022244817. Registry/COSV validators accept this truthful
incomplete-audit state; it is not native Goal admission or whole-repository completion.

Source errors resolved during work: a helper import used a wrong function name
(correct name `evaluate_candidate`); two guessed filenames were replaced by actual
`rg` results; one exec transport disconnect recovered on the next local call.
No failed source lookup was treated as evidence of absence; no credential or
production data was touched. Exact hosted CI, integration and served readback
remain to be filed against the source PR. Keep the same scope and evidence grades.
