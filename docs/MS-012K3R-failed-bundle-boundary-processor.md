# MS-012K.3R Failed Bundle Boundary Processor

## Purpose

This bundle turns `failed_bundles/` into an active bounded automation surface.

It does not merely classify evidence. It routes evidence within already-declared boundaries.

## Boundary behavior

```text
failed_bundles/
→ classify failed evidence group
→ terminal/deprecated/stale → reviewed_failed_bundles/
→ retryable repair → sandbox_queue/
→ workflow/authority mutation → privileged_queue/
→ unknown → remain in failed_bundles/
→ emit receipts and report
→ stop
```

## Safety

```text
No workflow files.
No deletion.
No direct install.
No sandbox direct install.
No authority expansion.
Unknown remains failed.
```
