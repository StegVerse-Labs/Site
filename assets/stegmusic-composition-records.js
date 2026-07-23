(() => {
  'use strict';

  const clone = (value) => JSON.parse(JSON.stringify(value));
  const now = () => new Date().toISOString();

  async function sha256(value) {
    const bytes = new TextEncoder().encode(typeof value === 'string' ? value : JSON.stringify(value));
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function buildCompositionRequest(input = {}) {
    const blockers = Array.from(new Set(input.blockers || []));
    const rightsGatePassed = Boolean(input.rightsGatePassed);
    const evidenceFrozen = Boolean(input.evidenceFrozen);
    const compositionMayExecute = evidenceFrozen && rightsGatePassed && blockers.length === 0;

    return {
      schema_version: '1.0.0',
      composition_request_id: input.compositionRequestId || `composition-request-${Date.now()}`,
      created_at: input.createdAt || now(),
      profile_scope: {
        profile_id: input.profileId || '',
        scope_id: input.scopeId || '',
        consent_ref: input.consentRef || '',
        allowed_personalization_signals: clone(input.allowedPersonalizationSignals || [])
      },
      session_intent: {
        intent_id: input.intentId || '',
        direction: input.direction || '',
        intensity: Number(input.intensity) || 0,
        duration_target_seconds: Number(input.durationTargetSeconds) || 1,
        explicit_user_text: input.explicitUserText ?? null
      },
      cultural_scope: {
        traditions: clone(input.traditions || []),
        historical_fidelity_target: Number(input.historicalFidelityTarget) || 0,
        innovation_distance: Number(input.innovationDistance) || 0,
        excluded_claims: clone(input.excludedClaims || [])
      },
      historical_scope: {
        periods: clone(input.periods || []),
        recording_technology_posture: input.recordingTechnologyPosture || 'UNSPECIFIED',
        allowed_revival_or_reinterpretation: Boolean(input.allowedRevivalOrReinterpretation)
      },
      audience_and_place_scope: {
        audience_function: clone(input.audienceFunction || []),
        place_conditioning: clone(input.placeConditioning || []),
        room_or_environment_profile: input.roomOrEnvironmentProfile ?? null
      },
      novelty_and_familiarity: {
        familiarity: Number(input.familiarity) || 0,
        novelty: Number(input.novelty) || 0,
        seed_influence: Number(input.seedInfluence) || 0,
        profile_influence: Number(input.profileInfluence) || 0
      },
      instrument_and_tool_availability: clone(input.instrumentAndToolAvailability || []),
      rights_constraints: {
        protected_expression_copying_prohibited: true,
        artist_voice_imitation_prohibited: true,
        source_audio_use: input.sourceAudioUse === 'AUTHORIZED_ONLY' ? 'AUTHORIZED_ONLY' : 'NONE',
        required_rights_evidence_refs: clone(input.requiredRightsEvidenceRefs || [])
      },
      evidence_requirements: {
        frozen_evidence_packet_id: input.frozenEvidencePacketId || '',
        required_song_references: clone(input.requiredSongReferences || []),
        required_corpus_references: clone(input.requiredCorpusReferences || []),
        unresolved_conflicts: clone(input.unresolvedConflicts || [])
      },
      execution_gate: {
        evidence_frozen: evidenceFrozen,
        rights_gate_passed: rightsGatePassed,
        composition_may_execute: compositionMayExecute,
        blockers
      },
      authority: 'none'
    };
  }

  function assertExecutable(request) {
    const gate = request && request.execution_gate;
    if (!gate || !gate.evidence_frozen) throw new Error('Composition evidence is not frozen');
    if (!gate.rights_gate_passed) throw new Error('Composition rights gate did not pass');
    if (!gate.composition_may_execute || (gate.blockers || []).length) throw new Error('Composition execution is blocked');
    return true;
  }

  async function buildCompositionReceipt(request, result = {}) {
    assertExecutable(request);
    const receipt = {
      schema_version: '1.0.0',
      composition_id: result.compositionId || `composition-${Date.now()}`,
      composition_request_id: request.composition_request_id,
      created_at: result.createdAt || now(),
      frozen_evidence_packet_id: request.evidence_requirements.frozen_evidence_packet_id,
      song_references: clone(result.songReferences || request.evidence_requirements.required_song_references || []),
      corpus_references: clone(result.corpusReferences || request.evidence_requirements.required_corpus_references || []),
      selected_conditions: clone(result.selectedConditions || {
        cultural: request.cultural_scope.traditions,
        historical: request.historical_scope.periods,
        audience: request.audience_and_place_scope.audience_function,
        place: request.audience_and_place_scope.place_conditioning,
        intent: request.session_intent.intent_id
      }),
      generation_state: clone(result.generationState || {}),
      performer_role_graph: clone(result.performerRoleGraph || { performers: [], roles: [], assignments: [], handoffs: [] }),
      instrument_and_tool_states: clone(result.instrumentAndToolStates || []),
      continuity_events: clone(result.continuityEvents || []),
      rights_and_originality_decision: clone(result.rightsAndOriginalityDecision || {
        decision: 'ESCALATE', protected_expression_risk: 0, artist_voice_risk: 0, evidence_refs: [], blockers: ['decision_not_supplied']
      }),
      evaluation_results: clone(result.evaluationResults || {
        cultural_credibility: 0, instrument_realism: 0, ensemble_interaction: 0, mechanical_artifact_risk: 1, blind_test_ref: null
      }),
      artifacts: clone(result.artifacts || []),
      provenance_disclosure: {
        generated_origin_disclosed: true,
        disclosure_text: result.disclosureText || 'This composition was generated by StegDJ from governed evidence and original synthesis.',
        disclosed_at: result.disclosedAt || now()
      },
      confidence_and_uncertainty: clone(result.confidenceAndUncertainty || { overall_confidence: 0, uncertainties: [], conflicts: [] }),
      receipt_hash: '',
      authority: 'none'
    };
    receipt.receipt_hash = await sha256({ ...receipt, receipt_hash: '' });
    return Object.freeze(receipt);
  }

  window.StegMusicCompositionRecords = Object.freeze({
    buildCompositionRequest,
    assertExecutable,
    buildCompositionReceipt,
    sha256
  });
})();
