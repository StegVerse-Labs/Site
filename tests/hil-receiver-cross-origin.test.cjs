// HIL receiver reachable from the static stegverse.org pages (StegVerse-Labs/.github#3106, Site#1565 follow-up):
// the Worker allows only the stegverse.org origins to read /api/hil/* responses (no credentials), and the page
// helper falls back to the receiver Worker only when the same-origin answer is not a JSON receiver response.
const fs = require('fs'); const path = require('path'); const os = require('os'); const vm = require('vm');
const root = path.join(__dirname, '..');
let n = 0; function check(ok, msg) { n++; if (!ok) throw new Error(msg); }
(async () => {
  const tmp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'hil-worker-')), 'worker.mjs');
  fs.writeFileSync(tmp, fs.readFileSync(path.join(root, 'src/worker.js'), 'utf8'));
  const worker = (await import('file://' + tmp)).default;
  const env = { ASSETS: { fetch: async () => new Response('<html>page</html>', { headers: { 'content-type': 'text/html' } }) } };
  const req = (p, init) => new Request('https://site.example' + p, init);

  for (const origin of ['https://stegverse.org', 'https://www.stegverse.org']) {
    const pre = await worker.fetch(req('/api/hil/submissions', { method: 'OPTIONS', headers: { origin, 'access-control-request-method': 'POST' } }), env);
    check(pre.status === 204 && pre.headers.get('access-control-allow-origin') === origin && /POST/.test(pre.headers.get('access-control-allow-methods')), 'preflight allowed for ' + origin);
    check(!pre.headers.get('access-control-allow-credentials'), 'no credentials are allowed cross-origin');
  }
  const bad = await worker.fetch(req('/api/hil/submissions', { method: 'OPTIONS', headers: { origin: 'https://evil.example' } }), env);
  check(bad.status === 403 && !bad.headers.get('access-control-allow-origin'), 'preflight refused for other origins');

  const ready = await worker.fetch(req('/api/hil/readiness', { headers: { origin: 'https://stegverse.org' } }), env);
  check(ready.headers.get('access-control-allow-origin') === 'https://stegverse.org' && /json/.test(ready.headers.get('content-type')), 'receiver JSON carries the allowed origin');
  const readyNoOrigin = await worker.fetch(req('/api/hil/readiness'), env);
  check(!readyNoOrigin.headers.get('access-control-allow-origin'), 'same-origin responses are unchanged');
  const readyEvil = await worker.fetch(req('/api/hil/readiness', { headers: { origin: 'https://evil.example' } }), env);
  check(!readyEvil.headers.get('access-control-allow-origin'), 'other origins cannot read receiver responses');
  const notFound = await worker.fetch(req('/api/hil/nope', { headers: { origin: 'https://stegverse.org' } }), env);
  check(notFound.status === 404 && notFound.headers.get('access-control-allow-origin') === 'https://stegverse.org', 'refusals are readable by the page too');
  const page = await worker.fetch(req('/index.html', { headers: { origin: 'https://stegverse.org' } }), env);
  check(!page.headers.get('access-control-allow-origin') && (await page.text()).includes('page'), 'non-HIL assets are untouched');

  // Page helper.
  function helperWith(hostname, responses) {
    const calls = [];
    const ctx = { location: { hostname }, fetch: async (url, init) => { calls.push({ url, init }); return responses.shift(); } };
    ctx.globalThis = ctx; vm.createContext(ctx);
    vm.runInContext(fs.readFileSync(path.join(root, 'assets/hil-receiver-fetch.js'), 'utf8'), ctx);
    return { H: ctx.StegVerseHilReceiverFetch, calls };
  }
  const html405 = () => new Response('<html>405</html>', { status: 405, headers: { 'content-type': 'text/html' } });
  const json200 = () => new Response('{"ok":true}', { status: 200, headers: { 'content-type': 'application/json' } });
  let h = helperWith('stegverse.org', [html405(), json200()]);
  const body = { marker: 'form' };
  let r = await h.H.fetch('/api/hil/submissions', { method: 'POST', body, credentials: 'same-origin', redirect: 'error' });
  check(r.status === 200 && h.calls.length === 2 && h.calls[1].url === h.H.receiver_origin + '/api/hil/submissions', 'static-host 405 falls back to the receiver Worker');
  check(h.calls[1].init.body === body && h.calls[1].init.method === 'POST' && h.calls[1].init.credentials === 'omit' && h.calls[1].init.mode === 'cors' && h.calls[1].init.redirect === 'error', 'fallback repeats the identical request without credentials');
  h = helperWith('stegverse.org', [json200()]);
  r = await h.H.fetch('/api/hil/submissions', { method: 'POST' });
  check(r.status === 200 && h.calls.length === 1, 'a routed receiver is used directly; no fallback');
  h = helperWith('site.rigelrandolph.workers.dev', [html405()]);
  r = await h.H.fetch('/api/hil/submissions', { method: 'POST' });
  check(r.status === 405 && h.calls.length === 1, 'no fallback away from stegverse.org');
  h = helperWith('stegverse.org', [html405(), undefined]);
  h.calls.length = 0;
  const failing = { location: { hostname: 'stegverse.org' }, fetch: async (url) => { if (url.startsWith('http')) throw new TypeError('network'); return html405(); } };
  failing.globalThis = failing; vm.createContext(failing); vm.runInContext(fs.readFileSync(path.join(root, 'assets/hil-receiver-fetch.js'), 'utf8'), failing);
  r = await failing.StegVerseHilReceiverFetch.fetch('/api/hil/submissions', { method: 'POST' });
  check(r.status === 405, 'a failed fallback reports the original answer so the page keeps the packet for retry');
  check(failing.StegVerseHilReceiverFetch.authority_effect === 'NONE', 'helper grants no authority');

  // Wiring.
  const read = f => fs.readFileSync(path.join(root, f), 'utf8');
  for (const [page, before] of [['humans-as-interoperability-layer.html', 'assets/hil-direct-upload-v1.js'], ['hil-receipt.html', 'INGRESS='], ['hil-accepted.html', 'assets/hil-post-submit-continuity.js']]) {
    const s = read(page); check(s.indexOf('assets/hil-receiver-fetch.js') > 0 && s.indexOf('assets/hil-receiver-fetch.js') < s.indexOf(before), 'helper loads first on ' + page);
  }
  check(/StegVerseHilReceiverFetch/.test(read('assets/hil-direct-upload-v1.js')) && (read('assets/hil-post-submit-continuity.js').match(/StegVerseHilReceiverFetch\.fetch/g) || []).length === 2 && /StegVerseHilReceiverFetch/.test(read('hil-receipt.html')), 'every receiver call uses the helper');
  console.log('PASS hil receiver cross-origin (' + n + ' checks)');
})().catch(e => { console.error(e); process.exit(1); });
