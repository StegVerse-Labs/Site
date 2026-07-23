(() => {
  'use strict';

  const PRIMARY = Object.freeze({
    title: 'Humans as the Interoperability Layer',
    version: 'v0.5',
    protocolVersion: 'HIL-PROTOCOL-v1.0',
    promptVersion: 'HIL-PROMPT-v1.0',
    sha256: '52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946',
    filename: 'Humans_as_the_Interoperability_Layer_Primary_Review_Candidate_v0_5.pdf',
    base64Path: 'data/hil-primary-v0.5-review.pdf.b64',
    state: 'REVIEW_CANDIDATE_NOT_YET_CANONICAL'
  });

  const byId = (id) => document.getElementById(id);
  const status = byId('intake-status');

  async function sha256Hex(buffer) {
    const digest = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function saveBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  async function downloadPrimary() {
    const button = byId('download-primary');
    const previous = button.textContent;
    button.disabled = true;
    button.textContent = 'Preparing review PDF…';
    try {
      const response = await fetch(PRIMARY.base64Path, { cache: 'no-store' });
      if (!response.ok) throw new Error(`Review artifact unavailable (${response.status})`);
      const encoded = (await response.text()).replace(/\s+/g, '');
      const binary = atob(encoded);
      const bytes = new Uint8Array(binary.length);
      for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
      const actualHash = await sha256Hex(bytes.buffer);
      if (actualHash !== PRIMARY.sha256) throw new Error('Review artifact hash mismatch; download blocked fail-closed.');
      saveBlob(new Blob([bytes], { type: 'application/pdf' }), PRIMARY.filename);
    } catch (error) {
      status.dataset.state = 'error';
      status.textContent = `${error.message}. The v0.5 review presentation is deployed, but the downloadable PDF artifact is still being installed.`;
    } finally {
      button.disabled = false;
      button.textContent = previous;
    }
  }

  async function copyPrompt() {
    const prompt = byId('canonical-prompt').textContent.trim();
    try {
      await navigator.clipboard.writeText(prompt);
      const button = byId('copy-prompt');
      const old = button.textContent;
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = old; }, 1500);
    } catch {
      status.dataset.state = 'warn';
      status.textContent = 'Copy was blocked by the browser. Select and copy the prompt manually.';
    }
  }

  function text(value) {
    return document.createTextNode(value == null ? 'unknown' : String(value));
  }

  function responseCard(record) {
    const article = document.createElement('article');
    article.className = 'sv-card';
    const heading = document.createElement('h3');
    heading.className = 'sv-h3';
    heading.appendChild(text(record.response_id));
    article.appendChild(heading);
    const summary = document.createElement('p');
    summary.appendChild(text(`${record.model || 'Unknown model'} · ${record.provider || 'Unknown provider'} · ${record.publication_state || 'unknown state'}`));
    article.appendChild(summary);
    if (record.artifact_path) {
      const link = document.createElement('a');
      link.className = 'sv-btn sv-btn-secondary';
      link.href = record.artifact_path;
      link.textContent = 'Open Response PDF';
      article.appendChild(link);
    }
    return article;
  }

  async function loadResponseIndex() {
    const target = byId('response-index');
    try {
      const response = await fetch('data/hil-responses.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`response index unavailable (${response.status})`);
      const index = await response.json();
      if (!Array.isArray(index.responses)) throw new Error('response index has invalid shape');
      target.replaceChildren();
      if (index.responses.length === 0) {
        target.className = 'hil-empty';
        const trace = index.initiating_trace || {};
        target.appendChild(text(`No standardized public responses have been published. ${trace.trace_id || 'HIL-TRACE-0001'} is attributed to ${trace.participant || 'the initiating participant'} and remains ${trace.review_state || 'under review'}.`));
        return;
      }
      target.className = '';
      index.responses.forEach((record) => target.appendChild(responseCard(record)));
    } catch (error) {
      target.className = 'hil-status';
      target.dataset.state = 'warn';
      target.textContent = `Public response index could not be loaded: ${error.message}`;
    }
  }

  byId('download-primary').addEventListener('click', downloadPrimary);
  byId('copy-prompt').addEventListener('click', copyPrompt);
  loadResponseIndex();
})();
