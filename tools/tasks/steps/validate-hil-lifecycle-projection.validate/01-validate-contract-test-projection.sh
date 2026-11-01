python scripts/validate_hil_lifecycle_projection.py \
  tests/fixtures/hil-site-lifecycle-projection.contract-test.json \
  --expected-response-sha256 1442c8407e6de8c66d1aa6d5180779a4c58cb449a46338bc9dae07e5ddf99285 \
  | tee hil-site-projection-validation.json
