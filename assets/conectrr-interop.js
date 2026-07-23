(() => {
  'use strict';

  const FIXTURE_URL = 'data/conectrr-independent-evaluation.fixture.json';

  function rendered(eventId) {
    return Boolean(document.querySelector(`#governedRecordList [data-event-id="${CSS.escape(eventId)}"]`));
  }

  function active(eventId) {
    return document.querySelector(`#governedRecordList [data-event-id="${CSS.escape(eventId)}"]`)?.classList.contains('correlated-active') === true;
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

    if (JSON.stringify(source) !== sourceSnapshot) throw new Error('Conectrr source mutated during import');
    if (!rendered(source.event_id) || !rendered(decision.event_id)) throw new Error('Conectrr source or downstream decision did not render');

    api.selectEvent(source.event_id, 'governed');
    if (!active(source.event_id) || !active(decision.event_id)) throw new Error('Source-to-decision correlation failed');

    api.selectEvent(decision.event_id, 'governed');
    if (!active(source.event_id) || !active(decision.event_id)) throw new Error('Decision-to-source correlation failed');

    document.documentElement.dataset.conectrrInterop = 'loaded';
    document.documentElement.dataset.conectrrBrowserTest = 'pass';
    document.documentElement.dataset.conectrrSourceEvent = source.event_id;
    document.documentElement.dataset.conectrrDecisionEvent = decision.event_id;
  }

  load().catch((error) => {
    document.documentElement.dataset.conectrrInterop = 'failed';
    document.documentElement.dataset.conectrrBrowserTest = 'fail';
    console.error(error);
  });
})();