---
layout: default
title: "Live Demo — Tier 0"
permalink: /demo.html
---

<!-- GCAT/BCAT Tier 0 — Browser-only Evaluation + Boundary Visualization -->
<script src="{{ '/assets/js/gcat-evaluator.js' | relative_url }}"></script>
<script src="{{ '/assets/js/boundary-viz.js' | relative_url }}"></script>
<script src="{{ '/assets/js/demo-integration.js' | relative_url }}"></script>

<section class="demo-hero">
  <div class="tier-badge">Tier 0 · Browser-only · No backend required</div>
  <h1>Stale-state execution vs.<br>commit-time constraint.</h1>
  <p class="lead">
    Paste static run data below. The demo reconstructs the commit boundary locally
    and returns <strong>ALLOW</strong>, <strong>DENY</strong>, or <strong>FAIL-CLOSED</strong>
    with a portable receipt hash.
  </p>
</section>

<section class="demo-controls">
  <div class="sample-buttons">
    <button id="sample-llm" class="btn-sample">Load LLM Adapter Sample</button>
    <button id="sample-sdk" class="btn-sample">Load SDK Sample</button>
    <button id="sample-human" class="btn-sample">Load Human Sample</button>
  </div>
</section>

<section class="demo-input">
  <div class="panel">
    <h2>Input run data</h2>
    <p class="panel-desc">
      This can be produced by a human, SDK example, or LLM adapter.
      The key distinction: the LLM proposes; StegVerse evaluates <em>before</em> effect.
    </p>
    <form id="demo-form">
      <textarea id="run-data-input" class="code-input" rows="18" placeholder='{
  "source": "llm_adapter",
  "demo_id": "demo_001",
  "commit_states": [
    [0.1, -0.2, 0.5],
    [-0.3, 0.4, -0.1],
    [0.2, 0.1, 0.3]
  ],
  "proposed_state": [0.5, -0.6, 0.8],
  "metadata": {}
}'></textarea>
      <button type="submit" class="btn-evaluate">Evaluate Commit Boundary</button>
    </form>
  </div>
</section>

<section id="result-display" class="demo-result hidden">
  <div class="panel">
    <h2>Evaluation Result</h2>

    <div class="result-grid">
      <div class="result-cell">
        <div class="result-label">Verdict</div>
        <div id="verdict-badge" class="verdict-badge">—</div>
      </div>
      <div class="result-cell">
        <div class="result-label">GOD Divergence</div>
        <div id="god-value" class="metric-value">—</div>
      </div>
      <div class="result-cell">
        <div class="result-label">Confidence</div>
        <div class="confidence-bar">
          <div id="confidence-bar" class="confidence-bar-fill"></div>
        </div>
      </div>
    </div>

    <!-- Boundary Visualization -->
    <div class="viz-container">
      <h3>Boundary Geometry</h3>
      <canvas id="boundary-canvas" class="viz-canvas"></canvas>
      <p class="viz-hint">← drag to rotate · green sphere = commit boundary · colored dot = proposed state</p>
    </div>

    <div class="result-details">
      <h3>Boundary Parameters</h3>
      <table class="data-table">
        <tr><td>Centroid</td><td id="boundary-centroid">—</td></tr>
        <tr><td>Radius</td><td id="boundary-radius">—</td></tr>
        <tr><td>Epsilon Zone</td><td id="boundary-epsilon">—</td></tr>
      </table>
    </div>

    <div class="result-receipt">
      <h3>Portable Receipt</h3>
      <div class="receipt-hash-row">
        <code id="receipt-hash" class="hash-display">—</code>
        <button class="btn-copy" onclick="navigator.clipboard.writeText(document.getElementById('receipt-hash').textContent)">Copy</button>
      </div>
      <details>
        <summary>Canonical form (for verification)</summary>
        <textarea id="receipt-canonical" class="code-input" rows="6" readonly></textarea>
      </details>
    </div>

    <div id="error-message" class="error-display"></div>
  </div>
</section>

<section class="demo-explanation">
  <div class="panel">
    <h2>What is happening here?</h2>
    <div class="explainer-grid">
      <div class="explainer-card">
        <h3>1. Commit Boundary</h3>
        <p>
          The <strong>commit_states</strong> array defines the geometric boundary
          of valid state space at commit time. The evaluator computes the centroid,
          radius, and principal normal of this manifold.
        </p>
      </div>
      <div class="explainer-card">
        <h3>2. GOD Divergence</h3>
        <p>
          <strong>Geometrically Ontological Divergence</strong> measures how far the
          proposed state sits from the commit boundary, normalized by the boundary's
          characteristic scale. GOD = 1.0 is the surface.
        </p>
      </div>
      <div class="explainer-card">
        <h3>3. Verdict</h3>
        <p>
          <span class="verdict-allow-inline">ALLOW</span> — within boundary, execute.<br>
          <span class="verdict-deny-inline">DENY</span> — outside but recoverable, reject.<br>
          <span class="verdict-fail-inline">FAIL-CLOSED</span> — catastrophic divergence, halt.
        </p>
      </div>
      <div class="explainer-card">
        <h3>4. Receipt</h3>
        <p>
          A SHA-256 hash of the canonical evaluation record. Anyone with the same
          inputs can reproduce the same hash, proving this evaluation happened
          without trusting the evaluator.
        </p>
      </div>
    </div>
  </div>
</section>
