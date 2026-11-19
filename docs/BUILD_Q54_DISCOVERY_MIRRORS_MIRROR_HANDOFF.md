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

