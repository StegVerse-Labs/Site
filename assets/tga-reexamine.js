(() => {
  'use strict';

  const SAMPLE_PATH = 'data/tga/tga-site-sample.json';
  const els = {
    video: document.getElementById('video'),
    localVideo: document.getElementById('local-video'),
    jumpStart: document.getElementById('jump-start'),
    playWindow: document.getElementById('play-window'),
    windowLabel: document.getElementById('window-label'),
    source: document.getElementById('source'),
    context: document.getElementById('context'),
    evaluation: document.getElementById('evaluation'),
    uncertainty: document.getElementById('uncertainty'),
    observations: document.getElementById('observations'),
    provenance: document.getElementById('provenance'),
    raw: document.getElementById('raw'),
    eventFile: document.getElementById('event-file'),
    reloadSample: document.getElementById('reload-sample'),
    loadStatus: document.getElementById('load-status')
  };

  let record = null;
  let localObjectUrl = null;
  let stopTimer = null;

  const text = value => value === null || value === undefined || value === '' ? 'UNSPECIFIED' : String(value);
  const msToClock = ms => {
    const total = Math.max(0, Number(ms) || 0);
    const minutes = Math.floor(total / 60000);
    const seconds = Math.floor((total % 60000) / 1000);
    const millis = total % 1000;
    return `${String(minutes).padStart(2,'0')}:${String(seconds).padStart(2,'0')}.${String(millis).padStart(3,'0')}`;
  };

  function addKv(container, label, value) {
    const dt = document.createElement('dt');
    const dd = document.createElement('dd');
    dt.textContent = label;
    dd.textContent = text(value);
    container.append(dt, dd);
  }

  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

  function validateRecord(value) {
    if (!value || typeof value !== 'object') throw new Error('Record must be a JSON object.');
    if (!value.source || !value.window || !Array.isArray(value.observations)) throw new Error('Record must include source, window, and observations.');
    if (!value.governing_context || !value.evaluation || !value.representation || !value.uncertainty) throw new Error('Record must include governing_context, evaluation, representation, and uncertainty.');
    const start = Number(value.window.start_ms);
    const end = Number(value.window.end_ms);
    if (!Number.isFinite(start) || !Number.isFinite(end) || start < 0 || end <= start) throw new Error('Temporal window must have numeric start_ms >= 0 and end_ms > start_ms.');
    if (value.representation.assertion !== 'INTERPRETIVE_ENCODING_NOT_GROUND_TRUTH') throw new Error('Record must explicitly assert INTERPRETIVE_ENCODING_NOT_GROUND_TRUTH.');
    return value;
  }

  function render(value) {
    record = validateRecord(value);
    const { source, window, governing_context: ctx, evaluation, uncertainty, observations, provenance, representation } = record;

    clear(els.source);
    addKv(els.source, 'Source ID', source.source_id);
    addKv(els.source, 'Kind', source.source_kind);
    addKv(els.source, 'Reference', source.uri);
    addKv(els.source, 'Custody posture', source.custody);
    addKv(els.source, 'Integrity', source.integrity && source.integrity.verification_state);
    addKv(els.source, 'Start', `${window.start_ms} ms · ${msToClock(window.start_ms)}`);
    addKv(els.source, 'End', `${window.end_ms} ms · ${msToClock(window.end_ms)}`);

    clear(els.context);
    addKv(els.context, 'Domain', ctx.domain);
    addKv(els.context, 'Authority / issuer', ctx.authority);
    addKv(els.context, 'Rule set', ctx.rule_set_id);
    addKv(els.context, 'Rule version', ctx.rule_version);
    addKv(els.context, 'Applicability', ctx.temporal_application);
    addKv(els.context, 'Event time', ctx.event_time);
    addKv(els.context, 'Rule effective', `${text(ctx.rule_effective_from)} → ${text(ctx.rule_effective_to)}`);
    addKv(els.context, 'Interpretation profile', ctx.interpretation_profile);
    addKv(els.context, 'Enforcement profile', ctx.enforcement_profile);

    clear(els.evaluation);
    addKv(els.evaluation, 'Conclusion', evaluation.conclusion);
    addKv(els.evaluation, 'Authority effect', evaluation.authority_effect);
    addKv(els.evaluation, 'Adjudicative authority', evaluation.adjudicative_authority);
    addKv(els.evaluation, 'Counterfactual', evaluation.counterfactual === true ? 'YES — hypothetical projection' : 'NO — contemporaneous evaluation');
    addKv(els.evaluation, 'Continuity', evaluation.continuity_state);

    clear(els.uncertainty);
    Object.entries(uncertainty).forEach(([key, val]) => addKv(els.uncertainty, key, Array.isArray(val) ? val.join('; ') : val));

    clear(els.observations);
    observations.forEach(obs => {
      const block = document.createElement('article');
      block.className = 'panel';
      const heading = document.createElement('h3');
      heading.textContent = `${text(obs.subject)} ${text(obs.predicate)} ${text(obs.object)}`;
      const meta = document.createElement('p');
      meta.className = obs.state === 'UNRESOLVED' || obs.state === 'CONTRADICTORY' ? 'state-unresolved' : 'muted';
      meta.textContent = `State: ${text(obs.state)} · Observation ID: ${text(obs.observation_id)}`;
      const refs = document.createElement('p');
      refs.className = 'muted';
      refs.textContent = `Evidence refs: ${(obs.evidence_refs || []).join(', ') || 'NONE'}`;
      block.append(heading, meta, refs);
      els.observations.appendChild(block);
    });

    clear(els.provenance);
    (provenance || []).forEach(ref => {
      const li = document.createElement('li');
      li.textContent = ref;
      els.provenance.appendChild(li);
    });

    els.windowLabel.textContent = `Bounded event window: ${msToClock(window.start_ms)} → ${msToClock(window.end_ms)} (${window.end_ms - window.start_ms} ms)`;
    els.raw.textContent = JSON.stringify(record, null, 2);
    els.loadStatus.textContent = `${representation.assertion} · record loaded successfully.`;
  }

  async function loadSample() {
    try {
      const response = await fetch(SAMPLE_PATH, { cache: 'no-store' });
      if (!response.ok) throw new Error(`Sample load failed: HTTP ${response.status}`);
      render(await response.json());
    } catch (error) {
      els.loadStatus.textContent = `Unable to load sample: ${error.message}`;
    }
  }

  els.localVideo.addEventListener('change', () => {
    const file = els.localVideo.files && els.localVideo.files[0];
    if (!file) return;
    if (localObjectUrl) URL.revokeObjectURL(localObjectUrl);
    localObjectUrl = URL.createObjectURL(file);
    els.video.src = localObjectUrl;
    els.video.load();
  });

  els.jumpStart.addEventListener('click', () => {
    if (!record) return;
    els.video.currentTime = Number(record.window.start_ms) / 1000;
  });

  els.playWindow.addEventListener('click', async () => {
    if (!record || !els.video.src) return;
    clearTimeout(stopTimer);
    const start = Number(record.window.start_ms) / 1000;
    const end = Number(record.window.end_ms) / 1000;
    els.video.currentTime = start;
    try { await els.video.play(); } catch (_) { return; }
    stopTimer = setTimeout(() => els.video.pause(), Math.max(0, (end - start) * 1000));
  });

  els.eventFile.addEventListener('change', async () => {
    const file = els.eventFile.files && els.eventFile.files[0];
    if (!file) return;
    try {
      render(JSON.parse(await file.text()));
    } catch (error) {
      els.loadStatus.textContent = `Record rejected: ${error.message}`;
    }
  });

  els.reloadSample.addEventListener('click', loadSample);
  window.addEventListener('beforeunload', () => { if (localObjectUrl) URL.revokeObjectURL(localObjectUrl); });
  loadSample();
})();
