# Two Entry Points Mirror Handoff

## Goal
Complete and activate two always-growing but fully functional public entry points:

1. Ecosystem Chat.
2. VA Claim Assistant.

Originating session goal: ensure neither surface is represented as complete until its full intended end-to-end path is installed, validated, integrated, activated, and durably owned.

## Canonical coordination

- Cross-entry registry: `StegVerse-Labs/Site#152`
- Ecosystem Chat runtime: `StegVerse-org/LLM-adapter#18`
- Ecosystem Chat Site activation: `StegVerse-Labs/Site#24`
- VA Claim Assistant: `StegVerse-Labs/Site#113`
- Machine state: `data/two-entry-points-execution-state.json`

## Transfer rule
Work is transferred only when a named executor has accepted a bounded claim, has mutation authority, and produces inspectable commits, runs, logs, artifacts, or receipts. A handoff alone never proves transfer or execution.

## Active claims

### ECP-001 — Ecosystem Chat runtime activation
- Repository: `StegVerse-org/LLM-adapter`
- Branch: `main`
- Owner: issue `#18` and repository-native workflows
- State: `MACHINE_OWNED_BLOCKED`
- Exact blocker: no verified authorized persistent runtime currently supplies provider and Master-Records configuration and exposes a healthy endpoint.
- Release condition: zero-blocker immutable live activation receipt.

### ECP-002 — Ecosystem Chat Site activation and propagation
- Repository: `StegVerse-Labs/Site`
- Branch: `main`
- Owner: issue `#24`
- State: `CLAIMED_FOR_INTEGRATION`
- Release condition: adapter verified receipt imported, Site `ACTIVATION_COMPLETE`, required downstream ingestion verified.

### VACP-001 — VA governed claim session
- Repository: `StegVerse-Labs/Site`
- Branch: `main`
- Owner: issue `#113`
- State: `CLAIMED_FOR_IMPLEMENTATION`
- Required dependencies: LLM-adapter governed retrieval/provenance, TVC scoped capability, Master-Records custody/reconstruction.
- Release condition: deployed source-grounded and document-aware session with reconstructable zero-blocker receipt and exact public capability status.

### CONS-001 — Cross-session consolidation
- Repository: `StegVerse-Labs/Site`
- Branch: `main`
- Owner: issue `#152`
- State: `CLAIMED_FOR_INTEGRATION`
- Scope: preserve originating requirements, prevent duplicate execution, aggregate activation state, and verify archive conditions.
- Release condition: both entry points complete or all remaining work actually transferred to active observable executors.

## Required capability inventory

### Ecosystem Chat
- governed request and provider response;
- durable provider-usage persistence;
- authenticated provider-usage custody;
- transition custody;
- reconstruction PASS for both chains;
- immutable zero-blocker activation receipt;
- Site activation;
- verified Publisher, admissibility-wiki, and stegguardian-wiki propagation.

### VA Claim Assistant
- bounded procedural guide retained;
- source-authority registry and freshness/supersession checks;
- claim-route classification;
- proposition-level provenance and citations;
- source fact, user-record fact, inference, contradiction, and uncertainty separation;
- document identity, page anchors, hashes, privacy classes, and contradiction extraction;
- TVC-scoped provider/source execution;
- Master-Records custody and reconstruction;
- deployed end-to-end governed claim session;
- exact public capability status derived from verified evidence.

## Authority boundaries
No handoff, issue, workflow, monitor, provider output, receipt, custody event, reconstruction result, or public display independently grants deployment, adjudication, medical, representation, publication, release, or execution authority.

## Validation
The machine state must enumerate every task, owner, claim state, evidence location, blocker, release condition, and next executable action. Duplicate active claims on the same repository/path/capability are invalid.

## Current completion posture
- Developed-file completion: 5/9 shared coordination and activation-control deliverables.
- Validation completion: 2/8 end-to-end validation classes.
- Integration completion: 2/7 required cross-repository integrations.
- Goal activation: Ecosystem Chat pending; VA Claim Assistant building.
- Session consolidation: unique requirements are now preserved in this handoff and issue #152, but active implementation and integration work remains.

## Archive conditions
This workstream is not complete until both entry points are activated or every incomplete item is actually transferred to a separately verified active executor. Documentation without active execution is insufficient.