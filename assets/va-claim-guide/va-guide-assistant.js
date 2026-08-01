(() => {
  const root = document.querySelector('[data-va-assistant]');
  if (!root) return;

  const status = {
    mode: 'BOUNDED_GUIDED_MODE',
    completeness: 68,
    liveLlm: false,
    uploads: false,
    citations: true,
    updated: '2026-07-31'
  };

  const answers = [
    {keys:['blue button','download','medical record'],answer:'Use the VA app to open Health → Medical records → Review medical records on VA.gov. Choose the Blue Button report, select All time and all available record categories, choose PDF, then complete the browser download prompt. On iPhone, check Files → Recents and the browser-named folder if Downloads appears empty.',source:'https://www.va.gov/health-care/get-medical-records/'},
    {keys:['intent to file','effective date'],answer:'Starting the verified online disability compensation application records an intent to file for that online claim. Preserve the start date and submit before the applicable deadline. Effective-date questions can become complex after prior denials or reopened claims, so use accredited help when the date is disputed.',source:'https://www.va.gov/resources/your-intent-to-file-a-va-claim/'},
    {keys:['secondary','caused by','aggravated'],answer:'A secondary claim generally needs a current condition, an already service-connected disability, and competent evidence that the service-connected disability caused or aggravated the new condition. The existing rating alone does not prove the relationship.',source:'https://www.va.gov/disability/how-to-file-claim/evidence-needed/'},
    {keys:['evidence','need for claim','service connection'],answer:'A direct claim generally needs evidence of a current disability or persistent symptoms, an in-service event, injury, disease, or exposure, and evidence connecting the two. Lay statements may establish observable events and symptoms, while diagnosis and medical causation may require a qualified clinician.',source:'https://www.va.gov/disability/how-to-file-claim/evidence-needed/'},
    {keys:['rating','percentage','how much'],answer:'This guide cannot reliably predict a percentage. VA applies the rating schedule to verified severity and functional evidence. Focus on accurate symptoms, frequency, duration, treatment, objective testing, and functional effects rather than targeting a percentage.',source:'https://www.va.gov/disability/about-disability-ratings/'},
    {keys:['representative','vso','lawyer','attorney'],answer:'Use an accredited VSO representative, claims agent, or attorney when records are missing, a prior claim was denied, the effective date matters, service events are disputed, or the theory depends on complex causation or aggravation.',source:'https://www.va.gov/get-help-from-accredited-representative/'},
    {keys:['status','where is my claim'],answer:'Check the current claim or appeal status through VA.gov or the VA mobile app. Respond to evidence requests by the stated deadline and preserve proof of every upload or submission.',source:'https://www.va.gov/claim-or-appeal-status/'}
  ];

  const box = root.querySelector('[data-va-answer]');
  const input = root.querySelector('textarea');
  const form = root.querySelector('form');
  const badge = root.querySelector('[data-va-status]');
  const meter = root.querySelector('[data-va-meter]');

  badge.textContent = `Current capability: ${status.mode.replaceAll('_',' ')} · live LLM ${status.liveLlm ? 'available' : 'in development'} · document upload ${status.uploads ? 'available' : 'not yet active'}`;
  meter.textContent = `${status.completeness}% assistant completeness`;

  const reply = (question) => {
    const q = question.toLowerCase();
    const match = answers.find(item => item.keys.some(key => q.includes(key)));
    if (!match) {
      return {
        answer:'This bounded guide does not yet have a verified answer for that question. Use the official VA sources below or an accredited representative. The live source-grounded assistant is still in development; watch this status box for capability updates.',
        source:'https://www.va.gov/disability/how-to-file-claim/'
      };
    }
    return match;
  };

  form.addEventListener('submit', event => {
    event.preventDefault();
    const question = input.value.trim();
    if (!question) return;
    const result = reply(question);
    box.innerHTML = `<p><strong>Direct answer</strong><br>${result.answer}</p><p><strong>Official source</strong><br><a href="${result.source}" rel="noopener">Open VA guidance</a></p><p class="muted">This response is procedural guidance, not a VA decision, medical opinion, or rating guarantee.</p>`;
  });
})();
