const crypto = require('crypto');

const EVENTS = new Set(['guide_opened','walkthrough_started','assistant_opened','assistant_question_submitted','quick_question_selected','phase_reached','official_source_opened','claim_form_opened','status_page_opened','guide_completed','client_error']);
const BASE_FIELDS = new Set(['event','page','policy_version','content_recorded']);
const OPTIONAL = {
  quick_question_selected: new Set(['choice']),
  phase_reached: new Set(['phase']),
  official_source_opened: new Set(['destination_class']),
  client_error: new Set(['error_class'])
};
const CHOICES = new Set(['blue_button','secondary_claim','intent_to_file','human_help']);
const DESTINATIONS = new Set(['official_va_source','va_claim_form','va_claim_status','openai_help']);
const ERRORS = new Set(['script_initialization','event_rejected','network_unavailable','collector_unavailable']);
const PROHIBITED = new Set(['name','email','phone','address','ssn','social_security_number','claim_number','veteran_id','diagnosis','condition','medical_record','question','message','document','filename','ip','user_agent','session_id','cookie','referrer','location','latitude','longitude']);

function send(res, status, body) {
  res.statusCode = status;
  res.setHeader('content-type', 'application/json; charset=utf-8');
  res.setHeader('cache-control', 'no-store');
  res.setHeader('referrer-policy', 'no-referrer');
  res.end(JSON.stringify(body));
}

function validate(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) return ['body_must_be_object'];
  const errors = [];
  const keys = Object.keys(body);
  for (const key of keys) if (PROHIBITED.has(key)) errors.push(`prohibited_field:${key}`);
  if (!EVENTS.has(body.event)) errors.push('event_not_allowed');
  if (body.page !== 'va-disability-claim-guide') errors.push('page_not_allowed');
  if (body.policy_version !== '1.0.0') errors.push('policy_version_invalid');
  if (body.content_recorded !== false) errors.push('content_recorded_must_be_false');
  const allowed = new Set(BASE_FIELDS);
  for (const key of OPTIONAL[body.event] || []) allowed.add(key);
  for (const key of keys) if (!allowed.has(key)) errors.push(`unknown_field:${key}`);
  if (body.event === 'quick_question_selected' && !CHOICES.has(body.choice)) errors.push('choice_invalid');
  if (body.event === 'phase_reached' && (!Number.isInteger(body.phase) || body.phase < 1 || body.phase > 6)) errors.push('phase_invalid');
  if (body.event === 'official_source_opened' && !DESTINATIONS.has(body.destination_class)) errors.push('destination_class_invalid');
  if (body.event === 'client_error' && !ERRORS.has(body.error_class)) errors.push('error_class_invalid');
  return [...new Set(errors)];
}

function projection(body) {
  const dimensions = {};
  for (const key of OPTIONAL[body.event] || []) dimensions[key] = body[key];
  return { schema: 'stegverse.governed-site-measurement.aggregate-input.v1', event: body.event, page: body.page, policy_version: body.policy_version, dimensions };
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('allow', 'POST');
    return send(res, 405, { state: 'FAILED', error: 'method_not_allowed' });
  }
  const errors = validate(req.body);
  if (errors.length) return send(res, 400, { state: 'FAILED', error: 'event_rejected', errors, content_retained: false });

  const aggregateUrl = process.env.GOVERNED_MEASUREMENT_AGGREGATE_URL;
  if (!aggregateUrl) return send(res, 503, { state: 'BLOCKED', error: 'durable_aggregate_unavailable', content_retained: false, release_condition: 'configure_GOVERNED_MEASUREMENT_AGGREGATE_URL' });

  const input = projection(req.body);
  const idempotency = crypto.createHash('sha256').update(JSON.stringify(input)).digest('hex');
  const headers = { 'content-type': 'application/json', 'idempotency-key': idempotency };
  if (process.env.GOVERNED_MEASUREMENT_AGGREGATE_TOKEN) headers.authorization = `Bearer ${process.env.GOVERNED_MEASUREMENT_AGGREGATE_TOKEN}`;
  try {
    const upstream = await fetch(aggregateUrl, { method: 'POST', headers, body: JSON.stringify(input), signal: AbortSignal.timeout(5000) });
    const result = await upstream.json().catch(() => ({}));
    if (!upstream.ok || result.state !== 'COMPLETE') return send(res, 502, { state: 'RETRY', error: 'aggregate_rejected', upstream_status: upstream.status, content_retained: false });
    return send(res, 202, { state: 'COMPLETE', aggregate_receipt: result.receipt_id || null, content_retained: false, identity_recorded: false });
  } catch (error) {
    return send(res, 503, { state: 'RETRY', error: 'aggregate_unreachable', content_retained: false });
  }
};

module.exports.validate = validate;
module.exports.projection = projection;
