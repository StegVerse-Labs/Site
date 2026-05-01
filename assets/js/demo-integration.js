/**
 * StegVerse Demo — Tier 0 Integration
 * Wires the GCAT/BCAT evaluator to the demo.md form
 */

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('demo-form');
    const inputArea = document.getElementById('run-data-input');
    const resultArea = document.getElementById('result-display');
    const verdictBadge = document.getElementById('verdict-badge');
    const godValue = document.getElementById('god-value');
    const confidenceBar = document.getElementById('confidence-bar');
    const receiptHash = document.getElementById('receipt-hash');
    const receiptCanonical = document.getElementById('receipt-canonical');

    // Sample buttons
    document.getElementById('sample-llm').addEventListener('click', () => loadSample('llm_adapter'));
    document.getElementById('sample-sdk').addEventListener('click', () => loadSample('sdk'));
    document.getElementById('sample-human').addEventListener('click', () => loadSample('human'));

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        await runEvaluation();
    });

    function loadSample(source) {
        const sample = GCATEvaluator.generateSample(source);
        inputArea.value = JSON.stringify(sample, null, 2);
        clearResult();
    }

    function clearResult() {
        resultArea.classList.add('hidden');
        verdictBadge.className = 'verdict-badge';
        verdictBadge.textContent = '—';
        godValue.textContent = '—';
        confidenceBar.style.width = '0%';
        receiptHash.textContent = '—';
        receiptCanonical.value = '';
    }

    async function runEvaluation() {
        let inputs;
        try {
            inputs = JSON.parse(inputArea.value);
        } catch (err) {
            showError('Invalid JSON: ' + err.message);
            return;
        }

        try {
            const result = await GCATEvaluator.run(inputs);
            displayResult(result);
        } catch (err) {
            showError('Evaluation failed: ' + err.message);
        }
    }

    function displayResult(result) {
        resultArea.classList.remove('hidden');

        // Verdict badge styling
        verdictBadge.textContent = result.verdict;
        verdictBadge.className = 'verdict-badge verdict-' + result.verdict.toLowerCase().replace('-', '_');

        // GOD value
        godValue.textContent = result.god.toFixed(6);

        // Confidence bar
        confidenceBar.style.width = (result.confidence * 100).toFixed(1) + '%';
        confidenceBar.className = 'confidence-bar-fill verdict-' + result.verdict.toLowerCase().replace('-', '_');

        // Receipt
        receiptHash.textContent = result.receipt.hash;
        receiptCanonical.value = result.receipt.canonical;

        // Boundary info
        document.getElementById('boundary-centroid').textContent = 
            '[' + result.boundary.centroid.map(v => v.toFixed(4)).join(', ') + ']';
        document.getElementById('boundary-radius').textContent = result.boundary.radius.toFixed(6);
        document.getElementById('boundary-epsilon').textContent = result.boundary.epsilon.toFixed(4);
    }

    function showError(msg) {
        resultArea.classList.remove('hidden');
        verdictBadge.textContent = 'ERROR';
        verdictBadge.className = 'verdict-badge verdict-fail_closed';
        document.getElementById('error-message').textContent = msg;
    }

    // Load a default sample on first visit
    if (!inputArea.value.trim()) {
        loadSample('sdk');
    }
});
