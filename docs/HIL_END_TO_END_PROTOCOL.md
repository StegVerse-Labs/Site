# HIL End-to-End Protocol

Version: `HIL-PROTOCOL-v1.1`

## Purpose

This document is the complete operational companion to the `Humans as the Interoperability Layer` Primary. The Primary owns the research thesis and the model-facing Independent Response Protocol. This document owns the end-to-end technical and governance lifecycle from Primary identity through deployed intake, review, publication, Site projection, and Master Record release.

The Primary must not be represented as the sole technical specification unless a future reviewed version explicitly incorporates this protocol.

## Document ownership

| Layer | Authoritative record | Responsibility |
|---|---|---|
| Research and model instructions | Primary PDF | Thesis, experiment framing, independent model response procedure |
| Machine-readable experiment contract | `data/hil-experiment.json` | Versioned Primary, prompt, submission, transport, and authority state |
| Response provenance | `data/schemas/hil-response-provenance.schema.json` | Required Primary → prompt → response chain |
| Receiver and review runtime | `StegVerse-org/LLM-adapter` | Validation, custody, receipts, review, and append-only publication |
| Site lifecycle | This protocol and `docs/HIL_SITE_MIRROR_HANDOFF.md` | Complete operational sequence and continuation |
| Master Record projection | Site builders and `master-records/orchestration` | Chained release and authorized custody submission |

## Preconditions

The controlled public experiment may not activate until all of the following are established:

1. The exact approved Primary bytes are installed and hash-verified.
2. The deployed gateway advertises the same Primary and prompt identities.
3. HIL storage is durable across an actual service restart.
4. Intake, private-review, and publication credentials are separately configured.
5. The live observer reports `CONTROLLED_CYCLE_READY`.
6. One complete deployed controlled cycle has produced persistent evidence.

Participant review and approval do not substitute for these technical preconditions.

## Canonical Primary identity

```text
filename: HIL_Canonical_Paper_v1_1.pdf
version: v1.1
size_bytes: 87271
sha256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
repository_artifact: data/HIL_Canonical_Paper_v1_1.pdf
protocol_version: HIL-PROTOCOL-v1.1
prompt_version: HIL-PROMPT-v1.1
prompt_sha256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
provenance_version: HIL-RESPONSE-PROVENANCE-v1.1
```

Only exact-byte identity satisfies installation. Filename, screenshots, reconstructed text, visual equivalence, or participant approval alone are insufficient.

## Participant and model procedure

1. Obtain the canonical Primary from the governed Site surface.
2. Verify the displayed Primary version and SHA-256.
3. Read the Primary in full.
4. Follow its Independent Response Protocol.
5. Use the exact invocation prompt registered in `data/hil-experiment.json`.
6. Produce the response as a PDF without silently replacing or rewriting the original model output after generation.
7. Preserve the model, provider, generation time, and any available conversation reference.
8. Create the required provenance manifest before transmission.

A Primary hash match proves artifact identity. It does not prove the model read the document or complied with every instruction.

## Provenance construction

The browser computes the response PDF SHA-256 and creates `HIL-RESPONSE-PROVENANCE-v1.1` containing at least:

- Primary version and SHA-256;
- protocol version;
- prompt version and SHA-256;
- response SHA-256;
- model identifier when available;
- provider identifier when available;
- generation time when available;
- producer-signature state when available;
- optional conversation reference.

The PDF and provenance manifest are separate artifacts. Neither may be derived from or silently rewritten to match the other after submission. Missing optional participant metadata must not be converted into consent, attribution, publication, or authority inference.

## Intake readiness

Before upload, the Site queries the gateway readiness endpoint. Transmission is allowed only when the deployed gateway reports:

- intake enabled;
- durable storage configured;
- the canonical Primary SHA-256;
- the canonical prompt SHA-256;
- the required provenance schema;
- review configuration present;
- publication configuration present where applicable;
- append-only publication posture;
- no execution, publication, or Master Record authority granted merely by readiness.

When readiness is unavailable or mismatched, the Site fails closed and may create only a browser-local record that does not claim transmission or custody.

## Governed submission

The Site sends the exact response PDF and provenance manifest to `/api/hil/submissions`.

