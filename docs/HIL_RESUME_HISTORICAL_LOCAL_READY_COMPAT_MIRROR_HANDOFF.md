# HIL Resume Historical Local-Ready Compatibility Mirror Handoff

Issue: #1265
Parent task: SHWP-HIL-SOVEREIGN-RECEIVER-001
Parent COSV: 50000000102000

## Observed failure

Current-iPhone Safari reached the canonical `stegos-bootstrap/hil-resume.html` surface and failed closed with:

`FAIL_CLOSED_DEVICE_CONTINUITY: stored local-ready result exists but fails canonical HIL validation`

## Exact source mismatch

The canonical historical producer `stegos-bootstrap/hil-browser-receiver.js` emits `stegos.hil_browser_receiver_activation_result/v1` without an `execution_surface` field in the final activation result. The new resume validator required `execution_surface === CURRENT_USER_IPHONE`, so valid persisted historical v1 evidence was rejected.

## Bounded repair

- keep exact schema/state/protocol/G25/fence/second-claim checks;
- accept omission of `execution_surface` for the historical canonical v1 activation result;
- if `execution_surface` is present, require `CURRENT_USER_IPHONE`;
- never rewrite or synthesize persisted evidence;
- preserve all custody/restart/TVC/authority boundaries;
- add regression coverage.

No parent COSV transition is authorized by this source repair.

## Public propagation boundary

Site PR #1267 merged the compatibility repair at `16988e6bc1aa2e7584d37948ceb2b3a4cbb38dbc` after all five exact-head Site gates passed.

HIL Public Page Proof run #21 then returned PASS, but its observed `hil-resume.html` SHA-256 remained exactly `a1a9bc783e6dcb177ad8c4a1bbd0a9a1255a9187fbf5dd06627f9cfb66ab278c`, identical to the pre-repair public page. The proof harness was only checking generic resume-contract markers, so that run demonstrated public resume-page availability but did not prove propagation of the compatibility repair.

The active claim therefore remains open. The existing proof workflow must require the exact compatibility expression:

`!Object.prototype.hasOwnProperty.call(value,"execution_surface")||value.execution_surface==="CURRENT_USER_IPHONE"`

A public proof is admissible for this repair only after the served page contains that exact logic and the resulting receipt records compatibility-marker verification. Until then, Safari must not be asked to retry and no runtime/custody inference is allowed.
