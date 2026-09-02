# My KV Optional-Step State Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Issue: `#917`  
Branch: `fix/my-kv-optional-step-state-917`  
State: IMPLEMENTATION_ACTIVE  
Authority effect: NONE  
Activation effect: false

## Observed defect

The My KV onboarding Node receipt correctly records Step 3 as `SKIPPED_OPTIONAL` when the user chooses `Continue — this step is optional`, but the presentation layer currently groups `SKIPPED_OPTIONAL` with `COMPLETED` and `VERIFIED` and renders all three as `DONE ✓`.

That conflates workflow disposition with capability completion. In the observed case, the canonical KV email mapping bridge was unavailable and the email remained `UNMAPPED`, yet Step 3 displayed `DONE ✓`.

## Required invariant

```text
workflow progression state != capability state
```

Presentation contract:

- `COMPLETED` -> `DONE ✓`
- `VERIFIED` -> `VERIFIED ✓`
- `SKIPPED_OPTIONAL` -> `SKIPPED — OPTIONAL`
- any other recorded state -> literal normalized state
- no receipt -> `Not done`

A skipped optional step may count as onboarding progression, but it must not receive completed/verified presentation semantics or green completed styling.

## Canonical personal-information location

The Personal Information contact-profile file is canonically:

```text
KnowledgeVault/_Entities/Self/Personal_Contact_Profile.json
```

Within an already-open KnowledgeVault root, the relative path is:

```text
_Entities/Self/Personal_Contact_Profile.json
```

Canonical upstream source: `StegVerse-Labs/continuity-vault-kit`.

## Boundary

This repair changes presentation semantics only. It does not alter:
- the Node receipt value `SKIPPED_OPTIONAL`;
- canonical KV profile persistence;
- mailbox mapping;
- SKAP Vault;
- provider activation;
- authority or activation state.
