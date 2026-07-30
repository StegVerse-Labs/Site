(() => {
  'use strict';

  const RECORD_PATH = 'data/hil-participant-readiness.json';
  const button = document.getElementById('upload-response');
  const status = document.getElementById('intake-status');
  if (!button || !status) return;

  let authorized = false;
  let applying = false;

  function enforce() {
    if (applying || authorized) return;
    applying = true;
    button.disabled = true;
    button.textContent = 'Upload unavailable';
    status.dataset.state = 'warn';
    status.textContent = 'Upload remains fail closed until the production test participant packet is uploaded, receipted, retrieved, and verified end to end.';
    applying = false;
  }

  async function verifyPublicReadiness() {
    try {
      const response = await fetch(`${RECORD_PATH}?t=${Date.now()}`, { cache: 'no-store' });
      if (!response.ok) throw new Error('public_readiness_record_unavailable');
      const record = await response.json();
      authorized = record.schema_version === 'HIL-PUBLIC-PARTICIPANT-READINESS-v1'
        && record.state === 'TEST_PARTICIPANT_PACKET_PASSED'
        && record.participant_ready === true
        && record.upload_button_authorized === true
        && record.test_case_id === 'HIL-E2E-001'
        && typeof record.submission_id === 'string'
        && typeof record.receipt_id === 'string'
        && record.exact_bytes_retrieved === true
        && record.positive_cycle_passed === true
        && record.negative_cases_passed === true;

      if (!authorized) {
        enforce();
        return;
      }

      button.disabled = false;
      button.textContent = 'Upload Response Packet';
      status.dataset.state = 'ok';
      status.textContent = `Test Participant Packet Passed. Upload, receipt, retrieval, and exact-byte verification were proven by ${record.submission_id}. Response-packet intake is ready.`;
    } catch (error) {
      console.debug('HIL public readiness gate failed', error);
      authorized = false;
      enforce();
    }
  }

  button.addEventListener('click', (event) => {
    if (authorized) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    enforce();
  }, true);

  new MutationObserver(() => enforce()).observe(button, { attributes: true, childList: true, subtree: true });
  new MutationObserver(() => enforce()).observe(status, { attributes: true, childList: true, subtree: true });

  enforce();
  verifyPublicReadiness();
})();
