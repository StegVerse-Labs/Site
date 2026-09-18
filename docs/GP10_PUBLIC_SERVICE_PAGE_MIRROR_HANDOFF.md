# GP10 Public Service Page Mirror Handoff

Status: SOURCE_PUBLISHED / PAGES_DEPLOYED / USER_OBSERVED_ON_CUSTOM_DOMAIN
Updated: 2026-09-17
Repository: `StegVerse-Labs/Site`
Parent commercial goal: `GP10-COMMERCIAL-RESPONSE-VALIDATION-001`
Source authority: `StegVerse-Labs/GP10/docs/business/PAID_FIELD_VALIDATION_OFFER.md`
Site claim: `SITE-GP10-PUBLIC-SERVICE-PAGE-20260917`

## Goal

Publish a normal prospect-facing GP10 service page on the public StegVerse Site while preserving the existing GP10 workspace as an unlisted, noindex operational surface.

## Public surface

```text
source: gp10-field-validation.html
intended public URL: https://stegverse.org/gp10-field-validation.html
discovery link: what-we-do.html
contact CTA: mailto:rigel@stegverse.org
```

The public page is explicitly indexable and contains:
- who the service is for;
- customer-authorized input types;
- provenance/conflict-preserving review behavior;
- bounded deliverables;
- explicit exclusions and authority limits;
- no-system-integration requirement for the initial review;
- scope-before-price posture;
- a request-review email CTA.

## Authority boundaries

The public page does not claim that GP10 itself:
- proves locomotive identity beyond supplied evidence;
- certifies safety, regulatory, emissions, or service compliance;
- determines part fitment;
- provides legal approval;
- validates market pricing or profitability;
- authorizes repair, retrofit, commissioning, purchase, release, or operation.

A request for review is discovery only. Paid work begins only after a written scope identifies the authorized dataset, exact deliverables, exclusions, customer responsibilities, fee, and stop-work conditions.

## Workspace isolation

The following existing pages remain operational surfaces and are not linked from the public GP10 service page:

```text
gp10-workspace.html
gp10-workspace-examples.html
```

Their existing `noindex,nofollow,noarchive` contract remains unchanged. The new public service page is a separate marketing/discovery surface and does not grant access to, or change the authority of, the workspace.

## Source evidence

```text
Site claim commit: 6c957e3d638856c2b3570d41fd356ede8dcfe793
public page source commit: f09cd593bde999cfd98b74bf042db6d2f6ebba0a
What We Do discovery-link commit: 15782d8b0773bfde973da09102a724635f16e596
claim-scope reconciliation commit: e2afbf2acc704836e1cb26e752322db34c75edb2
```

Source presence and repository commits are not live-route evidence. The custom domain is defined by repository `CNAME` as `stegverse.org`; a served-body observation is required before claiming that the new route is live.

## Cost and infrastructure boundary

No form backend, CRM, storage service, runtime, scheduler, provider connector, customer-upload endpoint, credential path, or new GitHub Actions workflow was added. No routine GitHub Actions run is required merely to create the source page.

## Continuation

1. Reconcile Site README and the existing GP10 workspace handoff.
2. Reconcile GP10 repository README/handoff and the canonical commercial-response task record.
3. Observe the live custom-domain route without treating source/merge as deployment proof.
4. If live, use the public URL in future prospect follow-up only as explanatory context; do not treat page visits, delivery, or opens as commercial validation.


## Native Pages deployment evidence

The repository's native GitHub Pages publisher completed successfully for a main commit that contains the new public page, the `what-we-do.html` discovery link, the Site README reconciliation, the public-page handoff, and the workspace-isolation handoff.

```text
Pages run: 35305152499
head SHA: 242d62a06088d81837a44c412a9af0dc0b6ce5b6
event: dynamic
run conclusion: success
build job: 105475731048 / success
deploy job: 105475763615 / success
Deploy to GitHub Pages step: success
```

This establishes successful native Pages publication for the exact source head. It does **not** substitute for a direct served-body observation of `https://stegverse.org/gp10-field-validation.html`. The network surfaces available during this session did not independently return that custom-domain body, so `served_body_observed=false` remains explicit.

No workflow was manually dispatched for this task; the observed Pages run was the repository's native publication event.


## Served-body re-observation attempt — 2026-09-17

A fresh direct external observation was attempted for:

```text
https://stegverse.org/gp10-field-validation.html
https://stegverse-labs.github.io/Site/gp10-field-validation.html
```

The available external web-fetch surface reported both URLs as inaccessible from the tool environment. A separate container network probe also failed DNS resolution from its isolated runtime.

Classification:

```text
native_pages_deployment_success: true
custom_domain_served_body_observed: false
github_pages_served_body_observed: false
served_body_probe_result: TOOL_NETWORK_ACCESS_UNAVAILABLE
site_failure_inferred: false
deployment_failure_inferred: false
```

This does not negate the already-observed successful native Pages deployment. It also does not upgrade source/deployment evidence into served-body proof. No workflow dispatch or publication retry was triggered.


## User-provided iPhone custom-domain observation — 2026-09-17

The user supplied a screenshot from an iPhone browser showing the GP10 public service page rendered under the visible origin `stegverse.org`.

Observed visible content includes the exact deployed page identity and primary call-to-action:

```text
origin shown in browser chrome: stegverse.org
visible eyebrow: GP10 · BOUNDED EVIDENCE REVIEW FOR OLDER AND REBUILT LOCOMOTIVES
visible hero: Clean up the record trail without pretending uncertainty is certainty.
visible CTA: Request a scoped review
visible secondary action: See what you receive
visible scope-boundary panel: present
```

Screenshot evidence:

```text
evidence_source: USER_PROVIDED_IPHONE_SCREENSHOT
sha256: 151a7311f57f30bfc20fb82c81bf9b92aa34b8862b8f1b50141877f9fd5be6b4
pixel_dimensions: 707x1536
custom_domain_served_body_observed: true
independent_machine_fetch_observed: false
commercial_validation_effect: NONE
```

The browser chrome displays the origin rather than the full path, while the rendered body matches the deployed `gp10-field-validation.html` hero and CTA content. This closes the custom-domain served-body predicate as **user-observed evidence**. It does not convert page reachability, a page view, or the screenshot itself into buyer interest, response evidence, paid-scope evidence, or revenue.
