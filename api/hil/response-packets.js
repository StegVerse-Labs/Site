const crypto = require('crypto');

function send(res, status, body) {
  res.statusCode = status;
  res.setHeader('content-type', 'application/json; charset=utf-8');
  res.setHeader('cache-control', 'no-store');
  res.end(JSON.stringify(body));
}

function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((k) => `${JSON.stringify(k)}:${canonicalJson(value[k])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function isSha256(value) {
  return typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
}

function validateEnvelope(body) {
  const errors = [];
  if (!body || typeof body !== 'object' || Array.isArray(body)) return ['body_must_be_object'];
  if (!body.source_object || typeof body.source_object !== 'object') errors.push('source_object_required');
  const source = body.source_object || {};
  if (!isSha256(source.sha256)) errors.push('source_object_sha256_invalid');
  if (source.uri !== `cas://sha256/${source.sha256}`) errors.push('source_object_uri_digest_mismatch');
  if (!Number.isSafeInteger(source.byte_size) || source.byte_size < 1) errors.push('source_object_byte_size_invalid');
  if (typeof source.media_type !== 'string' || !source.media_type) errors.push('source_object_media_type_required');
  if (typeof body.participant_posture !== 'string' || !body.participant_posture) errors.push('participant_posture_required');
  return errors;
}

function createRootOrder(body, requestId) {
  const source = body.source_object;
  const orderId = `ord-hil-${requestId}`;
  const expires = new Date(Date.now() + 60 * 60 * 1000).toISOString();
  return {
    schema_version: '1.0.0',
    order_id: orderId,
    root_order_id: orderId,
    parent_order_id: null,
    task_type: 'response-packet-verification',
    protocol_version: '1.0.0',
    subject_ref: body.subject_ref || source.uri,
    input_objects: [{
      uri: source.uri,
      sha256: source.sha256,
      byte_size: source.byte_size,
      media_type: source.media_type,
    }],
    dependency_receipts: [],
    expected_outputs: ['verification-receipt', 'destruction-receipt'],
    required_capabilities: ['isolated-execution', 'sha256', 'normalized-receipt-output'],
    authority_scope: {
      read_objects: [source.uri],
      write_outputs: ['verification-receipt', 'destruction-receipt'],
      repository_actions: [],
      publication_actions: [],
    },
    resource_limits: { cpu_seconds: 300, memory_mb: 1024, temporary_storage_mb: 1024, output_mb: 25 },
    network_policy: 'deny-by-default',
    expires_at: expires,
    max_attempts: 3,
    destruction_policy: 'required',
    admission_policy_ref: 'tvc:provider-agnostic-ephemeral-order:1.0.0',
    idempotency_key: crypto.createHash('sha256').update(canonicalJson({ source, participant_posture: body.participant_posture })).digest('hex'),
    extensions: {
      participant_posture: body.participant_posture,
      provenance_ref: body.provenance_ref || null,
      ingress: 'StegVerse-Labs/Site',
    },
  };
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('allow', 'POST');
    return send(res, 405, { error: 'method_not_allowed' });
  }
  const errors = validateEnvelope(req.body);
  if (errors.length) return send(res, 400, { error: 'invalid_response_packet_envelope', errors });

  const serviceUrl = process.env.HIL_ORDER_SERVICE_URL;
  if (!serviceUrl) {
    return send(res, 503, {
      error: 'order_service_unavailable',
      detail: 'Durable order admission is not configured; no 202 acceptance or execution claim is issued.',
    });
  }

  const requestId = crypto.randomUUID().replace(/-/g, '');
  const rootOrder = createRootOrder(req.body, requestId);
  const headers = { 'content-type': 'application/json', 'idempotency-key': rootOrder.idempotency_key };
  if (process.env.HIL_ORDER_SERVICE_TOKEN) headers.authorization = `Bearer ${process.env.HIL_ORDER_SERVICE_TOKEN}`;

  let upstream;
  try {
    upstream = await fetch(`${serviceUrl.replace(/\/$/, '')}/orders`, {
      method: 'POST', headers, body: JSON.stringify(rootOrder), signal: AbortSignal.timeout(10000),
    });
  } catch (error) {
    return send(res, 503, { error: 'order_service_request_failed', detail: String(error && error.message || error) });
  }

  const payload = await upstream.json().catch(() => ({}));
  if (!upstream.ok || !['ADMITTED', 'ACCEPTED', 'PROPOSED'].includes(payload.status)) {
    return send(res, 502, { error: 'order_service_rejected', upstream_status: upstream.status, upstream: payload });
  }
  return send(res, 202, {
    packet_id: payload.packet_id || `pkt-${requestId}`,
    order_id: payload.order_id || rootOrder.order_id,
    status: payload.status,
    intake_receipt: payload.intake_receipt || null,
    status_url: `/api/hil/orders/${encodeURIComponent(payload.order_id || rootOrder.order_id)}`,
  });
};
