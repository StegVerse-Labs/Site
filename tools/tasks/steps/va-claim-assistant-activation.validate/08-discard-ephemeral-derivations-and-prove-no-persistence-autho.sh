set -euo pipefail
git checkout -- \
  data/va-claim-assistant/activation-gates.json \
  data/va-claim-assistant/governance-validation-receipt.json \
  data/va-claim-assistant/source-grounded-activation-receipt.json
test -z "$(git status --porcelain -- data/va-claim-assistant/activation-gates.json data/va-claim-assistant/governance-validation-receipt.json data/va-claim-assistant/source-grounded-activation-receipt.json)"
echo 'VA_SOURCE_GROUNDED_REPOSITORY_WRITEBACK=NONE'
echo 'VA_SOURCE_GROUNDED_ARTIFACT_CUSTODY=NONE'
