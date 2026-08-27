# VA Private Document Actions Fanout — 2026-08-27 Mirror Handoff

## Authority and supersession

This is the newest continuation overlay for `docs/VA_PRIVATE_DOCUMENT_ACTIONS_FANOUT_MIRROR_HANDOFF.md`. It supersedes only the stale post-merge observability boundary in that historical handoff; the historical implementation and merge evidence remain authoritative.

```text
repository: StegVerse-Labs/Site
issue: Site#420
claim: SITE-VA-PRIVATE-DOCUMENT-HOURLY-FIXTURE-RETIREMENT-420-20260822
workflow: .github/workflows/va-private-document-runtime.yml
merge_commit: a8d6e1bf28291ff6ba7f0838950e6800760b7adf
state: MERGED_MAIN_PUSH_OBSERVED_VALIDATOR_FALSE_POSITIVE
credential_authority: TV/TVC
runtime_authority_effect: NONE
product_authority_effect: NONE
```

## Newly observable exact integrated execution

The current GitHub reader can enumerate arbitrary workflow runs by exact head SHA. The merge-triggered run previously described as unobservable is now directly observed:

```text
run: 32604657387
workflow_name: VA Private Document Fixture Validation
event: push
head_branch: main
head_sha: a8d6e1bf28291ff6ba7f0838950e6800760b7adf
job: 97107875859
job_name: validate-private-intake
run_conclusion: failure
```

Substantive execution steps all passed:

```text
credential refusal: PASS
anonymous exact-source fetch: PASS
preinstalled Python: PASS
bounded private-document fixture execution: PASS
privacy and authority boundaries: PASS
```

The only failed step was `Confirm validation-only containment`.

## Exact false-positive cause

The final containment step reads the workflow file itself and searches the raw text for these forbidden marker strings:

```text
schedule:
contents: write
github.token
GH_TOKEN:
actions/checkout@
actions/setup-python@
actions/upload-artifact@
git push
git commit
```

Those same literal strings are embedded inside the step's own Python `forbidden = [...]` list. Therefore `marker in workflow` is necessarily true for the checker source itself. The observed failure is a deterministic validator false positive, not evidence that hourly scheduling, GitHub-token authority, repository writeback, artifact custody, checkout/setup-python actions, or git mutation remained operational.

## Current completion boundary

Do **not** release the claim solely from this read because the canonical completion contract requires a PASS execution. Remaining machine-executable remediation is narrow and deterministic:

1. Change the containment validator so it inspects parsed YAML structure / executable workflow sections, or otherwise excludes its own checker literal source from forbidden-marker detection.
2. Preserve `workflow_dispatch`, bounded main-push validation, `permissions: {}`, anonymous exact-source acquisition, `/tmp`-only receipt behavior, `public_upload_enabled=false`, `raw_documents_published=false`, zero authority flags, and no persistence/custody authority.
3. Obtain an exact integrated PASS after the corrected validator is merged.
4. Record the run/job evidence in this lane and the claim registry.
5. Release the claim and close Site#420 only after that PASS.

No user action, credential entry, provider activation, iPhone action, private-upload activation, runtime activation, custody action, filing action, or claimant authority is required for this remediation.
