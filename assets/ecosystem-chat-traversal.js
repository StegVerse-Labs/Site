(() => {
  'use strict';

  const strip = document.getElementById('ecosystemTraversal');
  const form = document.getElementById('chatForm');
  const input = document.getElementById('messageInput');
  if (!strip || !form || !input) return;

  const steps = Array.from(strip.querySelectorAll('.traversal-step'));
  const ordered = ['request', 'intent', 'boundary', 'evidence', 'destination', 'receipt'];

  function phaseIndex(name) {
    return Math.max(0, ordered.indexOf(name));
  }

  function setPhase(name, posture = 'preview') {
    const activeIndex = phaseIndex(name);
    steps.forEach((step, index) => {
      step.classList.toggle('active', index <= activeIndex);
      step.dataset.posture = index <= activeIndex ? posture : 'pending';
      step.setAttribute('aria-current', index === activeIndex ? 'step' : 'false');
    });
    strip.dataset.phase = name;
    strip.dataset.authority = 'none';
    strip.dataset.execution = 'disabled';
  }

  function classifyTypingState(value) {
    if (!value.trim()) return 'request';
    if (value.trim().length < 12) return 'intent';
    return 'boundary';
  }

  input.addEventListener('input', () => {
    setPhase(classifyTypingState(input.value), 'local-preview');
  });

  form.addEventListener('submit', () => {
    setPhase('boundary', 'local-preview');
    window.setTimeout(() => setPhase('evidence', 'fixture-only'), 80);
    window.setTimeout(() => setPhase('destination', 'local-preview'), 160);
    window.setTimeout(() => setPhase('receipt', 'not-issued'), 240);
  });

  setPhase('request', 'local-preview');
})();
