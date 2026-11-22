# Suite Template — GEN 01

The canonical template from which every suite is instantiated ("comported
from the template"). Canonical home: this folder, in the Ecosystem KV
coordination directory. Copies elsewhere are scratch and carry no standing.

## The rule

1. Every new suite is instantiated from this template, by `instantiate.py`,
   never composed freehand.
2. The template's components are validated by hash: TEMPLATE__MANIFEST__01.json
   pins every component's size and SHA-256. `instantiate.py` verifies all of
   them before deriving anything; a single mismatch aborts the instantiation.
3. A derived suite's PACKAGE__MANIFEST records the template manifest's
   SHA-256 and the derived self_check.py's SHA-256, so derivation itself is
   checkable from the suite's own face.
4. The conformance checklist inside self_check.py is part of the template:
   it travels verbatim into every derived suite and cannot be edited away
   downstream without the manifest readback showing it.
5. The conformance PROOF lives inside the suite it proves:
   CONFORMANCE__PROOF__01.json, a member of the suite bound by the suite
   manifest's hash like every other member. A proof held anywhere else —
   including beside the template — is a diagnostic, not conformance.
   `prove_conformance.py <suite> --install` computes the elements, writes
   the proof in, and rebinds the manifest; derived suites are born with it.

## The identity elements every suite carries (from the reference suites)

- PACKAGE__MANIFEST__01.json — per-file size + SHA-256 for every member.
- self_check.py — verifies every member AND the conformance checklist.
- README.md — suite name, generation, ProjectID, Funding line, source.
- FUNDING__STATEMENT__01.md — the cost-tracking spine: ProjectID, funding
  status declared as data, funder, commercial-arrangement line. A suite
  without it cannot be charged, gated, or settled, and its self-check FAILS.
- SUITE__CHARTER__01.md — purpose and level discipline.
- REFERENCES__01.md — pointers to the surrounding record; carries no
  content of theirs.

## Instantiation

    python3 instantiate.py --name "Example Suite" --generation "GEN 01" \
        --project-id "EXAMPLE-SUITE-001" \
        --funding-line "FUNDED — principal-funded Build Lane work" \
        --funder "the principal" \
        --arrangement "false — no external counterparty" \
        --source "Where this suite's content comes from." \
        --out /path/to/new-suite

Spec members are then added to the derived suite (SPEC__MEMBER__01.md.tmpl
is the skeleton), the manifest regenerated to include them, and the
self-check re-run. The funding block is never among the things edited.
