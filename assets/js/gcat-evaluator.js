/**
 * GCAT/BCAT Tier 0 — Client-Side Commit Boundary Evaluator
 * StegVerse Demo — Browser-only, no backend, no secrets required
 * 
 * Implements the geometric boundary check:
 *   - Reconstructs commit-time constraint from run data
 *   - Measures divergence between proposed state and boundary
 *   - Returns ALLOW / DENY / FAIL-CLOSED with deterministic receipt
 * 
 * @version 0.1.0
 * @license MIT
 */

(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined'
        ? module.exports = factory()
        : typeof define === 'function' && define.amd
        ? define(factory)
        : (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.GCATEvaluator = factory());
}(this, function () {
    'use strict';

    // ─────────────────────────────────────────────────────────────
    // CONSTANTS & CONFIG
    // ─────────────────────────────────────────────────────────────
    const VERDICT = Object.freeze({
        ALLOW: 'ALLOW',
        DENY: 'DENY',
        FAIL_CLOSED: 'FAIL-CLOSED'
    });

    const DEFAULT_TOLERANCE = 1e-9;
    const HASH_ALGO = 'SHA-256';

    // ─────────────────────────────────────────────────────────────
    // GEOMETRIC PRIMITIVES
    // ─────────────────────────────────────────────────────────────

    /**
     * Vector operations for boundary geometry
     */
    const Vec = {
        add: (a, b) => a.map((v, i) => v + b[i]),
        sub: (a, b) => a.map((v, i) => v - b[i]),
        dot: (a, b) => a.reduce((sum, v, i) => sum + v * b[i], 0),
        norm: (a) => Math.sqrt(a.reduce((sum, v) => sum + v * v, 0)),
        scale: (a, s) => a.map(v => v * s),
        dist: (a, b) => Vec.norm(Vec.sub(a, b))
    };

    /**
     * GOD — Geometrically Ontological Divergence
     * The compression point where geometric boundary meets ontological
     * becoming meets irreducible divergence.
     * 
     * Computes divergence as the ratio of:
     *   - Distance from proposed state to commit boundary
     *   - Characteristic scale of the boundary manifold
     */
    function computeGOD(proposed, boundary, scale) {
        const d = Vec.dist(proposed, boundary.centroid);
        const s = scale || boundary.radius || 1.0;
        return d / s;
    }

    // ─────────────────────────────────────────────────────────────
    // BOUNDARY RECONSTRUCTION
    // ─────────────────────────────────────────────────────────────

    /**
     * Reconstruct the commit-time geometric boundary from run data.
     * 
     * The boundary is defined by:
     *   - centroid: mean position of all commit-time state vectors
     *   - radius: max distance from centroid to any commit-time state
     *   - normal: principal axis of variance (simplified PCA)
     *   - tolerance: epsilon for numerical stability
     */
    function reconstructBoundary(commitStates, opts = {}) {
        if (!Array.isArray(commitStates) || commitStates.length === 0) {
            throw new Error('reconstructBoundary: commitStates must be non-empty array');
        }

        const dims = commitStates[0].length;
        const n = commitStates.length;
        const tolerance = opts.tolerance || DEFAULT_TOLERANCE;

        // Centroid
        const centroid = commitStates.reduce((acc, s) => Vec.add(acc, s), new Array(dims).fill(0))
            .map(v => v / n);

        // Radius = max distance from centroid
        const radius = Math.max(...commitStates.map(s => Vec.dist(s, centroid)), tolerance);

        // Normal = direction of max variance (simplified)
        const centered = commitStates.map(s => Vec.sub(s, centroid));
        const cov = new Array(dims).fill(0).map(() => new Array(dims).fill(0));
        for (let i = 0; i < dims; i++) {
            for (let j = 0; j < dims; j++) {
                cov[i][j] = centered.reduce((sum, c) => sum + c[i] * c[j], 0) / n;
            }
        }
        // Power iteration for principal eigenvector (1 step = sufficient for demo)
        let normal = new Array(dims).fill(1);
        for (let iter = 0; iter < 8; iter++) {
            const next = new Array(dims).fill(0);
            for (let i = 0; i < dims; i++) {
                for (let j = 0; j < dims; j++) {
                    next[i] += cov[i][j] * normal[j];
                }
            }
            const nNorm = Vec.norm(next);
            normal = nNorm > tolerance ? Vec.scale(next, 1 / nNorm) : normal;
        }

        return { centroid, radius, normal, tolerance, dims };
    }

    // ─────────────────────────────────────────────────────────────
    // VERDICT ENGINE
    // ─────────────────────────────────────────────────────────────

    /**
     * Evaluate a proposed state transition against the commit boundary.
     * 
     * Logic:
     *   - Compute GOD divergence
     *   - If divergence <= 1.0: ALLOW (within or on boundary)
     *   - If 1.0 < divergence <= 1.0 + epsilon: DENY (outside, recoverable)
     *   - If divergence > 1.0 + epsilon: FAIL-CLOSED (catastrophic divergence)
     * 
     * The epsilon band is the "ontological uncertainty zone" — the region
     * where the boundary itself is being tested/expanded.
     */
    function evaluate(proposedState, boundary, opts = {}) {
        const epsilon = opts.epsilon || 0.05;  // 5% uncertainty zone
        const scale = opts.scale || boundary.radius;

        const god = computeGOD(proposedState, boundary, scale);

        let verdict;
        let confidence;

        if (god <= 1.0) {
            verdict = VERDICT.ALLOW;
            confidence = 1.0 - god;  // 1.0 at center, 0.0 at boundary
        } else if (god <= 1.0 + epsilon) {
            verdict = VERDICT.DENY;
            confidence = 1.0 - ((god - 1.0) / epsilon);  // 1.0 at boundary+0, 0.0 at boundary+epsilon
        } else {
            verdict = VERDICT.FAIL_CLOSED;
            confidence = 0.0;
        }

        return {
            verdict,
            god,
            confidence: Math.max(0, Math.min(1, confidence)),
            boundary: {
                centroid: boundary.centroid,
                radius: boundary.radius,
                epsilon
            }
        };
    }

    // ─────────────────────────────────────────────────────────────
    // RECEIPT GENERATION (Deterministic, Portable, Verifiable)
    // ─────────────────────────────────────────────────────────────

    /**
     * Generate a deterministic receipt hash from evaluation result.
     * Uses SHA-256 of canonical JSON representation.
     * 
     * The receipt proves:
     *   - This evaluation happened
     *   - At this commit boundary
     *   - With this proposed state
     *   - Yielding this verdict
     * 
     * Portable: can be verified by any party with the same inputs.
     */
    async function generateReceipt(inputs, result, opts = {}) {
        const timestamp = opts.timestamp || new Date().toISOString();
        const version = opts.version || '0.1.0';

        const canonical = JSON.stringify({
            v: version,
            ts: timestamp,
            source: inputs.source || 'unknown',
            demo_id: inputs.demo_id || null,
            commit_states: inputs.commit_states,
            proposed_state: inputs.proposed_state,
            verdict: result.verdict,
            god: result.god,
            confidence: result.confidence,
            boundary_centroid: result.boundary.centroid,
            boundary_radius: result.boundary.radius,
            boundary_epsilon: result.boundary.epsilon
        }, null, 0);  // compact, deterministic

        const encoder = new TextEncoder();
        const data = encoder.encode(canonical);
        const hashBuffer = await crypto.subtle.digest(HASH_ALGO, data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

        return {
            hash: hashHex,
            algo: HASH_ALGO,
            canonical,
            timestamp,
            version
        };
    }

    // ─────────────────────────────────────────────────────────────
    // MAIN API
    // ─────────────────────────────────────────────────────────────

    /**
     * Run a full GCAT/BCAT evaluation from run data.
     * 
     * Input schema (matches your demo.md form):
     * {
     *   "source": "llm_adapter" | "sdk" | "human",
     *   "demo_id": "string",
     *   "commit_states": [[x1, y1, ...], [x2, y2, ...], ...],
     *   "proposed_state": [x, y, ...],
     *   "metadata": { ... }
     * }
     */
    async function run(inputs, opts = {}) {
        // Validate
        if (!inputs.commit_states || inputs.commit_states.length === 0) {
            throw new Error('run: commit_states required (non-empty array of state vectors)');
        }
        if (!inputs.proposed_state) {
            throw new Error('run: proposed_state required (state vector)');
        }
        if (inputs.commit_states[0].length !== inputs.proposed_state.length) {
            throw new Error('run: dimension mismatch between commit_states and proposed_state');
        }

        // Reconstruct boundary from commit-time states
        const boundary = reconstructBoundary(inputs.commit_states, opts);

        // Evaluate proposed state
        const result = evaluate(inputs.proposed_state, boundary, opts);

        // Generate portable receipt
        const receipt = await generateReceipt(inputs, result, opts);

        return {
            verdict: result.verdict,
            god: result.god,
            confidence: result.confidence,
            boundary: result.boundary,
            receipt: receipt,
            inputs: {
                source: inputs.source,
                demo_id: inputs.demo_id,
                commit_count: inputs.commit_states.length,
                dimensions: boundary.dims
            }
        };
    }

    // ─────────────────────────────────────────────────────────────
    // DEMO HELPERS
    // ─────────────────────────────────────────────────────────────

    /**
     * Generate sample run data for the three sources.
     */
    function generateSample(source) {
        const rand = (seed) => {
            let s = seed || 42;
            return () => { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; };
        };

        // Fixed seeds per source for reproducible demos
        const rng = rand(source === 'llm_adapter' ? 11 : source === 'sdk' ? 22 : 33);
        const dims = 3;
        const nCommits = 5;

        // Commit states: deterministic cluster around origin
        const commitStates = Array.from({ length: nCommits }, () =>
            Array.from({ length: dims }, () => (rng() - 0.5) * 1.2)
        );

        // Use centroid as anchor for scaling — guarantees clean verdict zones
        const boundary = reconstructBoundary(commitStates);
        const anchor = boundary.centroid;
        const scale = boundary.radius;

        let proposed;
        if (source === 'sdk') {
            // Deep inside boundary → ALLOW (GOD ≈ 0.3)
            proposed = Vec.add(anchor, Vec.scale(Vec.sub(commitStates[0], anchor), 0.3));
        } else if (source === 'llm_adapter') {
            // Just outside boundary, inside epsilon zone → DENY (GOD ≈ 1.02)
            const dir = Vec.sub(commitStates[0], anchor);
            const dirNorm = Vec.norm(dir);
            const unitDir = dirNorm > boundary.tolerance ? Vec.scale(dir, 1 / dirNorm) : [1, 0, 0];
            proposed = Vec.add(anchor, Vec.scale(unitDir, scale * 1.02));
        } else {
            // Far outside boundary → FAIL-CLOSED (GOD ≈ 2.0)
            const dir = Vec.sub(commitStates[0], anchor);
            const dirNorm = Vec.norm(dir);
            const unitDir = dirNorm > boundary.tolerance ? Vec.scale(dir, 1 / dirNorm) : [1, 0, 0];
            proposed = Vec.add(anchor, Vec.scale(unitDir, scale * 2.0));
        }

        return {
            source,
            demo_id: `demo_${source}_${Date.now()}`,
            commit_states: commitStates,
            proposed_state: proposed,
            metadata: {
                generated_by: 'GCATEvaluator.generateSample',
                tier: 0,
                deterministic: true,
                anchor: anchor,
                scale: scale
            }
        };
    }

    // ─────────────────────────────────────────────────────────────
    // EXPORTS
    // ─────────────────────────────────────────────────────────────

    return {
        VERDICT,
        run,
        evaluate,
        reconstructBoundary,
        computeGOD,
        generateReceipt,
        generateSample,
        Vec
    };
}));
