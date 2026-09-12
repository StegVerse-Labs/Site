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
