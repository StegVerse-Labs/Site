set -euo pipefail
python3 scripts/process_va_private_document_fixture.py \
  data/va-claim-assistant/fixtures/private-document-intake.json \
  "$PRIVATE_DOCUMENT_RECEIPT"
test -s "$PRIVATE_DOCUMENT_RECEIPT"
