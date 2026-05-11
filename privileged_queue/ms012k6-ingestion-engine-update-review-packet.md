# MS-012K.6 Ingestion Engine Update Review Packet

## Subject

```text
ms012k6-manifest-post-install-task-bridge-v1.zip
```

## Current sandbox result

```text
verdict: HOLD
classification: manual_review_required
reason: Bundle mutates tools/bundle_ingest.py; sandbox will not emit an automatic repair candidate.
candidate_created: false
```

## Proposed change

MS-012K.6 proposes to update:

```text
tools/bundle_ingest.py
```

so that `bundle-manifest.json` can declare bounded post-install tasks.

Supported shape:

```json
{
  "post_install_tasks": [
    "data/headless-tasks/transition-automation-controller-v1.json"
  ]
}
```

## Intended execution path

```text
bundle-manifest.json
→ post_install_tasks
→ tools/bundle_ingest.py validates task paths
→ tools/headless_cmd_runner.py executes declared tasks
→ data/headless-task-policy-v1.json validates authority
→ ingestion receipt records post-install execution
```

## Bounds

```text
Only runs after ordinary ALLOW ingest.
Only accepts task paths under data/headless-tasks/.
Only accepts .json task files.
Does not run for sandbox_queue, failed_bundles, or privileged_queue routes.
Does not modify workflow files.
Does not bypass data/headless-task-policy-v1.json.
Does not run arbitrary task globs.
```

## Authority basis

```text
transition element: TE-012-executable-support-surface-update
action class: modify_executable_support
authority level: 4_privileged_review
human approval required: true
sandbox required: true
required receipt: executable_support_review_packet
```

## Human decision required

Approve means:

```text
Replace tools/bundle_ingest.py with the reviewed MS-012K.6 version.
```

Reject means:

```text
Do not install MS-012K.6. Manifest-declared post-install automation remains unavailable.
```

## Expected if approved

The already-installed trigger bundle can then activate:

```text
data/headless-tasks/transition-automation-controller-v1.json
```

Expected reports:

```text
transition_discovery_reports/transition-automation-controller-report.json
transition_discovery_reports/transition-automation-controller-report.md
transition_discovery_reports/failed-bundle-boundary-report.json
transition_discovery_reports/failed-bundle-boundary-report.md
headless_cmd_reports/transition-automation-controller-v1.receipt.json
headless_cmd_reports/transition-automation-controller-v1.report.md
```

## Decision marker

```text
PENDING_HUMAN_DECISION
```
