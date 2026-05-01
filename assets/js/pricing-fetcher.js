/**
 * StegVerse Pricing Fetcher
 * Pulls pricing manifest from a configurable source and renders it into the DOM.
 * Zero dependencies. Works with any static site.
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

            if (item.focus || item.features) {
                const list = document.createElement('ul');
                list.className = 'pricing-features';
                const items = item.focus || item.features || [];
                items.forEach(f => {
                    const li = document.createElement('li');
                    li.textContent = f;
                    list.appendChild(li);
                });
                card.appendChild(list);
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

    async function render(containerId, opts) {
        const container = document.getElementById(containerId);
        if (!container) throw new Error(`Container #${containerId} not found`);

        container.innerHTML = '<p class="pricing-loading">Loading pricing...</p>';

        try {
            const manifest = await fetchManifest(opts.source);
            container.innerHTML = '';

            if (opts.sections) {
                opts.sections.forEach(key => {
                    if (manifest.tiers[key]) renderTier(container, manifest.tiers[key], key);
                });
            } else {
                Object.keys(manifest.tiers).forEach(key => {
                    renderTier(container, manifest.tiers[key], key);
                });
            }

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
