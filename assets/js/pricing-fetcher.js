/**
 * StegVerse Pricing Fetcher v2
 * Renders pricing from manifest with ROI context and interactive calculator.
 */

(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined'
        ? module.exports = factory()
        : typeof define === 'function' && define.amd
        ? define(factory)
        : (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.StegVersePricing = factory());
}(this, function () {
    'use strict';

    const DEFAULT_SOURCE = 'https://raw.githubusercontent.com/StegVerse-org/manifests/main/pricing.json';

    async function fetchManifest(source) {
        const url = source || DEFAULT_SOURCE;
        const response = await fetch(url, { cache: 'no-store' });
        if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        return await response.json();
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

            if (item.duration) {
                const dur = document.createElement('div');
                dur.className = 'pricing-duration';
                dur.textContent = item.duration;
                card.appendChild(dur);
            }

            if (item.target_prevented_cost) {
                const target = document.createElement('div');
                target.className = 'pricing-target';
                target.textContent = `Prevents: ${item.target_prevented_cost} incidents`;
                card.appendChild(target);
            }

            if (item.features || item.focus) {
                const list = document.createElement('ul');
                list.className = 'pricing-features';
                const items = item.features || item.focus || [];
                items.forEach(f => {
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
            // Formula: monthly_evals * (incident_rate/100) * (governance_reduction/100) * avg_incident_cost * 12
            const savings = vals.monthly_evals * (vals.incident_rate / 100) * (vals.governance_reduction / 100) * vals.avg_incident_cost * 12;
            result.querySelector('.calc-value').textContent = '$' + Math.round(savings).toLocaleString();
        };

        form.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', update);
        });
        update();

        container.appendChild(calc);
    }

    async function render(containerId, opts) {
        const container = document.getElementById(containerId);
        if (!container) throw new Error(`Container #${containerId} not found`);

        container.innerHTML = '<p class="pricing-loading">Loading pricing...</p>';

        try {
            const manifest = await fetchManifest(opts.source);
            container.innerHTML = '';

            // Economic model header
            if (manifest.economic_model) {
                const econ = document.createElement('div');
                econ.className = 'pricing-econ';
                econ.innerHTML = `<p><strong>Model:</strong> Governance cost is ~10,000,000× cheaper than execution + failure cost. Break-even when <code>r · p_bad · (C_e + C_f) > C_g</code>.</p>`;
                container.appendChild(econ);
            }

            if (opts.sections) {
                opts.sections.forEach(key => {
                    if (manifest.tiers[key]) renderTier(container, manifest.tiers[key], key);
                });
            } else {
                Object.keys(manifest.tiers).forEach(key => {
                    renderTier(container, manifest.tiers[key], key);
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
            container.innerHTML = `<p class="pricing-error">Unable to load pricing: ${err.message}</p>`;
        }
    }

    return { fetchManifest, render, formatPrice };
}));
