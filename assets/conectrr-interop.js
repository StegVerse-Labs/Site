(() => {
  'use strict';

  const FIXTURE_URL = 'data/conectrr-independent-evaluation.fixture.json';

  function verifyExportReplay(api, sourceId, decisionId) {
    const events = api.getEvents();
    const json = JSON.stringify({ schema: 'stegverse.canonical-event-stream.v0.1', events });
    const jsonl = events.map((event) => JSON.stringify(event)).join('\n') + '\n';
    const replayedJson = JSON.parse(json).events;
    const replayedJsonl = jsonl.trim().split('\n').map((line) => JSON.parse(line));
    const required = [sourceId, decisionId];
    const jsonIds = new Set(replayedJson.map((event) => event.event_id));
    const jsonlIds = new Set(replayedJsonl.map((event) => event.event_id));
    if (!required.every((eventId) => jsonIds.has(eventId) && jsonlIds.has(eventId))) {
      throw new Error('Conectrr export replay omitted a correlated record');
    }
    const replayedDecision = replayedJsonl.find((event) => event.event_id === decisionId);
    if (replayedDecision?.parent_event_id !== sourceId || !replayedDecision?.evidence_refs?.includes(sourceId)) {
      throw new Error('Conectrr export replay broke source-decision correlation');
    }
    document.documentElement.dataset.conectrrExportReplay = 'pass';
  }

  async function load() {
    const api = window.StegVerseCanonicalEventStream;
    if (!api || typeof api.importCanonicalEvents !== 'function') return;

    const response = await fetch(FIXTURE_URL, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Conectrr fixture load failed: ${response.status}`);
    const payload = await response.json();
    const source = structuredClone(payload.source_event);
    const decision = structuredClone(payload.downstream_event);
    const sourceSnapshot = JSON.stringify(source);

    api.importCanonicalEvents([source, decision]);

    if (JSON.stringify(source) !== sourceSnapshot) {
      throw new Error('Conectrr source mutated during import');
    }

    document.documentElement.dataset.conectrrInterop = 'loaded';
    document.documentElement.dataset.conectrrSourceEvent = source.event_id;
    document.documentElement.dataset.conectrrDecisionEvent = decision.event_id;

    const sourceRecord = document.querySelector(`[data-event-id="${CSS.escape(source.event_id)}"]`);
    const decisionRecord = document.querySelector(`[data-event-id="${CSS.escape(decision.event_id)}"]`);
    if (!sourceRecord || !decisionRecord) throw new Error('Conectrr governed records did not render');

    api.selectEvent(source.event_id, 'governed');
    if (!sourceRecord.classList.contains('correlated-active') || !decisionRecord.classList.contains('correlated-active')) {
      throw new Error('Source-to-decision correlation failed');
    }
    api.selectEvent(decision.event_id, 'governed');
    if (!sourceRecord.classList.contains('correlated-active') || !decisionRecord.classList.contains('correlated-active')) {
      throw new Error('Decision-to-source correlation failed');
    }

    verifyExportReplay(api, source.event_id, decision.event_id);
    document.documentElement.dataset.conectrrBrowserTest = 'pass';
  }

  load().catch((error) => {
    document.documentElement.dataset.conectrrInterop = 'fail';
    document.documentElement.dataset.conectrrBrowserTest = 'fail';
    document.documentElement.dataset.conectrrExportReplay = 'failed';
    console.error(error);
  });
})();
