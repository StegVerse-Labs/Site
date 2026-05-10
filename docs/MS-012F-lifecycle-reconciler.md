# MS-012F Lifecycle Reconciler

This tool prevents us from treating failed-bundle evidence as installation evidence, or treating file presence alone as a complete bundle lifecycle.

## MS-012F status model

```text
target files exist + installed archive exists + installed receipt exists
→ installed_verified

target files exist + failed evidence exists + installed archive missing
→ conflicted

target files exist + installed archive missing
→ files_present_but_archive_missing

failed evidence exists + target files missing
→ failed_only
```

## Default MS-012F check

```text
python tools/bundle_lifecycle_reconcile.py \
  --subject data/lifecycle/ms012f-lifecycle-subject-v1.json \
  --policy data/lifecycle/bundle-lifecycle-reconciliation-policy-v1.json \
  --out-dir lifecycle_reports
```
