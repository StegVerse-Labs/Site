(() => {
  'use strict';

  const AVAILABILITY = Object.freeze(['AVAILABLE', 'ABSENT', 'UNKNOWN', 'RESTRICTED', 'CONFLICTED']);
  const MAPPING_CONFIDENCE = Object.freeze(['EXACT', 'HIGH_CONFIDENCE', 'PARTIAL', 'INTERPRETIVE', 'UNRESOLVED']);
  const STORAGE_POSTURES = Object.freeze(['STORE', 'QUERY', 'FREEZE_AFTER_QUERY']);

  const clone = (value) => JSON.parse(JSON.stringify(value));
  const now = () => new Date().toISOString();

  function assertEnum(value, allowed, label) {
    if (!allowed.includes(value)) throw new Error(`${label} must be one of ${allowed.join(', ')}`);
  }

  async function sha256(value) {
    const text = typeof value === 'string' ? value : JSON.stringify(value);
    const bytes = new TextEncoder().encode(text);
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function createSourceObservation(input = {}) {
    const availability = input.availability || 'UNKNOWN';
    const mappingConfidence = input.mappingConfidence || 'UNRESOLVED';
    assertEnum(availability, AVAILABILITY, 'availability');
    assertEnum(mappingConfidence, MAPPING_CONFIDENCE, 'mappingConfidence');
    return {
      observationId: input.observationId || `obs-${Date.now()}-${Math.random().toString(16).slice(2)}`,
      sourceName: input.sourceName || 'UNKNOWN_SOURCE',
      sourcePriority: Number.isFinite(input.sourcePriority) ? input.sourcePriority : null,
      sourceRecordId: input.sourceRecordId || null,
      canonicalField: input.canonicalField || null,
      sourceNativeField: input.sourceNativeField || null,
      sourceNativeValue: input.sourceNativeValue ?? null,
      normalizedValue: input.normalizedValue ?? null,
      availability,
      mappingConfidence,
      confidence: Number.isFinite(input.confidence) ? Math.max(0, Math.min(1, input.confidence)) : 0,
      uncertainty: input.uncertainty || [],
      rightsAndAccess: input.rightsAndAccess || { status: 'UNKNOWN', evidenceRefs: [] },
      retrievedAt: input.retrievedAt || now(),
      sourceVersionOrSnapshot: input.sourceVersionOrSnapshot || null,
      requestHash: input.requestHash || null,
      responseHash: input.responseHash || null,
      authority: 'none'
    };
  }

  function resolveField(primary, secondaryCandidates = []) {
    const primaryObservation = createSourceObservation(primary);
    const candidates = secondaryCandidates.map(createSourceObservation)
      .sort((a, b) => (a.sourcePriority ?? 999) - (b.sourcePriority ?? 999));

    if (primaryObservation.availability === 'AVAILABLE') {
      return {
        status: 'PRIMARY_ADOPTED',
        adopted: primaryObservation,
        primary: primaryObservation,
        secondaryCandidates: candidates,
        unresolvedPrimaryState: null,
        authority: 'none'
      };
    }

    const adoptedSecondary = candidates.find((candidate) => candidate.availability === 'AVAILABLE');
    if (!adoptedSecondary) {
      return {
        status: 'UNRESOLVED',
        adopted: null,
        primary: primaryObservation,
        secondaryCandidates: candidates,
        unresolvedPrimaryState: primaryObservation.availability,
        authority: 'none'
      };
    }

    return {
      status: 'SECONDARY_DERIVED',
      adopted: {
        ...adoptedSecondary,
        derivationState: 'SECONDARY_DERIVED',
        primaryObservationId: primaryObservation.observationId,
        primaryAvailability: primaryObservation.availability
      },
      primary: primaryObservation,
      secondaryCandidates: candidates,
      unresolvedPrimaryState: primaryObservation.availability,
      authority: 'none'
    };
  }

  function decideStoragePosture(input = {}) {
    const material = [
      input.compositionInfluence,
      input.upstreamVolatility,
      input.recomputationCost,
      input.replayNecessity,
      input.rightsSensitivity,
      input.conflictRelevance,
      input.corpusReuseValue
    ].some(Boolean);

    if (input.queried && input.compositionInfluence) return 'FREEZE_AFTER_QUERY';
    if (material) return 'STORE';
    return 'QUERY';
  }

  async function freezeEvidence(input = {}) {
    const storagePosture = input.storagePosture || decideStoragePosture({ ...input, queried: true });
    assertEnum(storagePosture, STORAGE_POSTURES, 'storagePosture');
    const packet = {
      schemaVersion: '1.0.0',
      evidencePacketId: input.evidencePacketId || `evidence-${Date.now()}-${Math.random().toString(16).slice(2)}`,
      compositionRequestId: input.compositionRequestId || null,
      retrievals: clone(input.retrievals || []),
      sourceGaps: clone(input.sourceGaps || []),
      secondarySubstitutions: clone(input.secondarySubstitutions || []),
      conflicts: clone(input.conflicts || []),
      adoptedValues: clone(input.adoptedValues || []),
      compositionEffects: clone(input.compositionEffects || []),
      storagePosture,
      frozen: true,
      mutableAfterFreeze: false,
      frozenAt: now(),
      compositionMayExecute: Boolean(input.compositionMayExecute),
      executionBlockers: clone(input.executionBlockers || []),
      authority: 'none'
    };
    packet.evidenceHash = await sha256(packet);
    return Object.freeze(packet);
  }

  function createCompositionEvidenceSession(input = {}) {
    const state = {
      compositionRequestId: input.compositionRequestId || `request-${Date.now()}-${Math.random().toString(16).slice(2)}`,
      observations: [],
      resolutions: [],
      frozenPacket: null
    };

    return Object.freeze({
      addObservation(observation) {
        if (state.frozenPacket) throw new Error('Evidence session is frozen');
        const normalized = createSourceObservation(observation);
        state.observations.push(normalized);
        return clone(normalized);
      },
      resolve(primaryObservationId, secondaryObservationIds = []) {
        if (state.frozenPacket) throw new Error('Evidence session is frozen');
        const primary = state.observations.find((item) => item.observationId === primaryObservationId);
        if (!primary) throw new Error(`Unknown primary observation: ${primaryObservationId}`);
        const secondary = secondaryObservationIds.map((id) => {
          const found = state.observations.find((item) => item.observationId === id);
          if (!found) throw new Error(`Unknown secondary observation: ${id}`);
          return found;
        });
        const resolution = resolveField(primary, secondary);
        state.resolutions.push(resolution);
        return clone(resolution);
      },
      async freeze(options = {}) {
        if (state.frozenPacket) return state.frozenPacket;
        const packet = await freezeEvidence({
          compositionRequestId: state.compositionRequestId,
          retrievals: state.observations,
          sourceGaps: state.resolutions.filter((item) => item.unresolvedPrimaryState),
          secondarySubstitutions: state.resolutions.filter((item) => item.status === 'SECONDARY_DERIVED'),
          adoptedValues: state.resolutions.filter((item) => item.adopted).map((item) => item.adopted),
          ...options
        });
        state.frozenPacket = packet;
        return packet;
      },
      snapshot() {
        return clone(state);
      }
    });
  }

  window.StegMusicSourceEvidence = Object.freeze({
    availabilityStates: AVAILABILITY,
    mappingConfidenceStates: MAPPING_CONFIDENCE,
    storagePostures: STORAGE_POSTURES,
    createSourceObservation,
    resolveField,
    decideStoragePosture,
    freezeEvidence,
    createCompositionEvidenceSession,
    sha256
  });
})();
