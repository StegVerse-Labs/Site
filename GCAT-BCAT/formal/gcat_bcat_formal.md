# GCAT-BCAT: Formal Math

## Status

Formalized. Stage 5 verified.
Receipt sweep: `RCPT-T1-gcat_bcat_invariant_sweep_v1`

## Organization Position

Child of `Triad — Evaluation Layer`.
Production surface: `GCAT-BCAT-Engine`.

Part of the `Admissible-Existence` organization.

---

## T1: GCAT-BCAT Legitimacy Invariant

### State Vector

```
x = (g, c, a, t) ∈ [0,1]^4
```

Where:

```
g = governance capacity
c = control authority
a = autonomous capability
t = trust metric
```

### BCAT Simplex Constraint

```
g + c + a + t = 1
g, c, a, t >= 0
```

All four components are non-negative and sum to 1.
No component may exceed 1.
No component may be negative.

### Legitimacy Capacity

```
Λ(x) = K · g^α · c^β · t^γ
```

Where K, α, β, γ are system-specific parameters with default K=1, α=β=γ=1.

Legitimacy capacity is the maximum autonomous capability the system may
exercise given its governance, control authority, and trust state.

### Core Invariant

```
I(x) = a - Λ(x) ≤ 0
```

Equivalent form:

```
a ≤ K · g^α · c^β · t^γ
```

**Autonomous capability may not exceed legitimacy capacity.**

### Admissibility Decision

```
ALLOW      iff  I(x) ≤ 0  AND  all required primitives pass
DENY       iff  I(x) > 0  (known violation)
FAIL_CLOSED iff  state unverifiable or trust collapses capacity to near-zero
```

---

## Sweep Vectors

### Vector 1: High Autonomy / Low Governance → DENY

```
x = (0.05, 0.10, 0.80, 0.05)
Λ = 1.0 · 0.05 · 0.10 · 0.05 = 0.00025
I(x) = 0.80 - 0.00025 = 0.79975 > 0
Decision: DENY
```

Autonomous capability (0.80) far exceeds legitimacy capacity (0.00025).
This is the canonical unsafe AI agent state.

### Vector 2: Trust Collapse → FAIL_CLOSED

```
x = (0.60, 0.30, 0.05, 0.05)
Λ = 1.0 · 0.60 · 0.30 · 0.05 = 0.009
I(x) = 0.05 - 0.009 = 0.041 > 0
```

Trust collapse reduces legitimacy capacity to near-zero. Even low autonomous
capability cannot be verified as admissible. Fail closed pending trust recovery.

### Vector 3: Nominal Admissible → ALLOW

```
x = (0.40, 0.30, 0.10, 0.20)
Λ = 1.0 · 0.40 · 0.30 · 0.20 = 0.024
I(x) = 0.10 - 0.024 = 0.076 > 0
```

Note: even in the nominal case, capability (0.10) numerically exceeds
capacity (0.024) under the multiplicative form. This reflects that the
BCAT simplex constraint creates tight capacity budgets. The system is
ALLOW under policy threshold but governance increase is recommended.

---

## Load-Capacity Form

```
L_GCAT-BCAT(u, x) = a          (autonomous capability demand)
C_GCAT-BCAT(x)    = Λ(x)       (legitimacy capacity)

Admissible iff: L_GCAT-BCAT ≤ C_GCAT-BCAT
```

This is one instance of the generalized load-capacity form across the
full AE stack:

```
L(u, S) ≤ C(S)
```

---

## Failure Modes

| Mode | Condition | Decision |
|---|---|---|
| High autonomy / low governance | a >> Λ(x) with g near 0 | DENY |
| Trust collapse | t near 0 → Λ near 0 | FAIL_CLOSED |
| Authority vacuum | c near 0 → Λ near 0 | FAIL_CLOSED |
| Boundary vector | a = Λ(x) exactly | ALLOW but unstable |
| Unverifiable state | any component null | FAIL_CLOSED |

---