The gateway must:

1. enforce `application/pdf` and the configured maximum size;
2. verify required PDF structure and reject prohibited active-content conditions;
3. recompute the response SHA-256 from received bytes;
4. validate the complete Primary → prompt → response provenance chain;
5. preserve the exact received PDF bytes;
6. preserve a normalized provenance manifest separately;
7. allocate a unique submission identifier;
8. record submission metadata in durable storage;
9. issue `HIL-RECEIVER-RECEIPT-v2`.

The receiver receipt proves what the gateway received and recorded. It is not acceptance, publication, endorsement, or Master Record custody.

## Private review

An authenticated reviewer may record exactly one terminal or governed review state:

- `ACCEPT_PRIVATE`;
- `QUARANTINE`;
- `REJECT`.

The review decision must bind the submission identifier, response hash, provenance hash, reviewer identity or credential reference, decision time, and reason where required. The gateway issues `HIL-PRIVATE-REVIEW-RECEIPT-v1`.

Private acceptance does not authorize publication.

## Append-only publication

A separately authenticated publisher may publish only a submission with `ACCEPT_PRIVATE` and the required participant publication-consent posture.

Publication must:

1. allocate one stable, never-reused `HIL-RESP` identifier;
2. bind the submission, response, provenance, receiver receipt, and private-review receipt;
3. preserve the repository-relative public PDF artifact path;
4. emit `HIL-PUBLICATION-RECORD-v1`;
5. provide no update or delete route for the published identity.

Publication is append-only. A publication record does not claim original-byte custody outside the gateway.

## Site projection

The Site importer validates the publication record and hash continuity before appending it to `data/hil-responses.json`.

The public detail surface resolves the stable `HIL-RESP` identifier and displays the bounded public record. The Site projection must distinguish:

- recorded provenance from inferred model behavior;
- publication from endorsement;
- gateway custody from Site indexing;
- participant consent from execution authority.

## Master Record release

The deterministic Site builder creates `HIL-MASTER-RECORD-RELEASE-v1` by binding:

- response PDF hash;
- provenance hash;
- receiver receipt hash or reference;
- private-review receipt hash;
- publication-record hash;
- stable response identifier;
- previous release hash;
- canonical release SHA-256.

Default operation is dry-run. Mutation requires explicit authorization. The Site release is a projection and does not replace `master-records/orchestration` custody.

## Deployed controlled-cycle proof

Before public acquisition opens, one deployed cycle must demonstrate:

```text
readiness
→ governed PDF + provenance submission
→ receiver receipt
→ actual service restart
→ exact-byte and manifest persistence
→ authenticated ACCEPT_PRIVATE
→ private-review receipt
→ authenticated append-only publication
→ stable public lookup
→ Site import
→ first chained Master Record release
```

CI and in-process test clients do not substitute for an actual deployed restart.

## Failure and recovery rules

- Primary mismatch: block transmission.
- Prompt mismatch: block transmission.
- Response hash mismatch: reject submission.
- Missing or invalid provenance: reject submission.
- Non-durable storage: readiness must not report controlled-cycle ready.
- Duplicate submission or response identifier: fail closed.
- Review credential failure: no review mutation.
- Publication credential failure: no publication mutation.
- Restart persistence failure: quarantine activation and retain evidence.
- Site import mismatch: do not append the public index.
- Master Record chain mismatch: do not apply the release.

Failed records must remain observable according to their governed retention posture; they must not be rewritten into success.

## Authority boundaries

```text
Primary identity != proof of reading
prompt identity != proof of instruction following
submission != receiver custody until receipt
receiver receipt != private acceptance
private acceptance != publication
publication != endorsement
publication record != original-byte custody
Site projection != Master Record custody
Master Record release != authorization to submit to orchestration
live readiness != activation authority
CI success != deployed restart proof
```

## Completion criterion

The end-to-end process is complete only when the canonical v1.1 Primary is installed, the deployed gateway is durably configured, `CONTROLLED_CYCLE_READY` is observed, one deployed controlled cycle survives restart, the first accepted response is append-only published and imported, and the first valid chained Master Record release is produced and submitted only under separate authorization.
