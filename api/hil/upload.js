export const config = { runtime: 'edge' };

const OWNER = 'StegVerse-Labs';
const REPO = 'Site';
const API = 'https://api.github.com';
const MAX_BYTES = 4 * 1024 * 1024;

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

async function gh(token, path, init = {}) {
  const response = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      accept: 'application/vnd.github+json',
      authorization: `Bearer ${token}`,
      'x-github-api-version': '2022-11-28',
      ...(init.headers || {})
    }
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : null;
  if (!response.ok) throw new Error(`github_${response.status}:${data?.message || 'request_failed'}`);
  return data;
}

function base64(bytes) {
  let binary = '';
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) binary += String.fromCharCode(...bytes.subarray(i, i + chunk));
  return btoa(binary);
}

async function sha256Hex(buffer) {
  const digest = await crypto.subtle.digest('SHA-256', buffer);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export default async function handler(request) {
  if (request.method === 'OPTIONS') return json({ ok: true });
  if (request.method !== 'POST') return json({ detail: 'method_not_allowed' }, 405);

  const token = process.env.HIL_GITHUB_TOKEN || process.env.GITHUB_TOKEN;
  if (!token) return json({ detail: 'hil_github_token_missing' }, 503);

  try {
    const form = await request.formData();
    const pdf = form.get('response_pdf');
    if (!(pdf instanceof File)) return json({ detail: 'response_pdf_required' }, 400);
    if (pdf.size < 5 || pdf.size > MAX_BYTES) return json({ detail: 'response_pdf_size_invalid' }, 413);
    if (!pdf.name.toLowerCase().endsWith('.pdf')) return json({ detail: 'response_pdf_extension_invalid' }, 400);

    const buffer = await pdf.arrayBuffer();
    const signature = new TextDecoder('ascii').decode(new Uint8Array(buffer).slice(0, 5));
    if (signature !== '%PDF-') return json({ detail: 'response_pdf_signature_invalid' }, 400);

    const submissionId = `HIL-SUBMISSION-${crypto.randomUUID()}`;
    const receiptId = `HIL-RECEIPT-${crypto.randomUUID()}`;
    const responseSha256 = await sha256Hex(buffer);
    const createdAt = new Date().toISOString();
    const displayName = String(form.get('display_name') || 'Anonymous').trim().slice(0, 100) || 'Anonymous';
    const displayNameAuthorized = String(form.get('display_name_authorized') || '') === 'true';
    const authorized = String(form.get('authorized') || '') === 'true';
    const unchanged = String(form.get('unchanged') || '') === 'true';
    if (!authorized || !unchanged) return json({ detail: 'required_confirmations_missing' }, 400);

    const repo = await gh(token, `/repos/${OWNER}/${REPO}`);
    const baseRef = await gh(token, `/repos/${OWNER}/${REPO}/git/ref/heads/${encodeURIComponent(repo.default_branch)}`);
    const branch = `hil-ingress/${submissionId.toLowerCase()}`;
    await gh(token, `/repos/${OWNER}/${REPO}/git/refs`, {
      method: 'POST',
      body: JSON.stringify({ ref: `refs/heads/${branch}`, sha: baseRef.object.sha })
    });

    const root = `incoming/hil/${submissionId}`;
    const metadata = {
      schema_version: 'HIL-DIRECT-INGRESS-v1',
      submission_id: submissionId,
      receipt_id: receiptId,
      created_at: createdAt,
      original_filename: pdf.name,
      size_bytes: pdf.size,
      response_sha256: responseSha256,
      display_name: displayName,
      display_name_authorized: displayNameAuthorized,
      authorized_to_submit: true,
      declared_unchanged: true,
      state: 'QUEUED_FOR_GITHUB_WORKER'
    };

    await gh(token, `/repos/${OWNER}/${REPO}/contents/${root}/response.pdf`, {
      method: 'PUT',
      body: JSON.stringify({ message: `Stage ${submissionId} response PDF`, content: base64(new Uint8Array(buffer)), branch })
    });
    await gh(token, `/repos/${OWNER}/${REPO}/contents/${root}/intake.json`, {
      method: 'PUT',
      body: JSON.stringify({ message: `Stage ${submissionId} intake metadata`, content: btoa(unescape(encodeURIComponent(`${JSON.stringify(metadata, null, 2)}\n`))), branch })
    });

    const issue = await gh(token, `/repos/${OWNER}/${REPO}/issues`, {
      method: 'POST',
      body: JSON.stringify({
        title: `[HIL RESPONSE PACKET] ${submissionId}`,
        body: [
          'Automated participant intake. GitHub is an internal processing layer and is not part of the participant interface.',
          '',
          `Submission ID: \`${submissionId}\``,
          `Receipt ID: \`${receiptId}\``,
          `Source branch: \`${branch}\``,
          `Response path: \`${root}/response.pdf\``,
          `Metadata path: \`${root}/intake.json\``,
          `PDF SHA-256: \`${responseSha256}\``
        ].join('\n')
      })
    });

    const receipt = {
      schema_version: 'HIL-INGRESS-RECEIPT-v1',
      submission_id: submissionId,
      receipt_id: receiptId,
      received_at: createdAt,
      submitted_file_sha256: responseSha256,
      original_filename: pdf.name,
      display_name: displayNameAuthorized ? displayName : 'Anonymous',
      state: 'QUEUED_FOR_GITHUB_WORKER',
      issue_number: issue.number
    };

    return json(receipt, 202);
  } catch (error) {
    console.error(error);
    return json({ detail: 'ingress_failed', message: String(error?.message || error) }, 500);
  }
}
