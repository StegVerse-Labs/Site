# Ecosystem Chat Governed Value-Claim Contract

## Status

Initial Site contract for preserving value claims arising from governed Ecosystem Chat submissions.

This contract does not guarantee payment, establish a market price, transfer ownership, authorize reuse, create custody, or grant settlement authority.

## Core distinction

A chat submission may be both:

```text
request for intelligence
+
contribution of intelligence
```

Token consumption measures compute use. It does not establish contribution, causation, admissibility, realized value, or compensation.

The governed value chain is:

```text
submitted
-> recognized
-> attributed
-> realized
-> distributable
-> settled
```

Stages MUST NOT be skipped. A later stage MUST reference the evidence supporting every prior stage.

## Claim stages

### submitted

The contribution entered the canonical governed event stream with stable identity, actor reference, timestamp, consent posture, source posture, and content or artifact hash.

### recognized

Evidence shows that the submitted information materially influenced a decision, artifact, workflow, model response, correction, evaluation, or later governed transition.

Recognition is not compensation and does not imply exclusivity, originality, ownership, or successful outcome.

### attributed

A governed attribution process assigns bounded influence among contributors, source materials, models, agents, infrastructure, and prior work.

Attribution MUST expose uncertainty, competing claims, overlap, dependency, and unresolved causality. It MUST NOT force a false single-author narrative.

### realized

A governed result produced measurable benefit or avoided measurable loss. The benefit may be economic, operational, intellectual, safety-related, evidentiary, social, or governance-related.

Realization MUST identify the measurement method, baseline, observation window, counterfactual limits, and externalized costs.

### distributable

An authorized policy or contract permits a defined reward class to be allocated. Distributable value may include payment, royalty candidacy, credit, standing, access, capability, governance participation, or another governed benefit.

Distributable does not mean paid.

### settled

An authorized settlement system records the final allocation and produces a settlement receipt. Settlement MUST reference the applicable contract, policy, custody records, identities or privacy-preserving claimant references, and dispute posture.

## Minimum value-claim object

```json
{
  "claim_id": "stable-unique-id",
  "submission_event_id": "stable-canonical-event-id",
  "claimant_refs": [],
  "stage": "submitted|recognized|attributed|realized|distributable|settled",
  "information_posture": {
    "source_type": "user_original|user_record|user_observation|user_correction|public|licensed|derived|unknown",
    "ownership_asserted": false,
    "consent_refs": [],
    "reuse_scope": "interaction_only|bounded_downstream|licensed_reuse|unknown",
    "sensitivity": "public|private|confidential|restricted|unknown"
  },
  "influence": {
    "target_event_refs": [],
    "mechanism": "context|correction|evidence|instruction|evaluation|artifact|other",
    "materiality": "unassessed|low|medium|high|decisive",
    "confidence": 0.0,
    "uncertainty": ""
  },
  "value": {
    "category": "unassessed|economic|operational|intellectual|safety|evidentiary|social|governance|mixed",
    "measurement_method": "",
    "baseline_refs": [],
    "observed_amount": null,
    "unit": null,
    "externalized_cost_refs": []
  },
  "distribution": {
    "reward_class": "none|credit|standing|access|capability|governance|royalty_candidate|payment|other",
    "policy_refs": [],
    "contract_refs": [],
    "allocation": null,
    "settlement_receipt_refs": []
  },
  "evidence_refs": [],
  "competing_claim_refs": [],
  "dispute_status": "none|open|resolved|rejected",
  "created_at": "RFC3339",
  "updated_at": "RFC3339",
  "hash": ""
}
```

## Information-value factors

User-supplied information MAY increase attributable value when evidence supports one or more of these factors:

```text
originality or scarcity
relevance to the governed result
material reduction in uncertainty
correction of a false assumption
causal influence on an artifact or transition
reuse beyond the immediate interaction
measurable improvement over baseline
lawful and consented availability
cost or harm avoided
new linkage among previously disconnected records
```

Personal or private information MUST NOT be presumed valuable merely because it is personal or private. Sensitivity is not a value multiplier. Unauthorized acquisition, coercive disclosure, or prohibited reuse makes the transition inadmissible regardless of apparent economic benefit.

## Anti-gaming invariants

1. Token count, message count, prompt length, or model cost MUST NOT independently advance a claim beyond `submitted`.
2. Self-reported importance MUST NOT establish material influence.
3. Duplicate, padded, fragmented, circular, or agent-generated submissions MUST NOT multiply attribution without independent evidence.
4. A successful outcome MUST NOT erase unauthorized use, externalized harm, or invalid consent.
5. Model output MUST NOT be treated as proof of originality or ownership.
6. Reward policies MUST disclose whether they compensate contribution, outcome, scarcity, risk, labor, reuse, or a combination.
7. Claim evaluation MUST remain reproducible from governed records without exposing restricted raw information to unauthorized viewers.
8. Revocation or narrowed consent MUST create a governed event and affect future use according to the controlling policy; it MUST NOT silently rewrite historical records.

## Expectation boundary

The public promise is:

> Every governed submission can preserve a traceable value claim. Compensation depends on demonstrated influence, admissibility, realized value, attribution rules, and an authorized distribution policy.

The system MUST visibly distinguish:

```text
claim preserved != value proven
value recognized != ownership proven
attribution != exclusivity
realized benefit != distributable value
distributable value != payment
prototype estimate != royalty
```

## Canonical event binding

A value claim is linked to the Ecosystem Node canonical event stream through stable identifiers. The browser MAY render a preview, but authoritative stage advancement, cryptographic hashing, custody, reconstruction, and settlement MUST occur in governed upstream systems.

Required event relationships:

```text
submission_event_id
recognition evidence event(s)
attribution decision event
realization measurement event(s)
distribution authorization event
settlement receipt event
```

## Initial Site behavior

The Site may:

- display claim stage and expectation boundaries;
- show captured versus derived information;
- expose evidence and policy references subject to disclosure rules;
- export non-authoritative preview JSON/JSONL;
- show unresolved, disputed, revoked, or non-payable status.

The Site must not:

- infer payment from activity;
- present prototype scores as money;
- advance stages without referenced evidence;
- conceal uncertainty or competing claims;
- treat consent as perpetual or universal;
- claim custody, settlement, or authority from browser-local state.

## Production next step

Bind value-claim creation and stage transitions to canonical gateway events, authenticated custody, reconstruction, policy evaluation, and settlement receipts. Add browser tests that verify stage ordering, anti-gaming rejection, consent/reuse boundaries, competing claims, and fail-closed non-payable status.