# HIL v1.0 Release Installation

## Purpose

This record defines the repository installation and activation path for the Humans as the Interoperability Layer v1.0 documentation set without requiring ad hoc manual continuation.

## Installed Primary

The exact v0.5 Primary review artifact is installed at `data/hil-primary-v0.5-review.pdf.b64`.

- decoded size: `109210` bytes
- SHA-256: `52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946`
- activation state: `VERIFIED_INSTALLED`

## v1.0 ownership

- Canonical Paper: claims, boundaries, canonical input, and canonical prompt.
- Experiment Protocol: participant instructions, response format, metadata, consent, and submission requirements.
- Governance Specification: custody, provenance, receipts, review, publication, continuity, and Master Record release.
- Site Handoff: current deployment state, remaining gates, and continuation ownership.

The earlier Independent Response Packet v0.4 is superseded as the active experiment-path description. It remains historical evidence only.

## Automated continuation

The gateway repository owns an automated deployment-proof workflow at:

`StegVerse-org/LLM-adapter/.github/workflows/hil-automated-deployment-proof.yml`

The workflow:

1. generates separate review and publication credentials at runtime;
2. runs the complete governed-cycle tests;
3. starts the gateway against a declared durable path;
4. stops and restarts the process against the same path;
5. verifies intake and publication readiness after restart;
6. emits `HIL-LIVE-READINESS-OBSERVATION-v2` as a workflow artifact;
7. fails closed unless the observation reaches `CONTROLLED_CYCLE_READY`.

The observation is explicitly scoped to a GitHub-hosted ephemeral deployment proof and does not falsely claim an external production deployment.

## Remaining external gate

A production service must consume the same bounded environment contract and durable storage semantics. External production activation remains non-authorizing until its independently observed readiness receipt is imported and validated.
