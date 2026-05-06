/**
 * StegVerse Pricing Fetcher v2
 * Renders pricing from manifest with ROI context, fallback manifest, and interactive calculator.
 */

(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined'
        ? module.exports = factory()
        : typeof define === 'function' && define.amd
        ? define(factory)
        : (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.StegVersePricing = factory());
}(this, function () {
    'use strict';

    const DEFAULT_SOURCES = [
        'pricing.json',
        './pricing.json',
        '/Site/pricing.json',
        'https://stegverse-labs.github.io/Site/pricing.json',
        'https://raw.githubusercontent.com/StegVerse-Labs/Site/main/pricing.json',
        'https://raw.githubusercontent.com/StegVerse-org/manifests/main/pricing.json'
    ];

    const FALLBACK_MANIFEST = {
        "_schema": "stegverse-pricing-v2",
        "_updated": "2026-05-01T08:48:00Z",
        "_basis": "GCAT/BCAT cost-of-transitions model: C_g << C_e + C_f",
        "currency": "USD",
        "economic_model": {
            "governance_cost_per_eval": "~10^0 FLOPs",
            "execution_cost_per_eval": "~10^6–10^9 FLOPs",
            "failure_cost_per_incident": "$10K–$10M+",
            "break_even": "r * p_bad * (C_e + C_f) > C_g",
            "roi_narrative": "Prevent a small fraction of bad actions → Save millions"
        },
        "value_tiers": {
            "prevented_failure_cost": {
                "low": 10000,
                "medium": 100000,
                "high": 1000000,
                "catastrophic": 10000000
            }
        },
        "tiers": {
            "audit": {
                "label": "Trust & Risk Audit",
                "description": "Expose silent failure modes before they compound",
                "economic_basis": "Fixed engagement. Value = prevented incidents × average incident cost.",
                "items": [
                    {
                        "id": "audit-tier-1",
                        "name": "AI & Governance Risk Audit",
                        "price": { "min": 12500, "max": 18000 },
                        "duration": "2–3 weeks",
                        "target_prevented_cost": "low–medium",
                        "focus": ["AI/automation inventory", "Failure mode analysis", "Oversight gaps", "Governance defensibility"],
                        "deliverables": ["Executive summary", "Risk register", "Board-ready briefing"],
                        "roi_note": "Single prevented incident ($50K–$200K) covers engagement cost 3–15×"
                    },
                    {
                        "id": "audit-tier-2",
                        "name": "Full Trust & Risk Audit",
                        "price": { "min": 20000, "max": 30000 },
                        "duration": "2–3 weeks",
                        "recommended": true,
                        "target_prevented_cost": "medium–high",
                        "focus": ["Everything in Tier 1", "Credential lifecycle", "Trust boundary mapping", "Privilege drift", "Audit trail integrity"],
                        "deliverables": ["Executive summary", "Risk register", "Remediation roadmap", "Board-ready briefing"],
                        "roi_note": "Prevents cascade failures. One stopped cascade ($500K–$2M) covers cost 15–100×"
                    },
                    {
                        "id": "audit-tier-3",
                        "name": "Continuous Trust Oversight",
                        "price": { "min": 60000, "max": 90000, "period": "year" },
                        "duration": "Quarterly (every 90 days)",
                        "target_prevented_cost": "high–catastrophic",
                        "focus": ["Delta analysis per quarter", "Drift detection", "Updated risk register", "Executive review"],
                        "deliverables": ["Quarterly executive summary", "Updated risk register", "Prioritized actions", "Executive review call"],
                        "roi_note": "Annual incident avoidance target: $2M–$10M. Cost ratio: 1:30 to 1:150"
                    }
                ]
            },
            "sdk": {
                "label": "StegVerse SDK",
                "description": "GCAT/BCAT execution-layer primitives. Embed governance into your systems.",
                "economic_basis": "Per-seat or per-evaluation. Value = C_g << C_e + C_f on every transition.",
                "items": [
                    {
                        "id": "sdk-community",
                        "name": "Community",
                        "price": { "min": 0, "max": 0 },
                        "period": "forever",
                        "evaluations_included": "unlimited",
                        "target_user": "Individual developers, researchers, proof-of-concept",
                        "features": ["GCAT/BCAT core evaluator (browser Tier 0)", "Basic receipt generation", "Deterministic testing", "Community support"],
                        "roi_note": "Free entry. Cost = your compute time. Value = learn the pattern before production."
                    },
                    {
                        "id": "sdk-pro",
                        "name": "Pro",
                        "price": { "min": 99, "max": 199, "period": "month", "unit": "seat" },
                        "evaluations_included": "unlimited",
                        "target_user": "Teams shipping to production",
                        "features": ["Everything in Community", "Server-side evaluation", "TV/TVC ephemeral secrets", "Deterministic test suites", "CI/CD integration", "Priority support"],
                        "roi_note": "At 1,000 evals/month: $0.10–$0.20 per evaluation. One prevented bad deploy saves $10K–$100K."
                    },
                    {
                        "id": "sdk-enterprise",
                        "name": "Enterprise",
                        "price": { "min": 0, "max": 0, "contact": true },
                        "evaluations_included": "unlimited",
                        "target_user": "Organizations with compliance requirements",
                        "features": ["Everything in Pro", "Custom boundary geometries", "On-premise / air-gapped", "SLA guarantees", "Dedicated support", "Custom integrations"],
                        "roi_note": "Custom pricing based on evaluation volume + prevented incident value. Typical: 1:500 to 1:5000 cost-to-value ratio."
                    }
                ]
            },
            "platform": {
                "label": "StegVerse Platform",
                "description": "Managed execution infrastructure. We run the governance layer; you run the business.",
                "economic_basis": "Per-evaluation or flat rate. Value = zero infrastructure + zero governance ops + maximum safety.",
                "items": [
                    {
                        "id": "platform-starter",
                        "name": "Starter",
                        "price": { "min": 499, "max": 799, "period": "month" },
                        "evaluations_included": 50000,
                        "overage": { "per_1000": 15 },
                        "target_user": "Small teams, startups",
                        "features": ["50,000 evaluations/month", "Standard receipts", "Email support", "99.5% uptime", "Basic analytics"],
                        "roi_note": "$0.01 per evaluation. One prevented data corruption incident ($50K) covers 3+ years of platform cost."
                    },
                    {
                        "id": "platform-growth",
                        "name": "Growth",
                        "price": { "min": 2499, "max": 3999, "period": "month" },
                        "evaluations_included": 500000,
                        "overage": { "per_1000": 10 },
                        "target_user": "Scaling teams, mid-market",
                        "features": ["500,000 evaluations/month", "Advanced analytics", "Priority support", "99.9% uptime", "Custom domains", "Team management"],
                        "roi_note": "$0.005–$0.008 per evaluation. Prevents cascade failures at scale. One stopped cascade ($500K) covers 1+ year."
                    },
                    {
                        "id": "platform-scale",
                        "name": "Scale",
                        "price": { "min": 0, "max": 0, "contact": true },
                        "evaluations_included": "unlimited",
                        "target_user": "Enterprise, regulated industries",
                        "features": ["Unlimited evaluations", "Dedicated infrastructure", "Custom SLAs", "On-premise option", "White-glove onboarding", "Quarterly business reviews"],
                        "roi_note": "Custom pricing based on evaluation volume + compliance value + incident avoidance. Typical enterprise saves $2M–$20M annually vs ungoverned execution."
                    }
                ]
            }
        },
        "calculator": {
            "enabled": true,
            "fields": [
                { "id": "monthly_evals", "label": "Monthly state transitions evaluated", "type": "number", "default": 10000 },
                { "id": "incident_rate", "label": "Current bad-action rate (%)", "type": "number", "default": 0.5 },
                { "id": "avg_incident_cost", "label": "Average incident cost ($)", "type": "number", "default": 50000 },
                { "id": "governance_reduction", "label": "Governance reduction in bad actions (%)", "type": "number", "default": 80 }
            ],
            "formula": "monthly_evals * (incident_rate / 100) * (governance_reduction / 100) * avg_incident_cost * 12"
        },
        "notes": [
            "All pricing grounded in GCAT/BCAT cost model: governance cost C_g is ~10^7× cheaper than execution cost C_e + failure cost C_f.",
            "Break-even: r * p_bad * (C_e + C_f) > C_g. Since C_g is tiny, threshold is extremely low.",
            "Academic and nonprofit discounts: 50% off Pro/Platform. Contact for Enterprise custom terms.",
            "Annual billing: 2 months free on all paid tiers."
        ]
    };

    async function fetchManifest(source) {
        const sources = Array.isArray(source)
            ? source
            : source
            ? [source]
            : DEFAULT_SOURCES;

        const errors = [];

        for (const url of sources) {
            try {
                const response = await fetch(url, { cache: 'no-store' });
                if (!response.ok) {
                    errors.push(`${url}: HTTP ${response.status}`);
                    continue;
                }
                return await response.json();
            } catch (err) {
                errors.push(`${url}: ${err.message}`);
            }
        }

        console.warn('StegVerse pricing manifest unavailable. Rendering embedded fallback.', errors);
        return FALLBACK_MANIFEST;
    }

    function formatPrice(price) {
        if (price.contact) return 'Contact us';
        if (price.min === 0 && price.max === 0) return 'Free';
        const min = price.min.toLocaleString();
        const max = price.max.toLocaleString();
        const period = price.period ? ` / ${price.period}` : '';
        const unit = price.unit ? ` per ${price.unit}` : '';
        if (min === max) return `$${min}${period}${unit}`;
        return `$${min} – $${max}${period}${unit}`;
    }

    function renderDetail(container, label, value) {
        if (value === undefined || value === null || value === '') return;

        const detail = document.createElement('div');
        detail.className = 'pricing-duration';
        detail.textContent = `${label}: ${value}`;
        container.appendChild(detail);
    }

    function renderTier(container, tierData, tierKey) {
        const section = document.createElement('section');
        section.className = 'pricing-section';
        section.dataset.tier = tierKey;

        const header = document.createElement('h2');
        header.textContent = tierData.label;
        section.appendChild(header);

        const desc = document.createElement('p');
        desc.className = 'pricing-desc';
        desc.textContent = tierData.description;
        section.appendChild(desc);

        if (tierData.economic_basis) {
            const basis = document.createElement('p');
            basis.className = 'pricing-basis';
            basis.textContent = tierData.economic_basis;
            section.appendChild(basis);
        }

        const grid = document.createElement('div');
        grid.className = 'pricing-grid';

        tierData.items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'pricing-card';
            if (item.recommended) card.classList.add('recommended');

            const name = document.createElement('h3');
            name.textContent = item.name;
            card.appendChild(name);

            const price = document.createElement('div');
            price.className = 'pricing-price';
            price.textContent = formatPrice(item.price);
            card.appendChild(price);

            renderDetail(card, 'Duration', item.duration);
            renderDetail(card, 'Evaluations included', item.evaluations_included);
            renderDetail(card, 'Target user', item.target_user);

            if (item.target_prevented_cost) {
                const target = document.createElement('div');
                target.className = 'pricing-target';
                target.textContent = `Prevents: ${item.target_prevented_cost} incidents`;
                card.appendChild(target);
            }

            if (item.overage && item.overage.per_1000) {
                const overage = document.createElement('div');
                overage.className = 'pricing-target';
                overage.textContent = `Overage: $${item.overage.per_1000}/1,000 evaluations`;
                card.appendChild(overage);
            }

            const bullets = [
                ...(item.features || []),
                ...(item.focus || []),
                ...(item.deliverables || []).map(d => `Deliverable: ${d}`)
            ];

            if (bullets.length) {
                const list = document.createElement('ul');
                list.className = 'pricing-features';
                bullets.forEach(f => {
                    const li = document.createElement('li');
                    li.textContent = f;
                    list.appendChild(li);
                });
                card.appendChild(list);
            }

            if (item.roi_note) {
                const roi = document.createElement('div');
                roi.className = 'pricing-roi';
                roi.textContent = item.roi_note;
                card.appendChild(roi);
            }

            if (item.recommended) {
                const badge = document.createElement('span');
                badge.className = 'pricing-badge';
                badge.textContent = 'Recommended';
                card.appendChild(badge);
            }

            grid.appendChild(card);
        });

        section.appendChild(grid);
        container.appendChild(section);
    }

    function renderCalculator(container, calculator) {
        if (!calculator || !calculator.enabled) return;

        const calc = document.createElement('div');
        calc.className = 'pricing-calculator';

        const title = document.createElement('h2');
        title.textContent = 'ROI Calculator';
        calc.appendChild(title);

        const desc = document.createElement('p');
        desc.textContent = 'Estimate annual savings from commit-time governance.';
        calc.appendChild(desc);

        const form = document.createElement('div');
        form.className = 'calc-form';

        calculator.fields.forEach(field => {
            const row = document.createElement('div');
            row.className = 'calc-row';

            const label = document.createElement('label');
            label.textContent = field.label;
            row.appendChild(label);

            const input = document.createElement('input');
            input.type = 'number';
            input.value = field.default;
            input.dataset.field = field.id;
            input.className = 'calc-input';
            row.appendChild(input);

            form.appendChild(row);
        });

        calc.appendChild(form);

        const result = document.createElement('div');
        result.className = 'calc-result';
        result.innerHTML = '<span class="calc-value">—</span><span class="calc-label">Estimated annual savings</span>';
        calc.appendChild(result);

        const update = () => {
            const vals = {};
            calculator.fields.forEach(f => {
                const el = form.querySelector(`[data-field="${f.id}"]`);
                vals[f.id] = parseFloat(el?.value) || 0;
            });

            const savings = vals.monthly_evals * (vals.incident_rate / 100) * (vals.governance_reduction / 100) * vals.avg_incident_cost * 12;
            result.querySelector('.calc-value').textContent = '$' + Math.round(savings).toLocaleString();
        };

        form.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', update);
        });
        update();

        container.appendChild(calc);
    }

    async function render(containerId, opts = {}) {
        const container = document.getElementById(containerId);
        if (!container) throw new Error(`Container #${containerId} not found`);

        container.innerHTML = '<p class="pricing-loading">Loading pricing...</p>';

        try {
            const manifest = await fetchManifest(opts.source);
            container.innerHTML = '';

            if (manifest.economic_model) {
                const econ = document.createElement('div');
                econ.className = 'pricing-econ';
                econ.innerHTML = `<p><strong>Model:</strong> Governance cost is ~10,000,000× cheaper than execution + failure cost. Break-even when <code>r · p_bad · (C_e + C_f) > C_g</code>.</p>`;
                container.appendChild(econ);
            }

            const tiers = manifest.tiers || {};
            if (opts.sections) {
                opts.sections.forEach(key => {
                    if (tiers[key]) renderTier(container, tiers[key], key);
                });
            } else {
                Object.keys(tiers).forEach(key => {
                    renderTier(container, tiers[key], key);
                });
            }

            renderCalculator(container, manifest.calculator);

            if (manifest.notes && manifest.notes.length) {
                const notes = document.createElement('div');
                notes.className = 'pricing-notes';
                manifest.notes.forEach(n => {
                    const p = document.createElement('p');
                    p.textContent = n;
                    notes.appendChild(p);
                });
                container.appendChild(notes);
            }
        } catch (err) {
            container.innerHTML = `<p class="pricing-error">Unable to render pricing: ${err.message}</p>`;
        }
    }

    return { fetchManifest, render, formatPrice };
}));
