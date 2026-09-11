# HIL HTTPS Origin Canonicalization Mirror Handoff

Updated: 2026-09-11
Parent goal: `SHWP-HIL-SOVEREIGN-RECEIVER-001`
Parent COSV: `50000000102000`
Site issue: `#1251`

## Observed failure

Current-iPhone evidence showed the HIL ESRL page opened under `http://stegverse.org/...` in a new tab and failed closed because same-context local-ready evidence was absent. The custody successor likewise reported no pending staged HIL packet. HTTP and HTTPS are distinct browser origins, so retained localStorage/IndexedDB state from the HTTPS HIL execution lane is not visible to an HTTP entry page.

## Bounded repair

Before any retained-state read, both `stegos-bootstrap/hil-esrl-activate.html` and `stegos-bootstrap/hil-custody-activate.html` must detect `http:` on canonical host `stegverse.org`, replace the location with the exact same path/query/hash under `https:`, and return immediately. The repair does not copy or migrate evidence between origins and does not reinterpret an HTTP failure as runtime evidence.

The HTTPS page then performs the existing exact fail-closed validations unchanged. G25/fence 25, browser context, node, accepted ESRL lineage, staged exact packet requirements, service-worker identity, TV/TVC authority, and downstream non-overclaim semantics remain unchanged.

## Evidence boundary

Source/CI/merge prove only origin-canonicalization source readiness. Authentic current-iPhone `HIL-RECEIVER-RECEIPT-v2` remains required before receiver custody is accepted. Parent COSV and the two retained parent blockers do not change from this source repair.
