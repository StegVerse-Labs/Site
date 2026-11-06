set -euo pipefail
git restore --worktree --staged -- data/va-claim-assistant/governed-product-goals-validation.json
test -z "$(git status --porcelain -- data/va-claim-assistant/governed-product-goals-validation.json)"
echo 'VA_GOVERNED_PRODUCT_GOALS_REPOSITORY_WRITEBACK=NONE'
echo 'VA_GOVERNED_PRODUCT_GOALS_ARTIFACT_CUSTODY=NONE'
