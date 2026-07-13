# Site ST-017 Adoption Handoff

## Authority

`docs/SITE_MIRROR_HANDOFF.md` remains the current Site task source of truth. This bounded adoption record does not replace it.

## Installed surface

```text
templates/sandbox-first/site.sandbox-profile.json
scripts/run_sandbox_validation.py
scripts/check_st017_sandbox_adoption.py
reports/sandbox-first-validation.report.json
.github/workflows/validate.yml
```

## Required sequence

```text
change installed
-> isolated Site repository copy
-> workflow inventory rebuilt inside the sandbox
-> workflow and application validation
-> durable sandbox report
-> SANDBOX PASS
-> hosted workflow observation
-> merge
-> separate current-main and public-output evidence
```

## Current state

```text
SANDBOX: NOT_RUN
GITHUB_ACTIONS: NOT_OBSERVED
PUBLIC_OUTPUT: NOT_VERIFIED
```

## Boundaries

Sandbox success does not activate live transport, deploy the usage endpoint, configure credentials, establish Master-Records custody, prove reconstructability, authorize release, or establish admissibility.

No release tag is authorized.
