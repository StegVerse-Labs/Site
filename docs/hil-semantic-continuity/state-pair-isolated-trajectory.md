# Governed State Pair and Isolated Trajectory — Formal Specification v0.1

## Scope

This specification defines the smallest HIL semantic-continuity case: one identity observed at two states with no material external interaction between them.

## Objects

Let `I` be an identity and let:

- `S_I(a)` be a governed description of `I` under observation condition `a`;
- `S_I(b)` be a governed description of `I` under observation condition `b`;
- `C` be the declared constraint set;
- `X` be the declared external-interaction set;
- `G_I(a,b)` be the governed comparison of the two states.

```text
G_I(a,b) = Compare(S_I(a), S_I(b), C, X)
```

## Identity condition

The comparison is admissible only when the governance record establishes one of:

1. preserved identity;
2. admissible successor identity;
3. split identity;
4. merged identity;
5. terminated identity;
6. identity not established.

An unproven identity relation cannot be silently treated as preserved identity.

## Isolation condition

The isolated model requires:

```text
X = empty
```

or a proof that every material interaction in `X` is already represented in `C` and both state descriptions.

Any newly discovered material interaction invalidates the isolated inference and requires a coupled-state model.

## Difference operator

Define the governed difference:

```text
Delta_I(a,b) = S_I(b) minus S_I(a), evaluated under C
```

`Delta_I(a,b)` must distinguish:

- location difference;
- ordering or time-coordinate difference;
- intrinsic property difference;
- measurement-frame difference;
- observer difference;
- representation difference;
- uncertainty difference;
- identity change;
- unexplained residual difference.

## Trajectory family

The admissible trajectory family is:

```text
T_I(a,b | C) = {tau : tau(a)=S_I(a), tau(b)=S_I(b), tau satisfies C}
```

Two states determine a unique trajectory only when:

```text
cardinality(T_I(a,b | C)) = 1
```

If more than one trajectory satisfies the observations and constraints, the result is underdetermined and all surviving trajectories remain admissible candidates.

## State inference

For any parameter value `u` on an admissible trajectory:

```text
S_I(u) = tau(u)
```

may be inferred only when `tau` is unique or when the inference is explicitly represented as a set or distribution over the surviving trajectory family.

## Governance role

Governance does not generate the states. Governance supplies the declared identity relation, observational conditions, constraints, exclusions, and comparison rules required to distinguish continuity from discontinuity.

## Time posture

Time is not assumed to generate the trajectory. It may serve as one coordinate or ordering parameter used to reconcile individual state descriptions with the governed trajectory.

## Required receipt fields

A state-pair receipt must include:

- identity reference;
- source and destination state references;
- observer/governance reference;
- declared constraints;
- declared interactions and isolation result;
- difference classification;
- trajectory-family cardinality or bounded estimate;
- unique, underdetermined, invalidated, or identity-not-established result;
- uncertainty and evidence references;
- `authority_effect: false` unless separately authorized by another governed layer.

## Invalid transitions

The inference fails closed when:

- identity is not established;
- a material interaction is omitted;
- observational frames are silently changed;
- uncertainty is removed;
- the trajectory family is plural but represented as unique;
- compatibility is represented as proof;
- a state description is substituted for trajectory evidence.

## Generalization boundary

Coupled identities, splitting, merging, environmental interaction, and reality-scale slices are outside this isolated specification and require separate RTG mappings.
