# StegOS Current-iPhone Validator Mirror Handoff

Updated: 2026-09-04
Repository: `StegVerse-Labs/Site`
Issue: #949 / successor compatibility #965 / current-iOS guard successor #998

## Purpose

Preserve the legacy exact StegOS bootstrap projection validator while admitting only exact successor blobs that have already been materialized by the governed current-iPhone/custody progression.

The historical predecessor identities remain valid exact inputs. Current-iPhone exact successor identities remain valid. No wildcard, prefix, semantic approximation, or arbitrary successor is accepted.

## Authority

This validator grants no Site mutation, claim, execution, credential, HB, WorkerCoordinator, TVC, release, custody, publication, or activation authority.

## Runtime truth

Validator PASS is source compatibility evidence only and does not prove physical SV001 execution, Master Records custody, public propagation, or interaction admission.

## Exact post-custody successor compatibility — 2026-09-03

Site #965 extends only the exact successor allowlist after the Master Records custody UI/service-worker progression already changed three projected blobs:

```text
stegos-bootstrap/index.html          926ccfd6c640bcfdb49298b05026b08325db0990
stegos-bootstrap/stegos-bootstrap.js c094719cc4e8708af15bc0d374252a62b064cfc8
stegos-bootstrap/service-worker.js   99d652dc961855b0b89d093a3f5ad2e027352849
```

The stale aggregate #949 validator ownership was released through bounded tombstone migration #972 / `7c0c0eae736cbf9123679af7096c389a7dc234f0`, after the underlying #949 implementation had already merged through #950 / `d4013fbae31aa455a5cf50d73e9e4d9fd0aee261`.

The current #965 successor claim therefore reacquires `site:stegos-bootstrap-validator` without overlapping active ownership. All predecessor/current-iPhone exact identities remain admitted. No wildcard or semantic approximation is introduced.

## Exact current-iOS interaction-guard successor — 2026-09-04

Site #991 / PR #996 merged a fail-closed current-iPhone interaction guard into `stegos-bootstrap/index.html`. The released #991 claim records source guard wiring complete while public/device observation remains separately unproven. That merge materialized the exact current-main index Git blob:

```text
stegos-bootstrap/index.html          630d2d826871f5b03b9976677793cf43a7952fa6
```

Site Bootstrap run `33923741167` demonstrated that the legacy validator remained exact but stale: all claim/orchestration validation passed, then `check_stegos_ipod_bootstrap_projection.py` rejected only this current-main index blob because it was absent from the exact successor allowlist.

Issue #998 therefore admits only `630d2d826871f5b03b9976677793cf43a7952fa6` as an additional exact `index.html` successor. No wildcard, prefix, semantic matching, arbitrary-successor admission, product mutation, or authority change is permitted.

The #998 repair remains source compatibility evidence only. It does not establish public propagation, device enforcement, runtime execution, custody, or activation.
