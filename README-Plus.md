# Transition Element Pages Bundle

## Assumptions

1. Every transition element should have its own public page.
2. Each element page should render from the shared discovery data file, not from duplicated hardcoded content.
3. The discovery map should link to each element page.
4. The transition class page should link relevant classifications back to element detail pages.
5. No workflow files are added or changed.

## Done Definition

This bundle is done when:

1. `data/formalism-tests/transition-discovery-map.json` includes `detail_page` and `details` for every mapped element.
2. `transition-discovery.html` links every element card to its page.
3. `transition-elements/index.html` lists every element page.
4. Each current mapped element has a page under `transition-elements/`.
5. `transition-table-classes.html` includes an Element column with links to detail pages.
6. No workflow files are included.

## Element Pages Included

```text
transition-elements/ae.html
transition-elements/bc.html
transition-elements/chf.html
transition-elements/dc.html
transition-elements/daco.html
transition-elements/triad.html
transition-elements/iw.html
transition-elements/re.html
transition-elements/reset-boundary.html
transition-elements/evolve-boundary.html
transition-elements/ai-block.html
transition-elements/finco-chain.html
transition-elements/role-non-transfer.html
transition-elements/local-composite.html
transition-elements/replay-non-reversal.html
transition-elements/representation-non-consequence.html
```

## Source of Truth

Each page renders from:

```text
data/formalism-tests/transition-discovery-map.json
```

The page shell only declares the `element_id`. Updating the shared JSON updates the element page content.

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
