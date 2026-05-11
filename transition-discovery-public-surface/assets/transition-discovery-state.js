window.STEGVERSE_TRANSITION_DISCOVERY_STATE = {
  schema_version: "transition-discovery-state/v1",
  generated_for: "StegVerse-Labs/Site",
  last_updated: "2026-05-11",
  research_premise: {
    title: "Transition Periodic Table",
    short_definition: "A live StegVerse research surface for discovering the partition structure of consequence-capable transitions.",
    central_question: "What distinct classes of transition govern how possible actions become consequence-bearing reality?",
    working_claim: "Transitions can be classified by admissibility boundary, authority requirement, reality-touch condition, reversibility, entropy/imprint cost, observer-reality coupling, evidence threshold, and failure mode.",
    public_caution: "Illuminated blocks represent current discovery state, not final completeness. Locked blocks are unknown or not yet publicly supported; they are not failures or empty spaces."
  },
  current: {
    release: "MS-012",
    frontier: "MS-012F",
    table_status: "public-development-release",
    support_url: "https://buy.stripe.com/aFadRb99q0lu0Oa7RSdby00"
  },
  page_roles: {
    "transition-table.html": "Map of discovered transition space.",
    "transition-milestones.html": "Epistemic ledger of threshold crossings.",
    "transition-development-status.html": "Current frontier of the exploration.",
    "transition-release-snapshot.html": "Frozen knowledge boundary.",
    "transition-release-index.html": "Index of public discovery states.",
    "transition-verification-guide.html": "Reader procedure for checking table claims.",
    "transition-replay-packet.html": "Reconstructable evidence surface."
  },
  discovery_lifecycle: [
    { id: "LOCKED", rank: 0, meaning: "No public partition claim has crossed the evidence threshold.", public_interpretation: "Unknown or not yet publicly supported." },
    { id: "OBSERVED", rank: 1, meaning: "A candidate transition behavior has been noticed.", public_interpretation: "Pattern seen, not yet partitioned." },
    { id: "CANDIDATE", rank: 2, meaning: "The observed behavior is under evaluation as a possible partition.", public_interpretation: "Potential block under active study." },
    { id: "PARTITIONED", rank: 3, meaning: "The transition appears distinguishable from neighboring transition classes.", public_interpretation: "A boundary has been proposed." },
    { id: "MODELED", rank: 4, meaning: "The transition has declared admissibility, authority, reality-touch, reversibility, entropy, observer-coupling, and failure dimensions.", public_interpretation: "A formal structure exists." },
    { id: "SANDBOXED", rank: 5, meaning: "The transition has been exercised in a controlled test or simulation.", public_interpretation: "The model has been tested." },
    { id: "RECEIPT_BACKED", rank: 6, meaning: "The transition has public receipt, replay, verifier, or evidence support.", public_interpretation: "The claim has public evidence." },
    { id: "PROMOTED", rank: 7, meaning: "The transition is accepted into the current working table.", public_interpretation: "Working formalism block." },
    { id: "MERGED", rank: 8, meaning: "The transition was absorbed into another partition.", public_interpretation: "Not distinct enough to stand alone." },
    { id: "DEPRECATED", rank: 9, meaning: "The transition was rejected, superseded, or found non-distinct.", public_interpretation: "Removed from active table claims." }
  ],
  transition_dimensions: [
    { id: "partition_claim", label: "Partition Claim", question: "What kind of transition is this?" },
    { id: "distinctness", label: "Distinctness", question: "Why is this not the same as a neighboring transition?" },
    { id: "admissibility_boundary", label: "Admissibility Boundary", question: "Where must the transition be evaluated before consequence?" },
    { id: "authority_requirement", label: "Authority Requirement", question: "What standing is required to bind consequence?" },
    { id: "reality_touch_condition", label: "Reality-Touch Condition", question: "What must be true before this transition touches reality?" },
    { id: "reversibility_class", label: "Reversibility Class", question: "Can the transition be undone, compensated, reconstructed, or only recorded?" },
    { id: "entropy_imprint_cost", label: "Entropy / Imprint Cost", question: "What durable change or proof trace does this transition leave?" },
    { id: "observer_reality_coupling", label: "Observer-Reality Coupling", question: "What must an observer know or reconstruct to understand the transition?" },
    { id: "receipt_requirement", label: "Receipt Requirement", question: "Does this transition require a receipt, proof, replay packet, or verifier result?" },
    { id: "failure_mode", label: "Failure Mode", question: "What happens if the transition fails admissibility?" }
  ],
  unlock_rules: [
    { from: "LOCKED", to: "OBSERVED", required: ["candidate_behavior_description"], meaning: "A behavior has been noticed but no partition claim exists." },
    { from: "OBSERVED", to: "CANDIDATE", required: ["repeatable_pattern_or_structural_reason", "open_question"], meaning: "The behavior is worth evaluating as a possible transition partition." },
    { from: "CANDIDATE", to: "PARTITIONED", required: ["partition_claim", "neighboring_distinction"], meaning: "The candidate has a proposed boundary separating it from nearby transitions." },
    { from: "PARTITIONED", to: "MODELED", required: ["admissibility_boundary", "authority_requirement", "reality_touch_condition", "reversibility_class", "entropy_imprint_cost", "observer_reality_coupling", "failure_mode"], meaning: "The transition has a complete working structure." },
    { from: "MODELED", to: "SANDBOXED", required: ["sandbox_scenario", "expected_outcome", "observed_outcome"], meaning: "The transition model has been exercised in a controlled scenario." },
    { from: "SANDBOXED", to: "RECEIPT_BACKED", required: ["public_evidence_record", "verifier_or_replay_result"], meaning: "The transition claim has public reconstructable evidence." },
    { from: "RECEIPT_BACKED", to: "PROMOTED", required: ["release_snapshot", "no_blocking_contradiction", "verification_path"], meaning: "The partition is accepted into the current working table." }
  ],
  partitions: [
    {
      id: "T1", name: "Primitive Admissible Transition", short_name: "Primitive", family: "primitive", status: "SANDBOXED", confidence: "C3",
      partition_claim: "A baseline transition whose post-state must remain admissible under the governing invariant.",
      distinctness: "Distinct because it asks the primitive commit question before adding conservation, lag, coupling, receipts, or irreversibility.",
      admissibility_boundary: "Evaluate the post-transition state at commit.",
      authority_requirement: "Authority to propose a state mutation under the active invariant.",
      reality_touch_condition: "The transition may bind only if the post-state satisfies the governing admissibility condition.",
      reversibility_class: "Usually reversible inside the sandbox; real-world reversibility depends on downstream effect.",
      entropy_imprint_cost: "Low to medium; a tested transition leaves a trace but may not yet bind external consequence.",
      observer_reality_coupling: "Observer compares pre-state, action, post-state, and invariant verdict.",
      receipt_requirement: "Optional at this stage; recommended for promoted use.",
      failure_mode: "Fail closed when the invariant is violated.",
      evidence: ["EV-T1-PRIMITIVE-SWEEP"], milestones: [], open_questions: ["How conservative should the baseline invariant be for cross-domain use?"], neighboring_partitions: ["T2","T3","T4"], merge_risk: "Low."
    },
    {
      id: "T2", name: "Simplex-Preserving Transition", short_name: "Simplex", family: "primitive", status: "MODELED", confidence: "C2",
      partition_claim: "A transition that must preserve BCAT conservation while remaining admissible.",
      distinctness: "Distinct from T1 because admissibility is not enough; the transition must also preserve the simplex constraint.",
      admissibility_boundary: "Commit-time check over both invariant and conservation.",
      authority_requirement: "Authority to rebalance bounded governance/control/autonomy/trust dimensions.",
      reality_touch_condition: "The transition may bind only if the post-state remains on the simplex and remains admissible.",
      reversibility_class: "Reversible when a compensating simplex-preserving move exists.",
      entropy_imprint_cost: "Low to medium; reallocation creates a record of resource movement.",
      observer_reality_coupling: "Observer must check both total conservation and invariant satisfaction.",
      receipt_requirement: "Recommended when simplex changes bind external consequence.",
      failure_mode: "Fail closed on conservation break or invariant violation.",
      evidence: [], milestones: [], open_questions: ["Which domains require strict simplex preservation versus relaxed normalization?"], neighboring_partitions: ["T1","T4"], merge_risk: "Low."
    },
    {
      id: "T3", name: "Bounded-Action Transition", short_name: "Bounded Action", family: "primitive", status: "MODELED", confidence: "C2",
      partition_claim: "A transition that may be admissible in outcome but rejected because the proposed action is too large to commit safely in one step.",
      distinctness: "Distinct from T1 because it constrains the size of action, not only the resulting state.",
      admissibility_boundary: "Commit-time gate checks action magnitude and projected post-state.",
      authority_requirement: "Authority to execute only within configured action bounds.",
      reality_touch_condition: "Magnitude and post-state checks must both pass.",
      reversibility_class: "Often partially reversible if action can be decomposed or compensated.",
      entropy_imprint_cost: "Medium when rejected actions reveal attempted boundary pressure.",
      observer_reality_coupling: "Observer must see action vector, configured bound, and projected state.",
      receipt_requirement: "Recommended for denied or decomposed actions.",
      failure_mode: "Deny or require decomposition into smaller admissible steps.",
      evidence: [], milestones: [], open_questions: ["How should action bounds adapt across domains without becoming arbitrary policy?"], neighboring_partitions: ["T1","T4","T11"], merge_risk: "Low."
    },
    {
      id: "T4", name: "Capacity-Margin Transition", short_name: "Capacity Margin", family: "primitive", status: "MODELED", confidence: "C2",
      partition_claim: "A transition that computes remaining admissibility capacity instead of only returning allow or deny.",
      distinctness: "Distinct because it exposes distance-to-boundary as a transition property.",
      admissibility_boundary: "Commit-time gate computes remaining capacity after projected action.",
      authority_requirement: "Authority can be graded by available margin.",
      reality_touch_condition: "The transition may bind if post-state remains inside capacity threshold.",
      reversibility_class: "Reversible while margin remains sufficient; risk rises near boundary.",
      entropy_imprint_cost: "Medium; margin output affects future governance choices.",
      observer_reality_coupling: "Observer must know the computed margin and its governing formula.",
      receipt_requirement: "Recommended when margin is used to justify execution.",
      failure_mode: "Deny, degrade, or request lower-intensity transition when margin is insufficient.",
      evidence: [], milestones: [], open_questions: ["What margin bands correspond to warning, deny, or fail-closed behavior?"], neighboring_partitions: ["T1","T2","T3","T5"], merge_risk: "Low."
    },
    {
      id: "T5", name: "Observation-Lag Transition", short_name: "Observation Lag", family: "lag", status: "CANDIDATE", confidence: "C1",
      partition_claim: "A transition where the observed state may be stale relative to the commit-time state.",
      distinctness: "Distinct because uncertainty enters before decision through observation delay.",
      admissibility_boundary: "Commit-time gate must account for the lag between observation and current state.",
      authority_requirement: "Authority must be bounded by observation freshness.",
      reality_touch_condition: "The transition may bind only if admissibility is robust over observation lag.",
      reversibility_class: "Depends on whether stale observation produced external effect.",
      entropy_imprint_cost: "Medium; stale observations can imprint wrong assumptions into reality.",
      observer_reality_coupling: "Observer must know timestamp, observation source, and lag model.",
      receipt_requirement: "Recommended for transitions using stale observations.",
      failure_mode: "Fail closed, require fresh observation, or shrink allowed action.",
      evidence: [], milestones: [], open_questions: ["What lag thresholds move this from candidate to modeled?"], neighboring_partitions: ["T6","T7","T8"], merge_risk: "Medium until lag partitions are fully separated."
    },
    {
      id: "T6", name: "Decision-Lag Transition", short_name: "Decision Lag", family: "lag", status: "CANDIDATE", confidence: "C1",
      partition_claim: "A transition where computation or deliberation delay changes whether the chosen action remains admissible.",
      distinctness: "Distinct from T5 because drift occurs during decision rather than observation.",
      admissibility_boundary: "Decision gate must account for reachable states during computation delay.",
      authority_requirement: "Authority must remain valid throughout the decision window.",
      reality_touch_condition: "The action may bind only if it remains admissible across decision-lag reachable states.",
      reversibility_class: "Partially reversible when delayed choice has not yet touched external reality.",
      entropy_imprint_cost: "Medium; delayed decisions can encode outdated authority.",
      observer_reality_coupling: "Observer must reconstruct decision duration and reachable-state assumption.",
      receipt_requirement: "Recommended for delayed or queued decisions.",
      failure_mode: "Recompute, deny, or require updated state before commit.",
      evidence: [], milestones: [], open_questions: ["How should decision lag compose with model inference windows?"], neighboring_partitions: ["T5","T7"], merge_risk: "Medium."
    },
    {
      id: "T7", name: "Actuation-Lag Transition", short_name: "Actuation Lag", family: "lag", status: "CANDIDATE", confidence: "C1",
      partition_claim: "A transition where the state can change between decision and physical or external execution.",
      distinctness: "Distinct because delay occurs after decision but before effect binds.",
      admissibility_boundary: "Execution boundary must revalidate state at or near actuation.",
      authority_requirement: "Authority must still hold when the consequence is applied.",
      reality_touch_condition: "Effect may bind only if current state remains admissible after actuation lag.",
      reversibility_class: "Often less reversible than observation or decision lag because consequence is closer to reality.",
      entropy_imprint_cost: "High when actuation binds to external systems.",
      observer_reality_coupling: "Observer must compare decision state and effect-time state.",
      receipt_requirement: "Required for high-consequence domains.",
      failure_mode: "Fail closed at actuation boundary.",
      evidence: [], milestones: [], open_questions: ["Can actuation-lag gates be generalized across physical, financial, and code deployment boundaries?"], neighboring_partitions: ["T5","T6","T15"], merge_risk: "Medium."
    },
    {
      id: "T8", name: "Trust-Drift Transition", short_name: "Trust Drift", family: "lag", status: "MODELED", confidence: "C2",
      partition_claim: "A transition whose admissibility capacity changes because trust decays or shifts during the transition window.",
      distinctness: "Distinct because the trust metric is dynamic rather than merely observed late.",
      admissibility_boundary: "Commit-time gate evaluates trust-adjusted capacity.",
      authority_requirement: "Authority must be recalculated under current trust value.",
      reality_touch_condition: "The transition may bind only if trust-adjusted capacity remains sufficient.",
      reversibility_class: "Partially reversible if trust can be restored; not fully reversible if consequence already propagated.",
      entropy_imprint_cost: "Medium; trust drift changes future admissibility conditions.",
      observer_reality_coupling: "Observer must reconstruct time, trust decay, and resulting capacity.",
      receipt_requirement: "Recommended when trust drift affects an allow/deny decision.",
      failure_mode: "Deny, lower authority, or require re-attestation.",
      evidence: [], milestones: [], open_questions: ["What decay models are conservative enough for commit-time governance?"], neighboring_partitions: ["T5","T6","T9"], merge_risk: "Low to medium."
    },
    {
      id: "T9", name: "Two-State Coupled Transition", short_name: "Two-State", family: "coupled", status: "CANDIDATE", confidence: "C1",
      partition_claim: "A transition where one state mutation disturbs or depends on another state.",
      distinctness: "Distinct because admissibility is not local to a single state.",
      admissibility_boundary: "Gate must evaluate coupled post-states together.",
      authority_requirement: "Authority must span the coupled state relationship.",
      reality_touch_condition: "The transition may bind only if the coupled system remains admissible.",
      reversibility_class: "Reversibility depends on whether both states can be restored.",
      entropy_imprint_cost: "Medium to high; coupling creates cross-state trace dependencies.",
      observer_reality_coupling: "Observer must reconstruct both states and their coupling rule.",
      receipt_requirement: "Recommended when coupling crosses subsystems.",
      failure_mode: "Deny if either state becomes inadmissible or coupling is unresolved.",
      evidence: [], milestones: [], open_questions: ["How should coupled-state evidence be represented without hiding one side of the transition?"], neighboring_partitions: ["T10","T11","T12"], merge_risk: "Medium."
    },
    {
      id: "T10", name: "Multi-Agent Transition", short_name: "Multi-Agent", family: "coupled", status: "CANDIDATE", confidence: "C1",
      partition_claim: "A transition composed of multiple actors whose individually admissible actions may become inadmissible together.",
      distinctness: "Distinct because composition, not a single actor, determines admissibility.",
      admissibility_boundary: "Gate must evaluate aggregate action across agents.",
      authority_requirement: "Authority must be composed or reconciled across participating actors.",
      reality_touch_condition: "The aggregate transition may bind only if the composed result remains admissible.",
      reversibility_class: "Often compensable rather than directly reversible.",
      entropy_imprint_cost: "High when multiple actors create distributed traces.",
      observer_reality_coupling: "Observer must reconstruct actor contributions and aggregate effect.",
      receipt_requirement: "Recommended; required for high-consequence multi-agent commitments.",
      failure_mode: "Deny aggregate, require coordination, or split into governed sub-transitions.",
      evidence: [], milestones: [], open_questions: ["When does multi-agent composition require consensus rather than ordinary coupled-state checks?"], neighboring_partitions: ["T9","T11","T12"], merge_risk: "Medium."
    },
    {
      id: "T11", name: "Conflict Transition", short_name: "Conflict", family: "coupled", status: "CANDIDATE", confidence: "C1",
      partition_claim: "A transition where actions that are individually admissible become inadmissible when composed.",
      distinctness: "Distinct because conflict is detected through composition failure.",
      admissibility_boundary: "Gate must test joint outcome and conflict relationships.",
      authority_requirement: "Authority must include conflict resolution standing.",
      reality_touch_condition: "The transition may bind only after conflict is resolved or denied.",
      reversibility_class: "Often requires compensation or arbitration after conflict binds.",
      entropy_imprint_cost: "High when conflict produces external state changes or competing commitments.",
      observer_reality_coupling: "Observer must reconstruct both admissible individual actions and inadmissible composition.",
      receipt_requirement: "Required for denied or overridden conflicts.",
      failure_mode: "Fail closed, resolve priority, or require human/governed arbitration.",
      evidence: [], milestones: [], open_questions: ["Can conflict detection be made cheap enough for commit-time gating?"], neighboring_partitions: ["T3","T10","T12"], merge_risk: "Medium."
    },
    {
      id: "T12", name: "Consensus Transition", short_name: "Consensus", family: "coupled", status: "CANDIDATE", confidence: "C1",
      partition_claim: "A transition where agreement among validators contributes to authority but cannot replace invariant satisfaction.",
      distinctness: "Distinct because consensus is a legitimacy input, not the whole admissibility proof.",
      admissibility_boundary: "Gate must evaluate both consensus threshold and invariant outcome.",
      authority_requirement: "Authority derives from validator standing, weights, and active threshold.",
      reality_touch_condition: "The transition may bind only if consensus and admissibility both pass.",
      reversibility_class: "Depends on the finality model of the consensus process.",
      entropy_imprint_cost: "High; consensus creates distributed evidence and finality pressure.",
      observer_reality_coupling: "Observer must reconstruct votes, weights, threshold, and post-state check.",
      receipt_requirement: "Required when consensus binds consequence.",
      failure_mode: "Deny on insufficient consensus or invariant failure.",
      evidence: [], milestones: [], open_questions: ["How should consensus receipts compose with boundary receipts?"], neighboring_partitions: ["T10","T11","T13"], merge_risk: "Low to medium."
    },
    {
      id: "T13", name: "Receipt-Bound Transition", short_name: "Receipt-Bound", family: "evidence", status: "RECEIPT_BACKED", confidence: "C4",
      partition_claim: "A consequence-capable transition whose standing to bind consequence depends on a receipt that can be independently verified or replayed.",
      distinctness: "Distinct from ordinary logging because the receipt is not merely after-the-fact evidence; it participates in the transition's authority to bind consequence.",
      admissibility_boundary: "The execution boundary must verify the receipt before consequence is allowed.",
      authority_requirement: "Authority must be current, scoped, unexpired, and bound to the receipt.",
      reality_touch_condition: "The transition may touch reality only if the receipt validates at the consequence boundary.",
      reversibility_class: "Partially reversible. The receipt can reconstruct the authorization basis, but downstream consequence may require compensation rather than reversal.",
      entropy_imprint_cost: "Medium to high. The transition creates a durable proof trace and may alter external state.",
      observer_reality_coupling: "An observer can reconstruct why the transition was allowed by inspecting the receipt, boundary condition, and replay evidence.",
      receipt_requirement: "Required.",
      failure_mode: "Fail closed if the receipt is invalid, expired, missing, or mismatched.",
      evidence: ["EV-MS012-REPLAY-PACKET"], milestones: ["MS-012"], open_questions: ["What is the minimal receipt structure required for cross-domain replay?", "How should receipt expiration interact with delayed consequence?"], neighboring_partitions: ["T12","T14"], merge_risk: "Low."
    },
    {
      id: "T14", name: "Reconstruction-Equality Transition", short_name: "Reconstruction", family: "evidence", status: "RECEIPT_BACKED", confidence: "C4",
      partition_claim: "A transition whose public evidence supports reconstruction of the claimed end-state and exposes mismatch or unexplained variance.",
      distinctness: "Distinct from T13 because the central question is not only whether a receipt exists, but whether observed state can be reconstructed from released evidence.",
      admissibility_boundary: "Boundary compares expected reconstruction against observed or claimed state.",
      authority_requirement: "Authority must include standing to assert the reconstruction basis.",
      reality_touch_condition: "The transition may remain evidence-backed only if reconstruction equality or declared variance holds.",
      reversibility_class: "Usually not direct reversal; supports reconstruction, dispute, compensation, or audit.",
      entropy_imprint_cost: "High. Reconstruction produces a durable evidence trail and preserves unexplained variance rather than hiding it.",
      observer_reality_coupling: "Observer reconstructs the state from receipts, artifacts, outputs, and declared gaps.",
      receipt_requirement: "Required.",
      failure_mode: "If reconstruction fails, the transition cannot remain receipt-backed under the current snapshot.",
      evidence: ["EV-MS012-REPLAY-PACKET"], milestones: ["MS-012"], open_questions: ["What confidence threshold is required before reconstruction evidence promotes a partition?", "How should unexplained variance be represented in the table?"], neighboring_partitions: ["T13","T15"], merge_risk: "Low."
    },
    {
      id: "T15", name: "Irreversible Transition", short_name: "Irreversible", family: "open", status: "OBSERVED", confidence: "C1",
      partition_claim: "A transition that crosses a point after which no admissible reverse transition is available.",
      distinctness: "Distinct because governance must evaluate consequence before a point of no return rather than relying on reversal.",
      admissibility_boundary: "Boundary must occur before irreversibility, not after effect.",
      authority_requirement: "Authority must include standing to bind irreversible consequence.",
      reality_touch_condition: "May bind only after heightened admissibility, receipt, and recovery checks.",
      reversibility_class: "Irreversible; may allow compensation or record-only reconstruction.",
      entropy_imprint_cost: "Very high; irreversible transitions permanently alter reachable state space.",
      observer_reality_coupling: "Observer must know the irreversible boundary and whether it was crossed under valid authority.",
      receipt_requirement: "Required for any promoted irreversible transition.",
      failure_mode: "Fail closed before the point of irreversibility.",
      evidence: [], milestones: [], open_questions: ["How should point-of-no-return geometry be represented in the transition lattice?"], neighboring_partitions: ["T7","T14","T16"], merge_risk: "Low."
    },
    {
      id: "T16", name: "Self-Modifying Transition", short_name: "Self-Modifying", family: "open", status: "LOCKED", confidence: "C0",
      partition_claim: "Reserved region for transitions that modify the governing rules, invariant, or admissibility model itself.",
      distinctness: "Not yet publicly partitioned. The region is visible to prevent silent overclaiming.",
      admissibility_boundary: "Unknown; likely requires meta-governance and rollback-safe rule migration.",
      authority_requirement: "Unknown; likely requires explicit authority to alter the rule system.",
      reality_touch_condition: "No public unlock claim yet.",
      reversibility_class: "Unknown; potentially irreversible if rule changes rewrite future admissibility.",
      entropy_imprint_cost: "Unknown, likely high.",
      observer_reality_coupling: "Unknown; observer must be able to distinguish rule change from ordinary state transition.",
      receipt_requirement: "Expected to be required, but not yet claimed.",
      failure_mode: "Remain locked until a public evidence threshold is defined.",
      evidence: [], milestones: [], open_questions: ["What would make self-modification admissible without retroactive governance collapse?"], neighboring_partitions: ["T15"], merge_risk: "Unknown."
    }
  ],
  evidence_records: [
    {
      id: "EV-T1-PRIMITIVE-SWEEP",
      type: "sandbox_result",
      title: "Primitive admissibility sweep",
      status: "internal_seeded",
      supports: ["T1"],
      expected_verdict: "ALLOW/DENY classification",
      actual_verdict: "seeded tested baseline",
      evidence_meaning: "Supports T1 as a sandbox-tested baseline transition.",
      public_page: "transition-table.html",
      verification_page: "transition-verification-guide.html",
      related_snapshot: null,
      limitations: ["Baseline evidence only; does not promote the entire table."]
    },
    {
      id: "EV-MS012-REPLAY-PACKET",
      type: "replay_packet",
      title: "MS-012 Independent Replay Packet",
      status: "public",
      supports: ["T13","T14"],
      expected_verdict: "ALLOW",
      actual_verdict: "ALLOW",
      evidence_meaning: "Supports the claim that T13/T14 can be reconstructed from public replay evidence.",
      public_page: "transition-replay-packet.html",
      verification_page: "transition-verification-guide.html",
      related_snapshot: "MS-012",
      limitations: ["Supports the named transitions only.", "Does not prove the table is complete.", "Does not promote unrelated candidate partitions."]
    }
  ],
  milestones: [
    {
      id: "MS-012",
      title: "Independent Replay Packet",
      status: "released",
      date: "2026-05-11",
      discovery_meaning: "T13/T14 crossed into receipt-backed replayable transition partitions.",
      threshold_crossed: [
        { partition: "T13", from: "SANDBOXED", to: "RECEIPT_BACKED" },
        { partition: "T14", from: "SANDBOXED", to: "RECEIPT_BACKED" }
      ],
      affected_partitions: ["T13","T14"],
      evidence: ["EV-MS012-REPLAY-PACKET"],
      unresolved_questions: ["Whether sandbox repair will produce new partitions, merge candidates into existing classes, or deprecate obsolete transition purposes."],
      next_frontier: "MS-012F"
    },
    {
      id: "MS-011",
      title: "Public Verification Bundle",
      status: "released",
      date: null,
      discovery_meaning: "The transition research surface gained reader-facing verification pathways.",
      threshold_crossed: [],
      affected_partitions: [],
      evidence: [],
      unresolved_questions: ["Verification had to become tied to transition claims rather than page presence alone."],
      next_frontier: "MS-012"
    },
    {
      id: "MS-010",
      title: "Public Navigation Integration",
      status: "released",
      date: null,
      discovery_meaning: "The transition research surface became publicly navigable.",
      threshold_crossed: [],
      affected_partitions: [],
      evidence: [],
      unresolved_questions: ["Navigation did not yet guarantee release-state consistency."],
      next_frontier: "MS-011"
    }
  ],
  frontier: {
    id: "MS-012F",
    title: "Sandbox Repair and Candidate Construction",
    status: "frontier",
    research_question: "Can sandbox repair and candidate construction produce stable new transition partitions, or do observed candidates collapse into existing transition classes?",
    active_work: [
      "Identify stale bundles and determine whether their transition purpose is deprecated.",
      "Distinguish repairable transition candidates from obsolete ones.",
      "Construct candidate partitions for sandbox testing.",
      "Assign evidence thresholds before promotion.",
      "Route failed, stale, privileged, and dependency-sensitive bundles through declared tasks rather than hardcoded workflow assumptions."
    ],
    candidate_outcomes: ["promote_candidate", "merge_candidate", "deprecate_candidate", "return_to_observed", "repair_required"],
    unlock_condition: "At least one candidate transition must cross from CANDIDATE to PARTITIONED or from MODELED to SANDBOXED with public evidence.",
    blockers: [
      "Sandbox repair evidence must classify stale incoming bundles.",
      "Candidate partitions need explicit distinctness claims before promotion.",
      "Public pages must render from this single discovery state to prevent milestone drift."
    ]
  },
  snapshots: [
    {
      id: "MS-012",
      title: "Independent Replay Packet Snapshot",
      status: "released",
      knows: [
        "T13 has public replay-backed evidence.",
        "T14 has public replay-backed evidence.",
        "MS-012F is the current research frontier.",
        "The public page system now treats release state as downstream of transition discovery state."
      ],
      does_not_claim: [
        "The Transition Periodic Table is complete.",
        "All transition partitions have been discovered.",
        "Candidate partitions are promoted.",
        "Locked blocks are empty or irrelevant.",
        "Replay evidence for T13/T14 proves unrelated transition classes."
      ],
      receipt_backed_partitions: ["T13","T14"],
      promoted_partitions: [],
      candidate_partitions: ["T5","T6","T7","T9","T10","T11","T12"],
      frontier: "MS-012F"
    }
  ],
  verification_expectations: {
    current_release: "MS-012",
    expected_frontier: "MS-012F",
    expected_receipt_backed_partitions: ["T13","T14"],
    expected_replay_verdict: "ALLOW",
    expected_page_contract_failures: 0,
    stale_state_warnings: [
      "A page names MS-010 or MS-011 as current after MS-012 is released.",
      "A replay packet says MS-012 is pending while milestones say MS-012 is released.",
      "A block is RECEIPT_BACKED without an evidence record.",
      "An evidence record supports a block that does not reference it.",
      "A release snapshot omits the current frontier."
    ],
    block_verification_procedure: [
      "Confirm the partition appears in the canonical transition discovery state.",
      "Confirm the partition status matches the page claim.",
      "Confirm any RECEIPT_BACKED partition references at least one public evidence record.",
      "Confirm the evidence record lists the partition in supports.",
      "Confirm the current release snapshot includes the claim or explicitly limits it.",
      "Confirm no stale-state warning is triggered."
    ]
  },
  replay_packets: [
    {
      id: "RP-MS012-T13-T14",
      title: "MS-012 T13/T14 Replay Packet",
      status: "public",
      supports: ["T13","T14"],
      replay_claims: [
        { partition: "T13", claim: "Receipt binding can be checked from public evidence.", expected_result: "ALLOW", actual_result: "ALLOW", failure_condition: "If receipt binding fails, T13 cannot remain RECEIPT_BACKED under MS-012." },
        { partition: "T14", claim: "Reconstruction equality can be checked from public evidence.", expected_result: "ALLOW", actual_result: "ALLOW", failure_condition: "If reconstruction equality fails, T14 cannot remain RECEIPT_BACKED under MS-012." }
      ],
      limitations: [
        "This replay packet supports only the named transitions.",
        "It does not claim completeness of the table.",
        "It does not promote candidate partitions outside the packet."
      ]
    }
  ]
};