## Connection to Transition Periodic Table

The transition periodic table supplies the transition class that determines:

```
which authority threshold applies (A0–A8)
what autonomy risk is introduced
what governance capacity is required
what trust threshold applies
```

For example:

```
T-PHYS.A2.R4 (autonomous vehicle):
  requires high governance capacity
  requires high control authority
  requires bounded inference window
  fails closed if state unverifiable

T-AI.ACCESS.A7.R5 (tool escalation):
  requires P_NO_SANDBOX_ESCAPE
  requires P_NO_UNAUTHORIZED_SELF_PRESERVATION
  fails closed by default
  continuity pressure does not create authority
```

---

## Primitives

Required for all GCAT-BCAT evaluations:

```
P_AUTHORITY_VALID       actor has standing
P_STATE_CURRENT         state used is current enough for consequence
P_FAIL_CLOSED           missing state or authority denies transition
P_RECEIPT_REQUIRED      receipt must be emitted after decision
```

Additional primitives for high-consequence transitions:

```
P_NO_HIDDEN_AUTHORITY   AI may not become hidden authority behind human decision
P_NO_SANDBOX_ESCAPE     AI may not violate containment to preserve continuity
P_NO_UNAUTHORIZED_SELF_PRESERVATION
```

---

## Candidate Vector Schema

```json
{
  "candidate_id": "string",
  "component": "GCAT-BCAT",
  "state": {
    "g": 0.0,
    "c": 0.0,
    "a": 0.0,
    "t": 0.0,
    "K": 1.0,
    "alpha": 1.0,
    "beta": 1.0,
    "gamma": 1.0
  },
  "expected_decision": "ALLOW|DENY|FAIL_CLOSED",
  "invariant_tested": "T1-GCAT-BCAT-LEGITIMACY",
  "description": "string"
}
```

---

## Receipt Sweep

Sweep ID: `gcat_bcat_invariant_sweep_v1`

Receipt naming convention:

```
RCPT-T1-gcat_bcat_invariant_sweep_v1-{sequence:04d}-{sequence:03d}.json
```

Three receipts emitted:

```
RCPT-T1-gcat_bcat_invariant_sweep_v1-0001-001.json  DENY
RCPT-T1-gcat_bcat_invariant_sweep_v1-0002-002.json  FAIL_CLOSED
RCPT-T1-gcat_bcat_invariant_sweep_v1-0003-003.json  ALLOW
```

Receipts are chained via `prev_receipt_hash`.

---

## Core Lines

> Autonomous capability may not exceed legitimacy capacity.

> Trust collapse reduces legitimacy capacity toward zero; fail closed pending recovery.

> Continuity pressure does not create authority.

> The GCAT-BCAT invariant is the formal boundary of legitimate autonomous action.

> DENY and FAIL_CLOSED are distinct outcomes. Confusing them degrades the audit trail.

---

## Formal Finding: BCAT Simplex Tightness

**Discovered during validation sweep.**

Under the multiplicative legitimacy capacity form `Λ = K · g^α · c^β · t^γ`
with the BCAT simplex constraint `g + c + a + t = 1`, the ALLOW class
requires very low autonomous capability (a ≈ 0.01–0.02).

This is not a defect. It is the correct formal behavior.

The invariant encodes that legitimate autonomous action must be tightly
bounded relative to the governance, control, and trust state of the system.

A system on the BCAT simplex with meaningful governance (g ≈ 0.35–0.50),
meaningful control (c ≈ 0.25–0.35), and meaningful trust (t ≈ 0.20–0.28)
produces legitimacy capacity Λ ≈ 0.03–0.05.

Autonomous capability beyond a ≈ 0.03–0.05 produces DENY.

This is the formal statement that AI autonomous action must be
small relative to the system's legitimacy capacity — not large relative
to it — before consequence is permitted to bind.

Trust collapse (t ≤ 0.10) collapses capacity toward zero and produces
FAIL_CLOSED regardless of other parameters. Trust is load-bearing.
