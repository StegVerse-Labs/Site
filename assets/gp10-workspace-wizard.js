(() => {
  'use strict';
  const steps = [...document.querySelectorAll('[data-gp10-step]')];
  const progress = document.getElementById('gp10Progress');
  let current = 0;

  function show(index) {
    current = Math.max(0, Math.min(index, steps.length - 1));
    steps.forEach((step, i) => {
      step.hidden = i !== current;
      step.setAttribute('aria-hidden', i === current ? 'false' : 'true');
    });
    if (progress) progress.textContent = `Step ${current + 1} of ${steps.length} · ${steps[current].dataset.stepName}`;
    window.scrollTo({top: 0, behavior: 'smooth'});
  }

  function requiredComplete(step) {
    const missing = [...step.querySelectorAll('[required]')].find(field => !String(field.value || '').trim());
    if (!missing) return true;
    missing.focus();
    const status = document.getElementById('status');
    if (status) status.textContent = 'Complete the required field before continuing.';
    return false;
  }

  document.addEventListener('click', event => {
    const next = event.target.closest('[data-next-step]');
    const back = event.target.closest('[data-prev-step]');
    if (next) {
      event.preventDefault();
      if (requiredComplete(steps[current])) show(current + 1);
    }
    if (back) {
      event.preventDefault();
      show(current - 1);
    }
  });

  document.getElementById('newRecord')?.addEventListener('click', () => setTimeout(() => show(0), 0));
  show(0);
})();