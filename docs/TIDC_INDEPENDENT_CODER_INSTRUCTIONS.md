# TIDC Independent Coder Instructions

## Required return format

Return exactly one JSON object that conforms to:

```text
data/tidc/coder-response.template.v0.1.json
```

Do not include Markdown fences, commentary before the JSON, commentary after the JSON, multiple candidate outputs, or explanatory prose outside the JSON object.

## Independence requirement

Set:

```json
"independence_attestation": true
```

only after completing the coding without consulting the published first-pass classifications or another coder's classifications.

Do not inspect the first-pass snapshot:

```text
data/tidc/coder-response.first-pass.v0.1.json
```

The first-pass snapshot exists only for later comparison by the agreement calculator.

## Allowed materials

Use:

- `data/tidc/second-coding-packet-v0.1.json`;
- the sources named for each candidate record;
- `docs/TIDC_SOURCE_PACKET_INDEX.md` for source-location and known-gap guidance;
- `docs/TIDC_CODEBOOK_REVISIONS.md` for current field definitions.

Do not use the public pilot classifications as coding answers. Do not infer missing dates from surrounding chronology. Do not convert an institutional announcement into peer-reviewed acceptance. Do not convert public availability into effective access without evidence.

## Coding rules

Complete one record object for every candidate record in the packet, preserving the packet order.

Use `null` or `Unresolved` where the evidence is missing, inaccessible, contradictory, or insufficient.

Record source locations or short evidence excerpts in `evidence_quotes_or_locations`. Keep quoted excerpts brief.

Record every material ambiguity in `uncertainty_notes`.

Set `exclusion_recommended` to true when the record is not a coherent event, combines materially distinct events, lacks enough evidence for inclusion, or belongs in a different record class. Supply an `exclusion_reason` whenever exclusion is recommended.

Disagreement is a valid result. Do not attempt to anticipate or match the first-pass coding.

## Required record set

The completed JSON must contain exactly these eleven records, once each and in this order:

```text
COMP-001
COMP-002
COMP-003
NET-001
NET-002
AI-001
AI-002
AI-003
QNT-001
QNT-002
QAI-2025-JP-OSAKA
```

## Submission boundary

The completed object is an independent coding artifact. It is not a validated result, a confirmation of the TIDC hypothesis, or authority to advance the release stage by itself.
