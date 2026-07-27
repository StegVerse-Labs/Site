# TIDC Codebook Revision Ledger

## Status

```text
posture: RELIABILITY_RECORD
research_state: PILOT_NOT_CONFIRMATORY
current_codebook_version: v0.1
independent_coding_completed: false
```

## Revision rule

Every change to a coding definition must record:

- the previous definition;
- the proposed definition;
- the evidence or disagreement that exposed the problem;
- affected record IDs;
- whether existing records were recoded;
- who approved the revision;
- the effective version and date.

No classification may be silently changed after independent coding begins.

## Baseline definitions

### Record kind

`discovery_event` identifies a mathematical, scientific, methodological, or independently verifiable capability result.

`access_precursor` identifies infrastructure or exposure changes that may alter later discovery conditions but do not themselves constitute discovery results.

### Dependency class

- **Necessary:** the result could not reasonably have been obtained in the documented form without the technology.
- **Material:** the technology substantially shaped the result, scale, timing, or method.
- **Supportive:** the technology assisted but was not central.
- **Incidental:** the technology was present but not causally important.
- **Unresolved:** evidence is insufficient or conflicting.

### Orientation

- **Self-capability:** the primary object of study is the technology's own behavior, limits, construction, control, verification, or reliability.
- **External:** the technology is applied primarily to a problem outside its own capability characterization.
- **Mixed:** self-capability and external-application objectives are inseparable.
- **Precursor variants:** reserved for access records and must not be collapsed into discovery-event orientation.

### Effective access

- **Yes:** eligible external users can practically execute meaningful work through the system.
- **Partial:** access exists but is materially restricted by eligibility, duration, queue, interface, documentation, or capability limits.
- **No:** announcement or demonstration does not provide practical external execution.
- **Unresolved:** evidence cannot establish effective access.

### Acceptance posture

Acceptance concerns conversion into recognized or operationally used knowledge and is distinct from publication or publicity.

## Pending ambiguity tests

1. Whether paper receipt dates are acceptable candidate-generation proxies.
2. When aggregate projects must be split into subevents.
3. How to code operational adoption without disciplinary consensus.
4. How to distinguish a new technology-native problem from an inherited problem newly made tractable.
5. Whether short-lived demonstration access qualifies as Partial or No effective access.
6. How to compare source-code openness with practical inspectability.
7. When independently verified self-capability results become external applications.

## Revision entries

No post-baseline revisions have been approved.

| Version | Date | Status | Trigger | Affected records | Change |
|---|---|---|---|---|---|
| v0.1 | 2026-07-27 | Baseline | Reliability workflow opening | All pilot and precursor records | Initial explicit coding definitions registered. |

## Boundary

Codebook clarity improves coding reproducibility. It does not establish historical causality or confirm the clustering hypothesis.
