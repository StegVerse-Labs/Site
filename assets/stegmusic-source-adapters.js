(() => {
  'use strict';

  const SOURCES = Object.freeze({
    GLOBAL_JUKEBOX: { id: 'global-jukebox', priority: 1 },
    DUNYA_COMPMUSIC: { id: 'dunya-compmusic', priority: 2 },
    MUSICBRAINZ: { id: 'musicbrainz', priority: 3 },
    ACOUSTICBRAINZ: { id: 'acousticbrainz', priority: 4 },
    NATIONAL_JUKEBOX: { id: 'loc-national-jukebox', priority: 5 },
    DOREMUS: { id: 'doremus', priority: 6 },
    RISM: { id: 'rism', priority: 7 },
    MILLION_SONG_DATASET: { id: 'million-song-dataset', priority: 8 }
  });

  const clone = (value) => JSON.parse(JSON.stringify(value));
  const now = () => new Date().toISOString();

  function field(value, nativePath, confidence = 'DIRECT') {
    const absent = value === undefined || value === null || value === '';
    return {
      status: absent ? 'ABSENT' : 'AVAILABLE',
      native_value: absent ? null : clone(value),
      normalized_value: absent ? null : clone(value),
      native_path: nativePath,
      mapping_confidence: absent ? 'UNRESOLVED' : confidence,
      uncertainty: []
    };
  }

  function baseObservation(source, nativeRecord, fields, options = {}) {
    const sourceHash = options.responseHash || null;
    return {
      schema_version: '1.0.0',
      source_id: source.id,
      priority: source.priority,
      retrieved_at: options.retrievedAt || now(),
      response_hash: sourceHash,
      provenance_path: clone(options.provenancePath || [source.id]),
      native_record: clone(nativeRecord),
      fields,
      restrictions: clone(options.restrictions || []),
      authority: 'none'
    };
  }

  function adaptGlobalJukebox(record = {}, options = {}) {
    return baseObservation(SOURCES.GLOBAL_JUKEBOX, record, {
      cultural_context: field(record.society || record.culture, 'society|culture'),
      place: field(record.region || record.location, 'region|location'),
      social_function: field(record.function || record.context, 'function|context'),
      musical_structure: field(record.cantometrics || record.features, 'cantometrics|features')
    }, options);
  }

  function adaptDunya(record = {}, options = {}) {
    return baseObservation(SOURCES.DUNYA_COMPMUSIC, record, {
      work_identity: field(record.title, 'title'),
      cultural_context: field(record.raaga || record.makam || record.tradition, 'raaga|makam|tradition'),
      musical_structure: field(record.sections || record.form, 'sections|form'),
      pitch_and_tuning: field(record.tonic || record.pitch, 'tonic|pitch')
    }, options);
  }

  function adaptMusicBrainz(record = {}, options = {}) {
    return baseObservation(SOURCES.MUSICBRAINZ, record, {
      work_identity: field(record.work?.id || record.id, 'work.id|id'),
      recording_identity: field(record.recording?.id || record.id, 'recording.id|id'),
      release_identity: field(record.release?.id || record.release_id, 'release.id|release_id'),
      performer_identity: field(record['artist-credit'] || record.artist_credit, 'artist-credit|artist_credit')
    }, options);
  }

  function adaptAcousticBrainz(record = {}, options = {}) {
    return baseObservation(SOURCES.ACOUSTICBRAINZ, record, {
      tempo: field(record.rhythm?.bpm || record.lowlevel?.bpm, 'rhythm.bpm|lowlevel.bpm'),
      meter: field(record.rhythm?.beats_count || record.rhythm?.meter, 'rhythm.beats_count|rhythm.meter'),
      timbre_and_acoustics: field(record.lowlevel || record.tonal, 'lowlevel|tonal'),
      dynamics: field(record.lowlevel?.average_loudness, 'lowlevel.average_loudness')
    }, options);
  }

  function adaptNationalJukebox(record = {}, options = {}) {
    return baseObservation(SOURCES.NATIONAL_JUKEBOX, record, {
      recording_identity: field(record.id || record.recording_id, 'id|recording_id'),
      recording_date: field(record.date || record.recording_date, 'date|recording_date'),
      place: field(record.place || record.location, 'place|location'),
      performer_identity: field(record.performers || record.contributors, 'performers|contributors')
    }, options);
  }

  function adaptDoremus(record = {}, options = {}) {
    return baseObservation(SOURCES.DOREMUS, record, {
      work_identity: field(record.work || record['@id'], 'work|@id'),
      performer_identity: field(record.cast || record.performer, 'cast|performer'),
      performance_period: field(record.performanceDate || record.date, 'performanceDate|date'),
      instrumentation: field(record.medium || record.instrumentation, 'medium|instrumentation')
    }, options);
  }

  function adaptRism(record = {}, options = {}) {
    return baseObservation(SOURCES.RISM, record, {
      work_identity: field(record.id || record.siglum, 'id|siglum'),
      composition_period: field(record.date || record.dating, 'date|dating'),
      place: field(record.provenance || record.place, 'provenance|place'),
      instrumentation: field(record.scoring || record.incipits, 'scoring|incipits')
    }, options);
  }

  function adaptMillionSongDataset(record = {}, options = {}) {
    return baseObservation(SOURCES.MILLION_SONG_DATASET, record, {
      recording_identity: field(record.track_id, 'track_id'),
      work_identity: field(record.song_id, 'song_id'),
      tempo: field(record.tempo, 'tempo'),
      musical_structure: field(record.sections_start || record.segments_start, 'sections_start|segments_start')
    }, options);
  }

  const adapters = Object.freeze({
    [SOURCES.GLOBAL_JUKEBOX.id]: adaptGlobalJukebox,
    [SOURCES.DUNYA_COMPMUSIC.id]: adaptDunya,
    [SOURCES.MUSICBRAINZ.id]: adaptMusicBrainz,
    [SOURCES.ACOUSTICBRAINZ.id]: adaptAcousticBrainz,
    [SOURCES.NATIONAL_JUKEBOX.id]: adaptNationalJukebox,
    [SOURCES.DOREMUS.id]: adaptDoremus,
    [SOURCES.RISM.id]: adaptRism,
    [SOURCES.MILLION_SONG_DATASET.id]: adaptMillionSongDataset
  });

  function adapt(sourceId, nativeRecord, options = {}) {
    const adapter = adapters[sourceId];
    if (!adapter) throw new Error(`Unsupported StegMusic source adapter: ${sourceId}`);
    return Object.freeze(adapter(nativeRecord, options));
  }

  window.StegMusicSourceAdapters = Object.freeze({ SOURCES, adapters, adapt });
})();
