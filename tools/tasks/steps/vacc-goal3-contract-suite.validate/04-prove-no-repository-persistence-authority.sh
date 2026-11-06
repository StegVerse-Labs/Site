set -euo pipefail
test -z "$(git status --porcelain -- data/va-claim-assistant/vacc-goal3-contract-suite-validation-receipt.json)"
echo 'VACC_GOAL3_CONTRACT_REPOSITORY_WRITEBACK=NONE'
echo 'VACC_GOAL3_CONTRACT_ARTIFACT_CUSTODY=NONE'
