(() => {
  'use strict';

  const FIELD_STATUSES = Object.freeze(['AVAILABLE', 'ABSENT', 'UNKNOWN', 'RESTRICTED', 'CONFLICTED', 'SECONDARY_DERIVED']);
  const SOURCE_ACCESS = Object.freeze(['OPEN', 'RESTRICTED', 'LICENSED', 'UNKNOWN', 'UNAVAILABLE']);
  const COMPOSITION_USE = Object.freeze(['ALLOW_DERIVED_ANALYSIS', 'ALLOW_REFERENCE_ONLY', 'REQUIRES_REVIEW', 'PROHIBITED', 'UNKNOWN']);
  const clone = (value) => JSON.parse(JSON.stringify(value));
  const now = () => new Date().toISOString();

  async function sha256(value) {
    const bytes = new TextEncoder().encode(typeof value === 'string' ? value : JSON.stringify(value));
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function assertEnum(value, allowed, label) {
    if (!allowed.includes(value)) throw new Error(`${label} must be one of ${allowed.join(', ')}`);
  }

  function normalizeSourceRecord(input = {}) {
    const fieldStatus = input.field_status || input.fieldStatus || 'UNKNOWN';
    assertEnum(fieldStatus, FIELD_STATUSES, 'field_status');
    return {
      source_id: input.source_id || input.sourceId || 'UNKNOWN_SOURCE',
      priority: Number.isInteger(input.priority) && input.priority > 0 ? input.priority : 999,
      field_status: fieldStatus,
      retrieved_at: input.retrieved_at || input.retrievedAt || now(),
      response_hash: input.response_hash || input.responseHash || null,
      provenance_path: clone(input.provenance_path || input.provenancePath || []),
      adopted_fields: clone(input.adopted_fields || input.adoptedFields || []),
      missing_fields: clone(input.missing_fields || input.missingFields || []),
      native_record: clone(input.native_record || input.nativeRecord || null),
      mapping_confidence: input.mapping_confidence || input.mappingConfidence || 'UNRESOLVED',
      uncertainty: clone(input.uncertainty || []),
      authority: 'none'
    };
  }

  function buildSourceIndex(records = []) {
    return records.map(normalizeSourceRecord).sort((a, b) => a.priority - b.priority);
  }

  function deriveConfidence(sourceRecords = [], conflicts = [], uncertainties = []) {
    const weighted = sourceRecords.reduce((total, record) => {
      const statusWeight = {
        AVAILABLE: 1,
        SECONDARY_DERIVED: 0.75,
        CONFLICTED: 0.35,
        RESTRICTED: 0.25,
        UNKNOWN: 0.1,
        ABSENT: 0
      }[record.field_status] ?? 0;
      return total + statusWeight / Math.max(1, record.priority);
    }, 0);
    const denominator = sourceRecords.reduce((total, record) => total + 1 / Math.max(1, record.priority), 0) || 1;
    const penalty = Math.min(0.6, conflicts.length * 0.1 + uncertainties.length * 0.03);
    return Math.max(0, Math.min(1, weighted / denominator - penalty));
  }

  function assertRightsPosture(rights = {}) {
    assertEnum(rights.source_access_posture, SOURCE_ACCESS, 'source_access_posture');
    assertEnum(rights.composition_use_posture, COMPOSITION_USE, 'composition_use_posture');
    if (rights.composition_use_posture === 'PROHIBITED' && rights.audio_custody_authorized) {
      throw new Error('Prohibited composition use cannot authorize source-audio custody');
    }
  }

  async function buildSongReference(input = {}) {
    const sourceRecords = buildSourceIndex(input.sourceRecords || []);
    const rights = {
      source_access_posture: input.sourceAccessPosture || 'UNKNOWN',
      composition_use_posture: input.compositionUsePosture || 'UNKNOWN',
      audio_custody_authorized: Boolean(input.audioCustodyAuthorized),
      restrictions: clone(input.restrictions || []),
      evidence_refs: clone(input.rightsEvidenceRefs || [])
    };
    assertRightsPosture(rights);

    const conflicts = clone(input.conflicts || []);
    const uncertainties = clone(input.uncertainties || []);
    const reference = {
      schema_version: '1.0.0',
      song_reference_id: input.songReferenceId || `song-reference-${Date.now()}-${Math.random().toString(16).slice(2)}`,
      identity: {
        work_identity: input.workIdentity ?? null,
        recording_identity: input.recordingIdentity ?? null,
        release_identity: input.releaseIdentity ?? null,
        external_ids: clone(input.externalIds || {})
      },
      source_records: sourceRecords,
      historical_context: clone(input.historicalContext || {
        composition_period: null,
        performance_period: null,
        recording_date: null,
        arrangement_date: null,
        technology_period: null,
        transmission_period: null,
        revival_or_reinterpretation_period: null,
        lineage_edges: []
      }),
      audience_and_place: clone(input.audienceAndPlace || {
        place: null,
        region: null,
        community_or_scene: null,
        audience: [],
        social_function: [],
        performance_setting: null,
        room_or_environment: {}
      }),
      musical_map: clone(input.musicalMap || {
        tempo: {}, meter: {}, pitch_and_tuning: {}, harmony: {}, rhythm: {}, melodic_contour: {},
        cadences: [], phrases: [], sections: [], microtiming: {}, dynamics: {}, timbre_and_spectrum: {}, variation_events: []
      }),
      performance_map: clone(input.performanceMap || {
        performers: [], instruments_and_tools: [], role_events: [], interaction_graph: {}, handoffs: [],
        interruptions: [], failures_repairs_and_recovery: [], room_and_proximity: {}
      }),
      rights_and_access: rights,
      provenance: {
        created_at: input.createdAt || now(),
        extractor_versions: clone(input.extractorVersions || {}),
        source_hashes: clone(input.sourceHashes || sourceRecords.map((record) => record.response_hash).filter(Boolean)),
        normalization_version: input.normalizationVersion || 'stegmusic-song-reference-builder-v1',
        builder_hash: null
      },
      confidence: {
        overall: deriveConfidence(sourceRecords, conflicts, uncertainties),
        uncertainties,
        conflicts
      },
      authority: 'none'
    };

    reference.provenance.builder_hash = await sha256({ ...reference, provenance: { ...reference.provenance, builder_hash: null } });
    return Object.freeze(reference);
  }

  function compositionEligibility(reference) {
    const posture = reference && reference.rights_and_access && reference.rights_and_access.composition_use_posture;
    const blockers = [];
    if (!reference || !reference.provenance || !reference.provenance.builder_hash) blockers.push('missing_builder_hash');
    if (!reference || !Array.isArray(reference.source_records) || !reference.source_records.length) blockers.push('missing_source_records');
    if (posture === 'PROHIBITED') blockers.push('composition_use_prohibited');
    if (posture === 'REQUIRES_REVIEW' || posture === 'UNKNOWN') blockers.push('composition_use_requires_review');
    return {
      eligible_for_derived_analysis: posture === 'ALLOW_DERIVED_ANALYSIS' && blockers.length === 0,
      eligible_for_reference_only: ['ALLOW_DERIVED_ANALYSIS', 'ALLOW_REFERENCE_ONLY'].includes(posture) && !blockers.includes('missing_builder_hash'),
      blockers,
      authority: 'none'
    };
  }

  window.StegMusicSongReferenceBuilder = Object.freeze({
    fieldStatuses: FIELD_STATUSES,
    sourceAccessPostures: SOURCE_ACCESS,
    compositionUsePostures: COMPOSITION_USE,
    normalizeSourceRecord,
    buildSourceIndex,
    deriveConfidence,
    assertRightsPosture,
    buildSongReference,
    compositionEligibility,
    sha256
  });
})();
