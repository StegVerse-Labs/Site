# Development Without Domination — Activation Tasks

## Task 1 — Exact PDF custody

- Repository: `StegVerse-Labs/Site`
- Branch: `publication/development-without-domination-v3`
- Path: `papers/development-without-domination/Development_Without_Domination_Rigel_Randolph_Final.pdf`
- Issue: `StegVerse-Labs/Site#128`
- Verifier: `scripts/observe_development_without_domination_publication.py`
- Expected SHA-256: `c2fcb0ce76f5eaba1a6dd4ccdd358fcae29b32b3110767b5f2b5b2ffa347c29d`

## Task 2 — Route verification and activation receipt

- Repository: `StegVerse-Labs/Site`
- Route source: `papers/development-without-domination/index.html`
- Status: `papers/development-without-domination/site-publication-status.json`
- Receipt destination: `papers/development-without-domination/site-mirror-receipt.json`
- Issue: `StegVerse-Labs/Site#128`
- Observer: `scripts/observe_development_without_domination_publication.py`
- Workflow: `.github/workflows/development-without-domination-publication.yml`

There are no external tasks. Every incomplete gate is repository-owned and machine-observed.
