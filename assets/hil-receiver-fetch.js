// HIL receiver fetch with a fallback for static hosting. The participant pages may be served from stegverse.org,
// where /api/hil/* is not yet routed to the receiver Worker and a POST returns a 405 HTML page. A request is sent
// to the same-origin path first; only when that answer is clearly not the receiver (a non-JSON response) and the
// page is on stegverse.org is the identical request repeated against the receiver Worker, without credentials.
// Once stegverse.org routes /api/hil/* to the Worker, the first attempt succeeds and the fallback never runs.
(function (root) {
  'use strict';
  const RECEIVER_ORIGIN = 'https://site.rigelrandolph.workers.dev';
  const FALLBACK_HOSTS = new Set(['stegverse.org', 'www.stegverse.org']);

  function isReceiverResponse(response) {
    return /application\/json/i.test(response.headers.get('content-type') || '');
  }

  async function hilReceiverFetch(path, init) {
    const options = Object.assign({}, init || {});
    const first = await root.fetch(path, options);
    if (isReceiverResponse(first) || !FALLBACK_HOSTS.has(root.location && root.location.hostname)) return first;
    const fallback = Object.assign({}, options, { mode: 'cors', credentials: 'omit' });
    try {
      return await root.fetch(RECEIVER_ORIGIN + path, fallback);
    } catch (error) {
      return first;
    }
  }

  root.StegVerseHilReceiverFetch = Object.freeze({ fetch: hilReceiverFetch, receiver_origin: RECEIVER_ORIGIN, authority_effect: 'NONE' });
})(typeof globalThis !== 'undefined' ? globalThis : this);
