/**
 * StegVerse Demo — Tier 0 Integration (Debug Build)
 * Wires the GCAT/BCAT evaluator to the demo form with full error handling.
 */

document.addEventListener('DOMContentLoaded', function () {
    console.log('[StegVerse Demo] DOM loaded. Initializing...');

    // Check if GCATEvaluator is available
    if (typeof GCATEvaluator === 'undefined') {
        console.error('[StegVerse Demo] CRITICAL: GCATEvaluator not loaded. Check script tag.');
        showFatal('GCAT/BCAT evaluator failed to load. Please refresh.');
        return;
    }
    console.log('[StegVerse Demo] GCATEvaluator loaded:', Object.keys(GCATEvaluator));

    // Check if BoundaryViz is available
    if (typeof BoundaryViz === 'undefined') {
        console.warn('[StegVerse Demo] BoundaryViz not loaded. Visualization disabled.');
    } else {
        console.log('[StegVerse Demo] BoundaryViz loaded.');
    }

    const form = document.getElementById('demo-form');
    const inputArea = document.getElementById('run-data-input');
    const resultArea = document.getElementById('result-display');
    const verdictBadge = document.getElementById('verdict-badge');
    const godValue = document.getElementById('god-value');
    const confidenceBar = document.getElementById('confidence-bar');
    const receiptHash = document.getElementById('receipt-hash');
    const receiptCanonical = document.getElementById('receipt-canonical');

    // Defensive element checks
    const elements = {
        form, inputArea, resultArea, verdictBadge, godValue,
        confidenceBar, receiptHash, receiptCanonical
    };
    for (const [name, el] of Object.entries(elements)) {
        if (!el) console.error(`[StegVerse Demo] Missing element: #${name}`);
    }

    // Sample buttons
    const btnLLM = document.getElementById('sample-llm');
    const btnSDK = document.getElementById('sample-sdk');
    const btnHuman = document.getElementById('sample-human');
    const btnGenerate = document.getElementById('generate-new');

    if (btnLLM) {
        btnLLM.addEventListener('click', () => {
            console.log('[StegVerse Demo] Loading LLM sample...');
            loadSample('llm_adapter');
        });
    } else { console.error('[StegVerse Demo] Missing button: #sample-llm'); }

    if (btnSDK) {
        btnSDK.addEventListener('click', () => {
            console.log('[StegVerse Demo] Loading SDK sample...');
            loadSample('sdk');
        });
    } else { console.error('[StegVerse Demo] Missing button: #sample-sdk'); }

    if (btnHuman) {
        btnHuman.addEventListener('click', () => {
            console.log('[StegVerse Demo] Loading Human sample...');
            loadSample('human');
        });
    } else { console.error('[StegVerse Demo] Missing button: #sample-human'); }

    if (btnGenerate) {
        btnGenerate.addEventListener('click', () => {
            console.log('[StegVerse Demo] Generating new random dataset...');
            generateNewDataset();
        });
    } else { console.error('[StegVerse Demo] Missing button: #generate-new'); }

    // Form submit
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            console.log('[StegVerse Demo] Evaluate clicked.');
            await runEvaluation();
        });
    }

    function loadSample(source) {
        console.log('[StegVerse Demo] loadSample called:', source);
        try {
            const sample = GCATEvaluator.generateSample(source);
            inputArea.value = JSON.stringify(sample, null, 2);
            clearResult();
            console.log('[StegVerse Demo] Sample loaded successfully.');
        } catch (err) {
            console.error('[StegVerse Demo] loadSample failed:', err);
            showError('Failed to load sample: ' + err.message);
        }
    }

    function generateNewDataset() {
        console.log('[StegVerse Demo] generateNewDataset called.');
        try {
            const current = inputArea.value.trim();
            let source = 'sdk';
            try {
                const parsed = JSON.parse(current);
                source = parsed.source || 'sdk';
            } catch(e) {}
            console.log('[StegVerse Demo] Generating random data for source:', source);

            let sample;
            if (GCATEvaluator.generateSampleRandom) {
                sample = GCATEvaluator.generateSampleRandom(source);
            } else {
                console.warn('[StegVerse Demo] generateSampleRandom not found, using fixed seed.');
                sample = GCATEvaluator.generateSample(source);
            }
            inputArea.value = JSON.stringify(sample, null, 2);
            clearResult();
            console.log('[StegVerse Demo] New dataset generated.');
        } catch (err) {
            console.error('[StegVerse Demo] generateNewDataset failed:', err);
            showError('Failed to generate dataset: ' + err.message);
        }
    }

    function clearResult() {
        if (resultArea) resultArea.classList.add('hidden');
        if (verdictBadge) {
            verdictBadge.className = 'verdict-badge';
            verdictBadge.textContent = '—';
        }
        if (godValue) godValue.textContent = '—';
        if (confidenceBar) confidenceBar.style.width = '0%';
        if (receiptHash) receiptHash.textContent = '—';
        if (receiptCanonical) receiptCanonical.value = '';
        const errMsg = document.getElementById('error-message');
        if (errMsg) errMsg.textContent = '';
    }

    async function runEvaluation() {
        console.log('[StegVerse Demo] runEvaluation started.');
        let inputs;
        try {
            inputs = JSON.parse(inputArea.value);
            console.log('[StegVerse Demo] Input parsed:', inputs.source, inputs.demo_id);
        } catch (err) {
            console.error('[StegVerse Demo] JSON parse failed:', err);
            showError('Invalid JSON: ' + err.message);
            return;
        }

        try {
            const result = await GCATEvaluator.run(inputs);
            console.log('[StegVerse Demo] Evaluation result:', result.verdict, 'GOD:', result.god);
            displayResult(result, inputs);
        } catch (err) {
            console.error('[StegVerse Demo] Evaluation failed:', err);
            showError('Evaluation failed: ' + err.message);
        }
    }

    function displayResult(result, inputs) {
        console.log('[StegVerse Demo] displayResult called:', result.verdict);
        if (resultArea) resultArea.classList.remove('hidden');

        if (verdictBadge) {
            verdictBadge.textContent = result.verdict;
            verdictBadge.className = 'verdict-badge verdict-' + result.verdict.toLowerCase().replace('-', '_');
        }

        if (godValue) godValue.textContent = result.god.toFixed(6);

        if (confidenceBar) {
            confidenceBar.style.width = (result.confidence * 100).toFixed(1) + '%';
            confidenceBar.className = 'confidence-bar-fill verdict-' + result.verdict.toLowerCase().replace('-', '_');
        }

        if (receiptHash) receiptHash.textContent = result.receipt.hash;
        if (receiptCanonical) receiptCanonical.value = result.receipt.canonical;

        const bc = document.getElementById('boundary-centroid');
        const br = document.getElementById('boundary-radius');
        const be = document.getElementById('boundary-epsilon');

        if (bc) bc.textContent = '[' + result.boundary.centroid.map(v => v.toFixed(4)).join(', ') + ']';
        if (br) br.textContent = result.boundary.radius.toFixed(6);
        if (be) be.textContent = result.boundary.epsilon.toFixed(4);

        // Visualization
        if (window.BoundaryViz && document.getElementById('boundary-canvas')) {
            console.log('[StegVerse Demo] Attaching visualization...');
            try {
                window._vizController = BoundaryViz.attachInteractive('boundary-canvas', inputs, result);
                console.log('[StegVerse Demo] Visualization attached.');
            } catch (vizErr) {
                console.error('[StegVerse Demo] Visualization failed:', vizErr);
            }
        } else {
            console.warn('[StegVerse Demo] Visualization skipped: BoundaryViz or canvas missing.');
        }
    }

    function showError(msg) {
        console.error('[StegVerse Demo] ERROR:', msg);
        if (resultArea) resultArea.classList.remove('hidden');
        if (verdictBadge) {
            verdictBadge.textContent = 'ERROR';
            verdictBadge.className = 'verdict-badge verdict-fail_closed';
        }
        const errMsg = document.getElementById('error-message');
        if (errMsg) errMsg.textContent = msg;
    }

    function showFatal(msg) {
        const container = document.querySelector('.demo-input .panel') || document.body;
        const div = document.createElement('div');
        div.style.cssText = 'background:#3b0d0d;color:#f87171;padding:20px;border-radius:12px;margin:20px 0;font-weight:700;';
        div.textContent = msg;
        container.appendChild(div);
    }

    // Load default sample on first visit
    if (inputArea && !inputArea.value.trim()) {
        console.log('[StegVerse Demo] Loading default SDK sample...');
        loadSample('sdk');
    }

    console.log('[StegVerse Demo] Initialization complete.');
});
