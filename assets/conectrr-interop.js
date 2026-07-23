(() => {
  'use strict';

  const FIXTURE_URL = 'data/conectrr-independent-evaluation.fixture.json';

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
  }

  load().catch((error) => {
    document.documentElement.dataset.conectrrInterop = 'failed';
    console.error(error);
  });
})();
