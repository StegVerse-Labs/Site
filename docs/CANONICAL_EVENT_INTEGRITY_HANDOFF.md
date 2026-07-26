# Canonical Event Integrity Handoff

## Repository

```text
StegVerse-Labs/Site
```

## Goal state

```text
canonical_event_schema_installed == true
canonical_sha256_validation_installed == true
stable_id_graph_validation_installed == true
adversarial_tests_installed == true
browser_gateway_binding_installed == false
```

## Installed path

```text
upstream governed event
→ schemas/ecosystem-node-canonical-event.schema.json
→ scripts/validate_ecosystem_node_canonical_events.py
→ stable event-ID graph validation
→ rendering eligibility evidence
```

## Non-authority invariants

```text
site_validation_is_execution == false
site_validation_is_admissibility == false
site_validation_is_publication_authority == false
hash_verification_is_signature_verification == false
rendering_eligibility_is_custody == false
projection_visibility_is_authority == false
```

## Activation requirement

The next goal must bind the browser renderer to validated upstream records without replacing the existing local preview boundary. Upstream records must use canonical SHA-256 and must not be silently rehashed, repaired, reordered, or assigned replacement identifiers by the browser.

## Local verification

```bash
python scripts/validate_ecosystem_node_canonical_events.py
python -m pytest tests/test_ecosystem_node_canonical_events.py -q
```

No manual user action is required for repository validation.
