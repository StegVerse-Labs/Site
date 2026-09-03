# StegOS Current-iPhone Validator Mirror Handoff

Updated: 2026-09-03
Repository: `StegVerse-Labs/Site`
Issue: #949

## Purpose

Preserve the legacy exact StegOS bootstrap projection validator while admitting only the exact current-iPhone successor blobs required by authentically admitted Site#932.

The four predecessor identities remain valid exact inputs. The four successor identities are the exact pinned source blobs from StegOS current-iPhone projection package merge `62fcc9db38548d82ae656447913595f0027ed395`.

No wildcard, prefix, semantic approximation, or arbitrary successor is accepted.

## Authority

This validator grants no Site mutation, claim, execution, credential, HB, WorkerCoordinator, TVC, release, or activation authority.

## Runtime truth

Validator PASS is source compatibility evidence only and does not prove physical SV001 execution.


## Exact post-custody successor compatibility — 2026-09-03

Site #965 extends only the exact successor allowlist after the Master Records custody UI/service-worker progression already changed three projected blobs:

```text
stegos-bootstrap/index.html          926ccfd6c640bcfdb49298b05026b08325db0990
stegos-bootstrap/stegos-bootstrap.js c094719cc4e8708af15bc0d374252a62b064cfc8
stegos-bootstrap/service-worker.js   99d652dc961855b0b89d093a3f5ad2e027352849
```

All predecessor/current-iPhone exact identities remain admitted. No wildcard or semantic approximation is introduced. This change is validation compatibility only and grants no runtime, custody, publication, WorkerCoordinator, TVC, HB, credential, or activation authority.
