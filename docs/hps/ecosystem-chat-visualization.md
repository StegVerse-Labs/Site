# HPS Ecosystem Chat Visualization

## Purpose

This document defines the Site-side preview contract for displaying Harmonic Principle of Standing (HPS) state inside Ecosystem Chat.

The Site does not own HPS mathematics. The canonical formalism lives in:

```text
Admissible-Existence/HPS
```

The Site does not own ecosystem-wide HPS orchestration. That belongs to:

```text
master-records/orchestration
```

The Site displays HPS as a preview visualization surface only.

## Boundary

```text
Site HPS visualization is not authority.
Site HPS visualization is not execution.
Site HPS visualization is not a live receipt issuer.
Site HPS visualization is not proof of current backend standing.
```

The Site may display fixture-bound HPS state and explain how a future live governed path should expose standing, capability windows, expiration, and reconstruction posture.

## Required display concepts

A valid Site HPS preview should distinguish:

- heartbeat state;
- standing class;
- standing score;
- capability windows open/closed/expired;
- replay availability;
- reconstruction availability;
- chain head reference;
- preview-only/no-authority posture.

## Canonical visualization statement

```text
HPS visualization is not a generic status light.
It is a governed preview of standing, phase, capability availability, expiration, and reconstructability.
```

## Site integration rule

The HPS preview should remain secondary to the primary Ecosystem Chat path. It should enhance the interaction-band and continuation-panel experience without turning the page into a task launcher, execution console, or repo control panel.

## Initial fixture

The initial fixture is:

```text
fixtures/ecosystem-chat/hps-visualization-status.example.json
```

The checker is:

```text
scripts/check_site_hps_visualization.py
```

## Future live path

When backend authority exists, the Site may consume a live HPS visualization payload produced from:

```text
heartbeat receipt + standing score + capability windows + expiration receipts
```

Until then, the Site remains preview-only.
