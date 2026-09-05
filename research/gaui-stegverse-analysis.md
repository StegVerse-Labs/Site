# Persistent Identity Is Not Persistent Permission

## A bounded comparative analysis of GAUI/BIGMAE and StegVerse transition admissibility

Status: research draft / not a publication claim
Issue: `StegVerse-Labs/Site#1005`
Primary external source: `https://zenodo.org/records/22301698`

## 1. Scope and source posture

This analysis compares a narrow architectural seam: persistent AI identity and authority continuity on one side, and consequence-specific transition admissibility on the other.

It does **not** claim that GAUI, BIGMAE/BIGMAS, and StegVerse are interoperable, equivalent, partnered, mutually endorsed, or already integrated. Similar terminology is not treated as proof of common semantics.

The comparison also preserves an important source distinction: GAUI is the identity/continuity research object identified in the cited Zenodo release; BIGMAE/BIGMAS execution-boundary statements must be evaluated as their own architectural claims rather than silently attributed to GAUI.

## 2. GAUI continuity and identity claims

The GAUI release is framed around persistent personal-AI identity under a human principal, with concerns including identity continuity, memory provenance, delegated authority, branching/lineage, embodiment continuity, revocation/forgetting, succession, and model-independent continuity.

For this comparison, the important architectural contribution is not a claim that continuity authorizes execution. It is the representation and preservation of identity-bearing and authority-lineage state across changes in model, application, device, agent, or embodiment.

That creates a useful input boundary for a separate question: what may a represented identity/authority state actually cause now?

## 3. Delegated authority and authority lineage

A represented authority state can answer questions such as:

- from whom was authority derived;
- what scope was represented;
- whether continuity and lineage are intact;
- whether a delegation is stale, revoked, superseded, or otherwise changed;
- which principal or agent relationship is being represented.

Those facts are important, but none is identical to a consequence-specific transition decision.

The distinction is:

```text
identity continuity != authority continuity != transition admissibility
```

A valid identity may coexist with invalid or stale authority. More importantly, valid authority may coexist with an inadmissible requested transition.

## 4. BIGMAE execution-boundary claim under examination

The relevant public discussion characterizes BIGMAE as beginning at a governed execution boundary and determining whether represented authority is sufficient for a requested consequence. That wording is architecturally important because the word **sufficient** can imply two materially different models.

### Model A — authority as represented condition

Authority is one element of the complete represented state evaluated before a transition.

```text
Adm(T_t) = F(S_t, T, A_t, M_t, E_t, C_t, U_t, ...)
```

Under this model, authority may be required for a transition class but never becomes synonymous with permission.

### Model B — authority as enabling authorization primitive

The execution boundary asks whether authority is sufficient and, if sufficient, allows the transition subject to subordinate checks.

Under this model, authority retains privileged enabling semantics even if additional runtime controls exist.

These models are not equivalent.

## 5. StegVerse transition-admissibility model

The StegVerse comparison treats authority as represented state/evidence entering the transition function rather than the cause that grants passage through it.

Candidate relations:

```text
I_t does not imply A_t
A_t does not imply Adm(T_t)
```

where:

- `I_t` = represented identity/continuity validity at time `t`;
- `A_t` = represented authority validity at time `t`;
- `Adm(T_t)` = admissibility of the proposed transition at time `t`.

A fuller candidate function is:

```text
Adm(T_t) = F(S_t, T, A_t, M_t, E_t, C_t, U_t, ...)
```

with, at minimum:

- current represented state `S_t`;
- proposed transition `T`;
- authority state `A_t`;
- mandate or governing objective `M_t`;
- evidence state `E_t`;
- represented constraints `C_t`;
- unknown/uncertainty state `U_t`.

The important property is that no single element is silently promoted into generalized permission.

## 6. Authority-as-condition vs authority-as-permission test

The strongest falsification test for apparent architectural convergence is simple:

> Can authority remain completely valid, current, authentic, properly derived, and in-scope while the requested transition is still inadmissible — without describing the authority itself as invalid or insufficient?

If yes, authority can remain a represented condition inside an independent admissibility function.

If no, and transition refusal is ultimately expressed as authority insufficiency, then authority is still functioning as an enabling authorization primitive even if the architecture uses a separate execution-control layer.

This is the key unresolved comparison with BIGMAE.

## 7. Candidate formal interface

A possible interface between the architectural concerns is:

```text
continuity / identity / authority representation
-> transition-admissibility evaluation
-> consequential transition
-> updated continuity / provenance representation
```

This is intentionally directional without assigning ownership of the execution boundary to either architecture.

A formal interface would need to specify at least:

- identity-state representation;
- authority-lineage representation;
- freshness and revocation semantics;
- evidence references;
- mandate/intent representation;
- uncertainty representation;
- proposed-transition identity;
- consequence representation;
- admissibility result and reason structure;
- post-transition continuity/provenance update;
- reconstruction semantics.

Until such an interface exists, correspondence is conceptual rather than interoperability evidence.

## 8. Non-equivalence and non-collaboration statement

This analysis records architectural correspondence only.

It does not establish:

- partnership;
- collaboration;
- endorsement;
- shared governance authority;
- implementation compatibility;
- runtime integration;
- common transition semantics;
- ownership of the governed-execution boundary.

Public discussion can motivate a research question; it cannot substitute for a specification or verified interface.

## 9. Open questions and falsification conditions

1. Does GAUI explicitly separate identity validity from delegated-authority validity in machine-evaluable state?
2. Does BIGMAE permit a fully valid authority state to coexist with a denied transition without reclassifying authority as insufficient?
3. Are consequence ceilings independent represented constraints or dimensions of authority scope?
4. Is staleness a property of identity, authority, evidence, mandate, context, or each independently?
5. Can intent continuity remain valid while a requested transition becomes inadmissible?
6. How are unknowns represented when the system cannot yet establish all transition attributes?
7. Does HITL introduce new evidence/state or act as a superior permission source?
8. Can the admissibility result be reconstructed independently from the identity/authority system that supplied inputs?
9. Can post-transition continuity be updated without allowing the continuity system to become transition authority?
10. What evidence would demonstrate that the execution boundary is genuinely independent of authority rather than an authorization layer with additional predicates?

## 10. Current comparative conclusion

The strongest shared architectural observation is the separation:

```text
identity validity does not imply authority validity;
authority validity does not imply transition admissibility.
```

The strongest unresolved difference is semantic, not terminological: whether authority is merely represented state supplied to a transition-admissibility function or remains the privileged enabling concept by which a consequence is permitted.

That question must be answered before claiming that StegVerse and BIGMAE meet at the same governed-execution boundary.

## 11. Next research step

The next bounded step is source-level examination of the GAUI/BIGMAE definitions for authority, delegation, consequence ceilings, staleness, intent continuity, autonomy, HITL, and execution-time controls, followed by a claim-by-claim matrix:

```text
external claim
-> source/version
-> formal meaning
-> StegVerse analogue, if any
-> semantic correspondence
-> semantic conflict
-> unresolved evidence
```

Any later public paper should be generated from that matrix and the canonical publication/provenance system rather than from social discussion alone.
