export const config = { runtime: 'edge' };

const TVC_INGRESS = 'https://tvc.stegverse.org/api/hil/ingress';
const MAX_BYTES = 4 * 1024 * 1024;
const LEASE_MS = 5 * 60 * 1000;

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store',
      'access-control-allow-origin': 'https://stegverse.org',
      'access-control-allow-methods': 'POST, OPTIONS',
      'access-control-allow-headers': 'content-type'
    }
  });
}

async function sha256Hex(buffer) {
  const digest = await crypto.subtle.digest('SHA-256', buffer);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export default async function handler(request) {
  if (request.method === 'OPTIONS') return json({ ok: true });
  if (request.method !== 'POST') return json({ detail: 'method_not_allowed' }, 405);

  try {
    const form = await request.formData();
    const pdf = form.get('response_pdf');
    if (!(pdf instanceof File)) return json({ detail: 'response_pdf_required' }, 400);
    if (pdf.size < 5 || pdf.size > MAX_BYTES) return json({ detail: 'response_pdf_size_invalid' }, 413);
    if (!pdf.name.toLowerCase().endsWith('.pdf')) return json({ detail: 'response_pdf_extension_invalid' }, 400);

    const authorized = String(form.get('authorized') || '') === 'true';
    const unchanged = String(form.get('unchanged') || '') === 'true';
    if (!authorized || !unchanged) return json({ detail: 'required_confirmations_missing' }, 400);

    const buffer = await pdf.arrayBuffer();
    const signature = new TextDecoder('ascii').decode(new Uint8Array(buffer).slice(0, 5));
    if (signature !== '%PDF-') return json({ detail: 'response_pdf_signature_invalid' }, 400);

    const issuedAt = new Date();
    const expiresAt = new Date(issuedAt.getTime() + LEASE_MS);
    const displayName = String(form.get('display_name') || 'Anonymous').trim().slice(0, 100) || 'Anonymous';
    const displayNameAuthorized = String(form.get('display_name_authorized') || '') === 'true';
    const envelope = {
      schema_version: 'HIL-TVC-CAPABILITY-REQUEST-v1',
      submission_id: `HIL-SUBMISSION-${crypto.randomUUID()}`,
      receipt_id: `HIL-RECEIPT-${crypto.randomUUID()}`,
      request_nonce: crypto.randomUUID(),
      issued_at: issuedAt.toISOString(),
      expires_at: expiresAt.toISOString(),
      target_repository: 'StegVerse-Labs/Site',
      target_workflow: 'hil-direct-ingress-worker.yml',
      operation: 'stage_hil_source_and_open_internal_intake',
      response_sha256: await sha256Hex(buffer),
      size_bytes: pdf.size,
      display_name: displayName,
      display_name_authorized: displayNameAuthorized,
      authorized_to_submit: true,
      declared_unchanged: true,
      secret_requested_by_site: false,
      participant_github_interaction_required: false
    };

    const outbound = new FormData();
    outbound.append('response_pdf', new File([buffer], pdf.name, { type: pdf.type || 'application/pdf' }));
    outbound.append('capability_request', new File([
      `${JSON.stringify(envelope, null, 2)}\n`
    ], 'hil-capability-request.json', { type: 'application/json' }));

    const response = await fetch(TVC_INGRESS, { method: 'POST', body: outbound });
    const text = await response.text();
    let result;
    try { result = text ? JSON.parse(text) : {}; }
    catch { result = { detail: 'invalid_tvc_response' }; }

    if (!response.ok) {
      return json({
        detail: result.detail || 'tvc_ingress_unavailable',
        authority_location: 'TV_TVC_ONLY',
        site_secret_access: false
      }, response.status || 502);
    }

    return json(result, 202);
  } catch (error) {
    console.error(error);
    return json({
      detail: 'site_tvc_handoff_failed',
      message: String(error?.message || error),
      authority_location: 'TV_TVC_ONLY',
      site_secret_access: false
    }, 502);
  }
}
