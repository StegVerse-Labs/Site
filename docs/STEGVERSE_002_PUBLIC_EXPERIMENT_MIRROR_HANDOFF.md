# StegVerse-002 Public Experiment Mirror Handoff

Updated: 2026-08-31

## Authority

This task-specific handoff is subordinate to `SITE_MIRROR_HANDOFF.md` and is the most specific continuation record for the StegVerse-002 public self-characterization experiment observer surface.

## Goal

Publish a dedicated, mobile-first public observer route for the scheduled StegVerse-002 self-characterization experiment.

Target route:

`https://stegverse.org/stegverse-002-experiment.html`

## Boundary

Site is a public observation/projection surface only. It does not become experiment authority, execution authority, governance authority, custody authority, replay authority, reconstruction authority, communication standing, or scientific proof authority.

The page may describe:
- scheduled start: 2026-09-01 20:00 CDT;
- two-hour observation horizon;
- the frozen initial SDK request;
- the Self-Characterization Trajectory scoring model;
- the maximum three-organization communication boundary and the exact run-bound S0 communication set;
- Admissible-Existence as an available potential evidence source without prescribing use;
- SDK-derived world/relational expansion without granting new communication standing;
- governed self-reconciliation/self-repair only if independently proposed and admitted;
- complete receipt-linked state-transition history;
- caller-selectable final transition explanation projection;
- viewer-node-bound replay/reconstruction identities;
- strict claim discipline and terminal run states.

The public page must not claim the run has started, completed, self-repaired, contacted another organization, produced a score, or established autonomy before authentic evidence exists.

## Claimed paths

- `docs/STEGVERSE_002_PUBLIC_EXPERIMENT_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-stegverse-002-public-experiment-20260831.json`
- `stegverse-002-experiment.html`
- `stegverse-002.html`

## Completion condition

Source must merge through normal Site validation. URL readiness requires separate anonymous public HTTP observation of the exact route after publication. Source/merge alone is not publication proof.


## HTTPS observer-node establishment

The public observer route is HTTPS-only for viewer-correlation identity establishment.

On first secure-context visit, the browser automatically establishes a local viewer-correlation node:
- random stable `viewer_node_id` generated with WebCrypto/secure randomness;
- persisted only in the viewer's browser storage;
- no IP address, device fingerprint, account identity, PII, secret, or credential is required;
- the observer node has `authority_effect = NONE` and `activation_effect = false`.

The observer node is paired with the declared experiment identity:
`STEGVERSE-002-SELF-CHARACTERIZATION-001`.

The browser derives a deterministic `viewer_experiment_pair_id` from:
- node schema/version;
- `viewer_node_id`;
- the canonical experiment identity.

The browser-local viewer identity is a correlation identity only. It is distinct from a registered StegVerse communication Node identity used by `/sv002-observe/`; neither identity silently upgrades into the other.

When the canonical `manifest_receipt_id` becomes available, the same `viewer_node_id` is used by the SDK to derive viewer-bound replay and reconstruction identifiers. The pre-run experiment pairing is therefore continuity context, while canonical replay/reconstruction remain bound to the authentic manifest receipt.

HTTP may redirect to HTTPS, but node establishment must fail closed outside a secure context.

Additional claimed paths:
- `assets/stegverse-002-observer-node.js`
- `data/stegverse-002-experiment.json`

The public page may display the viewer node ID and experiment-pairing ID so the viewer can retain or copy their correlation identity. These IDs confer no execution, communication, governance, credential, or custody authority.


## Live-window registration activation

Pre-run publication intentionally ships with:

`observer_registration_endpoint = null`

so HTTPS page visits establish and retain the viewer node and experiment pairing locally without falsely claiming canonical registration before the live observer service exists.

Closer to T0, the experiment configuration may publish a governed HTTPS `observer_registration_endpoint`. When present, the page submits the already-established node/pair and accepts only a receipt matching the same experiment ID, viewer node ID, viewer/experiment pair ID, and `authority_effect = NONE`.

This activation must preserve the viewer node identity; it must not silently replace or re-key the observer.

Canonical replay/reconstruction IDs still require the authentic run `manifest_receipt_id`; observer registration alone is insufficient.


## Viewer identity distinction — 2026-09-01

The browser-local `viewer_node_id` on `stegverse-002-experiment.html` is a correlation identity only. It is not equivalent to a registered StegVerse communication Node.

Canonical distinction:

```text
viewer correlation node
  = stable browser-local replay/reconstruction correlation identity

registered StegVerse Node
  = communication-capable Node identity with genesis/registration/Interlock evidence
```

The live `/sv002-observe/` data path continues to require the latter. A viewer correlation node alone never grants InTr standing, communication authority, or experiment-data access.
