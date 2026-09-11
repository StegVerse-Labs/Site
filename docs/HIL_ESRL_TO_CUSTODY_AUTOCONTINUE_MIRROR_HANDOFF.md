# HIL ESRL-to-Custody Auto-Continue Mirror Handoff

Updated: 2026-09-11
Repository: `StegVerse-Labs/Site`
Issue: `#1244`
Parent goal: `SHWP-HIL-SOVEREIGN-RECEIVER-001`
Parent COSV: `50000000102000`
Branch: `fix/hil-esrl-to-custody-autocontinue-1244`

## Source of truth

This file is the current handoff for the bounded Site continuation that removes manual navigation between an already validated/restored exact current-iPhone ESRL `LEASE_OPEN` and the merged same-device custody successor.

## Inherited canonical state

- `.github` PR `#1521` merged the parent handoff reconciliation at `8cd301d630cd5128a8995f5b9795af74ffe370c2`.
- Site PR `#1239` merged the same-device custody source at `29f369759d9d3e52299dfd3a7e0dcbd1207ccfb4`.
- Site PR `#1240` released that source claim at `fc0a3366b6cb7a0ae7952807741c063352c6ceb1`.
- Parent state remains `ACTIVE / HANDOFF_READY`, COSV `50000000102000`.
- Authentic current-iPhone `HIL-RECEIVER-RECEIPT-v2` remains unobserved.

## Gap

`stegos-bootstrap/hil-esrl-activate.html` validates/restores the exact retained ESRL lease and renders it, but stops there. `stegos-bootstrap/hil-custody-activate.html` already auto-executes fail-closed from that same lease plus the already-staged exact packet. Requiring a separate manual URL navigation between those two same-context stages is unnecessary and conflicts with the single-device autonomous continuation trajectory.

## Bounded repair

After `hil-esrl-activate.html` validates either a newly returned or restored exact `LEASE_OPEN`:

1. preserve `stegos-hil-esrl-last-success-v1` unchanged;
2. schedule same-context navigation to `./hil-custody-activate.html`;
3. do not navigate on failed ESRL validation;
4. do not construct, infer, or claim custody evidence on the ESRL page;
5. do not mint another WorkerCoordinator claim/fence or alter G25/fence 25;
6. retain TV/TVC credential/lifecycle authority and GitHub runtime authority `NONE`;
7. leave authentic custody, restart proof, and TVC lifecycle evidence to their existing independent validators.

## Evidence semantics

Navigation only makes the already-merged custody successor reachable. It is not custody evidence. Only a valid `HIL-RECEIVER-RECEIPT-v2` produced by the current-iPhone custody route may satisfy receiver/custody evidence.

## README maintenance

README is re-reviewed as part of this bounded repair. The existing source/CI/runtime-evidence and non-authority boundaries remain accurate; no README prose change is required unless implementation changes those public boundaries.

## Completion

Source completion requires focused regression coverage plus the normal Site Bootstrap, Handoff Orchestrator, Ecosystem Heartbeat, persistent-card/current-iPhone, and relevant projection validation at the exact PR head. Merge does not prove runtime custody.

## Next runtime action

Once merged and publicly propagated, the already-used standalone Safari HIL/ESRL context should progress from accepted/restored `LEASE_OPEN` into `hil-custody-activate.html` automatically. The custody page then remains responsible for exact staged-packet verification and authentic `HIL-RECEIVER-RECEIPT-v2` production.
