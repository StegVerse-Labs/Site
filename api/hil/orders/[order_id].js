function send(res, status, body) {
  res.statusCode = status;
  res.setHeader('content-type', 'application/json; charset=utf-8');
  res.setHeader('cache-control', 'no-store');
  res.end(JSON.stringify(body));
}

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') {
    res.setHeader('allow', 'GET');
    return send(res, 405, { error: 'method_not_allowed' });
  }
  const orderId = String(req.query && req.query.order_id || '');
  if (!/^ord-[A-Za-z0-9._:-]+$/.test(orderId)) return send(res, 400, { error: 'invalid_order_id' });

  const serviceUrl = process.env.HIL_ORDER_SERVICE_URL;
  if (!serviceUrl) {
    return send(res, 503, { error: 'order_service_unavailable', order_id: orderId, status: 'UNVERIFIED' });
  }
  const headers = { accept: 'application/json' };
  if (process.env.HIL_ORDER_SERVICE_TOKEN) headers.authorization = `Bearer ${process.env.HIL_ORDER_SERVICE_TOKEN}`;
  try {
    const upstream = await fetch(`${serviceUrl.replace(/\/$/, '')}/orders/${encodeURIComponent(orderId)}`, {
      method: 'GET', headers, signal: AbortSignal.timeout(10000),
    });
    const payload = await upstream.json().catch(() => ({}));
    return send(res, upstream.status, payload);
  } catch (error) {
    return send(res, 503, { error: 'order_service_request_failed', order_id: orderId, detail: String(error && error.message || error) });
  }
};
